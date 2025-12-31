# CQRS (Command Query Responsibility Segregation) — When and When Not (Advisory)

## Core Idea
Separate write model (commands) from read model (queries).

## Why It Helps
- read side can be optimized independently (projections, denormalization)
- write side can focus on invariants and transactional correctness

## When to Choose It
- read/query patterns differ significantly from write invariants
- you need multiple specialized read views

## When NOT To Choose It
- simple CRUD (Create, Read, Update, Delete) with minimal read complexity
- team cannot operate projections or accept eventual consistency

## Failure Modes
- accidental complexity from maintaining two models
- stale reads and confusing user experience

## Related Documents
- `architecture/rag/STATE_VS_EVENT_MODEL.md`
- `architecture/DATA_MODELING_GUIDE.md`
