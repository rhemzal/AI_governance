"""Disposable controls for Superpowers task-done limits (audit 2026-11-04)."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TASK_DONE = ROOT / "vendor/superpowers/v7.0.1/skills/executing-plans/scripts/task-done"


class SuperpowersTaskDoneLimits(unittest.TestCase):
    def test_failure_keeps_log_without_a_completion_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            base, ledger = _prepare_plan(adopter)
            result = _run_task_done(adopter, base, ["exit", "7"])
            self.assertEqual(result.returncode, 7, result.stdout + result.stderr)
            if ledger.exists():
                self.assertNotIn("Task 1: complete", ledger.read_text(encoding="utf-8"))
            log = adopter / ".superpowers/sdd/plan/task-1-tests.log"
            self.assertTrue(log.is_file())

    def test_success_appends_a_completion_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            base, ledger = _prepare_plan(adopter)
            result = _run_task_done(adopter, base, ["printf", "ok\\n"])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Task 1: complete", ledger.read_text(encoding="utf-8"))

    def test_true_is_accepted_without_command_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            base, ledger = _prepare_plan(adopter)
            result = _run_task_done(adopter, base, ["true"])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            text = ledger.read_text(encoding="utf-8")
            self.assertIn("Task 1: complete", text)
            self.assertIn("(no output)", text)

    def test_dirty_tree_does_not_change_the_recorded_head_range(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            base, ledger = _prepare_plan(adopter)
            first = _run_task_done(adopter, base, ["true"])
            self.assertEqual(first.returncode, 0)
            line_before = [line for line in ledger.read_text(encoding="utf-8").splitlines() if "Task 1:" in line][0]
            (adopter / "dirty.txt").write_text("untracked\n", encoding="utf-8")
            second = _run_task_done(adopter, base, ["true"])
            self.assertEqual(second.returncode, 0)
            line_after = [line for line in ledger.read_text(encoding="utf-8").splitlines() if "Task 1:" in line][-1]
            self.assertEqual(line_before, line_after)


def _prepare_plan(adopter: Path):
    subprocess.run(["git", "init", "-q"], cwd=adopter, check=True)
    subprocess.run(["git", "config", "user.email", "probe@example.com"], cwd=adopter, check=True)
    subprocess.run(["git", "config", "user.name", "probe"], cwd=adopter, check=True)
    plan = adopter / "plan.md"
    plan.write_text("# plan\n", encoding="utf-8")
    subprocess.run(["git", "add", "plan.md"], cwd=adopter, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=adopter, check=True)
    base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=adopter, text=True).strip()
    ledger = adopter / ".superpowers/sdd/plan/progress.md"
    return base, ledger


def _run_task_done(adopter: Path, base: str, command):
    plan = adopter / "plan.md"
    argv = ["bash", str(TASK_DONE), str(plan), "1", base, "--", *command]
    env = os.environ.copy()
    return subprocess.run(
        argv,
        cwd=adopter,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )


if __name__ == "__main__":
    unittest.main()
