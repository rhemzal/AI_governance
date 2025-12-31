# Modular Monolith — Advisory Note

## Core Idea
A single deployable unit with strong internal module boundaries.

## Why It Helps
- avoids distributed-systems complexity
- enables strong boundaries and team ownership
- easier local dev and testing than microservices

## When to Choose It
- you want modularity but don’t need independent deployment yet
- team size/ops maturity is limited

## Common Failure Modes
- “monolith” without modules → big ball of mud
- shared database tables across modules without ownership

## Heuristics
- enforce module boundaries with CI
- define module ownership and contracts

## Related Documents
- `ci/ARCHITECTURE_GATES.md`
