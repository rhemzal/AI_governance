# Release Readiness (Manifest 1.0)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

Checklist for promoting `kit-manifest.yml` from experimental `0.x` to stable adoption contract **`1.0`**. See `VERSIONING.md` for version semantics.

## Preconditions (all required)

- [x] **Enforcement dogfood (phase 1)** — `doc-hygiene`, `aep-advisory`, `adr-required` ([ADR-0005](adr/ADR_0005_Kit_CI_Dogfooding.md))
- [x] **Adopter contract (phase 2)** — `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`, `GOVERNANCE_WAIVERS.md`, `BOUNDARY_GATE_RECIPES.md` ([ADR-0006](adr/ADR_0006_Adopter_Enforcement_Contract.md))
- [x] **Extended CI dogfood** — `doc-delta-advisory`, `governance-waiver-advisory`; enhanced AEP field checks; D5 **error** mode in `doc-hygiene`
- [x] **No shipped repository scripts** — inline CI only
- [ ] **Audit clean** — no open **High** findings in `usage/AUDIT_REPORT.md` after full playbook re-run
- [ ] **Bundle stability** — bundle paths stable one tagged release cycle
- [x] **Enforcement matrix** — includes adopter default column and phase-2 gates
- [x] **Navigation** — README routing; debugging index; enforcement contract linked for adopters
- [ ] **CHANGELOG + tag** — release section cut; git tag aligned with `VERSIONING.md`

## Release cut steps

1. Move `CHANGELOG.md` **Unreleased** entries into a dated version section.
2. Update `VERSIONING.md` **Current release mapping** (git tag ↔ manifest `version`).
3. Bump `kit-manifest.yml` `version` to `1.0` with explicit note if breaking vs `0.2`.
4. Tag repository (recommended: `v1.0.0-manifest` or next semver per policy).
5. Re-run audit; update `usage/AUDIT_REPORT.md`.

## Explicitly deferred past 1.0

| Item | Decision |
| --- | --- |
| `interface/` normative promotion | Stay **proposal** until separate ADR |
| Repository script pack | **Rejected** |
| Boundary gate in kit repo | N/A |
| Full AEP semantic CI parser | Review + inline grep only |
| Compliance certification | Out of scope |

## Related Documents

- `VERSIONING.md`
- `CHANGELOG.md`
- `usage/AUDIT_PLAYBOOK.md`
- `usage/AUDIT_REPORT.md`
- `usage/ENFORCEMENT_MATRIX.md`
- `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- `adr/ADR_0005_Kit_CI_Dogfooding.md`
- `adr/ADR_0006_Adopter_Enforcement_Contract.md`
