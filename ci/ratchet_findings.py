#!/usr/bin/env python3
"""Compare successful, revision-bound finding sets; never run scanners or update baselines.

Provenance: AI_governance (https://github.com/rhemzal/AI_governance), MIT.
Contract and trust boundary: usage/ENGINEERING_METHODS_ADOPTION.md.
"""

import argparse
import json
from pathlib import Path
import re
import sys


class ReportError(ValueError):
    """An input cannot support a trustworthy comparison."""


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ReportError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def validate_revision(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value):
        raise ReportError("revision must be a full lowercase Git commit ID")


def string_set(value, label, allow_empty=False):
    if not isinstance(value, list) or (not value and not allow_empty):
        raise ReportError(f"{label} must be {'a' if allow_empty else 'a nonempty'} list")
    if not all(nonempty_string(item) for item in value):
        raise ReportError(f"{label} must contain nonempty strings without surrounding whitespace")
    if len(set(value)) != len(value):
        raise ReportError(f"{label} must not contain duplicates")
    return set(value)


def read_report(path, expected_revision):
    validate_revision(expected_revision)
    with Path(path).open(encoding="utf-8") as stream:
        report = json.load(stream, object_pairs_hook=unique_object)
    fields = {"schema_version", "revision", "check", "scope", "status", "findings"}
    if not isinstance(report, dict) or set(report) != fields:
        raise ReportError("report must contain exactly: " + ", ".join(sorted(fields)))
    if type(report["schema_version"]) is not int or report["schema_version"] != 1:
        raise ReportError("unsupported schema_version (expected integer 1)")
    validate_revision(report["revision"])
    if report["revision"] != expected_revision:
        raise ReportError("report revision does not match the expected commit")
    if report["status"] != "ok":
        raise ReportError("scanner did not complete successfully (status must be ok)")
    if not nonempty_string(report["check"]):
        raise ReportError("check must identify the scanner version and rule/configuration contract")
    scope = string_set(report["scope"], "scope")
    for item in scope:
        # Scope is a set of explicit repository-relative roots, not shell patterns.
        if item == ".":
            continue
        if (any(char in item for char in "\\:*?[]\n\r\t")
                or any(part in ("", ".", "..") for part in item.split("/"))):
            raise ReportError("scope entries must be normalized repository-relative roots or .")
    findings = string_set(report["findings"], "findings", allow_empty=True)
    return report, scope, findings


def compare(baseline_path, current_path, baseline_revision, current_revision):
    baseline, old_scope, old = read_report(baseline_path, baseline_revision)
    current, new_scope, new = read_report(current_path, current_revision)
    if baseline["check"] != current["check"] or old_scope != new_scope:
        raise ReportError("scanner contract or scope changed; review migration before comparison")
    introduced = sorted(new - old)
    return {
        "outcome": "regression" if introduced else "no_new_findings",
        "baseline_revision": baseline_revision,
        "current_revision": current_revision,
        "check": current["check"],
        "scope": sorted(new_scope),
        "introduced": introduced,
        "resolved": sorted(old - new),
        "remaining": sorted(old & new),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="trusted prior successful scanner report")
    parser.add_argument("--current", required=True, help="current successful scanner report")
    parser.add_argument("--baseline-revision", required=True, help="independently resolved base commit")
    parser.add_argument("--current-revision", required=True, help="independently resolved tested commit")
    args = parser.parse_args(argv)
    try:
        result = compare(args.baseline, args.current, args.baseline_revision, args.current_revision)
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"outcome": "invalid_input", "error": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 1 if result["introduced"] else 0


if __name__ == "__main__":
    sys.exit(main())
