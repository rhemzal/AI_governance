# AGENTS.md — AI Governance Projection

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This is a short agent-facing projection.
The source of truth remains the governance kit documents.

## Import scope (bundle-aware)

Only consult paths that **exist in your imported bundle** (`kit-manifest.yml`). If a referenced path is missing:
- do not invent rules from it
- skip unless the task is **HIGH-risk** and the path is required — then STOP and recommend importing the path or upgrading the bundle

| Bundle | Agent projections include | Typical optional paths (upgrade to `standard` / add bundles) |
| --- | --- | --- |
| **minimal** | `constitution/AI_RULES.md`, `AI_ENFORCEMENT.md`, `AI_ENFORCEMENT_DAILY.md`, `ADAPTIVE_GOVERNANCE.md`, `usage/AEP_VALIDATION.md`, `usage/QUICKGUIDE.md` | `architecture/**`, extended `usage/` playbooks, `usage/ENFORCEMENT_MATRIX.md`, `DEVELOPMENT.md` |
| **standard** | full `constitution/`, `ci/`, `usage/`, overlay template | `architecture/**`, `research/` |

**Terminology:** **Governance Level (G0–G4)** vs **CI Maturity (CM0–CM3)** — see `architecture/TERMINOLOGY_GLOSSARY.md` if imported; otherwise `constitution/ADAPTIVE_GOVERNANCE.md` for G.

## Quick rules

- For multi-file or cross-cutting changes, produce AEP first (`usage/AEP_VALIDATION.md` when present).
- If verification fails, use the AVR loop before asking the operator.
- For behavior changes, include DOC DELTA.
- For high-risk changes, use the full `## COMPLIANCE REPORT` from `constitution/AI_ENFORCEMENT.md`.
- High-risk = architecture boundaries, public contracts, CI gates, interface behavior, security, error model.
- Use non-interactive commands and wall-clock timeouts (`constitution/AI_RULES.md` §6.2).

## Required context

Before work, read or consult as applicable (**skip if path not in bundle**):

- `constitution/AI_RULES.md` *(minimal+)*
- `constitution/AI_ENFORCEMENT_DAILY.md` *(minimal+)*
- `constitution/AI_ENFORCEMENT.md` *(minimal+)*
- `constitution/ADAPTIVE_GOVERNANCE.md` *(minimal+)*
- `usage/AEP_VALIDATION.md` *(minimal+)*
- `architecture/TERMINOLOGY_GLOSSARY.md` *(standard+ or `architecture` bundle)*
- `architecture/README.md` *(standard+ or `architecture` bundle — consult before `architecture/rag/` work)*

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

Use `usage/AEP_VALIDATION.md` when present.

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

See `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` when present.

For troubleshooting/performance/debug work, start at `usage/DEBUGGING_INDEX.md` when present, then `usage/DECISION_PROMPTS_DEBUGGING.md` + catalog/playbook as needed. When cause is unclear, run **Prompt 7** triage (max 3 pattern IDs) before Prompt 6 / fixes.

## Method triage (non-debugging)

When scope or method is unclear, run **method triage** before loading large corpora. Respect **corpus budget** per area (consult `architecture/TERMINOLOGY_GLOSSARY.md` when present):

- **Architecture / RAG:** `architecture/ARCHITECTURE_DECISION_PROMPT.md` — precheck then max 2 RAG notes + 1 cross-cutting (`architecture/README.md`).
- **Security findings:** `usage/SECURITY_MINIMUM_ADOPTION.md` — triage before bulk upgrades (max 3 actions per iteration).
- **Governance audit:** `usage/AUDIT_PLAYBOOK.md` — pick audit scope before Steps 1–5.
- **Kit adoption:** `usage/ADOPTION_BUNDLES.md` — 1 baseline bundle + max 1 optional; defaults in `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`.
- **AEP discovery:** `usage/AEP_VALIDATION.md` — use `usage/PROACTIVE_TRIGGER_MAP.md` to narrow consulted paths when present.
- **Enforcement status:** `usage/ENFORCEMENT_MATRIX.md` — what kit CI automates vs adopter wiring.

Do not paste full playbooks into every task; link and load selected sections only. **Skip bullets for paths not in your bundle.**

## Planning calibration (when `usage/AI_PRODUCTIVITY_CALIBRATION.md` is present)

- **Phase 0–1:** do not state calendar time estimates for human or AI teams.
- Plan with: `task_class`, explicit file paths, iteration budget (**count**, not minutes), verify command, risk (LOW/HIGH).
- After task closure: offer ledger fields (`T_ai_active`, `ai_iterations`, `T_lead`, …) for `notes/local/ai-productivity/ledger.md`.
- Human-duration questions: answer only with `human_source` `measured` | `calibrated_ratio` | `unknown` — never invent a human-team calendar estimate.

## Verification

Always discover repo-local verification first:
- prefer `make` targets if available
- otherwise use repo-local tooling from `DEVELOPMENT.md` when present
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
- consult `architecture/TERMINOLOGY_GLOSSARY.md` when present
- do not introduce project-local acronyms unless explicitly defined
- use **G** / **CM** prefixes — not bare `L0`–`L3`

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
