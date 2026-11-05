# Fresh-context review (Experiment B scaffold)

_Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance)._

Harbor automates **filesystem control scenarios** (C1–C4). **Experiment B** compares
author-style review (B0) with a **fresh-context reviewer** (B1) on a fixed packet.
This directory does **not** run agents in CI.

## Spec and acceptance

- Trial spec: [`specs/004-fresh-context-review-trial/spec.md`](../../../specs/004-fresh-context-review-trial/spec.md)
- Progress ledger: [`specs/004-fresh-context-review-trial/progress.md`](../../../specs/004-fresh-context-review-trial/progress.md)

## Manual packet (B1)

Include only:

- Target diff or file list under review
- Acceptance criteria and required sources
- Explicit exclusion: prior chat, author verdict, COMPLIANCE blocks

Exclude author narrative and “already merged” claims.

## Recording outcomes

Append results to `specs/004-fresh-context-review-trial/progress.md`. Optional trial
Markdown under `research/benchmark_trials/` must follow `ci/benchmark_trials.py` schema
(scenario `B5`–`B8` is a different benchmark family).

## Automation boundary

A future native subagent or session harness belongs in a separate maintainer experiment.
Do not conflate B1 screening with Harbor reward `1` on C1–C4 tasks.

## Related

- Assessment table: [`research/EXTERNAL_PROJECT_EVALUATIONS.md`](../../EXTERNAL_PROJECT_EVALUATIONS.md#automated-control-scenarios-2026-11-05)
- specs/006 H7 row (scaffold only)
