# AI-Assisted Development Governance Kit

This repository is a reusable, project-agnostic governance kit for **AI-assisted software development**.

It provides:
- **Normative rules** (what must/must not happen)
- **Enforcement mechanisms** (how rules are enforced, including CI/CD gates)
- **Decision frameworks** (how to choose architecture and data models; not cargo-culted defaults)
- **Advisory theory grounding** (curated RAG-style notes to reduce dependence on any specific LLM’s training)

Normative sources live in `constitution/` and `ci/`; `architecture/rag/` is advisory.

## Why This Exists

Motto: Speed with oversight; every decision traceable.

- Author: Richard Hemzal. Keep choices auditable and reduce drift.
- Speed up work with AI-assisted programming without losing control.
- Test whether the rules remain universal across contexts and teams.
- Apply the same rules beyond programming (business, physics) for consistency.
- Clarify the future direction of programming work; show colleagues that AI is a tool to master.

## What This Repo Is
- A **governance constitution** for AI-assisted development.
- A set of **portable documents** you can copy into other repositories.
- A place to store **ADRs** (Architecture Decision Records) that keep decisions explicit and reviewable.

## What This Repo Is Not
- Not a code template.
- Not a framework-specific starter.
- Not a tool configuration repository (no vendor lock-in).

## Attribution / Traceability
If you copy parts of this kit into another repository, preserve the “Provenance” banner at the top of imported documents so the origin remains traceable.

## Disclaimer
This repository provides governance guidance and reusable documentation. It is not legal advice and does not guarantee compliance with any standard or regulation.

## Repository Structure
- `constitution/` — core rules and enforcement contracts
- `interface/` — rules for UI/CLI/TUI/headless interfaces and interface-specific CI gates
- `architecture/` — architecture decision framework + data modeling guidance
- `architecture/rag/` — short, curated theory notes (advisory; not normative)
- `ci/` — CI/CD gate definitions (principles and checks; implementation varies by stack)
- `tooling/` — AI-driven tool optimization protocols (experiments, benchmarks)
- `adr/` — ADR templates and accepted decisions for this governance kit
- `usage/` — how to import and apply this kit in other repositories

## Documents (Start Here)

## Find What You Need (Fast Navigation)
- Daily AI work: [constitution/AI_ENFORCEMENT_DAILY.md](constitution/AI_ENFORCEMENT_DAILY.md)
- High-risk change (boundaries/contracts): [constitution/AI_ENFORCEMENT.md](constitution/AI_ENFORCEMENT.md)
- Write a decision the “professional” way: [adr/ADR_TEMPLATE.md](adr/ADR_TEMPLATE.md)
- ADR index (this kit): [adr/README.md](adr/README.md)
- Pick or justify an architecture: [architecture/ARCHITECTURE_DECISION_FRAMEWORK.md](architecture/ARCHITECTURE_DECISION_FRAMEWORK.md)
- Compare styles quickly: [architecture/ARCHITECTURE_STYLE_MATRIX.md](architecture/ARCHITECTURE_STYLE_MATRIX.md)
- Validate trade-offs (theory prompts): [architecture/rag/QUALITY_ATTRIBUTES.md](architecture/rag/QUALITY_ATTRIBUTES.md)
- Avoid common failures: [architecture/rag/README.md](architecture/rag/README.md) (incl. distributed monolith + schema evolution)
- Keep terms unambiguous (LLM-safe vocabulary): [architecture/TERMINOLOGY_GLOSSARY.md](architecture/TERMINOLOGY_GLOSSARY.md)
- Import into another repo (and keep precedence clear): [usage/LOCAL_OVERLAY_AND_PRECEDENCE.md](usage/LOCAL_OVERLAY_AND_PRECEDENCE.md)
- Minimum viable CI adoption: [usage/CI_MINIMUM_ADOPTION.md](usage/CI_MINIMUM_ADOPTION.md)

### Constitution (Normative)
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
- `constitution/AI_ENFORCEMENT_DAILY.md`

### Interface Layer (Integration Boundary / Adapters)
- `interface/INTERFACE_RULES_PROPOSAL.md`
- `interface/INTERFACE_CI_GATES.md`

### Architecture Decision Guidance
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/ARCHITECTURE_STYLE_MATRIX.md`
- `architecture/DATA_MODELING_GUIDE.md`

### Research References (Advisory)
- `research/PROFESSIONAL_STANDARDS_AND_REFERENCES.md`

### RAG Notes (Advisory)
- `architecture/rag/README.md`
- `architecture/rag/INFORMATION_HIDING.md`
- `architecture/rag/CONWAYS_LAW.md`
- `architecture/rag/QUALITY_ATTRIBUTES.md`
- `architecture/rag/HEXAGONAL_RATIONALE_AND_FAILURE_MODES.md`
- `architecture/rag/STATE_VS_EVENT_MODEL.md`
- `architecture/rag/MEASURED_PERFORMANCE.md`
- `architecture/rag/DISTRIBUTED_MONOLITH.md`
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`

### CI Gates (Principles)
- `ci/ARCHITECTURE_GATES.md`
- `ci/TEST_GATES.md`
- `ci/INTERFACE_GATES.md`
- `ci/DOC_GATES.md`

### Tooling Protocols (Advisory)
- `tooling/AI_TOOL_OPTIMIZATION.md`
- `tooling/COPILOT_OPTIMIZATION_PROTOCOL.md`
- `tooling/BENCHMARK_SCENARIOS.md`

### ADRs
- `adr/ADR_TEMPLATE.md`
- `adr/ADR_0001_Automation_First_Interfaces.md`
- `adr/ADR_0002_Architecture_Is_Contextual.md`
- `adr/ADR_0003_RAG_Is_Advisory_Not_Normative.md`
- `adr/ADR_0004_Tooling_Is_Experimental.md`

### Usage
- `usage/QUICKGUIDE.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `usage/HOW_TO_USE_WITH_VSCODE.md`
- `usage/AUDIT_PLAYBOOK.md`
- `usage/AUDIT_REPORT.md` and `usage/FIX_PLAN.md` (latest audit run outputs)
- `usage/HOW_TO_IMPORT.md`
- `usage/FOR_EXISTING_PROJECTS.md`

## Quick Start (Import Into Another Repo)
1. Copy the folders you need (recommended minimum: `constitution/`, `interface/`, `adr/`, `usage/`).
2. Make the rules discoverable:
   - Keep rule files in the repo root or a top-level folder.
   - Use consistent filenames and terminology.
3. Add CI checks that enforce the rules (see `ci/`).

## PR Habit: “Doc Delta”
When a PR changes behavior, include the `### DOC DELTA` block from `usage/HOW_TO_USE_WITH_COPILOT.md`.
`DOC DELTA` is PR evidence/metadata: reference the source of truth (code/tests/ADRs) and list which docs were updated/removed. It can be filled by AI and reviewed like any other PR content.
For architecture-impacting changes, ensure the ADR includes `## Documentation Impact` (see `adr/ADR_TEMPLATE.md`).

## Governance Principles (High-Level)
- Rules are **normative**: MUST/MUST NOT.
- Tooling protocols are **advisory** and experimental.
- Architecture decisions are **contextual** and must be recorded.
- RAG notes are **advisory**, used to explain trade-offs and failure modes.

## License
This repository is intended to be publishable and reusable.

- Documentation and other non-code content: **CC BY 4.0** (see `LICENSE`).
- Scripts (e.g., `scripts/`): **MIT** (see `LICENSE-CODE`).

## Contributing
See `CONTRIBUTING.md`.

## Security
See `SECURITY.md`.
