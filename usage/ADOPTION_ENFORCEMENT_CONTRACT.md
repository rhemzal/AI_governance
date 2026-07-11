# Adoption Enforcement Contract (Advisory Defaults)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This contract defines **default enforcement expectations** per import bundle and **CI Maturity (CM0–CM3)**. It is **advisory** unless your `governance/LOCAL_OVERLAY.md` promotes items to required.

Normative gate definitions remain in `ci/`. **CI Maturity (CM)** semantics align with `usage/CI_MINIMUM_ADOPTION.md`. **Governance Level (G0–G4)** is a separate project-risk scale — see `architecture/TERMINOLOGY_GLOSSARY.md` and `constitution/ADAPTIVE_GOVERNANCE.md`. Gate timing for both scales: `usage/ENFORCEMENT_MATRIX.md`.

## Status legend

| Status | Meaning |
| --- | --- |
| **Required** | Must be satisfied at this CM level (CI or PR evidence) |
| **Advisory** | Recommended; failures are warnings or review items |
| **Deferred** | Intentionally not enforced until prerequisites exist |

## Bundle × CI Maturity matrix

### minimal bundle

| CM | Gates / practices | Status | Prerequisite | Evidence |
| --- | --- | --- | --- | --- |
| CM0 | Agent projections (`AGENTS.md`, Copilot instructions) | Required | Bundle imported | Files present |
| CM0 | Daily enforcement prompt (`constitution/AI_ENFORCEMENT_DAILY.md`) | Required | — | PR / agent output |
| CM0 | ADR template available | Advisory | — | `adr/ADR_TEMPLATE.md` |
| CM1+ | Doc hygiene CI, tests, boundary, AEP CI | Deferred | Upgrade to `standard` | — |

### standard bundle

| CM | Gates / practices | Status | Prerequisite | Evidence |
| --- | --- | --- | --- | --- |
| CM0 | Everything in **minimal** CM0 | Required | `standard` imported | Overlay declares CM level |
| CM0 | Doc hygiene: manifest paths, hub links, provenance (D3) | Required | CI or manual checklist | `doc-hygiene` job / `DEVELOPMENT.md` checklist |
| CM0 | Bundled cross-refs (import consistency) | Required | `kit-manifest.yml` present | `doc-hygiene` bundled cross-ref step |
| CM1 | Deterministic tests (T1) | Required | Test suite exists | `deterministic-tests` job |
| CM1 | AEP on multi-file PRs | Advisory | Agents active | `aep-advisory` / PR body |
| CM1 | Canonical test command in overlay | Required | CM1 declared | `governance/LOCAL_OVERLAY.md` |
| CM2 | DOC DELTA on behavior-changing PRs (D2) | Required | Review or CI | PR `### DOC DELTA` / `doc-delta-advisory` |
| CM2 | Boundary integrity (A1) | Required when tooling exists | Import lint / graph tool | `boundary-integrity` job |
| CM2 | D5 anti-fragmentation (hub links for new docs) | Advisory → Required | Hub indexes exist | `doc-hygiene` D5 step |
| CM3 | ADR on governance-impacting paths (A3) | Required | Stable team process | `adr-required` job |
| CM3 | Coverage / flakiness signals (T2, T4) | Advisory | Stable test history | Scorecard / CI |
| CM3 | AEP field completeness on READY | Advisory | Multi-agent workflow | Enhanced `aep-advisory` |

## Promotion path (recommended)

```text
Import standard → declare CM0 in overlay → wire doc-hygiene CI
  → when tests exist: promote to CM1 (+ test job, test command in overlay)
  → when boundary tooling exists: promote to CM2 (+ boundary job, DOC DELTA enforcement)
  → when stable: promote to CM3 (+ adr-required, risk signals)
```

Do not enable CM2/CM3 jobs as **required** until prerequisites pass — use `usage/GOVERNANCE_WAIVERS.md` for time-boxed exceptions.

## Waiver policy summary

When a **Required** gate cannot pass yet:

1. Record a waiver in the PR (`### Governance waiver`) per `usage/GOVERNANCE_WAIVERS.md`
2. Add row to overlay waiver registry
3. Set expiration and owner — no permanent waivers without quarterly review

## Copy-paste: overlay enforcement declaration

```markdown
## Enforcement maturity (CI Maturity)
- CM level: CM0 | CM1 | CM2 | CM3
- Declared: YYYY-MM-DD
- Next review: YYYY-MM-DD
- Bundle baseline: minimal | standard (+ optional: architecture | research)
- Governance Level (G) note (optional): G0 | G1 | G2 | G3 | G4 — project risk band; see ADAPTIVE_GOVERNANCE

## Required gates (this repo)
- [ ] List from contract for chosen CM level — check when CI/review active

## Canonical test command (CM1+)
- Command: `[e.g. make test]`

## Waiver registry
| Gate ID | Owner | Expiration | PR/issue | Status |
| --- | --- | --- | --- | --- |
```

## Related Documents

- `usage/ADOPTION_BUNDLES.md`
- `usage/HOW_TO_IMPORT.md`
- `usage/ENFORCEMENT_MATRIX.md`
- `usage/CI_MINIMUM_ADOPTION.md`
- `usage/GOVERNANCE_WAIVERS.md`
- `usage/BOUNDARY_GATE_RECIPES.md`
- `governance/LOCAL_OVERLAY_TEMPLATE.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`
- `adr/ADR_0006_Adopter_Enforcement_Contract.md`
- `adr/ADR_0007_Governance_Level_vs_CI_Maturity.md`
