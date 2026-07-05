# Changelog

This project follows a lightweight changelog intended for governance-kit consumers.

## Unreleased

### Added
- [Import bundle change] `kit-manifest.yml` — machine-readable adoption bundles (`minimal`, `standard`, `architecture`, `research`, `full`).
- [Advisory-only] `usage/ADOPTION_BUNDLES.md` — human guide for bundle selection.
- [Advisory-only] `usage/PROACTIVE_TRIGGER_MAP.md` — path-prefix trigger map for multi-agent checks.
- [Advisory-only] `VERSIONING.md` — kit versioning and upgrade policy for importers.
- [Advisory-only] `architecture/README.md` — architecture directory entry point.
- [Advisory-only] `architecture/ARCHITECTURE_DECISION_PROMPT.md` — copy-paste precheck prompt with fixed output format.
- [Advisory-only] `architecture/rag/RAG_NOTE_TEMPLATE.md` — extracted template for new advisory RAG notes.
- [Advisory-only] `architecture/rag/OBSERVABILITY_AS_ARCHITECTURE.md` — cross-cutting observability guidance.
- [Advisory-only] `architecture/rag/FEATURE_FLAGS_PROGRESSIVE_DELIVERY.md` — cross-cutting feature-flag guidance.

### Changed
- [Advisory-only] Agent projections (`AGENTS.md`, `.github/copilot-instructions.md`) — Quick rules summary block; architecture entry point.
- [Advisory-only] Import docs (`usage/HOW_TO_IMPORT.md`, `usage/QUICKGUIDE.md`, `README.md`) — reference manifest and adoption bundles.
- [Advisory-only] Provenance banners added to remaining architecture and research import-target documents.
- [Advisory-only] `architecture/SOLUTION_CLASS_TAXONOMY.md` — Feature Flags and Observability upgraded to Advisory; extension checklist clarifies cross-cutting matrix entries.
- [Advisory-only] `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`, `architecture/ARCHITECTURE_STYLE_MATRIX.md`, `architecture/DATA_MODELING_GUIDE.md` — links and `DATA MODEL DECISION RECORD` mini-template.
- [Import bundle change] `kit-manifest.yml` — `architecture` bundle includes `README.md` and `ARCHITECTURE_DECISION_PROMPT.md`.
- [Advisory-only] `usage/QUICKGUIDE.md` — Recipe F (architecture decision precheck).

### Removed
- Docs: remove OS-specific doc-audit script; keep CI guidance tool-agnostic.
- [Advisory-only] Removed the Python doctor script before release to preserve the kit's documentation-first, tool-agnostic positioning.

## v1.0.0 — 2025-12-31

- Public-ready baseline: clear licensing split for docs vs code.
- Community hygiene: contributing, security policy, code of conduct, PR/issue templates.
- Import traceability: provenance banners added to import-target documents.
- CI: CI gate principles provided; implementation is environment-specific.
