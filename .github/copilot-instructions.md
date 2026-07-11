# Copilot Instructions — AI Governance Projection

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This file is a concise projection for GitHub Copilot.
It is not a separate source of truth.

## Quick rules

- For multi-file or cross-cutting changes, produce AEP first (`usage/AEP_VALIDATION.md`).
- If verification fails, use the AVR loop before asking the operator.
- For behavior changes, include DOC DELTA.
- For high-risk changes, use the full `## COMPLIANCE REPORT` from `constitution/AI_ENFORCEMENT.md`.
- High-risk = architecture boundaries, public contracts, CI gates, interface behavior, security, error model.
- Use non-interactive commands and wall-clock timeouts (`constitution/AI_RULES.md` §6.2).

## Read first

- Core rules: `constitution/AI_RULES.md`
- Daily work: `constitution/AI_ENFORCEMENT_DAILY.md`
- High-risk work: `constitution/AI_ENFORCEMENT.md`
- Adaptive governance: `constitution/ADAPTIVE_GOVERNANCE.md`
- Terminology: `architecture/TERMINOLOGY_GLOSSARY.md`
- Architecture decisions: `architecture/README.md` (then framework / prompt as needed)

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

See `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`.

For troubleshooting/performance/debug work, use `usage/DECISION_PROMPTS_DEBUGGING.md` and `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md` (see `usage/DEBUGGING_ACCELERATION_PLAYBOOK.md`). When cause is unclear, falsify hypotheses before fixing (`DBG-science-01`; Prompt 6).

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
- Tests: OK / MISSING
- Docs: OK / UPDATE
- Scope: OK / EXPANDED
- Decision: PROCEED / STOP
```

For high-risk work, use the full `## COMPLIANCE REPORT` from `constitution/AI_ENFORCEMENT.md`.

## Related

- `AGENTS.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `usage/AEP_VALIDATION.md`
