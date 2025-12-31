# Interface CI Gates (Principles)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
These gates enforce automation-first interfaces (GUI/CLI/TUI/headless).

Primary reference:
- `interface/INTERFACE_CI_GATES.md`

## Gate I1: No Mandatory Human Interaction
Fail if the interface:
- blocks waiting for user input in default mode
- uses interactive prompts without a non-interactive alternative

## Gate I2: Headless Execution
Require a CI job that:
- runs interface flows headlessly
- verifies deterministic output format

## Gate I3: Machine-Readable Signals
Require at least one:
- structured output mode (e.g., JSON)
- exit codes / status codes
- stable logs for automation

## Gate I4: Performance Budget (If Declared)
If a performance contract exists:
- enforce it with a repeatable benchmark in CI

## Gate I5: GUI Visual Verification (If Applicable)
If the project has a GUI, require at least one automated verification that the rendered output matches expectations:
- screenshot/visual diff, and/or
- accessibility/DOM snapshot.

If correctness depends on exact visible text, require a rendered-text verification step (e.g., OCR) or equivalent.

## Related Documents
- `interface/INTERFACE_CI_GATES.md`
- `interface/INTERFACE_RULES_PROPOSAL.md`
- `adr/ADR_0001_Automation_First_Interfaces.md`
- `ci/TEST_GATES.md`

