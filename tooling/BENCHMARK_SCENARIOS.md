# Benchmark Scenarios (AI-Assisted Engineering)

## Purpose
These scenarios are designed to evaluate AI assistance with measurable outcomes. They also serve as **recommended Phase 1 starter tasks** for `usage/AI_PRODUCTIVITY_CALIBRATION.md` — record each run in `notes/local/ai-productivity/ledger.md`.

## Scenario B1: Boundary-Safe Feature Add
- Add a small feature without breaking architecture boundaries.
- Pass criteria: tests pass; no forbidden dependencies; minimal diff.
- **task_class:** `feature_local`
- **Ledger focus:** `T_ai_active`, `ai_iterations`, `T_verify`, `T_lead`, `human_rescue`

## Scenario B2: Interface Automation-First
- Add/modify an interface flow so it runs headlessly.
- Pass criteria: non-interactive mode exists; deterministic output; CI job added.
- **task_class:** `boundary`
- **Ledger focus:** `T_verify`, `T_review`, `verify_failures`, `scope_expansion`

## Scenario B3: Robustness Fix
- Fix an error-handling gap.
- Pass criteria: explicit error model; tests cover failure mode.
- **task_class:** `fix_local`
- **Ledger focus:** `ai_iterations`, `T_fixups`, `verify_failures`

## Scenario B4: Docs + ADR Consistency
- Make an architecture-impacting change.
- Pass criteria: ADR created/updated; docs updated; no duplication.
- **task_class:** `cross_cutting`
- **Ledger focus:** `T_docs`, `T_review`, `T_lead`, `aep_required`

## Related Documents
- `tooling/AI_TOOL_OPTIMIZATION.md`
- `usage/AI_PRODUCTIVITY_CALIBRATION.md`
- `usage/templates/AI_PRODUCTIVITY_LEDGER.template.md`
- `adr/ADR_TEMPLATE.md`
- `ci/ARCHITECTURE_GATES.md`
