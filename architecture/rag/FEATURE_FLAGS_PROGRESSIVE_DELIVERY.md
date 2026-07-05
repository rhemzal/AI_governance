# Feature Flags / Progressive Delivery — Advisory Note

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Coverage Level

**Advisory** — The kit covers architectural treatment of feature-flag state (boundaries, determinism, testing). Vendor-specific flag platforms (LaunchDarkly, Unleash, etc.) and release orchestration tooling are out of scope.

## Core Idea

Feature flags and progressive delivery **separate deployment from release**: code ships dark; behavior toggles per environment, cohort, or percentage.

Architecturally, flag evaluation is **hidden state** that changes runtime paths. If not bounded and testable, flags create nondeterminism, stale configuration, and blind spots for AI-assisted changes.

The defining characteristic: **flag state is an integration boundary** — like an external config service — not an inline `if` sprinkled through core logic.

## Why Teams Choose It

- Reduce risk of big-bang releases; roll out to internal users or percentages first.
- Kill-switch dangerous features without redeploying.
- Run experiments (A/B) without permanent branching in business logic.

## When to Choose It

- Releases are decoupled from deploys and you need **controlled exposure** of new behavior.
- You must **disable** a feature quickly when integration or performance risk is high.
- Multiple environments (staging, prod) need **different effective behavior** without divergent codebases.

## When NOT to Choose It

- Simple apps with continuous deploy-equals-release and low blast radius — flag infrastructure adds complexity without payoff.
- Flags would gate **core invariants** or security boundaries — use proper authorization and configuration instead.
- The team cannot commit to **flag lifecycle** (create, default, rollout, remove); permanent flags become undeletable dead code.
- Tests cannot fix or stub flag state deterministically — you will ship untestable combinations.

## Common Failure Modes

- **Flag sprawl**: hundreds of stale flags; no owner, no removal policy; code paths nobody can enumerate.
- **Hidden state in core**: domain logic branches on flag keys directly; AI agents add new branches without updating tests or docs.
- **Nondeterministic tests**: CI flakiness because flag evaluation depends on environment, time, or random percentage without test overrides.
- **Environment skew**: staging does not represent prod flag matrix; “works in staging” is meaningless.
- **Long-lived branches in behavior**: flags meant for rollout persist for years; two implementations of the same feature coexist.
- **Kill-switch surprise**: disabling a flag breaks dependent flows because coupling was implicit.

## Heuristics

- **Centralize evaluation** behind a small port/adapter; core asks “is feature X enabled for this context?” — not “read flag SDK.”
- Define **defaults explicitly** (off vs on) and document them in ADRs for behavior-changing flags.
- Every flag needs a **lifecycle**: owner, rollout plan, removal date or condition, and test matrix (on/off at minimum).
- In automated tests, **pin flag state** — same as mocking an external dependency; never rely on ambient environment.
- Treat flags that change **data writes or contracts** as high-risk: ADR-required, same as API changes.
- Prefer **short-lived rollout flags**; migrate to always-on and delete flag code once stable.
- Log or trace **flag decisions** at integration boundaries when debugging production behavior (which variant ran).

## How This Kit's Boundary Model Applies

- **Core** = business rules that should not depend on deployment mechanics; pass explicit capability/context into core rather than reading global flag state inside domain objects.
- **Boundary contracts** = inputs to core include resolved feature context where needed; contracts stay stable when flags flip.
- **Integration boundaries** = flag provider/SDK, evaluation cache, admin UI; all vendor-specific and environment-specific logic stays here.

Flag evaluation is an **adapter** to external configuration — apply the same discipline as database or HTTP adapters.

## Entry Points in This Kit

- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` §4 (determinism and testability) and §5 (points of no return — long-lived dual code paths)
- `architecture/ARCHITECTURE_DECISION_PROMPT.md` — `Failure zones` and `ADR required` fields
- `architecture/SOLUTION_CLASS_TAXONOMY.md` — cross-cutting concerns table
- `constitution/AI_RULES.md` §1 — treat flag providers as integration boundaries

## Related Documents

- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- `architecture/rag/OBSERVABILITY_AS_ARCHITECTURE.md`
- `architecture/rag/QUALITY_ATTRIBUTES.md`
- `architecture/rag/CONFIG_DRIVEN_PIPELINES.md`
- `constitution/AI_RULES.md`
