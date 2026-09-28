# Adoption Enforcement Contract (Advisory Defaults)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This contract defines **default enforcement expectations** per import bundle and **CI Maturity (CM0–CM3)**. It is **advisory** unless your `governance/LOCAL_OVERLAY.md` promotes items to required.

Normative gate definitions remain in `ci/`. **CI Maturity (CM)** semantics align with `usage/CI_MINIMUM_ADOPTION.md`. **Governance Level (G0–G4)** is a separate project-risk scale — see `architecture/TERMINOLOGY_GLOSSARY.md` and `constitution/ADAPTIVE_GOVERNANCE.md`. Gate timing for both scales: `usage/ENFORCEMENT_MATRIX.md`.

## Import boundary

Kit files live under the declared kit root; host instructions, workflow activation, project ADRs and the active overlay remain project-owned. Record selected bundles and source SHA. The complete manifest catalog does not imply every bundle was imported. Verify only the declared selection against that pinned source (`usage/HOW_TO_IMPORT.md`); kit-wide manifest and cross-reference jobs are maintainer checks, not adopter requirements for absent optional bundles.

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
| CM0 | Agent projections and host entry point | Required | Bundle imported safely | Kit projections present; host instructions preserved and reference the declared kit root |
| CM0 | Daily enforcement prompt (`constitution/AI_ENFORCEMENT_DAILY.md`) | Required | — | PR / agent output |
| CM0 | ADR template available | Advisory | — | `adr/ADR_TEMPLATE.md` |
| CM1+ | Doc hygiene CI, tests, boundary, AEP CI | Deferred | Upgrade to `standard` | — |

### standard bundle

| CM | Gates / practices | Status | Prerequisite | Evidence |
| --- | --- | --- | --- | --- |
| CM0 | Everything in **minimal** CM0 | Required | `standard` imported | Overlay declares CM level |
| CM0 | Doc hygiene: selected import, actual project links, provenance (D3) | Required | CI or manual checklist | Selected-bundle comparison; project-owned doc checks |
| CM0 | Applicable context / references | Required | Declared kit root and bundle selection | Baseline context present; optional upstream references explicitly identified |
| CM1 | Deterministic tests (T1) | Required | Test suite exists | `deterministic-tests` job |
| CM1 | AEP applicability / declaration shape | Missing plan advisory; declared plan validated | Agents active | `aep-advisory` + `ci/validate_aep.py` / PR body |
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

## Engineering methods: behavior versus optional automation

`constitution/AI_RULES.md` §6.5 supplies the non-trivial-task behavioral minimum at any
bundle/CM: record baseline/gap, observable acceptance, smallest method and uncertainty
in existing evidence. This is not contingent on opting into the advisory matrix above.
The selector and [rollout guide](ENGINEERING_METHODS_ADOPTION.md) are included in minimal.

A project may promote a proven outcome for one scope in its existing overlay, with a
host command, evidence, owner and review trigger. Existing local/CI checks perform the
verification; method names and file presence are not gates. The optional finding-set
comparator in standard/full is inactive until wired by the adopter. It adds no CM requirement.
Legacy baselines require approved exception handling wherever normative obligations apply.

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
- Kit root: vendor/AI_governance/ (or declared location)
- Upstream commit SHA: record the pinned source
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
