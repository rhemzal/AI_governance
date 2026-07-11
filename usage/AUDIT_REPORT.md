# Audit Report — AI_governance kit

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

Date: 2026-07-11
Scope: Post–enforcement-roadmap re-run of `usage/AUDIT_PLAYBOOK.md` (Steps 1–5) + doc hygiene verification.
Prior audit: 2026-07-05 (superseded by this report).

Result summary:
- Scavenger test: **PASS** (core items + audit playbook + enforcement matrix findable from README)
- Consistency scan: **PASS** (bundle cross-refs aligned; architecture paths fixed in ADOPTION_BUNDLES)
- Enforceability review: **PASS with caveats** (kit dogfoods doc-hygiene, AEP advisory, ADR-required; no repository scripts per ADR-0005)
- Theory validation: **PASS**
- Red-team drift scenarios: mitigated for phantom AEP and bundle cross-ref; standing items documented
- Doc hygiene check: **PASS** (hub links expected valid; manifest paths exist; provenance on import targets)

---

## Step 1 — Scavenger Test

| Item | Result | Path(s) | Notes |
| --- | --- | --- | --- |
| High-risk boundary/contract change | **Found** | `README.md` → `constitution/AI_ENFORCEMENT.md` | Direct from “Start here”. |
| ADR template and contents | **Found** | `README.md` → `adr/ADR_TEMPLATE.md` | — |
| Audit playbook | **Found** | `README.md` → `usage/AUDIT_PLAYBOOK.md` | Also in “I am… maintainer” routing. |
| Enforcement matrix | **Found** | `README.md` → `usage/ENFORCEMENT_MATRIX.md` | New; clarifies automated vs manual. |
| Debugging entry (not full catalog) | **Found** | `README.md` → `usage/DEBUGGING_INDEX.md` | Catalog deferred to index. |
| Non-interactive / timeout expectations | **Found** | `AGENTS.md` Quick rules → `constitution/AI_RULES.md` §6.2 | — |

---

## Findings

- **ID**: B-01
- **Severity**: Low
- **Category**: enforceability
- **Evidence**: AEP CI checks PR-body tokens only; full AEP field validation remains manual per `usage/AEP_VALIDATION.md`.
- **Impact**: Phantom AEP reduced but not eliminated for READY plans missing file paths.
- **Fix proposal**: Keep advisory; adopters may promote to required via local overlay.
- **Verification**: `aep-advisory.yml` fails on TBD/TODO in READY body.

- **ID**: B-02
- **Severity**: Low
- **Category**: theory
- **Evidence**: `interface/INTERFACE_RULES_PROPOSAL.md` marked proposal-only; `usage/ENFORCEMENT_MATRIX.md` documents non-normative status.
- **Impact**: None (positive control).
- **Fix proposal**: Defer normative promotion past manifest `1.0` per `usage/RELEASE_READINESS.md`.

No **High** or **Medium** open findings after roadmap implementation.

---

## Red-Team Drift Scenarios (Step 5)

### 1) Copy `standard` bundle; version docs missing
- **Status**: **Mitigated** — `standard` includes `VERSIONING.md`, `DEVELOPMENT.md`, `CHANGELOG.md`; CI bundled cross-ref check in kit repo.

### 2) “Doc hygiene passed” without evidence
- **Status**: **Mitigated** — `DEVELOPMENT.md` checklist + CI coverage table; workflows dogfood checks.

### 3) Phantom AEP
- **Status**: **Partially mitigated** — `aep-advisory.yml` token lint; full semantics still review.

### 4) Integration bypass under time pressure
- **Status**: **Standing** — downstream boundary CI per `usage/CI_MINIMUM_ADOPTION.md` L2.

### 5) New doc without hub link
- **Status**: **Partially mitigated** — D5 warning in `doc-hygiene` on PR; not yet failing.

---

## Doc Hygiene Evidence (2026-07-11)

- Kit workflows: `doc-hygiene.yml`, `aep-advisory.yml`, `adr-required.yml`
- No `scripts/` directory (tool-agnostic; ADR-0005)
- New docs: `usage/ENFORCEMENT_MATRIX.md`, `usage/DEBUGGING_INDEX.md`, `usage/RELEASE_READINESS.md`, `adr/ADR_0005_Kit_CI_Dogfooding.md`
- `interface/` remains proposal-only

## Related Documents

- `usage/FIX_PLAN.md`
- `usage/RELEASE_READINESS.md`
- `adr/ADR_0005_Kit_CI_Dogfooding.md`
