# Conway’s Law — Advisory Note

## Core Idea
System design tends to mirror the communication structure of the organization.

## Practical Heuristics
- If teams are independent, modular boundaries are easier to enforce.
- If teams are coupled, the architecture will drift toward coupling.

## What This Suggests Architecturally
- Pick boundaries that match ownership and deploy/release processes.
- If you cannot staff independent ownership, avoid premature microservices.

## When This Fails / Failure Modes
- Reorgs happen frequently; architecture becomes a moving target.
- “Team boundaries” are unclear; ownership conflicts produce boundary violations.
