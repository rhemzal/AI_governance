#!/usr/bin/env python3
"""Compute a content-aware identity for uncommitted working-tree changes.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).

Hashes porcelain status together with blob identities (or absent/link markers),
not status text alone. Two different edits to the same path yield different ids.
Symlinks contribute `link:<target>`; missing paths contribute `absent`. Returns
`clean`, `unknown`, or a 64-character hex digest.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


def _porcelain_entries(root: Path, data: bytes):
    i = 0
    n = len(data)
    while i < n:
        end = data.index(b"\0", i)
        entry = data[i:end]
        i = end + 1
        if len(entry) < 4:
            continue
        xy = entry[:2].decode("utf-8", errors="replace")
        path = entry[3:].decode("utf-8", errors="replace")
        orig = ""
        if "R" in xy or "C" in xy:
            if i >= n:
                break
            end = data.index(b"\0", i)
            orig = data[i:end].decode("utf-8", errors="replace")
            i = end + 1
        yield xy, path, orig


def _blob_marker(root: Path, rel: str) -> str:
    path = root / rel
    if path.is_symlink():
        target = path.readlink()
        return f"link:{target}"
    if path.is_file():
        proc = subprocess.run(
            ["git", "-C", str(root), "hash-object", "--no-filters", "--stdin-paths"],
            input=f"{rel}\n",
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
        return "hash-failed"
    if path.exists():
        return "other"
    return "absent"


def uncommitted_diff_identity(root: Path | None = None) -> str:
    root = root or Path.cwd()
    proc = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "status",
            "--porcelain=v1",
            "-z",
            "--untracked-files=all",
        ],
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        return "unknown"
    if not proc.stdout:
        return "clean"

    lines: list[str] = []
    for xy, path, orig in _porcelain_entries(root, proc.stdout):
        blob = _blob_marker(root, path)
        lines.append(f"{xy}\t{blob}\t{orig}\t{path}")

    if not lines:
        return "clean"

    lines.sort()
    payload = "\n".join(lines) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    print(uncommitted_diff_identity(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
