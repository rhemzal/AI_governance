# Enforcement Matrix (Reference Status)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This matrix is the **single source of truth** for gate timing across **CI Maturity (CM0–CM3)** and **Governance Level (G0–G4)**. It maps gate principles to kit reference implementation, automatibility, and adopter defaults (`usage/ADOPTION_ENFORCEMENT_CONTRACT.md`). It does not add new normative rules — see `constitution/` and `ci/`.

**Terminology:** See `architecture/TERMINOLOGY_GLOSSARY.md`. Do not use bare `L0`–`L3`.

## How to read this table

| Column | Meaning |
| --- | --- |
| **Gate** | Identifier from `ci/*.md` or cross-cutting workflow |
| **CM** | Adopter CI Maturity (`usage/CI_MINIMUM_ADOPTION.md`) |
| **G** | Governance Level when gate becomes recommended/mandatory per `ci/*.md` |
| **Kit reference** | Living workflow or starter in this repository |
| **Automatable** | Can be enforced in CI without stack-specific product code |
| **Adopter default** | Typical `standard` bundle expectation (overlay may override) |
| **Manual / review** | Human or PR checklist until prerequisites exist |

**Tooling note:** Most gates use inline CI steps. AEP uses the standard-library reference validator `ci/validate_aep.py` with regression tests (ADR-0009); see `usage/CI_STARTER_WORKFLOWS.md`. ADR-0010 also permits the scoped snapshot importer/checker `ci/import_bundle.py` and `ci/bundle_tests/`. Neither tool is an agent runtime. ADR-0011 adds executable fixtures in `ci/gate_tests/` for inline boundary recipes and the ADR check; `doc-hygiene` runs them. These validate reference implementations, not a product dependency graph.

## Canonical gate × CM × G table

| Gate | CM (adopter) | G (normative timing in `ci/`) | Kit reference | Automatable | Adopter default |
| --- | --- | --- | --- | --- | --- |
| D1 — Single source of truth | Advisory CM2; Required CM3 | Rec G2; Mand G3 | Starter §1 | Partial | Advisory CM2 |
| D2 — Docs updated with behavior | Required CM2 (review); CI advisory | Rec G2; Mand G3 | `doc-delta-advisory` | Partial (PR body) | Required CM2 review |
| D3 — Broken links / missing files | Required CM0 | Rec G1; Mand G2 | `doc-hygiene` (lychee) | Yes | Required CM0 |
| D4 — Reproducible doc generation | Deferred CM2+ | Rec G2; Mand G3 | — | Stack-dependent | Deferred |
| D5 — Anti-fragmentation | Advisory CM2; Required CM3 | Rec G2; Mand G3 | `doc-hygiene` (error on new docs) | Partial | Advisory CM2 → Required CM3 |
| T1 — Deterministic / non-interactive | Required CM1 | Rec G1; Mand G2 | Starter §2 | Yes (once tests exist) | Required CM1 |
| T2 — Coverage risk signal | Advisory CM3 | Rec G2; Mand G3 | — | Stack-dependent | Advisory CM3 |
| T3 — Test layer integrity | Deferred CM2+ | Rec G2; Mand G3 | — | Stack-dependent | Deferred |
| T4 — Flakiness budget | Advisory CM3 | Rec G2; Mand G3 | — | Partial | Advisory CM3 |
| A1 — Boundary integrity | Required CM2 when tooling exists | Rec G2; Mand G3 | Starter §3 + `BOUNDARY_GATE_RECIPES` | Stack-dependent | Required CM2 when wired |
| A2 — New adapter requires contract | Advisory CM2 | Rec G2; Mand G3 | — | Partial | Advisory CM2 |
| A3 — Architectural change requires ADR | Required CM3 | Rec G3; Mand G4 | `adr-required` | Yes (path-based) | Required CM3 |
| I1–I4 | Deferred CM2+ | Rec G2; Mand G3 | `interface/` proposal | Stack-dependent | Deferred |
| Selected import matches source | Required CM0 | — | `import_bundle.py --check`; all selections tested by kit CI | Yes | Check declared bundles against pinned source, not the full catalog |
| Applicable bundled context | Required CM0 | — | Kit cross-ref check + import fixtures | Partial | Baseline context present; review optional/upstream references |
| Provenance banners | Required CM0 | — | `doc-hygiene` | Yes | Required CM0 |
| AEP applicability / declaration shape | Advisory CM1; stronger CM3 | — | `aep-advisory` + reference validator | Structural only | Missing plan advisory; declared plan validated |
| Governance waiver block | Any CM | — | `governance-waiver-advisory` | Partial | When waiver used |
| Doc hygiene checklist 5–7 | Required CM0 (manual) | — | — | No | Required manual |

## Kit repo vs adopter repo (maintainer dogfood exceptions)

The kit repo contains documentation and reference-validator tests (no product test suite or product boundary lint). Maintainers run **stricter reference CI** than default adopter **CM0**. Adopters declare their own CM in overlay.

| Concern | Kit repo (maintainer) | Typical adopter (`standard`) |
| --- | --- | --- |
| Doc hygiene | **Required** (always on) | Required **CM0** |
| D5 anti-fragmentation | **Error** in `doc-hygiene` (maintainer policy) | Advisory **CM2** → Required **CM3** |
| DOC DELTA | Advisory (`doc-delta-advisory`) | Required **CM2** review; optional CI |
| Tests | AEP, import and inline gate regression fixtures + doc/CI verify; no product suite | Required **CM1** when tests exist |
| Boundary | N/A | Required **CM2** when recipes wired |
| ADR on governance paths | **Required** (`adr-required`) — maintainer dogfood | Required **CM3** |
| AEP | Advisory applicability + structured declaration validation and regression tests | Advisory applicability **CM1+**; declared plan shape validated |
| Waivers | Label advisory | `GOVERNANCE_WAIVERS` + overlay |

**Why ADR runs in kit repo before adopter CM3:** ADR-0005 dogfooding — governance-path changes in this repo must ship with an ADR. Adopters should not enable `adr-required` as required until **CM3** unless overlay promotes earlier.

**ADR check scope:** The reference requires an added/modified numbered regular ADR at the tested revision for governance-prefix changes. Deletions, templates and detected renames do not qualify. The starter fetches full history and uses the same check. Presence does not establish meaningful rationale or approval; see starter §4.

## Related Documents

- `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- `usage/GOVERNANCE_WAIVERS.md`
- `usage/BOUNDARY_GATE_RECIPES.md`
- `usage/CI_MINIMUM_ADOPTION.md`
- `usage/CI_STARTER_WORKFLOWS.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`
- `DEVELOPMENT.md`
- `ci/DOC_GATES.md`
- `ci/TEST_GATES.md`
- `ci/ARCHITECTURE_GATES.md`
- `ci/INTERFACE_GATES.md`
- `usage/AEP_VALIDATION.md`
- `adr/ADR_0005_Kit_CI_Dogfooding.md`
- `adr/ADR_0006_Adopter_Enforcement_Contract.md`
- `adr/ADR_0007_Governance_Level_vs_CI_Maturity.md`
