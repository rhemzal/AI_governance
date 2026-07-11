# ADR 0007: Governance Level (G) vs CI Maturity (CM)

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status
Accepted

## Context
Audit wave 1 (2026-07-11) found that **Governance Level** (`constitution/ADAPTIVE_GOVERNANCE.md`, G0–G4) and **CI Maturity** (`usage/CI_MINIMUM_ADOPTION.md`, formerly bare L0–L3) used the same numeric labels for different concepts. Gate docs in `ci/` referenced Governance Level while `usage/ENFORCEMENT_MATRIX.md` and the adopter contract referenced CI Maturity, producing contradictory “when is gate X required?” answers.

## Decision
1. **Governance Level** is labeled **G0–G4** (project maturity / risk band).
2. **CI Maturity** is labeled **CM0–CM3** (staged gate automation for kit adopters).
3. Canonical definitions and an orientation map live in `architecture/TERMINOLOGY_GLOSSARY.md`.
4. Canonical gate × CM × G mapping lives in `usage/ENFORCEMENT_MATRIX.md`.
5. `ci/*_GATES.md` rows cite **Governance Level (G)** for normative timing; CM columns point to the matrix.
6. Adopter overlay declares **CM** level, not G (G is assessed per task via GOVERNANCE FIT CHECK).

## Consequences
- Docs must not use bare `L0`–`L3` in normative paths (CM or G prefix required).
- Importers re-declare overlay enforcement maturity as CM0–CM3.
- Manifest `1.0` readiness still blocked until audit waves close; this ADR is governance-impacting but non-breaking for bundle paths.

## Related Documents
- `architecture/TERMINOLOGY_GLOSSARY.md`
- `constitution/ADAPTIVE_GOVERNANCE.md`
- `usage/ENFORCEMENT_MATRIX.md`
- `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- `usage/AUDIT_REPORT.md`
