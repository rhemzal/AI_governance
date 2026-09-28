# Spec-Driven AI Development

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Increase agent reliability by turning important intent into observable acceptance criteria before or alongside implementation.

"Specification" here does not mean a large design document. It can be a compact contract, example, scenario, invariant, fixture, assertion, or measurable budget.

## Verification-first rule of thumb

For non-trivial work, ask before implementation:

> What is the cheapest credible observation that would distinguish success from failure?

If no credible answer exists, the first engineering change may be a test, probe, fixture, contract assertion, or diagnostic surface.

## Specification ladder

| Need | Candidate form |
| --- | --- |
| Pure behavior | Unit/property test |
| API or adapter boundary | Contract/schema test |
| User-visible flow | Scenario/E2E acceptance test |
| Output stability | Golden/snapshot artifact |
| Time-dependent behavior | Virtual clock / accelerated scenario |
| Field-only failure | Redacted record/replay fixture |
| Performance requirement | Measured budget + reproducible workload |
| Resilience requirement | Deterministic fault injection |
| Architecture invariant | Boundary check / static rule |

## Good executable intent

A useful acceptance statement identifies initial state/fixture, action/event, observable result, tolerance/budget where applicable, environment assumptions, and forbidden side effects when important.

```text
Given a connected stream with one consumer,
when the upstream connection resets,
then delivery resumes within the declared test budget,
no duplicate consumer remains,
and the relevant resource counters return to the expected range.
```

## Avoid specification theater

Do not create exhaustive specs for trivial reversible edits, encode implementation details as requirements without reason, update snapshots blindly, make synthetic harnesses the only proof for real scheduling/hardware bugs, or claim verification when the oracle is only subjective agent judgment.

## Relationship to AEP and debugging

AEP defines execution planning and authority for applicable work. Executable specifications define observable success. Scientific debugging defines how to discriminate causes when success is not reached.

## Related documents

- [AI Engineering Methods](AI_ENGINEERING_METHODS.md)
- `ci/TEST_GATES.md`
- `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`
- `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md`
- `usage/AEP_VALIDATION.md`
