#!/usr/bin/env python3
"""Merge kit Cursor hooks and workflow registry entries into host files.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _refuse_symlink(path: Path) -> None:
    if path.is_symlink():
        raise SystemExit(f"install-opt-in-stack: refusing to update symlinked {path}")


def _load_object(path: Path) -> dict | None:
    _refuse_symlink(path)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"install-opt-in-stack: refusing to replace invalid JSON {path}: {exc}"
        ) from exc
    if not isinstance(data, dict):
        raise SystemExit(f"install-opt-in-stack: refusing to replace non-object JSON {path}")
    return data


def _write_object(path: Path, data: dict) -> None:
    _refuse_symlink(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(payload, encoding="utf-8")
    temporary.replace(path)


def merge_hooks(host_path: Path, kit_path: Path) -> None:
    kit = json.loads(kit_path.read_text(encoding="utf-8"))
    host = _load_object(host_path)
    if host is None:
        host = {"version": kit.get("version", 1), "hooks": {}}
    hooks = host.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise SystemExit(f"install-opt-in-stack: refusing to replace hooks in {host_path}")
    for event, entries in (kit.get("hooks") or {}).items():
        current = hooks.setdefault(event, [])
        if not isinstance(current, list):
            raise SystemExit(
                f"install-opt-in-stack: refusing to replace hook event {event} in {host_path}"
            )
        if not isinstance(entries, list):
            raise SystemExit(f"install-opt-in-stack: kit hook event {event} is not a list")
        for item in entries:
            command = item.get("command") if isinstance(item, dict) else None
            match = None
            if command is not None:
                match = next(
                    (
                        existing
                        for existing in current
                        if isinstance(existing, dict) and existing.get("command") == command
                    ),
                    None,
                )
            if match is None:
                current.append(item)
            elif match != item:
                print(f"install-opt-in-stack: keeping existing hook {command}")
    _write_object(host_path, host)


def merge_workflows(host_path: Path, kit_path: Path) -> None:
    kit = json.loads(kit_path.read_text(encoding="utf-8"))
    host = _load_object(host_path)
    if host is None:
        host = {"schema_version": kit.get("schema_version", "1.0"), "workflows": {}}
    workflows = host.setdefault("workflows", {})
    if not isinstance(workflows, dict):
        raise SystemExit(
            f"install-opt-in-stack: refusing to replace workflows in {host_path}"
        )
    for key, value in (kit.get("workflows") or {}).items():
        if key not in workflows:
            workflows[key] = value
        elif workflows[key] != value:
            print(f"install-opt-in-stack: keeping existing workflow {key}")
    _write_object(host_path, host)


def main(argv: list[str]) -> int:
    if len(argv) != 4 or argv[1] not in {"hooks", "workflows"}:
        raise SystemExit("usage: preserve_host_stack.py hooks|workflows HOST KIT")
    host = Path(argv[2])
    kit = Path(argv[3])
    if argv[1] == "hooks":
        merge_hooks(host, kit)
    else:
        merge_workflows(host, kit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
