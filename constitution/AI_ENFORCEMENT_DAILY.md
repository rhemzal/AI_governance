# AI_ENFORCEMENT_DAILY — Minimal Daily Prompt

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

Use this for 90% of everyday AI-assisted work.

## Paste This at the Start of Your Prompt
Load `constitution/AI_RULES.md`.
Respect architectural boundaries.
If any rule would be violated, stop and report.
Continue within the authorized task mandate; obtain approval before a new objective or unauthorized effect.

## Daily Checklist
- AEP: If HIGH-risk, dependent non-trivial steps, handoff, or concurrency are involved, is the Autonomous Execution Plan declared READY before edits? Routine reversible work may use a concise scope and verification statement.
  - **Discovery:** consult `usage/PROACTIVE_TRIGGER_MAP.md` before broad doc loads (`usage/AEP_VALIDATION.md`).
- Architecture: Which layer is this change in?
- Boundaries: Any inward-dependency violation?
- Overlay: Is there a local governance overlay, and was it considered?
- Determinism: Any hidden time/random/env dependency?
- Tests: What tests are required and where do they live?
  - **Test execution**: Use repo-local test command (e.g., `make test`, `.venv/bin/python -m pytest`, or docker). **Never assume global pytest.**
- **AVR loop**: If verification fails, diagnose, apply the smallest compliant fix, rerun checks, and report within the declared repair budget. Stop the affected action only on a real blocker or exhausted budget (`AI_ENFORCEMENT.md` §1.3).
- Docs: What documentation must be updated (or deleted)?
- Scope: List affected files.
- Authority: Confirm allowed effects and targets; preparation does not authorize merge or deployment.
- Evidence: Bind results to the tested revision/environment and identify unmet acceptance criteria.

## Required Mini-Report
## COMPLIANCE
- AEP: OK / NOT-REQUIRED / BLOCKED
- Architecture: OK / ISSUE
- Overlay: OK / NOT-APPLICABLE / UNKNOWN
- Tests: OK / MISSING
- Docs: OK / UPDATE
- Scope: OK / EXPANDED
- Decision: PROCEED / STOP

## Related Documents

- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
- `usage/LOCAL_OVERLAY_AND_PRECEDENCE.md`
- `usage/AEP_VALIDATION.md`
- `usage/PROACTIVE_TRIGGER_MAP.md`
- `ci/TEST_GATES.md`
- `ci/ARCHITECTURE_GATES.md`
