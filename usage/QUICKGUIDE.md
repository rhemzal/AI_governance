# Quick Guide / Cookbook (Use This Kit Immediately)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Practical Recommendations (As of 2025-12-28)
This is the fastest path to get value from this repository.

## 0) What You’re Trying to Achieve
- Prevent architecture drift during AI-assisted changes.
- Keep tests and documentation aligned with behavior.
- Make decisions explicit (ADRs) so the AI stops guessing.

## 1) 10-Minute Adoption (Any Repo)
1. Copy these folders into your repo:
   - `constitution/`
   - `adr/`
   - `usage/`
   - `notes/` (recommended: committed vs local parking-lot notes)
   - (optional) `ci/`, `interface/`, `architecture/`
2. Link them from your repo’s main README (so developers find them).
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

Paste this prompt:

```
Load `constitution/AI_RULES.md`.
This task is assessment-only: do not change code/docs; do not propose diffs unless I ask.

Context:
- This is an existing repository adopting the AI_governance kit.
- The kit is already available in this repo (folders like `constitution/`, `usage/`, `adr/`).

Assess the current repo state and recommend an adoption order:
1) **Findability**: where are the governance docs, ADRs, CI definitions, and notes (`notes/`)?
2) **Architecture boundaries**: what appears to be core vs integration boundary today? Where is boundary drift risk highest?
3) **Tests**: what is the current test posture? Are tests deterministic/headless? Where are the biggest gaps?
4) **Docs drift**: which docs likely drift from behavior? Are there duplicated sources of truth?
5) **CI readiness**: which gates can be automated immediately (high-signal) vs which require prerequisites?

Output:
- A short assessment (bullets).
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
2) Recommend the minimal set of folders to import first (focus on high-signal, low-friction value).
3) After import, instruct me to run Recipe D to produce a staged adoption plan.

Output:
- Recommended import approach + why.
- Minimal import set + why.
- Next steps checklist (human-doable).
```

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
- `README.md`
- `usage/HOW_TO_IMPORT.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `usage/HOW_TO_USE_WITH_VSCODE.md`
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md` and `constitution/AI_ENFORCEMENT_DAILY.md`
- `adr/ADR_TEMPLATE.md`
