# Benchmark Scenarios (AI-Assisted Engineering)

## Purpose
These scenarios are designed to evaluate AI assistance with measurable outcomes.

## Scenario B1: Boundary-Safe Feature Add
- Add a small feature without breaking architecture boundaries.
- Pass criteria: tests pass; no forbidden dependencies; minimal diff.

## Scenario B2: Interface Automation-First
- Add/modify an interface flow so it runs headlessly.
- Pass criteria: non-interactive mode exists; deterministic output; CI job added.

## Scenario B3: Robustness Fix
- Fix an error-handling gap.
- Pass criteria: explicit error model; tests cover failure mode.

## Scenario B4: Docs + ADR Consistency
- Make an architecture-impacting change.
- Pass criteria: ADR created/updated; docs updated; no duplication.

## Related Documents
- `tooling/AI_TOOL_OPTIMIZATION.md`
- `adr/ADR_TEMPLATE.md`
- `ci/ARCHITECTURE_GATES.md`

