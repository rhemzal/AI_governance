#!/usr/bin/env bash
# Print the canonical kit-repo maintenance acceptance command.
# Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
set -euo pipefail
printf '%s\n' 'timeout 120s python3 -m unittest ci.gate_tests.test_work_procedures ci.gate_tests.test_test_evidence ci.gate_tests.test_stop_hook_contract ci.gate_tests.test_open_claim_limits ci.gate_tests.test_workflow_acceptance ci.gate_tests.test_superpowers_task_done ci.gate_tests.test_spec_gates_git_environment -v'
