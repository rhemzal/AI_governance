"""Smoke checks for the adopter opt-in stack installer template."""

import json
import os
import shlex
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

    def test_stack_preserves_host_configuration_and_leaves_sandbox_unchanged(self):
        candidate = (
            ROOT
            / "governance/experimental/spec_gates/templates/autonomous-aep-execution.mdc.template"
        )
        with tempfile.TemporaryDirectory(dir=str(ROOT.parent)) as tmp:
            root = Path(tmp)
            kit = root / "kit"
            subprocess.run(
                ["git", "clone", "--local", str(ROOT), str(kit)],
                check=True,
                timeout=60,
            )
            revision = subprocess.check_output(
                ["git", "-C", str(kit), "rev-parse", "HEAD"],
                text=True,
                timeout=15,
            ).strip()
            preserved = self._install_stack_twice(
                root / "preserved",
                kit,
                revision,
                host_configuration=True,
            )
            fresh = self._install_stack_twice(
                root / "fresh",
                kit,
                revision,
                host_configuration=False,
            )

            adopter = preserved["adopter"]
            hooks = json.loads(
                (adopter / ".cursor/hooks.json").read_text(encoding="utf-8")
            )
            commands = [
                (event, entry.get("command"))
                for event, entries in hooks["hooks"].items()
                for entry in entries
            ]
            self.assertEqual(commands.count(("stop", ".cursor/hooks/host-stop.sh")), 1)
            self.assertEqual(
                commands.count(("afterFileEdit", ".cursor/hooks/host-after-edit.sh")),
                1,
            )
            self.assertEqual(
                commands.count(("stop", ".cursor/hooks/kit-verify-stop.sh")),
                1,
            )
            host_stop = next(
                entry
                for entry in hooks["hooks"]["stop"]
                if entry.get("command") == ".cursor/hooks/host-stop.sh"
            )
            self.assertEqual(host_stop["timeout"], 30)
            registry = json.loads(
                (adopter / ".specify/workflows/workflow-registry.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                registry["workflows"]["host-release"]["description"],
                "HOST-WORKFLOW-SENTINEL",
            )
            self.assertIn("ai-governance", registry["workflows"])
            self.assertEqual(
                (adopter / ".cursor/skills/governed-work/SKILL.md").read_text(
                    encoding="utf-8"
                ),
                "HOST-SKILL-SENTINEL\n",
            )
            self.assertEqual(
                (adopter / ".cursor/rules/autonomous-aep-execution.mdc").read_text(
                    encoding="utf-8"
                ),
                "HOST-RULE-SENTINEL\n",
            )
            self.assertEqual(
                (
                    adopter / ".specify/workflows/ai-governance/workflow.yml"
                ).read_text(encoding="utf-8"),
                "HOST-WORKFLOW-YML\n",
            )
            self.assertEqual(
                subprocess.check_output(
                    ["bash", str(adopter / ".cursor/hooks/host-stop.sh")],
                    text=True,
                    timeout=15,
                ),
                "HOST-STOP\n",
            )
            output = preserved["output"]
            self.assertNotIn("sandbox disabled", output.casefold())
            self.assertIn("leaving the Cursor sandbox choice to the operator", output)
            self.assertFalse(preserved["agent_log"].exists())

            installed_rule = (
                fresh["adopter"] / ".cursor/rules/autonomous-aep-execution.mdc"
            ).read_text(encoding="utf-8")
            candidate_text = candidate.read_text(encoding="utf-8")
            self.assertIn("After each milestone", candidate_text)
            self.assertNotEqual(installed_rule, candidate_text)
            self.assertNotIn("After each milestone", installed_rule)
            self.assertIn("Do not require", installed_rule)
            self.assertFalse(fresh["agent_log"].exists())

            linked = root / "linked-wrapper"
            linked.mkdir()
            outside = root / "outside-acceptance.sh"
            outside.write_text("OUTSIDE\n", encoding="utf-8")
            command = linked / "ci/adopter_task_acceptance_cmd.sh"
            command.parent.mkdir(parents=True)
            command.symlink_to(outside)
            gates = linked / ".specify/gates"
            gates.mkdir(parents=True)
            (gates / "verify.sh").write_text("exit 0\n", encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=linked, check=True, timeout=15)
            env = os.environ.copy()
            env["PATH"] = (
                f"{self._command_stubs(root / 'linked-bin', root / 'linked-agent.log')}:"
                f"{env['PATH']}"
            )
            env["KIT_SOURCE"] = str(kit)
            env["KIT_REVISION"] = revision
            env["ADOPTER_VERIFY_COMMAND"] = "printf ok"
            env["SKIP_SPEC_GATES"] = "1"
            env.pop("TASK_ACCEPTANCE_CMD", None)
            refused = subprocess.run(
                ["bash", str(INSTALLER), "--stack-only"],
                cwd=linked,
                env=env,
                text=True,
                capture_output=True,
                timeout=180,
            )
            self.assertNotEqual(refused.returncode, 0, refused.stdout + refused.stderr)
            self.assertIn("symlink", refused.stderr.casefold())
            self.assertEqual(outside.read_text(encoding="utf-8"), "OUTSIDE\n")
            self.assertTrue(command.is_symlink())

    def test_preserve_host_stack_merges_once_and_refuses_unsafe_host_files(self):
        helper = ROOT / "governance/experimental/spec_gates/preserve_host_stack.py"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kit_hooks = root / "kit-hooks.json"
            kit_hooks.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "hooks": {
                            "stop": [
                                {"command": ".cursor/hooks/kit-verify-stop.sh", "timeout": 150}
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            host_hooks = root / "hooks.json"
            host_hooks.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "hooks": {
                            "stop": [{"command": ".cursor/hooks/host-stop.sh", "timeout": 30}],
                            "afterFileEdit": [{"command": ".cursor/hooks/host-after-edit.sh"}],
                        },
                    }
                ),
                encoding="utf-8",
            )
            for _ in range(2):
                merged = subprocess.run(
                    ["python3", str(helper), "hooks", str(host_hooks), str(kit_hooks)],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)
            text = host_hooks.read_text(encoding="utf-8")
            self.assertEqual(text.count(".cursor/hooks/host-stop.sh"), 1)
            self.assertEqual(text.count(".cursor/hooks/kit-verify-stop.sh"), 1)
            self.assertEqual(text.count("host-after-edit.sh"), 1)

            same_command = root / "same-command.json"
            same_command.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "hooks": {
                            "stop": [
                                {
                                    "command": ".cursor/hooks/kit-verify-stop.sh",
                                    "timeout": 5,
                                }
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            kept = subprocess.run(
                ["python3", str(helper), "hooks", str(same_command), str(kit_hooks)],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(kept.returncode, 0, kept.stdout + kept.stderr)
            kept_hooks = json.loads(same_command.read_text(encoding="utf-8"))
            self.assertEqual(kept_hooks["hooks"]["stop"], [
                {"command": ".cursor/hooks/kit-verify-stop.sh", "timeout": 5}
            ])
            self.assertIn("keeping existing hook", kept.stdout)

            kit_registry = root / "kit-registry.json"
            kit_registry.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "workflows": {
                            "ai-governance": {"name": "Kit"},
                            "speckit": {"name": "Spec"},
                        },
                    }
                ),
                encoding="utf-8",
            )
            host_registry = root / "registry.json"
            host_registry.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "workflows": {
                            "host-release": {"name": "Host"},
                            "ai-governance": {"name": "Local"},
                        },
                    }
                ),
                encoding="utf-8",
            )
            registry_merge = subprocess.run(
                [
                    "python3",
                    str(helper),
                    "workflows",
                    str(host_registry),
                    str(kit_registry),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(
                registry_merge.returncode, 0, registry_merge.stdout + registry_merge.stderr
            )
            workflows = json.loads(host_registry.read_text(encoding="utf-8"))["workflows"]
            self.assertEqual(workflows["host-release"]["name"], "Host")
            self.assertEqual(workflows["ai-governance"]["name"], "Local")
            self.assertEqual(workflows["speckit"]["name"], "Spec")
            self.assertIn("keeping existing workflow ai-governance", registry_merge.stdout)

            invalid = root / "invalid.json"
            invalid.write_text("{", encoding="utf-8")
            refused = subprocess.run(
                ["python3", str(helper), "hooks", str(invalid), str(kit_hooks)],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("invalid JSON", refused.stderr)
            self.assertEqual(invalid.read_text(encoding="utf-8"), "{")

            outside = root / "outside.json"
            outside.write_text('{"outside": true}\n', encoding="utf-8")
            linked = root / "linked.json"
            linked.symlink_to(outside)
            symlink = subprocess.run(
                ["python3", str(helper), "workflows", str(linked), str(kit_hooks)],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertNotEqual(symlink.returncode, 0)
            self.assertIn("symlink", symlink.stderr.casefold())
            self.assertEqual(outside.read_text(encoding="utf-8"), '{"outside": true}\n')
            self.assertTrue(linked.is_symlink())

    def _install_stack_twice(self, adopter, kit, revision, host_configuration):
        adopter.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=adopter, check=True, timeout=15)
        agent_log = adopter.parent / f"{adopter.name}-agent.log"
        if host_configuration:
            self._seed_host_configuration(adopter)
        gates = adopter / ".specify/gates"
        gates.mkdir(parents=True)
        (gates / "verify.sh").write_text("exit 0\n", encoding="utf-8")
        env = os.environ.copy()
        env["PATH"] = f"{self._command_stubs(adopter.parent / f'{adopter.name}-bin', agent_log)}:{env['PATH']}"
        env["KIT_SOURCE"] = str(kit)
        env["KIT_REVISION"] = revision
        env["ADOPTER_VERIFY_COMMAND"] = "printf ok"
        env["SKIP_SPEC_GATES"] = "1"
        env["DISPLAY"] = ":99"
        env.pop("TASK_ACCEPTANCE_CMD", None)
        env.pop("TASK_ACCEPTANCE_EVIDENCE", None)
        env.pop("TASK_ACCEPTANCE_LOG", None)
        output = []
        for _ in range(2):
            result = subprocess.run(
                ["bash", str(INSTALLER), "--stack-only"],
                cwd=adopter,
                env=env,
                text=True,
                capture_output=True,
                timeout=180,
            )
            output.append(result.stdout + result.stderr)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return {
            "adopter": adopter,
            "agent_log": agent_log,
            "output": "\n".join(output),
        }

    def _seed_host_configuration(self, adopter):
        hooks = adopter / ".cursor/hooks"
        hooks.mkdir(parents=True)
        (hooks / "host-stop.sh").write_text(
            "#!/bin/sh\nprintf 'HOST-STOP\\n'\n", encoding="utf-8"
        )
        (hooks / "host-after-edit.sh").write_text(
            "#!/bin/sh\nprintf 'HOST-EDIT\\n'\n", encoding="utf-8"
        )
        (adopter / ".cursor/hooks.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "stop": [
                            {
                                "command": ".cursor/hooks/host-stop.sh",
                                "timeout": 30,
                            }
                        ],
                        "afterFileEdit": [
                            {"command": ".cursor/hooks/host-after-edit.sh"}
                        ],
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        skill = adopter / ".cursor/skills/governed-work"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("HOST-SKILL-SENTINEL\n", encoding="utf-8")
        rules = adopter / ".cursor/rules"
        rules.mkdir()
        (rules / "autonomous-aep-execution.mdc").write_text(
            "HOST-RULE-SENTINEL\n", encoding="utf-8"
        )
        workflow = adopter / ".specify/workflows/ai-governance"
        workflow.mkdir(parents=True)
        (workflow / "workflow.yml").write_text("HOST-WORKFLOW-YML\n", encoding="utf-8")
        (adopter / ".specify/workflows/workflow-registry.json").write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "workflows": {
                        "host-release": {
                            "name": "Host release",
                            "version": "1.0.0",
                            "description": "HOST-WORKFLOW-SENTINEL",
                            "source": "project",
                        }
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def _command_stubs(self, directory, agent_log):
        directory.mkdir()
        quoted = shlex.quote(str(agent_log))
        (directory / "agent").write_text(
            f"#!/bin/sh\nprintf '%s\\n' \"$*\" >> {quoted}\nexit 7\n",
            encoding="utf-8",
        )
        (directory / "uv").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        (directory / "curl").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        for name in ("agent", "uv", "curl"):
            (directory / name).chmod(0o755)
        return str(directory)
