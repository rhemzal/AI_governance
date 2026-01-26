# How to Use With GitHub Copilot (Practical)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Practical Recommendations (As of 2025-12-28)
This section is intentionally practical and time-stamped.
GitHub Copilot features and UI can change; treat this as a workflow pattern, not a promise of specific product behavior.

## Daily Work
Use:
- `constitution/AI_ENFORCEMENT_DAILY.md`

## High-Risk Changes
Use:
- `constitution/AI_ENFORCEMENT.md`

Trigger “high-risk” mode when:
- changing boundaries or architecture
- adding a new adapter
- changing interface behavior (automation-first)
- changing error model

## Expected Outputs From the AI
- explicit scope
- constraints honored
- compliance report (when required)

## Documentation Is as Important as Code
Use these rules to keep documentation coherent and prevent “shattering”:
- Prefer updating an existing document (new section) over creating a new file.
- If you add a new doc file, add it to `README.md` and include `Related Documents`.
- For architecture-impacting changes: write/update an ADR first, then implement.

### Reproducible Documentation Generation
If Copilot/AI generates documentation content or summaries:
- record where the truth comes from (code, tests, ADRs, usage docs)
- keep the generation repeatable (documented procedure)
- do not hand-edit generated outputs without updating the source

## ADR-First Workflow (When It Matters)
Use ADR-first when the change:
- alters architecture boundaries, dependency rules, or integration strategy
- introduces a new interface mode (automation/headless)
- changes the error model or system-of-record assumptions

Minimal sequence:
1. Write/update an ADR (decision + trade-offs + enforcement).
2. Implement code/tests.
3. Update docs.

## “Doc Delta” (PR-Ready Template)
When a PR changes behavior, paste this block into the PR description.

### DOC DELTA
- Source of truth:
  - Code:
  - Tests:
  - ADRs:
- Docs updated (paths):
- Docs removed/merged (paths):
- Generated docs?
  - yes/no
  - Generator/source:
  - Regeneration process (command or procedure):
- Review checklist:
  - Single source of truth preserved: yes/no
  - No overlapping docs introduced: yes/no
  - Links valid: yes/no

## Related Documents
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT_DAILY.md`
- `constitution/AI_ENFORCEMENT.md`
- `interface/INTERFACE_RULES_PROPOSAL.md` and `interface/INTERFACE_CI_GATES.md`
- `ci/ARCHITECTURE_GATES.md`, `ci/TEST_GATES.md`, `ci/INTERFACE_GATES.md`, `ci/DOC_GATES.md`

## Copilot Spaces (What to Put There)
If your team uses Copilot Spaces (or any shared “project context” feature), include only **stable, high-signal** artifacts.
Recommended content:
- `README.md` (as the hub)
- `constitution/AI_RULES.md`, `constitution/AI_ENFORCEMENT.md`, `constitution/AI_ENFORCEMENT_DAILY.md`
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` and `architecture/TERMINOLOGY_GLOSSARY.md`
- `adr/ADR_TEMPLATE.md` and the latest accepted ADRs
- `interface/INTERFACE_RULES_PROPOSAL.md` + `interface/INTERFACE_CI_GATES.md` (if you build any interfaces)

Avoid uploading:
- long, frequently changing notes
- duplicated docs that compete with repo sources of truth

## Recommended GitHub + Copilot “Toolchain” (As of 2025-12-28)
This is a practical recommendation set for teams using GitHub + Copilot.
Adopt the pieces that match your maturity; avoid adding tooling without enforcement.

### Use These (High-Leverage)
- **Copilot Chat / agent workflow**: for scoped changes with explicit constraints and compliance reporting.
- **Copilot inline suggestions**: for mechanical edits after decisions are made.
- **Copilot Spaces (or shared context)**: only for stable, high-signal governance docs (see above).
- **Pull Requests as the control point**:
  - require the `### DOC DELTA` block for behavior changes
  - require ADRs for architecture-impacting changes
- **Branch protection + required checks** (once CI exists):
  - require architecture/test/doc/interface gates (even if implemented as lightweight scripts initially)
  - disallow direct pushes to main
- **CODEOWNERS (optional but useful)**:
  - assign owners for `constitution/`, `architecture/`, `interface/`, `ci/`
  - force review by the right people when governance or boundaries change

### Do This Without Heavy Infrastructure
Even before full CI, you can enforce quality by workflow:
- keep PRs small
- use the weekly governance review
- treat failing local tests as a hard stop
- use ADR-first for architecture-impacting work

### When NOT To Use (Or When to Reduce AI Autonomy)
Reduce or gate AI autonomy when:
- changing public contracts (APIs, event schemas, CLI interface)
- making cross-cutting refactors across many modules
- incident response / production hotfixes under time pressure
- security-sensitive changes that require careful threat modeling

In these cases, use AI for:
- option exploration
- drafting ADR alternatives
- generating test scaffolding
But keep the final decision-making and integration more human-led/serial (this is a decision/review bottleneck, not “manual governance work” outside PRs).

## “No Infrastructure” Workflow (Still Safe)
When you cannot rely on CI yet (early repo / local work), keep the governance enforceable locally:
1. Always include `### DOC DELTA` for behavior-changing work.
2. Keep diffs small (one intent per PR/branch).
3. Require tests locally for non-trivial changes (even if CI is not wired).
4. For architecture-impacting work: write the ADR first, then code.
5. If you add docs, consolidate instead of creating new files (anti-fragmentation).

## Team Workflow for AI-Heavy Development
The goal is maximum parallelism without losing coherence.

### What to Parallelize (Works Well With AI)
- Drafting ADRs (multiple alternatives in parallel) — final selection is serial.
- Writing tests for an already decided behavior.
- Integration boundary (adapter/interface) work once boundary contracts are fixed.
- Documentation updates that are mechanical and traceable (Doc Delta driven).
- RAG note improvements (small, scoped updates with “when this fails”).

### What to Keep Serial (Decision Bottlenecks)
- Changing architecture boundaries and dependency rules.
- Selecting system-of-record assumptions (state vs event).
- Public contract changes (APIs, event schemas, CLI interface).
- Cross-cutting changes that touch many modules.

### Recommended Division of Labor
- One person (or a small rotating role) acts as “governance integrator”:
  - ensures ADR-first where required
  - checks boundary integrity
  - enforces Doc Delta and consolidation

### PR Review Pattern (AI-Friendly)
- Require:
  - clear scope statement
  - `## COMPLIANCE REPORT` (for high-risk changes)
  - `### DOC DELTA` (for behavior changes)
- Prefer multiple small PRs over one large PR.

## Team Roles & Cadence (Lightweight)
Keep this lightweight to avoid process overhead, but make it explicit.

Recommended roles (can rotate weekly):
- **Governance integrator**: enforces ADR-first, boundary integrity, Doc Delta, consolidation.
- **Release shepherd**: keeps PRs small, unblocks merges, watches risk accumulation.
- **Test owner** (optional): guards determinism and flakiness budget.

Cadence:
- **Per PR**: scope statement + (when required) compliance + Doc Delta.
- **Weekly (30–45 min)**: governance review
  - ADR backlog hygiene (merge/supersede)
  - doc consolidation sweep (delete duplicates)
  - flakiness / regression review

## Time Planning & Cost Model for AI-Heavy Development (As of 2025-12-28)
Goal: plan realistically for “automation-first coding” by modeling **human time** and **iteration loops**, not only typing speed.

Important note: This kit does not assume a universal global multiplier.
Productivity gains vary wildly by domain, codebase health, and enforcement strictness.
Use this as a **measurement-driven model**.

### What to Measure (Per Change)
Track these buckets (minutes/hours):
- `T_scope`: clarifying scope + constraints
- `T_ai_cycles`: AI iterations (prompt → diff → adjust)
- `T_review`: PR review + governance checks
- `T_tests`: writing/fixing tests + flakiness handling
- `T_docs`: docs updates + consolidation (Doc Delta)
- `T_fixups`: post-merge defects / follow-up PRs

### Baseline vs AI Comparison
Maintain two baselines:
- **Manual baseline**: historical median for similar tasks (pre-AI or “AI off”).
- **AI-governed baseline**: tasks done with this kit (AI on + enforcement).

Compare using:
- lead time (start → merged)
- rework rate (follow-up PRs per feature)
- defect escape rate (bugs after merge)
- churn (lines changed outside the intended scope)

### Planning Heuristic (No Fake Precision)
For estimates, use a range:
$$T_{total} = T_{scope} + T_{ai\_cycles} + T_{review} + T_{tests} + T_{docs} + T_{fixups}$$

Then:
- If the task is **architecture-impacting**, increase the uncertainty band (more review/ADR time).
- If tests are weak/flaky, increase `T_tests` and `T_fixups` (AI tends to amplify this cost).

### What to Parallelize vs Serialize (Time-Model View)
Parallelize when it reduces `T_total` without increasing `T_fixups`:
- tests/doc updates after the behavior is decided
- integration boundary work after boundary contracts are frozen

Serialize when parallelism increases rework:
- changing public contracts
- changing boundaries and invariants

### Practical Template (Paste Into an Issue/Plan)
**AI Time Plan**
- Scope/constraints (T_scope):
- AI iteration budget (T_ai_cycles):
- Tests budget (T_tests):
- Docs/consolidation budget (T_docs):
- Review/governance budget (T_review):
- Risk buffer (T_fixups):

**Success signals**
- tests deterministic: yes/no
- Doc Delta completed: yes/no
- no boundary violations: yes/no

