"""Spec-gates Git environment controls (audit 2026-11-04)."""

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC_GATE = ROOT / ".specify/gates/lib/spec-gate.sh"


class SpecGatesGitEnvironment(unittest.TestCase):
    def test_projected_blocks_unset_git_repository_variables(self):
        spec_gate = SPEC_GATE.read_text(encoding="utf-8")
        watch = (ROOT / ".specify/gates/lib/watch.sh").read_text(encoding="utf-8")
        self.assertIn("gates_git_env_clear", spec_gate)
        self.assertIn("GIT_DIR", watch)
        self.assertIn("GATES_GIT_INDEX_FILE", (ROOT / ".specify/gates/verify.sh").read_text(encoding="utf-8"))

    def test_inherited_git_dir_misdirects_an_uncleared_child_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp) / "parent"
            child = Path(tmp) / "child"
            parent.mkdir()
            child.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=parent, check=True)
            subprocess.run(["git", "init", "-q"], cwd=child, check=True)
            parent_git = subprocess.check_output(
                ["git", "-C", str(parent), "rev-parse", "--absolute-git-dir"],
                text=True,
            ).strip()
            child_git = subprocess.check_output(
                ["git", "-C", str(child), "rev-parse", "--absolute-git-dir"],
                text=True,
            ).strip()
            inherited = subprocess.run(
                [
                    "bash",
                    "-lc",
                    f'cd "{child}" && GIT_DIR="{parent_git}" git rev-parse --absolute-git-dir',
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(inherited.returncode, 0)
            self.assertEqual(inherited.stdout.strip(), parent_git)
            self.assertNotEqual(inherited.stdout.strip(), child_git)

    def test_cleared_block_environment_reports_the_child_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp) / "parent"
            child = Path(tmp) / "child"
            parent.mkdir()
            child.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=parent, check=True)
            subprocess.run(["git", "init", "-q"], cwd=child, check=True)
            parent_git = subprocess.check_output(
                ["git", "-C", str(parent), "rev-parse", "--absolute-git-dir"],
                text=True,
            ).strip()
            child_git = subprocess.check_output(
                ["git", "-C", str(child), "rev-parse", "--absolute-git-dir"],
                text=True,
            ).strip()
            cleared = subprocess.run(
                [
                    "bash",
                    "-lc",
                    (
                        f'export GIT_DIR="{parent_git}" && cd "{child}" && '
                        "env -u GIT_DIR -u GIT_INDEX_FILE git rev-parse --absolute-git-dir"
                    ),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(cleared.returncode, 0)
            self.assertEqual(cleared.stdout.strip(), child_git)


class SpecGatesUpgradePin(unittest.TestCase):
    def test_install_script_pins_v0_5_1(self):
        script = (ROOT / "governance/experimental/spec_gates/install-and-project.sh").read_text(
            encoding="utf-8"
        )
        self.assertRegex(script, r"SPEC_GATES_TAG=v0\.5\.1")


if __name__ == "__main__":
    unittest.main()
