# Orchestration-Centric Architecture (Saga / Workflow Engine) — Advisory Note (Entry Point)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Coverage Level
**Advisory** — Complementary to event-driven choreography, which this kit already covers. The trade-off matrix includes an Orchestration (Saga/Workflow) column. Workflow engine specifics (Temporal, Conductor, AWS Step Functions, Airflow) are out of scope.

## Core Idea
Orchestration-centric architecture uses a **central coordinator** (workflow engine or saga orchestrator) to manage multi-step processes. The orchestrator explicitly invokes each step, handles failures, manages retries, and tracks state.

This is the **complement and contrast** to event-driven choreography:
- **Choreography** (event-driven): components react to events; no central coordinator; decoupled but emergent behavior.
- **Orchestration**: a central coordinator owns the process definition, invokes steps, and manages compensation on failure.

## Why Teams Choose It
- Long-running processes that span multiple services and must be reliable (e.g., order fulfillment, loan approval, data migration).
- Explicit visibility: the workflow definition IS the process; easy to audit and understand the happy path and compensating actions.
- Built-in retry, timeout, and compensation (saga pattern): no need to hand-roll distributed transaction recovery.
- Easier to test individual steps in isolation: each step is a discrete, callable unit.

## When to Choose It
- Processes that must complete reliably across multiple services over minutes, hours, or days.
- Business processes where compensation (rollback equivalent) logic is required (saga pattern).
- Teams that prefer explicit process visibility over emergent choreography behavior.
- When debugging distributed workflows is a high priority (orchestration provides a central audit log).

## When NOT to Choose It
- Simple, single-service processes: orchestration adds complexity without benefit.
- High-throughput, low-latency paths: orchestrators add overhead and are not optimized for sub-millisecond calls.
- When the team cannot operate and monitor the orchestrator as infrastructure.
- When event-driven choreography already solves the problem with acceptable observability.

## Common Failure Modes
- **Orchestrator SPOF (Single Point of Failure)**: if the orchestrator is unavailable, all in-flight workflows stall; high availability and persistence of workflow state are non-negotiable.
- **Workflow versioning / migration**: changing the definition of a running workflow (adding/removing steps) while instances are in-flight is non-trivial; without versioning strategy, you will have broken in-flight instances.
- **State explosion**: storing too much data in workflow state (large payloads, full domain objects) leads to bloated state stores and serialization complexity.
- **Testing long-running workflows**: workflows that take hours to complete are hard to test end-to-end; lack of time-injection or step mocking leads to slow, flaky tests.
- **Timeout management complexity**: nested timeouts (step timeout, activity timeout, workflow timeout) interact in unexpected ways; under-specified timeout policy leads to zombie workflows.
- **Hidden coupling via shared DB**: orchestrator steps that share a database outside the orchestrator's state store re-introduce distributed monolith coupling.

## Heuristics
- Treat the workflow definition as a first-class artifact: version it, test it, review it.
- Keep workflow step inputs/outputs minimal (identifiers, not full objects); fetch data inside each step.
- Define and test compensation logic (saga rollback) as early as the happy path.
- Use time injection in step implementations to enable fast, deterministic workflow tests.
- Require a versioning strategy before any workflow definition is deployed to production.

## How This Kit's Boundary Model Applies
- **Core** = the business process definition (the orchestrator's workflow logic).
- **Boundary contracts** = the interface between the orchestrator and each step (activity/task contract).
- **Integration boundaries** = individual step implementations that call services, databases, or external APIs.

Each workflow step is an adapter. The orchestrator is the use-case layer. Keep business rules (eligibility checks, calculations) in the core, not in the workflow engine.

## Entry Points in This Kit
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` §1 — workflow-centric axis
- `architecture/rag/EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md` — choreography (the complementary approach)
- `architecture/SOLUTION_CLASS_TAXONOMY.md` — coverage map

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- `architecture/rag/EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md`
- `architecture/rag/STATE_VS_EVENT_MODEL.md`
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`
- `constitution/AI_RULES.md`
