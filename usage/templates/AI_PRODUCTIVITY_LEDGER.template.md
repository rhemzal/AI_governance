# AI Productivity Ledger (Local — Do Not Commit)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). Copy to `notes/local/ai-productivity/ledger.md` — that path is gitignored._

## Setup

1. Create folder: `notes/local/ai-productivity/`
2. Copy this file to `notes/local/ai-productivity/ledger.md`
3. Append one entry per closed task (issue, PR, or session)
4. Aggregate manually for Phase 2 — see `usage/AI_PRODUCTIVITY_CALIBRATION.md`

## Single entry template (copy below the line)

---

### Entry: `<task_id>` — `<YYYY-MM-DD>`

**Classification**
- task_class: `fix_local` | `feature_local` | `test_only` | `docs_only` | `boundary` | `cross_cutting` | `debug_triage`
- risk: LOW | HIGH
- files_touched:
- aep_required: yes | no
- scope_expansion: yes | no

**Time buckets (minutes)**
- T_scope:
- T_ai_active:
- T_operator:
- T_verify:
- T_review:
- T_docs:
- T_fixups:
- T_lead:

**AI-specific**
- ai_iterations:
- human_rescue: yes | no
- verify_failures:

**Phase 3+ (when planning with ranges)**
- estimate_at_plan: `[low, high]` min
- estimate_error_ratio:

**Human counterfactual (optional)**
- T_human_manual:
- human_source: measured | calibrated_ratio | unknown

**Notes**
- (one line: what made this task faster or slower)

---

## Manual aggregation table (Phase 2+)

Fill after you have enough entries. Minimum **N ≥ 10** per class before using for planning.

| task_class | N | median T_lead | p25 | p75 | median T_ai_active | median ai_iterations | human_vs_ai_ratio | human_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fix_local | | | | | | | | |
| feature_local | | | | | | | | |
| test_only | | | | | | | | |
| docs_only | | | | | | | | |
| boundary | | | | | | | | |
| cross_cutting | | | | | | | | |
| debug_triage | | | | | | | | |

**human_vs_ai_ratio** = `median(T_human_manual) / median(T_lead)` only when `human_source` is `measured` or `calibrated_ratio` with N ≥ 5.

## Related Documents

- `usage/AI_PRODUCTIVITY_CALIBRATION.md`
- `governance/AI_CALIBRATION_SUMMARY.template.md`
