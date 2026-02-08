# Test CI Gates (Principles)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
These gates enforce “no untested behavior” and prevent regressions.

## Gate T1: Deterministic, Headless Tests
Fail if:
- tests require human input
- tests depend on wall-clock time without control
- tests depend on network unless explicitly marked as integration

## Gate T2: Coverage as a Risk Signal (Not Vanity)
Require one of:
- minimum coverage threshold per critical package
- or explicit waiver documented in PR (risk accepted, why, follow-up issue)

## Gate T3: Layered Testing Expectations
- Core (domain/use-cases): fast unit/behavior tests, no I/O
- Boundary contracts (ports/interfaces): mocked or faked in core tests
- Integration boundary (adapters/infrastructure): contract/integration tests where appropriate

## Gate T4: Flakiness Budget
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
- the most important risk is “wrong behavior”, not internal structure

Common hybrid (recommended):
- use BDD-style acceptance/contract tests to lock behavior at boundaries
- use TDD-style unit tests to lock core logic cheaply
- keep UI/E2E minimal; prefer headless, deterministic seams

Methodology does not bypass gates:
- if you change a boundary contract, tests must change with it (and justify why)
- integration/UI tests are allowed only when they are stable and non-interactive

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
- `ci/ARCHITECTURE_GATES.md`
- `ci/INTERFACE_GATES.md`

