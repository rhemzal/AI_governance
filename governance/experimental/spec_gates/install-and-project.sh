#!/usr/bin/env bash
# shellcheck shell=bash
# One-time materialization of spec-gates runtime (pinned pilot versions).
# Run from kit repo root. Does not modify governance/experimental/spec_gates/policy.kit.json.
set -euo pipefail

SPEC_KIT_REV=4572a67fe0e72a6837e2d7bb0fda875bc41482e5
SPEC_GATES_REV=a42f1f7d34c6e190b5a640d67244cf6f071d07e7
SPEC_KIT_TAG=v1.2.5
SPEC_GATES_TAG=v0.5.1
SPEC_GATES_VERSION="${SPEC_GATES_TAG#v}"
SPEC_GATES_ZIP="gates-${SPEC_GATES_VERSION}.zip"
SPEC_GATES_RELEASE_BASE="https://github.com/schwichtgit/spec-gates/releases/download/${SPEC_GATES_TAG}"

root="$(git rev-parse --show-toplevel)"
work="${TMPDIR:-/tmp}/ai-governance-spec-gates-install.XXXXXX"
work="$(mktemp -d "$work")"
trap 'rm -rf "$work"' EXIT

command -v uv >/dev/null 2>&1 || { echo "install: uv required" >&2; exit 1; }
command -v git >/dev/null 2>&1 || { echo "install: git required" >&2; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "install: curl required" >&2; exit 1; }
command -v sha256sum >/dev/null 2>&1 || { echo "install: sha256sum required" >&2; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "install: jq required" >&2; exit 1; }

timeout 90s git clone --depth 1 --branch "$SPEC_KIT_TAG" \
  https://github.com/github/spec-kit.git "$work/spec-kit"
test "$(git -C "$work/spec-kit" rev-parse HEAD)" = "$SPEC_KIT_REV"

timeout 90s git clone --depth 1 --branch "$SPEC_GATES_TAG" \
  https://github.com/schwichtgit/spec-gates.git "$work/spec-gates"
test "$(git -C "$work/spec-gates" rev-parse HEAD)" = "$SPEC_GATES_REV"

curl -fsSL -o "$work/$SPEC_GATES_ZIP" "$SPEC_GATES_RELEASE_BASE/$SPEC_GATES_ZIP"
curl -fsSL -o "$work/$SPEC_GATES_ZIP.sha256" "$SPEC_GATES_RELEASE_BASE/$SPEC_GATES_ZIP.sha256"
(
  cd "$work"
  grep -F "$SPEC_GATES_ZIP" "$SPEC_GATES_ZIP.sha256" | sha256sum -c -
)

uv venv --python 3.12 "$work/venv"
timeout 120s uv pip install --python "$work/venv/bin/python" \
  --constraint "$root/research/experiments/spec_kit_spec_gates/dependencies.txt" \
  "$work/spec-kit"

cd "$root"
timeout 120s "$work/venv/bin/specify" init --here --force --non-interactive \
  --integration cursor-agent --ignore-agent-tools

if "$work/venv/bin/specify" extension remove gates --keep-config --force >/dev/null 2>&1; then
  :
fi
printf 'y\n' | timeout 120s "$work/venv/bin/specify" extension add gates --force \
  --from "$SPEC_GATES_RELEASE_BASE/$SPEC_GATES_ZIP"

installed_ver="$(sed -n 's/^  version: "\(.*\)"$/\1/p' .specify/extensions/gates/extension.yml | head -n 1)"
reg_ver="$(jq -r '.extensions.gates.version // empty' .specify/extensions/.registry 2>/dev/null || true)"
if [[ "$installed_ver" != "$SPEC_GATES_VERSION" || "$reg_ver" != "$SPEC_GATES_VERSION" ]]; then
  echo "install: extension/registry versions are ${installed_ver:-unknown}/${reg_ver:-unknown}; expected $SPEC_GATES_VERSION" >&2
  exit 1
fi

mkdir -p .specify/gates
install -m 0644 "$root/governance/experimental/spec_gates/policy.kit.json" \
  .specify/gates/policy.json

timeout 120s bash .specify/extensions/gates/runtime/project.sh
bash governance/experimental/spec_gates/sync-policy.sh

echo "install: projected .specify/gates — review git status before commit"
