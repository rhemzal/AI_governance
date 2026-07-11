# Fix Plan — AI_governance kit

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Active wave plan (2026-07-11 — full consistency audit)

**Scope:** `release` per `usage/AUDIT_PLAYBOOK.md` (Waves 0–8).  
**Status:** **All waves complete** (2026-07-11).  
**Report:** `usage/AUDIT_REPORT.md` — PASS, no open High findings.

### Wave status

| Wave | Theme | Status |
| --- | --- | --- |
| 0 | Baseline & scavenger | **Done** |
| 1 | Level taxonomy (G vs CM) | **Done** — ADR-0007, glossary, ADAPTIVE_GOVERNANCE |
| 2 | Gate × maturity alignment | **Done** — `ENFORCEMENT_MATRIX`, `ci/*.md` |
| 3 | Bundle & import graph | **Done** — minimal manifest + bundle-aware agents |
| 4 | Agent projections parity | **Done** — Overlay in COMPLIANCE; Copilot → AGENTS triage |
| 5 | Enforceability & dogfooding | **Done** — matrix kit exceptions; AEP doc-only escape |
| 6 | Theory & architecture corpus | **Done** — theory notes in AUDIT_REPORT |
| 7 | Red-team retest | **Done** |
| 8 | Release closure | **Done** — `CHANGELOG.md` v0.3.0; `VERSIONING.md` updated; **git tag pending** |

### Remaining maintainer actions (post-wave)

| Action | Owner | Notes |
| --- | --- | --- |
| Git tag `v0.3.0` | Maintainer | Changelog section cut; tag when ready |
| Manifest `1.0` promotion | Maintainer | See `usage/RELEASE_READINESS.md` — after one stable tagged cycle |
| Offline-first RAG depth | Optional | Low-priority theory bridge per AUDIT_REPORT Wave 6 |

---

## Completed work (prior audits — archive)

### Wave audit fixes (2026-07-11) — **Done**

All items H-01 through L-03 from `usage/AUDIT_REPORT.md`.

### Immediate fixes (2026-07-05 audit) — **Done**

| ID | Item |
| --- | --- |
| A-01 | Bundle root meta docs in `standard` |
| A-02 | Doc hygiene checklist in `DEVELOPMENT.md` |
| A-03 | Version mapping in `VERSIONING.md` |
| A-04–A-10 | Audit findability, kit CI, agent projections |

## Related Documents

- `usage/AUDIT_PLAYBOOK.md`
- `usage/AUDIT_REPORT.md`
- `usage/RELEASE_READINESS.md`
- `adr/ADR_0007_Governance_Level_vs_CI_Maturity.md`
