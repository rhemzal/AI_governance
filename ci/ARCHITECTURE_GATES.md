# Architecture CI Gates (Principles)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
These gates prevent architecture drift and boundary violations.
They are written as **principles** so you can implement them in your CI tool of choice.

See `constitution/ADAPTIVE_GOVERNANCE.md` (Governance Level G) and `usage/ENFORCEMENT_MATRIX.md` (CI Maturity CM). Do not use bare `L0`–`L3`.

## Gate: A1 — Boundary Integrity

- **Recommended from Governance Level (G):** G2
- **Mandatory from Governance Level (G):** G3
- **Adopter CI Maturity (CM):** Required CM2 when tooling exists — see `usage/ENFORCEMENT_MATRIX.md`
- **Risk mitigated:** Core (domain/use-case) code importing infrastructure concepts; architectural decay over time; boundary violations that are cheap to introduce but expensive to reverse.
- **Local alternative:** Run a static analysis or import-linting script locally before commit (e.g., `make check-boundaries`).
- **Cost:** Low to medium, depending on tooling. Dependency graph checks and import allow/deny lists can be set up once and maintained cheaply.
- **Failure action:** Abort the pipeline. The AI MUST NOT merge code that violates boundary integrity. Report the violation and propose a compliant alternative.

Fail the pipeline if:
- core (domain/use-cases) code imports from integration boundary code (adapters/infrastructure/frameworks)
- integration boundary code calls core via concrete classes instead of a boundary contract (port/interface)
- integration boundary code bypasses boundary contracts to call internal core services directly

Expected implementation options:
- static analysis (language-specific)
- dependency graph checks
- import allow/deny lists

## Gate: A2 — New Adapter Requires Contract

- **Recommended from Governance Level (G):** G2
- **Mandatory from Governance Level (G):** G3
- **Adopter CI Maturity (CM):** Advisory CM2 — see `usage/ENFORCEMENT_MATRIX.md`
- **Risk mitigated:** Adapters introduced without a defined port/interface; tight coupling that makes swapping or testing adapters difficult.
- **Local alternative:** PR description or commit message must state the contract name; reviewer (or AI agent) verifies it exists.
- **Cost:** Low. Requires only a naming convention check and a brief review step.
- **Failure action:** Block merge. Require the author to define and reference a boundary contract before the adapter is accepted.

If a new adapter is introduced, require:
- a boundary contract (port/interface) defined inward
- tests proving adapter behavior against the contract

## Gate: A3 — Architectural Change Requires ADR

- **Recommended from Governance Level (G):** G3
- **Mandatory from Governance Level (G):** G4
- **Adopter CI Maturity (CM):** Required CM3 — see `usage/ENFORCEMENT_MATRIX.md`
- **Risk mitigated:** Undocumented architectural decisions that are later reversed or misunderstood; loss of decision rationale over time.
- **Local alternative:** At G1–G2, a short comment in the commit message or a one-paragraph note in `notes/` is sufficient. A formal ADR is not required until G3.
- **Cost:** Medium. ADRs take time to write and maintain. Do not require them for reversible or small-scope decisions.
- **Failure action:** At G3+, block merge until an ADR is present in `adr/`. At G2, warn but do not block.

If PR changes boundaries, layering, or introduces new cross-cutting patterns:
- require an ADR in `adr/`

## Gate: A4 — No Hidden Global State

- **Recommended from Governance Level (G):** G1
- **Mandatory from Governance Level (G):** G2
- **Adopter CI Maturity (CM):** With T1 at CM1 — see `usage/ENFORCEMENT_MATRIX.md`
- **Risk mitigated:** Non-deterministic tests; hidden dependencies on time, randomness, or I/O that make tests unreliable and code hard to reason about.
- **Local alternative:** Code review by the developer or AI agent; grep for common patterns (`global`, `singleton`, `os.getenv` in unexpected places).
- **Cost:** Very low. A linting rule or a short grep check is sufficient.
- **Failure action:** Fail the pipeline. Require the global state to be injected or controlled.

Fail if new global singletons are added that:
- control time/randomness
- hide IO
- make tests non-deterministic

## Gate: A5 — Structural Change Blast-Radius

- **Recommended from Governance Level (G):** G2
- **Mandatory from Governance Level (G):** G3
- **Adopter CI Maturity (CM):** Advisory CM2 — see `usage/ENFORCEMENT_MATRIX.md`
- **Risk mitigated:** Accidental increase in rebuild or retest scope; structural changes that silently couple previously independent modules.
- **Local alternative:** At G1–G2, the developer (or AI agent) states the blast radius in the commit message. A dependency graph diff tool is not required.
- **Cost:** Medium. Dependency graph diffing requires tooling investment. At Level 2, a manual declaration is acceptable.
- **Failure action:** At G3+, block merge if blast radius has increased without justification. Require a declared scope list for changes spanning more than one logical slice.

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
- `usage/ENFORCEMENT_MATRIX.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `adr/ADR_TEMPLATE.md`
- `ci/TEST_GATES.md`

