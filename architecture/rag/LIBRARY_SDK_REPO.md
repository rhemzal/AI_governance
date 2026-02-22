# Library / SDK Repo — Advisory Note (Entry Point)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Coverage Level
**Acknowledged** (entry-point note) — The kit's boundary model needs reinterpretation: the public API surface IS the boundary contract. Consumer-facing governance (semver, backward compatibility, API design) is partially covered via `SCHEMA_EVOLUTION_AND_VERSIONING.md`. Library-specific publishing pipelines and registry tooling are out of scope.

## Core Idea
A **library/SDK repo** is fundamentally different from an application repo: the **public API surface IS the product**. There are no end-users; the consumers are other developers (internal or external). The library has no runtime of its own; it runs in the consumer's process.

This inverts the typical boundary model: instead of protecting the core from external integrations, the library must protect its **consumers** from its internal implementation changes.

## Why Teams Choose It
- Package and share reusable business logic, utility functions, or SDK wrappers across projects.
- Enable external developer ecosystems (open-source libraries, commercial SDKs).
- Enforce a clean separation between reusable logic and application-specific code.

## When to Choose It
- Reusable logic that is consumed by multiple projects with independent release cadences.
- When you need to provide a stable, versioned API to external consumers (open-source or commercial).
- When the team wants to enforce a clean boundary between "what is public API" and "what is internal implementation detail."

## When NOT to Choose It
- When the "library" is only ever used by one application and never needs to be versioned independently: extract the logic into a module within the application instead.
- When the library boundary is premature and the API design is still evolving rapidly: publishing unstable APIs to consumers creates a migration burden.

## Common Failure Modes
- **Breaking changes without semver**: renaming or removing public API members without a major version bump silently breaks consumers who update their dependency.
- **Consumer-unfriendly API design**: the API is designed from the maintainer's perspective (what is easy to implement) rather than the consumer's perspective (what is easy to use); results in verbose, leaky, or confusing APIs.
- **Inadequate backward compatibility testing**: the library has unit tests for internal behavior but no contract tests that verify backward compatibility against the previous public API version.
- **Documentation gap between maintainer and consumer perspective**: internal docs explain implementation details; consumer docs (how to use the API, migration guides, examples) are absent or outdated.
- **Internal implementation detail leakage**: internal types, errors, or behavior are accidentally exposed in the public API, creating unintended contracts that cannot be changed without breaking consumers.
- **Dependency version conflicts**: the library depends on specific versions of shared dependencies; consumers who pin different versions experience transitive dependency conflicts.

## Heuristics
- Define and enforce the public API surface boundary explicitly: use module visibility rules, explicit `__all__` (Python), `public`/`internal` modifiers, or package-level export control.
- Apply semver strictly: patch for bug fixes, minor for backward-compatible additions, major for any breaking change.
- Write contract tests that run against the public API surface (not internal implementation); use mutation testing or breaking-change detection tools.
- Maintain a CHANGELOG and migration guide for every minor and major version.
- Test the library from a consumer's perspective (install from package, use the public API, do not reference internal modules).

## How This Kit's Boundary Model Applies (Reinterpreted)
In a library/SDK repo, the standard boundary model inverts:
- **Core** = internal implementation (hidden from consumers).
- **Boundary contracts** = the **public API surface** (the ports that consumers depend on); this is the most critical asset and must be treated with the highest stability guarantee.
- **Integration boundaries** = how the library integrates into the consumer's environment (framework adapters, optional integrations with third-party libraries).

The normative rule from `AI_RULES.md` §1.4 — "boundary contracts MUST model domain-relevant operations (not technology details)" — applies directly: the public API should model the domain of the library, not expose implementation details.

## Entry Points in This Kit
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` §1 — contract-centric axis
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md` — versioning and backward compatibility
- `architecture/SOLUTION_CLASS_TAXONOMY.md` — coverage map

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`
- `architecture/rag/INFORMATION_HIDING.md`
- `constitution/AI_RULES.md`
