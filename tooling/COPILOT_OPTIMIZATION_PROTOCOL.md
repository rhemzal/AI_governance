# Copilot Optimization Protocol (Advisory)

## Purpose
Standardize how you tune Copilot usage patterns in a way that is measurable.

## Key Idea
Optimize for:
- fewer boundary violations
- fewer rework loops
- higher deterministic test pass rate

## Workflow Rules (Recommended)
- Always start tasks by restating scope + constraints.
- Require an explicit compliance report when changing architecture, boundaries, or interface behavior.
- Prefer small diffs.

## Experiment Variables
You can compare:
- prompt style (strict vs daily)
- time-boxing (e.g., 10-minute iterations)
- “test-first” vs “code-first” workflow

## How to Decide
Pick the configuration that:
- consistently produces compliant diffs
- reduces follow-up fixes

## Related Documents
- `adr/ADR_0004_Tooling_Is_Experimental.md`
- `tooling/BENCHMARK_SCENARIOS.md`
- `constitution/AI_ENFORCEMENT_DAILY.md` and `constitution/AI_ENFORCEMENT.md`

