# Changelog

This project follows a lightweight changelog intended for governance-kit consumers.

## Unreleased

### Added
- [Advisory-only] `usage/ENFORCEMENT_MATRIX.md` — maps CI gates to kit reference workflows vs adopter wiring.
- [Advisory-only] `usage/DEBUGGING_INDEX.md` — curated debugging entry (15 patterns).
- [Advisory-only] `usage/RELEASE_READINESS.md` — manifest `1.0` readiness checklist.
- [Advisory-only] `adr/ADR_0005_Kit_CI_Dogfooding.md` — inline CI dogfood; no repository scripts.
- [Advisory-only] Kit CI: `.github/workflows/aep-advisory.yml`, `adr-required.yml`; `doc-hygiene` extended (bundled cross-refs, D5 warning).

### Changed
- [Advisory-only] `README.md` — “I am…” role routing; enforcement matrix and debugging index links.
- [Advisory-only] `DEVELOPMENT.md` — CI vs manual checklist table; local verification without scripts.
- [Advisory-only] `usage/CI_STARTER_WORKFLOWS.md` — inline patterns only; kit workflow references.
- [Advisory-only] `usage/PROACTIVE_TRIGGER_MAP.md` — automation hooks for new workflows.
- [Advisory-only] `AGENTS.md` — enforcement matrix + debugging index in triage.
- [Advisory-only] `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md` — points to DEBUGGING_INDEX first.
- [Advisory-only] `interface/INTERFACE_RULES_PROPOSAL.md` — explicit proposal-only status.
- [Advisory-only] `usage/QUICKGUIDE.md` — audit hygiene note without minimal-bundle root cross-ref break.
- [Advisory-only] `usage/ADOPTION_BUNDLES.md` — full paths for architecture prompt/template refs.
- [Advisory-only] Governance audit (`usage/AUDIT_REPORT.md`) — 2026-07-11 re-run after enforcement roadmap.

## v0.2.0 — 2026-07-05

### Added
- [Import bundle change] `kit-manifest.yml` — machine-readable adoption bundles (`minimal`, `standard`, `architecture`, `research`, `full`); manifest schema `0.2`.
- [Import bundle change] `kit-manifest.yml` — `standard` bundle includes `kit-manifest.yml`, `VERSIONING.md`, `DEVELOPMENT.md`, `CHANGELOG.md`.
- [Advisory-only] `.github/workflows/doc-hygiene.yml` — kit-repo L0 doc hygiene (shell + `yq` + `lychee`; no Python scripts).
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
