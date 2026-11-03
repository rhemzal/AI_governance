# SDD ledger — plan: specs/001-benchmark-trial-records/tasks.md

Pre-flight: Task 2 consumes `tree_errors` and must not modify `ci/benchmark_trials.py`. No interface conflict.

Ruling: no commit — the operator did not authorize a commit. Upstream commit steps are not followed.
Ruling: no worktree — the operator assigned this checkout.
Ruling: the kept ledger is this file. `.superpowers/sdd/tasks/` is scratch from `task-start` and is gitignored.
Ruling: `task-start` on this plan printed base `158b6931817db531e9c0967430efd4b1ea11a2ea`, which is HEAD. There is no Task 1 commit.
Ruling: documentation and registry wording do not require a red-green test. The checker did. The first run failed with `FileNotFoundError` for `ci/benchmark_trials.py`. The rerun below passed.
Ruling: the plan file is `specs/001-benchmark-trial-records/tasks.md`, not `docs/superpowers/plans/`.

Task 1: complete (STALE — `tooling/BENCHMARK_SCENARIOS.md` hash differs from this pass; rerun recorded below. No new commit; worktree on 158b693, tests: python3 -m unittest ci.gate_tests.test_open_claim_limits.OpenClaimLimits.test_historical_absence_allows_later_trial_files -v → OK)

Verified file hashes at that pass:
- `ci/benchmark_trials.py` sha256 `e54aa03bd98f9dbcbce75f53ad49a94b56a6c438c4eca330f20c657ec9d54abe`
- `ci/gate_tests/test_open_claim_limits.py` sha256 `6823492c50d5ed7b5c653c1cba20731258f9004b3d38de66f97250a8f371aa98`
- `tooling/BENCHMARK_SCENARIOS.md` sha256 `d07d7700ca08fc8d066c49be12bbe3e930455532fa04baf4369fddcd61d0a9fb`
- `ci/claim_cards.json` sha256 `85fd28b266b061e3f33cc159d5a9b0c2a7a1ef1d0fc0257a60c31a067a4df024`

Task 1 stale rerun: three recorded hashes still match (`ci/benchmark_trials.py` `e54aa03bd98f9dbcbce75f53ad49a94b56a6c438c4eca330f20c657ec9d54abe`, `ci/gate_tests/test_open_claim_limits.py` `6823492c50d5ed7b5c653c1cba20731258f9004b3d38de66f97250a8f371aa98`, `ci/claim_cards.json` `85fd28b266b061e3f33cc159d5a9b0c2a7a1ef1d0fc0257a60c31a067a4df024`). `tooling/BENCHMARK_SCENARIOS.md` differs: now `bf1510154453375e37efb4fe484fe53d34af738c6150985676de78d933ec3a78` (recorded `d07d7700ca08fc8d066c49be12bbe3e930455532fa04baf4369fddcd61d0a9fb`). File not reverted. Historical sentence in that file: 1. Command: `python3 -m unittest ci.gate_tests.test_open_claim_limits.OpenClaimLimits.test_historical_absence_allows_later_trial_files -v` → OK (exit 0; Ran 1 test in 0.001s).

Do not redo Task 1 when those hashes still match. If a hash differs, the pass above is stale: rerun the same command and record the new hash. Do not revert the file just to restore the old hash.

Task 2: complete (no new commit; tests: python3 -m unittest ci.gate_tests.test_open_claim_limits.OpenClaimLimits.test_historical_absence_allows_later_trial_files -v → OK, exit 0, Ran 1 test in 0.001s)

Final review: fresh reviewer, read-only, no session history. It found two issues and did not edit the tree.

Final: fixed — `outcome: cancelled` was rejected (`outcome must be pass, fail, or blocked`) while the suite was green because the assertion was missing. Added the plan's `cancelled` and `blocked` assertions. RED: `AssertionError` on `cancelled`. GREEN after `OUTCOMES` included `cancelled`: the same unittest → OK.

Final: fixed — the test never called `tree_errors` on a path that did not exist. Added `directory / "absent"`. That assertion passed on the existing branch. Replacing `return []` for a missing directory with `return ["missing"]` made the same test FAIL on that assertion. Restoring the branch made it OK. The mutation is not in the tree.

Final: Ruling: nested Markdown, bullet field lines, `readme.md` versus `README.md`, non-Markdown names, quoted scenario tokens, `canceled`, extra prose, field order, and a non-UTF-8 decode error stay outside this checker. The spec's tokens are exact and files are the top-level Markdown records named in Task 2. A lower-case `readme.md` is a trial file and will fail if it is prose. Cost if wrong: an author who uses that name sees a field error instead of an ignored note.

Final review clean after the one fix pass. No second review. No commit. No pull request.
