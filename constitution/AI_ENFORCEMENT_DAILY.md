# AI_ENFORCEMENT_DAILY — Minimal Daily Prompt

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

Use this for 90% of everyday AI-assisted work.

## Paste This at the Start of Your Prompt
Load `constitution/AI_RULES.md`.
Respect architectural boundaries.
If any rule would be violated, stop and report.
Do not expand scope without confirmation.

## Daily Checklist
- AEP: If multi-file change, is the Autonomous Execution Plan declared READY before edits?
  - **Discovery:** consult `usage/PROACTIVE_TRIGGER_MAP.md` before broad doc loads (`usage/AEP_VALIDATION.md`).
- Architecture: Which layer is this change in?
- Boundaries: Any inward-dependency violation?
- Overlay: Is there a local governance overlay, and was it considered?
- Determinism: Any hidden time/random/env dependency?
- Tests: What tests are required and where do they live?
  - **Test execution**: Use repo-local test command (e.g., `make test`, `.venv/bin/python -m pytest`, or docker). **Never assume global pytest.**
- **AVR loop**: If verification fails, diagnose, apply the smallest compliant fix, rerun checks, and report. Do not ask the operator unless blocked.
- Docs: What documentation must be updated (or deleted)?
- Scope: List affected files.

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
