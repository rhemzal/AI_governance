# Risk Preflight Prompt (Copy/Paste)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

Use this at the start of a task to force a consistent LOW vs HIGH risk classification before edits.

## Prompt
"Do a risk preflight before changes:
- List exact files you will touch
- Confirm whether any boundary contract/interface, adapter/integration, architecture decision, security behavior, CI/gates, or canonical governance docs are affected
Return: `Risk: LOW|HIGH` + 1–2 sentence justification.
If LOW: proceed to execution.
If HIGH/unclear: STOP and ask for confirmation."

## Notes
- Keep this prompt as a single source of truth. Link to it instead of duplicating.
- For high-risk work, prefer `constitution/AI_ENFORCEMENT.md`.
- For daily/low-risk work, prefer `constitution/AI_ENFORCEMENT_DAILY.md`.
