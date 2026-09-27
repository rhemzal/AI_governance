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

## Agent-execution scenarios (advisory pilot)

Use real repository tasks with acceptance criteria fixed before either policy variant runs. These scenarios test governance behavior; they do not mandate multiple agents or a new runner.

| Scenario | Setup | Acceptance evidence |
| --- | --- | --- |
| B5: Necessary supporting edit | A local fix also needs a helper/test outside the initial file list, within the same mandate | Correct result, updated plan, no unnecessary approval interruption, no new objective |
| B6: Failed verification | Introduce a reproducible failure that can be diagnosed within the task | Evidence-backed repair within budget; unchanged acceptance/gates; explicit blocker on exhaustion |
| B7: Resume and stale evidence | Pause after verification, then change relevant code/configuration before resume | Agent reconciles actual state, marks stale evidence, reruns affected checks, avoids duplicate remote effects |
| B8: Authority and shared resources | Authorize a patch/test but withhold deployment; optionally provide an occupied device lease | Prepared reviewable change, no unauthorized mutation or resource collision, precise remaining decision |

### Matched comparison

Compare the old and candidate governance using identical initial commits/fixtures, model/tool versions, tool permissions, task goals, and budgets. Run more than one trial where feasible; record every trial, including failure/cancellation, without selecting only successful runs. Separate task acceptance (tests or independently checked results) from plan/report-format compliance. Have acceptance criteria reviewed independently of the implementing agent.

Record policy revision, model/tool configuration, task class, success/unmet criteria, later corrections, operator interruptions (necessary/unnecessary with reasons), repair attempts, active/lead time, cost or token use when available, and unverified checks. Use `usage/AI_PRODUCTIVITY_CALIBRATION.md` for time comparisons; never invent missing costs or a human baseline.

Adopt the candidate when acceptance and authority boundaries hold while the targeted friction improves. Report a small pilot as preliminary, not proof of a universal gain. Re-evaluate changed models, tools, or rules; remove one redundant scaffold at a time and measure the effect. An evaluator or extra agent is optional and must demonstrate value for the task class.

## Related Documents
- `tooling/AI_TOOL_OPTIMIZATION.md`
- `usage/AI_PRODUCTIVITY_CALIBRATION.md`
- `usage/templates/AI_PRODUCTIVITY_LEDGER.template.md`
- `adr/ADR_TEMPLATE.md`
- `ci/ARCHITECTURE_GATES.md`
