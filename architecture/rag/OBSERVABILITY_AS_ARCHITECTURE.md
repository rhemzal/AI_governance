# Observability-as-Architecture — Advisory Note

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Coverage Level

**Advisory** — The kit covers when observability belongs in architectural decisions (correlation, failure zones, testability). Vendor-specific tooling (Datadog, OpenTelemetry collectors, log pipelines) and SRE runbooks are out of scope.

## Core Idea

Observability-as-Architecture means **how you detect, trace, and reason about failures is designed with the system**, not added after deployment.

Logs, metrics, and traces are not “ops polish” — they are part of the boundary model: they determine whether retries, fallbacks, and async flows remain understandable and testable.

The defining characteristic: a reader (or agent) can follow a request across boundaries without guessing which ad-hoc `console.log` or retry block is authoritative.

## Why Teams Choose It

- Async, event-driven, and multi-adapter systems fail in ways that unit tests alone cannot surface.
- Production debugging depends on correlating work across modules, queues, and external APIs.
- Operability is a ranked quality attribute (availability, mean time to recovery).

## When to Choose It

- The system has **multiple failure zones** (network, DB, external APIs, queues) where cascading errors are plausible.
- Work crosses **module or service boundaries** and must be traced end-to-end.
- You use **retries, timeouts, circuit breakers, or fallbacks** — each must be observable, not invisible control flow.
- **AI-assisted changes** are frequent; without explicit observability contracts, agents add ad-hoc logging and retry logic that drifts from design.

## When NOT to Choose It

- A single-process CRUD app with synchronous, local-only I/O and no external integrations — minimal structured logging may suffice.
- You have not yet defined failure zones (framework §4) — observability design will be arbitrary.
- The team treats observability as “we’ll add Datadog later” while shipping complex async topology now.

## Common Failure Modes

- **Bolt-on observability**: logs and metrics added per PR with no correlation strategy; production incidents require code archaeology.
- **Ad-hoc retry/fallback sprawl**: AI and humans add `try/catch`, retries, and silent fallbacks without shared policy; behavior differs by file with no trace.
- **Missing correlation**: requests cannot be tied across handlers, jobs, or adapters; distributed debugging is guesswork.
- **Log noise without signals**: high volume of unstructured logs; alerts fire on symptoms, not on violated invariants.
- **Untestable failure paths**: retry and timeout behavior is only validated in production; tests mock away the observability contract.
- **Metrics without scenarios**: dashboards exist but do not map to quality attribute scenarios from `architecture/rag/QUALITY_ATTRIBUTES.md`.

## Heuristics

- Decide **correlation identity** at architectural boundaries (request ID, trace context) before adding retries or async handoffs.
- Treat **retry, timeout, and fallback** as explicit design choices — document them in ADRs and make them visible in logs/traces (what retried, why, outcome).
- Prefer **structured, stable log fields** at integration boundaries; free-text debug prints are not a contract.
- Map observability to **failure zones** from `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` §4: each zone should have a defined “how we know it failed.”
- Separate **performance measurement** (`architecture/rag/MEASURED_PERFORMANCE.md`) from **runtime diagnosability** — both matter; neither replaces the other.
- In tests, assert on **observable outcomes** for critical paths (e.g., dead-letter, error metric hook, structured error event) where operability is a top-3 attribute.

## How This Kit's Boundary Model Applies

- **Core** = domain logic that should stay deterministic; failures at edges should surface as explicit outcomes, not swallowed logs.
- **Boundary contracts** = ports/interfaces and event/API schemas; each crossing should propagate correlation context and emit boundary-level success/failure signals.
- **Integration boundaries** = adapters, handlers, clients; retries and timeouts live here and must be observable without leaking provider SDK details into core.

Observability is how you **enforce** that integration boundaries fail loudly and traceably instead of hiding state in implicit control flow.

## Entry Points in This Kit

- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` §2 (Operability as quality attribute) and §4 (failure zones)
- `architecture/ARCHITECTURE_DECISION_PROMPT.md` — `Failure zones` field
- `architecture/SOLUTION_CLASS_TAXONOMY.md` — cross-cutting concerns table
- `architecture/rag/MEASURED_PERFORMANCE.md` — performance budgets (complementary)

## Related Documents

- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- `architecture/rag/QUALITY_ATTRIBUTES.md`
- `architecture/rag/MEASURED_PERFORMANCE.md`
- `architecture/rag/EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md`
- `constitution/AI_RULES.md`
