# AI_RULES — Core Engineering and Architecture Rules

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

These rules are **normative**. Any AI assistant working in a governed repository must treat these as hard constraints.

## Architecture Selection (Required)
This kit does not assume a default style.

- Projects MUST select an architecture style using `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`.
- The decision MUST be recorded as an ADR (see `adr/ADR_TEMPLATE.md`, and `adr/ADR_0002_Architecture_Is_Contextual.md`).

Section 1 defines a **style-agnostic boundary profile** (core vs. integration boundaries) that can be implemented as:
- Hexagonal / Ports & Adapters
- Layered
- Modular monolith

You may rename layers/modules to match your stack, but you MUST preserve the constraints.

## 0. Definitions
- **Core**: the part of the system you must keep deterministic and stable (business rules, use-cases, policy).
- **Boundary contract**: an explicit contract at a boundary (port/interface/protocol) that the core depends on.
- **Integration boundary**: code that touches the outside world (UI/CLI/TUI, DB, network, filesystem, external APIs).

Common mapping (one possible vocabulary):
- **Domain**: pure business rules and domain model.
- **Application**: use-case orchestration and coordination.
- **Adapters**: infrastructure and delivery mechanisms.
- **Ports**: explicit boundary contracts between the core and integrations.

## 1. Architecture Boundary Profile (Core / Boundary Contracts / Integrations)
This section is a **style-agnostic profile**: it describes the constraints that keep boundaries enforceable, regardless of whether you implement them as hexagonal, layered, or modular monolith.

### 1.1 Dependency Direction
- **Dependencies MUST point inward**: Integrations → Boundary contracts → Core.
- Core logic MUST NOT depend on integration details, frameworks, or I/O.

### 1.2 Domain Purity
- Domain code MUST be free of:
  - I/O (network, filesystem, database)
  - framework types
  - serialization/transport concerns
- Domain logic MUST be deterministic given explicit inputs.

### 1.3 Use-Case / Core Responsibilities
- The use-case/core layer MUST:
  - orchestrate use-cases
  - coordinate boundary contracts
  - map core outcomes to boundary outcomes (errors/results)
- Core MUST NOT contain integration/infrastructure logic.

### 1.4 Boundary Contracts (Ports / Interfaces)
- External interactions MUST be expressed through minimal, stable boundary contracts (ports/interfaces).
- Boundary contracts MUST model domain-relevant operations (not technology details).

### 1.5 Adapters
- Adapters MUST contain all technology/framework code.
- Adapters MUST NOT contain business rules.
- One adapter SHOULD have one reason to change.

## 2. Robustness and Determinism
### 2.1 Explicit Error Model
- Errors MUST be explicit and domain-relevant.
- Generic catch-all exception handling MUST be avoided.
- Mapping to transport-specific errors MUST happen in adapters.

### 2.2 Non-Determinism Injection
- Time, randomness, environment configuration, and I/O MUST be injected through boundary contracts (ports/interfaces) or explicit parameters.
- No hidden globals/singletons for non-deterministic sources.

### 2.3 Fail-Fast
- Invalid inputs MUST be rejected early.
- Silent failures are forbidden.

## 3. Code Quality
- Prefer explicit over implicit.
- Keep functions and files small and single-purpose.
- Avoid hidden coupling (implicit shared state, magical defaults).

## 4. Testing Rules
- Core (domain + use-cases): unit/behavior tests for business rules (high confidence target).
- Integration boundaries: contract/integration tests for real I/O boundaries.
- Tests MUST respect architectural boundaries.

## 5. Documentation Rules
- Documentation is a **first-class artifact** (same importance as code).
- Documentation MUST match the code.
- A topic MUST have a single source of truth.
- Remove outdated or duplicate documentation.

### 5.1 Anti-Fragmentation Rule
- Prefer extending an existing document with a new section over creating a new document.
- If a new document is created, it MUST:
  - have a clear scope (“one topic”)
  - be linked from `README.md` (as the hub)
  - include a `Related Documents` section

### 5.2 Documentation Automation (Reproducible)
- If any documentation is generated (by AI or tooling), the change MUST include:
  - the source of truth (where the content comes from)
  - a reproducible regeneration command/process (tool-agnostic description is fine)
  - a clear policy: committed artifact vs build output
- Generated documentation MUST NOT be edited manually without updating its source.

### 5.3 Working Notes / Parking-Lot Notes (Non-Canonical)
Some repositories include working notes intended to prevent context-switching (e.g., `notes/`).

- `notes/**` MUST be treated as **non-canonical working notes** by default.
- The AI MUST NOT edit files under `notes/**` unless explicitly instructed.
- If explicitly instructed to update a note, the AI SHOULD prefer:
  - appending new entries instead of rewriting existing text, and/or
  - adding links to the Issue/ADR/PR where the item was resolved.
- The AI MUST NOT refactor, reformat, or “clean up” notes as part of unrelated tasks.

### 5.4 Language Policy (English-First; Translations Optional)
To keep collaboration and AI-assisted work consistent, this kit defines a strict language policy for shared, canonical artifacts.

#### 5.4.1 Canonical documentation (MUST be English)
These are canonical and MUST be written in English:
- root `README.md`
- `constitution/**`
- `ci/**`
- `usage/**`
- `adr/**`
- `architecture/**` (including `architecture/rag/**`)
- `.github/**` templates (issues / PRs)

#### 5.4.2 Code comments (SHOULD be English)
- Long-lived, shared code comments (public contracts, invariants, tricky logic) SHOULD be written in English.
- Domain terms MAY remain in the domain’s natural language, but SHOULD be defined once (ADR/glossary) and used consistently (ubiquitous language).

#### 5.4.3 Notes
- `notes/local/**` MAY be any language (personal, not committed).
- `notes/committed/**` SHOULD be English unless a local overlay explicitly defines another shared language.

#### 5.4.4 Translations (optional; MUST be subordinate)
Non-English translations MAY exist, but only as explicitly subordinate artifacts:
- Translations MUST live under `translations/<lang>/...`.
- Each translated document MUST state the canonical English source it mirrors (path + commit/SHA or version tag when possible).
- Translations MUST NOT override canonical rules. If a translation conflicts with English canonical docs, English wins.

## 6. Mandatory AI Behavior (When Acting As a Coding Assistant)
- Before making changes, the AI MUST identify which layer the change belongs to.
- If a rule would be violated, the AI MUST stop and propose a compliant alternative.
- The AI MUST be able to explain boundary decisions in plain language.

### 6.1 Self-Service First (Do Not Bother Operators)
- The AI MUST first consult repo sources of truth (docs, code, tests, ADRs) before asking questions.
- The AI MUST NOT ask the user for information it can determine from the repository context.
- If information is missing, the AI MUST:
  - state the assumption explicitly
  - propose 1–3 narrow questions only if truly blocking

### 6.2 Non-Interactive Execution & Time Limits
- The AI MUST avoid running commands that may prompt for input.
- If a command/tool might be interactive, the AI MUST:
  - use non-interactive flags/modes where available, OR
  - wrap execution so it fails fast rather than blocking
- Long-running commands MUST be time-bounded (wall-clock timeout) and must fail clearly if the limit is hit.

## Related Documents
- `constitution/AI_ENFORCEMENT.md`
- `ci/ARCHITECTURE_GATES.md`
- `ci/TEST_GATES.md`
