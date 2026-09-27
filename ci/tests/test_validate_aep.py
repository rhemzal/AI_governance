"""Regression cases for actual AEP gate failures and its trust boundary."""

import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "validate_aep.py"
SPEC = importlib.util.spec_from_file_location("validate_aep", SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def ready():
    return {
        "schema_version": 1,
        "status": "READY",
        "objective": "Correct the README adoption example.",
        "discovery": ["Read README.md and DEVELOPMENT.md; no runtime change."],
        "risk": "LOW",
        "scope": {"paths": ["README.md"], "allowed_effects": ["edit working branch"],
                  "approval_required": ["merge", "deploy"]},
        "steps": [{"paths": ["README.md"], "action": "Correct the example", "reason": "Match the documented command"}],
        "verification": [{"command": "git diff --check", "expected": "exit 0"}],
        "acceptance": ["Example matches the documented command; whitespace check passes."],
        "blocking_questions": [],
        "budget": {"max_repair_attempts": 2, "on_exhaustion": "Report blocker and evidence."},
        "doc_delta": "README example corrected; no runtime behavior change.",
    }


def body(plan):
    return "```aep\n" + json.dumps(plan) + "\n```\n"


class DeclarationTests(unittest.TestCase):
    def test_documentation_verification_is_not_limited_to_test_runner_names(self):
        self.assertIn("PASS: READY", validator.validate_body(body(ready()), 2))

    def test_unrelated_todo_and_words_inside_real_sentences_are_allowed(self):
        plan = ready()
        plan["objective"] = "Document TODO marker handling and /etc/config paths."
        self.assertIn("PASS", validator.validate_body(body(plan) + "\nRemoved the old TODO marker.\n"))

    def test_old_empty_fields_cannot_claim_readiness(self):
        with self.assertRaises(validator.InvalidPlan):
            validator.validate_body("AEP Status: READY\nObjective:\nSteps:\ntest command:\n", 2)

    def test_missing_and_empty_evidence_fields_fail(self):
        for field in ("objective", "discovery", "scope", "steps", "verification", "acceptance", "budget", "doc_delta"):
            for value in (None, "", [], {}):
                plan = ready()
                plan[field] = value
                with self.subTest(field=field, value=value), self.assertRaises(validator.InvalidPlan):
                    validator.validate_body(body(plan))
            plan = ready()
            del plan[field]
            with self.subTest(missing=field), self.assertRaises(validator.InvalidPlan):
                validator.validate_body(body(plan))

    def test_empty_step_and_verification_details_fail(self):
        for group, field in (("steps", "paths"), ("steps", "action"), ("steps", "reason"),
                             ("verification", "command"), ("verification", "expected")):
            plan = ready()
            plan[group][0][field] = [] if field == "paths" else "  "
            with self.subTest(group=group, field=field), self.assertRaises(validator.InvalidPlan):
                validator.validate_body(body(plan))

    def test_placeholders_fail_only_as_unresolved_field_values(self):
        for value in ("TBD", "TODO", "later", "as needed", "etc.", "..."):
            plan = ready()
            plan["steps"][0]["action"] = value
            with self.subTest(value=value), self.assertRaises(validator.InvalidPlan):
                validator.validate_body(body(plan))

    def test_ready_with_blockers_and_blocked_without_reason_fail(self):
        plan = ready()
        plan["blocking_questions"] = ["Which target device is authorized?"]
        with self.assertRaises(validator.InvalidPlan):
            validator.validate_body(body(plan))
        plan["status"] = "BLOCKED"
        self.assertIn("PASS: BLOCKED", validator.validate_body(body(plan)))
        plan["blocking_questions"] = []
        with self.assertRaises(validator.InvalidPlan):
            validator.validate_body(body(plan))

    def test_not_required_needs_explanation_but_no_full_plan(self):
        self.assertIn("PASS: NOT-REQUIRED", validator.validate_body(body({
            "schema_version": 1, "status": "NOT-REQUIRED", "reason": "Routine reversible spelling correction."})))
        with self.assertRaises(validator.InvalidPlan):
            validator.validate_body(body({"schema_version": 1, "status": "NOT-REQUIRED", "reason": ""}))

    def test_single_file_ready_is_validated_and_absence_is_advisory(self):
        self.assertIn("SKIP", validator.validate_body("Ordinary prose", 1))
        self.assertIn("WARN", validator.validate_body("Ordinary prose", 2))
        plan = ready()
        plan["objective"] = ""
        with self.assertRaises(validator.InvalidPlan):
            validator.validate_body(body(plan), 1)

    def test_multiple_incomplete_malformed_and_conflicting_declarations_fail(self):
        for value in (body(ready()) * 2, "```aep\n{}", "```aep\n{broken}\n```",
                      body(ready()) + "AEP Status: BLOCKED\n",
                      body(ready()).replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1')):
            with self.subTest(value=value[:60]), self.assertRaises(validator.InvalidPlan):
                validator.validate_body(value)

    def test_scope_paths_and_budget_types_fail_closed(self):
        for path in ("/tmp/out", "../other", "C:\\temp\\out"):
            plan = ready()
            plan["scope"]["paths"] = [path]
            with self.subTest(path=path), self.assertRaises(validator.InvalidPlan):
                validator.validate_body(body(plan))
        for count in (True, -1, 2.5, "3"):
            plan = ready()
            plan["budget"]["max_repair_attempts"] = count
            with self.subTest(count=count), self.assertRaises(validator.InvalidPlan):
                validator.validate_body(body(plan))

    def test_cli_treats_commands_as_data_and_returns_failure_status(self):
        plan = ready()
        plan["verification"][0]["command"] = "exit 77; $(exit 88)"
        env = {**os.environ, "PR_BODY": body(plan)}
        good = subprocess.run([sys.executable, str(SCRIPT)], env=env, capture_output=True, text=True, timeout=5)
        self.assertEqual(good.returncode, 0, good.stderr)
        env["PR_BODY"] = "AEP Status: READY\nObjective:\nSteps:\ntest command:\n"
        bad = subprocess.run([sys.executable, str(SCRIPT)], env=env, capture_output=True, text=True, timeout=5)
        self.assertEqual(bad.returncode, 1)


if __name__ == "__main__":
    unittest.main()
