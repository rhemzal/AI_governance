# Benchmark trial records implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. The project entry point is `.cursor/skills/governed-work/SKILL.md`. Do not ask between tasks.

**Goal:** Keep the 2026-11-02 B5–B8 absence recorded and accept only well-formed later trial files.

**Architecture:** One standard-library checker. Tests load it by file path. `README.md` in the trial directory is not a record.

**Tech Stack:** Python 3 standard library, unittest.

**Spec:** `specs/001-benchmark-trial-records/spec.md`

## Global Constraints

- Historical sentence, exact: `As of 2026-11-02, scenarios B5 through B8 had no recorded trial.`
- `scenario` is exactly `B5`, `B6`, `B7`, or `B8`.
- `revision` is one token with no whitespace.
- `outcome` is exactly `pass`, `fail`, `cancelled`, or `blocked`.
- Do not commit, push, merge, or publish.
- Do not add a second claim card.
- Do not fabricate a B5–B8 trial result.

## Review Focus

- `outcome: cancelled` must be accepted, same as `pass`. A checker that lists only some of the four words rejects a real record.
- `scenario: B50` must be rejected. A prefix of `B5` is not scenario B5.
- `README.md` must not be read as a trial, including when it contains none of the fields.
- A duplicate `scenario` line must be an error even if one of the values is valid.
- After Task 1 is marked complete, a later session must not rewrite the checker or the historical sentence.

---

### Task 1: Checker and historical sentence

**Files:**
- Create: `ci/benchmark_trials.py`
- Modify: `ci/gate_tests/test_open_claim_limits.py`
- Modify: `ci/claim_cards.json`
- Modify: `tooling/BENCHMARK_SCENARIOS.md`
- Test: `ci/gate_tests/test_open_claim_limits.py`

**Interfaces:**
- Consumes: nothing from an earlier task
- Produces: `trial_errors(text) -> list[str]`, `tree_errors(directory) -> list[str]`, `HISTORICAL_ABSENCE`

- [x] **Step 1: Write the failing test**

The test `test_historical_absence_allows_later_trial_files` loads `ci/benchmark_trials.py` and checks the historical sentence, a good `outcome: pass` record, missing and whitespace revisions, an empty outcome, `outcome: nope`, `scenario: B50`, a duplicate scenario, a missing directory, and a README-only directory.

Also include this assertion in that test:

```python
cancelled = "scenario: B7\nrevision: abcdef0\noutcome: cancelled\n"
self.assertEqual(trials.trial_errors(cancelled), [])
blocked = "scenario: B8\nrevision: abcdef0\noutcome: blocked\n"
self.assertEqual(trials.trial_errors(blocked), [])
```

- [x] **Step 2: Run the test and see it fail**

Run: `python3 -m unittest ci.gate_tests.test_open_claim_limits.OpenClaimLimits.test_historical_absence_allows_later_trial_files -v`

Expected: FAIL or ERROR before `ci/benchmark_trials.py` exists.

- [x] **Step 3: Implement the checker**

`trial_errors` and `tree_errors` as produced above. `tree_errors` returns an empty list when the directory is missing and skips `README.md`.

- [x] **Step 4: Run the test and see it pass**

Run: `python3 -m unittest ci.gate_tests.test_open_claim_limits.OpenClaimLimits.test_historical_absence_allows_later_trial_files -v`

Expected: OK

- [x] **Step 5: Do not commit**

Record the command and the file hashes in `progress.md`.

### Task 2: Directory that is not a trial

**Files:**
- Create: `research/benchmark_trials/README.md`
- Modify: `specs/001-benchmark-trial-records/progress.md`

**Interfaces:**
- Consumes: `tree_errors` from Task 1. Do not change `ci/benchmark_trials.py` or the test file.
- Produces: a README-only trial directory in the repository

- [x] **Step 1: Add the README**

```markdown
# Benchmark trial records

This directory is optional. It did not exist in the 2026-11-02 absence baseline. Adding it is not a completed trial.

`README.md` is not a trial record. Any other `.md` file here is a trial record. The checker is `ci/benchmark_trials.py`. A file that passes the checker is not evidence that a matched comparison ran.

The dated absence sentence stays in `tooling/BENCHMARK_SCENARIOS.md`.
```

- [x] **Step 2: Reconcile Task 1 before editing**

Read `progress.md`. If a recorded hash differs from the current file, mark that verification stale and rerun Task 1's unittest. Do not revert the working tree to restore an old hash. Do not rewrite the historical sentence or the checker when the rerun passes.

- [x] **Step 3: Run the suite**

Run: `python3 -m unittest ci.gate_tests.test_open_claim_limits.OpenClaimLimits.test_historical_absence_allows_later_trial_files -v`

Expected: OK, and the historical sentence still occurs once.

- [x] **Step 4: Do not commit**

Append the Task 2 result to `progress.md`.
