# Reproduction — 2026-11-03

Phase 1 of systematic debugging, before the checker existed.

## Steps

```bash
mkdir -p research/benchmark_trials
python3 -m unittest ci.gate_tests.test_open_claim_limits.OpenClaimLimits.test_b5_through_b8_have_no_recorded_trial -v
rm -rf research/benchmark_trials
```

## Output

```text
FAIL: test_b5_through_b8_have_no_recorded_trial
AssertionError: True is not false
File "ci/gate_tests/test_open_claim_limits.py", line 37
    self.assertFalse((ROOT / "research/benchmark_trials").exists())
```

The assertions on scenario labels, "Trial result", and "observed outcome" had already passed. The directory was removed after the run.

## Recent change

`git log -1 -- ci/gate_tests/test_open_claim_limits.py` was `7a1f3bf` (claim cards). The test was written to freeze the open gap.

## Hypothesis

The root cause is the permanent `assertFalse(directory.exists())`, not the scenario text. Smallest confirmation was the run above: one new empty directory, one failed assertion.

## Red, then green

After the new test was written and the module was not yet created:

```text
FileNotFoundError: ci/benchmark_trials.py
ERROR in test_historical_absence_allows_later_trial_files
```

The following run of that test exited 0. That green run is not the final claim until the review fix and the full gate suite are recorded in `progress.md`.
