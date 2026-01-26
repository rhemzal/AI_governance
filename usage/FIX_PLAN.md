# Fix Plan — AI_governance kit

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

Date: 2025-12-28
Context: Generated after a full re-run of `usage/AUDIT_PLAYBOOK.md`.

## Immediate Fixes (Required)
- None identified in this re-run.

## Recommended Next Fixes (Downstream / Adoption)
1) Implement CI checks for gate principles
- Why: the kit’s `ci/*_GATES.md` are intentionally principles; without wiring, enforcement falls back to human review (PR checklist discipline) until CI exists.
- Minimum: one job each for docs/test/architecture/interface gates.
  - Adoption guidance: implement progressively so CI stays high-signal (see `usage/CI_MINIMUM_ADOPTION.md`).

2) Add a documentation hygiene check to CI
- Why: makes doc hygiene enforceable.

3) Add dependency boundary enforcement appropriate to the stack
- Examples: import allow/deny lists, dependency graph checks, static analysis.

4) Add a minimal “ADR required” check in CI
- Trigger: changes touching boundaries/contracts/interfaces.

5) (Optional) Extend your documentation hygiene check to also validate regular markdown links
- Many lightweight doc checks validate backtick `.md` references but do not parse `[text](path)` links.
