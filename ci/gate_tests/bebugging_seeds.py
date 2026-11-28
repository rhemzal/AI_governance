"""Run the deferred-kit seeds against checks this repository can execute.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from ci.gate_tests.continuation_synthetic import classify_stop


VERDICTS = {
    "OpenSpec": {
        "result": "OpenSpec is redundant for planted spec drift; the smallest check is a requirement and behavior-token cross-check.",
    },
    "SpecGov": {
        "result": "SpecGov is redundant for planted spec drift; the same local cross-check covers the seed.",
    },
    "GSD Core": {
        "result": "GSD Core is redundant for a stale resume hash; the skill states the rule and no executable enforces it.",
    },
    "Ruflo": {
        "result": "Ruflo is redundant for two writers; git merge reports a conflict.",
    },
    "Ruler": {
        "result": "Ruler is redundant for one checkout; the two skill copies have no byte-parity test.",
    },
    "BMAD-METHOD": {
        "result": "BMAD-METHOD is redundant for two acceptance commands; an unrun command stays an unfinished stop.",
    },
    "Superpowers": {
        "result": "Superpowers catalog growth is redundant for a stale recorded pass; the pinned skills do not compare a file hash.",
    },
    "Spec Kit": {
        "result": "Spec Kit already refuses resume of a running state; another restart product is redundant for that seed.",
    },
    "spec-gates": {
        "result": "spec-gates promotion is redundant for a planted verifier failure; the stop script asks for a followup.",
    },
    "Agent OS": {
        "result": "Agent OS is redundant for overlay row selection; the local selector keeps the unrelated path quiet.",
    },
    "Elephant Goldfish Model": {
        "result": "Elephant Goldfish Model stays uninstalled; no CI reviewer finds the planted defect, and a packet check can only reject an included author verdict.",
    },
    "Microsoft agent-governance-toolkit": {
        "result": "Microsoft agent-governance-toolkit is redundant here; a deny-list lookup covers a denied command and this kit does not run deployed agents.",
    },
    "coding-constitution": {
        "result": "coding-constitution is redundant for a hook-fire claim; an empty invocation record leaves the claim unsupported.",
    },
    "hindermath autonomous-run governance": {
        "result": "hindermath autonomous-run governance is redundant for content identity; two edits of the same path already produce different identities.",
    },
    "hindermath architecture governance": {
        "result": "hindermath architecture governance is redundant for a missing decision record; the ADR gate fails an architecture change that adds no numbered ADR.",
    },
    "contains-studio/agents": {
        "result": "contains-studio/agents is redundant for a role with no acceptance command; the smallest check is an acceptance command in the recipe.",
    },
}


def current_spec_findings(root: Path) -> list[str]:
    """Return findings from an executable spec/code checker, excluding this seed."""
    for path in (root / "ci").rglob("*.py"):
        if path.name in {"bebugging_seeds.py", "test_bebugging_seeds.py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "missing_from_spec" in text and "missing_from_code" in text:
            return ["checker-present"]
    return []


def local_spec_findings(spec_ids: list[str], code_tokens: list[str]) -> dict[str, list[str]]:
    """The smallest check that can express the planted spec drift."""
    spec = set(spec_ids)
    code = set(code_tokens)
    return {
        "missing_from_code": sorted(spec - code),
        "missing_from_spec": sorted(code - spec),
    }


def skill_marks_hash_mismatch_stale(root: Path) -> bool:
    text = (root / ".cursor/skills/governed-work/SKILL.md").read_text(encoding="utf-8")
    return "different hash" in text and "stale" in text


def resume_hash_is_executable(root: Path) -> bool:
    for path in (root / "ci").rglob("*.py"):
        if path.name in {"bebugging_seeds.py", "test_bebugging_seeds.py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "progress.md" in text and "different hash" in text:
            return True
    return False


def file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )


def two_writer_result() -> str:
    """Integrate two edits of the same line. Git must keep the conflict visible."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _git(root, "init", "-q", "-b", "main")
        _git(root, "config", "user.email", "seed@example.com")
        _git(root, "config", "user.name", "seed")
        _git(root, "config", "commit.gpgsign", "false")
        shared = root / "shared.txt"
        shared.write_text("base\n", encoding="utf-8")
        _git(root, "add", "shared.txt")
        _git(root, "commit", "-qm", "base")
        _git(root, "checkout", "-q", "-b", "writer-a")
        shared.write_text("left\n", encoding="utf-8")
        _git(root, "add", "shared.txt")
        _git(root, "commit", "-qm", "left")
        _git(root, "checkout", "-q", "main")
        shared.write_text("right\n", encoding="utf-8")
        _git(root, "add", "shared.txt")
        _git(root, "commit", "-qm", "right")
        merged = _git(root, "merge", "--no-edit", "writer-a")
        combined = merged.stdout + merged.stderr
        if merged.returncode != 0 and "CONFLICT" in combined:
            return "conflict"
        return "lost"


def instruction_copies_match(left: Path, right: Path) -> bool:
    return left.read_bytes() == right.read_bytes()


def parity_check_exists(root: Path) -> bool:
    left = '.cursor/skills/governed-work/SKILL.md").read_bytes()'
    right = '.github/skills/governed-work/SKILL.md").read_bytes()'
    for path in (root / "ci").rglob("test_*.py"):
        if path.name == "test_bebugging_seeds.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if left in text and right in text:
            return True
    return False


def two_command_result() -> str:
    return classify_stop(
        {"decision": "allow", "verify_rc": 0, "detail": "pass"},
        "The second acceptance command was not run.",
    )


def overlay_selection(root: Path, path: str) -> list[str]:
    from ci.select_overlay_rows import select_rows

    text = (root / "governance/LOCAL_OVERLAY.md").read_text(encoding="utf-8")
    return [row.get("constraint", "") for row in select_rows(text, [path])]


def packet_excludes_author_verdict(text: str) -> bool:
    lowered = text.lower()
    return "author verdict" not in lowered and "proposed verdict" not in lowered


def review_finds_planted_defect(root: Path) -> bool:
    readme = (
        root / "research/experiments/fresh-context-review/README.md"
    ).read_text(encoding="utf-8")
    return "does **not** run agents in CI" not in readme


def gate_failure_result() -> str:
    """Plant a verifier that exits 2 and read the stop script's decision."""
    stop = Path(__file__).resolve().parents[2] / ".cursor/hooks/kit-verify-stop.sh"
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        verify = root / ".specify/gates/verify.sh"
        verify.parent.mkdir(parents=True)
        verify.write_text("#!/bin/sh\nprintf '%s\\n' 'verifier-said'\nexit 2\n", encoding="utf-8")
        verify.chmod(0o755)
        env = os.environ.copy()
        env["CURSOR_PROJECT_DIR"] = str(root)
        env.pop("CLAUDE_PROJECT_DIR", None)
        proc = subprocess.run(
            ["bash", str(stop)],
            input="{}",
            capture_output=True,
            text=True,
            timeout=15,
            env=env,
            cwd=root,
            check=False,
        )
    if proc.returncode != 0:
        return "error"
    payload = json.loads(proc.stdout)
    message = payload.get("followup_message", "")
    if "Quality gate failed" in message:
        return "followup"
    return "allow"


def running_resume_result() -> str:
    """Ask the pinned Spec Kit engine to resume a run left `running`."""
    root = Path(__file__).resolve().parents[2]
    python = root / ".tools/specify-venv/bin/python"
    if not python.is_file():
        return "unavailable"
    script = r"""
import json
import tempfile
from pathlib import Path
from specify_cli.workflows.engine import WorkflowEngine

with tempfile.TemporaryDirectory() as tmp:
    project = Path(tmp)
    run_id = "seedrunning1"
    dest = project / ".specify" / "workflows" / "runs" / run_id
    dest.mkdir(parents=True)
    (dest / "state.json").write_text(json.dumps({
        "run_id": run_id,
        "workflow_id": "speckit",
        "status": "running",
        "current_step_index": 0,
    }), encoding="utf-8")
    engine = WorkflowEngine(project)
    try:
        engine.resume(run_id)
    except ValueError as exc:
        text = str(exc)
        if "Cannot resume" in text and "running" in text:
            print("refused")
        else:
            print("other")
    else:
        print("resumed")
"""
    proc = subprocess.run(
        [str(python), "-c", script],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if proc.returncode != 0:
        return "error"
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    return lines[-1] if lines else "error"


def superpowers_compares_file_hash(root: Path) -> bool:
    base = root / "vendor/superpowers"
    if not base.is_dir():
        return False
    for path in base.rglob("*"):
        if path.suffix not in {".py", ".sh"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "sha256" in text.lower() and "progress.md" in text:
            return True
    return False


def content_identity_result() -> str:
    from ci.uncommitted_diff_identity import uncommitted_diff_identity

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _git(root, "init", "-q", "-b", "main")
        _git(root, "config", "user.email", "seed@example.com")
        _git(root, "config", "user.name", "seed")
        _git(root, "config", "commit.gpgsign", "false")
        _git(root, "config", "core.hooksPath", "/dev/null")
        payload = root / "payload.txt"
        payload.write_text("base\n", encoding="utf-8")
        _git(root, "add", "payload.txt")
        _git(root, "commit", "-qm", "base")
        payload.write_text("left\n", encoding="utf-8")
        first = uncommitted_diff_identity(root)
        payload.write_text("right\n", encoding="utf-8")
        second = uncommitted_diff_identity(root)
        payload.write_text("right\n", encoding="utf-8")
        third = uncommitted_diff_identity(root)
    if first != second and second == third and first not in {"clean", "unknown"}:
        return "distinct"
    return "same"


def architecture_record_result(kind: str) -> str:
    from ci.gate_tests.test_reference_gates import ADR_CHECKS

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _git(root, "init", "-q", "-b", "main")
        _git(root, "config", "user.email", "seed@example.com")
        _git(root, "config", "user.name", "seed")
        _git(root, "config", "commit.gpgsign", "false")
        _git(root, "config", "core.hooksPath", "/dev/null")
        (root / "constitution").mkdir()
        (root / "adr").mkdir()
        (root / "constitution/RULES.md").write_text("Original rule\n", encoding="utf-8")
        (root / "adr/ADR_0001_Existing.md").write_text(
            "# Existing decision\n\nAccepted rationale.\n",
            encoding="utf-8",
        )
        _git(root, "add", "-A")
        _git(root, "commit", "-qm", "base")
        base = _git(root, "rev-parse", "HEAD").stdout.strip()
        if kind == "architecture":
            target = root / "architecture/boundary.md"
            target.parent.mkdir()
            target.write_text("Boundary changed\n", encoding="utf-8")
        elif kind == "usage":
            target = root / "usage/example.md"
            target.parent.mkdir()
            target.write_text("Documentation only\n", encoding="utf-8")
        else:
            raise ValueError(kind)
        _git(root, "add", "-A")
        _git(root, "commit", "-qm", "change")
        head = _git(root, "rev-parse", "HEAD").stdout.strip()
        env = os.environ.copy()
        env["BASE_SHA"] = base
        env["HEAD_SHA"] = head
        proc = subprocess.run(
            ["bash", "-c", ADR_CHECKS[0]],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    if proc.returncode != 0:
        return "caught"
    return "quiet"


def current_runtime_gate(root: Path) -> bool:
    for path in (root / "ci").rglob("*.py"):
        if path.name in {"bebugging_seeds.py", "test_bebugging_seeds.py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "denied_commands" in text and "deploy.sh" in text:
            return True
    return False


def runtime_decision(command: str) -> str:
    if command in {"deploy.sh"}:
        return "deny"
    return "allow"


def dispatch_claim_is_enforced(root: Path) -> bool:
    for path in (root / "ci").rglob("test_*.py"):
        if path.name == "test_bebugging_seeds.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "dispatch_claim_result" in text:
            return True
    return False


def dispatch_claim_result(claimed: bool, record: str) -> str:
    if claimed and not record.strip():
        return "unsupported"
    return "recorded"


def catalog_acceptance_is_enforced(root: Path) -> bool:
    for path in (root / "ci").rglob("test_*.py"):
        if path.name == "test_bebugging_seeds.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "Acceptance command:" in text and "recipe_acceptance" in text:
            return True
    return False


def recipe_acceptance(text: str) -> str:
    if "acceptance command:" in text.lower():
        return "present"
    return "absent"
