# Data Store Selection — Advisory Note

## Purpose
Help decide between relational/document/key-value/graph/time-series stores.

## Heuristic Map
- **Relational (SQL)**: strong consistency, joins, transactions, constraints.
- **Document**: flexible schema, aggregate-oriented reads/writes.
- **Key-value**: very fast simple access patterns; limited query expressiveness.
- **Graph**: relationship-heavy queries (paths, traversals).
- **Time-series**: append-heavy metrics/events with windowed queries.

## Failure Modes
- choosing based on novelty instead of access patterns
- forcing relational joins onto document stores or vice versa
- skipping operational cost evaluation

## Mandatory Inputs Before Deciding
- top 5 access patterns (reads/writes)
- consistency needs
- growth and retention expectations
- operational constraints

## Related Documents
- `architecture/DATA_MODELING_GUIDE.md`
- `architecture/rag/MEASURED_PERFORMANCE.md`
