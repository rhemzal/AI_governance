"""Contract of the experimental Cursor stop script. Not a native host dispatch.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
Python standard library and Bash. The project root is a temp directory, so the
real verify.sh is not executed.
"""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
STOP = ROOT / ".cursor/hooks/kit-verify-stop.sh"


class StopHookContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()

    def verify(self, code):
        path = self.root / ".specify/gates/verify.sh"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"#!/bin/sh\nprintf '%s\\n' 'verifier-said'\nexit {code}\n")
        path.chmod(0o755)

    def run_stop(self, stdin="{}"):
        env = os.environ.copy()
        env["CURSOR_PROJECT_DIR"] = str(self.root)
        env.pop("CLAUDE_PROJECT_DIR", None)
        return subprocess.run(
            ["bash", str(STOP)],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=15,
            env=env,
            cwd=self.root,
        )

    def payload(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_missing_or_other_verify_exit_allows_stop(self):
        missing = self.run_stop()
        self.assertEqual(self.payload(missing), {})
        self.assertIn("allowing stop", missing.stderr)
        self.verify(1)
        other = self.run_stop()
        self.assertEqual(self.payload(other), {})
        self.assertIn("could not run", other.stderr)
        self.assertNotIn("followup_message", other.stdout)

    def test_verify_exit_two_asks_for_a_followup(self):
        self.verify(2)
        result = self.run_stop()
        message = self.payload(result)["followup_message"]
        self.assertIn("Quality gate failed", message)
        self.assertIn("verifier-said", message)

    def test_stop_hook_active_allows_stop_before_verify(self):
        self.verify(2)
        result = self.run_stop('{"stop_hook_active": true}')
        self.assertEqual(self.payload(result), {})
        self.assertIn("stop_hook_active", result.stderr)
