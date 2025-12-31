# ADR 0004: Tooling Optimization Is Experimental

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status
Accepted

## Context
Tooling (models, agents, IDE features) evolves quickly.
If tooling choices become “law”, teams may optimize for tool convenience instead of system correctness.

## Decision
Tooling protocols in `tooling/` are **experimental and advisory**.
They may recommend workflows, experiments, and benchmarks, but they MUST NOT override:
- governance rules (`constitution/`)
- architecture decision process (`architecture/`)

## Consequences
- We keep the project tool-agnostic.
- We can still run systematic experiments and iterate.

## Enforcement
- Tooling changes do not change rules; rules change only via ADRs.
