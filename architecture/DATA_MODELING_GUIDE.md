# Data Modeling Guide (Project-Agnostic)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._


## Purpose
This guide helps choose and communicate data modeling approaches and hybrids.
It is optimized for teams that want **clear trade-offs**, not theory-heavy jargon.

## 1) Decide What Your Model Optimizes For
Choose primary objective:
- Transactional correctness (invariants, atomic updates)
- Query flexibility (reporting, ad-hoc views)
- Auditability (traceability over time)
- Performance/latency
- Integration interoperability

## 2) Common Model Families
### 2.1 Rich Domain Model (Behavior-Centric)
- Model objects enforce invariants and encapsulate business behavior.
- Strong fit when domain rules are complex and stable.

**Typical failure**: over-modeling simple CRUD (Create, Read, Update, Delete); coupling domain types to persistence concerns.

### 2.2 Anemic Domain Model (Data-Centric)
- Domain objects mostly store data; behavior is in services.
- Can be acceptable for simple CRUD systems.

**Typical failure**: business rules scattered and duplicated; hard to enforce invariants.

### 2.3 State Model vs. Event Model
- **State model**: system-of-record stores current state.
- **Event model**: system-of-record stores events; current state is derived.

**Event model failure modes**:
- replays become expensive
- schema evolution is hard
- ordering/consistency become complex

### 2.4 Comparison Cheat Sheet (What to Choose, and Why Not)
This is a fast comparison to help explain decisions to humans and to the AI.

| Choice | Strong when | Watch out / Not suitable when |
|---|---|---|
| Rich domain model | invariants are complex; behavior is the product | simple CRUD; the team will fight the model; persistence leaks into domain |
| Anemic model | rules are thin; speed of delivery matters | rules grow and scatter; invariants become unenforced |
| State as system-of-record | you need simple transactions and immediate correctness | you need full audit trail/temporal queries as a first-class requirement |
| Events as system-of-record | auditability/temporal truth is required; async workflows dominate | you can’t operate projections/versioning; you need simple CRUD semantics |
| CQRS (Command Query Responsibility Segregation; separate read/write) | read model differs sharply from write invariants | you can’t accept stale reads; you can’t operate projections |

| Data store family | Strong when | Watch out / Not suitable when |
|---|---|---|
| Relational (SQL) | constraints, joins, transactions, strong consistency | extreme scale with simple access patterns only; operational constraints may dominate |
| Document | aggregate-oriented access; flexible schema evolution | heavy joins/relational queries; cross-document invariants |
| Key-value | very simple access patterns; caching/session-style data | you actually need query expressiveness |
| Graph | relationship/path queries dominate | simple entity CRUD; ops/tooling mismatch |
| Time-series | append-heavy metrics/events + windowed queries | transactional business invariants |

## 3) Hybrids (Common and Risky)
### 3.1 “Rich Domain + ORM (Object-Relational Mapper) as if it was free”
Risk: persistence leakage into domain.
Mitigation: persistence is an adapter; map domain to persistence models.

### 3.2 “Events for everything”
Risk: you build distributed systems complexity without the benefits.
Mitigation: use events where auditability/choreography are truly required.

### 3.3 “One model for writes and reads”
Risk: write invariants fight read/query performance.
Mitigation: separate write model from read projections when justified.

## 4) Mandatory Output When Proposing a Data Model
When proposing a data model, always state:
- invariants and where they are enforced
- source of truth (state vs. events)
- expected evolution points (schema changes)
- testing strategy (including determinism)

### 4.1 Communication Pattern (Reduce AI Confusion)
When discussing “models”, always disambiguate which model you mean:
- domain model (behavior + invariants)
- persistence model (tables/documents)
- read model (projections/views)

Ask the AI to restate your definitions before proposing changes.

## 5) Data Model Decision Record

When persistence or modeling is central, capture decisions in a short block (paste into an ADR or attach to `ARCHITECTURE DECISION PRECHECK` output). Not a separate ADR type — a consistent mini-template.

```text
DATA MODEL DECISION RECORD
- Domain model:
- Persistence model:
- Read model:
- System of record:
- Invariants:
- Schema evolution strategy:
- Migration / rollback:
- Testing strategy:
```

Fill each line explicitly; use `none` or `N/A` only when justified.

| Field | What to state |
|---|---|
| Domain model | Objects, behavior, where invariants live (rich vs anemic) |
| Persistence model | Tables, documents, events — how domain maps to storage |
| Read model | Projections, views, CQRS read side if any |
| System of record | State vs events; source of truth for each aggregate |
| Invariants | Rules and **where enforced** (domain, DB constraint, both) |
| Schema evolution strategy | Versioning, backward compatibility, expand-contract |
| Migration / rollback | How schema/data changes ship and revert |
| Testing strategy | Determinism, replay, fixture strategy, contract tests |

See also `architecture/rag/STATE_VS_EVENT_MODEL.md` and `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`.

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/ARCHITECTURE_DECISION_PROMPT.md`
- `architecture/rag/STATE_VS_EVENT_MODEL.md`
- `architecture/rag/MEASURED_PERFORMANCE.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`
- `constitution/AI_RULES.md`

