#!/usr/bin/env bash
# Spec Kit entry point — delegates to the canonical kit acceptance runner.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
exec bash "$ROOT/ci/run_task_acceptance_check.sh"
