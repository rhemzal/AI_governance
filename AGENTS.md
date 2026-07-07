# AGENTS.md — AI Governance Projection

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This is a short agent-facing projection.
The source of truth remains the governance kit documents.

## Quick rules

- For multi-file or cross-cutting changes, produce AEP first (`usage/AEP_VALIDATION.md`).
- If verification fails, use the AVR loop before asking the operator.
- For behavior changes, include DOC DELTA.
- For high-risk changes, use the full `## COMPLIANCE REPORT` from `constitution/AI_ENFORCEMENT.md`.
- High-risk = architecture boundaries, public contracts, CI gates, interface behavior, security, error model.
- Use non-interactive commands and wall-clock timeouts (`constitution/AI_RULES.md` §6.2).

## Required context

Before work, read or consult as applicable:
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT_DAILY.md`
- `constitution/AI_ENFORCEMENT.md`
- `constitution/ADAPTIVE_GOVERNANCE.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`
- `architecture/README.md` (architecture entry point; consult before `architecture/rag/` work)
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

## Test diagnostics

When testing:
- run the smallest useful scope first
- prefer fail-fast diagnostics over long post-run log analysis
- stop on first critical signal
- capture minimal evidence
- use the AVR loop before asking the operator
- do not weaken or delete tests to make verification pass

See `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`.

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
