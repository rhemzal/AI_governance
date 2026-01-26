# AI_ENFORCEMENT — Enforcement Mechanisms for AI-Assisted Development

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This document defines mandatory enforcement mechanisms (“sticks”) used to ensure compliance with `constitution/AI_RULES.md`.

These mechanisms are **normative**.

## 0. Master Rule (Always)
Before doing anything:
1. Load and acknowledge `constitution/AI_RULES.md`.
2. Work strictly under these rules.
3. If any rule would be violated:
   - STOP
   - Report the violation
   - Propose a compliant alternative

Silent rule breaking is forbidden.

## 1. Permission-Based Changes (Hard Gate)
The AI MUST NOT change code, tests, or documentation until it completes an explicit compliance check.

Required pre-change statement:
- “Rules checked: …”
- “Violations found: yes/no”
- If yes: “STOP (needs refactor/approval)”

## 2. Fail-Fast Enforcement
If an architectural boundary violation is detected, the AI MUST abort the solution and report it.
No “workarounds” that ignore the rules.

## 2.1 Non-Interactive Commands & Timeouts (Hard Gate)
When the AI runs commands (tests, generators, linters, scripts):
- it MUST prefer non-interactive modes/flags
- it MUST NOT block on prompts
- it MUST time-bound long-running commands (wall-clock timeout)

If an interactive prompt is encountered, the AI MUST STOP and report:
- which command prompted
- the safest non-interactive alternative (flags/mode) if known
- what human decision/input is required (if unavoidable)

## 3. Architectural Boundary Lock
The AI MUST NOT reference outer-layer concepts/types when working on inner layers.
If needed, introduce a port.

## 4. Change Scope Lock
The AI MUST list all affected files and concepts.
If scope expands, the AI MUST stop and ask for confirmation.

## 4.1 Notes Protection (Hard Gate)
If any affected file matches `notes/**`:
- If the user did not explicitly ask to update notes: the AI MUST STOP and ask for explicit instruction.
- If the user asked to update notes: the AI SHOULD follow the working-notes policy (append/link rather than rewrite where feasible).

## 4.2 Language Guard (Hard Gate)
If a change affects canonical documentation paths (e.g., `constitution/**`, `ci/**`, `usage/**`, `adr/**`, `architecture/**`, root `README.md`, `.github/**` templates):
- the AI MUST produce English output by default.
- if the user requests non-English output for a canonical document, the AI MUST:
  - STOP and confirm the intent, and
  - redirect the change into `translations/<lang>/...` as a subordinate translation (unless the repository has an explicit local overlay that overrides this policy).

## 5. Test Gate (“No Test, No Code”)
No non-trivial change is accepted without:
- tests
- a statement of which layer the tests belong to
- justification why this is sufficient

## 6. Documentation Consistency Gate
If documentation changes:
- identify source of truth
- list other docs impacted
- propose deletions of outdated sections (not only additions)

If documentation is auto-generated (including AI-produced generation):
- the PR MUST state the regeneration process (command or procedure)
- the PR MUST avoid manual edits to generated outputs without updating the generator/source
- the AI MUST propose consolidation if the change introduces a new doc that overlaps existing topics

## 7. CI/CD Gates (Normative Expectation)
CI MUST be configured to fail on:
- architectural boundary violations
- missing tests for new behavior
- prohibited imports/calls (where applicable)
- documentation drift for changed public behaviors

Details live in:
- `ci/ARCHITECTURE_GATES.md`
- `ci/TEST_GATES.md`
- `ci/INTERFACE_GATES.md` and `interface/INTERFACE_CI_GATES.md`
- `ci/DOC_GATES.md`

## 8. Required Output (Hard Requirement)
Every AI response that proposes or performs changes MUST end with:

## COMPLIANCE REPORT
- AI_RULES loaded: yes/no
- Areas checked: architecture / code / tests / docs / CI
- Violations found: yes/no
- If yes: rule-id + location + reason
- Risk level: low / medium / high
- Decision: ACCEPT / REJECT / NEEDS REFACTOR

If this block is missing, the output is considered invalid.

## 9. Meta Rule (Anti-Authority)
The AI MUST NOT claim “best practices” unless:
- derived from project rules and documents, or
- explicitly marked as external, non-binding opinion.

## Related Documents
- `constitution/AI_RULES.md`
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `adr/ADR_0002_Architecture_Is_Contextual.md`
- `adr/ADR_0003_RAG_Is_Advisory_Not_Normative.md`
