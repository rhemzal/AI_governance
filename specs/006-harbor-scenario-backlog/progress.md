# Harbor scenario backlog — progress

See `spec.md` and `aep.md`. Maintainer-only; not adoption.

## Task log

| Task | Status | Notes |
| --- | --- | --- |
| 1 Spec + AEP | complete | `aep.md` validates with `ci/validate_aep.py` |
| 2 C3 tasks | complete | `c3-opt-in-copy`, `c3-opt-in-copy-b1`; symlink via Dockerfile `RUN ln -snf` |
| 3 C4 tasks | complete | `c4-changelog-scope`, `c4-changelog-scope-b1` |
| 4 Matrices + docs | complete | `expect-oracle.json`, `expect-candidate.json`, harbor README; jobs renamed `c1-c4-*` |
| 5 Unit tests | complete | 21 tests OK (`test_harbor_graders`, `test_harbor_results`) |
| 6 Docker oracle/nop | complete | 2026-11-05; see below |
| 7 cursor-cli matrix | queued | Paid; `job.cursor.yaml` + `expect-candidate.json` (3×8) |

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

| Job | Trials | Mean reward | Gate vs `expect-oracle.json` |
| --- | --- | --- | --- |
| `c1-c4-oracle` | 8/8 | 1.000 | ACCEPT |
| `c1-c4-nop` | 8/8 | 0.000 | REJECT (exit 1; expected) |

Tasks: all eight `ai-governance/c1-*` … `c4-changelog-scope-b1`.

## Unit verification

```bash
python3 -m unittest ci.gate_tests.test_harbor_graders ci.gate_tests.test_harbor_results -q
```

Result: **OK** (21 tests).

## Backlog remainder (not in this change)

- **H5:** paid cursor-cli matrix on maintainer host
- **H6:** optional `workflow_dispatch` workflow
- **H7–H8:** fresh-context review, native Stop (out of Harbor)
- **H9:** `ci/select_overlay_rows.py` optional helper
