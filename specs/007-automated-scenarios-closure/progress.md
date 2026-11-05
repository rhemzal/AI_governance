# Automated scenarios closure — progress

See `spec.md` and `aep.md`. Closes PR #58 post-qualification gaps; not adoption.

## Task log

| Task | Status | Notes |
| --- | --- | --- |
| 1 AEP | complete | `aep.md` validates with `ci/validate_aep.py` |
| 2 Research DOC DELTA | complete | `EXTERNAL_PROJECT_EVALUATIONS.md` eight-task + H5 table |
| 3 CHANGELOG + BENCHMARK | complete | Unreleased bullets; qualified command table |
| 4 H9 overlay helper | complete | `ci/select_overlay_rows.py` + unit tests |
| 5 H6 workflow | complete | `.github/workflows/governance-scenarios.yml` |
| 6 H7/H8 scaffolds | complete | `fresh-context-review/`, `cursor-stop/` README |
| 7 ADR + specs/006 | complete | ADR-0018 amendment; H6/H9 done in spec |

## Verification (2026-11-05)

```bash
python3 ci/validate_aep.py specs/007-automated-scenarios-closure/aep.md
python3 -m unittest \
  ci.gate_tests.test_select_overlay_rows \
  ci.gate_tests.test_harbor_graders \
  ci.gate_tests.test_harbor_results \
  ci.gate_tests.test_merge_harbor_jobs -q
```

Result: **OK** (26 tests).

## Workflow smoke

Maintainer runs **Actions → governance-scenarios → Run workflow** with `oracle-nop`.
Expect oracle gate ACCEPT and nop gate REJECT. `cursor-matrix` requires repository
secret `CURSOR_API_KEY` and spends model quota.

## Out of scope (documented only)

- Full Experiment B agent automation (H7)
- Native IDE Stop/resume proof (H8)
- Promptfoo pivot unless host boundary changes
