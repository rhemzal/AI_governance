# Fix Plan — AI_governance kit

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Active backlog — 2026-09-27

**Baseline:** `768e2028eaabf943cb6b68e077d891db16f90332` (merged PR #34).

**Report:** [AUDIT_REPORT.md](AUDIT_REPORT.md), current September audit.

**State:** review complete with **17 open findings (1 High, 13 Medium, 3 Low)**. This PR records evidence and proposals; it does not implement repairs. The July closure below is historical.

Prioritize safe adoption and truthful verification before adding enforcement. Fix existing checks with small negative fixtures; do not introduce a general script pack, agent orchestrator, mandatory extra reviewers, or broad new process. Existing tests passing is compatible with uncovered defects.

### Repair themes in priority order

Each row is a focused repair theme with acceptance criteria, not a new workflow mandate. Keep implementation PRs small, use the existing ADR process for affected normative decisions, and stop expanding a theme once its demonstrated risk is addressed.

| Priority | Theme / findings | Target paths | Smallest useful change | Acceptance evidence |
| --- | --- | --- | --- | --- |
| P0 | Safe copy import — A-01, A-02 | `usage/HOW_TO_IMPORT.md`, `usage/ADOPTION_BUNDLES.md`, `kit-manifest.yml`, agent projections, affected normative context and import CI guidance | Preserve project-owned instructions/meta files; surface collisions; reconcile required context with selected bundles; separate kit-wide and adopter checks | Existing-file sentinel fixture preserves host content; empty minimal/standard/optional/full copies resolve applicable prerequisites; missing required files fail |
| P1 | Reliable boundary recipes — A-03 | `usage/BOUNDARY_GATE_RECIPES.md`, starter §3 | Detect path/scanner errors and ordinary forbidden imports; state limits | Missing paths and direct/from/indented/relative forbidden imports fail; allowed dependencies pass |
| P1 | AEP declaration detection — A-07 | `ci/validate_aep.py`, `ci/tests/test_validate_aep.py`, `usage/AEP_VALIDATION.md`, related guidance if needed | Recognize or explicitly reject alternate fences; keep absent plans advisory | Existing 12 tests plus canonical/indented/tilde/longer/multiple/unfinished-fence regressions; valid recognized plans pass |
| P1 | ADR correctness and starter parity — A-04, A-05 | `.github/workflows/adr-required.yml`, starter §4 | Require an existing eligible added/updated record; fetch comparison revisions; exclude deletion/template loopholes | PR-style checkout works; no-ADR/deleted-ADR/rename-away/template-only negatives fail; qualifying decision passes |
| P2 | Useful advisory evidence — A-06 | Waiver and DOC DELTA workflows, PR template, waiver guide | Inspect section-local non-placeholder values; retain advisory severity | Empty templates warn; unrelated matching prose does not suppress warnings; populated sections and exemptions work |
| P2 | One applicability and gate contract — A-09, A-10, A-16 | Constitution/daily enforcement, architecture/interface gates, matrix, contributing/import/overlay projections | Decide A3 timing; enumerate A4/A5/I5; qualify G/CM; reconcile reporting, ADR/test applicability, interface authority and automation scope | Complete gate-ID/timing comparison; G0, reversible G1, CM0 without tests, and high-risk scenarios agree; interactive and automation modes have consistent rules |
| P2 | Architecture selection examples — A-11, A-12 | Quality-attributes RAG note, architecture style matrix, corresponding framework references | Correct dependency prohibition; make exactly-once requirement-dependent | Core-to-adapter violation rejected, inward dependency allowed; suitable at-least-once/idempotent streaming remains eligible |
| P2 | Accurate enforcement status — A-08 | Enforcement matrix and trigger guidance; workflow implementation only if required statuses are selected | Separate policy, check execution, and branch enforcement; prevent path-filter pending checks before a required-status rollout | Dated metadata matches docs; governance, usage-only and Python-only PRs get intended status; no automatic protection change |
| P2/P3 | Current release/setup/navigation guidance — A-13, A-14, A-15, A-17 | README, version mapping, ADR-0008/0009 status, release checklist, VS Code setup, audit playbook, local-link scope | Describe untagged releases truthfully; reconcile merged ADR status; update extension guidance; fix relative links; remove residual finding quota | Advertised pins resolve; release states agree; official setup source checked; local links resolve; zero-defect audit satisfies the playbook |

### Ordering and decisions

- Start with host-file collisions. Do not recommend fresh literal copy imports until a preservation rule exists.
- Repair demonstrated detection gaps before presenting green checks as substantive evidence. A populated plan or ADR still needs review of meaning and authority.
- Resolve canonical applicability before copying more quick rules. Decide A3 timing explicitly; this audit does not silently choose G3 or G4.
- Branch protection is **not** a prerequisite for repairs. If the maintainer wants required checks, prepare compatible statuses first and make that policy decision separately. Preserve adaptive governance for solo use.
- Tag creation and manifest `1.0` promotion remain separate maintainer decisions. Do not publish a tag just to reconcile stale text.

### Retest and closure

| Checkpoint | Required evidence | Current state |
| --- | --- | --- |
| Finding closed | Implemented repair; original failing scenario now behaves correctly; unaffected control still works | All A-01–A-17 open |
| Wave 7 closure | At least three distinct drift scenarios recorded; no open High finding | Scenarios recorded; High A-01 open |
| Clean release audit | Material findings repaired or explicitly dispositioned with rationale; applicable wave exit criteria rechecked against an exact revision | Not established |
| Stable bundle contract | Selected-bundle adoption works; one tagged stable cycle; release mapping and remaining checklist conditions satisfied | Not established |

Record the new SHA and environment beside retest results; retain original failure evidence. A passing doc-hygiene job or merge of this audit PR closes no finding by itself. This plan waives none.

---

## Historical fix plan — 2026-07-11

Preserved as recorded. “All waves complete” and “PASS” below refer to the earlier audit, not the active backlog.

<details>
<summary>July 2026 plan (historical record)</summary>

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

</details>
