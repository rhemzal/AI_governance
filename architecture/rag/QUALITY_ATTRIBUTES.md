# Quality Attributes — Advisory Note

## Core Idea
Architecture is primarily about meeting **quality attribute** goals (not just functionality).

## Practical Heuristics
- Write 2–5 concrete quality attribute scenarios (stimulus → measurable response).
- Decide trade-offs explicitly (e.g., modifiability vs. performance).

### Quality Attribute Scenario Template
Use this template to keep decisions measurable:
- **Stimulus**: what happens?
- **Environment**: under what conditions?
- **Artifact**: what part of the system?
- **Response**: what must the system do?
- **Response measure**: threshold (p95 latency, deploy time, data loss window, etc.)

Example (performance):
- Stimulus: user requests account summary
- Environment: peak traffic
- Artifact: read model + API
- Response: return summary
- Measure: p95 < 300ms, error rate < 0.1%

## What This Suggests Architecturally
- If testability and modifiability are top priorities, strong boundaries pay off.
- If throughput/latency dominates, measure first and budget performance early.

### Tactics Map (Very Short)
Use tactics as the “theory bridge” between scenarios and architecture:
- Modifiability/testability: dependency inversion, stable boundaries, small interfaces, explicit boundary contracts (ports/interfaces)
- Availability/resilience: timeouts, retries with backoff, bulkheads, circuit breakers, graceful degradation
- Performance: caching, batching, async work, queueing/backpressure, avoiding chatty call chains
- Security: least privilege, threat modeling, clear trust boundaries, auditability
- Operability: observability (logs/metrics/traces), runbooks, feature flags, safe rollouts

## Worked Example (Scenario → Tactics → Architecture → Enforcement)
Goal: make the “theory bridge” concrete and auditable.

### Example A: Modifiability + Testability (Integration Volatility)
Quality attribute scenario:
- Stimulus: add a new external payment provider
- Environment: normal development, existing provider must keep working
- Artifact: payments capability
- Response: implement + ship safely
- Measure: change is limited to adapter + configuration; core tests remain unchanged; delivery in ≤ 3 days

Candidate tactics:
- dependency inversion via explicit boundary contracts (ports/interfaces)
- small stable boundary contracts
- contract tests for integration boundaries (adapters)

Architectural choice implied (common fit):
- modular monolith with clear module boundary for payments
- boundary contracts (ports/interfaces) + integration adapters inside the payments module for provider integrations

Enforcement / evidence:
- ADR records this scenario and the chosen tactics
- CI gate: boundary integrity checks (no adapter imports from core) (see `ci/ARCHITECTURE_GATES.md`)
- Tests: adapter contract tests against the boundary contract; core tests remain isolated

Sensitivity points to record in the ADR:
- “One shortcut” import from adapter into core breaks the boundary and makes future providers expensive.
- “Port too wide” makes tests flaky and couples to provider details.

### Example B: Availability + Operability (External Dependency Failure)
Quality attribute scenario:
- Stimulus: downstream API returns 500s for 10 minutes
- Environment: peak traffic
- Artifact: integration boundary + request handling
- Response: degrade gracefully; protect internal resources
- Measure: error rate visible in dashboards; no cascading failure; p95 latency within agreed budget for unaffected endpoints

Candidate tactics:
- timeouts + retries with backoff
- circuit breaker + bulkhead isolation
- structured logs/metrics/traces

Architectural choice implied (common fit):
- explicit integration boundary (edge) layer, with resilience policies owned at the boundary

Enforcement / evidence:
- ADR lists tactics and where they apply (boundary)
- CI/tests: resilience tests (timeouts/circuit breaker behavior) for the adapter; chaos test optional if maturity allows

## When This Fails / Failure Modes
- Attributes are stated but not measurable.
- Teams optimize for what’s easy to code, not what matters.
- “Performance” becomes an excuse for breaking boundaries without measurement.
- Scenarios are written but never used to evaluate alternatives (paperwork without impact).
