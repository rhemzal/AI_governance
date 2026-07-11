# Changelog

This project follows a lightweight changelog intended for governance-kit consumers.

## Unreleased

_(No entries yet.)_

## v0.3.0 — 2026-07-11

Full consistency audit (Waves 0–8). Terminology and gate-timing alignment; minimal bundle expansion; audit closure.

### Added
- [Governance-impacting] `adr/ADR_0007_Governance_Level_vs_CI_Maturity.md` — G0–G4 vs CM0–CM3 disambiguation.
- [Advisory-only] `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`, `usage/GOVERNANCE_WAIVERS.md`, `usage/BOUNDARY_GATE_RECIPES.md`, `adr/ADR_0006_Adopter_Enforcement_Contract.md` (shipped post-v0.2.0; recorded here).
- [Advisory-only] Kit CI: `doc-delta-advisory.yml`, `governance-waiver-advisory.yml`.
- [Advisory-only] `usage/AUDIT_PLAYBOOK.md` — Full audit waves (0–8) procedure.

### Changed
- [Import bundle change] `kit-manifest.yml` — `minimal` bundle adds `constitution/AI_ENFORCEMENT.md`, `ADAPTIVE_GOVERNANCE.md`, `usage/AEP_VALIDATION.md`.
- [Governance-impacting] `architecture/TERMINOLOGY_GLOSSARY.md` — Governance Level (G) and CI Maturity (CM) terms + orientation map.
- [Governance-impacting] `constitution/ADAPTIVE_GOVERNANCE.md` — Governance Level G0–G4 labels; GOVERNANCE FIT CHECK includes CM hint.
- [Advisory-only] `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`, `usage/CI_MINIMUM_ADOPTION.md`, `governance/LOCAL_OVERLAY_TEMPLATE.md` — CM0–CM3 (replaces bare L0–L3).
- [Advisory-only] `usage/ENFORCEMENT_MATRIX.md` — canonical gate × CM × G table; kit maintainer dogfood exceptions.
- [Governance-impacting] `ci/DOC_GATES.md`, `ci/TEST_GATES.md`, `ci/ARCHITECTURE_GATES.md` — G and CM columns; link to matrix.
- [Advisory-only] `AGENTS.md`, `.github/copilot-instructions.md` — bundle-aware import scope; COMPLIANCE Overlay line; CM/G terminology.
- [Advisory-only] `usage/AEP_VALIDATION.md` — doc-only / no-test-suite verification escape.
- [Advisory-only] `usage/AUDIT_REPORT.md`, `usage/FIX_PLAN.md` — wave audit closed (PASS).
- [Advisory-only] `README.md`, `usage/HOW_TO_IMPORT.md`, `usage/ADOPTION_BUNDLES.md` — CM labels in adoption guidance.
- [Advisory-only] Prior v0.2.0 post-release items: enforcement matrix phase 2, `aep-advisory` field grep, D5 error in `doc-hygiene`, PR waiver block, `RELEASE_READINESS.md`.

## v0.2.0 — 2026-07-05

### Added
- [Import bundle change] `kit-manifest.yml` — machine-readable adoption bundles (`minimal`, `standard`, `architecture`, `research`, `full`); manifest schema `0.2`.
- [Import bundle change] `kit-manifest.yml` — `standard` bundle includes `kit-manifest.yml`, `VERSIONING.md`, `DEVELOPMENT.md`, `CHANGELOG.md`.
- [Advisory-only] `.github/workflows/doc-hygiene.yml` — kit-repo CM0 doc hygiene (shell + `yq` + `lychee`; no Python scripts).
- [Advisory-only] `usage/ADOPTION_BUNDLES.md` — human guide for bundle selection.
- [Advisory-only] `usage/PROACTIVE_TRIGGER_MAP.md` — path-prefix trigger map for multi-agent checks.
- [Advisory-only] `VERSIONING.md` — kit versioning and upgrade policy for importers; current release mapping table.
- [Advisory-only] `architecture/README.md` — architecture directory entry point.
- [Advisory-only] `architecture/ARCHITECTURE_DECISION_PROMPT.md` — copy-paste precheck prompt with fixed output format.
- [Advisory-only] `architecture/rag/RAG_NOTE_TEMPLATE.md` — extracted template for new advisory RAG notes.
- [Advisory-only] `architecture/rag/OBSERVABILITY_AS_ARCHITECTURE.md` — cross-cutting observability guidance.
- [Advisory-only] `architecture/rag/FEATURE_FLAGS_PROGRESSIVE_DELIVERY.md` — cross-cutting feature-flag guidance.
- [Advisory-only] `DEVELOPMENT.md` — numbered Doc Hygiene Checklist with PR output template.
- [Advisory-only] `usage/QUICKGUIDE.md` — Recipe F (architecture decision precheck); Recipe G (governance audit).
- [Advisory-only] Full governance audit (`usage/AUDIT_REPORT.md`, `usage/FIX_PLAN.md`) — 2026-07-05.

### Changed
- [Advisory-only] Agent projections (`AGENTS.md`, `.github/copilot-instructions.md`) — Quick rules summary block; architecture entry point; provenance banners; non-interactive/timeout quick rule.
- [Advisory-only] Import docs (`usage/HOW_TO_IMPORT.md`, `usage/QUICKGUIDE.md`, `README.md`) — reference manifest and adoption bundles; Option A resolves paths from manifest only.
- [Advisory-only] `usage/ADOPTION_BUNDLES.md` — documents root meta docs in `standard`.
- [Advisory-only] `usage/CI_STARTER_WORKFLOWS.md` — expanded starters (doc hygiene, boundary, AEP advisory); points to kit workflow.
- [Advisory-only] Provenance banners added to remaining architecture and research import-target documents.
- [Advisory-only] `architecture/SOLUTION_CLASS_TAXONOMY.md` — Feature Flags and Observability upgraded to Advisory; extension checklist clarifies cross-cutting matrix entries.
- [Advisory-only] `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`, `architecture/ARCHITECTURE_STYLE_MATRIX.md`, `architecture/DATA_MODELING_GUIDE.md` — links and `DATA MODEL DECISION RECORD` mini-template.
- [Import bundle change] `kit-manifest.yml` — `architecture` bundle includes `README.md` and `ARCHITECTURE_DECISION_PROMPT.md`.
- [Advisory-only] `README.md` — version note; link to audit playbook.
- [Advisory-only] `usage/AUDIT_PLAYBOOK.md` — `architecture/README.md` in mandatory inputs.
- [Advisory-only] `usage/PROACTIVE_TRIGGER_MAP.md` — automation hooks for CI starters and kit workflow.
- [Advisory-only] `governance/LOCAL_OVERLAY_TEMPLATE.md` — standard provenance banner.

### Removed
- Docs: remove OS-specific doc-audit script; keep CI guidance tool-agnostic.
- [Advisory-only] Removed the Python doctor script before release to preserve the kit's documentation-first, tool-agnostic positioning.

## v1.0.0 — 2025-12-31

- Public-ready baseline: clear licensing split for docs vs code.
- Community hygiene: contributing, security policy, code of conduct, PR/issue templates.
- Import traceability: provenance banners added to import-target documents.
- CI: CI gate principles provided; implementation is environment-specific.
