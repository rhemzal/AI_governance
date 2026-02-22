# Template Catalog / Scaffold Repository — Advisory Note

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Core Idea
A repository that is **not a single application** but a **catalog of independent, self-contained templates** — each deployable on its own, each demonstrating a concrete, working pattern.

The repository's primary value is **discoverability and standardization**, not a unified runtime.

## Why It Helps
- **Fast onboarding**: developers can copy and deploy a working template immediately.
- **Standardized patterns**: common conventions (config structure, Dockerfile, README format) are enforced across the organization.
- **Reuse without coupling**: each template is independent; there is no shared state or internal dependency to break.
- **Living documentation**: templates serve as tested, executable documentation of recommended patterns.

## When to Choose It
- Cookbooks and example repositories for a framework or platform.
- Starter kits for AI/ML pipeline collections.
- Internal developer portals where teams share deployment-ready patterns.
- Any context where onboarding speed and pattern consistency are the primary goals.

## When NOT to Choose It
- When templates need tight cross-cutting coordination at runtime (they are no longer independent — consider a monorepo with shared runtime instead).
- When the "catalog" is actually a single application with multiple modes (the template abstraction is false).
- When templates share enough internal code that copy-paste maintenance becomes a drag (extract a library/package instead).

## Common Failure Modes
- **Drift between templates**: templates accumulate different config patterns, different Docker conventions, inconsistent README structure — the catalog loses its standardization value.
- **Orphaned templates**: templates exist in the repository but are not listed in the main index/README; they become undiscoverable and unmaintained.
- **No cross-template consistency checks in CI**: templates diverge silently because CI only tests them in isolation, never checks structural compliance.
- **Template coupling**: templates begin sharing internal code or state, defeating independence and making individual deployment harder.
- **Stale templates**: templates are not updated when the underlying framework or platform evolves; users copy outdated patterns.

## Heuristics
- **Define a template contract**: every template MUST include at minimum: a README, a config file, a Dockerfile (or equivalent), and at least one runnable example or smoke test.
- **Enforce consistency via CI**: lint all templates for structural compliance (presence of required files, README sections, config schema adherence) on every PR.
- **Main README/index is the single source of truth**: a template that is not listed in the index does not exist for users. Treat index maintenance as mandatory.
- **Treat each template as an independent deploy unit**: shared code goes into a versioned library or package — never copy-paste. If you copy-paste, you own divergence forever.
- **Archive stale templates explicitly**: mark outdated templates as archived/deprecated rather than leaving them silently in the catalog.

## Quality Attribute Emphasis
- **Consistency > individual template complexity**: a simpler, consistent template beats a clever, idiosyncratic one.
- **Discoverability > feature richness**: a template that cannot be found provides no value.
- **Onboarding speed as a primary metric**: how long does it take a new developer to go from zero to running instance? This is the key measure of a template catalog's success.

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/ARCHITECTURE_STYLE_MATRIX.md`
- `ci/DOC_GATES.md`
