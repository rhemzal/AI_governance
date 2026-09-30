# ADR 0013: Test Evidence and Runner Conformance

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If copied, preserve this line._

## Status

Proposed

## Context

Agent-operated debugging depends on trustworthy test instruments. An exit code can hide
empty selection or skipped behavior; a terminated parent can leave a nested process alive.
The preceding NVRM audit used isolated simulated-runner probes to expose these possibilities.
Those probes were not live lab or native CTest validation. Project changes still need
controls at their real native-result and supervision boundaries.

The kit already defines bounded verification, evidence and outcome-based method adoption.
Related repositories already have runners, scenario catalogs, replay fixtures and local
verification paths. Another execution platform would duplicate these mechanisms.

Priorities are correctness of observed acceptance, testability of misleading-pass cases,
and low adoption cost. Representative scenarios are: zero selected required assertions
must not verify; stale run/build evidence must be rejected; interrupted execution must
preserve its outcome and disclose incomplete cleanup.

## Decision

Extend the existing advisory guides with an optional automation profile and concrete runner
conformance controls. Keep execution, native-result normalization, artifact storage and
resource supervision in each host project.

Provide a small standard-library data assessor, `ci/validate_test_evidence.py`, with pure
assessment logic separated from JSON file/command-line handling. Its inputs are independently
resolved expectations and normalized observations. A non-empty required set, matching
identities, passing required observations, successful execution and applicable cleanup
are necessary for its declared-data verdict. The helper never executes supplied commands.

Review common guidance upstream first. Prepare narrow downstream fixes under the accepted
baseline, then update pins and active local adoption records after upstream acceptance.
Existing host coordination and authority remain applicable.

## Alternatives Considered

- Prose alone: cheapest to import, but does not provide executable negative controls for
  consumers choosing machine-readable evidence. Prose remains sufficient for small tasks.
- Universal runner, report store or agent platform: duplicates existing host capabilities
  and adds operational ownership without evidence of need.
- Mandatory adopter gate: premature before native normalizers and scoped pilots demonstrate
  useful signal. This decision installs no new adopter requirement.

## Trade-Offs

The shared reference makes failure cases inspectable at low dependency cost. A host may
prefer equivalent assertions in its existing format. Normalization is an additional
maintenance responsibility only when that host elects to use the helper.

The helper validates declarations, not reality. Fabricated evidence can satisfy it; artifact
references are not dereferenced, identities are not authenticated and cleanup is not
observed by the helper. Its verdict never substitutes for the whole task's acceptance.

## Sensitivity Points & Risks

- Required checks and tested identities must come from independent host expectations, not
  from the candidate report. A source label alone does not identify an executed binary.
- Native adapters must distinguish setup/teardown, behavior skips, discovery and execution.
  Test known-good, empty, failed, skipped and stale native reports.
- Cancellation must be tested through the actual supervisor, including nested sessions.
  Direct-child tests alone cannot establish descendant cleanup.
- Compare adoption benefit with missed failures, repair/review effort and maintenance cost.
  Small synthetic controls do not establish broad agent productivity gains.

## Points of No Return

No new service, storage system or mandatory workflow is introduced. A host can retire the
optional helper while retaining its native tests and existing mandatory invariants.

## Consequences

Standard/full imports receive the helper through the existing `ci/` directory selection.
Minimal imports remain documentation-only. Importing files does not activate a runner or
a local enforcement policy. Project pilots and accepted pin changes remain explicit.

## Enforcement

The kit's existing `ci/gate_tests` job runs positive and negative reference-helper tests.
Its existing path filters include the helper so later code-only changes trigger those tests.
No new workflow or governance gate is added. Host activation and acceptance require the
host's own reviewed wiring and observed results.

## Documentation Impact

Source of truth: `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` for execution guidance and
`usage/AI_RUN_EVIDENCE.md` for the optional input contract. Update the existing method
selector, adoption and evaluation guides, changelog and ADR index. No duplicated guide
or generated documentation is introduced; no existing document needs removal.

## Governance Change

- Advisory guidance and optional reference tooling; constitutional rules are unchanged.
- No imported kit upgrade occurs in this repository; no local overlay override is approved.
- Existing CI job gains regressions, not a new gate. Downstream enforcement is opt-in.
- Downstream pins move only after upstream acceptance; each host records pilot scope,
  unavailable checks, promotion/retirement criteria and rollback under its current controls.

## Related Documents

- [Test execution and diagnostics](../usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md)
- [Run evidence](../usage/AI_RUN_EVIDENCE.md)
- [Existing-project adoption](../usage/ENGINEERING_METHODS_ADOPTION.md)
- [Agent evaluation](../usage/AGENT_EVALUATION.md)
