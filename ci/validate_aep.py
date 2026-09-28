"""Validate the structured AEP declaration in a PR body; never execute its commands.

Reference implementation of usage/AEP_VALIDATION.md. Python standard library only.
"""

import argparse
import json
import os
import re
import sys
from pathlib import PurePosixPath


class InvalidPlan(ValueError):
    """A declaration is malformed or contradicts its readiness status."""


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidPlan(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise InvalidPlan(f"{label}: expected non-empty text")
    normalized = value.strip().casefold()
    if normalized == "..." or normalized.rstrip(".") in {"tbd", "todo", "later", "as needed", "etc"}:
        raise InvalidPlan(f"{label}: unresolved placeholder")


def _strings(value, label, *, empty=False, paths=False):
    if not isinstance(value, list) or (not empty and not value):
        raise InvalidPlan(f"{label}: expected {'a' if empty else 'a non-empty'} list")
    for index, item in enumerate(value):
        name = f"{label}[{index}]"
        _text(item, name)
        if paths:
            path = PurePosixPath(item)
            if path.is_absolute() or ".." in path.parts or "\\" in item or ":" in item:
                raise InvalidPlan(f"{name}: use a repository-relative POSIX path or glob")


def _fields(value, names, label):
    if not isinstance(value, dict):
        raise InvalidPlan(f"{label}: expected an object")
    missing = set(names) - value.keys()
    extra = value.keys() - set(names)
    if missing or extra:
        raise InvalidPlan(f"{label}: missing={sorted(missing)}, unknown={sorted(extra)}")


def _records(value, names, label):
    if not isinstance(value, list) or not value:
        raise InvalidPlan(f"{label}: expected a non-empty list")
    for index, record in enumerate(value):
        name = f"{label}[{index}]"
        _fields(record, names, name)
        for field in names:
            if field == "paths":
                _strings(record[field], f"{name}.paths", paths=True)
            else:
                _text(record[field], f"{name}.{field}")


def validate_plan(plan):
    if not isinstance(plan, dict):
        raise InvalidPlan("AEP must be a JSON object")
    if type(plan.get("schema_version")) is not int or plan["schema_version"] != 1:
        raise InvalidPlan("schema_version must be integer 1")
    status = plan.get("status")
    if status not in ("READY", "BLOCKED", "NOT-REQUIRED"):
        raise InvalidPlan("status must be READY, BLOCKED, or NOT-REQUIRED")
    if status == "NOT-REQUIRED":
        _fields(plan, ("schema_version", "status", "reason"), "AEP")
        _text(plan["reason"], "reason")
        return status

    _fields(plan, ("schema_version", "status", "objective", "discovery", "risk",
                   "scope", "steps", "verification", "acceptance", "blocking_questions",
                   "budget", "doc_delta"), "AEP")
    _text(plan["objective"], "objective")
    _strings(plan["discovery"], "discovery")
    if plan["risk"] not in ("LOW", "HIGH"):
        raise InvalidPlan("risk must be LOW or HIGH")
    _fields(plan["scope"], ("paths", "allowed_effects", "approval_required"), "scope")
    _strings(plan["scope"]["paths"], "scope.paths", paths=True)
    _strings(plan["scope"]["allowed_effects"], "scope.allowed_effects")
    _strings(plan["scope"]["approval_required"], "scope.approval_required", empty=True)
    _records(plan["steps"], ("paths", "action", "reason"), "steps")
    _records(plan["verification"], ("command", "expected"), "verification")
    _strings(plan["acceptance"], "acceptance")
    _strings(plan["blocking_questions"], "blocking_questions", empty=True)
    if (status == "READY") != (not plan["blocking_questions"]):
        raise InvalidPlan("READY requires no blockers; BLOCKED requires at least one blocker")
    _fields(plan["budget"], ("max_repair_attempts", "on_exhaustion"), "budget")
    count = plan["budget"]["max_repair_attempts"]
    if type(count) is not int or count < 0:
        raise InvalidPlan("budget.max_repair_attempts must be a non-negative integer")
    _text(plan["budget"]["on_exhaustion"], "budget.on_exhaustion")
    _text(plan["doc_delta"], "doc_delta")
    return status


def _declarations(body):
    """Scan the documented top-level fence subset, not a full Markdown AST."""
    blocks, markers, content = [], [], []
    active = None
    for line in re.split(r"\r\n|\r|\n", body):
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if active:
            delimiter, is_aep = active
            if (fence and fence[1][0] == delimiter[0]
                    and len(fence[1]) >= len(delimiter) and not fence[2].strip()):
                if is_aep:
                    blocks.append("\n".join(content))
                active, content = None, []
            elif is_aep:
                content.append(line)
            continue
        if fence:
            info = fence[2].strip()
            if info.split()[:1] == ["aep"] and info != "aep":
                raise InvalidPlan("aep fence info must contain only the language name")
            # Backticks in a backtick info string do not open a Markdown block.
            if fence[1][0] == "`" and "`" in info:
                continue
            active = (fence[1], info == "aep")
            continue
        if re.match(r"^[ \t>]*(?:(?:[-+*]|[0-9]+[.)])[ \t]+)?"
                    r"(?:`{3,}|~{3,})[ \t]*aep(?:[ \t]|$)", line):
            raise InvalidPlan("put the aep fence at top level, indented at most three spaces")
        marker = re.match(r"^\s*(?:[-*]\s+)?AEP Status:\s*(\S+)", line)
        if marker:
            markers.append(marker[1])
    if active and active[1]:
        raise InvalidPlan("expected exactly one complete fenced aep block")
    return blocks, markers


def validate_body(body, changed_files=0):
    """Return a status message; missing declarations remain advisory.

    Only one fenced `aep` JSON block is authoritative. Other PR prose is ignored,
    except an optional legacy status marker, which must agree if supplied.
    """
    blocks, markers = _declarations(body)
    if not blocks:
        if markers:
            raise InvalidPlan("legacy AEP Status marker requires a structured aep block; see migration guide")
        return "WARN: no AEP declaration; review applicability" if changed_files >= 2 else "SKIP: no AEP declaration"
    if len(blocks) != 1:
        raise InvalidPlan("expected exactly one complete fenced aep block")
    try:
        plan = json.loads(blocks[0], object_pairs_hook=_object)
    except json.JSONDecodeError as error:
        raise InvalidPlan(f"invalid AEP JSON at line {error.lineno}, column {error.colno}") from error
    status = validate_plan(plan)
    if markers and (len(markers) != 1 or markers[0] != status):
        raise InvalidPlan("AEP Status marker contradicts the structured declaration")
    return f"PASS: {status} declaration shape; authority, feasibility, and results still require review"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--changed-files", type=int, default=0)
    args = parser.parse_args(argv)
    body = os.environ["PR_BODY"] if "PR_BODY" in os.environ else sys.stdin.read()
    try:
        print(validate_body(body, args.changed_files))
    except InvalidPlan as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
