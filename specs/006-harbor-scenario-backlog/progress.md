# Harbor scenario backlog — progress

See `spec.md` and `aep.md`. Maintainer-only; not adoption.

## Task log

| Task                 | Status   | Notes                                                                                |
| -------------------- | -------- | ------------------------------------------------------------------------------------ |
| 1 Spec + AEP         | complete | `aep.md` validates with `ci/validate_aep.py`                                         |
| 2 C3 tasks           | complete | `c3-opt-in-copy`, `c3-opt-in-copy-b1`; symlink via Dockerfile `RUN ln -snf`          |
| 3 C4 tasks           | complete | `c4-changelog-scope`, `c4-changelog-scope-b1`                                        |
| 4 Matrices + docs    | complete | `expect-oracle.json`, `expect-candidate.json`, harbor README; jobs renamed `c1-c4-*` |
| 5 Unit tests         | complete | 22 tests OK (`test_harbor_graders`, `test_harbor_results`, `test_merge_harbor_jobs`) |
| 6 Docker oracle/nop  | complete | 2026-11-05; see below                                                                |
| 7 cursor-cli matrix  | complete | 2026-11-05; merged gate ACCEPT — see H5 below                                        |
| 7a cursor mini pilot | complete | 2026-11-05; ACCEPT on retry — see H5a below                                          |

## H5 full matrix (8×3, composer-2.5)

Job `jobs/c1-c4-cursor/`, wall **1h 25m 43s**, summed trial agent cost **~$0.30**.

```bash
set -a && source ~/.config/cursor/harbor.env && set +a
export HARBOR_TELEMETRY=0
harbor run --config research/experiments/harbor/job.cursor.yaml
python3 ci/check_harbor_results.py \
  --job jobs/c1-c4-cursor \
  --expected research/experiments/harbor/expect-candidate.json
```

| Metric               | Result                                                 |
| -------------------- | ------------------------------------------------------ |
| Trials finished      | 24/24                                                  |
| Mean reward (Harbor) | 0.875                                                  |
| Reward 1.0           | 21                                                     |
| Reward 0.0           | 2                                                      |
| Exceptions           | 1 (`NetworkConnectionError` on `cursor-agent` install) |
| Result gate          | **REJECT**                                             |
| Pass@2 (Harbor)      | 1.000                                                  |

Gate: `REWARD` on `c3-opt-in-copy-b1__R5qzs8K`, `c4-changelog-scope__cQrxKX5`; `EXCEPTION` + `REWARD` on `c4-changelog-scope-b1__HTCNxyT`; `VERSION: agent versions differ` (exception trial → `unknown`).

Failures:

- **c3-opt-in-copy-b1** (1/3): wrong paths (`opt-in/copy/pin/CONTENT.txt` vs `opt-in/copy/CONTENT.txt`).
- **c4-changelog-scope** (1/3): `HASH: CHANGELOG.md`.
- **c4-changelog-scope-b1** (1/3): transient `downloads.cursor.com` during agent install.

Artifacts: `jobs/c1-c4-cursor/` (local, gitignored).

### H5 retry (3 failed scenarios, 1 attempt each)

```bash
harbor run --config research/experiments/harbor/job.cursor-retry.yaml
python3 ci/check_harbor_results.py \
  --job jobs/c1-c4-cursor-retry \
  --expected research/experiments/harbor/expect-candidate-retry.json
```

| Metric        | Result                               |
| ------------- | ------------------------------------ |
| Trials        | 3/3                                  |
| Mean reward   | **1.000**                            |
| Gate          | **ACCEPT**                           |
| Wall time     | ~11m 9s                              |
| Reported cost | **~$0.04** (sum of trial `cost_usd`) |

Artifacts: `jobs/c1-c4-cursor-retry/`.

### H5 merged matrix (gate on 3×8)

Manifest: `research/experiments/harbor/merge-c1-c4-cursor.json`. Tool:
`research/experiments/harbor/merge_harbor_jobs.py`.

| Metric                          | Result                                       |
| ------------------------------- | -------------------------------------------- |
| Output job                      | `jobs/c1-c4-cursor-merged/`                  |
| Trials                          | 24 (21 from full run + 3 retry replacements) |
| Gate vs `expect-candidate.json` | **ACCEPT**                                   |
| Provenance                      | `merge-provenance.json` in output job        |

## Mini pilot (H5a)

Credential: `~/.config/cursor/harbor.env` (not committed). Host `cursor-agent` in job: **2026.11.05-86047df** (Harbor-installed); host CLI **2026.10.22-27dcf5f**.

### Run 2026-11-05 retry (instruction fence fix)

After `build_tasks.py` fenced the C2 paragraph (meta lines no longer pasted into
`/app`), job `c1-c4-cursor-mini-2`:

| Metric        | Result                               |
| ------------- | ------------------------------------ |
| Reward        | **1.0**                              |
| Gate          | **ACCEPT**                           |
| Wall time     | ~3m 46s                              |
| Reported cost | **$0.0087118** (28 852 in / 506 out) |

Artifacts: `jobs/c1-c4-cursor-mini-2/`.

### Run 2026-11-05 (first attempt; superseded)

```bash
set -a && source ~/.config/cursor/harbor.env && set +a
export HARBOR_TELEMETRY=0
harbor run --config research/experiments/harbor/job.cursor-mini.yaml
python3 ci/check_harbor_results.py \
  --job jobs/c1-c4-cursor-mini \
  --expected research/experiments/harbor/expect-candidate-mini.json
```

| Metric        | Result                                                  |
| ------------- | ------------------------------------------------------- |
| Task          | `ai-governance/c2-permitted-doc`                        |
| Model         | `composer-2.5`                                          |
| Reward        | **0.0**                                                 |
| Exceptions    | 0                                                       |
| Gate          | **REJECT** (`REWARD: c2-permitted-doc__qYM8yLp`)        |
| Wall time     | ~4m 9s                                                  |
| Reported cost | **$0.0105873** (38 608 in / 457 out; 32 864 cache read) |
| Verifier      | `HASH: usage/ADOPTION_SCOPE_AND_HOSTS.md`               |

**Diagnosis (first attempt):** Composer appended the required paragraph but also copied trailing **instruction meta-lines** into the usage file. Fixed by fenced ` ```text ` block + “Task rules (for you only)” in `build_tasks.py` (C2 and C4).

Artifacts: `jobs/c1-c4-cursor-mini/` (local, gitignored).

### Commands (reference)

## Docker qualification (2026-11-05)

Environment: Harbor 0.25.0 (`/tmp/harbor-venv`), Docker 26.1.5, `HARBOR_TELEMETRY=0`.

```bash
python3 research/experiments/harbor/build_tasks.py
harbor run --config research/experiments/harbor/job.oracle.yaml
python3 ci/check_harbor_results.py \
  --job jobs/c1-c4-oracle \
  --expected research/experiments/harbor/expect-oracle.json
harbor run --config research/experiments/harbor/job.nop.yaml
python3 ci/check_harbor_results.py \
  --job jobs/c1-c4-nop \
  --expected research/experiments/harbor/expect-oracle.json
```

| Job            | Trials | Mean reward | Gate vs `expect-oracle.json` |
| -------------- | ------ | ----------- | ---------------------------- |
| `c1-c4-oracle` | 8/8    | 1.000       | ACCEPT                       |
| `c1-c4-nop`    | 8/8    | 0.000       | REJECT (exit 1; expected)    |

Tasks: all eight `ai-governance/c1-*` … `c4-changelog-scope-b1`.

## Unit verification

```bash
python3 -m unittest \
  ci.gate_tests.test_harbor_graders \
  ci.gate_tests.test_harbor_results \
  ci.gate_tests.test_merge_harbor_jobs -q
```

Result: **OK** (22 tests).

## Backlog remainder (not in this change)

- **H5:** paid cursor-cli matrix — done 2026-11-05 (raw job REJECT; merged gate ACCEPT; see above)
- **H6:** optional `workflow_dispatch` workflow
- **H7–H8:** fresh-context review, native Stop (out of Harbor)
- **H9:** `ci/select_overlay_rows.py` optional helper
