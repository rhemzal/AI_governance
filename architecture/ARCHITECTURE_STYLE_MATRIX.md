# Architecture Style Matrix (Trade-Off Map)

## Purpose
This matrix is a **trade-off map**, not dogma.
It supports the `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`.

Legend:
- ✅ Strong fit
- ⚠️ Possible, but watch the trade-offs
- ❌ Usually a mismatch

| Criterion / Goal | Hexagonal (Ports & Adapters) | Layered | Modular Monolith | Event-Driven | Microservices | Pipeline/Batch |
|---|---:|---:|---:|---:|---:|---:|
| Stable domain rules | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ | ❌ |
| Many external integrations | ✅ | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ |
| Automation-first testability | ✅ | ⚠️ | ✅ | ⚠️ | ❌ | ⚠️ |
| Determinism by design | ✅ | ⚠️ | ✅ | ❌ (harder) | ❌ (harder) | ⚠️ |
| Simple CRUD (Create, Read, Update, Delete) / data-first | ⚠️ | ✅ | ✅ | ⚠️ | ❌ | ⚠️ |
| High throughput streaming | ⚠️ | ❌ | ⚠️ | ✅ | ✅ | ✅ |
| Low cognitive load for small teams | ⚠️ | ✅ | ✅ | ❌ | ❌ | ⚠️ |
| Clear failure isolation boundaries | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ |

## Notes (Failure Modes)
- Hexagonal fails when you pretend a system is domain-centric but it is actually data/query-centric.
- Event-driven fails when observability, ordering, and consistency requirements are underestimated.
- Layered fails when “layers” become a dumping ground and boundaries are not enforced.
- Pipelines fail when they accidentally evolve into distributed stateful systems without explicit coordination.

## Quick Guidance (Choose / Avoid)
Use this as a fast sanity check before writing an ADR.

- Hexagonal: choose for domain-centric + lots of volatility at edges; avoid for simple CRUD/data-first where the “domain” is thin.
- Layered: choose for simple teams and straightforward apps; avoid if you cannot enforce boundaries.
- Modular monolith: choose when you want strong boundaries without distributed ops; avoid if you need independent deploy/scaling now.
- Event-driven: choose for async workflows + decoupled integration; avoid if you can’t invest in observability/versioning/idempotency.
- Microservices: choose only with ops maturity + stable boundaries; avoid if you risk a distributed monolith.

## Hybridization Guidance (Keep It Intentional)
Most systems are hybrids.

This section is a **summary** to support fast scanning.
Canonical hybridization rules and required ADR fields live in:
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` (section “Hybrid Architectures”)

The professional move is to make the hybrid explicit:
- pick a dominant style per bounded context/module
- define where the secondary pattern applies (boundary)
- name the main new risks (versioning, observability, operational load)

Common hybrids that often work:
- Modular monolith + boundary contracts (ports/interfaces) and integration adapters at volatile edges
- Layered core + boundary contracts (ports/interfaces) for integrations
- Event-driven between contexts + state model inside contexts

Hybrids that often fail without strong governance:
- Microservices + shared DB tables/ownership
- Event-driven + no schema evolution policy
- CQRS everywhere (projection sprawl)

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/rag/QUALITY_ATTRIBUTES.md`
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`
- `architecture/rag/DISTRIBUTED_MONOLITH.md`
- `architecture/rag/HEXAGONAL_RATIONALE_AND_FAILURE_MODES.md`
- `architecture/rag/LAYERED_RATIONALE_AND_FAILURE_MODES.md`
- `architecture/rag/EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md`
- `architecture/rag/MODULAR_MONOLITH.md`
- `architecture/rag/MICROSERVICES_WHEN_NOT_TO.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`

