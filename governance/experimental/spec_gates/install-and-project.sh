#!/usr/bin/env bash
# shellcheck shell=bash
# One-time materialization of spec-gates runtime (pinned pilot versions).
# Run from kit repo root. Does not modify governance/experimental/spec_gates/policy.kit.json.
set -euo pipefail

SPEC_KIT_REV=4572a67fe0e72a6837e2d7bb0fda875bc41482e5
SPEC_GATES_REV=8a5a0e8a58aa548ad3dbba6f61e772c73cde50ae
SPEC_KIT_TAG=v1.2.5
SPEC_GATES_TAG=v0.5.0

root="$(git rev-parse --show-toplevel)"
work="${TMPDIR:-/tmp}/ai-governance-spec-gates-install.XXXXXX"
work="$(mktemp -d "$work")"
trap 'rm -rf "$work"' EXIT

command -v uv >/dev/null 2>&1 || { echo "install: uv required" >&2; exit 1; }
command -v git >/dev/null 2>&1 || { echo "install: git required" >&2; exit 1; }

timeout 90s git clone --depth 1 --branch "$SPEC_KIT_TAG" \
  https://github.com/github/spec-kit.git "$work/spec-kit"
timeout 90s git clone --depth 1 --branch "$SPEC_GATES_TAG" \
  https://github.com/schwichtgit/spec-gates.git "$work/spec-gates"
test "$(git -C "$work/spec-kit" rev-parse HEAD)" = "$SPEC_KIT_REV"
test "$(git -C "$work/spec-gates" rev-parse HEAD)" = "$SPEC_GATES_REV"

uv venv --python 3.12 "$work/venv"
timeout 120s uv pip install --python "$work/venv/bin/python" \
  --constraint "$root/research/experiments/spec_kit_spec_gates/dependencies.txt" \
  "$work/spec-kit"

cd "$root"
timeout 120s "$work/venv/bin/specify" init --here --force --non-interactive \
  --integration cursor-agent --ignore-agent-tools \
  --extension "$work/spec-gates/extension"

# project.sh requires an approved policy on disk (see /speckit.gates.init).
mkdir -p .specify/gates
install -m 0644 "$root/governance/experimental/spec_gates/policy.kit.json" \
  .specify/gates/policy.json

timeout 120s bash .specify/extensions/gates/runtime/project.sh
bash governance/experimental/spec_gates/sync-policy.sh

echo "install: projected .specify/gates — review git status before commit"
