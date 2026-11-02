"""The finding comparator accepts hand-written reports and does not run a scanner.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
Python standard library. Report files are data. No scanner binary is invoked.
"""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TOOL = Path(__file__).resolve().parents[1] / "ratchet_findings.py"
BASE = "a" * 40
HEAD = "b" * 40
FINDING = "boundary:src/core/a.py:load:adapters.db"


def report(revision, findings):
    return {
        "schema_version": 1,
        "revision": revision,
        "check": "hand-written@1",
        "scope": ["src/core"],
        "status": "ok",
        "findings": findings,
    }


class RatchetCanary(unittest.TestCase):
    def test_hand_written_reports_pass_without_a_scanner(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / "base.json"
            current = root / "current.json"
            baseline.write_text(json.dumps(report(BASE, [FINDING])), encoding="utf-8")
            current.write_text(json.dumps(report(HEAD, [FINDING])), encoding="utf-8")
            before = baseline.read_bytes(), current.read_bytes()
            result = subprocess.run(
                [sys.executable, str(TOOL), "--baseline", str(baseline), "--current", str(current),
                 "--baseline-revision", BASE, "--current-revision", HEAD],
                capture_output=True, text=True, timeout=10, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["outcome"], "no_new_findings")
            self.assertEqual(payload["remaining"], [FINDING])
            self.assertEqual(before, (baseline.read_bytes(), current.read_bytes()))
            self.assertFalse((root / "hand-written").exists())
            current.write_text(json.dumps(report(HEAD, [FINDING, "boundary:new"])), encoding="utf-8")
            rejected = subprocess.run(
                [sys.executable, str(TOOL), "--baseline", str(baseline), "--current", str(current),
                 "--baseline-revision", BASE, "--current-revision", HEAD],
                capture_output=True, text=True, timeout=10, check=False,
            )
            self.assertEqual(rejected.returncode, 1, rejected.stderr)
            self.assertEqual(json.loads(rejected.stdout)["introduced"], ["boundary:new"])
