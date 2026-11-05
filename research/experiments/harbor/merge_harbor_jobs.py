#!/usr/bin/env python3
"""Merge Harbor job trial directories after targeted retries.

Copies a base job to a new output directory, drops selected trial folders,
and adds replacement trials from an overlay job. Writes merge-provenance.json
for audit. Does not re-run graders or rewrite Harbor aggregate result.json.

Provenance: AI_governance (https://github.com/rhemzal/AI_governance).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


def _trial_dirs(job_dir: Path) -> dict[str, Path]:
    found = {}
    for child in sorted(job_dir.iterdir()):
        if not child.is_dir() or child.is_symlink():
            continue
        if (child / "result.json").is_file():
            found[child.name] = child
    return found


def merge(
    base: Path,
    overlay: Path,
    output: Path,
    *,
    drop: list[str],
    add: list[str],
    force: bool,
) -> Path:
    base = base.resolve()
    overlay = overlay.resolve()
    output = output.resolve()

    if not base.is_dir():
        raise ValueError(f"base is not a directory: {base}")
    if not overlay.is_dir():
        raise ValueError(f"overlay is not a directory: {overlay}")
    if output.exists():
        if not force:
            raise ValueError(f"output already exists: {output} (use --force)")
        shutil.rmtree(output)
    output.mkdir(parents=True)

    base_trials = _trial_dirs(base)
    overlay_trials = _trial_dirs(overlay)

    drop_set = set(drop)
    unknown_drop = sorted(drop_set - set(base_trials))
    if unknown_drop:
        raise ValueError(f"drop names not in base job: {', '.join(unknown_drop)}")

    add_set = set(add)
    unknown_add = sorted(add_set - set(overlay_trials))
    if unknown_add:
        raise ValueError(
            f"add names not in overlay job: {', '.join(unknown_add)}"
        )

    overlap = drop_set & add_set
    if overlap:
        raise ValueError(f"drop and add must differ; overlap: {sorted(overlap)}")

    for name, path in base_trials.items():
        if name in drop_set:
            continue
        shutil.copytree(path, output / name)

    for name in sorted(add_set):
        shutil.copytree(overlay_trials[name], output / name)

    for item in base.iterdir():
        if item.is_dir() and (item / "result.json").is_file():
            continue
        if item.is_file():
            shutil.copy2(item, output / item.name)

    provenance = {
        "base_job": str(base),
        "overlay_job": str(overlay),
        "output_job": str(output),
        "dropped_trials": sorted(drop_set),
        "added_trials": sorted(add_set),
    }
    (output / "merge-provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n",
        encoding="utf-8",
    )
    return output


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--drop",
        action="append",
        default=[],
        metavar="TRIAL_DIR",
        help="Trial directory name to omit from the base job (repeatable).",
    )
    parser.add_argument(
        "--add",
        action="append",
        default=[],
        metavar="TRIAL_DIR",
        help="Trial directory name to copy from the overlay job (repeatable).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing output directory.",
    )
    args = parser.parse_args(argv)
    if len(args.drop) != len(args.add):
        print(
            "merge_harbor_jobs: drop and add lists must have the same length",
            file=sys.stderr,
        )
        return 2
    try:
        merge(
            args.base,
            args.overlay,
            args.output,
            drop=args.drop,
            add=args.add,
            force=args.force,
        )
    except ValueError as error:
        print(f"merge_harbor_jobs: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
