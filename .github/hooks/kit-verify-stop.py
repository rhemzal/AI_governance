#!/usr/bin/env python3
"""Run the Tier C verifier from a GitHub Copilot agentStop hook."""

import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone


VERIFY_TIMEOUT_SECONDS = 140
REASON_LIMIT = 6000
VERIFIER = Path(".specify/gates/verify.sh")


def _text(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def run_verifier(project_root, timeout_seconds=VERIFY_TIMEOUT_SECONDS):
    verifier = project_root / VERIFIER
    if not verifier.is_file() or not os.access(verifier, os.X_OK):
        return "missing", None, "verify.sh missing or not executable"

    env = os.environ.copy()
    env.pop("CLAUDE_PROJECT_DIR", None)
    env.pop("CURSOR_PROJECT_DIR", None)

    try:
        result = subprocess.run(
            ["bash", str(verifier), "--boundary", "agent"],
            cwd=project_root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return "timeout", None, _text(error.stdout) + _text(error.stderr)
    except OSError as error:
        return "unavailable", None, str(error)

    return "completed", result.returncode, result.stdout


def decision_for(status, return_code, output, stop_hook_active):
    if stop_hook_active:
        return {}
    if status == "completed" and return_code == 0:
        return {}
    if status == "completed" and return_code == 2:
        reason = output
        if output:
            reason += "\n\n"
        reason += "Quality gate failed at the agent boundary. Fix the issues above before stopping."
        return {"decision": "block", "reason": reason[-REASON_LIMIT:]}

    if status == "missing":
        detail = "verify.sh missing"
    elif status == "timeout":
        detail = "verifier timed out"
    elif status == "completed":
        detail = f"verifier exit {return_code}"
    else:
        detail = f"verifier could not run: {output}"
    reason = (
        f"Quality gate did not run ({detail}). Report this work as UNVERIFIED. "
        "Do not claim it is verified, and do not change the gate so this stop can succeed."
    )
    return {"decision": "block", "reason": reason[-REASON_LIMIT:]}


def emit(payload):
    sys.stdout.write(json.dumps(payload, ensure_ascii=True) + "\n")


def record_invocation(project_root, decision, status, return_code):
    marker = project_root / ".github/hooks/record-stop-invocations"
    if not marker.is_file():
        return

    log = project_root / ".github/hooks/stop-invocations.jsonl"
    record = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "vscode-copilot",
        "decision": "block" if decision.get("decision") == "block" else "allow",
        "verify_status": status,
        "verify_rc": return_code,
    }
    try:
        descriptor = os.open(log, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
        with os.fdopen(descriptor, "a", encoding="utf-8") as output:
            output.write(json.dumps(record, ensure_ascii=True) + "\n")
    except OSError as error:
        print(f"gates: could not write the optional dispatch recorder: {error}", file=sys.stderr)


def main():
    project_root = Path.cwd().resolve()
    try:
        event = json.loads(sys.stdin.read())
    except json.JSONDecodeError as error:
        print(f"gates: invalid Copilot hook JSON ({error}); allowing stop as UNVERIFIED.", file=sys.stderr)
        decision = {}
        record_invocation(project_root, decision, "invalid-input", None)
        emit(decision)
        return 0

    if not isinstance(event, dict) or type(event.get("stop_hook_active")) is not bool:
        print("gates: invalid Copilot agentStop payload; allowing stop as UNVERIFIED.", file=sys.stderr)
        decision = {}
        record_invocation(project_root, decision, "invalid-input", None)
        emit(decision)
        return 0

    active = event["stop_hook_active"]
    if active:
        print("gates: stop_hook_active set; allowing stop to prevent a continuation loop.", file=sys.stderr)
        decision = {}
        record_invocation(project_root, decision, "active-loop", None)
        emit(decision)
        return 0

    status, return_code, output = run_verifier(project_root)
    decision = decision_for(status, return_code, output, stop_hook_active=False)
    if decision.get("decision") == "block":
        print(decision["reason"], file=sys.stderr)
    record_invocation(project_root, decision, status, return_code)
    emit(decision)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
