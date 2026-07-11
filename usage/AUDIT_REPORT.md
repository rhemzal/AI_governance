# Audit Report — AI_governance kit

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

Date: 2026-07-11 (full consistency audit — **closed**)  
Scope: `release` per `usage/AUDIT_PLAYBOOK.md` — Waves 0–8.  
ADR: `adr/ADR_0007_Governance_Level_vs_CI_Maturity.md`

## Wave status

| Wave | Focus | Status |
| --- | --- | --- |
| 0 | Baseline & scavenger | **Done** |
| 1 | Level taxonomy (G vs CM) | **Done** |
| 2 | Gate × maturity alignment | **Done** |
| 3 | Bundle & import graph | **Done** |
| 4 | Agent projections parity | **Done** |
| 5 | Enforceability & dogfooding | **Done** |
| 6 | Theory & architecture corpus | **Done** |
| 7 | Red-team retest | **Done** |
| 8 | Release closure (changelog cut) | **Done** (git tag pending maintainer) |

## Result summary

| Step | Status | Notes |
| --- | --- | --- |
| Scavenger test | **PASS** | Hub links, G/CM glossary, enforcement contract findable |
| Consistency scan | **PASS** | H-01–H-03 closed (ADR-0007, matrix, minimal bundle) |
| Enforceability review | **PASS** | Kit dogfood exceptions documented; AEP doc-only escape |
| Theory validation | **PASS** | See theory-bridge notes below (advisory gaps only) |
| Red-team drift | **PASS** | Scenarios retested; standing items documented |
| Doc hygiene CI | **PASS** | Kit repo |

**Release gate:** No open **High** findings. Manifest `1.0` promotion still requires stable bundle cycle + git tag per `usage/RELEASE_READINESS.md`.

---

## Closed findings (waves 1–5)

| ID | Severity | Resolution |
| --- | --- | --- |
| H-01 | High | G0–G4 and CM0–CM3 in glossary; ADAPTIVE_GOVERNANCE relabeled; ADR-0007 |
| H-02 | High | Canonical gate table in `ENFORCEMENT_MATRIX.md`; `ci/*.md` G + CM columns |
| H-03 | High | Minimal bundle extended; bundle-aware `AGENTS.md` / Copilot |
| M-01 | Medium | G×CM orientation map; CM0 cheap hygiene vs G2 anti-bloat explained |
| M-02 | Medium | Overlay line in agent COMPLIANCE footers |
| M-03 | Medium | AEP verification escape for doc-only repos |
| M-04 | Medium | Standing risk — overlay precedence documented in red-team table |
| M-05 | Medium | Kit vs adopter table in `ENFORCEMENT_MATRIX.md` |
| L-01 | Low | README duplicate heading removed |
| L-02 | Low | VERSIONING mapping documents v1.0.0 → v0.x lineage |
| L-03 | Low | Copilot points to `AGENTS.md` for full method triage |
| C-01 | Low | Accepted — DOC DELTA advisory in kit repo by design |

---

## Step 6 — Theory validation (Wave 6)

Spot-check of `architecture/SOLUTION_CLASS_TAXONOMY.md` vs `architecture/rag/`:

| Topic | Taxonomy | RAG coverage | Bridge gap |
| --- | --- | --- | --- |
| Feature flags | Advisory | `FEATURE_FLAGS_PROGRESSIVE_DELIVERY.md` | OK |
| Observability | Advisory | `OBSERVABILITY_AS_ARCHITECTURE.md` | OK |
| Offline-first | Mentioned | `CONSISTENCY_MODELS.md` partial | **Standing** — sync/conflict specifics out of scope (documented in taxonomy) |
| Schema evolution | Advisory | `SCHEMA_EVOLUTION_AND_VERSIONING.md` | OK |

No normative contradiction found. Optional follow-up: expand offline-first RAG note (low priority).

---

## Red-Team Drift Scenarios (Wave 7 retest)

| Scenario | Status |
| --- | --- |
| Standard import without CM declaration | **Mitigated** — overlay template + HOW_TO_IMPORT |
| Silent gate bypass | **Mitigated** — `GOVERNANCE_WAIVERS.md` + PR block |
| Phantom AEP | **Partially mitigated** — `aep-advisory` field grep |
| Boundary skip at CM2 | **Standing** — adopter must wire `BOUNDARY_GATE_RECIPES` |
| Level scale confusion (G2 vs CM2) | **Mitigated** — glossary + matrix + ADR-0007 |
| Minimal bundle phantom refs | **Mitigated** — bundle paths + bundle-aware agents |
| Overlay weakens constitution silently | **Standing** — requires explicit Overrides + review; no CI check |

---

## Related Documents

- `usage/AUDIT_PLAYBOOK.md`
- `usage/FIX_PLAN.md`
- `usage/RELEASE_READINESS.md`
- `adr/ADR_0007_Governance_Level_vs_CI_Maturity.md`
