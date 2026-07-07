# Test CI Gates (Principles)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
These gates enforce “no untested behavior” and prevent regressions.

See `constitution/ADAPTIVE_GOVERNANCE.md` for guidance on which level each gate is appropriate for.

## Gate: T1 — Deterministic, Headless Tests

- **Recommended from level:** 1
- **Mandatory from level:** 2
- **Risk mitigated:** Non-deterministic test results that mask real failures; tests that require human input and cannot run in CI.
- **Local alternative:** Run tests locally with `make test` or equivalent. At Level 0–1, local execution is sufficient; no CI required.
- **Cost:** Very low. Deterministic, headless tests are the baseline expectation for any test that will be rerun.
- **Failure action:** Fail the pipeline. Non-deterministic or interactive tests MUST be fixed or quarantined before merge.

Fail if:
- tests require human input
- tests depend on wall-clock time without control
- tests depend on network unless explicitly marked as integration

## Gate: T2 — Coverage as a Risk Signal (Not Vanity)

- **Recommended from level:** 2
- **Mandatory from level:** 3
- **Risk mitigated:** Critical logic paths with no test coverage; regressions in untested code going undetected.
- **Local alternative:** At Level 0–1, coverage is not required. At Level 2, a developer or AI agent review of uncovered critical paths is sufficient.
- **Cost:** Low to medium. Coverage tooling is cheap to run. Coverage thresholds that block iteration are expensive; use them carefully.
- **Failure action:** At Level 3+, fail the pipeline if coverage falls below the declared threshold for critical packages. At Level 2, require a waiver comment if coverage is not tracked.

Require one of:
- minimum coverage threshold per critical package
- or explicit waiver documented in PR (risk accepted, why, follow-up issue)

## Gate: T3 — Layered Testing Expectations

- **Recommended from level:** 2
- **Mandatory from level:** 3
- **Risk mitigated:** Core logic tested only through integration tests (slow, fragile); boundary contracts tested without isolation (coupling).
- **Local alternative:** At Level 1, ensure core logic has at least one fast unit test. Integration tests can be deferred.
- **Cost:** Low. Layered testing is a design principle, not a tooling cost. The cost is in discipline, not infrastructure.
- **Failure action:** At Level 3+, block merge if core logic has no unit tests. Require a stated testing layer justification.

- Core (domain/use-cases): fast unit/behavior tests, no I/O
- Boundary contracts (ports/interfaces): mocked or faked in core tests
- Integration boundary (adapters/infrastructure): contract/integration tests where appropriate

## Gate: T4 — Flakiness Budget

- **Recommended from level:** 2
- **Mandatory from level:** 3
- **Risk mitigated:** Flaky tests that erode trust in the test suite; persistent flakiness masking real failures.
- **Local alternative:** At Level 1, note flaky tests in `notes/` and rerun manually when suspected. At Level 2, quarantine flaky tests rather than deleting them.
- **Cost:** Low to medium. Flakiness tracking requires a policy and minimal tooling. The cost of not tracking is higher over time.
- **Failure action:** At Level 3+, fail builds after N flakes in a window. Require a fix or quarantine policy before merge.

If tests are flaky:
- fail builds after N flakes in a window
- require a fix or quarantine policy

## Guidance: TDD vs BDD (Not a Mandate)
This kit does **not** mandate a specific methodology. It mandates tests that are **deterministic**, **reviewable**, and that **protect contracts**.

Choose **TDD** (Test-Driven Development) when:
- you are changing core logic / invariants
- correctness is best expressed as small, stable tests
- you want fast feedback and design pressure on core APIs

Choose **BDD** (Behavior-Driven Development) when:
- you are changing workflows / acceptance criteria
- you need tests to communicate intent across roles (product/QA/engineering)
- the most important risk is "wrong behavior", not internal structure

Common hybrid (recommended):
- use BDD-style acceptance/contract tests to lock behavior at boundaries
- use TDD-style unit tests to lock core logic cheaply
- keep UI/E2E minimal; prefer headless, deterministic seams

Methodology does not bypass gates:
- if you change a boundary contract, tests must change with it (and justify why)
- integration/UI tests are allowed only when they are stable and non-interactive

## Guidance: TDD vs AVR loop
- **TDD** is a development methodology: failing tests drive design of new behavior.
- **AVR loop** (Autonomous Verification & Repair) is an AI-agent execution pattern: verify → detect failure → diagnose → minimal compliant repair → rerun checks → report.
- Use **TDD** when tests should drive design of new behavior.
- Use **AVR** whenever an AI agent executes work autonomously and must verify, detect failures, repair minimally, and rerun checks without operator input.
- **AVR does not replace** TDD, BDD, integration tests, or CI gates — it complements them during autonomous agent execution.

## Guidance: Fail-Fast Diagnostic Testing

AI agents SHOULD prefer short, observable test loops.

When a test can expose critical runtime signals during execution, the agent SHOULD stop on the first critical signal instead of completing a long scenario and analyzing logs afterward.

Critical signals include:
- assertion failures
- uncaught runtime errors
- failed required network calls
- critical console errors
- timeouts
- contract/schema violations
- visual/DOM/accessibility mismatches

The agent MUST preserve enough evidence to diagnose the failure before attempting repair.

See `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`.

## Advisory: Advanced Testing Techniques (Optional)
These techniques are **optional** and should be considered based on risk profile and complexity. Use them when they provide clear risk reduction beyond standard tests.

**Property-based testing (PBT)**
- Use when invariants are complex or span many input combinations.
- Use when you want to discover edge cases automatically rather than listing examples.
- Focus on domain rules that must hold for all valid inputs (e.g., roundtrip encoding, commutativity, associativity).

**Stateful testing**
- Use when behavior depends on sequences of operations (e.g., state machines, workflows, resource lifecycle).
- Use when single-operation tests miss bugs that only appear after specific transitions.

**Schema-driven API testing**
- Use when API schemas (OpenAPI, GraphQL, JSON Schema) exist and can be validated programmatically.
- Use to enforce contract conformance automatically (request/response shapes, required fields, types).

**Mutation testing**
- Use when test quality is uncertain and you want evidence that tests catch real bugs.
- Use to find weak tests that pass even when code is broken.
- Note: typically slower; consider on critical paths only.

**Chaos/resilience testing**
- Use when system must tolerate partial failures (network, dependencies, infrastructure).
- Use to validate retry logic, circuit breakers, fallback behavior, and graceful degradation.

**Load/soak testing**
- Use when throughput, latency, or resource exhaustion are risks.
- Use to find leaks, contention, or scalability limits before production.

**Fuzzing**
- Use when parsing untrusted input (file formats, network protocols, user-supplied data).
- Use to discover crashes, hangs, or security vulnerabilities via randomized inputs.

## Related Documents
- `constitution/AI_RULES.md` and `constitution/AI_ENFORCEMENT.md`
- `constitution/ADAPTIVE_GOVERNANCE.md`
- `ci/ARCHITECTURE_GATES.md`
- `ci/INTERFACE_GATES.md`
- `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`
