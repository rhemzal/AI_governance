# Changelog

This project follows a lightweight changelog intended for governance-kit consumers.

## Unreleased

### Added
- [Import bundle change] `kit-manifest.yml` — machine-readable adoption bundles (`minimal`, `standard`, `architecture`, `research`, `full`).
- [Advisory-only] `usage/ADOPTION_BUNDLES.md` — human guide for bundle selection.
- [Advisory-only] `usage/PROACTIVE_TRIGGER_MAP.md` — path-prefix trigger map for multi-agent checks.
- [Advisory-only] `VERSIONING.md` — kit versioning and upgrade policy for importers.
- [Governance-impacting] `scripts/doctor.py` — doc hygiene checks (links, provenance, README anchors, terminology, manifest paths, Related Documents).

### Changed
- [Advisory-only] Agent projections (`AGENTS.md`, `.github/copilot-instructions.md`) — Quick rules summary block.
- [Advisory-only] Import docs (`usage/HOW_TO_IMPORT.md`, `usage/QUICKGUIDE.md`, `README.md`) — reference manifest and adoption bundles.
- [Advisory-only] Provenance banners added to remaining architecture and research import-target documents.

### Removed
- Docs: remove OS-specific doc-audit script; keep CI guidance tool-agnostic.

## v1.0.0 — 2025-12-31

- Public-ready baseline: clear licensing split for docs vs code.
- Community hygiene: contributing, security policy, code of conduct, PR/issue templates.
- Import traceability: provenance banners added to import-target documents.
- CI: CI gate principles provided; implementation is environment-specific.
