# Native Cursor Stop / resume observation (H8 scaffold)

_Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance)._

Harbor **`cursor-cli`** batch runs do **not** establish:

- IDE Stop hook dispatch
- Approval UX
- Resumed-session behavior (Experiment A **B7** / benchmark **B7**)

## What to observe (Tier C)

On a capable host with projected Cursor hooks:

1. Trigger Stop during an in-flight agent task with a defined follow-up message.
2. Record whether the session resumes with reconciled state vs stale evidence.
3. Compare with [`usage/AI_ENGINEERING_METHODS.md`](../../../usage/AI_ENGINEERING_METHODS.md) resume guidance.

Do not claim Harbor trial success as proof of Stop behavior.

## Related documents

- Benchmark B7: [`tooling/BENCHMARK_SCENARIOS.md`](../../../tooling/BENCHMARK_SCENARIOS.md)
- Automated scenarios limits: [`research/EXTERNAL_PROJECT_EVALUATIONS.md`](../../EXTERNAL_PROJECT_EVALUATIONS.md#automated-control-scenarios-2026-11-05)
- specs/006 H8 (out of Harbor scope)

Optional experimental adapter work may live on a separate maintainer branch; nothing here
is required for kit import.
