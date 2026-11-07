#!/usr/bin/env bash
# Report opt-in stack installation completeness and what still fails at runtime.
#
#   bash governance/experimental/spec_gates/check-opt-in-stack.sh
#   bash governance/experimental/spec_gates/check-opt-in-stack.sh --strict   # exit 1 if any gap
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"
STRICT=0
for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=1 ;;
    -h | --help)
      sed -n '1,8p' "$0"
      exit 0
      ;;
  esac
done

MISSING=0
WARN=0

note() { echo "  [ok] $*"; }
warn() {
  echo "  [gap] $*"
  WARN=$((WARN + 1))
}
fail() {
  echo "  [missing] $*"
  MISSING=$((MISSING + 1))
}

echo "opt-in-stack check (repository: $ROOT)"
echo

echo "Phase A — policy snapshot (import bundle, not the procedure pin alone)"
if [[ -d vendor/AI_governance ]]; then
  note "vendor/AI_governance present"
else
  warn "no vendor/AI_governance — run install-opt-in-stack.sh for a first import, or readopt"
fi
if [[ -d vendor/AI_governance.next ]]; then
  fail "vendor/AI_governance.next waiting — review readopt-report and run install with --switch-snapshot"
fi

echo
echo "Phase B — Superpowers pin (required for executing-plans / governed procedures)"
if [[ -d vendor/superpowers/v7.0.2 ]]; then
  note "vendor/superpowers/v7.0.2 present"
  if [[ -f vendor/superpowers/v7.0.2/SHA256SUMS ]]; then
    if ( cd vendor/superpowers/v7.0.2 && sha256sum -c SHA256SUMS >/dev/null 2>&1 ); then
      note "Superpowers SHA256SUMS verify"
    else
      warn "Superpowers SHA256SUMS failed — pin may be corrupt; re-copy from kit HOW_TO_IMPORT"
    fi
  else
    warn "no SHA256SUMS in pin"
  fi
else
  fail "no vendor/superpowers/v7.0.2 — copy pin per usage/HOW_TO_IMPORT.md § Opt-in work procedures (install-opt-in-stack does not copy it)"
fi

echo
echo "Phase C — agent routing (skills + intuitive AEP execution)"
if [[ -f .cursor/skills/governed-work/SKILL.md ]]; then
  note "governed-work skill entry"
else
  warn "no .cursor/skills/governed-work/SKILL.md — run procedure copy or install-opt-in-stack --stack-only"
fi
if [[ -f .cursor/rules/autonomous-aep-execution.mdc ]]; then
  note "alwaysApply autonomous AEP rule (.cursor/rules/autonomous-aep-execution.mdc)"
else
  warn "no alwaysApply AEP rule — natural-language 'finish the AEP' may not run inline; copy template from kit or re-run stack install"
fi
if grep -q "autonomous-aep-execution\|Active autonomous\|inline completion" AGENTS.md 2>/dev/null; then
  note "AGENTS.md mentions autonomous / AEP execution (review text)"
else
  warn "AGENTS.md has no autonomous mandate pointer — merge host mandate; skills alone do not grant authority"
fi
if [[ -f .github/skills/governed-work/SKILL.md ]]; then
  note "VS Code governed-work skill entry"
else
  warn "no .github/skills/governed-work/SKILL.md — install the VS Code workspace route"
fi
if grep -qF '<!-- AI Governance Tier C route -->' .github/copilot-instructions.md 2>/dev/null; then
  note "VS Code Copilot instruction route"
else
  warn "no VS Code Copilot instruction route in .github/copilot-instructions.md"
fi

echo
echo "Phase D — acceptance + workflow + gates"
if [[ -x ci/adopter_task_acceptance_cmd.sh ]]; then
  note "ci/adopter_task_acceptance_cmd.sh"
else
  warn "no generated acceptance wrapper — set ADOPTER_VERIFY_COMMAND and run install-opt-in-stack"
fi
if [[ -x ci/run_task_acceptance_check.sh ]]; then
  note "ci/run_task_acceptance_check.sh"
else
  warn "missing ci/run_task_acceptance_check.sh"
fi
if [[ -f .specify/workflows/ai-governance/workflow.yml ]]; then
  note "ai-governance workflow (verify-acceptance step)"
else
  warn "no .specify/workflows/ai-governance/workflow.yml"
fi
if [[ -x .tools/specify-venv/bin/specify ]]; then
  note "specify CLI venv (.tools/specify-venv)"
else
  warn "no .tools/specify-venv — specify workflow run will fail; run stack install"
fi
if [[ -x .specify/gates/verify.sh ]]; then
  note "projected spec-gates (.specify/gates/verify.sh)"
else
  warn "spec-gates not projected — pre-commit / Stop hook verify may be absent"
fi
if [[ -f .cursor/hooks.json ]] && grep -q '"stop"' .cursor/hooks.json 2>/dev/null; then
  note "Cursor Stop hook configured"
else
  warn "no Stop hook in .cursor/hooks.json"
fi
if python3 - <<'PY' >/dev/null 2>&1
import json
from pathlib import Path

path = Path(".github/hooks/ai-governance.json")
try:
    config = json.loads(path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    raise SystemExit(1)
if not isinstance(config, dict) or config.get("version") != 1:
    raise SystemExit(1)
hooks = config.get("hooks")
if not isinstance(hooks, dict) or not isinstance(hooks.get("agentStop"), list):
    raise SystemExit(1)
expected_commands = {
    "bash": "python3 .github/hooks/kit-verify-stop.py",
    "powershell": "py -3 .github/hooks/kit-verify-stop.py",
}
verifier_timeout_seconds = 140  # Keep aligned with VERIFY_TIMEOUT_SECONDS in the adapter.
for hook in hooks["agentStop"]:
    if (
        isinstance(hook, dict)
        and hook.get("type") == "command"
        and hook.get("cwd") == "."
        and all(hook.get(shell) == command for shell, command in expected_commands.items())
        and type(hook.get("timeoutSec")) is int
        and hook["timeoutSec"] > verifier_timeout_seconds
    ):
        raise SystemExit(0)
raise SystemExit(1)
PY
then
  if [[ -f .github/hooks/kit-verify-stop.py ]]; then
    note "VS Code Copilot agentStop hook configured"
  else
    warn "VS Code agentStop config exists but kit-verify-stop.py is missing"
  fi
else
  warn "no valid VS Code Copilot agentStop hook in .github/hooks/ai-governance.json"
fi
if [[ -s .github/hooks/stop-invocations.jsonl ]]; then
  note "VS Code hook invocation log present — correlate with a fresh Copilot session and host version"
else
  warn "native VS Code Copilot dispatch is unverified — run a fresh Copilot session; config and tests do not prove dispatch"
fi

echo
echo "Phase E — operator habits"
if [[ -f scripts/activate-governance-specify-env.sh ]]; then
  note "scripts/activate-governance-specify-env.sh (source before specify workflow)"
else
  warn "no activate-governance-specify-env.sh helper"
fi

echo
TOTAL=$((MISSING + WARN))
if [[ "$MISSING" -gt 0 ]]; then
  echo "Summary: $MISSING blocking gap(s), $WARN advisory gap(s). Fix [missing] before expecting full stack behavior."
  echo "See governance/experimental/spec_gates/OPT_IN_STACK.md § Installation completeness."
  [[ "$STRICT" == 1 ]] && exit 1
  exit 0
fi
if [[ "$WARN" -gt 0 ]]; then
  echo "Summary: install usable with $WARN advisory gap(s). Some features will feel 'broken' until gaps are closed."
  [[ "$STRICT" == 1 ]] && exit 1
  exit 0
fi
echo "Summary: no gaps reported by this check (does not prove agent behavior or CI wiring)."
