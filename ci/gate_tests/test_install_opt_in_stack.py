"""Smoke checks for the adopter opt-in stack installer template."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INSTALLER = ROOT / "governance/experimental/spec_gates/install-opt-in-stack.sh"
STACK_CHECKER = ROOT / "governance/experimental/spec_gates/check-opt-in-stack.sh"
VSCODE_ADAPTER_INSTALLER = (
    ROOT / "governance/experimental/spec_gates/install-vscode-adapter.py"
)


class InstallOptInStackTemplate(unittest.TestCase):
    def test_installer_passes_bash_syntax_check(self):
        subprocess.run(["bash", "-n", str(INSTALLER)], check=True, cwd=ROOT)

    def test_adopter_policy_shape_from_embedded_generator(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "policy.adopter.json"
            subprocess.run(
                [
                    "python3",
                    "-",
                    str(out),
                    "adopter-verify",
                    "timeout 10s echo ok",
                    "15",
                ],
                input=b"""import json, sys
from pathlib import Path
out, gate_id, cmd, timeout_s = sys.argv[1:5]
data = {
    "hooks": {
        "verify-quality": {
            "orchestrator": "none",
            "severity": "error",
            "gates": {gate_id: {"command": cmd, "timeout_s": int(timeout_s)}},
        }
    },
    "git": {"block_main_commits": False},
    "spec": {"enabled": False},
    "attestation": {"enabled": True, "parity": "error"},
}
Path(out).write_text(json.dumps(data, indent=2) + "\\n", encoding="utf-8")
""",
                check=True,
                cwd=ROOT,
            )
            data = json.loads(out.read_text(encoding="utf-8"))
            gate = data["hooks"]["verify-quality"]["gates"]["adopter-verify"]
            self.assertEqual(gate["command"], "timeout 10s echo ok")
            self.assertEqual(gate["timeout_s"], 15)

    def test_example_policy_template_is_valid_json(self):
        example = (
            ROOT
            / "governance/experimental/spec_gates/templates/policy.adopter.template.json"
        )
        text = example.read_text(encoding="utf-8")
        text = text.replace("__GATE_ID__", "adopter-verify")
        text = text.replace('"__VERIFY_COMMAND__"', '"echo ok"')
        text = text.replace("__TIMEOUT_S__", "130")
        json.loads(text)

    def test_check_script_and_aep_rule_template_exist(self):
        check = ROOT / "governance/experimental/spec_gates/check-opt-in-stack.sh"
        rule = (
            ROOT
            / "governance/experimental/spec_gates/templates/autonomous-aep-execution.mdc.template"
        )
        self.assertTrue(check.is_file())
        self.assertTrue(rule.is_file())
        subprocess.run(["bash", "-n", str(check)], check=True, cwd=ROOT)
        self.assertIn("alwaysApply: true", rule.read_text(encoding="utf-8"))
        self.assertIn("run_task_acceptance_check.sh", rule.read_text(encoding="utf-8"))

    def test_vscode_adapter_installs_hook_and_copilot_route_idempotently(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            for _ in range(2):
                result = subprocess.run(
                    [
                        "python3",
                        str(VSCODE_ADAPTER_INSTALLER),
                        "--source",
                        str(ROOT),
                        "--root",
                        str(adopter),
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            hooks = adopter / ".github/hooks"
            config = json.loads((hooks / "ai-governance.json").read_text(encoding="utf-8"))
            self.assertIn("agentStop", config["hooks"])
            self.assertTrue((hooks / "kit-verify-stop.py").is_file())
            source_skill = ROOT / ".github/skills/governed-work/SKILL.md"
            copied_skill = adopter / ".github/skills/governed-work/SKILL.md"
            self.assertEqual(copied_skill.read_bytes(), source_skill.read_bytes())
            instructions = (adopter / ".github/copilot-instructions.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("AI Governance Tier C route", instructions)
            self.assertEqual(instructions.count("AI Governance Tier C route"), 1)

    def test_vscode_adapter_preserves_existing_host_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            hooks = adopter / ".github/hooks"
            hooks.mkdir(parents=True)
            instructions = adopter / ".github/copilot-instructions.md"
            instructions.write_text("HOST-COPILOT-SENTINEL\n", encoding="utf-8")
            skill = adopter / ".github/skills/governed-work/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("HOST-SKILL-SENTINEL\n", encoding="utf-8")
            (hooks / "ai-governance.json").write_text(
                '{"host":"config"}\n', encoding="utf-8"
            )
            (hooks / "custom.json").write_text('{"host":"custom"}\n', encoding="utf-8")

            result = subprocess.run(
                [
                    "python3",
                    str(VSCODE_ADAPTER_INSTALLER),
                    "--source",
                    str(ROOT),
                    "--root",
                    str(adopter),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            copilot_text = instructions.read_text(encoding="utf-8")
            self.assertTrue(copilot_text.startswith("HOST-COPILOT-SENTINEL\n"))
            self.assertIn("AI Governance Tier C route", copilot_text)
            self.assertEqual(skill.read_text(encoding="utf-8"), "HOST-SKILL-SENTINEL\n")
            self.assertEqual(
                (hooks / "ai-governance.json").read_text(encoding="utf-8"),
                '{"host":"config"}\n',
            )
            self.assertEqual(
                (hooks / "custom.json").read_text(encoding="utf-8"),
                '{"host":"custom"}\n',
            )

    def test_vscode_adapter_refuses_symlinked_host_instruction_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp) / "adopter"
            adopter.mkdir()
            outside = Path(tmp) / "outside.md"
            outside.write_text("OUTSIDE-SENTINEL\n", encoding="utf-8")
            instructions = adopter / ".github/copilot-instructions.md"
            instructions.parent.mkdir(parents=True)
            instructions.symlink_to(outside)

            result = subprocess.run(
                [
                    "python3",
                    str(VSCODE_ADAPTER_INSTALLER),
                    "--source",
                    str(ROOT),
                    "--root",
                    str(adopter),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr.casefold())
            self.assertEqual(outside.read_text(encoding="utf-8"), "OUTSIDE-SENTINEL\n")

    def test_stack_checker_distinguishes_configuration_from_native_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            installed = subprocess.run(
                [
                    "python3",
                    str(VSCODE_ADAPTER_INSTALLER),
                    "--source",
                    str(ROOT),
                    "--root",
                    str(adopter),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)

            result = subprocess.run(
                ["bash", str(STACK_CHECKER)],
                cwd=adopter,
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("VS Code Copilot agentStop hook configured", result.stdout)
            self.assertIn("native VS Code Copilot dispatch is unverified", result.stdout)
            self.assertNotIn("VS Code hook invocation log present", result.stdout)

    def test_stack_checker_rejects_inert_agent_stop_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            installed = subprocess.run(
                [
                    "python3",
                    str(VSCODE_ADAPTER_INSTALLER),
                    "--source",
                    str(ROOT),
                    "--root",
                    str(adopter),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)

            config_path = adopter / ".github/hooks/ai-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            hook = config["hooks"]["agentStop"][0]
            hook["bash"] = "echo kit-verify-stop.py"
            hook["powershell"] = "Write-Output kit-verify-stop.py"
            config_path.write_text(json.dumps(config), encoding="utf-8")

            result = subprocess.run(
                ["bash", str(STACK_CHECKER)],
                cwd=adopter,
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("no valid VS Code Copilot agentStop hook", result.stdout)
            self.assertNotIn("VS Code Copilot agentStop hook configured", result.stdout)

    def test_stack_checker_rejects_host_timeout_not_exceeding_verifier_timeout(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            installed = subprocess.run(
                [
                    "python3",
                    str(VSCODE_ADAPTER_INSTALLER),
                    "--source",
                    str(ROOT),
                    "--root",
                    str(adopter),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)

            config_path = adopter / ".github/hooks/ai-governance.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["hooks"]["agentStop"][0]["timeoutSec"] = 140
            config_path.write_text(json.dumps(config), encoding="utf-8")

            result = subprocess.run(
                ["bash", str(STACK_CHECKER)],
                cwd=adopter,
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("no valid VS Code Copilot agentStop hook", result.stdout)
            self.assertNotIn("VS Code Copilot agentStop hook configured", result.stdout)

    def test_vscode_hook_install_preserves_executable_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            installed = subprocess.run(
                [
                    "python3",
                    str(VSCODE_ADAPTER_INSTALLER),
                    "--source",
                    str(ROOT),
                    "--root",
                    str(adopter),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)

            hook = adopter / ".github/hooks/kit-verify-stop.py"
            self.assertTrue(hook.stat().st_mode & 0o111)

    def test_bootstrap_imports_snapshot_pin_and_host_files(self):
        with tempfile.TemporaryDirectory(dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            kit = root / "kit"
            adopter = root / "adopter"
            adopter.mkdir()
            subprocess.run(
                ["git", "clone", "--local", str(ROOT), str(kit)],
                check=True,
                timeout=60,
            )
            subprocess.run(["git", "init"], cwd=adopter, check=True, timeout=15)
            revision = subprocess.check_output(
                ["git", "-C", str(kit), "rev-parse", "HEAD"],
                text=True,
                timeout=15,
            ).strip()
            env = os.environ.copy()
            env["KIT_SOURCE"] = str(kit)
            env["KIT_REVISION"] = revision
            env["ADOPTER_VERIFY_COMMAND"] = "printf ok"
            env.pop("TASK_ACCEPTANCE_EVIDENCE", None)
            env.pop("TASK_ACCEPTANCE_LOG", None)
            first = subprocess.run(
                ["bash", str(INSTALLER), "--bootstrap"],
                cwd=adopter,
                env=env,
                text=True,
                capture_output=True,
                timeout=120,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertTrue((adopter / "vendor/AI_governance/kit-manifest.yml").is_file())
            self.assertTrue(
                (
                    adopter / "vendor/AI_governance/usage/ADOPTION_SCOPE_AND_HOSTS.md"
                ).is_file()
            )
            self.assertTrue(
                (
                    adopter
                    / "vendor/AI_governance/research/POST_INCIDENT_AGENT_HOST_BOUNDARY_20261105.md"
                ).is_file()
            )
            self.assertFalse(
                (adopter / "governance/experimental/spec_gates/install-opt-in-stack.sh").exists()
            )
            pin = adopter / "vendor/superpowers/v7.0.2"
            self.assertTrue((pin / "SHA256SUMS").is_file())
            skill = adopter / ".cursor/skills/governed-work/SKILL.md"
            self.assertTrue(skill.is_file())
            self.assertFalse(skill.is_symlink())
            overlay = (adopter / "governance/LOCAL_OVERLAY.md").read_text(encoding="utf-8")
            self.assertIn(revision, overlay)
            self.assertIn("printf ok", overlay)
            self.assertIn("does not sandbox", overlay.casefold())
            agents = (adopter / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(agents.count("## Governance baseline"), 1)
            self.assertIn(revision, agents)
            again = subprocess.run(
                ["bash", str(INSTALLER), "--bootstrap"],
                cwd=adopter,
                env=env,
                text=True,
                capture_output=True,
                timeout=120,
            )
            self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
            self.assertEqual(
                (adopter / "AGENTS.md").read_text(encoding="utf-8").count(
                    "## Governance baseline"
                ),
                1,
            )
            nested = subprocess.run(
                ["bash", str(INSTALLER), "--import-only"],
                cwd=ROOT,
                env={**env, "KIT_SOURCE": str(ROOT), "KIT_REVISION": revision},
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertNotEqual(nested.returncode, 0)
            self.assertIn("nest the kit", nested.stderr)
