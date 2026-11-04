"""Disposable controls for vendored Superpowers helper scripts (v7.0.2 pin).

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
"""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TASK_BRIEF = ROOT / "vendor/superpowers/v7.0.2/skills/subagent-driven-development/scripts/task-brief"
SDD_WORKSPACE = ROOT / "vendor/superpowers/v7.0.2/skills/subagent-driven-development/scripts/sdd-workspace"


class SuperpowersHelperControls(unittest.TestCase):
    def test_task_brief_distinguishes_task_6_from_6b(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "tasks.md"
            plan.write_text("## Task 6\nMARKER-6\n\n## Task 6b\nMARKER-6B\n", encoding="utf-8")
            out = Path(tmp) / "out.md"
            proc = subprocess.run(
                ["bash", str(TASK_BRIEF), str(plan), "6", str(out)],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            text = out.read_text(encoding="utf-8")
            self.assertIn("MARKER-6", text)
            self.assertNotIn("MARKER-6B", text)

    def test_task_brief_matches_a1_not_a2(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "tasks.md"
            plan.write_text("## Task A1\nMARKER-A1\n\n## Task A2\nMARKER-A2\n", encoding="utf-8")
            out = Path(tmp) / "out.md"
            proc = subprocess.run(
                ["bash", str(TASK_BRIEF), str(plan), "A1", str(out)],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            text = out.read_text(encoding="utf-8")
            self.assertIn("MARKER-A1", text)
            self.assertNotIn("MARKER-A2", text)

    def test_task_brief_rejects_unclosed_fence_before_next_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "tasks.md"
            plan.write_text("## Task 6\nMARKER-6\n```\n\n## Task 7\nMARKER-7\n", encoding="utf-8")
            out = Path(tmp) / "out.md"
            proc = subprocess.run(
                ["bash", str(TASK_BRIEF), str(plan), "6", str(out)],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(proc.returncode, 4, proc.stdout + proc.stderr)
            self.assertFalse(out.exists())

    def test_sdd_workspace_refuses_outside_git_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp)
            plan = outside / "plan.md"
            plan.write_text("## Task 1\nx\n", encoding="utf-8")
            proc = subprocess.run(
                ["bash", str(SDD_WORKSPACE), str(plan)],
                cwd=outside,
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            self.assertFalse((outside / ".superpowers").exists())


if __name__ == "__main__":
    unittest.main()
