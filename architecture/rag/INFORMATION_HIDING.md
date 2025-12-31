# Information Hiding (Parnas) — Advisory Note

## Core Idea
Design modules so that **volatile decisions are hidden** behind stable interfaces.
A “secret” is any design choice likely to change.

## Practical Heuristics
- Put volatility at the edges: protocols, persistence, vendors, UIs.
- Keep the core stable: domain rules, invariants, policies.
- If a change forces edits across many modules, information hiding is failing.

## What This Suggests Architecturally
- Clear boundaries and boundary contracts (ports/interfaces) help isolate change.
- Dependency direction should point toward stable policy.

## When This Fails / Failure Modes
- The team cannot identify what is volatile (wrong stability assumptions).
- Premature abstraction: hiding “secrets” that are not actually volatile.
- Performance constraints force leaky abstractions (e.g., query patterns crossing boundaries).
