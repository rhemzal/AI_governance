# Enforcement Matrix (Reference Status)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This matrix maps **CI gate principles** to **kit reference implementation**, **automatibility**, and **adopter defaults** (`usage/ADOPTION_ENFORCEMENT_CONTRACT.md`). It does not add new normative rules — see `constitution/` and `ci/`.

## How to read this table

| Column | Meaning |
| --- | --- |
| **Gate** | Identifier from `ci/*.md` or cross-cutting workflow |
| **CI maturity** | Suggested level from `usage/CI_MINIMUM_ADOPTION.md` |
| **Kit reference** | Living workflow or starter in this repository |
| **Automatable** | Can be enforced in CI without stack-specific product code |
| **Adopter default** | Typical `standard` bundle expectation (overlay may override) |
| **Manual / review** | Human or PR checklist until prerequisites exist |

**Tooling note:** No repository scripts. Inline CI steps only (`usage/CI_STARTER_WORKFLOWS.md`).

## Documentation gates (`ci/DOC_GATES.md`)

| Gate | CI maturity | Kit reference | Automatable | Adopter default | Manual / review |
| --- | --- | --- | --- | --- | --- |
| D1 — Single source of truth | L2+ | Starter §1 (provenance subset) | Partial | Advisory L2 | Rule duplication review |
| D2 — Docs updated with behavior | L2+ | `doc-delta-advisory` | Partial (PR body) | Required L2 (review); CI advisory | Full doc impact judgment |
| D3 — Broken links / missing files | L0+ | `doc-hygiene` (lychee) | Yes | Required L0 | — |
| D4 — Reproducible doc generation | L2+ | — | Stack-dependent | Deferred | Generator discipline |
| D5 — Anti-fragmentation | L2+ | `doc-hygiene` (error on new docs) | Partial | Advisory L2; Required L3 | Hub link in PR |

## Test gates (`ci/TEST_GATES.md`)

| Gate | CI maturity | Kit reference | Automatable | Adopter default | Manual / review |
| --- | --- | --- | --- | --- | --- |
| T1 — Deterministic / non-interactive | L1+ | Starter §2 | Yes (once tests exist) | Required L1 | Pick repo-local command |
| T2 — Coverage risk signal | L3 | — | Stack-dependent | Advisory L3 | Waivers / thresholds |
| T3 — Test layer integrity | L2+ | — | Stack-dependent | Deferred | Layer conventions |
| T4 — Flakiness budget | L3 | — | Partial | Advisory L3 | Quarantine policy |

## Architecture gates (`ci/ARCHITECTURE_GATES.md`)

| Gate | CI maturity | Kit reference | Automatable | Adopter default | Manual / review |
| --- | --- | --- | --- | --- | --- |
| A1 — Boundary integrity | L2+ | Starter §3 + `BOUNDARY_GATE_RECIPES` | Stack-dependent | Required L2 when tooling exists | Import lint setup |
| A2 — New adapter requires contract | L2+ | — | Partial | Advisory L2 | PR + contract name |
| A3 — Architectural change requires ADR | L3 | `adr-required` | Yes (path-based) | Required L3 | L1–2: warn locally |

## Interface gates (`ci/INTERFACE_GATES.md`)

| Gate | CI maturity | Kit reference | Automatable | Adopter default | Manual / review |
| --- | --- | --- | --- | --- | --- |
| I1–I4 | L2+ | `interface/` **proposal only** | Stack-dependent | Deferred | Merge with local rules |

## Cross-cutting

| Check | CI maturity | Kit reference | Automatable | Adopter default | Manual / review |
| --- | --- | --- | --- | --- | --- |
| Manifest paths exist | L0 | `doc-hygiene` | Yes | Required L0 (`standard`) | — |
| Bundled cross-refs | L0 | `doc-hygiene` | Yes | Required L0 (`standard`) | Upstream-only refs |
| Provenance banners | L0 | `doc-hygiene` | Yes | Required L0 | — |
| AEP READY (multi-file PR) | L1+ | `aep-advisory` | Partial | Advisory L1; stronger at L3 | Full AEP semantics |
| Governance waiver block | Any | `governance-waiver-advisory` | Partial (label + body) | When waiver used | Overlay registry |
| Doc hygiene checklist 5–7 | L0 | — | No | Required (manual) | Terminology, Related Docs |

## Kit repo vs adopter repo

| Concern | Kit repo | Typical adopter (`standard`) |
| --- | --- | --- |
| Doc hygiene | Required | Required L0 |
| DOC DELTA | Advisory (`doc-delta-advisory`) | Required L2 review; optional CI |
| Tests | No product suite | Required L1 when tests exist |
| Boundary | N/A | Required L2 when recipes wired |
| ADR on governance paths | Required | Required L3 |
| AEP multi-file | Advisory + field grep | Advisory L1+ |
| Waivers | Label advisory | `GOVERNANCE_WAIVERS` + overlay |

## Related Documents

- `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- `usage/GOVERNANCE_WAIVERS.md`
- `usage/BOUNDARY_GATE_RECIPES.md`
- `usage/CI_MINIMUM_ADOPTION.md`
- `usage/CI_STARTER_WORKFLOWS.md`
- `DEVELOPMENT.md`
- `ci/DOC_GATES.md`
- `ci/TEST_GATES.md`
- `ci/ARCHITECTURE_GATES.md`
- `ci/INTERFACE_GATES.md`
- `usage/AEP_VALIDATION.md`
- `adr/ADR_0005_Kit_CI_Dogfooding.md`
- `adr/ADR_0006_Adopter_Enforcement_Contract.md`
