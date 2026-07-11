# How to Use With GitHub Copilot (Practical)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Practical Recommendations (As of 2025-12-28)
This section is intentionally practical and time-stamped.
GitHub Copilot features and UI can change; treat this as a workflow pattern, not a promise of specific product behavior.

## Test Execution (Canonical Path)
**DO NOT assume global pytest or global test runners.**

Each repository should use a repo-local virtual environment and/or make/docker workflow.

### Preferred Test Invocation Order
1. **Make targets** (if available): `make test`, `make test-unit`, `make test-integration`
2. **Repo-local venv** (Python projects): `.venv/bin/python -m pytest` or `.venv/bin/pytest`
3. **Docker fallback** (if provided): `docker compose run --rm test` or similar

### Why This Matters
- Global test runners break reproducibility (version skew, missing dependencies).
- Repo-local venvs ensure consistency across team members and CI.
- Make targets abstract the test command and provide a stable interface.

### When You Don't Know the Test Command
1. Check for a `Makefile` with test targets: `grep -E "^test" Makefile`
2. Check for a `.venv` directory and use `.venv/bin/python -m pytest`
3. Check for `docker-compose.yml` or `compose.yml` with test services
4. Check `README.md` or `CONTRIBUTING.md` for test instructions
5. If none exist, create a virtual environment: `python3 -m venv .venv && .venv/bin/pip install -e .[dev]` (or similar)

### For AI Assistants
- Always discover the test execution path before assuming pytest is globally available.
- Prefer `make test` if it exists; otherwise use `.venv/bin/python -m pytest`.
- Never install or recommend installing test dependencies globally.

## Repo-Local Output Paths (Temp, Artifacts, Caches)
- AI MUST prefer repo-local paths for temporary artifacts, generated outputs, caches, logs, and intermediate files.
- AI MUST NOT write to external paths (e.g. `/tmp`, home directory, parent directories) unless the operator explicitly requests it.
- If a tool or command defaults to an external temp path, redirect it to a repo-local equivalent when feasible.
- If redirection is not feasible, STOP and request confirmation before proceeding.
- Recommended repo-local scratch directories: `.tmp/`, `tmp/`, `.artifacts/`, `.cache/` (follow repo convention).
- Ephemeral outputs should be gitignored if they are not canonical artifacts.

## Agent Instruction Files (AGENTS.md, Copilot Instructions)

Agent instruction files must not become large duplicated playbooks.
They should contain only minimal, task-critical instructions and references to deeper governance documents.

Recommended pattern:
- **Source of truth**: `constitution/`, `ci/`, `adr/`, `architecture/`
- **Projections** (keep short): `AGENTS.md`, `.github/copilot-instructions.md`

Each projection should include:
- how to build, test, and verify changes
- links to `constitution/AI_RULES.md` and the appropriate enforcement doc
- one or two project-specific constraints not covered elsewhere

Do not paste full governance documents, architecture theory, or enterprise process into files loaded on every AI task.

See `research/PLAYBOOK_ADAPTATION_GUIDE.md` (Section 1.1 and Agent Instructions) for adaptation rationale.

## Debugging Strategy Comparisons (Advisory)
For troubleshooting, performance work, or test diagnosis, ask the assistant to pick methods **before** implementing fixes. Do not load the full debugging catalog unless triage says so (pattern budget: max **3** IDs — see `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md` anti-overload rules).

Recommended flow:
1. **Unclear cause or first fix failed:** `usage/DECISION_PROMPTS_DEBUGGING.md` **Prompt 7** (method triage) → **Prompt 6** (falsification) if scientific path applies.
2. **Known domain** (playback, MCP, flakes, heavy repro): domain prompt **2–5** from the same file.
3. **Explicit strategy comparison** among options (operator request): **Prompt 1** — only after Prompt 7 when cause was unclear, or when cause is already proven.
4. Follow LOW vs HIGH paths in `usage/DEBUGGING_ACCELERATION_PLAYBOOK.md`.

This is advisory guidance — normative test policy remains in `ci/TEST_GATES.md`; high-risk stops remain in `constitution/AI_ENFORCEMENT.md`.

## Method triage (non-debugging)

When scope or method is unclear, apply **method triage** before loading large document corpora. Terms: `architecture/TERMINOLOGY_GLOSSARY.md` (method triage, corpus budget).

| Area | Document | Corpus budget |
| --- | --- | --- |
| Architecture / RAG | `architecture/ARCHITECTURE_DECISION_PROMPT.md`, `architecture/README.md` | Max 2 RAG notes + 1 cross-cutting; matrix columns for selected styles only |
| Security findings | `usage/SECURITY_MINIMUM_ADOPTION.md` | Max 3 actions per iteration (fix / waiver / defer) |
| Governance audit | `usage/AUDIT_PLAYBOOK.md` | Pick scope first; scoped minimum findings (not always 10) |
| Kit adoption | `usage/ADOPTION_BUNDLES.md` | 1 baseline bundle + max 1 optional |
| AEP discovery | `usage/AEP_VALIDATION.md` | Max 5 consulted paths (LOW-risk); narrow via `usage/PROACTIVE_TRIGGER_MAP.md` |

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

## Risk Preflight Prompt (Copy/Paste)
Use this at the start of a task to force a consistent LOW vs HIGH risk classification before edits.

"Do a risk preflight before changes:
- List exact files you will touch
- Confirm whether any boundary contract/interface, adapter/integration, architecture decision, security behavior, CI/gates, or canonical governance docs are affected
Return: `Risk: LOW|HIGH` + 1–2 sentence justification.
If LOW: proceed to execution.
If HIGH/unclear: STOP and ask for confirmation."

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
- `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md`
- `usage/DEBUGGING_ACCELERATION_PLAYBOOK.md`
- `usage/DECISION_PROMPTS_DEBUGGING.md`
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

Goal: plan realistically for “automation-first coding” by modeling **iteration loops** and **measured lead time**, not human-team calendar guesses.

**Canonical calibration guide:** `usage/AI_PRODUCTIVITY_CALIBRATION.md` (phases, ledger, human vs AI methodology).

### Phase 0 rule (cold start)

During Phase 0–1, do **not** state calendar estimates for human teams or AI assistants (“2 days”, “~4 hours”). Plan with `task_class`, file paths, iteration budget (**count**), verify command, and risk (LOW/HIGH). See Recipe I in `usage/QUICKGUIDE.md`.

### Time buckets (per change)

Track in minutes where possible:
- `T_scope`: clarifying scope + constraints
- `T_ai_active`: wall-clock while AI worked (tools, generation); ledger field in calibration guide
- `T_ai_cycles` / `ai_iterations`: AI iterations (prompt → diff → adjust) — prefer **count** in Phase 0
- `T_operator`: human wait (review prompts, decisions)
- `T_verify` / `T_tests`: tests, CI, local verify
- `T_review`: PR review + governance checks
- `T_docs`: docs updates + consolidation (Doc Delta)
- `T_fixups`: post-merge defects / follow-up PRs (within 7 days)
- `T_lead`: start → merge

### Baseline vs AI comparison

Maintain two baselines (see calibration guide for `human_source` rules):
- **Manual baseline**: historical median for similar tasks (pre-AI or “AI off”).
- **AI-governed baseline**: tasks done with this kit (AI on + enforcement).

Compare: lead time, rework rate, defect escape rate, churn outside scope.

### Planning heuristic (no fake precision)

After Phase 2 calibration (N ≥ 10 per `task_class`), use data-derived **ranges** — not LLM calendar guesses.

$$T_{total} \approx T_{scope} + T_{ai\_active} + T_{operator} + T_{verify} + T_{review} + T_{docs} + T_{fixups}$$

Increase uncertainty for architecture-impacting work or weak/flaky tests.

### Practical template (Phase 0 — scope only)

**AI Scope Plan** (no calendar ETA)
- Planning mode: COLD_START
- task_class:
- Files / steps (explicit paths):
- AI iteration budget (count, not minutes):
- Verify command:
- Risk: LOW | HIGH

**Success signals**
- tests deterministic: yes/no
- Doc Delta completed: yes/no
- no boundary violations: yes/no

After task closure, append a ledger entry — `usage/templates/AI_PRODUCTIVITY_LEDGER.template.md`.

