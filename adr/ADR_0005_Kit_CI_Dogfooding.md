# ADR 0005: Kit Repo CI Dogfooding (Inline Workflows Only)

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status
Accepted

## Context
The kit documents CI gates as principles but historically under-implemented reference enforcement in its own repository. A roadmap proposed a `scripts/` directory for validators; that conflicts with tool-agnostic positioning (`adr/ADR_0004_Tooling_Is_Experimental.md`, removal of the Python doctor script in v0.2.0).

Adopters need clarity on what is automatable vs manual (`usage/ENFORCEMENT_MATRIX.md`).

## Decision
1. The kit repo **dogfoods** L0–L1 enforcement via GitHub Actions workflows with **inline shell steps only** — no repository script pack.
2. Reference patterns live in `usage/CI_STARTER_WORKFLOWS.md` for copy/adapt into any CI platform.
3. Add `usage/ENFORCEMENT_MATRIX.md`, `usage/DEBUGGING_INDEX.md`, and `usage/RELEASE_READINESS.md` as advisory navigation and release criteria — no new normative constitution rules.
4. `interface/` remains **proposal-only** until a future ADR promotes it.

## Consequences
- Maintainers get automated doc hygiene, bundled cross-ref checks, AEP token lint, and ADR-required on governance paths.
- Adopters copy YAML blocks, not scripts — stack and CI vendor remain their choice.
- Manifest `1.0` readiness is defined in `usage/RELEASE_READINESS.md`.

## Enforcement
- Workflows: `.github/workflows/doc-hygiene.yml`, `aep-advisory.yml`, `adr-required.yml`
- Matrix: `usage/ENFORCEMENT_MATRIX.md`
