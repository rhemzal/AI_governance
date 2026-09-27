# ADR 0009: Structured AEP Declaration Validation

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status
Proposed — implemented on this review branch; acceptance occurs through maintainer review/merge.

## Context
The inline whole-body grep accepts empty Objective/Steps/test-command fields and rejects unrelated TODO text. The specification permits documentation verification, while the grep expects selected test-runner names. The kit deliberately avoided a general-purpose script pack; duplicating a more complex parser inside workflow examples would make it harder to test and maintain.

## Decision
Permit one scoped, dependency-free Python reference validator (`ci/validate_aep.py`) and its regression tests. PRs declare plans in one fenced `aep` JSON block, schema version 1. This supersedes the blanket no-repository-scripts implementation policy only for this validator and its tests. Tool/model experimentation remains advisory under ADR-0004.

Missing AEP declarations remain advisory. Explicit declarations are structurally checked for all PR sizes. Readiness, blocked, and not-required states are distinct; a structural pass never grants execution, merge, or deployment authority.

## Alternatives Considered
- Expand grep: still conflates prose with data and has weak structural checks.
- Embed Python in both workflow and starter: duplicate source with poor local testability.
- Full semantic/LLM policy engine: costly, non-deterministic, and cannot prove real authorization; defer.

## Trade-Offs
Adds a Python 3 standard-library dependency only for adopters of this optional gate. The PR serialization is more explicit but introduces a breaking migration for old declarations. Conversational plans remain concise prose; routine tasks do not require full serialized plans.

## Sensitivity Points & Risks
The validator checks declaration shape, not whether commands exist, run, or prove acceptance. It never executes commands in PR text. Scope containment, real permissions, budget enforcement, and applicability still require independent controls/review. Workflow runs use pull_request with read-only contents permission and non-persistent checkout credentials.

## Points of No Return
No product-state changes. Roll back workflow, validator, and declaration format as one versioned unit if needed; never silently disable the gate to pass a task.

## Consequences
`standard` imports the validator/tests through its existing `ci/` inclusion. Minimal documentation imports gain no Python requirement unless they opt into this gate. Update the starter, PR template, enforcement matrix, development guide, release checklist, and changelog together. No new agent framework or product test harness is introduced.

## Enforcement
Run `timeout 60s python3 -m unittest discover -s ci/tests -v` locally and in the reference workflow. Regressions cover empty declarations, unrelated prose, documentation commands, missing fields, malformed/conflicting declarations, blocker consistency, and command-as-data behavior. Review governance/gate changes under current controls.

## Documentation Impact
Canonical format: `usage/AEP_VALIDATION.md`. Implementation: `ci/validate_aep.py`. Workflow and starter invoke that source rather than duplicate its logic. Existing July audit remains historical; this change needs a new release audit before a stable-contract promotion.

## Governance Change
- Breaking rule/gate change: yes, legacy AEP Status-only PR bodies must migrate when using this gate.
- Bundle content change: standard/full include validator/tests via existing paths; manifest schema and bundle names unchanged.
- Local overlay: retain stricter applicability if explicitly desired, but remove assumptions that file count alone establishes risk or that a schema pass proves correctness.
- Rollout: copy workflow + validator + template from one pinned revision; copy tests if retaining the regression step; validate existing open PR declarations before enabling the new check.

## Related Documents
- `usage/AEP_VALIDATION.md`
- `usage/CI_STARTER_WORKFLOWS.md`
- `usage/ENFORCEMENT_MATRIX.md`
- `adr/ADR_0004_Tooling_Is_Experimental.md`
- `adr/ADR_0008_Bounded_Agent_Execution.md`
