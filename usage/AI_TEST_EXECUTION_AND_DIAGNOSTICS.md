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

## Optional automation profile

Automate a reliable loop inside the existing runner before adding another orchestration
service. This profile is advisory: it adds no mandatory governance gate, runner, artifact
store, or model service. A project can adopt one capability at a time and run it locally
when hosted continuous integration (CI) is unavailable.

| Stage | Smallest useful automation | Evidence / stop condition |
| --- | --- | --- |
| Select | Map the symptom or changed boundary to existing scenario IDs | Record required checks before execution; an unknown mapping falls back to an existing broader check, never an empty success |
| Preflight | Check fixture, build, permissions and declared resource ownership | Missing prerequisites are explicit; discovery alone does not establish execution |
| Execute | Invoke the existing bounded, non-interactive command | Preserve exit status, timeout, cancellation and every retry |
| Observe | Collect native test results and the first useful diagnostic | Identify executed behavior assertions, required skips and missing results |
| Evaluate | Compare observations with independent acceptance criteria | Process exit zero alone is insufficient |
| Reproduce | Minimize the failure into an existing fixture/replay path | The control detects the defect before the repair and accepts intended behavior after it |
| Release | Verify cleanup at the actual supervising boundary | Report remaining processes/resources; parent exit alone is insufficient |

Reuse a project's scenario catalog, metadata and report format. A small explicit mapping
is usually enough for initial test selection. Measure missed relevant checks before
introducing a model-based selector or a new coverage database.

### Runner conformance controls

Before trusting automated diagnosis, exercise the instrument with disposable fixtures.
Select controls for the runner's actual failure modes:

| Control | Expected observation |
| --- | --- |
| Known-good selected behavior | Required behavior assertions execute and pass |
| Injected assertion failure, including a wrapper that exits zero | Native failure remains a failure |
| Empty selection or renamed test | No successful outcome; report what was selected and executed |
| Missing fixture or all required behavior skipped | Prerequisite/coverage gap, not a pass |
| Old report, stale binary or wrong fixture | Reject the mismatched run/build/fixture identity |
| Timeout or cancellation through the real supervisor | Forward termination, finish bounded cleanup and preserve the outcome |
| Parent exits while a descendant remains alive | Cleanup remains incomplete; do not release ownership as if nothing remains |
| Retry after failure | Keep both attempts; a later pass does not erase the first failure |

Count executed behavior assertions, not discovery entries or setup/teardown successes.
An outer test may pass while a nested framework skips the behavior of interest; normalize
that framework's native results before deciding success. A headless GUI check establishes
only the tier it exercises, not device presentation or rendering quality.

Exercise cancellation across the actual process boundary used by the backend or launcher,
including nested subprocess sessions when present. A direct-child unit test cannot prove
that boundary safe. Cleanup should target resources owned by the run, not unrelated
processes found by name. Record incomplete cleanup before releasing a device lease.

### Turn a failure into a regression

1. Preserve the first failing result, exact tested identities and bounded diagnostics.
2. Distinguish product failure from environment, fixture and harness failure; test competing
   explanations before changing product code.
3. Minimize a replay in the existing fixture path. Pin relevant inputs, clock and event
   order; a random seed alone may not reproduce a concurrent failure.
4. Keep the expected result independent of the repair. Demonstrate failure before and
   success after the change, then run adjacent compatibility checks.
5. Version the small regression fixture and its expectation; redact sensitive captures
   and retain bulky artifacts according to existing project policy.

For repeated ordering/lifecycle defects, a small stateful test can complement one replay.
Start with one invariant and the existing test framework. Defer a general chaos platform.
Do not automatically weaken the oracle, bless a snapshot or retry until green.

Use [run evidence](AI_RUN_EVIDENCE.md) for comparable observations and
[existing-project adoption](ENGINEERING_METHODS_ADOPTION.md) for a bounded pilot.

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

## Hypothesis before repair

When the cause is unclear, do not implement the first guess.

0. Run **method triage** first: `usage/DECISION_PROMPTS_DEBUGGING.md` **Prompt 7** (max 3 pattern IDs; do not enumerate the full catalog).
1. Formulate 2–3 competing **working hypotheses** (`architecture/TERMINOLOGY_GLOSSARY.md`).
2. Run the cheapest **falsification test** per hypothesis before editing product code (`DBG-science-01` in `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md`).
3. State **prediction-before-change** before any fix (`DBG-science-02`): if H holds, after X we will see Y.
4. If the prediction fails after the change, revert and reject H.

Use **Prompt 7** → **Prompt 6** and the scientific-style section in `usage/DEBUGGING_ACCELERATION_PLAYBOOK.md`.

When investigation depends on test runners, MCP, or CI harnesses, run an **instrument sanity check** (`DBG-science-07`) before long product-code changes.

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

* `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md`
* `usage/DECISION_PROMPTS_DEBUGGING.md`
* `ci/TEST_GATES.md`
* `ci/INTERFACE_GATES.md`
* `interface/INTERFACE_RULES_PROPOSAL.md`
* `constitution/AI_ENFORCEMENT_DAILY.md`
* `AGENTS.md`
* `usage/PROACTIVE_TRIGGER_MAP.md`
