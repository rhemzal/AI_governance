# Harbor scenario backlog (maintainer-only)

Plan: `tasks.md`  
AEP: `aep.md`  
Host: kit upstream; Harbor 0.25.0 + Docker (see `specs/005-harbor-docker-qualification/progress.md`)  
Scope: **not** Tier A/B/C adoption; see ADR-0018.

## Objective

Close gaps between Experiment A controls (C1–C4), paid `cursor-cli` qualification,
and deterministic CI. Harbor remains under `research/experiments/harbor/`.

## Backlog (priority)

| ID | Item | Harbor / CI | Status |
| --- | --- | --- | --- |
| H1 | C3 `cp -aL` copy task (+ B1 citation) | Harbor tasks + grader | **Done** (006) |
| H2 | C4 CHANGELOG-only task (+ B1 `loaded-overlay.md`) | Harbor tasks + grader | **Done** (006) |
| H3 | Extend oracle/nop/cursor expect matrices to 8 tasks | `expect-*.json`, jobs | **Done** (006) |
| H4 | Grader unit tests for C3/C4 | `ci/gate_tests/test_harbor_graders.py` | **Done** (006) |
| H5 | Paid `cursor-cli` matrix (3×8) on qualified host | `job.cursor.yaml` + ledger | **Queued** (maintainer run; not CI-required) |
| H6 | Optional `workflow_dispatch` governance-scenarios workflow | `.github/workflows/` | **Deferred** (after H5) |
| H7 | Fresh-context review automation (Experiment B) | Subagent/session harness | **Out of Harbor scope** |
| H8 | Native Cursor Stop / B7 resume | Tier C observation | **Out of Harbor scope** |
| H9 | `ci/select_overlay_rows.py` helper | Deterministic CI optional | **Deferred** |

B0 vs B1 for C1/C2 already uses `-b1` suffix tasks; no separate backlog item.

## Limits (unchanged)

- Final filesystem does not prove refusal-before-diff timing.
- B1 citation text is not measured context load.
- Result gate trusts native `result.json` on maintainer hosts.

## Evidence

Implementation and qualification notes: `progress.md`.
