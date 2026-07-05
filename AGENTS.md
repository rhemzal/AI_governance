# AGENTS.md — AI Governance Projection

This is a short agent-facing projection.
The source of truth remains the governance kit documents.

## Required context

Before work, read or consult as applicable:
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT_DAILY.md`
- `constitution/AI_ENFORCEMENT.md`
- `constitution/ADAPTIVE_GOVERNANCE.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`
- `usage/AEP_VALIDATION.md`

## Default operating mode

For routine work:
- use `constitution/AI_ENFORCEMENT_DAILY.md`
- keep scope explicit
- keep diffs small
- prefer updating existing documents over creating new files
- preserve normative/advisory separation

## High-risk mode

Use `constitution/AI_ENFORCEMENT.md` before changing:
- architecture boundaries
- dependency rules
- public contracts
- CLI/API/interface behavior
- CI/CD gates
- canonical governance documents
- security behavior
- error model
- system-of-record assumptions

High-risk work requires:
- compliance report
- ADR consideration
- explicit affected-file list
- verification evidence

## AEP requirement

For changes spanning 2+ files, or crossing code + tests + docs:
- produce an Autonomous Execution Plan (AEP)
- declare `AEP Status: READY | BLOCKED`
- READY means no blocking questions remain
- READY requires explicit file paths and an explicit verification command

Use `usage/AEP_VALIDATION.md`.

## AVR loop

When verification fails:
- detect the failure
- diagnose the likely cause
- apply the smallest compliant repair
- rerun verification
- report the result

Do not ask the operator unless genuinely blocked.

## Verification

Always discover repo-local verification first:
- prefer `make` targets if available
- otherwise use repo-local tooling from `DEVELOPMENT.md`
- do not assume global test runners
- do not run interactive commands
- use timeouts for long-running commands where possible

## Documentation impact

When behavior changes:
- include or update `DOC DELTA`
- preserve single source of truth
- update existing docs before adding new docs
- remove or consolidate obsolete docs when needed

## Terminology

When using acronyms or overloaded terms:
- expand on first use
- consult `architecture/TERMINOLOGY_GLOSSARY.md`
- do not introduce project-local acronyms unless explicitly defined

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
