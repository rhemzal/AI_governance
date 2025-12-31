# Interface Development Rules — General AI Alignment Proposal

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
This is a **project-agnostic**, English-only proposal of rules for any **Interface layer**, including:
- Graphical UIs (GUI)
- Command-line interfaces (CLI)
- Text/terminal interfaces (TUI)
- Headless operator/control interfaces

These rules are intended for AI-assisted development. The AI must **compare and integrate** these rules with an existing project’s rules and documentation.

## Instruction to the AI Assistant
You are given this document as a general proposal.

Your task:
1. Compare these rules with the project’s existing rules and documentation.
2. Identify overlaps, conflicts, and gaps.
3. Propose a merged, conflict-free rule set.
4. Do not silently override existing constraints.
5. Do not generate interface code until alignment is complete and reported.

## 1. Architectural Position
### 1.1 Interface Is Not a Domain Owner
- The interface MUST NOT own business rules.
- The interface MUST NOT redefine domain behavior.

### 1.2 Interface as an Adapter
- Treat the interface as an integration boundary (an adapter/edge layer).
- The interface communicates only through defined boundary contracts (ports/interfaces/APIs).

## 2. Responsibility & Scope
### 2.1 Minimal Responsibility
- Each interface component/command MUST have one clear responsibility.
- Avoid “smart” multi-purpose components or commands.

### 2.2 Explicit State Ownership
- Interface state MUST be explicit and predictable.
- Shared/global state MUST be justified and documented.

## 3. Interaction Flow & Behavior
### 3.1 Predictable Interaction
- Prefer explicit, predictable interaction flows.
- Avoid hidden bidirectional mutations.

### 3.2 Determinism
- Given the same inputs, the interface MUST produce the same output.
- Time/random/environment/I/O MUST be injected.

### 3.3 Headless & Automated Execution (MANDATORY)
- Core interface behavior MUST be executable without human interaction.
- Human input is an adapter, not a requirement.
- No mandatory prompts, blocking reads, or interactive pauses in core logic.

## 4. Error Handling & Operator Feedback
### 4.1 Explicit States
Interfaces MUST explicitly represent:
- waiting/loading
- empty/no-result
- error/failure
- success/completion

Silent failures are forbidden.

### 4.2 Failure Isolation
Interface failures MUST NOT cascade into backend/system instability.

## 5. Terminology & Semantics
### 5.1 Domain Language
- Interface terminology MUST match the domain language.
- Do not introduce synonyms for existing concepts.

### 5.2 Semantic Consistency
- The same concept MUST behave consistently across the interface.

## 6. Testability, Automation & Autonomy
### 6.1 Automation-First
- All interface behavior MUST be triggerable programmatically.
- Manual interaction MUST NOT be required for core functionality.

### 6.2 Deterministic & Machine-Readable Output
- Output MUST be deterministic.
- Prefer structured, machine-readable outputs where applicable.
- Free-form text MUST NOT be the only machine-consumable signal.

### 6.3 No Test, No Behavior
- Any non-trivial interface behavior MUST be covered by tests.

### 6.4 GUI Verification (When a Human UI Exists)
If the interface includes a GUI (web/desktop/mobile):
- Changes MUST be verifiable without manual-only review.
- Prefer automated UI checks that validate what a human sees:
  - screenshot/visual regression tests (image diff), and/or
  - accessibility/DOM snapshots.

If the correctness depends on **exact visible text** (receipts, confirmations, compliance text):
- add an automated check that verifies rendered text (e.g., OCR on screenshots or equivalent).

## 7. Performance as a Contract
- Interface operations MUST have predictable performance characteristics.
- Long-running operations MUST expose progress/status.
- Blocking behavior MUST be explicit and justified.

## 8. Cognitive Load & Maintainability
- Prefer readability over cleverness.
- Use predictable structure and naming.

## 9. Mandatory AI Behavior
When working on interface code, the AI MUST:
- reference existing project rules/docs
- identify conflicts with this proposal
- propose a merged rule set
- reject designs requiring human interaction for core behavior
- state which rules are adopted/adapted/rejected

## 10. Required Output Format
# INTERFACE RULES ALIGNMENT REPORT
- Existing rules reviewed: yes/no
- Conflicts found: yes/no
- Integrated rules:
  - proposal-rule → existing-doc
- New rules proposed:
- Rules rejected (with justification):
- Final recommendation: ACCEPT / ADAPT / REJECT

## Related Documents
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md` and `constitution/AI_ENFORCEMENT_DAILY.md`
- `adr/ADR_0001_Automation_First_Interfaces.md`
- `interface/INTERFACE_CI_GATES.md` and `ci/INTERFACE_GATES.md`
- `ci/TEST_GATES.md`
