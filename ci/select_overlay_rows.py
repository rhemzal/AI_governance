#!/usr/bin/env python3
"""Select LOCAL_OVERLAY table rows whose Load when matches touched paths.

Optional deterministic helper for agents and maintainers. It does not load
context into a model; it only filters overlay markdown tables.

Provenance: AI_governance (https://github.com/rhemzal/AI_governance).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def _split_table_line(line: str) -> list[str]:
    line = line.strip()
    if not line.startswith("|"):
        return []
    parts = [cell.strip() for cell in line.strip("|").split("|")]
    return parts


def _is_separator(parts: list[str]) -> bool:
    return bool(parts) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in parts)


def parse_overlay_table(text: str) -> list[dict[str, str]]:
    """Return table rows as dicts keyed by normalized header names."""
    rows: list[dict[str, str]] = []
    headers: list[str] | None = None
    for raw in text.splitlines():
        parts = _split_table_line(raw)
        if not parts:
            continue
        if _is_separator(parts):
            continue
        if headers is None:
            headers = [
                re.sub(r"\s+", "_", cell.strip().lower()) for cell in parts
            ]
            continue
        if len(parts) < len(headers):
            parts.extend([""] * (len(headers) - len(parts)))
        row = {headers[i]: parts[i] for i in range(len(headers))}
        rows.append(row)
    return rows


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip().lower()


def path_matches_load_when(path: str, load_when: str) -> bool:
    """Heuristic match between touched paths and Load when text."""
    norm = _normalize_path(path)
    lw = load_when.lower()
    if not lw or not norm:
        return False
    if norm in lw:
        return True
    for token in re.findall(r"[a-z0-9][a-z0-9_./-]*(?:\.[a-z0-9]+)?", lw):
        token = token.strip("./")
        if len(token) >= 8 and token in norm:
            return True
    if "import_bundle" in norm and "import_bundle" in lw:
        return True
    if ("copy" in norm or "/opt-in/" in f"/{norm}/") and (
        "copies" in lw or "symlink" in lw or "cp -a" in lw
    ):
        return True
    return False


def select_rows(overlay_text: str, paths: list[str]) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for row in parse_overlay_table(overlay_text):
        load_when = row.get("load_when") or row.get("load_when_column") or ""
        if not load_when:
            for key, value in row.items():
                if "load" in key and "when" in key:
                    load_when = value
                    break
        if any(path_matches_load_when(path, load_when) for path in paths):
            selected.append(row)
    return selected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--overlay",
        type=Path,
        required=True,
        help="Path to LOCAL_OVERLAY.md (or compatible table).",
    )
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        dest="paths",
        metavar="PATH",
        help="Touched file path (repeatable).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON array of selected rows.",
    )
    args = parser.parse_args(argv)
    if not args.paths:
        print("select_overlay_rows: at least one --path is required", file=sys.stderr)
        return 2
    try:
        text = args.overlay.read_text(encoding="utf-8")
    except OSError as error:
        print(f"select_overlay_rows: {error}", file=sys.stderr)
        return 2
    rows = select_rows(text, args.paths)
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
    else:
        for row in rows:
            constraint = row.get("constraint") or row.get("constraint_column") or ""
            load_when = row.get("load_when") or ""
            print(f"{constraint}\t{load_when}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
