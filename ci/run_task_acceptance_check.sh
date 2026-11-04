#!/usr/bin/env bash
# Run the task acceptance command and record native execution evidence.
#
# Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
#
# Usage (from repository root):
#   bash ci/run_task_acceptance_check.sh
#
# Environment:
#   TASK_ACCEPTANCE_CMD   Shell command to run (required for adopters; kit default when unset)
#   TASK_ACCEPTANCE_EVIDENCE  Output markdown path (optional)
#   TASK_ACCEPTANCE_LOG   Command log path (optional; defaults beside evidence)
#   SPECIFY_FEATURE       When set, default evidence goes under specs/<feature>/
#
# Exit code matches the acceptance command. A report-shaped file is written even
# on failure so reviewers can see what ran; outcome lines reflect the real exit code.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CMD="${TASK_ACCEPTANCE_CMD:-}"
if [[ -z "${CMD//[[:space:]]/}" ]]; then
  CMD="$(bash "$SCRIPT_DIR/kit_maintenance_acceptance_cmd.sh")"
fi

case "${CMD//[[:space:]]/}" in
  true|:)
    echo "run_task_acceptance_check: refusing a no-op acceptance command" >&2
    exit 2
    ;;
esac
if [[ "$CMD" =~ ^[[:space:]]*exit[[:space:]]+0[[:space:]]*$ ]]; then
  echo "run_task_acceptance_check: refusing a no-op acceptance command" >&2
  exit 2
fi

EVIDENCE_PATH="${TASK_ACCEPTANCE_EVIDENCE:-}"
if [[ -z "$EVIDENCE_PATH" ]]; then
  if [[ -n "${SPECIFY_FEATURE:-}" ]]; then
    EVIDENCE_PATH="specs/${SPECIFY_FEATURE}/acceptance-run-evidence.md"
  else
    EVIDENCE_PATH=".specify/acceptance-run-evidence.latest.md"
  fi
fi

LOG_FILE="${TASK_ACCEPTANCE_LOG:-${EVIDENCE_PATH%.md}.log}"
mkdir -p "$(dirname "$EVIDENCE_PATH")" "$(dirname "$LOG_FILE")"

COMMIT="$(git rev-parse HEAD 2>/dev/null || echo unknown)"
REMOTE="$(git config --get remote.origin.url 2>/dev/null || echo unknown)"
DIRTY_ID="$(python3 "$SCRIPT_DIR/uncommitted_diff_identity.py" "$ROOT")"

set +e
bash -lc "$CMD" >"$LOG_FILE" 2>&1
EXIT=$?
set -e

if [[ "$EXIT" -eq 0 ]]; then
  OUTCOME="VERIFIED"
else
  OUTCOME="BLOCKED"
fi

python3 - <<'PY' "$EVIDENCE_PATH" "$LOG_FILE" "$CMD" "$EXIT" "$OUTCOME" "$COMMIT" "$REMOTE" "$DIRTY_ID"
import sys
from pathlib import Path

(
    evidence_path,
    log_file,
    command,
    exit_code,
    outcome,
    commit,
    remote,
    dirty_id,
) = sys.argv[1:]

body = f"""### AI RUN EVIDENCE
- Model/tooling context (high level, no secrets):
  - Assistant/tool: native shell acceptance runner (`ci/run_task_acceptance_check.sh`)
  - Execution mode: workflow or direct invocation
  - Key constraints/rules consulted: task mandate acceptance command (pre-selected)
- Task outcome: {outcome}
- Acceptance criteria: see feature spec / task mandate; this file records only the executed check
- Tested state:
  - Repository and exact commit(s): {remote} @ {commit}
  - Uncommitted diff identity (if any): {dirty_id}
  - Environment, relevant configuration, hardware/fixture identity: local host shell
- Checks run:
  - Command/check: {command}
  - Result: exit {exit_code}
- Artifacts/logs:
  - Local evidence (if any): {log_file}
- Assumptions:
  - The command above was chosen before its outcome was known
- Known limitations:
  - This file does not authenticate the producer or scan referenced artifacts
- Unverified or stale checks, and why:
  - Outcome is historical if the tree changes after this run
- Merge/deployment authorization (separate from verification):
  - Not recorded here
"""
Path(evidence_path).write_text(body, encoding="utf-8")
PY

exit "$EXIT"
