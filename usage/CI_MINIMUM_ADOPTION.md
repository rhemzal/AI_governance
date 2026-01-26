# CI Minimum Adoption (Start Small, Stay Enforceable)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This kit provides CI gates as **principles** (not tool-specific implementations).
If you are adopting the kit in an existing repo, you can start with a minimal set of checks that produces immediate governance value.

## Minimum Viable CI (Recommended Order)

### Step 1 — Doc Hygiene Gate (Fast)
Goal: prevent documentation drift and broken references.
- Run `scripts/audit-docs.ps1 -FailOnWarning` in CI.
- Make the job required on PRs.

Why first: it is deterministic, fast, and enforces “single source of truth” behavior.

### Step 2 — Determinism / Non-Interactive Gate (Fast)
Goal: avoid human-in-the-loop tests and flaky pipelines.
- Enforce `ci/TEST_GATES.md` Gate T1 (headless, deterministic tests).
- Add timeouts to test execution.

Why second: it directly supports AI-heavy iteration and reduces “rerun until green”.

### Step 3 — Boundary Integrity Gate (Incremental)
Goal: stop architectural erosion early.
- Enforce `ci/ARCHITECTURE_GATES.md` Gate A1 (boundary integrity).
- Start with the simplest mechanism your stack supports:
  - import allow/deny lists
  - dependency graph checks
  - static analysis rules

Why third: it’s highly valuable, but language/tooling dependent.

## What to Do If You Have No CI Yet
- Apply the same gates as PR checklist items (human review) until CI exists.
- Do not weaken the rules; only change the enforcement mechanism.
  - Note: this is a temporary enforcement mode (human-review fallback). Governance stays normative; the target state is CI-backed enforcement.

## Related Documents
- `scripts/audit-docs.ps1`
- `ci/DOC_GATES.md`
- `ci/TEST_GATES.md`
- `ci/ARCHITECTURE_GATES.md`
- `constitution/AI_ENFORCEMENT.md`
