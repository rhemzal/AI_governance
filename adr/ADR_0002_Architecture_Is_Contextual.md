# ADR 0002: Architecture Is Contextual (No Default Style)

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status
Accepted

## Context
AI assistants often propose a single “best practice” architecture as a default.
In reality, architectural styles are sets of trade-offs.

This repository aims to:
- make architectural choices explicit
- highlight trade-offs and failure modes
- prevent cargo-cult adoption

## Decision
There is **no default architecture style**.

Any architecture recommendation MUST:
1. Use `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`.
2. Record the decision in an ADR.
3. Explicitly name trade-offs, failure modes, and points of no return.

## Consequences
- We spend a small amount of time up front to avoid irreversible mistakes.
- AI is required to slow down at architectural decision points.

## Enforcement
- PRs that introduce architecture-wide changes MUST include an ADR.
- CI should require ADR presence for changes that touch core boundaries.
