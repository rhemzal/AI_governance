# Distributed Monolith — Advisory Note

## Core Idea
A system that is *distributed like microservices* (many deployables, network calls) but *coupled like a monolith* (tight runtime dependencies, shared releases in practice).

It combines:
- distributed-systems failure modes (latency, partial failure, retries)
with
- monolithic coupling (changes require coordinated deployments).

## Why It Happens
- microservices adopted before boundaries stabilize
- “services by org chart” rather than domain language
- shared database schemas or shared integration logic
- synchronous call chains replacing modular boundaries
- governance missing for contracts, versioning, and ownership

## Symptoms (Detect Early)
- frequent “deploy all services” releases
- changes require PRs across many repos/services
- long synchronous call chains (A→B→C→D)
- shared libraries that effectively act as a hidden monolith core
- shared database tables or cross-service joins
- incidents cascade across services

## Failure Modes
- **Latency amplification**: each hop adds tail latency.
- **Cascading failures**: partial outage propagates through dependencies.
- **Coupled releases**: coordination overhead becomes the real bottleneck.
- **Data ownership confusion**: nobody owns invariants; everyone patches.
- **Testing collapse**: integration/E2E becomes the only confidence signal.

## Heuristics (Practical)
### Prefer a modular monolith until proven otherwise
If you cannot demonstrate:
- stable bounded contexts
- clear data ownership
- operational maturity (observability, on-call)
then microservices are likely premature.

### If you already have many services, reduce coupling deliberately
- make dependencies explicit (service map, call graph)
- break synchronous chains; use async events where appropriate
- introduce strict API/event compatibility rules and schema evolution discipline
- eliminate shared database tables across services; define ownership

### Treat contracts as first-class
- version API/event schemas
- define deprecation policy
- require ADRs for breaking boundary changes

## Related Documents
- `architecture/rag/MICROSERVICES_WHEN_NOT_TO.md`
- `architecture/rag/MODULAR_MONOLITH.md`
- `architecture/rag/CONWAYS_LAW.md`
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`
- `ci/ARCHITECTURE_GATES.md`
