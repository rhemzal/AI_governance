# AI Calibration Summary (Optional — Team Aggregate)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). Copy to `governance/AI_CALIBRATION_SUMMARY.md` in your repo when ready to share aggregates with the team._

**Policy:** Commit **aggregates only**. Raw ledger entries stay in `notes/local/ai-productivity/ledger.md` (gitignored).

## Declaration

- **Period:** YYYY-MM-DD → YYYY-MM-DD
- **Calibration phase:** Phase 0 | Phase 1 | Phase 2 | Phase 3
- **Total closed tasks (ledger):**
- **Last updated:** YYYY-MM-DD
- **Owner:**

## Aggregates by task class

Minimum **N ≥ 10** per class before using ranges in Phase 3 planning.

| task_class | N | median T_lead (min) | p25 | p75 | median T_ai_active | median ai_iterations | human_rescue rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fix_local | | | | | | | |
| feature_local | | | | | | | |
| test_only | | | | | | | |
| docs_only | | | | | | | |
| boundary | | | | | | | |
| cross_cutting | | | | | | | |
| debug_triage | | | | | | | |

## Human vs AI (only when data supports it)

| task_class | human_vs_ai_ratio | human_source | N (human) | Notes |
| --- | --- | --- | --- | --- |
| | | measured \| calibrated_ratio \| unknown | | |

**human_vs_ai_ratio** = `median(T_human_manual) / median(T_lead)`.

Report a ratio only when `human_source` is `measured` or `calibrated_ratio` and N ≥ 5 for that class. Otherwise state `insufficient data`.

## Planning bands (Phase 3)

Classes with N ≥ 10 — suggested planning range for `T_lead`:

| task_class | planning_range (min) | estimate_error_ratio trend | action |
| --- | --- | --- | --- |
| | `[low, high]` | | widen band / OK |

If `estimate_error_ratio` is systematically **> 1.3**, widen the band for that class.

## Observations / next actions

- Top slowdown bucket (T_verify, T_fixups, …):
- Classes still in Phase 0–1 (N < 10):
- Next review date:

## Related Documents

- `usage/AI_PRODUCTIVITY_CALIBRATION.md`
- `usage/templates/AI_PRODUCTIVITY_LEDGER.template.md`
- `governance/LOCAL_OVERLAY_TEMPLATE.md`
