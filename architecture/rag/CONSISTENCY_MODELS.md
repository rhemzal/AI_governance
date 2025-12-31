# Consistency Models — Advisory Note

## Core Idea
Consistency is about **what other parts of the system can observe, and when**.

## Common Models
- **Strong consistency**: reads reflect the latest committed write (within the model’s scope).
- **Eventual consistency**: updates propagate; reads may be stale temporarily.

## When Eventual Consistency Hurts
- user workflows require immediate confirmation
- invariants span multiple entities/services
- financial/accounting-like correctness constraints

## Heuristics
- keep invariants within a single transactional boundary when possible
- if you accept eventual consistency, design UX and retries explicitly

## Related Documents
- `architecture/rag/EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md`
- `architecture/rag/CQRS_WHEN_AND_WHEN_NOT.md`
