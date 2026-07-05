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

## 1.1 Pre-Execution Plan (Hard Gate)
For changes spanning 2+ files or crossing code + tests + documentation:
- The AI MUST produce an Autonomous Execution Plan (AEP) before any edits.
- The AEP MUST declare `AEP Status: READY | BLOCKED`.
- If BLOCKED: the AI MUST list blocking items and STOP.
- If READY: the AI MUST be able to execute all steps without further operator input.
- An AEP with "TBD" steps, unresolved dependencies, or vague actions MUST NOT be declared READY.

For trivial single-file edits: the existing compliance check (Section 1) is sufficient.

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

## 4.3 Structural Scope Guard (Hard Gate)
If a proposed change includes structural work (module extraction, file reorganisation, bulk renaming, build-graph restructuring, or cross-cutting refactoring) that was NOT listed in the original scope:
- The AI MUST STOP.
- The AI MUST report: "Structural scope expansion detected — [description of structural change]."
- The AI MUST propose the minimal-structural-impact alternative first.
- The AI MUST NOT proceed with the structural expansion without explicit operator confirmation.

If the operator confirms, the AI MUST declare the expanded structural scope before any edits (see Section 1.1 AEP requirement).

## 4.4 Terminology Check (Hard Gate)
Before introducing or using an acronym in governance, architecture, CI/CD, testing, or AI workflow documents, the AI MUST check whether the term already exists in `architecture/TERMINOLOGY_GLOSSARY.md`.

If the acronym is ambiguous or overloaded:
- expand it on first use
- avoid using it as the primary term
- mark project-local terms explicitly (with definition)

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

## 10. Adaptive Governance Check

Before recommending or adding CI/CD, ADR requirements, documentation processes, or any enforcement mechanism, the AI assistant MUST answer the following questions:

1. What is the current project maturity level?
2. What concrete risk is this process or gate mitigating?
3. Is the proposed gate required now, or can it be deferred?
4. Is local verification sufficient?
5. What is the maintenance cost of this process?
6. What is the simplest useful enforcement mechanism?

Every response that proposes, recommends, or adds CI/CD, enforcement mechanisms, documentation processes, ADRs, or workflow requirements MUST include this output block exactly:

```
GOVERNANCE FIT CHECK
- Project stage: exploration / solo prototype / serious solo / shared / production
- Recommended enforcement level: 0 / 1 / 2 / 3 / 4
- CI/CD needed now: yes / no / partial
- Reason:
- What to defer:
```

If this block is missing from a response that proposes governance or process changes, the response is considered non-compliant.

The AI assistant MUST NOT recommend enterprise-grade CI/CD, PR workflows, or release governance for solo or early-stage projects unless the risk clearly justifies it.

See `constitution/ADAPTIVE_GOVERNANCE.md` for the full governance level definitions and anti-overengineering rules.

## 11. Playbook Adaptation Check

Before importing any practice from an external engineering playbook, the AI MUST complete this check:

```
PLAYBOOK ADAPTATION CHECK
- Source practice:
- Underlying principle:
- Is this a principle or a process?
- Minimum project level where it applies:
- Risk mitigated:
- Maintenance cost:
- Adopt / adapt / defer / reject:
```

If the check recommends **adopt** or **adapt**, the AI MUST also include the GOVERNANCE FIT CHECK (Section 10) when proposing any new process, gate, or enforcement mechanism.

Research and adaptation references (non-normative): `research/RESEARCH_ENGINEERING_PLAYBOOKS.md`, `research/PLAYBOOK_ADAPTATION_GUIDE.md`.

## Related Documents
- `constitution/AI_RULES.md`
- `constitution/ADAPTIVE_GOVERNANCE.md`
- `research/RESEARCH_ENGINEERING_PLAYBOOKS.md`
- `research/PLAYBOOK_ADAPTATION_GUIDE.md`
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `adr/ADR_0002_Architecture_Is_Contextual.md`
- `adr/ADR_0003_RAG_Is_Advisory_Not_Normative.md`
