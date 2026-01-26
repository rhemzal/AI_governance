# Architecture & Data Terminology Glossary (Advisory)

## Purpose
Provide a shared vocabulary so architecture discussions are consistent, reviewable, and less “LLM-magic”.

This glossary is **advisory**. Normative rules live in `constitution/`.

## Recommended Default Vocabulary (Style-Agnostic)
When writing governance text in this repo, prefer these neutral terms:
- **Core**: domain + use-cases/policy that must stay deterministic.
- **Boundary contract**: the explicit contract at the boundary (ports/interfaces/APIs).
- **Integration boundary**: code that touches the outside world (adapters/infrastructure).

These map cleanly to multiple architecture styles:
- Hexagonal: core + ports + adapters
- Layered: domain/application as core, boundaries expressed as interfaces, integrations at the edge
- Modular monolith: core within modules, integration boundaries at module edges

## Core Architecture Terms
- **Boundary**: a line beyond which different rules apply (dependencies, ownership, change cadence).
- **Module**: a unit of code organization with explicit responsibilities (can be enforced by tooling).
- **Component**: a runtime unit or deployable unit (not always equal to a module).
- **Layer**: an ordered dependency structure (e.g., UI → application → domain → infrastructure).
- **Adapter**: code that translates between the system and external concerns (UI, DB, network).
- **Port**: an inward-facing contract that defines what the core needs from outside.

## Domain & Modeling Terms
- **Invariant**: a rule that must always hold (e.g., “balance cannot be negative”).
- **Aggregate**: a consistency boundary for enforcing invariants in one transaction.
- **Bounded Context**: a boundary where a domain model and its language are consistent.
- **Ubiquitous Language**: shared terms used in code, docs, and interfaces.

## Data & Consistency Terms
- **System of record**: the authoritative source of truth for some facts.
- **State model**: stores current truth.
- **Event model**: stores immutable facts over time; state is derived.
- **Idempotency**: repeating an operation has the same effect as doing it once.
- **Consistency model**: the guarantees about visibility/order of updates (strong vs eventual).

## Governance & Enforcement Terms (AI Workflow)
- **Human-review fallback (enforcement)**: temporary enforcement mode when CI gates are not wired yet; compliance is checked via PR checklist/review.
- **Automation-first enforcement**: enforcement is implemented as deterministic checks (CI gates/scripts) and the PR provides evidence (e.g., `DOC DELTA`) rather than relying on informal manual process.

## Delivery & Operations Terms
- **SLO/SLA**: service-level objective/agreement; what “good” means operationally.
- **Backpressure**: resisting overload by slowing producers / shedding work.
- **Observability**: ability to infer internal state from outputs (logs/metrics/traces).

## Common Acronyms the AI Will Use (And Where Confusion Happens)
Use this section to keep AI conversations precise.

### Architecture / Design
- **ADR**: Architecture Decision Record.
- **ATAM**: Architecture Tradeoff Analysis Method (use “ATAM-lite” here: validate choices against measurable quality attribute scenarios).
- **ISO/IEC 25010**: quality model taxonomy (what “quality attributes” usually refer to in professional contexts).
- **C4**: diagramming model for software architecture (Context/Container/Component/Code) to keep docs consistent.
- **DDD**: Domain-Driven Design (can be confused with “data-driven design”).
- **EDA**: Event-Driven Architecture.
- **CQRS**: Command Query Responsibility Segregation (separate command/write model from query/read model; implies projections and operational cost, often with eventual consistency/staleness).
- **CRUD**: Create, Read, Update, Delete (data-centric application style; often paired with simpler domain rules).
- **ORM**: Object-Relational Mapper (maps objects to relational tables; common failure mode is “ORM leakage” where persistence concerns bleed into the domain model).
- **ES**: Event Sourcing (sometimes confused with “Elasticsearch”).
- **SoR**: System of Record.
- **BC**: Bounded Context.
- **API**: Application Programming Interface (also “public contract”).
- **RFC**: Request for Comments (decision proposal format; org-dependent).

### Security (Common Evaluation Vocabulary)
- **STRIDE**: threat modeling categories (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege).
- **CSF**: (NIST) Cybersecurity Framework.
- **SSDF**: (NIST) Secure Software Development Framework.
- **RBAC**: Role-Based Access Control (authorize by role membership).
- **ABAC**: Attribute-Based Access Control (authorize by attributes, context, and policy rules).
- **AuthN/AuthZ**: Authentication vs Authorization.

### Testing
- **SUT**: System Under Test.
- **TDD**: Test-Driven Development.
- **BDD**: Behavior-Driven Development.
- **E2E**: End-to-end tests.
- **UAT**: User Acceptance Testing.
- **NFR**: Non-Functional Requirements (quality attributes).

### Delivery / Ops
- **CI/CD**: Continuous Integration / Continuous Delivery.
- **SLA/SLO**: availability/latency goals (often confused or used interchangeably).
- **MTTR**: Mean Time To Recovery.
- **RTO**: Recovery Time Objective (maximum acceptable time to restore service after an incident).
- **RPO**: Recovery Point Objective (maximum acceptable data loss window, measured in time).

### Supply Chain / Provenance
- **SBOM**: Software Bill of Materials (inventory of components/dependencies used to build a system).
- **SLSA**: Supply-chain Levels for Software Artifacts (levels for build provenance and supply-chain integrity).
- **SPDX**: Software Package Data Exchange (one SBOM/specification format).
- **CycloneDX**: an SBOM standard/specification (commonly used for dependency inventory).

### Compliance / Regulation (Context-Dependent)
- **NIS2**: EU Network and Information Systems Directive (NIS2).
- **DORA**: (EU) Digital Operational Resilience Act.

### AI Workflow
- **RAG**: Retrieval-Augmented Generation (advisory grounding in this repo).
- **MCP**: Model Context Protocol (optional external context integration).

### Accessibility
- **a11y**: Accessibility (shorthand: “a” + 11 letters + “y”).
- **WCAG**: Web Content Accessibility Guidelines.

## How to Use Acronyms in Prompts (Examples)
Use “define before use” to prevent the assistant from guessing.

Example prompt snippets:
- “Use **DDD** to mean *Domain-Driven Design* (bounded contexts + ubiquitous language), not ‘data-driven’."
- “When you say **ES**, confirm you mean *Event Sourcing* (not Elasticsearch)."
- “For **CQRS**, explain the operational cost (projections, staleness) and when we should NOT choose it."
- “Define **SUT** and propose tests by layer (domain/application/adapters)."

## When Confusion Is Likely
- Same acronym means different things across teams/tools (e.g., ES).
- “Model” is overloaded: domain model vs persistence model vs read model.
- “Architecture” is overloaded: code structure vs deployment topology.
- “Quality” is overloaded: quality attributes vs code quality vs UX polish.

Mitigation:
- Ask the AI to restate definitions in 2–3 bullets before proposing changes.
- Prefer explicit terms over acronyms in ADRs and public docs.

## When this fails
- If terms are used inconsistently, architecture discussions become unreviewable.
- If the glossary is treated as authority, it can block pragmatic decisions.

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/DATA_MODELING_GUIDE.md`
- `architecture/rag/QUALITY_ATTRIBUTES.md`
- `constitution/AI_RULES.md`
