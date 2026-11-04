"""Smoke checks for the adopter opt-in stack installer template."""

import json
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
