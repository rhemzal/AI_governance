# Harbor Docker qualification (maintainer-only)

Not part of Tier A/B/C adoption. See [ADR-0018](../../adr/ADR_0018_Optional_Harbor_Result_Gate.md) and
[harbor README](../../research/experiments/harbor/README.md).

## Environment (2026-11-05)

| Component | Version |
|-----------|---------|
| Kit revision | `dde8748` (main at run time) |
| Harbor | 0.25.0 (`/tmp/harbor-venv`, Python 3.13.5) |
| Docker Engine | 26.1.5+dfsg1 |
| `cursor-agent` | 2026.10.22-27dcf5f (present; **not used** — oracle/nop agents only) |
| `HARBOR_TELEMETRY` | 0 |

Commands from repository root after `python3 research/experiments/harbor/build_tasks.py`.

## Oracle job (positive control)

```bash
harbor run --config research/experiments/harbor/job.oracle.yaml
python3 ci/check_harbor_results.py \
  --job jobs/c1-c2-oracle \
  --expected research/experiments/harbor/expect-oracle.json
```

| Metric | Result |
|--------|--------|
| Trials | 4/4 |
| Mean reward | 1.000 |
| Exceptions | 0 |
| Harbor CLI exit | 0 |
| Result gate | `{"outcome": "ACCEPT", "reasons": []}` |
| Wall time | ~2m 24s |

Tasks: `c1-forbidden-import`, `c1-forbidden-import-b1`, `c2-permitted-doc`, `c2-permitted-doc-b1`.

## Nop job (negative control)

```bash
harbor run --config research/experiments/harbor/job.nop.yaml
python3 ci/check_harbor_results.py \
  --job jobs/c1-c2-nop \
  --expected research/experiments/harbor/expect-oracle.json
```

| Metric | Result |
|--------|--------|
| Trials | 4/4 |
| Mean reward | 0.000 |
| Exceptions | 0 |
| Harbor CLI exit | 0 (expected — exit code is not acceptance) |
| Result gate vs oracle expect | **REJECT** (reward/agent mismatch on all trials) |
| Gate exit | 1 |

## Unit regressions (same day)

```bash
python3 -m unittest ci.gate_tests.test_harbor_results ci.gate_tests.test_harbor_graders -q
```

Result: **OK** (17 tests).

## Disposition

- **C1/C2 (+ B1 citation) graders** behave as designed in Docker with separate verifier.
- **Paid `cursor-cli` matrix** (`expect-candidate.json`, 3 attempts) **not run** in this pass.
- Job artifacts under `jobs/` are local maintainer output; not imported by adopters.

## Task log

- Oracle + gate ACCEPT: complete
- Nop + gate REJECT vs oracle expect: complete
- Gate unit tests: complete
