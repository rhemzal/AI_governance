# Event-Driven Architecture — Rationale and Failure Modes (Advisory)

## Core Idea
Components communicate via events (facts) instead of direct calls.

## Why It Helps
- loose coupling between producers and consumers
- supports async processing and scalability
- enables integration via published facts

## When to Choose It
- asynchronous workflows dominate
- you need decoupled integrations
- you can invest in observability and operational discipline

## Common Failure Modes
- hidden coupling via event schemas and ordering assumptions
- hard debugging without traces and correlation IDs
- consistency surprises (eventual consistency)
- duplicated business logic across consumers

## Heuristics
- define event ownership and versioning rules
- require idempotent consumers
- treat “exactly once” as rare and expensive

## Related Documents
- `architecture/rag/STATE_VS_EVENT_MODEL.md`
- `architecture/rag/QUALITY_ATTRIBUTES.md`
