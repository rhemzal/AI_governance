# AI_ENFORCEMENT_DAILY — Minimal Daily Prompt

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

Use this for 90% of everyday AI-assisted work.

## Paste This at the Start of Your Prompt
Load `constitution/AI_RULES.md`.
Respect architectural boundaries.
If any rule would be violated, stop and report.
Do not expand scope without confirmation.

## Daily Checklist
- Architecture: Which layer is this change in?
- Boundaries: Any inward-dependency violation?
- Overlay: Is there a local governance overlay, and was it considered?
- Determinism: Any hidden time/random/env dependency?
- Tests: What tests are required and where do they live?
- Docs: What documentation must be updated (or deleted)?
- Scope: List affected files.

## Required Mini-Report
## COMPLIANCE
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
- `ci/TEST_GATES.md`
- `ci/ARCHITECTURE_GATES.md`
