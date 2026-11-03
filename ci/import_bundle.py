"""Copy a selected kit snapshot into a NEW directory, or verify an existing copy.

Read JSON converted from kit-manifest.yml by yq; never interpret imported code.
Source inventory comes from Git's index, contents from its current working tree.
Use a clean pinned checkout for an adoption record. Python standard library only.
"""

import argparse
import fnmatch
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys


class BundleError(ValueError):
    """Invalid selection, unsafe path, or incomplete snapshot."""


def relative_path(value, *, pattern=False):
    if not isinstance(value, str) or not value or any(c in value for c in "\\:\0\r\n\t"):
        raise BundleError(f"Invalid relative path: {value!r}")
    plain = value.rstrip("/")
    parts = PurePosixPath(plain)
    if not plain or parts.is_absolute() or ".." in parts.parts or str(parts) != plain:
        raise BundleError(f"Unsafe relative path: {value!r}")
    if not pattern and any(c in value for c in "*?["):
        raise BundleError(f"Bundle paths must be literal: {value!r}")
    return value


def resolve_paths(manifest, selected):
    if not isinstance(manifest, dict) or not isinstance(manifest.get("bundles"), dict):
        raise BundleError("Manifest must contain a bundles object")
    selected = set(selected)
    if len(selected & {"minimal", "standard", "full"}) != 1:
        raise BundleError("Select exactly one baseline: minimal, standard, or full")
    if "full" in selected and len(selected) != 1:
        raise BundleError("full already composes the optional bundles")
    visiting, done, paths = set(), set(), set()

    def visit(name):
        if name in visiting:
            raise BundleError(f"Bundle inheritance cycle: {name}")
        if name in done:
            return
        bundle = manifest["bundles"].get(name)
        if not isinstance(bundle, dict):
            raise BundleError(f"Unknown or invalid bundle: {name}")
        visiting.add(name)
        parents = bundle.get("composes", [])
        if not isinstance(parents, list) or any(not isinstance(x, str) for x in parents):
            raise BundleError(f"Invalid composes in {name}")
        if "extends" in bundle:
            if not isinstance(bundle["extends"], str):
                raise BundleError(f"Invalid extends in {name}")
            parents = parents + [bundle["extends"]]
        entries = bundle.get("paths")
        if not isinstance(entries, list):
            raise BundleError(f"Invalid paths in {name}")
        for entry in entries:
            paths.add(relative_path(entry))
        for parent in parents:
            visit(parent)
        visiting.remove(name)
        done.add(name)

    for name in sorted(selected):
        visit(name)
    excludes = manifest.get("exclude", [])
    if not isinstance(excludes, list):
        raise BundleError("exclude must be a list")
    return paths, [relative_path(x, pattern=True) for x in excludes]


def excluded(path, patterns):
    return any(
        (path == p.rstrip("/") or path.startswith(p)) if p.endswith("/")
        else fnmatch.fnmatchcase(path, p)
        for p in patterns
    )


def no_symlinks(path):
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise BundleError(f"Symlink path is not supported: {candidate}")


def snapshot(source, manifest, selected):
    source = Path(os.path.abspath(source))
    no_symlinks(source)
    paths, excludes = resolve_paths(manifest, selected)
    root = subprocess.run(["git", "-C", str(source), "rev-parse", "--show-toplevel"],
                          check=True, capture_output=True, text=True, timeout=15).stdout.strip()
    if Path(root).resolve() != source.resolve():
        raise BundleError("Source must be the root of the pinned kit checkout")
    raw = subprocess.run(["git", "-C", str(source), "ls-files", "--stage", "-z"],
                         check=True, capture_output=True, timeout=15).stdout
    inventory = {}
    for item in raw.split(b"\0"):
        if not item:
            continue
        metadata, name = item.decode("utf-8").split("\t", 1)
        mode, _oid, stage = metadata.split()
        inventory[name] = (mode, stage)
    names = set()
    for entry in sorted(paths):
        candidates = {p for p in inventory if p.startswith(entry)} if entry.endswith("/") else {entry} & inventory.keys()
        if not candidates:
            raise BundleError(f"Selected path has no tracked source content: {entry}")
        names.update(p for p in candidates if not excluded(p, excludes))
    if not names:
        raise BundleError("Selection contains no importable files")
    result = {}
    for name in sorted(names):
        relative_path(name)
        mode, stage = inventory[name]
        if mode not in ("100644", "100755") or stage != "0":
            raise BundleError(f"Not a regular, merged tracked file: {name}")
        path = source / name
        no_symlinks(path)
        if not path.is_file():
            raise BundleError(f"Missing selected source file: {name}")
        result[name] = (path.read_bytes(), int(mode[-3:], 8))
    return result, excludes


def verify_copy(destination, files, excludes):
    destination = Path(os.path.abspath(destination))
    no_symlinks(destination)
    if not destination.is_dir():
        raise BundleError(f"Missing imported directory: {destination}")
    actual = set()
    for path in destination.rglob("*"):
        name = path.relative_to(destination).as_posix()
        no_symlinks(path)
        if path.is_file() and not excluded(name, excludes):
            actual.add(name)
    missing, extra = files.keys() - actual, actual - files.keys()
    if missing or extra:
        raise BundleError(f"Imported file set differs: missing={sorted(missing)}, extra={sorted(extra)}")
    for name, (content, mode) in files.items():
        path = destination / name
        if path.read_bytes() != content:
            raise BundleError(f"Imported content differs from source: {name}")
        if os.name != "nt" and bool(path.stat().st_mode & 0o111) != bool(mode & 0o111):
            raise BundleError(f"Imported executable bit differs: {name}")


HOST_OWNED = (
    "AGENTS.md",
    ".github/copilot-instructions.md",
    "CHANGELOG.md",
    "DEVELOPMENT.md",
    "VERSIONING.md",
    "governance/LOCAL_OVERLAY.md",
)


def readopt_destination(project_root):
    """Choose a fresh snapshot path. Never replace an active snapshot or the project root."""
    project_root = Path(os.path.abspath(project_root))
    if not project_root.is_dir():
        raise BundleError(f"Missing project root: {project_root}")
    active = project_root / "vendor" / "AI_governance"
    staged = project_root / "vendor" / "AI_governance.next"
    if active.exists() and not active.is_dir():
        raise BundleError(f"Refusing non-directory snapshot path: {active}")
    chosen = staged if active.exists() else active
    if chosen.exists():
        raise BundleError(f"Refusing existing destination (even if empty): {chosen}")
    return chosen


def _adopted_bytes(project_root, name):
    active = project_root / "vendor" / "AI_governance" / name
    if active.is_file():
        return active.read_bytes()
    if name in HOST_OWNED or (project_root / "vendor" / "AI_governance").is_dir():
        return None
    root_file = project_root / name
    if root_file.is_file():
        return root_file.read_bytes()
    return None


def merge_readopt(project_root, new_files, previous=None):
    """Join a new snapshot with rules already in the project. Do not drop a local rule."""
    project_root = Path(os.path.abspath(project_root))
    previous = previous or {}
    merged = {}
    lines = ["# Re-adoption report", "",
             "Host-owned files were not modified. A local rule is kept when it differs",
             "from the new kit and the previous revision does not show it was unchanged.",
             ""]
    for name in HOST_OWNED:
        if (project_root / name).is_file():
            lines.append(f"- host file unchanged: {name}")
    for name, (new_content, mode) in sorted(new_files.items()):
        adopted = _adopted_bytes(project_root, name)
        base = previous.get(name)
        if adopted is None or adopted == new_content:
            merged[name] = (new_content, mode)
            if name in HOST_OWNED and (project_root / name).is_file():
                lines.append(f"- merge by hand: kit copy of {name} is in the new snapshot")
            continue
        if base is not None and adopted == base:
            merged[name] = (new_content, mode)
            lines.append(f"- took upstream: {name}")
        else:
            merged[name] = (adopted, mode)
            why = "previous revision unknown" if base is None else "both sides changed"
            lines.append(f"- kept local rule ({why}): {name}")
    old_root = project_root / "vendor" / "AI_governance"
    if old_root.is_dir():
        for path in old_root.rglob("*"):
            if path.is_file():
                name = path.relative_to(old_root).as_posix()
                if name not in new_files:
                    lines.append(f"- old snapshot file not in the new selection: {name}")
    elif (project_root / "constitution" / "AI_RULES.md").is_file():
        lines.append("- root-layout file left unchanged: constitution/AI_RULES.md")
    lines.append("")
    return merged, "\n".join(lines)


def _previous_files(source, revision, new_files):
    if len(revision) != 40 or any(character not in "0123456789abcdefABCDEF" for character in revision):
        raise BundleError("Previous revision must be a full 40-character SHA")
    found = {}
    for name in new_files:
        result = subprocess.run(
            ["git", "-C", str(source), "show", f"{revision}:{name}"],
            capture_output=True, timeout=15,
        )
        if result.returncode == 0:
            found[name] = result.stdout
    return found


def import_copy(source, destination, files, excludes):
    source, destination = Path(os.path.abspath(source)), Path(os.path.abspath(destination))
    no_symlinks(destination)
    if destination.exists():
        raise BundleError(f"Refusing existing destination (even if empty): {destination}")
    if destination.is_relative_to(source):
        raise BundleError("Destination must be outside the source checkout")
    # Validate/read the complete snapshot before this function. Reserve a fresh
    # directory exclusively; never replace, merge, delete, or repair a target.
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()
    for name, (content, mode) in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(content)
        path.chmod(mode)
    verify_copy(destination, files, excludes)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-json", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--bundle", action="append", required=True)
    parser.add_argument("--check", action="store_true", help="read-only comparison; do not copy")
    parser.add_argument("--readopt", action="store_true",
                        help="destination is the project root; merge into a new snapshot beside any existing one")
    parser.add_argument("--previous", default="",
                        help="full SHA of the previously imported kit revision, for a three-way join")
    args = parser.parse_args(argv)
    try:
        project_root = args.destination
        if args.readopt:
            args.destination = readopt_destination(args.destination)
        manifest = json.loads(args.manifest_json.read_text(encoding="utf-8"))
        files, excludes = snapshot(args.source, manifest, args.bundle)
        if args.readopt and not args.check:
            previous = _previous_files(args.source, args.previous, files) if args.previous else {}
            files, report = merge_readopt(project_root, files, previous)
            report_path = project_root / "vendor" / "AI_governance.readopt-report.md"
            if report_path.exists():
                raise BundleError(f"Refusing existing re-adoption report: {report_path}")
            import_copy(args.source, args.destination, files, excludes)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(report, encoding="utf-8")
        elif args.check:
            verify_copy(args.destination, files, excludes)
        else:
            import_copy(args.source, args.destination, files, excludes)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {'verified' if args.check else 'imported'} {len(files)} files; bundles={','.join(args.bundle)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
