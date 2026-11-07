#!/usr/bin/env python3
"""Install the opt-in VS Code Copilot hook and workspace route."""

import argparse
from pathlib import Path
import shutil


ROUTE_MARKER = "<!-- AI Governance Tier C route -->"


def install_file(source, destination):
    if not source.is_file():
        raise FileNotFoundError(f"required kit file is missing: {source}")
    if destination.exists() or destination.is_symlink():
        print(f"install-vscode-adapter: keeping existing {destination}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    print(f"install-vscode-adapter: installed {destination}")


def install_route(source, destination):
    if not source.is_file():
        raise FileNotFoundError(f"required kit file is missing: {source}")
    if destination.is_symlink():
        raise ValueError(f"refusing to update symlinked host instructions: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    existing = destination.read_text(encoding="utf-8") if destination.exists() else ""
    if ROUTE_MARKER in existing:
        print(f"install-vscode-adapter: keeping existing route in {destination}")
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    with destination.open("a", encoding="utf-8") as instructions:
        instructions.write(separator + source.read_text(encoding="utf-8"))
    print(f"install-vscode-adapter: appended the Tier C route to {destination}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True, help="Pinned AI_governance root")
    parser.add_argument("--root", type=Path, required=True, help="Adopter project root")
    args = parser.parse_args()
    source = args.source.resolve()
    root = args.root.resolve()

    install_file(
        source / ".github/hooks/kit-verify-stop.py",
        root / ".github/hooks/kit-verify-stop.py",
    )
    install_file(
        source / ".github/hooks/ai-governance.json",
        root / ".github/hooks/ai-governance.json",
    )
    install_file(
        source / ".github/skills/governed-work/SKILL.md",
        root / ".github/skills/governed-work/SKILL.md",
    )
    install_route(
        source
        / "governance/experimental/spec_gates/templates/copilot-instructions-opt-in.md.template",
        root / ".github/copilot-instructions.md",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
