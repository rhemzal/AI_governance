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

    def test_missing_or_other_verify_exit_asks_once_for_unverified(self):
        missing = self.run_stop()
        notice = self.payload(missing)["followup_message"]
        self.assertIn("UNVERIFIED", notice)
        self.assertIn("verify.sh missing", notice)
        self.assertIn("asking for an unverified report", missing.stderr)
        again = self.run_stop('{"loop_count": 1}')
        self.assertEqual(self.payload(again), {})
        self.assertIn("allowing stop after the unverified notice", again.stderr)
        self.verify(1)
        other = self.run_stop()
        message = self.payload(other)["followup_message"]
        self.assertIn("UNVERIFIED", message)
        self.assertIn("verifier exit 1", message)
        self.assertIn("could not run", other.stderr)

    def test_passing_verify_allows_stop(self):
        self.verify(0)
        result = self.run_stop('{"loop_count": 0}')
        self.assertEqual(self.payload(result), {})

    def test_followup_keeps_only_the_tail(self):
        path = self.root / ".specify/gates/verify.sh"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "#!/bin/sh\n"
            "printf 'START-'\n"
            "i=0\n"
            "while [ \"$i\" -lt 7000 ]; do printf 'A'; i=$((i + 1)); done\n"
            "printf 'END-MARKER\\n'\n"
            "exit 2\n"
        )
        path.chmod(0o755)
        message = self.payload(self.run_stop())["followup_message"]
        self.assertLessEqual(len(message), 6000)
        self.assertIn("END-MARKER", message)
        self.assertIn("Quality gate failed", message)
        self.assertNotIn("START-", message)

    def test_verifier_does_not_inherit_project_dir(self):
        path = self.root / ".specify/gates/verify.sh"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "#!/bin/sh\n"
            "printf 'CLAUDE=%s\\n' \"${CLAUDE_PROJECT_DIR-<unset>}\"\n"
            "printf 'CURSOR=%s\\n' \"${CURSOR_PROJECT_DIR-<unset>}\"\n"
            "exit 2\n"
        )
        path.chmod(0o755)
        env = os.environ.copy()
        env["CURSOR_PROJECT_DIR"] = str(self.root)
        env["CLAUDE_PROJECT_DIR"] = "/tmp/other-project"
        result = subprocess.run(
            ["bash", str(STOP)],
            input="{}",
            capture_output=True,
            text=True,
            timeout=15,
            env=env,
            cwd=self.root,
        )
        message = self.payload(result)["followup_message"]
        self.assertIn("CLAUDE=<unset>", message)
        self.assertIn("CURSOR=<unset>", message)

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
