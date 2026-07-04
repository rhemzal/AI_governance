# Interface CI Gates (Principles)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
These gates enforce automation-first interfaces (GUI/CLI/TUI/headless).

Primary reference:
- `interface/INTERFACE_CI_GATES.md`

See `constitution/ADAPTIVE_GOVERNANCE.md` for guidance on which level each gate is appropriate for.

## Gate: I1 — No Mandatory Human Interaction

- **Recommended from level:** 1
- **Mandatory from level:** 2
- **Risk mitigated:** Interfaces that block in CI or automation contexts; scripts that hang indefinitely waiting for user input.
- **Local alternative:** Manual smoke-test the interface with `--non-interactive` or equivalent flag before commit.
- **Cost:** Very low. Requires only a flag or mode check at interface design time.
- **Failure action:** Fail the pipeline. The AI MUST NOT ship an interface that blocks in non-interactive mode. Require a non-interactive alternative (flag/mode) before accepting the change.

Fail if the interface:
- blocks waiting for user input in default mode
- uses interactive prompts without a non-interactive alternative

## Gate: I2 — Headless Execution

- **Recommended from level:** 2
- **Mandatory from level:** 3
- **Risk mitigated:** Interface flows that cannot be verified in CI; regressions in CLI or API output that go undetected.
- **Local alternative:** At Level 1–2, run the interface flow manually and confirm deterministic output. Document the expected output in a comment or test fixture.
- **Cost:** Low to medium. A simple shell script or integration test covers most cases.
- **Failure action:** At Level 3+, block merge until a headless CI job exists and passes. At Level 2, warn if no headless verification is present.

Require a CI job that:
- runs interface flows headlessly
- verifies deterministic output format

## Gate: I3 — Machine-Readable Signals

- **Recommended from level:** 1
- **Mandatory from level:** 2
- **Risk mitigated:** Interfaces that are difficult to compose with other tools; silent failures that produce no parseable output.
- **Local alternative:** At Level 0–1, ensure exit codes are set correctly. Structured output (JSON) can be deferred.
- **Cost:** Low. Exit codes are free. A `--json` flag is a small addition.
- **Failure action:** At Level 2+, block merge if the interface produces no machine-readable signal (no exit code, no structured output, no stable log format).

Require at least one:
- structured output mode (e.g., JSON)
- exit codes / status codes
- stable logs for automation

## Gate: I4 — Performance Budget (If Declared)

- **Recommended from level:** 3
- **Mandatory from level:** 4
- **Risk mitigated:** Performance regressions that violate declared contracts; latency or throughput degradation undetected until production.
- **Local alternative:** At Level 1–2, run a manual timing check (e.g., `time ./cli`) and note the result in the commit. No automated benchmark required.
- **Cost:** Medium to high. Benchmarks require setup, baseline management, and can be flaky. Do not add unless a performance contract is declared.
- **Failure action:** At Level 4, block merge if the benchmark fails the declared budget. At Level 3, warn and open a follow-up issue.

If a performance contract exists:
- enforce it with a repeatable benchmark in CI

## Gate: I5 — GUI Visual Verification (If Applicable)

- **Recommended from level:** 3
- **Mandatory from level:** 4
- **Risk mitigated:** Visual regressions in rendered output; text-critical GUI elements that break without detection.
- **Local alternative:** At Level 1–2, manual visual inspection is sufficient. Screenshot diffing is not required.
- **Cost:** High. Visual diffing tools require baseline management, are sensitive to rendering differences, and add CI complexity. Only add if the project has a GUI and visual regressions are a real risk.
- **Failure action:** At Level 4, block merge on visual diff failures. At Level 3, warn and require human review of the diff.

If the project has a GUI, require at least one automated verification that the rendered output matches expectations:
- screenshot/visual diff, and/or
- accessibility/DOM snapshot.

If correctness depends on exact visible text, require a rendered-text verification step (e.g., OCR) or equivalent.

## Related Documents
- `interface/INTERFACE_CI_GATES.md`
- `interface/INTERFACE_RULES_PROPOSAL.md`
- `constitution/ADAPTIVE_GOVERNANCE.md`
- `adr/ADR_0001_Automation_First_Interfaces.md`
- `ci/TEST_GATES.md`

