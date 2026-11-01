#!/usr/bin/env bash
# shellcheck shell=bash
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
src="$root/governance/experimental/spec_gates/policy.kit.json"
dest="$root/.specify/gates/policy.json"

if [[ ! -f "$src" ]]; then
  echo "sync-policy: missing $src" >&2
  exit 1
fi
if [[ ! -d "$root/.specify/gates" ]]; then
  echo "sync-policy: no projected .specify/gates/ — run install-and-project.sh first" >&2
  exit 1
fi

install -m 0644 "$src" "$dest"
echo "sync-policy: installed $(basename "$src") -> .specify/gates/policy.json"
