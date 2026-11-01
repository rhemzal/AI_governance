#!/usr/bin/env bash
# shellcheck shell=bash
# Cursor stop hook for the experimental spec-gates adapter.
#
# Host contract observed in Cursor IDE 3.27.22
# (commit b1aa50cb6db84fd3e8c808259cb172ea73425c10) and the same stop mapping
# in Cursor Agent CLI 2026.10.01-e373342:
#   stdin is JSON. The native loop counter is loop_count (starts at 0).
#   This host does not send stop_hook_active.
#   stdout must be one JSON object. {"followup_message":"..."} is the next
#   user turn. {} allows the stop.
#   Exit 2 does not continue a stop hook. The host drops the reason and
#   substitutes {}. Always exit 0 after writing the JSON object.
# The hook entry's loop_limit (default 5) skips this script once loop_count
# reaches it. Each invocation the host still runs re-checks the gate.
# stop_hook_active is honored only as a Claude-compatible loop guard.
set -euo pipefail

INPUT="$(cat 2>/dev/null || true)"

emit() {
  KIND="$1" FOLLOWUP_MSG="${2:-}" python3 -c '
import json, os, sys
kind = os.environ["KIND"]
if kind == "followup":
    json.dump({"followup_message": os.environ.get("FOLLOWUP_MSG", "")}, sys.stdout)
else:
    json.dump({}, sys.stdout)
sys.stdout.write("\n")
'
}

if [[ -n "${CURSOR_PROJECT_DIR:-}" && -d "${CURSOR_PROJECT_DIR}" ]]; then
  PROJECT_ROOT="${CURSOR_PROJECT_DIR}"
else
  PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
fi

loop_state="$(printf '%s' "$INPUT" | python3 -c '
import json, sys
raw = sys.stdin.read()
try:
    data = json.loads(raw) if raw.strip() else {}
except Exception:
    data = {}
if not isinstance(data, dict):
    data = {}
if data.get("stop_hook_active") is True:
    print("claude-active")
else:
    try:
        count = int(data.get("loop_count") or 0)
    except Exception:
        count = 0
    print("count:%s" % count)
' 2>/dev/null || printf '%s\n' "count:0")"

record() {
  local decision="$1" verify_rc="$2" detail="$3"
  local marker="$PROJECT_ROOT/.cursor/hooks/record-stop-invocations"
  [[ -f "$marker" ]] || return 0
  DECISION="$decision" VERIFY_RC="$verify_rc" DETAIL="$detail" \
    LOOP_STATE="$loop_state" CURSOR_VERSION="${CURSOR_VERSION:-}" \
    PROJECT_ROOT="$PROJECT_ROOT" python3 -c '
import json, os
from datetime import datetime, timezone
path = os.path.join(os.environ["PROJECT_ROOT"], ".cursor", "hooks", "stop-invocations.jsonl")
row = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "source": "cursor",
    "cursor_version": os.environ.get("CURSOR_VERSION") or None,
    "loop_state": os.environ.get("LOOP_STATE"),
    "decision": os.environ.get("DECISION"),
    "verify_rc": int(os.environ.get("VERIFY_RC") or "0"),
    "detail": os.environ.get("DETAIL") or "",
}
with open(path, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(row, ensure_ascii=True) + "\n")
' || true
}

finish() {
  record "$1" "$2" "$3"
  if [[ "$1" == "followup" ]]; then
    emit followup "$4"
  else
    emit allow
  fi
  exit 0
}

if [[ "$loop_state" == "claude-active" ]]; then
  printf '%s\n' "gates: stop_hook_active set; allowing stop." >&2
  finish allow 0 "claude-loop-guard" ""
fi

VERIFY="$PROJECT_ROOT/.specify/gates/verify.sh"
if [[ ! -x "$VERIFY" ]]; then
  printf '%s\n' "gates: verify.sh missing; allowing stop." >&2
  finish allow 0 "missing-verify" ""
fi

set +e
OUTPUT="$(
  cd "$PROJECT_ROOT"
  unset CLAUDE_PROJECT_DIR CURSOR_PROJECT_DIR
  "$VERIFY" --boundary agent 2>&1
)"
RC=$?
set -e

case "$RC" in
  0)
    finish allow 0 "pass" ""
    ;;
  2)
    MSG="$(printf '%s\n\nQuality gate failed at the agent boundary. Fix the issues above before stopping.' "$OUTPUT")"
    MSG="$(printf '%s' "$MSG" | python3 -c 'import sys; t=sys.stdin.read(); sys.stdout.write(t[-6000:] if len(t)>6000 else t)')"
    finish followup 2 "gate-failed" "$MSG"
    ;;
  *)
    printf 'gates: verify.sh could not run (exit %s); allowing stop.\n%s\n' "$RC" "$OUTPUT" >&2
    finish allow "$RC" "unavailable" ""
    ;;
esac
