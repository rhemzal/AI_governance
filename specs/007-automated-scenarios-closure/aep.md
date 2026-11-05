# Autonomous Execution Plan — 007 automated scenarios closure

AEP Status: READY

```aep
{
  "schema_version": 1,
  "status": "READY",
  "objective": "Close PR #58 post-qualification documentation gaps, add maintainer governance-scenarios workflow_dispatch, optional overlay row helper, and H7/H8 manual scaffolds.",
  "discovery": [
    "PR #58 handoff promised DOC DELTA after qualification; EXTERNAL still describes four tasks and twelve cursor trials only.",
    "specs/006 marks H6/H9 deferred and H7/H8 out of Harbor scope after H5 merged gate ACCEPT (#62).",
    "GitHub-hosted runners provide Docker; oracle/nop Harbor jobs need no model secret.",
    "ci/ changes require a numbered ADR amendment per adr-required workflow."
  ],
  "risk": "HIGH",
  "scope": {
    "paths": [
      "specs/007-automated-scenarios-closure/**",
      "specs/006-harbor-scenario-backlog/spec.md",
      "specs/006-harbor-scenario-backlog/progress.md",
      "research/EXTERNAL_PROJECT_EVALUATIONS.md",
      "research/experiments/harbor/README.md",
      "research/experiments/fresh-context-review/**",
      "research/experiments/cursor-stop/**",
      "tooling/BENCHMARK_SCENARIOS.md",
      "CHANGELOG.md",
      "ci/select_overlay_rows.py",
      "ci/gate_tests/test_select_overlay_rows.py",
      ".github/workflows/governance-scenarios.yml",
      "adr/ADR_0018_Optional_Harbor_Result_Gate.md"
    ],
    "allowed_effects": [
      "Advisory documentation and maintainer-only workflow",
      "Optional deterministic overlay helper under ci/",
      "Update specs/006 backlog status rows"
    ],
    "approval_required": ["Merge", "workflow_dispatch CI run with secrets"]
  },
  "steps": [
    {
      "paths": ["research/EXTERNAL_PROJECT_EVALUATIONS.md", "CHANGELOG.md", "tooling/BENCHMARK_SCENARIOS.md"],
      "action": "Record eight-task Docker qualification, H5 cursor matrix, merge gate, digest and install limits",
      "reason": "D1/D2 DOC DELTA promised after qualification"
    },
    {
      "paths": ["ci/select_overlay_rows.py", "ci/gate_tests/test_select_overlay_rows.py"],
      "action": "Implement optional Load-when row selector with unit tests",
      "reason": "H9 deferred helper from specs/006"
    },
    {
      "paths": [".github/workflows/governance-scenarios.yml", "research/experiments/harbor/README.md"],
      "action": "Add workflow_dispatch oracle/nop job and document optional cursor matrix secret",
      "reason": "H6 selective automation after observed cost"
    },
    {
      "paths": ["research/experiments/fresh-context-review/README.md", "research/experiments/cursor-stop/README.md"],
      "action": "Publish manual trial scaffolds for Experiment B and Stop observation",
      "reason": "H7/H8 boundaries without false automation claims"
    },
    {
      "paths": ["adr/ADR_0018_Optional_Harbor_Result_Gate.md", "specs/006-harbor-scenario-backlog/spec.md", "specs/007-automated-scenarios-closure/progress.md"],
      "action": "Amend ADR-0018 and sync backlog status",
      "reason": "Governance path changes and ledger continuity"
    }
  ],
  "verification": [
    {
      "command": "python3 ci/validate_aep.py specs/007-automated-scenarios-closure/aep.md",
      "expected": "Exit 0 with PASS"
    },
    {
      "command": "python3 -m unittest ci.gate_tests.test_select_overlay_rows ci.gate_tests.test_harbor_graders ci.gate_tests.test_harbor_results ci.gate_tests.test_merge_harbor_jobs -q",
      "expected": "All tests OK"
    }
  ],
  "acceptance": [
    "Assessment section documents eight tasks, H5 merged ACCEPT, and known digest or skip_install limits",
    "governance-scenarios workflow runs oracle/nop gate checks on workflow_dispatch without mandatory PR trigger",
    "select_overlay_rows selects fixture overlay rows for touched paths with tests",
    "H7/H8 README scaffolds link to specs/004 and Tier C observation without CI agent runs",
    "specs/006 marks H6 and H9 done; H7/H8 remain scoped scaffolds"
  ],
  "blocking_questions": [],
  "budget": {
    "max_repair_attempts": 3,
    "on_exhaustion": "Stop the affected step, preserve CI logs, and report maintainer follow-up."
  },
  "doc_delta": "Post-qualification research/changelog/benchmark updates; optional maintainer workflow and overlay helper; no adopter requirement."
}
```
