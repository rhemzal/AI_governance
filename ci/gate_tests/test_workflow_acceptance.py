"""Workflow acceptance runner and governed-workflow shell verification.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
"""

from __future__ import annotations

import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "ci/run_task_acceptance_check.sh"
GOVERNED = ROOT / ".specify/workflows/ai-governance/workflow.yml"
PASS_FIXTURE = Path(__file__).resolve().parent / "fixtures/disposable_workflow_pass.yml"
FAIL_FIXTURE = Path(__file__).resolve().parent / "fixtures/disposable_workflow_fail.yml"


class WorkflowAcceptanceContract(unittest.TestCase):
    """Fast contract checks used as the kit-repo default acceptance command."""

    def test_contract_is_discoverable(self):
        self.assertTrue(RUNNER.is_file())


class RunTaskAcceptanceCheck(unittest.TestCase):
    def test_success_writes_evidence_and_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            _init_git(adopter)
            env = os.environ.copy()
            env["TASK_ACCEPTANCE_CMD"] = "printf 'ok\\n'"
            env["TASK_ACCEPTANCE_EVIDENCE"] = str(adopter / "evidence.md")
            result = subprocess.run(
                ["bash", str(RUNNER)],
                cwd=adopter,
                env=env,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            text = (adopter / "evidence.md").read_text(encoding="utf-8")
            self.assertIn("Task outcome: VERIFIED", text)
            self.assertIn("printf 'ok", text)
            self.assertIn("Result: exit 0", text)
            self.assertIn("@", text)
            self.assertTrue((adopter / "evidence.log").is_file())

    def test_failure_writes_blocked_outcome_and_preserves_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            _init_git(adopter)
            env = os.environ.copy()
            env["TASK_ACCEPTANCE_CMD"] = "exit 7"
            env["TASK_ACCEPTANCE_EVIDENCE"] = str(adopter / "evidence.md")
            result = subprocess.run(
                ["bash", str(RUNNER)],
                cwd=adopter,
                env=env,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(result.returncode, 7, result.stdout + result.stderr)
            text = (adopter / "evidence.md").read_text(encoding="utf-8")
            self.assertIn("Task outcome: BLOCKED", text)
            self.assertIn("Result: exit 7", text)

    def test_runner_refuses_a_no_op_acceptance_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            _init_git(adopter)
            env = os.environ.copy()
            env["TASK_ACCEPTANCE_CMD"] = "true"
            env["TASK_ACCEPTANCE_EVIDENCE"] = str(adopter / "evidence.md")
            result = subprocess.run(
                ["bash", str(RUNNER)],
                cwd=adopter,
                env=env,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertFalse((adopter / "evidence.md").exists())

    def test_dirty_tree_identity_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            _init_git(adopter)
            (adopter / "dirty.txt").write_text("x\n", encoding="utf-8")
            env = os.environ.copy()
            env["TASK_ACCEPTANCE_CMD"] = "printf 'ok\\n'"
            env["TASK_ACCEPTANCE_EVIDENCE"] = str(adopter / "evidence.md")
            subprocess.run(
                ["bash", str(RUNNER)],
                cwd=adopter,
                env=env,
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            text = (adopter / "evidence.md").read_text(encoding="utf-8")
            self.assertNotIn("Uncommitted diff identity (if any): clean", text)

    def test_dirty_tree_identity_reflects_file_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            _init_git(adopter)
            path = adopter / "dirty.txt"
            env_base = os.environ.copy()
            env_base["TASK_ACCEPTANCE_CMD"] = "printf 'ok\\n'"
            env_base["TASK_ACCEPTANCE_EVIDENCE"] = str(adopter / "evidence.md")

            def run_and_dirty_id(content: str) -> str:
                path.write_text(content, encoding="utf-8")
                env = env_base.copy()
                subprocess.run(
                    ["bash", str(RUNNER)],
                    cwd=adopter,
                    env=env,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                text = (adopter / "evidence.md").read_text(encoding="utf-8")
                match = re.search(
                    r"Uncommitted diff identity \(if any\): ([0-9a-f]{64}|clean|unknown)",
                    text,
                )
                self.assertIsNotNone(match, text)
                return match.group(1)  # type: ignore[union-attr]

            first = run_and_dirty_id("alpha\n")
            second = run_and_dirty_id("beta\n")
            self.assertNotEqual(first, second)
            self.assertNotEqual(first, "clean")
            self.assertNotEqual(second, "clean")

    def test_dirty_tree_identity_reflects_symlink_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            _init_git(adopter)
            link = adopter / "dirty.link"
            (adopter / "target-a").write_text("a\n", encoding="utf-8")
            (adopter / "target-b").write_text("b\n", encoding="utf-8")
            env_base = os.environ.copy()
            env_base["TASK_ACCEPTANCE_CMD"] = "printf 'ok\\n'"
            env_base["TASK_ACCEPTANCE_EVIDENCE"] = str(adopter / "evidence.md")

            def run_and_dirty_id(target: str) -> str:
                if link.exists() or link.is_symlink():
                    link.unlink()
                link.symlink_to(target)
                env = env_base.copy()
                subprocess.run(
                    ["bash", str(RUNNER)],
                    cwd=adopter,
                    env=env,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                text = (adopter / "evidence.md").read_text(encoding="utf-8")
                match = re.search(
                    r"Uncommitted diff identity \(if any\): ([0-9a-f]{64}|clean|unknown)",
                    text,
                )
                self.assertIsNotNone(match, text)
                return match.group(1)  # type: ignore[union-attr]

            first = run_and_dirty_id("target-a")
            second = run_and_dirty_id("target-b")
            self.assertNotEqual(first, second)


class SavedAcceptanceCommand(unittest.TestCase):
    def test_fresh_shell_records_saved_outcome_for_green_and_red(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = _adopter_with_runner(Path(tmp))
            _write_outcome_wrapper(adopter)
            (adopter / "ci/kit_maintenance_acceptance_cmd.sh").write_text(
                "#!/bin/sh\nprintf '%s\\n' \"printf 'kit-default\\\\n'\"\n",
                encoding="utf-8",
            )
            red = _run_acceptance(adopter)
            self.assertEqual(red.returncode, 1, red.stdout + red.stderr)
            red_text = _evidence(adopter)
            self.assertIn("Task outcome: BLOCKED", red_text)
            self.assertIn("Result: exit 1", red_text)
            self.assertIn("bash ci/adopter_task_acceptance_cmd.sh", red_text)
            self.assertNotIn("kit-default", red_text)

            (adopter / "outcome.txt").write_text("complete\n", encoding="utf-8")
            green = _run_acceptance(adopter)
            self.assertEqual(green.returncode, 0, green.stdout + green.stderr)
            green_text = _evidence(adopter)
            self.assertIn("Task outcome: VERIFIED", green_text)
            self.assertIn("Result: exit 0", green_text)

            (adopter / "outcome.txt").unlink()
            empty_verify = _run_acceptance(
                adopter, {"TASK_ACCEPTANCE_CMD": ""}, unset=False
            )
            self.assertEqual(
                empty_verify.returncode, 1, empty_verify.stdout + empty_verify.stderr
            )
            self.assertIn("Task outcome: BLOCKED", _evidence(adopter))

    def test_explicit_command_overrides_saved_wrapper(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = _adopter_with_runner(Path(tmp))
            _write_outcome_wrapper(adopter)
            result = _run_acceptance(
                adopter,
                {"TASK_ACCEPTANCE_CMD": "printf 'task-override\\n'"},
                unset=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            text = _evidence(adopter)
            self.assertIn("Task outcome: VERIFIED", text)
            self.assertIn("task-override", text)
            self.assertNotIn("adopter_task_acceptance_cmd.sh", text)

    def test_kit_default_is_used_only_when_no_saved_command_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = _adopter_with_runner(Path(tmp))
            (adopter / "ci/kit_maintenance_acceptance_cmd.sh").write_text(
                "#!/bin/sh\nprintf '%s\\n' \"printf 'kit-default\\\\n'\"\n",
                encoding="utf-8",
            )
            result = _run_acceptance(adopter)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            text = _evidence(adopter)
            self.assertIn("Task outcome: VERIFIED", text)
            self.assertIn("kit-default", text)

    def test_symlinked_saved_command_is_not_executed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            adopter = root / "adopter"
            adopter.mkdir()
            _adopter_with_runner(adopter)
            outside = root / "outside.sh"
            outside.write_text("#!/bin/sh\nprintf 'FOLLOWED\\n'\n", encoding="utf-8")
            outside.chmod(0o755)
            wrapper = adopter / "ci/adopter_task_acceptance_cmd.sh"
            wrapper.symlink_to(outside)
            result = _run_acceptance(adopter)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("symlink", result.stderr.casefold())
            self.assertFalse(_evidence_path(adopter).exists())
            self.assertNotIn("FOLLOWED", result.stdout + result.stderr)

    def test_failing_kit_default_does_not_record_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = _adopter_with_runner(Path(tmp))
            (adopter / "ci/kit_maintenance_acceptance_cmd.sh").write_text(
                "#!/bin/sh\nexit 3\n",
                encoding="utf-8",
            )
            result = _run_acceptance(adopter)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("no acceptance command is selected", result.stderr)
            self.assertFalse(_evidence_path(adopter).exists())

    def test_empty_kit_default_does_not_record_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = _adopter_with_runner(Path(tmp))
            (adopter / "ci/kit_maintenance_acceptance_cmd.sh").write_text(
                "#!/bin/sh\nexit 0\n",
                encoding="utf-8",
            )
            result = _run_acceptance(adopter)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("no acceptance command is selected", result.stderr)
            self.assertFalse(_evidence_path(adopter).exists())

    def test_missing_command_exits_before_writing_a_false_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = _adopter_with_runner(Path(tmp))
            result = _run_acceptance(adopter)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("no acceptance command is selected", result.stderr)
            self.assertFalse(_evidence_path(adopter).exists())


class GovernedWorkflowDefinition(unittest.TestCase):
    def test_verify_shell_step_follows_implement(self):
        text = GOVERNED.read_text(encoding="utf-8")
        self.assertIn("verify-acceptance", text)
        self.assertIn("type: shell", text)
        self.assertIn("bash ci/run_task_acceptance_check.sh", text)
        self.assertIn("verify:", text)
        self.assertIn("saved project command", text)
        self.assertRegex(
            text,
            r"id: implement[\s\S]*id: verify-acceptance",
        )
        self.assertNotIn("continue_on_error", text)

    def test_wrapper_delegates_to_canonical_runner(self):
        wrapper = ROOT / ".specify/scripts/bash/run-task-acceptance-check.sh"
        self.assertTrue(wrapper.is_file())
        body = wrapper.read_text(encoding="utf-8")
        self.assertIn("ci/run_task_acceptance_check.sh", body)


class DisposableShellWorkflowRunner(unittest.TestCase):
    def test_pass_probe_runs_marker_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            code = _run_shell_only_workflow(PASS_FIXTURE, cwd)
            self.assertEqual(code, 0)
            self.assertEqual((cwd / "marker.txt").read_text(encoding="utf-8"), "Executed\n")

    def test_fail_probe_stops_before_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            code = _run_shell_only_workflow(FAIL_FIXTURE, cwd)
            self.assertEqual(code, 7)
            self.assertFalse((cwd / "marker.txt").exists())


class SpecKitEngineShellProbe(unittest.TestCase):
    _venv_python: Path | None = None

    @classmethod
    def setUpClass(cls):
        if importlib.util.find_spec("specify_cli") is not None:
            cls._venv_python = Path(sys.executable)
            return
        base = Path(tempfile.mkdtemp(prefix="specify-cli-probe-"))
        venv = base / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True, timeout=120)
        pip = venv / "bin/pip"
        install = subprocess.run(
            [str(pip), "install", "-q", "specify-cli==1.2.5"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if install.returncode != 0:
            cls._venv_python = None
            return
        cls._venv_python = venv / "bin/python"

    @classmethod
    def tearDownClass(cls):
        if cls._venv_python and "specify-cli-probe-" in str(cls._venv_python):
            shutil.rmtree(cls._venv_python.parent.parent, ignore_errors=True)

    def setUp(self):
        if self._venv_python is None:
            self.skipTest("specify-cli 1.2.5 is not available for engine probe")

    def test_engine_pass_and_fail_probes(self):
        for fixture, expect_exit in (
            (PASS_FIXTURE, 0),
            (FAIL_FIXTURE, 7),
        ):
            with self.subTest(fixture=fixture.name):
                with tempfile.TemporaryDirectory() as tmp:
                    cwd = Path(tmp)
                    script = (
                        "from pathlib import Path\n"
                        "from specify_cli.workflows.engine import WorkflowEngine\n"
                        "from specify_cli.workflows.engine import WorkflowDefinition\n"
                        f"root = Path({str(cwd)!r})\n"
                        f"definition = WorkflowDefinition.from_yaml(Path({str(fixture)!r}))\n"
                        "engine = WorkflowEngine(root)\n"
                        "errors = engine.validate(definition)\n"
                        "if errors:\n"
                        "    raise SystemExit('validate: ' + '; '.join(errors))\n"
                        "state = engine.execute(definition, inputs={})\n"
                        "marker = root / 'marker.txt'\n"
                        "print(state.status.value)\n"
                        "print(marker.exists())\n"
                        "raise SystemExit(0 if state.status.value == 'completed' else 7)\n"
                    )
                    proc = subprocess.run(
                        [str(self._venv_python), "-c", script],
                        cwd=cwd,
                        check=False,
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )
                    self.assertEqual(proc.returncode, expect_exit, proc.stdout + proc.stderr)
                    lines = proc.stdout.strip().splitlines()
                    if expect_exit == 0:
                        self.assertEqual(lines[0], "completed")
                        self.assertEqual(lines[-1], "True")
                    else:
                        self.assertEqual(lines[0], "failed")
                        self.assertEqual(lines[-1], "False")
                        self.assertFalse((cwd / "marker.txt").exists())


def _adopter_with_runner(adopter: Path) -> Path:
    _init_git(adopter)
    ci = adopter / "ci"
    ci.mkdir()
    shutil.copy(RUNNER, ci / "run_task_acceptance_check.sh")
    shutil.copy(ROOT / "ci/uncommitted_diff_identity.py", ci / "uncommitted_diff_identity.py")
    return adopter


def _write_outcome_wrapper(adopter: Path) -> None:
    wrapper = adopter / "ci/adopter_task_acceptance_cmd.sh"
    wrapper.write_text(
        """#!/usr/bin/env bash
set -euo pipefail
test "$(cat outcome.txt 2>/dev/null || true)" = complete
""",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)


def _run_acceptance(adopter: Path, updates: dict | None = None, unset: bool = True):
    env = os.environ.copy()
    if unset:
        env.pop("TASK_ACCEPTANCE_CMD", None)
    if updates:
        env.update(updates)
    env.pop("TASK_ACCEPTANCE_EVIDENCE", None)
    env.pop("TASK_ACCEPTANCE_LOG", None)
    return subprocess.run(
        ["bash", "ci/run_task_acceptance_check.sh"],
        cwd=adopter,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )


def _evidence_path(adopter: Path) -> Path:
    return adopter / ".specify/acceptance-run-evidence.latest.md"


def _evidence(adopter: Path) -> str:
    return _evidence_path(adopter).read_text(encoding="utf-8")


def _init_git(adopter: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=adopter, check=True, timeout=30)
    subprocess.run(["git", "config", "user.email", "probe@example.com"], cwd=adopter, check=True)
    subprocess.run(["git", "config", "user.name", "probe"], cwd=adopter, check=True)
    (adopter / "README.md").write_text("probe\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=adopter, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=adopter, check=True)


def _run_shell_only_workflow(fixture: Path, cwd: Path) -> int:
    steps = []
    for block in fixture.read_text(encoding="utf-8").split("- id:")[1:]:
        if "type: shell" not in block:
            continue
        run_match = re.search(r'run: "([^"]*)"', block)
        if not run_match:
            run_match = re.search(r"run: '([^']*)'", block)
        if not run_match:
            raise AssertionError(f"missing run in {fixture}")
        steps.append(run_match.group(1))
    exit_code = 0
    for command in steps:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if proc.returncode != 0:
            return proc.returncode
    return exit_code


if __name__ == "__main__":
    unittest.main()
