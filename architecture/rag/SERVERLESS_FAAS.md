# Serverless / FaaS — Advisory Note (Entry Point)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Coverage Level
**Advisory** — The kit's boundary model applies and the trade-off matrix includes a Serverless/FaaS column. Provider-specific enforcement (Lambda, Cloud Functions, Azure Functions) and deployment tooling are out of scope.

## Core Idea
Functions-as-a-Service (FaaS) is a deployment topology where code is packaged as **individual functions** that are invoked by events (HTTP, queues, timers, storage triggers) and managed entirely by the cloud provider. Infrastructure provisioning, scaling, and runtime lifecycle are invisible to the developer.

The defining characteristic is that the **deployment unit is a function**, not a service or application.

## Why Teams Choose It
- Zero infrastructure management; scales to zero cost when idle.
- Natural event-driven integration: functions are triggered by events.
- Fine-grained pay-per-use billing.
- Fast iteration for glue logic and integration workflows.

## When to Choose It
- Workloads are event-triggered and stateless (no need for in-memory state between invocations).
- Traffic is highly variable or bursty; scale-to-zero economics matter.
- Integration glue: connecting external services, processing queue messages, reacting to storage events.
- Short-lived operations with predictable completion times.

## When NOT to Choose It
- Long-running computations that exceed provider timeout limits (typically 15 minutes max).
- Workloads requiring persistent in-memory state between invocations.
- Systems where cold-start latency is unacceptable (e.g., synchronous, user-facing APIs with strict p99 targets).
- When portability and avoiding vendor lock-in outweigh operational simplicity.
- When local development and testing fidelity is critical: emulators frequently diverge from production behavior.

## Common Failure Modes
- **Function sprawl**: dozens or hundreds of functions with no coherent ownership or naming discipline — a distributed monolith at the function level.
- **Hidden coupling via shared state**: functions share state through DynamoDB, S3, or Redis, creating invisible coupling that is hard to test and reason about.
- **Cold start latency surprises**: latency spikes under intermittent load are accepted at design time and then cause SLA violations in production.
- **Vendor lock-in**: trigger bindings, SDK calls, and configuration are provider-specific; migrating away is expensive.
- **Testing gap**: local emulation (LocalStack, SAM CLI, Functions Core Tools) diverges from cloud behavior; integration gaps are only discovered in staging/prod.
- **Observability fragmentation**: each function emits logs/traces independently; without a unified observability strategy, tracing requests across functions is impractical.
- **Timeout-driven design**: logic is structured around provider timeout limits rather than domain requirements, leading to accidental complexity (e.g., chunking work to fit in 15 minutes).

## Heuristics
- Keep functions small and single-purpose; a function with multiple unrelated triggers is a coupling smell.
- Treat the event schema as a boundary contract — version it and validate it at the handler entry point.
- Isolate provider SDK calls in a thin adapter layer; keep business logic in pure, testable functions.
- Define an explicit observability strategy (correlation IDs, structured logging, distributed tracing) before shipping to production.
- Test business logic independently of the FaaS runtime; use the provider runtime only for integration tests.

## How This Kit's Boundary Model Applies
The kit's core boundary model (`AI_RULES.md` §1) maps cleanly onto serverless:
- **Core** = pure business logic (deterministic, no I/O, no SDK dependencies).
- **Boundary contracts** = event schemas (the "port" into the function).
- **Integration boundaries** = provider-specific handler/trigger code and SDK calls.

The function handler is an adapter: it receives the provider event, translates it to a domain input, calls core logic, and returns a provider-shaped response.

## Entry Points in This Kit
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` §1 — integration-centric and deployment-topology-centric axes
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` §4 — failure zones (timeout, cold start, shared state)
- `architecture/SOLUTION_CLASS_TAXONOMY.md` — coverage map

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- `architecture/rag/EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md`
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`
- `constitution/AI_RULES.md`
