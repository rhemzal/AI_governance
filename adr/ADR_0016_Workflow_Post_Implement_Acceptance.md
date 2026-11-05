# ADR 0016: Workflow Post-Implement Acceptance

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it, preserve this line._

## Status

Accepted — 2026-11-04.

## Context

PR #49 analyzed the gap between loaded governance instructions and everyday agent
completion at `52f9c26f342b3517384e96f7d289bb300a72aaa4`. The governed Spec Kit
workflow ended after `speckit.implement` without a deterministic verification step.
Agents could report completion while omitting the project's selected acceptance
command. `usage/AI_RUN_EVIDENCE.md` already described state-bound evidence; the kit
did not consistently produce that block from a native run at workflow completion.

ADR-0015 pinned Superpowers procedures and a gate-free `ai-governance` workflow.
That preset did not add shell verification. The evidence helper in ADR-0013
assesses supplied records; it does not execute checks or refuse no-op commands.
Spec-gates remains experimental and supplies gate observations, not whole-task
acceptance.

The audit recommended reusing existing runners and CI commands rather than a new
schema, orchestrator, or mandatory adopter gate.

## Decision

1. Add a final native `type: shell` step to `.specify/workflows/ai-governance/workflow.yml`
   after `implement`. It runs `ci/run_task_acceptance_check.sh`, which executes the
   host-selected command, propagates its exit code, and writes an `AI RUN EVIDENCE`
   markdown block with commit and dirty-tree identity. The workflow input `verify`
   supplies the command when present; direct invocation uses `TASK_ACCEPTANCE_CMD`.
   **Amendment (2026-11-04):** dirty-tree identity must incorporate uncommitted file
   content (porcelain status plus blob hashes via `ci/uncommitted_diff_identity.py`),
   not `git status` text alone, so distinct edits to the same path do not collide.
   **Amendment (2026-11-05):** regression test covers untracked symlink targets in
   `test_dirty_tree_identity_reflects_symlink_target` (Experiment B follow-up).
2. Introduce `ci/kit_maintenance_acceptance_cmd.sh` as the kit-repo default command
   for maintenance tasks, shared by the runner, workflow examples, and gate tests.
3. Extend `ci/validate_test_evidence.py` with non-blocking `advisories` and stderr
   `ADVISORY:` lines when declared artifact paths are missing on disk. Schema
   agreement outcomes are unchanged.
4. Add regression tests for the runner, workflow wiring, Superpowers `task-done`
   disposable limits, and spec-gates Git-environment controls. Qualify experimental
   spec-gates **v0.5.1** in the kit dogfood tree via `governance/experimental/spec_gates/install-and-project.sh`
   and `.specify/gates/.upgrade-holds`; that projection is kit-repo experimental
   material, not a default import-bundle requirement.

Out of scope: branch-protection changes, mandatory adopter workflow activation,
native Cursor Stop proof, productivity claims, and replacing host test runners.

## Alternatives Considered

- Rely on agent `verification-before-completion` prose alone. Cheapest, but the
  audit showed completion without executing the selected check.
- Add a new evidence schema or orchestrator service. Rejected as duplicate of
  existing runners and CI.
- Make the shell step optional via `continue_on_error`. Rejected; a failed check
  must fail the workflow run.
- Promote spec-gates to required adopter checks. Deferred per existing pilot and
  ADR-0004.

## Trade-Offs

- Workflow users gain a deterministic completion boundary when they run the preset.
  Ordinary chats still depend on governed-work and direct verification.
- The runner refuses `true`, `:`, and `exit 0` no-ops, but cannot judge whether the
  command is sufficient for the product task.
- Missing-artifact advisories improve honesty without blocking VERIFIED on schema
  agreement; they do not dereference or authenticate artifacts.

## Sensitivity Points & Risks

- A weak but non-no-op command can still pass. Independent expectations and review
  remain necessary.
- Local evidence blocks are not authenticated. CI and host review supply stronger
  assurance.
- Porcelain-only dirty identity (pre-amendment) could not distinguish two different
  edits to the same path; content-aware hashing closes that audit gap without changing
  the evidence schema.
- Adopters must wire their own acceptance command when copying the workflow; the
  kit default applies to kit maintenance only.

## Points of No Return

None. Removing the shell step and runner restores the ADR-0015 workflow shape.
Tests document the prior gap if reverted deliberately.

## Consequences

Kit maintenance and workflow runs can end with native command execution and a
written evidence block. Copy-import adopters receive the scripts through `ci/` and
workflow files only when they opt into the work-procedure bundle; nothing auto-runs
in downstream repositories. Named downstream trials remain a separate host decision.

## Enforcement

- `ci/gate_tests/test_workflow_acceptance.py` — runner, workflow, disposable engine probes.
- `ci/uncommitted_diff_identity.py` — content-aware uncommitted diff identity for the runner.
- `ci/gate_tests/test_superpowers_task_done.py` — vendored completion limits.
- `ci/gate_tests/test_spec_gates_git_environment.py` — install pin and Git-env controls.
- `ci/gate_tests/test_test_evidence.py` — advisory behavior on missing paths.
- `.specify/gates/verify.sh --boundary git` — projected policy gates including `kit-gate-tests`.

## Documentation Impact

- Updated: `usage/AI_RUN_EVIDENCE.md`, `usage/FOR_EXISTING_PROJECTS.md`,
  `DEVELOPMENT.md`, `research/EXTERNAL_PROJECT_EVALUATIONS.md`, `CHANGELOG.md`,
  `.cursor/skills/governed-work/SKILL.md`, plan template, experimental spec-gates README.
- New: this ADR.

## Governance Change (If Applicable)

- Is this a governance change? yes — kit dogfood workflow and `ci/` behavior.
- Imported kit upgrade: adopters pick up files on their next pin; no automatic activation.
- Local overlay impact: none in upstream kit; adopters may reference the runner in overlay rows.
- Enforcement impact: additional gate tests; no new required GitHub check for adopters.
- Migration: existing clones gain the shell step when they use the updated workflow YAML.

## References

- `research/EXTERNAL_PROJECT_EVALUATIONS.md` — Agent runtime analysis (PR #49) and implementation table
- `adr/ADR_0015_Pinned_Work_Procedures.md`
- `adr/ADR_0013_Test_Evidence_And_Runner_Conformance.md`
- `usage/AEP_VALIDATION.md`
