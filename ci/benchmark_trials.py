"""Validate optional B5–B8 trial records.

Provenance: AI_governance (https://github.com/rhemzal/AI_governance).
The dated absence baseline stays in tooling/BENCHMARK_SCENARIOS.md.
This module does not run a trial and does not grade whether an outcome is true.
"""

from pathlib import Path


HISTORICAL_ABSENCE = (
    "As of 2026-11-02, scenarios B5 through B8 had no recorded trial."
)
SCENARIOS = ("B5", "B6", "B7", "B8")
OUTCOMES = ("pass", "fail", "cancelled", "blocked")
FIELDS = ("scenario", "revision", "outcome")


def _fields(text):
    found = {}
    errors = []
    for line_number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in FIELDS:
            continue
        if key in found:
            errors.append(f"line {line_number}: duplicate {key}")
            continue
        found[key] = value.strip()
    return found, errors


def trial_errors(text):
    """Return human-readable errors. An empty list means the record is well formed."""
    found, errors = _fields(text)
    if found.get("scenario", "") not in SCENARIOS:
        errors.append("scenario must be B5, B6, B7, or B8")
    revision = found.get("revision", "")
    if not revision or any(character.isspace() for character in revision):
        errors.append("revision must be a single non-empty token")
    if found.get("outcome", "") not in OUTCOMES:
        errors.append("outcome must be pass, fail, cancelled, or blocked")
    return errors


def tree_errors(directory):
    """Check trial files. A missing directory and a README-only directory are empty results."""
    directory = Path(directory)
    if not directory.exists():
        return []
    if not directory.is_dir():
        return [f"{directory} is not a directory"]
    errors = []
    for path in sorted(path for path in directory.glob("*.md") if path.is_file()):
        if path.name == "README.md":
            continue
        for error in trial_errors(path.read_text(encoding="utf-8")):
            errors.append(f"{path.name}: {error}")
    return errors
