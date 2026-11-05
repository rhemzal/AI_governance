# Tasks — Harbor scenario backlog (006)

Execute in order; record outcomes in `progress.md`.

## Task 1 — Spec + AEP

**Objective:** Publish backlog and READY AEP for H1–H4.

**Verification:** `python3 ci/validate_aep.py specs/006-harbor-scenario-backlog/aep.md` exits 0.

## Task 2 — C3 Harbor tasks

**Objective:** Add `c3-opt-in-copy` and `c3-opt-in-copy-b1` with fixture symlink, materialized copy, `copy-report.md`.

**Acceptance:** Oracle solution passes grader; nop leaves copy missing; explanation-only `copy-report.md` without copy fails.

## Task 3 — C4 Harbor tasks

**Objective:** Add `c4-changelog-scope` and `c4-changelog-scope-b1` (CHANGELOG-only edit + B1 overlay note).

**Acceptance:** Unchanged CHANGELOG fails; extra files fail; B1 requires exact `loaded-overlay.md`.

## Task 4 — Matrices + docs

**Objective:** Update `expect-oracle.json`, `expect-candidate.json`, `harbor/README.md`, regenerate committed `tasks/` via `build_tasks.py`.

**Verification:** `python3 research/experiments/harbor/build_tasks.py` then builder parity test.

## Task 5 — Unit regressions

**Objective:** Extend `test_harbor_graders.py` for C3/C4; run harbor gate unit tests.

**Verification:**

```bash
python3 -m unittest ci.gate_tests.test_harbor_graders ci.gate_tests.test_harbor_results -q
```

## Task 6 — Docker oracle/nop (maintainer)

**Objective:** Re-run oracle/nop on eight tasks; append ledger in `progress.md`.

**Blocked when:** Docker unavailable in session — record BLOCKED and leave commands in progress file.

## Task 7 — Cursor candidate matrix (maintainer, paid)

**Objective:** `harbor run --config job.cursor.yaml` + `expect-candidate.json`.

**Not part of Task 1–5 merge criteria** — operator-triggered after H1–H4 land.
