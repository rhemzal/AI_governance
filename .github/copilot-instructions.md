# Copilot Instructions — AI Governance Projection

This file is a concise projection for GitHub Copilot.
It is not a separate source of truth.

## Read first

- Core rules: `constitution/AI_RULES.md`
- Daily work: `constitution/AI_ENFORCEMENT_DAILY.md`
- High-risk work: `constitution/AI_ENFORCEMENT.md`
- Adaptive governance: `constitution/ADAPTIVE_GOVERNANCE.md`
- Terminology: `architecture/TERMINOLOGY_GLOSSARY.md`

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
- public contracts
- interface behavior
- CI/CD gates
- security behavior
- canonical governance rules

High-risk work must include a compliance report and ADR consideration.

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

## Documentation

For behavior changes:
- include DOC DELTA
- preserve single source of truth
- avoid duplicate docs

## Related

- `AGENTS.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `usage/AEP_VALIDATION.md`
