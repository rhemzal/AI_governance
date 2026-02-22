# Monorepo (Multi-Project) — Advisory Note (Entry Point)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Coverage Level
**Acknowledged** (entry-point note) — The kit applies per-project within a monorepo. Cross-project boundary enforcement, selective CI, and shared vs. per-project governance are not yet fully covered by this kit.

## Core Idea
A **monorepo** hosts multiple distinct projects (applications, libraries, services) in a single version-controlled repository. All projects share the same commit history, tooling configuration, and CI pipeline, but maintain logical separation via directory structure and ownership rules.

The key distinction: a monorepo is not a monolith. It is a **repository structure choice** that is orthogonal to architecture style. A monorepo can contain microservices, modular monoliths, or any combination.

## Why Teams Choose It
- Atomic cross-project changes: refactor a shared interface and update all consumers in a single commit.
- Shared tooling, linting, and CI configuration reduce duplication.
- Easier code reuse: shared libraries are just internal packages, no publish/consume cycle.
- Single source of truth for all projects: no version matrix between repos.

## When to Choose It
- Multiple projects that share significant code or have frequent cross-cutting changes.
- Teams that want unified tooling and CI without managing separate repo configurations.
- When the overhead of coordinating releases across multiple repos outweighs the complexity of a monorepo.

## When NOT to Choose It
- Projects with fundamentally different access control requirements (e.g., open-source library alongside proprietary code).
- When CI build times become unacceptably long and selective build/test tooling (Nx, Turborepo, Bazel) is not in place.
- When different projects need radically different versioning or release cadences that monorepo tooling cannot accommodate cleanly.

## Common Failure Modes
- **"Big ball of mud" across projects**: without enforced module boundaries, code from one project imports internals of another, re-creating tight coupling at scale.
- **CI bottleneck**: every commit triggers the full build and test suite for all projects; without selective CI (affected-project detection), PR cycle times become unacceptable.
- **Governance sprawl**: each project has different standards; without a clear policy for shared vs. per-project governance, rules become inconsistent and unenforced.
- **CODEOWNERS complexity**: CODEOWNERS files grow unwieldy; ownership boundaries are unclear; reviews are routed to the wrong team.
- **Selective enforcement gap**: some CI gates or lint rules apply to all projects, others only to specific ones; without explicit scoping, either over-enforcement (breaking unrelated projects) or under-enforcement (gaps in coverage) occurs.

## Heuristics
- Establish a top-level `CODEOWNERS` policy and per-project ownership early; changing ownership later requires significant migration effort.
- Use selective CI (affected-project detection) from the start; adding it later requires restructuring the entire CI pipeline.
- Define explicit "shared" vs. "per-project" governance boundaries: which rules apply globally and which are project-local?
- Enforce cross-project import rules with tooling (ESLint `import/no-restricted-paths`, ArchUnit, custom linting); do not rely on conventions alone.
- Consider a LOCAL_OVERLAY at the repo root to define cross-project rules, with per-project overlays for project-specific extensions.

## How This Kit Applies to a Monorepo
The kit is designed around a **single-project repo** as the default. In a monorepo:
- Apply the kit's governance **per project directory**: each project directory is treated as if it were an independent single-project repo.
- Use a `LOCAL_OVERLAY` at the repo root to define cross-project rules (shared dependency policies, inter-project import restrictions, cross-cutting CI gates).
- Use per-project `LOCAL_OVERLAY` files for project-specific rule extensions.
- Cross-project boundary enforcement and selective CI configuration are not yet provided by this kit; teams must supply this using monorepo tooling (Nx, Turborepo, Bazel, custom scripts).

## Entry Points in This Kit
- `governance/LOCAL_OVERLAY_TEMPLATE.md` — per-project and cross-project overlay rules
- `ci/ARCHITECTURE_GATES.md` — CI gate principles applicable per project
- `architecture/SOLUTION_CLASS_TAXONOMY.md` — coverage map

## Related Documents
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `governance/LOCAL_OVERLAY_TEMPLATE.md`
- `ci/ARCHITECTURE_GATES.md`
- `constitution/AI_RULES.md`
