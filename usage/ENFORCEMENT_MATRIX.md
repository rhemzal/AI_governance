# Enforcement Matrix (Reference Status)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This matrix maps **CI gate principles** to **what the kit repo implements** vs **what adopters must wire locally**. It does not add new normative rules — see `constitution/` and `ci/` for requirements.

## How to read this table

| Column | Meaning |
| --- | --- |
| **Gate** | Identifier from `ci/*.md` or cross-cutting workflow |
| **CI maturity** | Suggested level from `usage/CI_MINIMUM_ADOPTION.md` |
| **Kit reference** | Living workflow or starter in this repository |
| **Automatable** | Can be enforced in CI without stack-specific product code |
| **Manual / review** | Human or PR checklist until prerequisites exist |

**Tooling note:** The kit ships **no repository scripts**. Reference checks are **inline CI steps** (shell, `yq`, actions) documented in `usage/CI_STARTER_WORKFLOWS.md`. Adopters copy YAML blocks into their CI platform of choice.

## Documentation gates (`ci/DOC_GATES.md`)

| Gate | CI maturity | Kit reference | Automatable | Manual / review |
| --- | --- | --- | --- | --- |
| D1 — Single source of truth | L2+ | Starter §1 (provenance subset) | Partial (grep) | Rule duplication review |
| D2 — Docs updated with behavior | L2+ | — | No | `DOC DELTA` in PR |
| D3 — Broken links / missing files | L0+ | `.github/workflows/doc-hygiene.yml` (lychee hubs) | Yes | — |
| D4 — Reproducible doc generation | L2+ | — | Stack-dependent | Generator discipline |
| D5 — Anti-fragmentation | L2+ | `doc-hygiene` (warning on new `usage/` / `architecture/` docs) | Partial | Hub link in PR review |

## Test gates (`ci/TEST_GATES.md`)

| Gate | CI maturity | Kit reference | Automatable | Manual / review |
| --- | --- | --- | --- | --- |
| T1 — Deterministic / non-interactive | L1+ | Starter §2 | Yes (once tests exist) | Pick repo-local command |
| T2 — Coverage risk signal | L3 | — | Stack-dependent | Waivers / thresholds |
| T3 — Test layer integrity | L2+ | — | Stack-dependent | Layer conventions |
| T4 — Flakiness budget | L3 | — | Partial | Quarantine policy |

## Architecture gates (`ci/ARCHITECTURE_GATES.md`)

| Gate | CI maturity | Kit reference | Automatable | Manual / review |
| --- | --- | --- | --- | --- |
| A1 — Boundary integrity | L2+ | Starter §3 (placeholder) | Stack-dependent | Import lint / graph tooling |
| A2 — New adapter requires contract | L2+ | — | Partial | PR + contract name |
| A3 — Architectural change requires ADR | L3 | `.github/workflows/adr-required.yml` (kit dogfood) | Yes (path-based) | Level 1–2: warn only locally |

## Interface gates (`ci/INTERFACE_GATES.md`)

| Gate | CI maturity | Kit reference | Automatable | Manual / review |
| --- | --- | --- | --- | --- |
| I1–I4 | L2+ | `interface/` is **proposal only** (not normative) | Stack-dependent | Merge proposal with local rules |

## Cross-cutting

| Check | CI maturity | Kit reference | Automatable | Manual / review |
| --- | --- | --- | --- | --- |
| Manifest paths exist | L0 | `doc-hygiene` | Yes (`yq`) | — |
| Bundled cross-refs | L0 | `doc-hygiene` | Yes (inline shell) | Upstream-only refs in docs |
| Provenance banners | L0 | `doc-hygiene` | Yes | — |
| AEP READY (multi-file PR) | L1+ | `.github/workflows/aep-advisory.yml` | Partial (PR body tokens) | Full AEP semantics |
| Doc hygiene checklist items 5–7 | L0 | — | No | Terminology, Related Documents, changelog |

## Kit repo vs adopter repo

| Concern | Kit repo | Typical adopter |
| --- | --- | --- |
| Doc hygiene | Required CI (`doc-hygiene`) | Copy starter §1; adapt paths |
| Tests | No product test suite | Starter §2 when tests exist |
| Boundary | No application layers | Starter §3 when tooling exists |
| ADR on governance paths | Required (`adr-required`) | Optional until L3 |
| AEP on multi-file PRs | Advisory (`aep-advisory`) | Enable when agents are primary authors |

## Related Documents

- `usage/CI_MINIMUM_ADOPTION.md`
- `usage/CI_STARTER_WORKFLOWS.md`
- `DEVELOPMENT.md`
- `ci/DOC_GATES.md`
- `ci/TEST_GATES.md`
- `ci/ARCHITECTURE_GATES.md`
- `ci/INTERFACE_GATES.md`
- `usage/AEP_VALIDATION.md`
- `adr/ADR_0004_Tooling_Is_Experimental.md`
