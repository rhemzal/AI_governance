# Architecture CI Gates (Principles)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
These gates prevent architecture drift and boundary violations.
They are written as **principles** so you can implement them in your CI tool of choice.

## Gate A1: Boundary Integrity
Fail the pipeline if:
- core (domain/use-cases) code imports from integration boundary code (adapters/infrastructure/frameworks)
- integration boundary code calls core via concrete classes instead of a boundary contract (port/interface)
- integration boundary code bypasses boundary contracts to call internal core services directly

Expected implementation options:
- static analysis (language-specific)
- dependency graph checks
- import allow/deny lists

## Gate A2: “New Adapter Requires Contract”
If a new adapter is introduced, require:
- a boundary contract (port/interface) defined inward
- tests proving adapter behavior against the contract

## Gate A3: Architectural Change Requires ADR
If PR changes boundaries, layering, or introduces new cross-cutting patterns:
- require an ADR in `adr/`

## Gate A4: No Hidden Global State
Fail if new global singletons are added that:
- control time/randomness
- hide IO
- make tests non-deterministic

## Gate A5: Structural Change Blast-Radius
If a PR reorganises modules, splits or merges build targets, or moves files across package/module boundaries:
- Verify that the rebuild/retest blast radius of unrelated modules has not increased (dependency graph check).
- Require a stated justification for the structural change (boundary clarification, volatility reduction, or measurable build benefit).
- If the structural change spans more than one logical slice (module/boundary/dependency direction), require a declared scope list before merge.

Expected implementation options:
- dependency graph diff (before vs after the PR)
- build system `--affected` query or equivalent
- PR checklist: "structural change justified by: boundary / volatility / build measurement / other (state)"

## Related Documents
- `constitution/AI_RULES.md` and `constitution/AI_ENFORCEMENT.md`
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `adr/ADR_TEMPLATE.md`
- `ci/TEST_GATES.md`

