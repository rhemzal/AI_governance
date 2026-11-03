# Benchmark trial records — technical plan

**Spec**: `specs/001-benchmark-trial-records/spec.md`

## Summary

The failing assertion is the directory prohibition in the open-claim test, not the scenario text. Keep that absence as one dated sentence. Check later files in `ci/benchmark_trials.py`. Do not run B5–B8 in this change.

The executable steps are `tasks.md`. This file is the design record and the Autonomous Execution Plan.

## File map

- `ci/benchmark_trials.py` — field checks. Created by Task 1.
- `ci/gate_tests/test_open_claim_limits.py` — replaces the absence assertion.
- `ci/claim_cards.json` — card `benchmark-scenarios-unrun` only. No new card.
- `tooling/BENCHMARK_SCENARIOS.md` — dated sentence and recording rules.
- `research/benchmark_trials/README.md` — Task 2. Not a trial record.
- Procedure pin, preset, and profile are the surrounding adoption. They are not a second benchmark implementation.

```aep
{
  "schema_version": 1,
  "status": "READY",
  "objective": "Allow a later B5-B8 trial file while keeping the 2026-11-02 absence sentence, and pin the work procedures used to do it.",
  "discovery": [
    "On 2026-11-03, creating research/benchmark_trials made test_b5_through_b8_have_no_recorded_trial fail at assertFalse(directory.exists()) with AssertionError: True is not false. The scenario-text assertions had already passed.",
    "The root cause is that the test encoded a missing directory as a permanent invariant. The card rerun_when already said a trial record should change the claim.",
    "Risk is HIGH because the change edits a CI gate test and the claim registry. Constitutional rules are not edited."
  ],
  "risk": "HIGH",
  "scope": {
    "paths": [
      "ci/benchmark_trials.py",
      "ci/gate_tests/test_open_claim_limits.py",
      "ci/gate_tests/test_work_procedures.py",
      "ci/claim_cards.json",
      "tooling/BENCHMARK_SCENARIOS.md",
      "research/benchmark_trials/README.md",
      "specs/001-benchmark-trial-records/**",
      "vendor/superpowers/v7.0.1/**",
      ".cursor/skills/**",
      ".specify/presets/**",
      ".specify/workflows/ai-governance/**",
      ".specify/workflows/workflow-registry.json",
      ".gitignore",
      "usage/AI_ENGINEERING_METHODS.md",
      "adr/ADR_0015_Pinned_Work_Procedures.md",
      "adr/README.md",
      "README.md",
      "CHANGELOG.md",
      "research/EXTERNAL_PROJECT_EVALUATIONS.md"
    ],
    "allowed_effects": [
      "Edit the current checkout",
      "Run non-interactive unit tests",
      "Record the feature ledger"
    ],
    "approval_required": [
      "Merge",
      "Push",
      "Publish",
      "Deploy"
    ]
  },
  "steps": [
    {"paths": ["specs/001-benchmark-trial-records/spec.md"], "action": "Record the spec and continuation decision", "reason": "The approved mandate names the acceptance cases"},
    {"paths": ["ci/gate_tests/test_open_claim_limits.py", "ci/benchmark_trials.py"], "action": "Replace the absence invariant with the checker", "reason": "A new trial directory must be legal and a bad record must fail"},
    {"paths": ["research/benchmark_trials/README.md"], "action": "Add a non-trial README after Task 1 is ledgered", "reason": "Show the directory can exist without a fabricated trial"},
    {"paths": ["usage/AI_ENGINEERING_METHODS.md", "adr/ADR_0015_Pinned_Work_Procedures.md"], "action": "Point routine work at the pinned procedures", "reason": "The pin is unused unless the selector names it"}
  ],
  "verification": [
    {"command": "python3 -m unittest ci.gate_tests.test_open_claim_limits ci.gate_tests.test_work_procedures ci.gate_tests.test_claim_cards -v", "expected": "Exit 0"},
    {"command": "python3 ci/validate_aep.py --changed-files 2 < specs/001-benchmark-trial-records/plan.md", "expected": "Output starts with PASS"}
  ],
  "acceptance": [
    "The 2026-11-02 absence sentence remains once.",
    "A missing directory and a README-only directory are success.",
    "A B50 scenario, a broken revision, and a bad outcome fail.",
    "outcome cancelled and outcome blocked are accepted.",
    "The governed workflow has no review gate and the bundled workflow still has two."
  ],
  "blocking_questions": [],
  "budget": {"max_repair_attempts": 3, "on_exhaustion": "Stop the affected action and report the last command output plus the next decision."},
  "doc_delta": "Update the method selector, ADR 0015, the benchmark scenario note, the changelog, and the external-project verdict. Do not copy the rules into the preset."
}
```

## Method

- **Baseline:** directory creation fails the old test at the `assertFalse` line. Commit under test was the claim-card revision that introduced that test (`7a1f3bf`).
- **Acceptance observation:** red was `FileNotFoundError` for `ci/benchmark_trials.py` after the new test existed. Green is the unittest above. Known-bad inputs are in the spec.
- **Smallest method:** systematic debugging for the failure, then test-driven development for the checker, `executing-plans` for Task 1 then Task 2, and one fresh review. No new orchestrator.
- **Uncertainty:** a fresh reviewer may miss a field the tests do not exercise. The review record says what was found.

## Rulings already fixed

- No commit and no pull request. The operator did not authorize them.
- No new git worktree. This checkout is the assigned workspace.
- The kept ledger is `progress.md` in this directory. `.superpowers/` is scratch and gitignored.
- Documentation and the claim-card sentence do not require a red-green cycle. The checker does.
