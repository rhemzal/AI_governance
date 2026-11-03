"""Schema version 1 does not check that a method rationale is present.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
Python standard library. The plan is data; its commands are not executed.
"""

import importlib.util
import json
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "validate_aep.py"
SPEC = importlib.util.spec_from_file_location("validate_aep_method", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def plan():
    return {
        "schema_version": 1,
        "status": "READY",
        "objective": "Correct the README adoption example.",
        "discovery": ["Read README.md."],
        "risk": "LOW",
        "scope": {
            "paths": ["README.md"],
            "allowed_effects": ["edit working branch"],
            "approval_required": ["merge"],
        },
        "steps": [{
            "paths": ["README.md"],
            "action": "Correct the example",
            "reason": "Match the documented command",
        }],
        "verification": [{"command": "git diff --check", "expected": "exit 0"}],
        "acceptance": ["Example matches the documented command."],
        "blocking_questions": [],
        "budget": {"max_repair_attempts": 2, "on_exhaustion": "Report blocker and evidence."},
        "doc_delta": "README example corrected.",
    }


def body(value):
    return "```aep\n" + json.dumps(value) + "\n```\n"


class MethodRationale(unittest.TestCase):
    def test_ready_plan_without_a_method_comparison_passes(self):
        declared = plan()
        self.assertNotIn("method", declared)
        message = VALIDATOR.validate_body(body(declared), 1)
        self.assertIn("PASS: READY", message)
        self.assertIn("still require review", message)
        declared["discovery"] = []
        with self.assertRaises(VALIDATOR.InvalidPlan):
            VALIDATOR.validate_body(body(declared), 1)
