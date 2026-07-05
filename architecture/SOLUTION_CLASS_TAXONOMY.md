# Solution Class Taxonomy & Coverage Map

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
This document is the **central coverage map** for the AI_governance kit. It answers:
- Which architectural styles, repo/project structure patterns, and cross-cutting concerns exist?
- How fully does this kit cover each one?
- Where should teams go if this kit does not fully cover their case?

This is an **entry point for teams** evaluating whether the kit applies to their system.

## Coverage Level Legend
| Level | Meaning |
|---|---|
| **Full** | Kit has RAG note + matrix entry + framework guidance + enforcement consideration |
| **Advisory** | RAG note + mentioned in matrix or framework; guidance exists but enforcement is not enforced by CI |
| **Mentioned** | Referenced in passing in kit documents; no dedicated note or matrix column |
| **Acknowledged** | Explicitly named; kit explains why it is not covered in depth and where to go instead (entry-point note) |
| **Out of scope** | Explicitly excluded with rationale |

---

## A) Architecture Styles / Solution Classes

| Solution Class | Coverage Level | Kit References | Notes |
|---|---|---|---|
| Hexagonal / Ports & Adapters | **Full** | RAG: `HEXAGONAL_RATIONALE_AND_FAILURE_MODES.md`; Matrix col; Framework §1 (behavior-centric), §6; `AI_RULES.md` §1 | Core kit style; full boundary model, failure modes, and enforcement guidance |
| Layered | **Full** | RAG: `LAYERED_RATIONALE_AND_FAILURE_MODES.md`; Matrix col; Framework §6; `AI_RULES.md` §1 | Full coverage including failure modes and CI gate guidance |
| Modular Monolith | **Full** | RAG: `MODULAR_MONOLITH.md`; Matrix col; Framework §6; `AI_RULES.md` §1 | Full coverage; recommended as default starting style |
| Event-Driven | **Full** | RAG: `EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md`; Matrix col; Framework §1 (workflow-centric), §6 | Full coverage including choreography failure modes |
| Microservices | **Full** | RAG: `MICROSERVICES_WHEN_NOT_TO.md`; Matrix col; Framework §6 | Covered primarily as "when NOT to"; full failure mode analysis |
| CQRS | **Advisory** | RAG: `CQRS_WHEN_AND_WHEN_NOT.md`; Matrix col | Advisory: when to choose, when not to choose; matrix column added |
| Config-Driven Pipeline | **Advisory** | RAG: `CONFIG_DRIVEN_PIPELINES.md`; Matrix col; Framework §1 (configuration-centric) | Full RAG note (incl. Coverage Level, Boundary Model, Entry Points) and matrix column; enforcement advisory only |
| Template Catalog | **Advisory** | RAG: `TEMPLATE_CATALOG.md`; mentioned in Framework | Advisory guidance for template-based generation |
| Pipeline/Batch | **Advisory** | RAG: `PIPELINE_BATCH.md`; Matrix col; Framework §1 (workflow-centric) | Full RAG note added; matrix column exists |
| Serverless / FaaS | **Advisory** | RAG: `SERVERLESS_FAAS.md`; Matrix col; Framework §1 (deployment-topology-centric) | Upgraded to Advisory; kit boundary model applies; provider-specific enforcement is out of scope |
| Orchestration-Centric (Saga / Workflow Engine) | **Advisory** | RAG: `ORCHESTRATION_SAGA_WORKFLOW.md`; Matrix col; Framework §1 (workflow-centric) | Upgraded to Advisory; complementary to event-driven choreography; orchestrator-specific tooling out of scope |
| Plugin / Extension Architecture | **Acknowledged** | RAG: `PLUGIN_EXTENSION_ARCHITECTURE.md` (entry-point note); Framework §1 (extensibility-centric) | Extension point design patterns noted; plugin runtime/lifecycle tooling out of scope |
| Streaming / Reactive (Continuous Data Flow) | **Advisory** | RAG: `STREAMING_REACTIVE.md`; Matrix col; Framework §1 (latency/throughput-centric) | Upgraded to Advisory; distinct from event-driven; stream-processing framework specifics out of scope |
| Actor Model | **Acknowledged** | — | Conceptually similar to event-driven; actor framework specifics (Akka, Erlang/OTP) are out of scope. Use event-driven guidance as starting point |
| Space-Based / Grid | **Acknowledged** | — | Niche pattern for extreme scale; no current kit coverage. Teams should consult vendor documentation |
| Cell-Based / Bulkhead | **Acknowledged** | — | Failure isolation concept; partially covered by boundary model. Full cell architecture is out of scope |
| Edge / Multi-Tier Deployment | **Acknowledged** | RAG: `EDGE_MULTI_TIER_DEPLOYMENT.md` (entry-point note); Framework §1 (deployment-topology-centric) | Entry-point note added; edge-specific runtime, CDN configuration, IoT gateway specifics out of scope |
| Embedded / Real-Time Systems | **Out of scope** | — | Hard real-time constraints, deterministic scheduling, and RTOS patterns are outside the kit's domain. Consult IEC 61508 / MISRA guidance |

---

## B) Repository / Project Structure Patterns

| Repo / Project Pattern | Coverage Level | Kit References | Notes |
|---|---|---|---|
| Single-App Repo | **Full** (implicit) | All kit documents assume this as default | Default assumed structure; all enforcement and CI gates apply directly |
| Template Catalog Repo | **Advisory** | RAG: `TEMPLATE_CATALOG.md` | Advisory guidance for template-based repos; scaffolding governance included |
| Monorepo (Multi-Project) | **Acknowledged** | RAG: `MONOREPO_PATTERNS.md` (entry-point note; extended with Cross-Project CI and Governance Layering sections) | Per-project governance works; cross-project CI guidance and governance layering examples added |
| Polyrepo (Coordinated Multi-Repo) | **Acknowledged** | — | Kit applies per repo; cross-repo contract governance (API versioning, shared schema) covered partially via `SCHEMA_EVOLUTION_AND_VERSIONING.md` |
| Library / SDK Repo | **Acknowledged** | RAG: `LIBRARY_SDK_REPO.md` (entry-point note; extended with Contract Testing and CI Gate Adaptation sections); Framework §1 (contract-centric) | Fundamentally different boundary model: public API surface IS the product; contract testing and CI gate guidance added |
| Contract-First / API-First Repo | **Acknowledged** | RAG: `CONTRACT_FIRST_API_FIRST.md` (entry-point note); Framework §1 (contract-centric) | Schema is the primary artifact; schema drift and versioning failure modes covered |
| Infrastructure-as-Code Repo | **Acknowledged** | — | IaC-specific linting and drift detection are out of scope; boundary model concepts (separation of concerns) apply |
| Data / Analytics Repo | **Acknowledged** | — | Data modeling guidance in `DATA_MODELING_GUIDE.md` partially applies; data pipeline governance is advisory |
| Mobile App Repo | **Acknowledged** | — | Boundary model applies (core vs. platform adapters); mobile-specific CI/CD (signing, store submission) is out of scope |
| Documentation-Only Repo | **Acknowledged** | — | Documentation rules from `AI_RULES.md` §5 apply; no architecture enforcement needed |
| Research / Experiment Repo | **Acknowledged** | — | Kit governance is intentionally lightweight here; teams may use advisory notes for framing experiments |
| Generated / Scaffold-Output Repo | **Acknowledged** | RAG: `TEMPLATE_CATALOG.md` | Template catalog guidance applies to generation; generated code governance policy required in LOCAL_OVERLAY |
| Fork-Based Contribution Model | **Acknowledged** | — | Standard fork/PR workflow; kit's doc delta and ADR conventions apply to contributions |

---

## C) Cross-Cutting Concerns

These patterns can be layered on top of any architecture style or repo structure.

| Cross-Cutting Concern | Coverage Level | Kit References | Notes |
|---|---|---|---|
| Multi-Tenancy | **Mentioned** | Implicitly relevant to boundary model and data isolation | Not yet dedicated guidance; tenant isolation is a boundary concern (apply `AI_RULES.md` §1) |
| Feature Flags / Progressive Delivery | **Advisory** | RAG: `FEATURE_FLAGS_PROGRESSIVE_DELIVERY.md`; Framework §4–§5 | Flag state as integration boundary; determinism and testing guidance; vendor platforms out of scope |
| Observability-as-Architecture | **Advisory** | RAG: `OBSERVABILITY_AS_ARCHITECTURE.md`; Framework §4; `MEASURED_PERFORMANCE.md` | When diagnosability belongs in design (correlation, retries, failure zones); tooling/runbooks out of scope |
| Zero-Trust / Defense-in-Depth | **Mentioned** | `AI_RULES.md` §1 (boundary contracts imply trust boundaries) | Boundary model aligns with zero-trust principles; security-specific enforcement is out of scope |
| Offline-First / Local-First | **Mentioned** | RAG: `CONSISTENCY_MODELS.md` | Consistency model guidance partially applies; conflict-resolution and sync specifics are out of scope |
| Multi-Language / Polyglot Codebase | **Mentioned** | `AI_RULES.md` §5.4 (language policy for docs) | Doc language policy defined; polyglot code governance (per-language linting, boundary contracts across languages) not yet covered |

---

## How to Extend This Taxonomy

When a new solution class, repo pattern, or cross-cutting concern is identified, follow this checklist to add it to the kit:

### Checklist: Adding a New Entry

- [ ] **Assess coverage level**: Does this need Full, Advisory, Acknowledged, or just Mentioned?
- [ ] **Write a RAG entry-point note** (if Acknowledged or higher):
  - File: `architecture/rag/<CLASSNAME>.md`
  - Use `architecture/rag/RAG_NOTE_TEMPLATE.md` (extracted structure; prefer extending an existing note over a new file)
- [ ] **Add a matrix entry** (if Advisory or higher):
  - **Architecture styles / repo patterns:** add column(s) to `architecture/ARCHITECTURE_STYLE_MATRIX.md`; add criterion rows and failure-mode notes as needed.
  - **Cross-cutting concerns:** add or extend the “Cross-Cutting Concerns” section in the matrix (not a style column); link the RAG note from framework §4 where relevant.
- [ ] **Update the Framework** (if Advisory or higher):
  - Add a new axis to §1 of `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` if the class introduces a new primary axis
  - Link to the new RAG note from Related Documents
- [ ] **Consider enforcement** (if Full):
  - Add CI gate or ADR-required check in `ci/ARCHITECTURE_GATES.md`
  - Update `constitution/AI_RULES.md` if the class changes normative behavior
- [ ] **Update this taxonomy**: Add a row to the appropriate table (A, B, or C) with the new entry's coverage level, kit references, and notes
- [ ] **Update the RAG README** (`architecture/rag/README.md`): Add the new note to the appropriate category in the Notes Index
- [ ] **Update `README.md`**: Add the new entry point to "Start here" if it is a top-level entry point
- [ ] **Record an ADR** if the extension represents a significant kit governance decision (use `adr/ADR_TEMPLATE.md`)

### Coverage Level Upgrade Path
`Acknowledged` → `Advisory`: Write a full RAG note + add a matrix column.
`Advisory` → `Full`: Add CI enforcement + update normative rules in `AI_RULES.md`.

---

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/ARCHITECTURE_DECISION_PROMPT.md`
- `architecture/ARCHITECTURE_STYLE_MATRIX.md`
- `architecture/rag/README.md`
- `architecture/rag/RAG_NOTE_TEMPLATE.md`
- `constitution/AI_RULES.md`
- `adr/ADR_TEMPLATE.md`
