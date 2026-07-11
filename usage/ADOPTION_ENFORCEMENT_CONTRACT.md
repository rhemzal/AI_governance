# Adoption Enforcement Contract (Advisory Defaults)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This contract defines **default enforcement expectations** per import bundle and CI maturity level (L0–L3). It is **advisory** unless your `governance/LOCAL_OVERLAY.md` promotes items to required.

Normative gate definitions remain in `ci/`. Maturity semantics align with `usage/CI_MINIMUM_ADOPTION.md` and `constitution/ADAPTIVE_GOVERNANCE.md`.

## Status legend

| Status | Meaning |
| --- | --- |
| **Required** | Must be satisfied at this level (CI or PR evidence) |
| **Advisory** | Recommended; failures are warnings or review items |
| **Deferred** | Intentionally not enforced until prerequisites exist |

## Bundle × maturity matrix

### minimal bundle

| Level | Gates / practices | Status | Prerequisite | Evidence |
| --- | --- | --- | --- | --- |
| L0 | Agent projections (`AGENTS.md`, Copilot instructions) | Required | Bundle imported | Files present |
| L0 | Daily enforcement prompt (`constitution/AI_ENFORCEMENT_DAILY.md`) | Required | — | PR / agent output |
| L0 | ADR template available | Advisory | — | `adr/ADR_TEMPLATE.md` |
| L1+ | Doc hygiene CI, tests, boundary, AEP CI | Deferred | Upgrade to `standard` | — |

### standard bundle

| Level | Gates / practices | Status | Prerequisite | Evidence |
| --- | --- | --- | --- | --- |
| L0 | Everything in **minimal** L0 | Required | `standard` imported | Overlay declares level |
| L0 | Doc hygiene: manifest paths, hub links, provenance (D3) | Required | CI or manual checklist | `doc-hygiene` job / `DEVELOPMENT.md` checklist |
| L0 | Bundled cross-refs (import consistency) | Required | `kit-manifest.yml` present | `doc-hygiene` bundled cross-ref step |
| L1 | Deterministic tests (T1) | Required | Test suite exists | `deterministic-tests` job |
| L1 | AEP on multi-file PRs | Advisory | Agents active | `aep-advisory` / PR body |
| L1 | Canonical test command in overlay | Required | L1 declared | `governance/LOCAL_OVERLAY.md` |
| L2 | DOC DELTA on behavior-changing PRs (D2) | Required | Review or CI | PR `### DOC DELTA` / `doc-delta-advisory` |
| L2 | Boundary integrity (A1) | Required when tooling exists | Import lint / graph tool | `boundary-integrity` job |
| L2 | D5 anti-fragmentation (hub links for new docs) | Advisory → Required | Hub indexes exist | `doc-hygiene` D5 step |
| L3 | ADR on governance-impacting paths (A3) | Required | Stable team process | `adr-required` job |
| L3 | Coverage / flakiness signals (T2, T4) | Advisory | Stable test history | Scorecard / CI |
| L3 | AEP field completeness on READY | Advisory | Multi-agent workflow | Enhanced `aep-advisory` |

## Promotion path (recommended)

```text
Import standard → declare L0 in overlay → wire doc-hygiene CI
  → when tests exist: promote to L1 (+ test job, test command in overlay)
  → when boundary tooling exists: promote to L2 (+ boundary job, DOC DELTA enforcement)
  → when stable: promote to L3 (+ adr-required, risk signals)
```

Do not enable L2/L3 jobs as **required** until prerequisites pass — use `usage/GOVERNANCE_WAIVERS.md` for time-boxed exceptions.

## Waiver policy summary

When a **Required** gate cannot pass yet:

1. Record a waiver in the PR (`### Governance waiver`) per `usage/GOVERNANCE_WAIVERS.md`
2. Add row to overlay waiver registry
3. Set expiration and owner — no permanent waivers without quarterly review

## Copy-paste: overlay enforcement declaration

```markdown
## Enforcement maturity
- Level: L0 | L1 | L2 | L3
- Declared: YYYY-MM-DD
- Next review: YYYY-MM-DD
- Bundle baseline: minimal | standard (+ optional: architecture | research)

## Required gates (this repo)
- [ ] List from contract for chosen level — check when CI/review active

## Canonical test command (L1+)
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
- `adr/ADR_0006_Adopter_Enforcement_Contract.md`
