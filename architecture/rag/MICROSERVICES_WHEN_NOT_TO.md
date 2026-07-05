# Microservices — When NOT To Choose Them (Advisory)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._


## Core Idea
Multiple independently deployable services communicating over the network.

## Why Teams Want Them
- independent scaling/deploy
- team autonomy (in theory)

## When NOT To Choose Them
- you cannot staff reliable on-call / ops
- you lack observability and incident discipline
- boundaries are unclear or domain language is unstable
- you expect a lot of cross-service transactions

## Common Failure Modes
- distributed monolith (tight coupling over HTTP)
- cascading failures and latency amplification
- data ownership confusion

## Heuristics
- start with a modular monolith, graduate when boundaries and ops maturity exist
- require explicit ownership of data per service

## Related Documents
- `architecture/rag/CONWAYS_LAW.md`
- `architecture/rag/MODULAR_MONOLITH.md`
- `architecture/rag/DISTRIBUTED_MONOLITH.md`
