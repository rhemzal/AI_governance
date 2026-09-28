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

## Oracle quality in existing systems

A test is an oracle only for the properties it distinguishes. Derive expected behavior
from an agreed contract, a reported failure, a reviewed example or an independent reference;
a test generated from the new implementation can repeat the same misunderstanding.

- For a bug, reproduce the original failure when practical and keep a nearby success case.
- For poorly isolated legacy code, characterize the touched boundary before changing it.
  Mark known defects separately; a golden output is not automatically the desired behavior.
- For replacements, compare old/new behavior on representative inputs and list intentional
  differences. Use shadow comparison only with authorized, isolated effects and redacted data;
  do not execute payments, writes or device commands twice.
- Property/metamorphic tests can verify relations when exact expected values are hard to
  enumerate. Mutation or fault injection can test whether the oracle detects the relevant
  defect; use it selectively rather than imposing a new project-wide score.
- A fake clock/mock is useful for logic, but does not prove real scheduling, GPU, GUI or
  device behavior. Keep the smallest representative integration observation where needed.

Preserve existing issue/contract/test sources of truth. A specification framework is a
candidate implementation, not a prerequisite; review its artifact duplication and update cost.

## Relationship to AEP and debugging

AEP defines execution planning and authority for applicable work. Executable specifications define observable success. Scientific debugging defines how to discriminate causes when success is not reached.

## Related Documents

- [AI Engineering Methods](AI_ENGINEERING_METHODS.md)
- `ci/TEST_GATES.md`
- `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`
- `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md`
- `usage/AEP_VALIDATION.md`
