"""CLI regressions for legacy-debt comparison, including misleading green results."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TOOL = Path(__file__).resolve().parents[1] / "ratchet_findings.py"
BASE = "a" * 40
HEAD = "b" * 40
OLD = "boundary:src/core/a.py:load:adapters.db"
NEW = "boundary:src/core/b.py:save:adapters.net"


class RatchetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.baseline = self.report(BASE, [OLD])
        self.current = self.report(HEAD, [OLD])

    @staticmethod
    def report(revision, findings):
        return {"schema_version": 1, "revision": revision, "check": "boundary@1:rules@1",
                "scope": ["src/core"], "status": "ok", "findings": findings}

    def run_cli(self, base_text=None, current_text=None, missing=False):
        base_path, current_path = self.root / "base.json", self.root / "current.json"
        base_path.write_text(json.dumps(self.baseline) if base_text is None else base_text)
        if missing:
            current_path.unlink(missing_ok=True)
        else:
            current_path.write_text(json.dumps(self.current) if current_text is None else current_text)
        before = {p: p.read_bytes() for p in self.root.iterdir()}
        result = subprocess.run(
            [sys.executable, str(TOOL), "--baseline", str(base_path), "--current", str(current_path),
             "--baseline-revision", BASE, "--current-revision", HEAD],
            capture_output=True, text=True, timeout=5)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.iterdir()})
        return result

    def assert_invalid(self, **kwargs):
        result = self.run_cli(**kwargs)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stderr)["outcome"], "invalid_input")
        self.assertEqual(result.stdout, "")

    def test_unchanged_legacy_findings_pass_without_claiming_clean(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["outcome"], "no_new_findings")
        self.assertEqual(report["remaining"], [OLD])

    def test_removal_passes_and_reports_resolved(self):
        self.current["findings"] = []
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["resolved"], [OLD])

    def test_new_finding_fails(self):
        self.current["findings"].append(NEW)
        result = self.run_cli()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["introduced"], [NEW])

    def test_equal_count_replacement_still_fails(self):
        self.current["findings"] = [NEW]
        result = self.run_cli()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["resolved"], [OLD])

    def test_successful_empty_scans_pass(self):
        self.baseline["findings"] = self.current["findings"] = []
        self.assertEqual(self.run_cli().returncode, 0)

    def test_scanner_failure_skip_and_timeout_are_not_empty_success(self):
        for name in ("baseline", "current"):
            for status in ("error", "skipped", "timeout", "", None):
                with self.subTest(side=name, status=status):
                    report = getattr(self, name)
                    report["status"] = status
                    self.assert_invalid()
                    report["status"] = "ok"

    def test_revision_mismatch_on_either_side_fails(self):
        for name in ("baseline", "current"):
            with self.subTest(side=name):
                report = getattr(self, name)
                old = report["revision"]
                report["revision"] = "c" * 40
                self.assert_invalid()
                report["revision"] = old

    def test_changed_scanner_or_scope_needs_review(self):
        for key, value in (("check", "boundary@2:rules@1"), ("scope", ["src/core/subset"])):
            with self.subTest(key=key):
                old = self.current[key]
                self.current[key] = value
                self.assert_invalid()
                self.current[key] = old

    def test_order_of_scope_and_findings_is_irrelevant(self):
        self.baseline["scope"] = ["src/core", "src/api"]
        self.current["scope"] = ["src/api", "src/core"]
        self.baseline["findings"] = [OLD, NEW]
        self.current["findings"] = [NEW, OLD]
        self.assertEqual(self.run_cli().returncode, 0)

    def test_duplicate_findings_and_scope_rejected(self):
        for key, value in (("findings", [OLD, OLD]), ("scope", ["src/core", "src/core"])):
            with self.subTest(key=key):
                old = self.current[key]
                self.current[key] = value
                self.assert_invalid()
                self.current[key] = old

    def test_malformed_missing_and_duplicate_json_keys_fail(self):
        self.assert_invalid(current_text="{")
        self.assert_invalid(current_text='{"status":"error","status":"ok"}')
        self.assert_invalid(missing=True)
        self.assert_invalid(base_text="[]")

    def test_incomplete_or_unknown_schema_cannot_pass(self):
        for key in list(self.current):
            with self.subTest(missing=key):
                value = self.current.pop(key)
                self.assert_invalid()
                self.current[key] = value
        for value in (True, 2, "1", None):
            self.current["schema_version"] = value
            self.assert_invalid()
        self.current["schema_version"] = 1
        self.current["unreviewed_exceptions"] = [NEW]
        self.assert_invalid()

    def test_bad_types_and_non_normalized_scopes_fail(self):
        for key, value in (("findings", ""), ("findings", [""]), ("findings", [None]),
                           ("check", " "), ("scope", []), ("scope", ["../src"]),
                           ("scope", ["/src"]), ("scope", ["src/**"]),
                           ("scope", ["src/./core"]), ("scope", ["C:/src"]),
                           ("revision", "main")):
            with self.subTest(key=key, value=value):
                old = self.current[key]
                self.current[key] = value
                self.assert_invalid()
                self.current[key] = old


if __name__ == "__main__":
    unittest.main()
