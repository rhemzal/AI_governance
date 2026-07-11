# Quick Guide / Cookbook (Use This Kit Immediately)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Practical Recommendations (As of 2025-12-28)
This is the fastest path to get value from this repository.

## 0) What You’re Trying to Achieve
- Prevent architecture drift during AI-assisted changes.
- Keep tests and documentation aligned with behavior.
- Make decisions explicit (ADRs) so the AI stops guessing.

## 1) 10-Minute Adoption (Any Repo)
1. Import a bundle from `kit-manifest.yml` (start with `minimal` or `standard`; add `architecture` / `research` as needed).
2. Link imported paths from your repo’s main README (so developers find them).
3. Decide how strict you want to be:
   - day-to-day: use the daily enforcement prompt
   - high-risk changes: require full enforcement + compliance report

## 2) Copy-Paste Prompts (Recipes)

### Recipe A — Daily (90% of work)
Paste this at the top of your prompt:

- `constitution/AI_ENFORCEMENT_DAILY.md`

Then ask:
- “List the files you will change and why. Keep the diff minimal.”
- “Add tests in the correct layer. If unclear, propose options.”

### Recipe B — High-Risk Change (Boundaries / Contracts)
Paste this at the top of your prompt:

- `constitution/AI_ENFORCEMENT.md`

Then require:
- a compliance report
- ADR-first workflow (decision before code)

### Recipe C — Behavior Change With Docs
Add:
- “Include the `### DOC DELTA` block in your output (see `usage/HOW_TO_USE_WITH_COPILOT.md`).”

### Recipe D — Adoption Assessment (Existing Repo; Kit Imported)
Use this when the kit is already present in the repo and you want an AI to recommend what to adopt (and in what order) without blindly copying everything.

**Scope:** Use `usage/PROACTIVE_TRIGGER_MAP.md` to narrow discovery — if only `minimal` is imported, do not audit the full kit tree; assess what is present and what to add next per `usage/ADOPTION_BUNDLES.md`.

Paste this prompt:

```
Load `constitution/AI_RULES.md` and `usage/PROACTIVE_TRIGGER_MAP.md`.
This task is assessment-only: do not change code/docs; do not propose diffs unless I ask.

Context:
- This is an existing repository adopting the AI_governance kit.
- The kit is already available in this repo (folders like `constitution/`, `usage/`, `adr/`).
- Identify which bundles appear imported (minimal only vs standard vs more) before scoping assessment.

Assess the current repo state and recommend an adoption order:
1) **Findability**: where are the governance docs, ADRs, CI definitions, and notes (`notes/`)?
2) **Architecture boundaries**: what appears to be core vs integration boundary today? Where is boundary drift risk highest?
3) **Tests**: what is the current test posture? Are tests deterministic/headless? Where are the biggest gaps?
4) **Docs drift**: which docs likely drift from behavior? Are there duplicated sources of truth?
5) **CI readiness**: which gates can be automated immediately (high-signal) vs which require prerequisites?

Output:
- A short assessment (bullets).
- ADOPTION BUNDLE TRIAGE (if expansion needed): 1 baseline + max 1 optional per usage/ADOPTION_BUNDLES.md.
- A staged adoption recommendation in order (L0 → L3), with prerequisites for each stage:
  - L0: doc hygiene (fast, deterministic)
  - L1: deterministic tests
  - L2: boundary integrity
  - L3: risk signals (coverage/flakiness budget/ADR-required checks)
- What to defer (and why).
- List any missing information you could not infer (max 3 questions).
```

### Recipe E — Adoption Assessment (Existing Repo; Kit Not Yet Imported / URL Reference)
Use this when the kit is not yet imported and you only have a Git URL reference. The goal is to decide how to import first, then run Recipe D.

Paste this prompt:

```
This task is assessment-only: do not change code/docs.

Context:
- This is an existing repository considering adoption of the AI_governance kit at: <PASTE_GIT_URL_HERE>
- Assume the kit is not yet imported unless you see it in the repo.

1) Recommend an import approach (Copy vs Submodule vs Fork) based on practical constraints (team workflow, desired update cadence, willingness to customize).
2) Read `kit-manifest.yml` and `usage/ADOPTION_BUNDLES.md` — run bundle triage: 1 baseline (`minimal` or `standard`) + max 1 optional (`architecture` or `research`). Do NOT recommend `full` for a trial without explicit governance-baseline justification.
3) Output ADOPTION BUNDLE TRIAGE block (see usage/ADOPTION_BUNDLES.md).
4) After import, instruct me to run Recipe D to produce a staged adoption plan.

Output:
- Recommended import approach + why.
- ADOPTION BUNDLE TRIAGE (baseline, optional, deferred, full justified yes/no).
- Next steps checklist (human-doable).
```

### Recipe F — Architecture Decision Precheck (Before Style / ADR)
Use before picking hexagonal vs layered vs event-driven vs hybrid, or before architecture-impacting implementation.

1. Paste the prompt from `architecture/ARCHITECTURE_DECISION_PROMPT.md` (step A precheck, then step B RAG triage).
2. Require `ARCHITECTURE DECISION PRECHECK` and `ARCHITECTURE RAG TRIAGE` output blocks.
3. If `ADR required: yes`, stop and use `adr/ADR_TEMPLATE.md` before code changes — do not load `architecture/rag/` beyond the triaged notes.

### Recipe G — Governance Audit (Kit or Imported Repo)
Use quarterly, before a release tag, or after `[Import bundle change]` / governance-impacting edits.

Paste this prompt (or use AI-Assisted Audit Prompt in `usage/AUDIT_PLAYBOOK.md`):

```
Role: Strict governance reviewer.
Load `usage/AUDIT_PLAYBOOK.md`.

Step 0 — Scope triage (mandatory before Steps 1–5):
- Pick scope: post_import | prefix | release | quarterly
- If post_import: after kit import. If prefix: single path change. If release/quarterly: full audit.
- Load only the mandatory input subset for that scope (see Audit scope triage table).

Goal: Find contradictions, duplication, unenforceable rules, missing theory support (within scope).

Constraints:
- Propose minimal diffs; prefer consolidating into existing docs.
- Use the Findings Format from the playbook (ID, Severity, Category, Evidence, Impact, Fix proposal, Verification).
- Meet minimum findings for scope (5 for post_import/prefix; 10 incl. 3 high for release/quarterly).
- Drift scenarios: 1 for scoped; 3 for release/quarterly.

Deliverables:
- Update or create `usage/AUDIT_REPORT.md`
- Update `usage/FIX_PLAN.md` (top fixes ordered by severity)
```

Complete the **Doc Hygiene Checklist** in `DEVELOPMENT.md` as part of Step 1 evidence.

### Recipe H — Debugging (Triage First)
Use when troubleshooting, performance investigation, or test diagnosis — before the assistant jumps to a fix.

**Default (unclear cause or first fix failed):** paste **Prompt 7** from `usage/DECISION_PROMPTS_DEBUGGING.md`, then **Prompt 6** if the scientific path applies.

**Known domain:** use domain prompts **2–5** (playback, MCP, flakes, minimal repro) from the same file.

**Explicit strategy comparison** (operator wants pros/cons among options): use **Prompt 1** only when cause is already proven, or after Prompt 7 narrowed candidates.

```
Load usage/DEBUGGING_EFFECTIVENESS_CATALOG.md (Scientific method triage section only)
and usage/DEBUGGING_ACCELERATION_PLAYBOOK.md.

Before changing code:
1. Risk preflight: LOW or HIGH.
2. Run Prompt 7 (method triage) — max 3 pattern IDs; do not dump the full catalog.
3. If scientific path: Prompt 6 (falsification) before any product fix.
4. Recommend one path with smallest useful verification scope.
5. Include assumptions, risks, verification steps, and PR evidence output.

Issue:
<PASTE SYMPTOM OR FAILURE>
```

When cause is unclear or the first fix failed, use **Prompt 7** (triage) then **Prompt 6** (hypothesis falsification) — not another blind implementation guess or catalog-wide pattern listing.

## 3) When ADR-First is Mandatory
Use ADR-first when you:
- change architecture boundaries/dependency rules
- change public contracts (APIs, event schemas, CLI interface)
- change system-of-record assumptions (state vs event)
- introduce a new adapter or new interface mode (automation/headless)

Start with:
- `adr/ADR_TEMPLATE.md`

## 4) Minimal PR Rules (Even Without CI)
- Keep PRs small (one intent).
- Require `### DOC DELTA` for behavior changes.
- Require ADRs for architecture-impacting changes.
- Treat failing tests as a hard stop.

## 5) CI On-Ramp (Add Later)
When ready, implement these gates in your CI tool:
- `ci/ARCHITECTURE_GATES.md`
- `ci/TEST_GATES.md`
- `ci/DOC_GATES.md`
- `ci/INTERFACE_GATES.md` (if you have interfaces)

## 6) “Where Do I Start Reading?”
1. `constitution/AI_RULES.md`
2. `constitution/AI_ENFORCEMENT_DAILY.md`
3. `usage/HOW_TO_USE_WITH_COPILOT.md`
4. `usage/HOW_TO_USE_WITH_VSCODE.md`
5. `adr/ADR_TEMPLATE.md`

## Related Documents
- `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md`
- `usage/DEBUGGING_ACCELERATION_PLAYBOOK.md`
- `usage/DECISION_PROMPTS_DEBUGGING.md`
- `usage/AUDIT_PLAYBOOK.md`
- `architecture/ARCHITECTURE_DECISION_PROMPT.md`
- `README.md`
- `usage/HOW_TO_IMPORT.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `usage/HOW_TO_USE_WITH_VSCODE.md`
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md` and `constitution/AI_ENFORCEMENT_DAILY.md`
- `adr/ADR_TEMPLATE.md`
