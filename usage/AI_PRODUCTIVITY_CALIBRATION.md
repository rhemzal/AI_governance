# AI Productivity Calibration (Advisory)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This guide defines a **measurement-driven** planning model for AI-assisted development. It is **advisory** unless your `governance/LOCAL_OVERLAY.md` promotes specific phases or metrics to required.

**Non-goals:**
- No universal “AI is N× faster” multiplier.
- No calendar time estimates during cold start (Phase 0–1).
- No LLM-generated human-team duration guesses (`human_source` must never be `llm_guess`).

## Relationship to other documents

| Document | Role |
| --- | --- |
| `usage/HOW_TO_USE_WITH_COPILOT.md` | Time buckets (`T_scope`…`T_fixups`) — summary + link here |
| `tooling/AI_TOOL_OPTIMIZATION.md` | Tool/model trials; priors → measurements |
| `tooling/BENCHMARK_SCENARIOS.md` | Recommended Phase 1 starter tasks (B1–B4) |
| `usage/GOVERNANCE_SCORECARD.md` | Optional AI productivity KPIs |
| `usage/templates/AI_PRODUCTIVITY_LEDGER.template.md` | Local ledger copy-paste template |
| `governance/AI_CALIBRATION_SUMMARY.template.md` | Optional committed team summary |

## Calibration phases

```text
Phase 0 (Cold start) → Phase 1 (Collect) → Phase 2 (Calibrate) → Phase 3 (Plan with ranges)
```

### Phase 0 — Cold start

**When:** New project, new repo adoption, or fewer than ~10 closed tasks in the ledger.

**Rules:**
- Do **not** state calendar estimates for human teams or AI assistants (“2 days”, “1 week”, “~4 hours”).
- Plan with: `task_class`, explicit file paths, iteration budget (**count**, not minutes), verify command, risk (LOW/HIGH).
- AEP remains compatible — add optional `Planning mode: COLD_START` (no ETA fields).

**Exit criteria:** Operator declares Phase 1, or first ledger entry is recorded.

### Phase 1 — Collect

**When:** Actively building a local dataset.

**Rules:**
- After each closed task (issue/PR/session), append one **ledger entry** to `notes/local/ai-productivity/ledger.md` (gitignored; copy template from `usage/templates/AI_PRODUCTIVITY_LEDGER.template.md`).
- Do **not** refine estimates from sparse data — collect facts only.
- Recommended minimum before Phase 2: **10–20** closed tasks total; **≥10** per `task_class` before class-specific ranges.

**Exit criteria:** Minimum sample reached; operator declares Phase 2.

### Phase 2 — Calibrate

**When:** Enough ledger entries exist to compute medians per `task_class`.

**Rules:**
- Aggregate locally (manually): median, p25, p75 for `T_lead`, `T_ai_active`, `ai_iterations`.
- Optionally publish anonymized aggregates to `governance/AI_CALIBRATION_SUMMARY.md` (copy from `governance/AI_CALIBRATION_SUMMARY.template.md`).
- Commit **aggregates only** — never raw ledger rows.

**Exit criteria:** Summary published or operator declares Phase 3 for a given `task_class`.

### Phase 3 — Plan with ranges

**When:** A `task_class` has **N ≥ 10** ledger entries.

**Rules:**
- State estimates as **ranges** derived from your data plus an explicit uncertainty band.
- For “how long would humans take?” use only:
  1. **Measured** manual baseline (`human_source: measured`), or
  2. **Calibrated ratio** from your data (`human_source: calibrated_ratio`).
- If insufficient data: answer `human_source: unknown` — do not invent a human duration.

## Task class taxonomy (starter set)

| Class | Example |
| --- | --- |
| `fix_local` | Single-module bugfix, no public contract change |
| `feature_local` | Small feature in one area |
| `test_only` | Tests, flakes, harness fixes |
| `docs_only` | DOC DELTA / docs without code |
| `boundary` | Adapter, public contract, interface change |
| `cross_cutting` | 3+ modules or architecture-impacting work |
| `debug_triage` | Method triage (e.g. Prompt 7) → fix |

Add project-local classes in `governance/LOCAL_OVERLAY.md` if needed.

## Ledger entry (per closed task)

### Required fields (minimum viable entry)

| Field | Type | Notes |
| --- | --- | --- |
| `task_id` | string | Issue, PR, or session label |
| `date` | ISO date | Close date |
| `task_class` | enum | From taxonomy above |
| `risk` | LOW \| HIGH | Per risk preflight |
| `T_ai_active` | minutes | Wall-clock while AI worked (tools, generation) |
| `T_lead` | minutes | Start → merge (or session end if no PR) |
| `ai_iterations` | integer | Prompt → diff cycles |

### Recommended fields

| Field | Type | Notes |
| --- | --- | --- |
| `files_touched` | integer | From PR or session |
| `aep_required` | yes/no | Per AEP rules |
| `T_scope` | minutes | Scoping, context reading |
| `T_operator` | minutes | Human wait: review prompts, decisions |
| `T_verify` | minutes | Tests, CI, local verify |
| `T_review` | minutes | PR review |
| `T_docs` | minutes | DOC DELTA / docs |
| `T_fixups` | minutes | Follow-up work within 7 days |
| `human_rescue` | yes/no | Human finished after AI stalled |
| `verify_failures` | integer | AVR loop count |
| `scope_expansion` | yes/no | Scope grew beyond initial plan |

### Phase 3+ fields

| Field | Type | Notes |
| --- | --- | --- |
| `estimate_at_plan` | range | What the plan predicted (minutes) |
| `estimate_error_ratio` | float | `actual_T_lead / estimate_mid` — for self-calibration only |

### Human vs AI counterfactual (optional, Phase 2+)

| Field | Type | Notes |
| --- | --- | --- |
| `T_human_manual` | minutes | Comparable pre-AI task, if it exists |
| `human_source` | enum | `measured` \| `calibrated_ratio` \| `unknown` — **never** `llm_guess` |

Full copy-paste block: `usage/templates/AI_PRODUCTIVITY_LEDGER.template.md`.

## Aggregation rules

1. Per `task_class`, require **N ≥ 10** before class-specific planning ranges.
2. Compute: `median(T_lead)`, `median(T_ai_active)`, `median(ai_iterations)`, p25/p75 where useful.
3. **Planning range** for a new task in class C:
   - If N ≥ 10: use `[p25, p75]` of `T_lead`, or `[median × 0.7, median × 1.5]` when percentiles are noisy.
   - If N < 10: stay in Phase 0–1 for that class (scope-only plan).
4. Track `estimate_error_ratio`; if systematically **> 1.3**, widen the band for that class.
5. **Human vs AI ratio** (report only when justified):
   - If `T_human_manual` with `human_source: measured` exists for **≥ 5** tasks in class C:  
     `ratio = median(T_human_manual) / median(T_lead)`.
   - Else: report `insufficient data` — not an LLM guess.

## Anti-patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Calendar ETA in Phase 0–1 | Trained on human-team text; not calibrated to your repo |
| Global “10× faster” multiplier | Ignores governance, tests, rework (`T_fixups`) |
| Fake precision after 5 tasks | High variance; use wide bands or stay scope-only |
| `human_source: llm_guess` | Unfalsifiable; breaks human vs AI comparisons |
| Skipping ledger in Phase 1 | No data → permanent cold start |

## Optional PR / issue block

Adopters may add this voluntary block to issues or PR descriptions:

```markdown
### AI productivity (optional)
- task_class:
- ai_iterations:
- T_ai_active (min):
- human_rescue: yes/no
```

Raw ledger rows belong in `notes/local/ai-productivity/ledger.md`, not in PR bodies, unless your team policy says otherwise.

## Related Documents

- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `usage/AEP_VALIDATION.md`
- `usage/QUICKGUIDE.md` (Recipe I)
- `usage/GOVERNANCE_SCORECARD.md`
- `tooling/AI_TOOL_OPTIMIZATION.md`
- `tooling/BENCHMARK_SCENARIOS.md`
- `governance/LOCAL_OVERLAY_TEMPLATE.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`
