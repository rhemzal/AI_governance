# State vs. Event Model — Advisory Note

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._


## Core Idea
- State model stores current truth.
- Event model stores facts over time; state is derived.

## What Events Buy You
- auditability
- temporal queries
- integration via facts

## What Events Cost
- schema evolution complexity
- replay/projection complexity
- consistency/ordering complexity

## When This Fails / Failure Modes
- You need simple transactional updates but choose events for “coolness”.
- You cannot operate projections reliably.
- You underestimate data migration and versioning.

## Heuristics
- Use events when auditability and temporal reasoning are real requirements.
- Otherwise start with state and introduce events surgically.
