# Architecture Decision Framework (Project-Agnostic)

## Purpose
This document provides a **decision framework** for selecting an architectural style (e.g., Hexagonal, Layered, Event-Driven, Pipeline) **without cargo-culting**.

It is designed for AI-assisted development:
- It forces explicit reasoning.
- It highlights **points of no return**.
- It separates **normative rules** (in `constitution/`) from **decision guidance** (here).

## Rule of Use
Architecture style selection MUST:
1. Answer the questions in this framework.
2. Produce an ADR using `adr/ADR_TEMPLATE.md`.

If the answers are unknown, treat this as risk and explicitly record it.

---

## 1) Identify the System’s Primary Axis
Choose the dominant axis (often 1–2):
- **Behavior-centric**: business rules are the long-lived core; integrations change.
- **Data-centric**: data shape/queries dominate; rules are thin.
- **Integration-centric**: many external systems; protocols and adapters are the hard part.
- **Workflow-centric**: orchestration of steps dominates (pipelines, jobs).
- **Latency/throughput-centric**: performance constraints dominate design trade-offs.

### Why this matters
Different architectural styles optimize different axes.

---

## 2) Define Quality Attribute Priorities (Top 3)
Pick the top three and rank them:
- Modifiability
- Testability
- Performance
- Availability
- Security
- Operability
- Usability (for human-facing interfaces)
- Cost efficiency

For each priority, write:
- what “good” means (observable)
- what failure looks like

### Make it professional: write 2–5 Quality Attribute Scenarios
Do not stop at adjectives (“fast”, “scalable”). Use measurable scenarios:
- **Stimulus**: what happens?
- **Environment**: under what conditions?
- **Artifact**: what part of the system?
- **Response**: what must the system do?
- **Response measure**: measurable threshold (p95 latency, RPO (recovery point objective), deploy time, etc.)

Scenario template and examples:
- `architecture/rag/QUALITY_ATTRIBUTES.md`

If you do only one “theory” step, do this one.

---

## 3) Locate Stability (What Changes the Least?)
Identify what is expected to be most stable over time:
- domain rules
- external integrations
- interface/presentation
- data model
- deployment/runtime environment

### Heuristic
- If **domain rules** are stable and important, architectures that protect the core (e.g., boundary contracts via ports/interfaces) are often a good fit.
- If **data model** and queries dominate, consider whether a data-centric approach is more appropriate.

---

## 4) Boundaries and Failure Zones
Answer:
- Where can failures happen? (network, DB, external APIs, user inputs)
- How do we isolate failures from cascading?
- What MUST remain deterministic and testable?

---

## 5) Points of No Return (Irreversible Commitments)
Explicitly decide whether you are committing to any of these:
- Shared database across bounded contexts
- Event sourcing / append-only event log as system-of-record
- Microservices decomposition early
- Tight coupling to a specific framework/runtime
- Domain model that is deeply intertwined with persistence/ORM (Object-Relational Mapper)

If “yes”, the ADR MUST include:
- why this is worth it
- how rollback would work (if at all)

---

## 6) Choose a Baseline Style (Then Stress-Test It)
Pick one baseline style.

Then evaluate two alternatives and state why they lose.

Recommended baseline candidates:
- Hexagonal / Ports & Adapters
- Traditional Layered
- Event-Driven (choreography)
- Pipeline/Batch
- Modular monolith (style + boundaries)

---

## 6a) Hybrid Architectures (How to Combine Styles Without Drift)
Most real systems are hybrids. The goal is to make the hybrid **intentional** and enforceable.

Rules of thumb:
- Pick a **dominant style** for the core reasoning model (your “default”).
- Introduce secondary patterns only with an explicit **boundary** (where they start/stop).
- Hybridize by **bounded context/module**, not randomly by file.

Common safe hybrids:
- **Modular monolith + (Hexagonal inside modules)**: module boundaries are the primary guardrails; boundary contracts (ports/interfaces) + integration adapters protect volatile edges.
- **Layered + boundary contracts at the edges**: keep a simple layered core, but enforce dependency inversion for external integrations.
- **Event-driven for integration + state model inside modules**: events connect contexts; invariants still live in one transactional boundary.
- **CQRS only where query pressure demands it**: keep “one model” by default; add projections intentionally.

Common risky hybrids (require stronger governance):
- Microservices + shared database ownership.
- Event-driven + unclear ordering/idempotency + no schema evolution policy.
- CQRS everywhere (projection sprawl, hard-to-debug staleness).

If you choose a hybrid, the ADR MUST state:
- dominant style
- where the secondary pattern applies (boundary)
- compatibility/versioning strategy for any contracts (API/event/schema)
- the failure modes you accept and how you detect them

---

## 6b) Architecture Validation (ATAM-lite)
This is a lightweight, repeatable version of the idea behind ATAM-style evaluation: validate architecture against quality attribute scenarios.

Minimal procedure:
1. List the top 3 quality attributes and 2–5 scenarios (from section 2).
2. For each scenario, list candidate tactics (e.g., caching, timeouts, dependency inversion, bulkheads).
3. Identify sensitivity points (places where a small change breaks an attribute).
4. Identify trade-off points (e.g., performance vs. modifiability) and decide deliberately.
5. Record risks and “unknowns” in the ADR, including what you will measure.

Record items (3)–(5) explicitly in the ADR under:
- “Sensitivity Points & Risks” (see `adr/ADR_TEMPLATE.md`)

Output expectation:
- A reader can trace: scenario → tactic → architectural choice → enforcement/measurement.

---

## 7) Required Output: Architecture Decision Report
Create an ADR that includes:
- context and constraints
- alternatives considered
- trade-offs and failure modes
- points of no return
- how decisions are enforced (CI gates, tests)

## Related Documents
- `adr/ADR_TEMPLATE.md`
- `adr/ADR_0002_Architecture_Is_Contextual.md`
- `architecture/ARCHITECTURE_STYLE_MATRIX.md`
- `architecture/DATA_MODELING_GUIDE.md`
- `constitution/AI_RULES.md` and `constitution/AI_ENFORCEMENT.md`
- `ci/ARCHITECTURE_GATES.md` and `ci/TEST_GATES.md`

