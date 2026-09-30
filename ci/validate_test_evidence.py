#!/usr/bin/env python3
"""Assess declared test observations against independent expectations; never run tests."""

import argparse
import json
from pathlib import Path
import sys

MAX_BYTES = 1024 * 1024


class EvidenceError(ValueError):
    """Invalid or incomparable evidence."""


def _object(value, fields, label):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise EvidenceError(f"{label}: expected exactly {', '.join(fields)}")


def _text(value, label):
    if (not isinstance(value, str) or not value or value != value.strip()
            or len(value) > 2048 or any(ord(char) < 32 for char in value)):
        raise EvidenceError(f"{label}: expected non-empty, bounded text")
    return value


def _strings(value, label, *, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise EvidenceError(f"{label}: expected {'non-empty ' if nonempty else ''}list")
    for item in value:
        _text(item, label)
    if len(set(value)) != len(value):
        raise EvidenceError(f"{label}: duplicate entries")


def _state(value, label):
    if not isinstance(value, dict) or not value:
        raise EvidenceError(f"{label}: expected non-empty identity map")
    for key, identity in value.items():
        _text(key, label)
        _text(identity, label)
        if identity.lower() in {"unknown", "unavailable", "tbd", "todo"}:
            raise EvidenceError(f"{label}: unresolved identity")


def _version(value):
    if type(value) is not int or value != 1:
        raise EvidenceError("schema_version: expected integer 1")


def assess(expected, report):
    """Return an assessment of supplied data, not proof that a test really ran."""
    _object(expected, ("schema_version", "run_id", "tested_state",
                       "required_checks", "cleanup_required"), "expected")
    _object(report, ("schema_version", "run_id", "tested_state",
                     "execution", "checks", "cleanup"), "report")
    for label, record in (("expected", expected), ("report", report)):
        _version(record["schema_version"])
        _text(record["run_id"], f"{label}.run_id")
        _state(record["tested_state"], f"{label}.tested_state")
    _strings(expected["required_checks"], "required_checks", nonempty=True)
    if type(expected["cleanup_required"]) is not bool:
        raise EvidenceError("cleanup_required: expected boolean")
    if expected["run_id"] != report["run_id"]:
        raise EvidenceError("run_id: evidence belongs to a different run")
    if expected["tested_state"] != report["tested_state"]:
        raise EvidenceError("tested_state: evidence is stale or incomparable")

    execution = report["execution"]
    _object(execution, ("status", "exit_code"), "execution")
    status = _text(execution["status"], "execution.status")
    if status not in {"completed", "failed", "timed_out", "cancelled"}:
        raise EvidenceError("execution.status: unsupported value")
    exit_code = execution["exit_code"]
    if exit_code is not None and type(exit_code) is not int:
        raise EvidenceError("execution.exit_code: expected integer or null")
    if status == "completed" and exit_code is None:
        raise EvidenceError("completed execution requires an exit code")

    if not isinstance(report["checks"], list):
        raise EvidenceError("checks: expected list")
    checks = {}
    for check in report["checks"]:
        _object(check, ("id", "status", "evidence"), "check")
        check_id = _text(check["id"], "check.id")
        check_status = _text(check["status"], "check.status")
        if check_status not in {"passed", "failed", "error", "skipped", "not_run"}:
            raise EvidenceError("check.status: unsupported value")
        _strings(check["evidence"], "check.evidence", nonempty=check_status == "passed")
        if check_id in checks:
            raise EvidenceError(f"duplicate check: {check_id}")
        checks[check_id] = check

    cleanup = _text(report["cleanup"], "cleanup")
    if cleanup not in {"complete", "failed", "unknown", "not_required"}:
        raise EvidenceError("cleanup: unsupported value")
    reasons = []
    if status != "completed":
        reasons.append(f"execution {status}")
    if exit_code != 0:
        reasons.append(f"execution exit code {exit_code}")
    for check_id in expected["required_checks"]:
        if check_id not in checks:
            reasons.append(f"required check missing: {check_id}")
        elif checks[check_id]["status"] != "passed":
            reasons.append(f"required check {checks[check_id]['status']}: {check_id}")
    required = set(expected["required_checks"])
    for check_id, check in checks.items():
        if check_id not in required and check["status"] in {"failed", "error"}:
            reasons.append(f"additional check {check['status']}: {check_id}")
    if cleanup == "failed" or (expected["cleanup_required"] and cleanup != "complete"):
        reasons.append(f"cleanup {cleanup}")
    outcome = "PARTIAL" if reasons else "VERIFIED"
    if status == "cancelled":
        outcome = "CANCELLED"
    return {
        "outcome": outcome,
        "run_id": report["run_id"],
        "reasons": reasons,
        "optional_skipped_checks": [
            key for key, check in checks.items()
            if key not in required and check["status"] in {"skipped", "not_run"}
        ],
    }


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise EvidenceError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value):
    raise EvidenceError(f"invalid JSON constant: {value}")


def read_json(path):
    if not path.is_file():
        raise EvidenceError(f"expected a regular JSON file: {path}")
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise EvidenceError(f"JSON file exceeds {MAX_BYTES} bytes")
    return json.loads(data.decode("utf-8"), object_pairs_hook=_pairs,
                      parse_constant=_constant)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = assess(read_json(args.expected), read_json(args.report))
    except (EvidenceError, OSError, UnicodeError, ValueError, RecursionError) as error:
        print(json.dumps({"outcome": "BLOCKED", "reasons": [str(error)]}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0 if result["outcome"] == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
