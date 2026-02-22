# Contract-First / API-First — Advisory Note (Entry Point)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Coverage Level
**Acknowledged** (entry-point note) — The kit's boundary model applies directly: the schema IS the boundary contract. Schema evolution and versioning are covered by `SCHEMA_EVOLUTION_AND_VERSIONING.md`. Code generation tooling specifics are out of scope.

## Core Idea
In a **Contract-First / API-First** approach, the **schema (OpenAPI, protobuf, GraphQL, AsyncAPI) is the primary artifact**. Code either conforms to the schema (hand-written) or is generated from it. The contract is designed, reviewed, and versioned before implementation begins.

The defining characteristic: **the schema is the source of truth**, not the code. Code is subordinate to the contract.

## Why Teams Choose It
- Enables parallel development: frontend/backend or service/client teams can work independently once the contract is agreed upon.
- Forces API design discipline: thinking about the contract before the implementation avoids exposing implementation details in the API.
- Enables automatic code generation, validation, and documentation from a single source of truth.
- Supports consumer-driven contract testing: consumers define their expectations against the schema.

## When to Choose It
- Multiple teams or systems consume the same API; contract stability is critical.
- API is a product (external-facing, publicly documented, versioned).
- Code generation reduces boilerplate and ensures implementation conforms to the schema.
- Consumer teams need to test against the contract without depending on a live implementation.

## When NOT to Choose It
- Internal APIs that are consumed by only one caller and changed together with the implementation: the ceremony of contract-first outweighs the benefit.
- When the domain model is still highly exploratory; locking a contract early in a rapidly-changing domain leads to premature commitment and frequent breaking changes.
- When the team lacks the discipline to treat the schema as the source of truth: if code is manually edited after generation, or the schema drifts from implementation, contract-first becomes an anti-pattern.

## Common Failure Modes
- **Schema drift from implementation**: the schema says one thing, the implementation does another; consumers rely on the schema and encounter runtime failures; no automated validation between schema and implementation exists.
- **Generated code treated as hand-editable**: developers edit generated code directly instead of updating the schema and regenerating; the generated code diverges from the schema and the source-of-truth relationship is broken.
- **Contract versioning neglected**: the schema evolves without semver or deprecation policy; consumers receive breaking changes without warning; no migration guide exists.
- **Consumer testing gap**: contract tests exist for the provider side but not the consumer side; consumer expectations are not validated against the contract, leading to integration failures discovered late.
- **Over-specified contracts**: the contract exposes internal implementation details (internal field names, implementation-specific error codes); changes to implementation inevitably break the contract.
- **Schema review as afterthought**: the schema is created after the implementation as documentation; it inherits the implementation's design flaws and inconsistencies.

## Heuristics
- Treat the schema as a pull request artifact: schema changes require review before implementation begins.
- Automate schema-to-implementation conformance validation in CI (e.g., `openapi-enforcer`, `prism`, `buf lint`).
- Apply the same schema evolution discipline as to event schemas: see `SCHEMA_EVOLUTION_AND_VERSIONING.md`.
- Generate code from the schema; never edit generated code manually; if generation output is unsatisfactory, improve the generator or templates.
- Write consumer-driven contract tests (Pact, WireMock, `buf`'s breaking change detection) as part of the CI pipeline.

## How This Kit's Boundary Model Applies
The contract-first approach is a direct embodiment of the kit's boundary model (`AI_RULES.md` §1.4):
- **Core** = business logic that implements the contract's behavior.
- **Boundary contracts** = the schema (OpenAPI/protobuf/GraphQL); this IS the port; it is the most critical asset.
- **Integration boundaries** = framework-specific route handlers, serialization/deserialization code, and generated stubs/skeletons.

The normative rule — "boundary contracts MUST model domain-relevant operations, not technology details" — means the schema should be designed around domain concepts, not HTTP verbs, database columns, or framework conventions.

## Entry Points in This Kit
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` §1 — contract-centric axis
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md` — schema versioning and backward compatibility
- `architecture/SOLUTION_CLASS_TAXONOMY.md` — coverage map

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`
- `architecture/rag/LIBRARY_SDK_REPO.md`
- `architecture/rag/INFORMATION_HIDING.md`
- `constitution/AI_RULES.md`
