# AEP Validation Specification (Machine-Checkable)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This specification defines minimum checks for an Autonomous Execution Plan (AEP) declared `AEP Status: READY`.

It aligns with:
- `constitution/AI_ENFORCEMENT.md` (Section 1.1)
- `governance/LOCAL_OVERLAY_TEMPLATE.md` (AEP validation rules)

## Applicability
- AEP is required for tasks spanning 2+ files or code+tests+docs.
- Trivial single-file edits may use the standard compliance pre-check instead.

## Required fields for `READY`
1. `Objective`: observable outcome (1–2 sentences).
2. `Discovery log`: consulted files/rules/ADRs and assumptions.
3. `Risk`: `LOW | HIGH` with justification.
4. `Steps`: ordered, concrete steps. Each step must include:
   - at least one explicit file path
   - action verb (e.g., add/update/remove)
   - reason
5. `Test execution step`: explicit repo-local command (no placeholders).
6. `Doc update step`: required when behavior changes (`DOC DELTA` compatibility).
7. `Blocking questions`: 0–3; READY requires zero blocking questions.
8. `Exit criteria`: tests green, docs aligned, compliance output.
9. `AEP Status`: `READY` or `BLOCKED`.

## Fail conditions for `READY`
Mark plan invalid (fail) if any apply:
- missing any required field above
- any step contains `TBD`, `TODO`, `later`, `as needed`, `etc.`, or similarly vague placeholders
- any step lacks explicit file paths
- missing explicit test command
- steps require operator input while status is `READY`
- blocking questions are present while status is `READY`
- status is `READY` but unresolved dependencies are present

## Suggested CI/Lint Output Contract
- Output: `PASS` or `FAIL`
- On failure: report field-level reasons (e.g., `missing test command`, `step 3 missing file path`)
- Keep this validator advisory until integrated as a required check in local policy

## Related Documents
- `constitution/AI_ENFORCEMENT.md`
- `governance/LOCAL_OVERLAY_TEMPLATE.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
