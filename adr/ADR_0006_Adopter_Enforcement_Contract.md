# ADR 0006: Adopter Enforcement Contract

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status
Accepted

## Context
After kit-repo CI dogfooding (ADR-0005), adopters of the `standard` bundle still lacked a single document defining **Required vs Advisory vs Deferred** gates per maturity level L0–L3. Waivers were security-focused only. Boundary enforcement remained abstract without stack recipes.

Tool-agnostic positioning forbids a repository `scripts/` pack (ADR-0004, ADR-0005).

## Decision
1. Add `usage/ADOPTION_ENFORCEMENT_CONTRACT.md` as the **advisory default** for bundle × maturity enforcement expectations.
2. Add `usage/GOVERNANCE_WAIVERS.md` for auditable, time-boxed gate exceptions (not silent bypass).
3. Add `usage/BOUNDARY_GATE_RECIPES.md` with inline CI copy-paste patterns per stack (advisory).
4. Extend `governance/LOCAL_OVERLAY_TEMPLATE.md` as **system-of-record** for declared maturity, required gates, test command, and waiver registry.
5. Kit repo dogfoods additional inline workflows: `doc-delta-advisory`, `governance-waiver-advisory`; strengthen `aep-advisory`; promote D5 to error in `doc-hygiene`.
6. **No new constitution rules** — contract and recipes are usage-layer guidance; local overlay may promote items to required.

## Consequences
- Adopters have an explicit adoption enforcement path without new normative law in `constitution/`.
- Maintainers carry more CI jobs; all remain inline YAML.
- Manifest `1.0` readiness criteria expand per `usage/RELEASE_READINESS.md`.

## Enforcement
- Contract: `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- Waivers: `usage/GOVERNANCE_WAIVERS.md`
- Matrix: `usage/ENFORCEMENT_MATRIX.md`
- Workflows: `.github/workflows/doc-delta-advisory.yml`, `governance-waiver-advisory.yml`, updated `aep-advisory.yml`, `doc-hygiene.yml`
