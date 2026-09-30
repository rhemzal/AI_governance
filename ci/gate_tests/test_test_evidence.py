"""Behavioral controls for the optional test-evidence assessment."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "validate_test_evidence.py"
SPEC = importlib.util.spec_from_file_location("test_evidence_validator", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def records():
    expected = {
        "schema_version": 1, "run_id": "attempt-1",
        "tested_state": {"source": "commit-a", "build": "binary-a", "fixture": "fixture-a"},
        "required_checks": ["seek.click", "seek.frame"], "cleanup_required": True,
    }
    report = {
        "schema_version": 1, "run_id": "attempt-1",
        "tested_state": dict(expected["tested_state"]),
        "execution": {"status": "completed", "exit_code": 0},
        "checks": [
            {"id": name, "status": "passed", "evidence": [f"result.json#{name}"]}
            for name in expected["required_checks"]
        ],
        "cleanup": "complete",
    }
    return expected, report


class TestEvidenceAssessment(unittest.TestCase):
    def test_known_good_and_no_input_mutation(self):
        expected, report = records()
        original = copy.deepcopy((expected, report))
        self.assertEqual("VERIFIED", VALIDATOR.assess(expected, report)["outcome"])
        self.assertEqual(original, (expected, report))

    def test_exit_zero_with_empty_or_partial_selection_is_not_verified(self):
        for checks in ([], records()[1]["checks"][:1]):
            with self.subTest(checks=checks):
                expected, report = records()
                report["checks"] = checks
                self.assertEqual("PARTIAL", VALIDATOR.assess(expected, report)["outcome"])

    def test_required_skip_failure_or_not_run_is_not_verified(self):
        for status in ("skipped", "not_run", "failed", "error"):
            with self.subTest(status=status):
                expected, report = records()
                report["checks"][0].update(status=status, evidence=[])
                self.assertEqual("PARTIAL", VALIDATOR.assess(expected, report)["outcome"])

    def test_additional_failure_is_not_hidden(self):
        for status in ("failed", "error"):
            with self.subTest(status=status):
                expected, report = records()
                report["checks"].append({"id": "other", "status": status, "evidence": []})
                self.assertEqual("PARTIAL", VALIDATOR.assess(expected, report)["outcome"])

    def test_optional_skips_are_reported(self):
        expected, report = records()
        report["checks"].append({"id": "other", "status": "skipped", "evidence": []})
        result = VALIDATOR.assess(expected, report)
        self.assertEqual("VERIFIED", result["outcome"])
        self.assertEqual(["other"], result["optional_skipped_checks"])

    def test_failed_timed_out_cancelled_and_nonzero_execution(self):
        for status, code, outcome in (
            ("completed", 1, "PARTIAL"), ("failed", 0, "PARTIAL"),
            ("timed_out", None, "PARTIAL"), ("cancelled", -15, "CANCELLED"),
        ):
            with self.subTest(status=status, code=code):
                expected, report = records()
                report["execution"] = {"status": status, "exit_code": code}
                self.assertEqual(outcome, VALIDATOR.assess(expected, report)["outcome"])

    def test_required_cleanup_must_be_observed_complete(self):
        for cleanup in ("failed", "unknown", "not_required"):
            with self.subTest(cleanup=cleanup):
                expected, report = records()
                report["cleanup"] = cleanup
                self.assertEqual("PARTIAL", VALIDATOR.assess(expected, report)["outcome"])

    def test_cleanup_not_required_still_does_not_hide_a_failure(self):
        expected, report = records()
        expected["cleanup_required"] = False
        report["cleanup"] = "not_required"
        self.assertEqual("VERIFIED", VALIDATOR.assess(expected, report)["outcome"])
        report["cleanup"] = "failed"
        self.assertEqual("PARTIAL", VALIDATOR.assess(expected, report)["outcome"])

    def test_run_and_each_state_identity_must_match(self):
        for field in ("run_id", "source", "build", "fixture"):
            with self.subTest(field=field):
                expected, report = records()
                if field == "run_id":
                    report[field] = "old-run"
                else:
                    report["tested_state"][field] = "old"
                with self.assertRaises(VALIDATOR.EvidenceError):
                    VALIDATOR.assess(expected, report)

    def test_empty_duplicate_and_malformed_expectations_are_blocked(self):
        for field, value in (
            ("required_checks", []), ("required_checks", ["a", "a"]),
            ("required_checks", [{}]), ("cleanup_required", 1),
            ("tested_state", {}), ("tested_state", {"build": "unknown"}),
            ("schema_version", True), ("run_id", " "),
        ):
            with self.subTest(field=field, value=value):
                expected, report = records()
                expected[field] = value
                with self.assertRaises(VALIDATOR.EvidenceError):
                    VALIDATOR.assess(expected, report)

    def test_missing_and_unknown_fields_are_blocked(self):
        for target in ("expected", "report", "execution", "check"):
            for mode in ("missing", "unknown"):
                with self.subTest(target=target, mode=mode):
                    expected, report = records()
                    record = {"expected": expected, "report": report,
                              "execution": report["execution"],
                              "check": report["checks"][0]}[target]
                    if mode == "missing":
                        del record[next(iter(record))]
                    else:
                        record["surprise"] = True
                    with self.assertRaises(VALIDATOR.EvidenceError):
                        VALIDATOR.assess(expected, report)

    def test_invalid_native_normalization_is_blocked(self):
        for field, value in (("status", {}), ("status", "success"),
                             ("id", []), ("evidence", []), ("evidence", ["x", "x"])):
            with self.subTest(field=field, value=value):
                expected, report = records()
                report["checks"][0][field] = value
                with self.assertRaises(VALIDATOR.EvidenceError):
                    VALIDATOR.assess(expected, report)
        expected, report = records()
        report["checks"].append(copy.deepcopy(report["checks"][0]))
        with self.assertRaises(VALIDATOR.EvidenceError):
            VALIDATOR.assess(expected, report)

    def test_invalid_execution_and_cleanup_are_blocked(self):
        for execution in ([], {"status": "completed", "exit_code": None},
                          {"status": "completed", "exit_code": False},
                          {"status": [], "exit_code": 0}):
            with self.subTest(execution=execution):
                expected, report = records()
                report["execution"] = execution
                with self.assertRaises(VALIDATOR.EvidenceError):
                    VALIDATOR.assess(expected, report)
        expected, report = records()
        report["cleanup"] = {}
        with self.assertRaises(VALIDATOR.EvidenceError):
            VALIDATOR.assess(expected, report)

    def test_cli_exit_codes_and_outcomes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for mode, code, outcome in (("good", 0, "VERIFIED"),
                                        ("empty", 1, "PARTIAL"),
                                        ("cancelled", 1, "CANCELLED"),
                                        ("stale", 2, "BLOCKED")):
                with self.subTest(mode=mode):
                    expected, report = records()
                    if mode == "empty":
                        report["checks"] = []
                    elif mode == "cancelled":
                        report["execution"] = {"status": "cancelled", "exit_code": -15}
                    elif mode == "stale":
                        report["run_id"] = "old"
                    (root / "expected.json").write_text(json.dumps(expected), encoding="utf-8")
                    (root / "report.json").write_text(json.dumps(report), encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(SCRIPT), "--expected", str(root / "expected.json"),
                         "--report", str(root / "report.json")],
                        capture_output=True, text=True, timeout=10, check=False,
                    )
                    self.assertEqual(code, result.returncode, result.stderr)
                    self.assertEqual(outcome, json.loads(result.stdout)["outcome"])

    def test_json_ambiguity_corruption_and_size_are_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            for raw in ('{"a": 1, "a": 2}', '{"nested": {"a": 1, "a": 2}}',
                        '{"number": NaN}', '{"number": Infinity}', '{broken',
                        " " * (VALIDATOR.MAX_BYTES + 1)):
                with self.subTest(prefix=raw[:30]):
                    path.write_text(raw, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        VALIDATOR.read_json(path)
            path.write_bytes(b"\xff")
            with self.assertRaises(UnicodeError):
                VALIDATOR.read_json(path)
            with self.assertRaises(VALIDATOR.EvidenceError):
                VALIDATOR.read_json(Path(directory))


if __name__ == "__main__":
    unittest.main()
