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
A good audit produces:
- at least 10 findings (incl. 3 high-severity)
- at least 5 specific fix proposals (exact docs/sections to change)
- at least 3 “bypass” scenarios (how teams could drift while appearing compliant)

## Recommended Roles (Best Results)
- **Architecture reviewer**: boundaries, hybridization, trade-offs
- **Test/quality reviewer**: determinism, CI gates, evidence quality
- **Security reviewer**: trust boundaries, authn/authz vocabulary, threat modeling assumptions

## Audit Inputs (Start Here)
Mandatory:
- `README.md`
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/ARCHITECTURE_STYLE_MATRIX.md`
- `architecture/rag/README.md`

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

- Role: You are a strict reviewer.
- Goal: find contradictions, duplication, unenforceable rules, missing theory support.
- Constraints: propose minimal diffs; do not invent new topics; prefer consolidating into existing docs.
- Output: at least 10 findings using the Findings Format above; include 3 drift/bypass scenarios.

## Output Deliverables
- Suggested deliverables (create in your repo as needed):
  - AUDIT_REPORT.md (findings list)
  - FIX_PLAN.md (top 5 fixes, ordered by severity)
- One PR per fix theme (keep diffs small)
