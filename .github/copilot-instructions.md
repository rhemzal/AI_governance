# Copilot Instructions — AI Governance Projection

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This file is a concise projection for GitHub Copilot.
It is not a separate source of truth. For full method triage and bundle rules, see `AGENTS.md`.

## Import scope (bundle-aware)

Only consult paths that exist in your imported bundle (`kit-manifest.yml`). If missing, skip — do not invent content. See `AGENTS.md` → Import scope.

## Quick rules

- For multi-file or cross-cutting changes, produce AEP first (`usage/AEP_VALIDATION.md` when present).
- If verification fails, use the AVR loop before asking the operator.
- For behavior changes, include DOC DELTA.
- For high-risk changes, use the full `## COMPLIANCE REPORT` from `constitution/AI_ENFORCEMENT.md`.
- High-risk = architecture boundaries, public contracts, CI gates, interface behavior, security, error model.
- Use non-interactive commands and wall-clock timeouts (`constitution/AI_RULES.md` §6.2).

## Read first

- Core rules: `constitution/AI_RULES.md`
- Daily work: `constitution/AI_ENFORCEMENT_DAILY.md`
- High-risk work: `constitution/AI_ENFORCEMENT.md`
- Adaptive governance (G0–G4): `constitution/ADAPTIVE_GOVERNANCE.md`
- AEP spec: `usage/AEP_VALIDATION.md`
- Terminology (G vs CM): `architecture/TERMINOLOGY_GLOSSARY.md` *(when imported)*
- Architecture decisions: `architecture/README.md` *(when imported)*

## How to work

- Keep changes small, scoped, and reviewable.
- Prefer updating existing documents over creating new large documents.
- Preserve normative/advisory separation:
  - rules and gates: `constitution/`, `ci/`
  - guidance/research: `usage/`, `research/`, `architecture/rag/`
- Do not expand scope silently.
- Do not ask the operator for information that can be found in the repo.

## Risk handling

Use routine mode for small, low-risk edits.

Use high-risk mode before changing:
- architecture boundaries
- dependency rules
- public contracts
- CLI/API/interface behavior
- CI/CD gates
- canonical governance documents
- security behavior
- error model
- system-of-record assumptions

High-risk work must include a full compliance report, ADR consideration, explicit affected-file list, and verification evidence.

## AEP and verification

For multi-file or cross-cutting changes:
- produce AEP first
- declare READY or BLOCKED
- include explicit file paths
- include explicit verification command

Verification must use repo-local commands. Do not assume global test runners.

## Failure handling

If verification fails:
- use AVR loop: detect → diagnose → minimal compliant repair → rerun → report
- do not ask for help unless blocked

## Testing diagnostics

When tests fail, do not default to long log archaeology.
Use the smallest useful scope, stop on first critical signal, capture minimal evidence, apply AVR loop, and rerun.
Do not weaken or delete tests to make the run pass.

See `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` when present.

For troubleshooting/performance/debug work, start at `usage/DEBUGGING_INDEX.md` when present, then prompts/catalog as needed. When cause is unclear, run **Prompt 7** triage (max 3 pattern IDs) before Prompt 6 / fixes.

## Method triage (non-debugging)

When scope is unclear, triage methods before loading large corpora. Full corpus budget and entry points: **`AGENTS.md` → Method triage** (skip paths not in your bundle).

## Documentation

For behavior changes:
- include DOC DELTA
- preserve single source of truth
- avoid duplicate docs

## Output expectations

For low-risk work, end with:

```text
## COMPLIANCE
- AEP: OK / NOT-REQUIRED / BLOCKED
- Architecture: OK / ISSUE
- Overlay: OK / NOT-APPLICABLE / UNKNOWN
- Tests: OK / MISSING
- Docs: OK / UPDATE
- Scope: OK / EXPANDED
- Decision: PROCEED / STOP
```

For high-risk work, use the full `## COMPLIANCE REPORT` from `constitution/AI_ENFORCEMENT.md`.

## Related

- `AGENTS.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md` *(when imported)*
- `usage/AEP_VALIDATION.md`
