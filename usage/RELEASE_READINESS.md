# Release Readiness (Manifest 1.0)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

Checklist for promoting `kit-manifest.yml` from experimental `0.x` to stable adoption contract **`1.0`**. See `VERSIONING.md` for version semantics.

## Preconditions (all required)

- [x] **Enforcement dogfood (phase 1)** — `doc-hygiene`, `aep-advisory`, `adr-required` ([ADR-0005](adr/ADR_0005_Kit_CI_Dogfooding.md))
- [x] **Adopter contract (phase 2)** — `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`, `GOVERNANCE_WAIVERS.md`, `BOUNDARY_GATE_RECIPES.md` ([ADR-0006](adr/ADR_0006_Adopter_Enforcement_Contract.md))
- [x] **Extended CI dogfood** — `doc-delta-advisory`, `governance-waiver-advisory`; enhanced AEP field checks; D5 **error** mode in `doc-hygiene`
- [ ] **Reference validator adoption** — ADR-0009 permits the scoped AEP validator and regression tests; confirm one tagged bundle cycle before promotion
- [ ] **Audit clean** — the [2026-09-27 audit](AUDIT_REPORT.md) of merged PR #34 records 17 open findings (1 High, 13 Medium, 3 Low). Wave 7 scenarios were exercised, but its no-open-High closure criterion is unmet; see [repair plan](FIX_PLAN.md). The July PASS is historical, not current validation.
- [ ] **Bundle stability** — bundle paths stable one tagged release cycle (`v0.3.0` tag pending)
- [ ] **Enforcement matrix** — reconcile missing/conflicting gate mappings and distinguish policy from actual branch enforcement (September findings A-08/A-09).
- [ ] **Navigation** — retain README/debugging/adopter routing; repair the two ADR links in this checklist and retest local links (September finding A-15).
- [ ] **CHANGELOG + tag** — release section cut in `CHANGELOG.md` v0.3.0; git tag `v0.3.0` aligned with `VERSIONING.md` (section cut **done**; tag pending)

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
| General-purpose repository script pack / agent orchestrator | **Deferred**; ADR-0009 permits only the scoped AEP validator and tests |
| Boundary gate in kit repo | N/A |
| Full AEP semantic CI parser | **Deferred**; structural JSON validation + independent review |
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
