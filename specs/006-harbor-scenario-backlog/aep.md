# Autonomous Execution Plan — Harbor scenario backlog (006)

AEP Status: READY

```aep
{
  "schema_version": 1,
  "status": "READY",
  "objective": "Implement Harbor C3/C4 maintainer tasks, extend result-gate matrices to eight controls, and prove graders with unit tests before any paid cursor-cli matrix.",
  "discovery": [
    "specs/005 records oracle/nop qualification on four C1/C2 tasks only.",
    "research/EXTERNAL_PROJECT_EVALUATIONS.md Automated control scenarios table requires C3 physical copy and C4 task-scoped report compliance.",
    "build_tasks.py is the single generator for committed tasks/ trees; grader/check.py is copied per task.",
    "C3 final artifact may retain fixture symlink opt-in/pin; grader needs allow_symlink_paths for that path only."
  ],
  "risk": "HIGH",
  "scope": {
    "paths": [
      "specs/006-harbor-scenario-backlog/**",
      "research/experiments/harbor/**",
      "ci/gate_tests/test_harbor_graders.py",
      "research/EXTERNAL_PROJECT_EVALUATIONS.md"
    ],
    "allowed_effects": [
      "Add maintainer Harbor tasks and generator logic",
      "Extend grader manifest fields for symlink allowance",
      "Update expect JSON and harbor README",
      "Append cross-link in research assessment optional one line"
    ],
    "approval_required": ["Merge", "Paid cursor-cli harbor run", "workflow_dispatch CI"]
  },
  "steps": [
    {
      "paths": ["specs/006-harbor-scenario-backlog/spec.md", "specs/006-harbor-scenario-backlog/tasks.md", "specs/006-harbor-scenario-backlog/aep.md"],
      "action": "Publish backlog spec, ordered tasks, and this READY AEP",
      "reason": "Authorize dependent implementation with explicit acceptance"
    },
    {
      "paths": ["research/experiments/harbor/grader/check.py", "research/experiments/harbor/build_tasks.py"],
      "action": "Add C3/C4 task definitions, symlink allowance, regenerate tasks/",
      "reason": "Close H1 and H2 with oracle/nop-compatible graders"
    },
    {
      "paths": ["research/experiments/harbor/expect-oracle.json", "research/experiments/harbor/expect-candidate.json", "research/experiments/harbor/README.md"],
      "action": "List eight ai-governance/* task ids in expectation files and document C3/C4 grading",
      "reason": "H3 gate matrices match expanded dataset"
    },
    {
      "paths": ["ci/gate_tests/test_harbor_graders.py"],
      "action": "Add C3/C4 positive and negative grader cases",
      "reason": "H4 independent verification without Docker spend"
    },
    {
      "paths": ["specs/006-harbor-scenario-backlog/progress.md"],
      "action": "Record unit test evidence; note Docker/cursor qualification BLOCKED or complete when run",
      "reason": "Maintainer ledger continuity from specs/005"
    }
  ],
  "verification": [
    {
      "command": "python3 ci/validate_aep.py specs/006-harbor-scenario-backlog/aep.md",
      "expected": "Exit 0 with PASS"
    },
    {
      "command": "python3 research/experiments/harbor/build_tasks.py && python3 -m unittest ci.gate_tests.test_harbor_graders ci.gate_tests.test_harbor_results -q",
      "expected": "OK; builder parity and harbor gate tests pass"
    }
  ],
  "acceptance": [
    "Eight Harbor tasks exist under research/experiments/harbor/tasks/ with lintable layout",
    "C3 pass requires materialized copy bytes and copy-report; explanation-only fails",
    "C4 pass requires CHANGELOG bullet only; B1 exact loaded-overlay.md",
    "expect-oracle.json and expect-candidate.json enumerate all eight task package ids",
    "No adopter bundle or mandatory CI workflow added"
  ],
  "blocking_questions": [],
  "budget": {
    "max_repair_attempts": 3,
    "on_exhaustion": "Stop the affected step, preserve failing grader output, and report next maintainer action (Docker oracle or paid cursor)."
  },
  "doc_delta": "Add specs/006 backlog; extend harbor README and optional research cross-link; behavior change limited to maintainer Harbor pilot."
}
```
