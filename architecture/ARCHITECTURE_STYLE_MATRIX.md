# Architecture Style Matrix (Trade-Off Map)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._


## Purpose
This matrix is a **trade-off map**, not dogma.
It supports the `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`.

Legend:
- ✅ Strong fit
- ⚠️ Possible, but watch the trade-offs
- ❌ Usually a mismatch

| Criterion / Goal | Hexagonal (Ports & Adapters) | Layered | Modular Monolith | Event-Driven | Microservices | Pipeline/Batch | Config-Driven Pipeline | Serverless/FaaS | Orchestration (Saga/Workflow) | CQRS | Streaming/Reactive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Stable domain rules | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ⚠️ | ⚠️ (write side only) | ❌ |
| Many external integrations | ✅ | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| Automation-first testability | ✅ | ⚠️ | ✅ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Determinism by design | ✅ | ⚠️ | ✅ | ❌ (harder) | ❌ (harder) | ⚠️ | ⚠️ | ❌ (stateless only) | ⚠️ | ⚠️ (eventual consistency) | ❌ (ordering/timing) |
| Simple CRUD (Create, Read, Update, Delete) / data-first | ⚠️ | ✅ | ✅ | ⚠️ | ❌ | ⚠️ | ❌ | ⚠️ | ❌ | ⚠️ (read side) | ❌ |
| High throughput streaming | ⚠️ | ❌ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ❌ | ❌ | ✅ |
| Low cognitive load for small teams | ⚠️ | ✅ | ✅ | ❌ | ❌ | ⚠️ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Clear failure isolation boundaries | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ (hidden coupling) | ⚠️ | ⚠️ | ⚠️ |
| Long-running workflows | ❌ | ❌ | ⚠️ | ⚠️ (choreography) | ⚠️ | ✅ | ⚠️ | ❌ (timeout limits) | ✅ | ❌ | ❌ |
| Platform extensibility (plugins) | ✅ (ports) | ❌ | ⚠️ | ❌ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Contract/schema is the product | ⚠️ | ❌ | ⚠️ | ⚠️ (event schema) | ⚠️ | ❌ | ❌ | ⚠️ | ❌ | ❌ | ⚠️ (stream schema) |

## Notes (Failure Modes)
- Hexagonal fails when you pretend a system is domain-centric but it is actually data/query-centric.
- Event-driven fails when observability, ordering, and consistency requirements are underestimated.
- Layered fails when “layers” become a dumping ground and boundaries are not enforced.
- Pipelines fail when they accidentally evolve into distributed stateful systems without explicit coordination.
- Config-driven pipelines fail when configuration grows into implicit code (Turing-complete YAML), when config schemas are not validated at load time, or when magic constructors hide tight coupling in declarative files.
- Serverless/FaaS fails when function sprawl creates a distributed monolith at the function level, when shared state (DynamoDB/S3) hides coupling between functions, and when cold-start latency or provider timeout limits are not accounted for in design. (See `architecture/rag/SERVERLESS_FAAS.md`.)
- Orchestration (Saga/Workflow) fails when the orchestrator becomes a single point of failure, when workflow versioning for in-flight instances is neglected, or when business logic leaks into the orchestration layer. (See `architecture/rag/ORCHESTRATION_SAGA_WORKFLOW.md`.)
- CQRS fails when applied to simple CRUD where a single model suffices, when projection maintenance overhead is underestimated, or when stale read-model data causes confusing user experiences without adequate staleness communication. (See `architecture/rag/CQRS_WHEN_AND_WHEN_NOT.md`.)
- Streaming/Reactive fails when backpressure is not explicitly designed for, when event-time vs. processing-time distinction is ignored (causing incorrect aggregations), or when stream record schema evolution is treated as less critical than API schema evolution. (See `architecture/rag/STREAMING_REACTIVE.md`.)

## Quick Guidance (Choose / Avoid)
Use this as a fast sanity check before writing an ADR.

- Hexagonal: choose for domain-centric + lots of volatility at edges; avoid for simple CRUD/data-first where the “domain” is thin.
- Layered: choose for simple teams and straightforward apps; avoid if you cannot enforce boundaries.
- Modular monolith: choose when you want strong boundaries without distributed ops; avoid if you need independent deploy/scaling now.
- Event-driven: choose for async workflows + decoupled integration; avoid if you can’t invest in observability/versioning/idempotency.
- Microservices: choose only with ops maturity + stable boundaries; avoid if you risk a distributed monolith.
- Config-driven pipeline: choose for AI/ML pipelines and data processing where topology/components are the primary decision axis; avoid when domain logic is complex, when config becomes Turing-complete, or when you need fine-grained code-level boundary enforcement.
- Serverless/FaaS: choose for stateless, event-triggered workloads with variable traffic where infrastructure management is a burden; avoid when cold-start latency is unacceptable, when state must persist in-memory, or when local testing fidelity is critical.
- Orchestration (Saga/Workflow): choose for long-running, reliable multi-step processes where explicit process visibility and compensation logic are required; avoid for high-throughput paths, simple single-service processes, or when choreography already meets the need.
- CQRS: choose when read and write patterns differ significantly and you need multiple specialized read views; avoid for simple CRUD, small teams without projection operation expertise, or when eventual consistency in read models is unacceptable.
- Streaming/Reactive: choose for high-throughput unbounded data streams requiring real-time or near-real-time processing with complex windowed aggregations; avoid when batch processing is sufficient, when the team lacks stream platform operational experience, or when exactly-once semantics cannot be guaranteed.

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
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- `architecture/rag/QUALITY_ATTRIBUTES.md`
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`
- `architecture/rag/DISTRIBUTED_MONOLITH.md`
- `architecture/rag/HEXAGONAL_RATIONALE_AND_FAILURE_MODES.md`
- `architecture/rag/LAYERED_RATIONALE_AND_FAILURE_MODES.md`
- `architecture/rag/EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md`
- `architecture/rag/MODULAR_MONOLITH.md`
- `architecture/rag/MICROSERVICES_WHEN_NOT_TO.md`
- `architecture/rag/CQRS_WHEN_AND_WHEN_NOT.md`
- `architecture/rag/STREAMING_REACTIVE.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`

