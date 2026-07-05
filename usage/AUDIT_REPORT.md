# Audit Report — AI_governance kit

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

Date: 2026-07-05
Scope: Full re-run of `usage/AUDIT_PLAYBOOK.md` (Steps 1–5) + doc hygiene check (link validation, manifest path validation, provenance spot-check).
Prior audit: 2025-12-28 (superseded by this report).

Result summary:
- Scavenger test: **PASS with caveats** (all five core items findable; three require a second hop beyond README)
- Consistency scan: **ISSUE** (bundle contents vs. cross-references in bundled `usage/` docs)
- Enforceability review: **ISSUE** (CI gates remain principles; automated doc hygiene removed; no kit-repo CI workflows)
- Theory validation: **PASS** (scenario → tactics → architecture → enforcement chain intact)
- Red-team drift scenarios: documented below
- Doc hygiene check: **PASS** (no broken relative links in hub docs; all `kit-manifest.yml` explicit paths exist)

---

## Step 1 — Scavenger Test

| Item | Result | Path(s) | Notes |
| --- | --- | --- | --- |
| High-risk boundary/contract change | **Found** | `README.md` → `constitution/AI_ENFORCEMENT.md` | Direct from “Start here (top links)”. |
| ADR template and contents | **Found** | `README.md` → `adr/ADR_TEMPLATE.md` | Template includes Trade-Offs, Sensitivity Points. |
| Hybrid architecture guidance | **Found** (2 hops) | `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` §6a | README links framework, not “hybrid” by keyword. |
| Schema evolution / versioning | **Found** (2 hops) | `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md` | Via `architecture/README.md` or `architecture/rag/README.md`; not in README hub. |
| Non-interactive / timeout expectations | **Found** (2 hops) | `constitution/AI_RULES.md` §6.2, `constitution/AI_ENFORCEMENT.md` §2.1 | Not listed in README hub or agent projections. |
| Adoption bundles (added) | **Found** | `kit-manifest.yml`, `usage/ADOPTION_BUNDLES.md` | In README “Choose your path” and top links. |
| Audit playbook (added) | **Not found** | — | `usage/AUDIT_PLAYBOOK.md` not linked from `README.md`, `QUICKGUIDE.md`, or `GOVERNANCE_SCORECARD.md` hub path. |

---

## Findings

- **ID**: A-01
- **Severity**: High
- **Category**: contradiction
- **Evidence**: `usage/HOW_TO_IMPORT.md` § Governance Versioning: “See `VERSIONING.md`…”; `usage/ADOPTION_BUNDLES.md` Related Documents lists `VERSIONING.md`; `usage/CI_MINIMUM_ADOPTION.md` references `DEVELOPMENT.md`. Manifest resolution shows `VERSIONING.md`, `DEVELOPMENT.md`, `kit-manifest.yml`, `CHANGELOG.md`, and `README.md` are **not** in `minimal`, `standard`, or `full` bundles (`kit-manifest.yml` paths verified programmatically).
- **Impact**: Copy importers get bundled `usage/` docs with broken root-level references; version traceability and doc-hygiene guidance fail silently after import.
- **Fix proposal**: Add a `meta` or `root` path group to `kit-manifest.yml` (at minimum `kit-manifest.yml`, `VERSIONING.md`, `DEVELOPMENT.md`; consider `CHANGELOG.md`) and include it in `standard` and `full` via `extends`/`composes`. Align `usage/HOW_TO_IMPORT.md` Option A with the machine-readable bundle list.
- **Verification**: Resolve all bundle paths after change; grep bundled `usage/` for root `.md` refs and confirm each target is in the importer’s copied set (or rewrite refs as “read from upstream kit repo only”).

- **ID**: A-02
- **Severity**: High
- **Category**: enforceability
- **Evidence**: `CHANGELOG.md` Unreleased: “Removed the Python doctor script…”; `DEVELOPMENT.md`: “AI-assisted review… CI doc-hygiene gate”; repository has no `.github/workflows/` and no `Makefile`. Prior audit A-06 noted CI gates are principles-only; automated hygiene previously cited as passing is no longer available in-repo.
- **Impact**: Doc drift, broken manifest paths, and provenance gaps accumulate without a deterministic local/CI check; “paper compliant” merges remain easy.
- **Fix proposal**: Document a minimal tool-agnostic doc hygiene checklist in `DEVELOPMENT.md` (explicit grep/link steps). Optionally add a reference workflow under `usage/CI_STARTER_WORKFLOWS.md` for downstream repos; kit repo may stay workflow-free if checklist is mandatory in `DEVELOPMENT.md` and `usage/PROACTIVE_TRIGGER_MAP.md`.
- **Verification**: Operator can complete checklist in &lt;15 minutes; checklist covers manifest paths, hub links, provenance on import targets.

- **ID**: A-03
- **Severity**: High
- **Category**: contradiction
- **Evidence**: `CHANGELOG.md`: `## v1.0.0 — 2025-12-31` plus a large `## Unreleased` section with `[Import bundle change]` entries; `kit-manifest.yml`: `version: "0.1"`; `VERSIONING.md`: manifest `version` tracks “manifest schema and bundle contract, not every doc edit.”
- **Impact**: Importers and maintainers cannot tell whether they are on `v1.0.0`, `0.1` manifest schema, or unreleased head; ADR version records become ambiguous.
- **Fix proposal**: Cut a release (tag + changelog section) or add a `## Unreleased` note in `VERSIONING.md` mapping git tag ↔ manifest `version` ↔ adoption contract. Until release, state in `README.md` that `main` may be ahead of latest tag.
- **Verification**: Single table in `VERSIONING.md` answers “what version am I on?” for tag, manifest, and branch head.

- **ID**: A-04
- **Severity**: Medium
- **Category**: findability
- **Evidence**: `usage/AUDIT_PLAYBOOK.md` exists; `usage/GOVERNANCE_SCORECARD.md` links it only under Related Documents; `README.md` “Start here (top links)” omits audit playbook and `usage/FIX_PLAN.md`.
- **Impact**: Kit maintainers and quarterly reviewers miss the canonical audit procedure; governance maintenance becomes ad hoc.
- **Fix proposal**: Add to `README.md` top links: Audit playbook (`usage/AUDIT_PLAYBOOK.md`). Add Recipe in `usage/QUICKGUIDE.md` pointing to playbook + AI-assisted prompt.
- **Verification**: Scavenger item “run a governance audit” resolves from README in &lt;60 seconds.

- **ID**: A-05
- **Severity**: Medium
- **Category**: duplication
- **Evidence**: `usage/AUDIT_PLAYBOOK.md` mandatory inputs list `architecture/rag/README.md` but not `architecture/README.md` (new entry point per `AGENTS.md`, `CHANGELOG.md`, `architecture/README.md`). `usage/HOW_TO_IMPORT.md` Option A lists manual folders that diverge from `kit-manifest.yml` `full` compose (no mention of `kit-manifest.yml` snapshot, `ARCHITECTURE_DECISION_PROMPT.md` path in Option A prose).
- **Impact**: Audits and imports follow stale checklists; new entry point under-reviewed.
- **Fix proposal**: Add `architecture/README.md` to `AUDIT_PLAYBOOK.md` mandatory inputs; replace Option A folder bullet list with “resolve `full` bundle from `kit-manifest.yml`” as single source.
- **Verification**: Playbook inputs match `AGENTS.md` required context; HOW_TO_IMPORT Option A matches manifest `full` resolution.

- **ID**: A-06
- **Severity**: Medium
- **Category**: enforceability
- **Evidence**: `ci/ARCHITECTURE_GATES.md`, `ci/TEST_GATES.md`, `ci/DOC_GATES.md`, `ci/INTERFACE_GATES.md` remain “principles”; `constitution/ADAPTIVE_GOVERNANCE.md` scales enforcement by level but kit repo implements no gates.
- **Impact**: Downstream repos inherit principles without a working reference implementation; enforcement defaults to human review only.
- **Fix proposal**: Downstream action (unchanged): adopt `usage/CI_MINIMUM_ADOPTION.md` progressively. Kit action: add “reference implementation status” subsection to `DEVELOPMENT.md` stating kit repo is intentionally gate-free but documents the checklist contract.
- **Verification**: New importer reads `DEVELOPMENT.md` and understands what they must wire locally.

- **ID**: A-07
- **Severity**: Medium
- **Category**: security
- **Evidence**: `AGENTS.md` and `.github/copilot-instructions.md` are in `minimal` bundle paths but lack Provenance banners (spot-check: first 500 chars); other import targets under `constitution/`, `ci/`, `usage/`, `architecture/` include banners.
- **Impact**: Copy importers lose traceability on the highest-traffic agent entry points; audits cannot confirm kit origin from file headers alone.
- **Fix proposal**: Add one-line provenance footer or header to `AGENTS.md` and `.github/copilot-instructions.md` (match `usage/GOVERNANCE_SCORECARD.md` banner style).
- **Verification**: Provenance grep on `minimal` bundle file list returns 100% coverage.

- **ID**: A-08
- **Severity**: Low
- **Category**: theory
- **Evidence**: `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` requires 2–5 measurable quality attribute scenarios; `architecture/rag/QUALITY_ATTRIBUTES.md` provides template; `adr/ADR_TEMPLATE.md` includes Trade-Offs and Sensitivity Points.
- **Impact**: None identified (positive control).
- **Fix proposal**: None.
- **Verification**: Framework → template → ADR chain intact.

- **ID**: A-09
- **Severity**: Low
- **Category**: contradiction
- **Evidence**: `architecture/ARCHITECTURE_STYLE_MATRIX.md`: “hybridization guidance is a summary… canonical rules in `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`” (§ near Hybrid Architectures pointer).
- **Impact**: None identified (positive control; single canonical owner for hybrid rules).
- **Fix proposal**: None.
- **Verification**: Consistency scan found no competing hybrid rule owners.

- **ID**: A-10
- **Severity**: Low
- **Category**: findability
- **Evidence**: `constitution/AI_RULES.md` §6.2 and `constitution/AI_ENFORCEMENT.md` §2.1 define non-interactive/time-bounded execution; neither appears in `README.md` hub or `AGENTS.md` “Required context”.
- **Impact**: Agents may miss hard gate until they open constitution; automation hang risk in early adoption.
- **Fix proposal**: Add one bullet to `AGENTS.md` Quick rules: “Use non-interactive commands and wall-clock timeouts (`constitution/AI_RULES.md` §6.2).” Mirror in `.github/copilot-instructions.md`.
- **Verification**: Scavenger for timeouts succeeds from agent projection without opening daily enforcement doc.

- **ID**: A-11
- **Severity**: Low
- **Category**: enforceability
- **Evidence**: `usage/AUDIT_REPORT.md` (2025-12-28) cited README section “Find What You Need (Fast Navigation)”; current `README.md` uses “Start here (top links)”.
- **Impact**: Stale audit evidence misleads reviewers about navigation structure.
- **Fix proposal**: Superseded by this report (done). Keep audit reports dated and replace on full re-run.
- **Verification**: No references to removed section names in current `AUDIT_REPORT.md`.

- **ID**: A-12
- **Severity**: Low
- **Category**: duplication
- **Evidence**: High-risk trigger lists are aligned across `AGENTS.md`, `.github/copilot-instructions.md`, and `constitution/AI_ENFORCEMENT.md` (same boundary/contract/CI/interface set).
- **Impact**: Positive control; projections stay in sync.
- **Fix proposal**: None; re-check on future projection edits.
- **Verification**: Diff agent projections after constitution changes.

---

## Red-Team Drift Scenarios (Step 5)

### 1) Copy `standard` bundle; version docs missing
- **How it slips through**: Team copies `standard`, follows `usage/HOW_TO_IMPORT.md`, records import in ADR referencing `VERSIONING.md` changelog labels — file does not exist in target repo.
- **Smallest fix**: Include `VERSIONING.md` (and `kit-manifest.yml` snapshot) in `standard` bundle (A-01).

### 2) “Doc hygiene passed” without evidence
- **How it slips through**: After script removal, agent or human marks PR compliant with “ran doc check” but no checklist artifact; broken cross-refs in bundled docs go unnoticed.
- **Smallest fix**: Mandatory checklist output block in `DEVELOPMENT.md` (A-02); optional `usage/AI_RUN_EVIDENCE.md` block for hygiene runs.

### 3) Manifest `0.1` vs tag `v1.0.0` vs unreleased head
- **How it slips through**: Importer pins submodule to tag `v1.0.0` but reads `kit-manifest.yml` from `main` with bundle changes not in tag; ADR records wrong capability set.
- **Smallest fix**: Version mapping table + import ADR fields for both git tag and manifest `version` (A-03).

### 4) Integration bypass under time pressure (standing)
- **How it slips through**: New integration imports domain internals “temporarily”; no boundary CI in early adoption.
- **Smallest fix**: Downstream — dependency allowlist + ADR for boundary changes (`ci/ARCHITECTURE_GATES.md` A1).

### 5) Phantom AEP (standing)
- **How it slips through**: AEP marked READY with vague steps (“update docs”, “run tests”); execution diverges.
- **Smallest fix**: Enforce `usage/AEP_VALIDATION.md` fail conditions; require concrete paths and test command in READY plans.

---

## Doc Hygiene Evidence (2026-07-05)

- Relative markdown links in hub docs (`README.md`, `usage/HOW_TO_IMPORT.md`, `usage/ADOPTION_BUNDLES.md`, `architecture/README.md`, `DEVELOPMENT.md`, `VERSIONING.md`): **0 broken**
- All explicit paths in `kit-manifest.yml` bundles: **exist**
- `architecture/**/*.md` provenance banners: **100%** (spot-check)
- Import targets missing provenance: `AGENTS.md`, `.github/copilot-instructions.md` only
