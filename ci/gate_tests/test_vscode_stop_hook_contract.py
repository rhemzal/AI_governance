"""Contract tests for the VS Code Copilot agentStop adapter."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".github/hooks/kit-verify-stop.py"


class VscodeStopHookContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()

    def write_verifier(self, body):
        path = self.root / ".specify/gates/verify.sh"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"#!/usr/bin/env bash\nset -eu\n{body}\n", encoding="utf-8")
        path.chmod(0o755)
        return path

    def run_hook(self, payload, extra_env=None):
        env = os.environ.copy()
        env["CURSOR_PROJECT_DIR"] = "/tmp/other-cursor-project"
        env["CLAUDE_PROJECT_DIR"] = "/tmp/other-claude-project"
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            ["python3", str(HOOK)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=15,
            env=env,
            cwd=self.root,
        )

    def decision(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as error:
            self.fail(f"hook stdout was not one JSON object: {error}: {result.stdout!r}")

    def test_passing_verifier_allows_stop(self):
        self.write_verifier("printf 'verified\\n'\nexit 0")

        result = self.run_hook('{"stop_hook_active": false}')

        self.assertEqual(self.decision(result), {})

    def test_gate_failure_blocks_with_bounded_tail(self):
        self.write_verifier(
            "printf 'START-MARKER-'\n"
            "i=0\n"
            "while [ \"$i\" -lt 7000 ]; do printf 'A'; i=$((i + 1)); done\n"
            "printf 'END-MARKER\\n'\n"
            "exit 2"
        )

        payload = self.decision(self.run_hook('{"stop_hook_active": false}'))
        reason = payload["reason"]

        self.assertEqual(payload["decision"], "block")
        self.assertIn("Quality gate failed", reason)
        self.assertIn("END-MARKER", reason)
        self.assertNotIn("START-MARKER", reason)
        self.assertLessEqual(len(reason), 6000)

    def test_unavailable_verifier_requests_unverified_and_active_followup_allows(self):
        missing = self.decision(self.run_hook('{"stop_hook_active": false}'))

        self.assertEqual(missing["decision"], "block")
        self.assertIn("UNVERIFIED", missing["reason"])
        self.assertIn("verify.sh missing", missing["reason"])

        marker = self.root / "verifier-ran"
        self.write_verifier(f"touch '{marker}'\nexit 2")
        followup = self.run_hook('{"stop_hook_active": true}')

        self.assertEqual(self.decision(followup), {})
        self.assertFalse(marker.exists())
        self.assertIn("stop_hook_active", followup.stderr)

    def test_unexpected_verifier_exit_requests_unverified(self):
        self.write_verifier("printf 'verifier-failed\\n'\nexit 1")

        payload = self.decision(self.run_hook('{"stop_hook_active": false}'))

        self.assertEqual(payload["decision"], "block")
        self.assertIn("UNVERIFIED", payload["reason"])
        self.assertIn("verifier exit 1", payload["reason"])

    def test_invalid_verifier_bytes_still_emit_json_block(self):
        self.write_verifier("printf '\\377'\nexit 2")

        payload = self.decision(self.run_hook('{"stop_hook_active": false}'))

        self.assertEqual(payload["decision"], "block")
        self.assertIn("\ufffd", payload["reason"])

    def test_timeout_requests_unverified(self):
        self.write_verifier("sleep 2\nexit 0")
        if not HOOK.exists():
            self.fail("VS Code stop adapter is missing")
        spec = importlib.util.spec_from_file_location("kit_verify_stop", HOOK)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        status, code, output = module.run_verifier(self.root, timeout_seconds=0.1)
        payload = module.decision_for(status, code, output, stop_hook_active=False)

        self.assertEqual(payload["decision"], "block")
        self.assertIn("UNVERIFIED", payload["reason"])
        self.assertIn("timed out", payload["reason"])

    def test_invalid_input_is_diagnosed_and_returns_one_valid_allow_object(self):
        result = self.run_hook("[]")

        self.assertEqual(self.decision(result), {})
        self.assertIn("invalid", result.stderr.casefold())

    def test_verifier_does_not_inherit_other_project_roots(self):
        self.write_verifier(
            "printf 'CURSOR=%s\\n' \"${CURSOR_PROJECT_DIR-<unset>}\"\n"
            "printf 'CLAUDE=%s\\n' \"${CLAUDE_PROJECT_DIR-<unset>}\"\n"
            "exit 2"
        )

        payload = self.decision(self.run_hook('{"stop_hook_active": false}'))

        self.assertIn("CURSOR=<unset>", payload["reason"])
        self.assertIn("CLAUDE=<unset>", payload["reason"])

    def test_recorder_writes_minimal_dispatch_evidence_only_when_enabled(self):
        self.write_verifier("exit 0")
        hooks = self.root / ".github/hooks"
        hooks.mkdir(parents=True)
        (hooks / "record-stop-invocations").touch()

        payload = self.decision(self.run_hook('{"stop_hook_active": false}'))
        log = hooks / "stop-invocations.jsonl"
        self.assertTrue(log.is_file(), "dispatch recorder did not create its log")
        record = json.loads(log.read_text(encoding="utf-8").splitlines()[0])

        self.assertEqual(payload, {})
        self.assertEqual(record["source"], "vscode-copilot")
        self.assertEqual(record["decision"], "allow")
        self.assertNotIn("transcript_path", record)
        self.assertNotIn("session_id", record)


if __name__ == "__main__":
    unittest.main()
