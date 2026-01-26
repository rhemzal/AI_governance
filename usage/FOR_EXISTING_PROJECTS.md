# Adopting This Kit in Existing Projects

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Step 1: Baseline Assessment
- Where are the boundaries today?
- What is the current test posture?
- Where does non-determinism enter the system?

## Step 2: Introduce Rules Without Big Refactors
- Add `constitution/` and align terminology.
- Add CI gates as warnings first (optional), then enforce.

Practical rule for early adoption: keep CI automation aligned with current project maturity.
- Prefer adding automated checks that can pass immediately (doc hygiene).
- If a gate’s prerequisites do not exist yet (no tests, no boundary tooling), keep the check informational/non-required or enforce it via PR checklist review until the prerequisites are in place.

## Step 3: Pay Down the Biggest Risks
Prioritize:
- hidden IO and global state
- lack of interface headless mode
- missing tests for critical flows

## Step 4: Record Decisions
Use ADRs for major changes so AI-assisted work stays consistent.

## Related Documents
- `constitution/AI_RULES.md` and `constitution/AI_ENFORCEMENT.md`
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `adr/ADR_TEMPLATE.md`
- `ci/ARCHITECTURE_GATES.md` and `ci/TEST_GATES.md`

