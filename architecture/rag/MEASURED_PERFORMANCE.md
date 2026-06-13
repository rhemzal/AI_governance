# Measured Performance — Advisory Note

## Core Idea
Performance decisions should be based on **measurement and budgets**, not assumptions.

## Practical Heuristics
- Define a performance budget for critical flows.
- Benchmark under representative conditions.
- Prefer changes that keep boundaries intact; break boundaries only when measured.

## Structural Changes and Build Performance
The same measurement discipline applies to structural and build-graph changes:
- Do not reorganise modules or split build targets to "improve build speed" without a baseline measurement.
- If the claim is "this extraction reduces rebuild time", show the before/after build graph or affected-target count.
- Build-graph cleanup is a legitimate and encouraged practice — but only when the benefit is stated and traceable.
- If structural change is proposed primarily for aesthetic reasons ("cleaner layout", "smaller files"), defer or batch it separately from functional work (see `constitution/AI_RULES.md` §3.1).

## When This Fails / Failure Modes
- Benchmarks do not represent reality.
- Measurements are noisy/non-deterministic.
- The team treats performance as a late-stage emergency only.
- Structural changes are justified with unmeasured build-speed claims.
- "Cleanup" PRs accumulate structural churn without any demonstrable benefit.

## Related Documents
- `constitution/AI_RULES.md` §3.1 (Incremental Structural Hygiene)
- `architecture/rag/INFORMATION_HIDING.md` (Extraction Discipline)
- `ci/ARCHITECTURE_GATES.md` Gate A5
