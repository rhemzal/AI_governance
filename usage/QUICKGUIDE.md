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
