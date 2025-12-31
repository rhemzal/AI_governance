# ADR 0001: Automation-First Interfaces

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status
Accepted

## Context
The project uses AI-assisted development and aims to maximize:
- autonomous programming
- automated testing
- deterministic behavior
- long-term maintainability

Traditional interaction-first assumptions (mandatory prompts, pause-driven flows) conflict with these goals.

## Decision
All interface layers (GUI/CLI/TUI/headless control layers) MUST follow an **Automation-First** design:
- core interface behavior MUST be executable without human input
- human interaction is treated as an adapter, not a requirement
- interface logic MUST be deterministic and scriptable

## Rationale
Automation-first:
- enables CI-level interface testing
- enables safer AI-driven refactoring
- reduces hidden interaction paths
- improves operability and debuggability

## Consequences
Positive:
- interfaces are testable in isolation
- shared interaction core is possible across CLI/UI
- CI becomes a true quality gate

Trade-offs:
- slightly more upfront design effort
- requires explicit modeling of interaction state

These trade-offs are accepted.

## Enforcement
Enforced by:
- `interface/INTERFACE_RULES_PROPOSAL.md`
- `interface/INTERFACE_CI_GATES.md`
- `constitution/AI_ENFORCEMENT.md`
