# Audit Playbook (Opposition / Review)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Purpose
This playbook helps you **audit this governance kit** (or a repo that imports it) to:
- find contradictions, duplication, and “hard to find” guidance
- detect requirements that are not enforceable in practice
- verify theoretical soundness for architecture selection and hybridization
- produce a concrete fix list that can be implemented as PRs

This document is **advisory**. Normative rules live in `constitution/`.

## What “Good Audit” Means
A good audit records which areas were examined, the evidence used, limitations, and any reproducible findings. Findings and severity are outcomes of the audit, not quotas. Zero findings is valid when supported by documented coverage; never invent or inflate findings to satisfy a target.

For release/quarterly audits, exercise at least three distinct drift/bypass scenarios and record whether each is prevented, detected, or remains unresolved. This is a coverage requirement, not a requirement to discover three defects.

## Audit scope triage

Pick scope **before** loading all mandatory inputs or running all steps. Do not default to Steps 1–5 for every task.

| Scope | When | Steps | Mandatory inputs (subset) | Required coverage |
| --- | --- | --- | --- | --- |
| **post_import** | After kit import | 1, 3, 5 | `README.md`, `constitution/AI_RULES.md`, `usage/HOW_TO_IMPORT.md`, `kit-manifest.yml` | Import completeness, applicability, enforcement |
| **prefix** | Change in one path prefix | 2, 3 | `usage/PROACTIVE_TRIGGER_MAP.md` row + affected paths | Changed rules, projections, enforcement |
| **release** | Before release tag | 1–5 | Full mandatory list below | All audit areas and three drift scenarios |
| **quarterly** | Regular governance review | 1–5 | Full mandatory list below | All audit areas and three drift scenarios |

Anti-overload: load only the input subset for the chosen scope; expand if evidence requires it.

## Full audit waves (release / quarterly)

For a **complete kit audit**, run waves in order. Each wave is one PR theme (or one focused session). Do not start Wave 8 until Waves 1–7 have findings recorded in `usage/AUDIT_REPORT.md`.

**Tracking:** `usage/FIX_PLAN.md` (wave backlog + PR themes) · `usage/AUDIT_REPORT.md` (findings + wave status).

| Wave | Focus | Playbook steps | Primary inputs | Exit criteria |
| --- | --- | --- | --- | --- |
| **0** | Baseline & scavenger | 1 | `README.md`, hub indexes, `kit-manifest.yml` | Scavenger table complete; wave status table opened in `AUDIT_REPORT.md` |
| **1** | Level taxonomy (G vs CM) | 2 | `ADAPTIVE_GOVERNANCE.md`, `CI_MINIMUM_ADOPTION.md`, `ADOPTION_ENFORCEMENT_CONTRACT.md`, `TERMINOLOGY_GLOSSARY.md` | Two named scales documented; no bare `L0`–`L3` in normative paths without qualifier |
| **2** | Gate × maturity alignment | 2, 3 | `ci/*_GATES.md`, `ENFORCEMENT_MATRIX.md`, `ADOPTION_ENFORCEMENT_CONTRACT.md` | Single mapping table: gate ID → CM level → adopter default; `ci/` level numbers cross-reference G or CM explicitly |
| **3** | Bundle & import graph | 2, 3 | `kit-manifest.yml`, `ADOPTION_BUNDLES.md`, `AGENTS.md`, `.github/copilot-instructions.md`, `doc-hygiene.yml` | Every path referenced from a bundle entry file exists in that bundle (or marked upstream-only) |
| **4** | Agent projections parity | 2 | `AGENTS.md`, `.github/copilot-instructions.md`, `AI_ENFORCEMENT_DAILY.md` | Quick rules + COMPLIANCE footer aligned; bundle-aware “skip if not imported” where needed |
| **5** | Enforceability & dogfooding | 3, 5 | Kit workflows (`.github/workflows/`), `RELEASE_READINESS.md`, `LOCAL_OVERLAY_TEMPLATE.md` | Kit-only CI exceptions documented; red-team scenarios updated |
| **6** | Theory & architecture corpus | 4 | `architecture/README.md`, framework, style matrix, taxonomy, selected `architecture/rag/` | Theory-bridge gaps listed or closed; taxonomy coverage notes current |
| **7** | Red-team retest | 5 | Prior findings + bypass table in `AUDIT_REPORT.md` | ≥3 drift scenarios with status; no open **High** findings |
| **8** | Release closure | 1–5 (light) | `RELEASE_READINESS.md`, `CHANGELOG.md`, `VERSIONING.md` | Audit clean; changelog section cut; mapping table updated |

### Wave timeboxes (suggested)

| Wave | Maintainer session | Reviewer pass |
| --- | --- | --- |
| 0 | 30 min | — |
| 1–2 | 60–90 min each | 30 min |
| 3–4 | 45–60 min each | 20 min |
| 5 | 60 min | 30 min |
| 6 | 90 min (corpus budget: max 3 RAG notes + framework) | 30 min |
| 7 | 45 min | 20 min |
| 8 | 30 min | sign-off |

### Wave dependencies

```text
0 → 1 → 2 → 3 → 4
         ↘     ↓
           5 ← ┘
           ↓
           6 → 7 → 8
```

- **Wave 1 blocks Wave 2:** gate “level” columns cannot be reconciled until G vs CM naming exists.
- **Wave 3 can parallel Wave 2** only for non-overlapping files; prefer sequential to avoid merge conflicts.
- **Wave 8** requires `RELEASE_READINESS.md` precondition “Audit clean”.

### Coverage per wave

For each wave, record examined paths, checks/scenarios, evidence, limitations, and findings (including “none found”). Severity follows impact and evidence. Do not set a minimum number or severity of findings per wave. Unexamined areas must be marked as such; a scoped audit does not establish release readiness.

## Recommended Roles (Best Results)
- **Architecture reviewer**: boundaries, hybridization, trade-offs
- **Test/quality reviewer**: determinism, CI gates, evidence quality
- **Security reviewer**: trust boundaries, authn/authz vocabulary, threat modeling assumptions

## Audit Inputs (Start Here)
Mandatory:
- `README.md`
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
- `architecture/README.md`
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/ARCHITECTURE_STYLE_MATRIX.md`
- `architecture/rag/README.md`
- `kit-manifest.yml` and `usage/ADOPTION_BUNDLES.md` (if bundles are in scope)

Optional (if relevant):
- `interface/INTERFACE_RULES_PROPOSAL.md`, `interface/INTERFACE_CI_GATES.md`
- `ci/*_GATES.md`
- `adr/ADR_TEMPLATE.md`
- `research/PROFESSIONAL_STANDARDS_AND_REFERENCES.md`

## Procedure (90 Minutes, Repeatable)
### Step 1 — Scavenger Test (Findability)
Timebox: 10 minutes.

Tasks (each must be findable in < 60 seconds):
- What to do for a high-risk boundary/contract change?
- Where is the ADR template and what must it contain?
- Where is hybrid architecture guidance?
- Where is schema evolution/versioning guidance?
- Where are non-interactive/timeout expectations?

Output:
- “Found / Not found” per item + exact path(s) + what was confusing.

### Step 2 — Consistency Scan (Contradictions & Duplication)
Timebox: 20 minutes.

Look for:
- the same rule expressed differently in multiple places
- the same topic “owned” by multiple docs
- conflicting terms (e.g., “model”, “interface”, “core”)

Output:
- list of duplicate/conflicting statements (with exact locations)
- recommended canonical location (single source of truth)

### Step 3 — Enforceability Review (Can This Be Policed?)
Timebox: 20 minutes.

For each normative rule, answer:
- can we detect violations via CI or review?
- what evidence is required in a PR?
- what are common bypass paths?

Output:
- 3–5 rules that are “normative but unenforceable” today
- proposed enforcement mechanism (CI gate / PR template / ADR requirement)

### Step 4 — Theory Validation (Professional Alignment)
Timebox: 20 minutes.

Use the framework as a checklist:
- Are quality attributes expressed as measurable scenarios?
- Are trade-offs explicit (ATAM-lite)?
- Are sensitivity points and risks recorded?
- Are hybrid boundaries explicit?

Output:
- missing “theory bridge” items (scenario → tactic → architecture → enforcement)

### Step 5 — Red-Team Drift Scenarios (Break It)
Timebox: 20 minutes.

Write 3 realistic scenarios:
- “We used AI and shipped something that looks compliant but isn’t.”

Examples:
- a new integration bypasses boundary contracts (ports/interfaces) under time pressure
- tests exist but are flaky/non-deterministic
- docs drift because multiple files describe the same behavior

Output:
- scenario description
- how it slips through
- the smallest fix to prevent it next time

## Findings Format (Hard Requirement)
Use this exact template for each finding:

- **ID**: A-01
- **Severity**: High / Medium / Low
- **Category**: findability / contradiction / duplication / enforceability / theory / security / interface
- **Evidence**: path + quoted sentence(s)
- **Impact**: what breaks or drifts
- **Fix proposal**: exact doc change (where + what)
- **Verification**: how we know the fix worked

## AI-Assisted Audit Prompt (If You Use an LLM)

Paste this (then provide repo docs as context):

```
Role: Strict governance reviewer.
Load usage/AUDIT_PLAYBOOK.md.

Step 0 — Scope triage (mandatory):
- Pick scope: post_import | prefix | release | quarterly
- State which procedure steps and input subset apply (see Audit scope triage table)
- Do not load full mandatory inputs unless scope requires it

Goal: Find contradictions, duplication, unenforceable rules, missing theory support (within scope).

Constraints:
- Propose minimal diffs; prefer consolidating into existing docs.
- Use the Findings Format from the playbook.
- Record coverage and evidence for the chosen scope; report only substantiated findings. Zero findings is allowed.
- Include drift/bypass scenarios: 3 for release/quarterly; 1 for post_import/prefix.

Output: AUDIT_REPORT findings + FIX_PLAN (top fixes ordered by severity).
```

## Output Deliverables
- Suggested deliverables (create in your repo as needed):
  - AUDIT_REPORT.md (findings list + wave status table)
  - FIX_PLAN.md (wave backlog + top fixes ordered by severity)
- For **release/quarterly** scope, use **Full audit waves** above (Waves 0–8).
- One PR per fix theme (keep diffs small)
