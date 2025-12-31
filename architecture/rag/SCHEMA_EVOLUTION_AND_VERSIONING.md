# Schema Evolution & Versioning — Advisory Note

## Core Idea
Systems live longer than their schemas.
Schema evolution is the discipline of changing:
- API contracts (request/response shapes)
- event schemas
- storage schemas (tables, documents, indexes)
without breaking consumers or corrupting meaning.

This note focuses on **practical versioning strategies** and **common failure modes**.

## When It Matters Most
- multiple consumers exist (services, jobs, BI, dashboards)
- you publish events or public APIs
- data must be retained for long periods
- you backfill/replay events
- your system is “automation-first” (machines depend on stable outputs)

## Failure Modes (Common)
- **Breaking change disguised as a refactor**: renamed/removed fields without migration.
- **Producer-first upgrades**: producers deploy new schema before consumers can handle it.
- **Consumer-first deadlock**: consumers wait on producers, producers wait on consumers.
- **Semantic drift**: field name stays the same but meaning changes (worst kind).
- **Dual-write inconsistency**: writing old+new shapes causes divergence.
- **Replay/backfill surprises**: old events cannot be interpreted by new code.
- **Schema sprawl**: too many versions with unclear support policy.

## Heuristics (Actionable)
### Prefer additive change
- Add new optional fields; do not remove fields immediately.
- Keep old fields until all consumers are migrated.
- Deprecate explicitly (docs + timelines).

### Be explicit about compatibility
Define compatibility per surface:
- **API contracts**: backward compatible for clients? forward compatible?
- **Event schemas**: can old consumers ignore new fields? can new consumers read old events?
- **Storage**: do old queries still work? are new writes readable by old code?

### Version at the boundary, not everywhere
- Prefer **schema/contract versioning** at public boundaries (API, events).
- Avoid versioning internal types unless there is a real independent consumer.

### Evolve with a two-phase rollout
Typical patterns:
- **Consumer-first**: deploy consumers that accept both old+new, then deploy producers.
- **Producer-first** (risky): only if consumers are already tolerant/forward-compatible.

### Maintain an explicit support policy
For each boundary:
- supported versions (N latest? time-based?)
- deprecation process
- ownership (who approves breaking changes)

### Treat semantics as part of the schema
- Document meaning, units, default values, and invariants.
- A compatible wire format with incompatible semantics is still a breaking change.

## Practical Patterns (Choose the Simplest That Works)
- **API**: semantic versioning for public APIs; additive fields; explicit deprecations.
- **Events**:
  - prefer additive fields + defaults
  - avoid renaming; add a new field and deprecate the old
  - if breaking change is unavoidable, publish a new event type/name
- **Database**:
  - expand/contract migrations
  - avoid long-running locks; migrate in small steps
  - consider backfill jobs with idempotency

## Related Documents
- `architecture/rag/CQRS_WHEN_AND_WHEN_NOT.md`
- `architecture/rag/CONSISTENCY_MODELS.md`
- `architecture/rag/STATE_VS_EVENT_MODEL.md`
- `architecture/rag/DATA_STORE_SELECTION.md`
- `ci/DOC_GATES.md`
