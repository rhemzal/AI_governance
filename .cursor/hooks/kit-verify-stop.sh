#!/usr/bin/env bash
# shellcheck shell=bash
# Cursor stop hook — agent boundary via spec-gates verify.sh (kit adapter).
set -euo pipefail

INPUT="$(cat 2>/dev/null || true)"

if command -v jq >/dev/null 2>&1; then
  if [[ "$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null)" == "true" ]]; then
    exit 0
  fi
fi

# Prefer git root; ignore CLAUDE_PROJECT_DIR from unrelated pilot shells.
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
VERIFY="$PROJECT_ROOT/.specify/gates/verify.sh"

[[ -x "$VERIFY" ]] || exit 0

set +e
OUTPUT="$("$VERIFY" --boundary agent 2>&1)"
RC=$?
set -e

case "$RC" in
  2)
    {
      printf '%s\n\n' "$OUTPUT"
      echo "Quality gate failed at the agent boundary. Fix the issues above before stopping."
    } >&2
    exit 2
    ;;
  0)
    printf '%s\n' "$OUTPUT"
    exit 0
    ;;
  *)
    printf 'gates: verify.sh could not run (exit %s); allowing stop.\n%s\n' \
      "$RC" "$OUTPUT" >&2
    exit 0
    ;;
esac
