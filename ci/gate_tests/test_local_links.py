"""Offline check that tracked Markdown links resolve inside the repository.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
Network URLs are ignored. This is the local half of documentation gate D3.
"""

import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"```.*?```", re.S)


class LocalMarkdownLinks(unittest.TestCase):
    def test_tracked_markdown_links_resolve(self):
        files = subprocess.check_output(
            ["git", "ls-files", "*.md"],
            cwd=ROOT,
            text=True,
        ).splitlines()
        missing = []
        for relative in files:
            path = ROOT / relative
            text = FENCE.sub("", path.read_text(encoding="utf-8"))
            for match in LINK.finditer(text):
                target = match.group(1).split("#", 1)[0]
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                dest = (path.parent / target).resolve()
                try:
                    dest.relative_to(ROOT.resolve())
                except ValueError:
                    missing.append(f"{relative} -> {target}")
                    continue
                if not dest.exists():
                    missing.append(f"{relative} -> {target}")
        self.assertEqual(missing, [])
