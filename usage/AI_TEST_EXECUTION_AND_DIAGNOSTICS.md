# AI Test Execution & Diagnostics Playbook

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Guide AI agents to test in short, observable, fail-fast loops.

This document is advisory execution guidance. Normative test gates remain in `ci/TEST_GATES.md`.

## Core principle

Detect failures during execution, not only after execution.

AI agents should prefer short, observable test loops over long runs followed by log archaeology.

## Execution loop

1. Define the smallest useful test scope.
2. Enable relevant diagnostic signals/watchers.
3. Run the check non-interactively.
4. Stop on the first critical signal.
5. Capture minimal evidence.
6. Diagnose the likely cause.
7. Apply the smallest compliant repair.
8. Rerun the smallest useful scope.
9. Escalate only when blocked.

## Failure signal classes

Examples of critical signals:

- assertion failure
- uncaught runtime exception
- browser/page error
- critical console error
- failed required network request
- timeout
- visual / DOM / accessibility mismatch
- schema / contract violation
- performance budget breach

## GUI diagnostics

For GUI/web/desktop/mobile interface tests:

- prefer live failure detection over post-run log archaeology
- attach watchers before executing the scenario
- stop on first critical browser/runtime signal
- capture minimal evidence: screenshot, trace, DOM snapshot, video, network/console slice, or equivalent
- use stable user-visible locators/contracts where possible
- avoid brittle selectors tied to implementation details
- avoid manual sleeps; prefer framework-native waiting/assertions
- do not full-rerun the entire E2E suite until the smallest failing scope is understood

## CLI/API diagnostics

For CLI/API/headless interfaces:

- verify exit/status code first
- prefer structured output where applicable
- keep stdout/stderr semantics stable
- validate schemas/contracts before full E2E flows
- rerun the smallest failing command/request first

## Evidence before repair

Before modifying code, the agent should preserve enough evidence to explain the failure.

Evidence may be:

- failing assertion
- relevant log slice
- trace/screenshot/video
- request/response sample
- schema violation
- minimized reproduction command

Do not collect excessive artifacts when the first failure signal is already sufficient.

## Do not hide failures

The AI must not:

- delete tests to make the run green
- weaken assertions without justification
- replace deterministic checks with vague snapshots
- ignore failing diagnostics because a later step passed
- treat flaky failure as product failure without evidence

## Flaky vs deterministic failures

If the failure is not reproducible:

- mark it as suspected flakiness or environment issue
- capture the evidence
- avoid broad product-code changes
- recommend quarantine, retry policy, or environment stabilization if appropriate

## Required output

When testing/diagnosing, the AI should report:

```text
TEST DIAGNOSTICS REPORT
- Test scope:
- Command/check:
- Watchers/signals enabled:
- First failure signal:
- Evidence captured:
- Diagnosis:
- Repair attempted:
- Rerun command:
- Result:
- Escalation needed: yes/no
```

## Related Documents

* `ci/TEST_GATES.md`
* `ci/INTERFACE_GATES.md`
* `interface/INTERFACE_RULES_PROPOSAL.md`
* `constitution/AI_ENFORCEMENT_DAILY.md`
* `AGENTS.md`
* `usage/PROACTIVE_TRIGGER_MAP.md`
