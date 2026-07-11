# Release Readiness (Manifest 1.0)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

Checklist for promoting `kit-manifest.yml` from experimental `0.x` to stable adoption contract **`1.0`**. See `VERSIONING.md` for version semantics.

## Preconditions (all required)

- [ ] **Enforcement dogfood** — Kit repo runs `doc-hygiene`, `aep-advisory`, and `adr-required` workflows; status documented in `usage/ENFORCEMENT_MATRIX.md`.
- [ ] **No shipped repository scripts** — Validation stays inline in CI YAML per `adr/ADR_0004_Tooling_Is_Experimental.md` and `usage/CI_STARTER_WORKFLOWS.md` (tool-agnostic).
- [ ] **Audit clean** — Full `usage/AUDIT_PLAYBOOK.md` re-run; no open **High** findings in `usage/AUDIT_REPORT.md`.
- [ ] **Bundle stability** — `kit-manifest.yml` bundle paths unchanged for one tagged release cycle (or changes only with `[Import bundle change]` + migration note).
- [ ] **Enforcement matrix complete** — All D/T/A gates mapped in `usage/ENFORCEMENT_MATRIX.md`.
- [ ] **Navigation** — `README.md` role routing; `usage/DEBUGGING_INDEX.md` for catalog entry.
- [ ] **CHANGELOG + tag** — Release section cut; git tag aligned with `VERSIONING.md` mapping table.

## Release cut steps

1. Move `CHANGELOG.md` **Unreleased** entries into a dated version section.
2. Update `VERSIONING.md` **Current release mapping** (git tag ↔ manifest `version`).
3. Bump `kit-manifest.yml` `version` to `1.0` with explicit note if breaking vs `0.2`.
4. Tag repository (recommended: `v1.0.0-manifest` or next semver per policy).
5. Re-run audit; archive prior `usage/AUDIT_REPORT.md` date in the new report.

## Explicitly deferred past 1.0

| Item | Decision |
| --- | --- |
| `interface/` normative promotion | Stay **proposal** until separate ADR and consumer demand (`interface/INTERFACE_RULES_PROPOSAL.md`) |
| Repository script pack | **Rejected** — adopters use CI inline patterns, not copied shell libraries |
| Boundary gate in kit repo | N/A — no application code to lint |
| Compliance certification | Out of scope (see `README.md` disclaimer) |

## Related Documents

- `VERSIONING.md`
- `CHANGELOG.md`
- `usage/AUDIT_PLAYBOOK.md`
- `usage/AUDIT_REPORT.md`
- `usage/ENFORCEMENT_MATRIX.md`
- `adr/ADR_0004_Tooling_Is_Experimental.md`
