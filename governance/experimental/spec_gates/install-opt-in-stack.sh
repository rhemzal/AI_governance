#!/usr/bin/env bash
# Install full governance opt-in stack in an adopter or kit dogfood repo:
# readopt (optional), work procedures, spec-gates 0.5.1, Cursor Stop hook, specify venv.
#
# Copy this script to the host (e.g. scripts/) or run from a pinned KIT_SOURCE checkout:
#   bash "$KIT_SOURCE/governance/experimental/spec_gates/install-opt-in-stack.sh" …
#
# Required environment:
#   ADOPTER_VERIFY_COMMAND   Shell command for task acceptance and spec-gates gate (chosen before use)
#   KIT_SOURCE               Path to clean AI_governance checkout (defaults to kit root when detected)
#   KIT_REVISION             Full commit SHA of that checkout (must match HEAD)
#
# Readopt (when vendor/AI_governance exists):
#   PREVIOUS_KIT_SHA         Prior imported kit SHA
#   ADOPTER_BUNDLES          Space-separated bundles (default: standard research)
#
# Optional:
#   ADOPTER_GATE_ID          Policy gate name (default: adopter-verify)
#   ADOPTER_GATE_TIMEOUT_S   Gate timeout seconds (default: 130)
#   SKIP_READOPT=1           Skip import_bundle readopt
#   SKIP_SPEC_GATES=1        Skip install-and-project.sh
#
# Usage:
#   …/install-opt-in-stack.sh              # new tree: first import + pin + stack
#                                          # existing snapshot: readopt, then stop for review
#   …/install-opt-in-stack.sh --switch-snapshot
#   …/install-opt-in-stack.sh --bootstrap  # snapshot, pin, overlay, AGENTS; no downloads
#   …/install-opt-in-stack.sh --import-only
#   …/install-opt-in-stack.sh --stack-only # refresh stack without readopt
#   …/check-opt-in-stack.sh [--strict]     # report gaps (see OPT_IN_STACK.md)
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ADOPTER_GATE_ID="${ADOPTER_GATE_ID:-adopter-verify}"
ADOPTER_GATE_TIMEOUT_S="${ADOPTER_GATE_TIMEOUT_S:-130}"
ADOPTER_BUNDLES="${ADOPTER_BUNDLES:-standard research}"
export PATH="${HOME}/.local/bin:${PATH}"

usage() {
  sed -n '2,36p' "$0"
  exit "${1:-0}"
}

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "install-opt-in-stack: missing command: $1" >&2
    exit 1
  }
}

check_prereqs() {
  local need_downloads="${1:-0}"
  need git
  need sha256sum
  need python3
  if [[ "$need_downloads" == 1 ]]; then
    need curl
    need uv
  fi
  if ! command -v yq >/dev/null 2>&1 || ! yq --version 2>&1 | grep -q mikefarah; then
    if ! python3 -c 'import yaml' >/dev/null 2>&1; then
      echo "install-opt-in-stack: need mikefarah yq or python3-yaml to read kit-manifest.yml" >&2
      exit 1
    fi
  fi
  : "${ADOPTER_VERIFY_COMMAND:?Set ADOPTER_VERIFY_COMMAND to the project acceptance shell command}"
  if [[ -z "${ADOPTER_VERIFY_COMMAND//[[:space:]]/}" ]]; then
    echo "install-opt-in-stack: ADOPTER_VERIFY_COMMAND is empty" >&2
    exit 1
  fi
}

same_tree() {
  [[ "$(cd "$ROOT" && pwd -P)" == "$(cd "$KIT_SOURCE" && pwd -P)" ]]
}

detect_kit_source() {
  if [[ -n "${KIT_SOURCE:-}" ]]; then
    return 0
  fi
  if [[ -f "$ROOT/ci/import_bundle.py" && -f "$ROOT/kit-manifest.yml" ]]; then
    KIT_SOURCE="$ROOT"
    export KIT_SOURCE
  fi
}

require_kit_env() {
  detect_kit_source
  : "${KIT_SOURCE:?Set KIT_SOURCE to AI_governance checkout}"
  if [[ -z "${KIT_REVISION:-}" ]]; then
    KIT_REVISION="$(git -C "$KIT_SOURCE" rev-parse HEAD)"
    export KIT_REVISION
  fi
  test -d "$KIT_SOURCE"
  test "$(git -C "$KIT_SOURCE" rev-parse HEAD)" = "$KIT_REVISION"
  git -C "$KIT_SOURCE" diff --exit-code HEAD --
}

dependencies_constraint_path() {
  local vend="$ROOT/vendor/AI_governance/research/experiments/spec_kit_spec_gates/dependencies.txt"
  local kit="$KIT_SOURCE/research/experiments/spec_kit_spec_gates/dependencies.txt"
  if [[ -f "$vend" ]]; then
    echo "$vend"
  elif [[ -f "$kit" ]]; then
    echo "$kit"
  else
    echo "install-opt-in-stack: missing dependencies.txt (import research bundle or copy from kit)" >&2
    exit 1
  fi
}

write_manifest_json() {
  local dest="$1"
  if command -v yq >/dev/null 2>&1 && yq --version 2>&1 | grep -q mikefarah; then
    yq -o=json . "$KIT_SOURCE/kit-manifest.yml" >"$dest"
    return 0
  fi
  python3 - "$KIT_SOURCE/kit-manifest.yml" "$dest" <<'PY'
import json, sys
from pathlib import Path
import yaml
src, dest = sys.argv[1:]
data = yaml.safe_load(Path(src).read_text(encoding="utf-8"))
Path(dest).write_text(json.dumps(data), encoding="utf-8")
PY
}

run_first_import() {
  if same_tree; then
    echo "install-opt-in-stack: KIT_SOURCE is this checkout; first import would nest the kit. Use --stack-only for dogfood." >&2
    exit 1
  fi
  if [[ -e "$ROOT/vendor/AI_governance" || -L "$ROOT/vendor/AI_governance" ]]; then
    echo "install-opt-in-stack: vendor/AI_governance exists — use readopt, not first import" >&2
    exit 1
  fi
  mkdir -p "$ROOT/vendor"
  local json bundles=() args=() b
  json="$(mktemp)"
  write_manifest_json "$json"
  read -r -a bundles <<<"$ADOPTER_BUNDLES"
  args=(--manifest-json "$json" --source "$KIT_SOURCE" --destination "$ROOT/vendor/AI_governance")
  for b in "${bundles[@]}"; do
    args+=(--bundle "$b")
  done
  python3 "$KIT_SOURCE/ci/import_bundle.py" "${args[@]}"
  python3 "$KIT_SOURCE/ci/import_bundle.py" "${args[@]}" --check
  rm -f "$json"
  echo "install-opt-in-stack: first import verified at $KIT_REVISION"
}

install_procedure_pin() {
  if same_tree; then
    return 0
  fi
  local pin="$ROOT/vendor/superpowers/v7.0.2"
  local src="$KIT_SOURCE/vendor/superpowers/v7.0.2"
  if [[ -e "$pin" || -L "$pin" ]]; then
    echo "install-opt-in-stack: keeping existing Superpowers pin"
  else
    test -d "$src"
    mkdir -p "$ROOT/vendor/superpowers"
    cp -aL "$src" "$pin"
    ( cd "$pin" && sha256sum -c SHA256SUMS )
    echo "install-opt-in-stack: copied Superpowers pin"
  fi
  local skill="$ROOT/.cursor/skills/governed-work/SKILL.md"
  if [[ -e "$skill" || -L "$skill" ]]; then
    echo "install-opt-in-stack: keeping existing governed-work skill"
  else
    mkdir -p "$ROOT/.cursor/skills/governed-work"
    cp -L "$KIT_SOURCE/.cursor/skills/governed-work/SKILL.md" "$skill"
    test ! -L "$skill"
  fi
}

seed_host_entry() {
  if same_tree; then
    return 0
  fi
  local template="$KIT_SOURCE/governance/LOCAL_OVERLAY_TEMPLATE.md"
  local overlay="$ROOT/governance/LOCAL_OVERLAY.md"
  if [[ ! -e "$overlay" && ! -L "$overlay" ]]; then
    mkdir -p "$ROOT/governance"
    cp -L "$template" "$overlay"
    cat >>"$overlay" <<EOF

## Installed by opt-in stack

- Kit revision: \`$KIT_REVISION\`
- Bundles: $ADOPTER_BUNDLES
- Acceptance command: \`$ADOPTER_VERIFY_COMMAND\`
- Push or merge requires that command recorded through \`ci/run_task_acceptance_check.sh\`, even when the agent does not invoke \`/governed-work\`.
- Tier C does not sandbox the agent shell. A gitignored tool root still needs an explicit mandate.
EOF
    echo "install-opt-in-stack: seeded governance/LOCAL_OVERLAY.md"
  else
    echo "install-opt-in-stack: keeping existing governance/LOCAL_OVERLAY.md"
  fi
  local block="$KIT_SOURCE/usage/templates/AGENTS_GOVERNANCE_OPT_IN_BLOCK.md"
  local agents="$ROOT/AGENTS.md"
  if [[ -f "$agents" ]] && grep -q '## Governance baseline' "$agents"; then
    echo "install-opt-in-stack: keeping existing AGENTS.md governance block"
    return 0
  fi
  if [[ ! -e "$agents" ]]; then
    printf '%s\n\n' '# Agent instructions' >"$agents"
  fi
  sed "s/<KIT_REVISION>/$KIT_REVISION/g" "$block" >>"$agents"
  echo "install-opt-in-stack: appended governance baseline to AGENTS.md"
}

run_readopt() {
  : "${PREVIOUS_KIT_SHA:?Set PREVIOUS_KIT_SHA for readopt}"
  test -d "$ROOT/vendor/AI_governance" || {
    echo "install-opt-in-stack: no vendor/AI_governance — skip readopt or use first import" >&2
    exit 1
  }
  test ! -e "$ROOT/vendor/AI_governance.next" || {
    echo "install-opt-in-stack: remove or switch vendor/AI_governance.next first" >&2
    exit 1
  }
  rm -f "$ROOT/vendor/AI_governance.readopt-report.md"
  local json bundles=()
  json="$(mktemp)"
  trap 'rm -f "$json"' RETURN
  write_manifest_json "$json"
  read -r -a bundles <<<"$ADOPTER_BUNDLES"
  local args=(--manifest-json "$json" --source "$KIT_SOURCE" --destination "$ROOT" --readopt --previous "$PREVIOUS_KIT_SHA")
  local b
  for b in "${bundles[@]}"; do
    args+=(--bundle "$b")
  done
  python3 "$KIT_SOURCE/ci/import_bundle.py" "${args[@]}"
  echo "install-opt-in-stack: readopt wrote vendor/AI_governance.next — review readopt-report.md before --switch-snapshot"
}

switch_snapshot() {
  test -d "$ROOT/vendor/AI_governance.next" || {
    echo "install-opt-in-stack: no vendor/AI_governance.next" >&2
    exit 1
  }
  if test -d "$ROOT/vendor/AI_governance"; then
    rm -rf "$ROOT/vendor/AI_governance.prev"
    mv "$ROOT/vendor/AI_governance" "$ROOT/vendor/AI_governance.prev"
  fi
  mv "$ROOT/vendor/AI_governance.next" "$ROOT/vendor/AI_governance"
  if ! grep -qxF 'vendor/AI_governance.prev/' "$ROOT/.gitignore" 2>/dev/null; then
    echo 'vendor/AI_governance.prev/' >>"$ROOT/.gitignore"
  fi
}

ensure_dependencies_txt() {
  local kit="$KIT_SOURCE/research/experiments/spec_kit_spec_gates/dependencies.txt"
  local dest="$ROOT/vendor/AI_governance/research/experiments/spec_kit_spec_gates/dependencies.txt"
  if [[ -f "$kit" && -d "$ROOT/vendor/AI_governance" && ! -f "$dest" ]]; then
    mkdir -p "$(dirname "$dest")"
    cp -L "$kit" "$dest"
  fi
}

install_host_adapter() {
  mkdir -p "$ROOT/governance/experimental"
  cp -a "$KIT_SOURCE/governance/experimental/spec_gates" "$ROOT/governance/experimental/"
  local dep
  dep="$(dependencies_constraint_path)"
  if [[ "$dep" == "$ROOT/vendor/"* ]]; then
    sed -i "s|\$root/research/experiments/spec_kit_spec_gates/dependencies.txt|\$root/vendor/AI_governance/research/experiments/spec_kit_spec_gates/dependencies.txt|" \
      "$ROOT/governance/experimental/spec_gates/install-and-project.sh" 2>/dev/null || true
  fi
  write_adopter_policy "$ROOT/governance/experimental/spec_gates/policy.adopter.json"
  cp "$ROOT/governance/experimental/spec_gates/policy.adopter.json" \
    "$ROOT/governance/experimental/spec_gates/policy.kit.json"
}

write_adopter_policy() {
  local out="$1"
  python3 - "$out" "$ADOPTER_GATE_ID" "$ADOPTER_VERIFY_COMMAND" "$ADOPTER_GATE_TIMEOUT_S" <<'PY'
import json, sys
from pathlib import Path
out, gate_id, cmd, timeout_s = sys.argv[1:5]
data = {
    "hooks": {
        "verify-quality": {
            "orchestrator": "none",
            "severity": "error",
            "gates": {
                gate_id: {"command": cmd, "timeout_s": int(timeout_s)},
            },
        }
    },
    "git": {
        "block_main_commits": False,
        "conventional_commits": False,
        "forbid_ai_isms": False,
        "protected_change_trailer": False,
    },
    "spec": {"enabled": False},
    "attestation": {"enabled": True, "parity": "error"},
}
Path(out).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY
}

write_adopter_acceptance_cmd() {
  mkdir -p "$ROOT/ci"
  local out="$ROOT/ci/adopter_task_acceptance_cmd.sh"
  python3 - "$out" "$ADOPTER_VERIFY_COMMAND" <<'PY'
import shlex, sys
from pathlib import Path
out, cmd = sys.argv[1], sys.argv[2]
body = f"""#!/usr/bin/env bash
set -euo pipefail
exec bash -c {shlex.quote(cmd)}
"""
Path(out).write_text(body, encoding="utf-8")
PY
  chmod +x "$out"
}

install_procedures_and_ci() {
  mkdir -p "$ROOT/scripts" "$ROOT/.cursor/skills/governed-work" "$ROOT/.specify/presets" \
    "$ROOT/.specify/workflows/ai-governance" "$ROOT/.specify/scripts/bash" "$ROOT/ci" "$ROOT/.cursor/hooks"
  cp -L "$KIT_SOURCE/.cursor/skills/governed-work/SKILL.md" "$ROOT/.cursor/skills/governed-work/"
  mkdir -p "$ROOT/.cursor/rules"
  if [[ ! -f "$ROOT/.cursor/rules/autonomous-aep-execution.mdc" ]]; then
    cp -L "$SCRIPT_DIR/templates/autonomous-aep-execution.mdc.template" \
      "$ROOT/.cursor/rules/autonomous-aep-execution.mdc"
    echo "install-opt-in-stack: installed .cursor/rules/autonomous-aep-execution.mdc (alwaysApply)"
  else
    echo "install-opt-in-stack: keeping existing .cursor/rules/autonomous-aep-execution.mdc"
  fi
  if [[ -d "$KIT_SOURCE/.specify/presets/ai-governance" ]]; then
    cp -aL "$KIT_SOURCE/.specify/presets/ai-governance" "$ROOT/.specify/presets/"
  fi
  cp -L "$KIT_SOURCE/.specify/workflows/ai-governance/workflow.yml" "$ROOT/.specify/workflows/ai-governance/"
  cp -L "$KIT_SOURCE/.specify/workflows/workflow-registry.json" "$ROOT/.specify/workflows/"
  cp -L "$KIT_SOURCE/.specify/scripts/bash/run-task-acceptance-check.sh" "$ROOT/.specify/scripts/bash/"
  cp -L "$KIT_SOURCE/ci/run_task_acceptance_check.sh" "$ROOT/ci/"
  chmod +x "$ROOT/ci/run_task_acceptance_check.sh" "$ROOT/.specify/scripts/bash/run-task-acceptance-check.sh"
  write_adopter_acceptance_cmd
  cp -L "$KIT_SOURCE/.cursor/hooks/kit-verify-stop.sh" "$ROOT/.cursor/hooks/"
  cp -L "$KIT_SOURCE/.cursor/hooks.json" "$ROOT/.cursor/hooks.json"
  chmod +x "$ROOT/.cursor/hooks/kit-verify-stop.sh"
  python3 - <<'PY'
import json
from pathlib import Path
path = Path(".specify/presets/.registry")
if path.is_file():
    data = json.loads(path.read_text(encoding="utf-8"))
else:
    data = {"schema_version": "1.0", "presets": {}}
presets = data.setdefault("presets", {})
if "ai-governance" not in presets:
    presets["ai-governance"] = {
        "version": "1.0.0",
        "enabled": True,
        "priority": 10,
        "source": "project",
    }
path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY
  for line in .specify-dev/ .specify/feature.json .specify/memory/ .specify/workflows/runs/ \
    .specify/acceptance-run-evidence.latest.md vendor/AI_governance.prev/; do
    grep -qxF "$line" "$ROOT/.gitignore" 2>/dev/null || echo "$line" >>"$ROOT/.gitignore"
  done
  cp -L "$KIT_SOURCE/governance/experimental/spec_gates/activate-specify-env.sh" "$ROOT/scripts/activate-governance-specify-env.sh" 2>/dev/null || \
    cp -L "$SCRIPT_DIR/activate-specify-env.sh" "$ROOT/scripts/activate-governance-specify-env.sh" 2>/dev/null || true
  if [[ -f "$ROOT/scripts/activate-governance-specify-env.sh" ]]; then
    chmod +x "$ROOT/scripts/activate-governance-specify-env.sh"
  fi
}

install_spec_gates() {
  cp "$ROOT/governance/experimental/spec_gates/policy.adopter.json" "$ROOT/governance/experimental/spec_gates/policy.kit.json"
  ( cd "$ROOT" && printf 'y\n' | timeout 600s bash governance/experimental/spec_gates/install-and-project.sh )
  cp "$ROOT/governance/experimental/spec_gates/policy.adopter.json" "$ROOT/.specify/gates/policy.json"
  ( cd "$ROOT" && bash governance/experimental/spec_gates/sync-policy.sh )
}

overlay_kit_slim_speckit_skills() {
  KIT_SOURCE="$KIT_SOURCE" bash "$SCRIPT_DIR/overlay-speckit-checklist-skill.sh"
}

install_specify_venv() {
  local constraint
  constraint="$(dependencies_constraint_path)"
  UV_VENV_CLEAR=1 uv venv --python 3.12 "$ROOT/.tools/specify-venv"
  uv pip install --python "$ROOT/.tools/specify-venv/bin/python" \
    --constraint "$constraint" \
    "git+https://github.com/github/spec-kit.git@v1.2.5"
}

configure_agent_cli() {
  if command -v agent >/dev/null 2>&1; then
    agent sandbox disable >/dev/null 2>&1 || true
    echo "install-opt-in-stack: Cursor agent sandbox disabled (recommended on headless Linux)"
  fi
}

verify_stack() {
  ( cd "$ROOT" && timeout 180s bash .specify/gates/verify.sh --boundary git )
  ( cd "$ROOT" && export TASK_ACCEPTANCE_CMD="bash ci/adopter_task_acceptance_cmd.sh" && bash ci/run_task_acceptance_check.sh )
  echo
  bash "$SCRIPT_DIR/check-opt-in-stack.sh" || true
}

MODE=full
SWITCH=0
for arg in "$@"; do
  case "$arg" in
    -h | --help) usage 0 ;;
    --switch-snapshot) SWITCH=1 ;;
    --stack-only) MODE=stack ;;
    --readopt-only) MODE=readopt ;;
    --bootstrap) MODE=bootstrap ;;
    --import-only) MODE=import ;;
    *)
      echo "install-opt-in-stack: unknown argument: $arg" >&2
      exit 1
      ;;
  esac
done

if [[ "$MODE" == stack || "$MODE" == full ]]; then
  check_prereqs 1
else
  check_prereqs 0
fi
detect_kit_source
if [[ "$MODE" == import || "$MODE" == full ]] && same_tree; then
  echo "install-opt-in-stack: KIT_SOURCE is this checkout; first import would nest the kit. Use --stack-only for dogfood." >&2
  exit 1
fi
require_kit_env
mkdir -p "$ROOT/scripts"

case "$MODE" in
  import)
    run_first_import
    exit 0
    ;;
  bootstrap)
    if [[ ! -e "$ROOT/vendor/AI_governance" && ! -L "$ROOT/vendor/AI_governance" ]]; then
      run_first_import
    fi
    install_procedure_pin
    seed_host_entry
    exit 0
    ;;
  readopt)
    run_readopt
    exit 0
    ;;
  stack)
    if ! same_tree && [[ ! -e "$ROOT/vendor/AI_governance" && ! -L "$ROOT/vendor/AI_governance" ]]; then
      run_first_import
    fi
    install_procedure_pin
    seed_host_entry
    ensure_dependencies_txt
    install_host_adapter
    install_procedures_and_ci
    if [[ "${SKIP_SPEC_GATES:-}" != 1 ]]; then
      install_spec_gates
    fi
    overlay_kit_slim_speckit_skills
    install_specify_venv
    configure_agent_cli
    verify_stack
    ;;
  full)
    if same_tree; then
      echo "install-opt-in-stack: this checkout is the kit. Use --stack-only for dogfood, not a nested import." >&2
      exit 1
    fi
    if [[ "${SKIP_READOPT:-}" != 1 ]] && [[ -d "$ROOT/vendor/AI_governance" ]]; then
      run_readopt
      if [[ "$SWITCH" != 1 ]]; then
        echo "install-opt-in-stack: re-run with --switch-snapshot after reviewing vendor/AI_governance.readopt-report.md"
        exit 0
      fi
      switch_snapshot
    elif [[ ! -e "$ROOT/vendor/AI_governance" && ! -L "$ROOT/vendor/AI_governance" ]]; then
      run_first_import
    fi
    install_procedure_pin
    seed_host_entry
    ensure_dependencies_txt
    install_host_adapter
    install_procedures_and_ci
    install_spec_gates
    overlay_kit_slim_speckit_skills
    install_specify_venv
    configure_agent_cli
    verify_stack
    echo "install-opt-in-stack: done. Example: source scripts/activate-governance-specify-env.sh"
    echo "  export TASK_ACCEPTANCE_CMD=\"bash ci/adopter_task_acceptance_cmd.sh\""
    ;;
esac
