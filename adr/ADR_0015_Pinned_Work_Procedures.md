# ADR 0015: Pinned Work Procedures

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If copied, preserve this line._

## Status

Proposed — acceptance is the maintainer's merge decision.

## Context

The kit can record limits and run advisory checks, and it can describe an
Autonomous Execution Plan. Agents still had to improvise debugging, plan
execution, verification, and review. The default Spec Kit workflow also stops
for `review-spec` and `review-plan` even after the operator has authorized the
outcome. Separately, `test_b5_through_b8_have_no_recorded_trial` treated the
absence of `research/benchmark_trials` as a permanent invariant, so a later
trial record could not be added without failing the suite.

Superpowers v7.0.1 already contains procedures for those gaps.
`executing-plans` continues through authorized tasks and keeps a ledger that
a later session can resume. Copying the whole catalog, or adding another
orchestrator, was not justified.

## Decision

1. Pin Superpowers v7.0.1, commit `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`,
   for `systematic-debugging`, `verification-before-completion`,
   `executing-plans`, and the plan, test, review, and script files those
   procedures call. Leave the texts under their MIT license. Do not install
   `subagent-driven-development` as a skill.
2. Route use through `.cursor/skills/governed-work/SKILL.md` and the method
   selector. Constitution authority wins. A documentation or registry-wording
   change does not require test-driven development. A behavior change does.
3. Add a project Spec Kit preset that appends mandate, acceptance, and
   Autonomous Execution Plan pointers to the core templates, and a workflow
   without the two approval gates. Keep the bundled workflow unchanged.
4. Replace the benchmark absence invariant with a dated historical sentence
   plus a checker for later trial files. The first recorded cycle is
   `specs/001-benchmark-trial-records/`.

Out of scope: publishing the preset, adopting every Superpowers skill, changing
constitutional rules, and further Stop-hook work.

## Alternatives Considered

- Leave Superpowers as inspiration and keep writing local checklists. That
  preserves uniqueness and continues the gap the operator described.
- Import the full Superpowers catalog and require test-driven development for
  every edit. That conflicts with proportional documentation work.
- Adopt an external autonomous-run preset as the governance standard. It
  duplicates mandate and evidence rules this kit already has.
- Keep forbidding `research/benchmark_trials` and store trials somewhere else.
  The test would still encode "no evidence" as success.

## Trade-Offs

- Pinned procedure text gives an agent a concrete next action and adds files
  that must be re-pinned on upgrade.
- Skipping the two Spec Kit gates removes a habitual pause. The remaining
  stops are the ones that change authority or leave the worktree.
- A historical absence sentence can survive after a trial exists. A
  well-formed trial file can still be untrue. The checker does not prevent
  that.

## Sensitivity Points & Risks

- A skill that says "always" can be mistaken for permission. The profile and
  `constitution/AI_ENFORCEMENT.md` §1.2 say it is not.
- A ledger can claim a task is complete when a required test was never run.
  Fresh review against the spec is the check for that miss.
- Vendored hashes detect silent edits. They do not prove the procedure was
  followed. The cycle notes are the use evidence.

## Points of No Return

None. The pin, preset, and checker are reviewable files. Removing them
restores the previous selector text and the absence invariant only if that
test is restored deliberately.

## Consequences

Agents in this repository have a default route for debug, execute, verify,
resume, and review. Copy-import bundles do not gain those files until an
adopter copies the pin. The benchmark suite can accept a later trial file
and still rejects a malformed one. A file the checker accepts is not a
completed matched trial. Review of the first green checker found that
`cancelled` was rejected and that a missing directory was not what the test
called. Both were fixed in this change: the new assertion failed, then passed.

## Enforcement

- `ci/gate_tests/test_work_procedures.py` checks the pin hashes, the preset
  append, and that the governed workflow has no approval gate.
- `ci/gate_tests/test_open_claim_limits.py` checks the absence sentence and
  trial records.
- The claim card `benchmark-scenarios-unrun` points at that test. Accepting a
  file is not proof a matched trial ran.

## Documentation Impact

- Source of truth for authority: `constitution/AI_ENFORCEMENT.md` and
  `constitution/AI_RULES.md` §6.5. This ADR does not move those rules.
- Docs updated: `usage/AI_ENGINEERING_METHODS.md`, `README.md`,
  `adr/README.md`, `tooling/BENCHMARK_SCENARIOS.md`, `CHANGELOG.md`,
  `research/EXTERNAL_PROJECT_EVALUATIONS.md`.
- Docs removed: none.
- Generated docs: no.

## Governance Change (If Applicable)

- Is this a governance change? yes. The benchmark gate no longer treats a
  missing trial directory as the required state. Policy text in
  `constitution/` is unchanged.
- Imported kit upgrade: no.
- Local overlay impact: none.
- Enforcement impact: the trial checker and the pin-hash test. No new
  adopter-mandatory workflow.
- Migration: existing clones gain the files at this revision. A live project
  trial uses `usage/HOW_TO_IMPORT.md` § Opt-in work procedures and does not
  install spec-gates or a Stop hook. A trial file
  added under `research/benchmark_trials/` must carry `scenario`, `revision`,
  and `outcome`. `README.md` is ignored.

## References

- Superpowers v7.0.1 `skills/executing-plans/SKILL.md`
- Spec Kit v1.2.5 preset resolution in `.specify/scripts/bash/common.sh`
- `adr/ADR_0012_Outcome_Based_Method_Adoption.md`
