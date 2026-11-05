# Maintainer workflow — governance scenarios (Harbor)

_Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance)._

Runs on **`workflow_dispatch` only**. Required kit CI does **not** invoke Harbor on
every pull request. Paid `cursor-cli` trials need repository secret `CURSOR_API_KEY`.

## Inputs

| Input | Values | Notes |
| --- | --- | --- |
| `scenario` | `oracle-nop` (default), `cursor-matrix` | See workflow file |

## Local equivalent

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

Cursor matrix: see [`../harbor/README.md`](../harbor/README.md) and
`specs/006-harbor-scenario-backlog/progress.md` (H5).

## Experiment B (H7)

Manual fresh-context review trials use [`../fresh-context-review/README.md`](../fresh-context-review/README.md).
This workflow does not start reviewer agents.

## Native Stop (H8)

See [`../cursor-stop/README.md`](../cursor-stop/README.md). Harbor does not observe IDE Stop.
