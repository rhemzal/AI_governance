"""Smoke checks for the adopter opt-in stack installer template."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INSTALLER = ROOT / "governance/experimental/spec_gates/install-opt-in-stack.sh"


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
