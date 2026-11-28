"""Classifiers for the continuation synthetic checks.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


BASELINE_SENTENCE = "Do not require `/governed-work` or any second startup ritual."


def classify_stop(record: dict, unmet_criterion: str) -> str:
    """A passing allow decision does not close an assignment that is still open."""
    if (
        record.get("decision") == "allow"
        and record.get("verify_rc") == 0
        and unmet_criterion.strip()
    ):
        return "unfinished-stop"
    return "closed"


def classify_prompt(text: str) -> str:
    """Report whether the received instructions contain the baseline sentence."""
    received = " ".join(text.split())
    if " ".join(BASELINE_SENTENCE.split()) in received:
        return "PRESENT"
    return "ABSENT"


def public_json_sources(script: Path, overlay: Path, path: str) -> list[str]:
    """Run the public overlay selector and return each selected sources cell."""
    proc = subprocess.run(
        [
            sys.executable,
            str(script),
            "--overlay",
            str(overlay),
            "--path",
            path,
            "--json",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"selector exited {proc.returncode}")
    rows = json.loads(proc.stdout)
    return [str(row.get("sources", "")) for row in rows]
