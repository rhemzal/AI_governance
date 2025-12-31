# Interface CI Gates — Automation-First Enforcement

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
This document defines **CI/CD gates** for the Interface layer (GUI/CLI/TUI/headless interfaces).

Goal:
- automation-first execution
- testability without human input
- determinism and scriptability
- prevention of architectural leakage

These gates are **normative expectations** for governed projects.

## 1. Mandatory Human-Interaction Constraints
### 1.1 No Mandatory Human Interaction
CI MUST FAIL if:
- core logic requires stdin/user input
- blocking prompts exist in production code paths
- interactive pauses are required to proceed

Examples of forbidden patterns:
- direct `readLine()` / `input()` / `prompt()` in core paths
- UI event handlers containing business logic
- CLI commands that cannot be executed non-interactively

### 1.2 Headless Execution Required
CI MUST VERIFY:
- interface behavior can run headlessly (no human interaction)
- interaction is an adapter around callable core logic

## 2. Determinism & Output Enforcement
### 2.1 Deterministic Behavior
CI MUST FAIL if:
- output depends on implicit time/randomness/environment
- identical inputs produce different outputs

Recommended checks:
- golden/snapshot tests
- deterministic execution tests

### 2.2 Machine-Readable Signals
CI SHOULD ENFORCE:
- structured output for CLI/automation paths (e.g., JSON)
- exit codes or structured status signals

CI MUST FAIL if:
- success/failure is only detectable via free-form text parsing

## 3. Test Enforcement
### 3.1 Automation-Only Tests
CI MUST FAIL if:
- interface tests require manual steps
- tests require real user interaction

### 3.2 No Test, No Behavior
CI MUST FAIL if:
- new interface behavior has no tests

### 3.3 Boundary-Safe Tests
CI MUST FAIL if:
- tests cross forbidden architectural boundaries

### 3.4 GUI Visual Verification (If Applicable)
If the project has a GUI interface, CI MUST FAIL if:
- GUI behavior changes without any automated verification of rendered output.

Accepted evidence (choose the simplest that fits):
- screenshot/visual regression tests (image diff)
- accessibility tree snapshots
- DOM snapshot tests

If correctness depends on exact visible text, CI SHOULD include a rendered-text verification step
(e.g., OCR on screenshots or equivalent).

## 4. Performance & Blocking Rules
### 4.1 Blocking Disclosure
CI MUST FAIL if:
- blocking operations are undocumented
- long-running operations expose no progress/status

### 4.2 Regression Detection (Recommended)
CI SHOULD:
- benchmark key interface operations
- detect regressions against a baseline

## 5. Architectural Boundary Gates
CI MUST FAIL if:
- interface imports domain internals (bypassing boundary contracts)
- interface contains business rules

## Final Rule
If an interface cannot be:
- executed headlessly
- tested automatically
- reasoned about deterministically

it must not be merged.

## Related Documents
- `interface/INTERFACE_RULES_PROPOSAL.md`
- `adr/ADR_0001_Automation_First_Interfaces.md`
- `constitution/AI_RULES.md` and `constitution/AI_ENFORCEMENT.md`
- `ci/INTERFACE_GATES.md`
- `ci/TEST_GATES.md`
