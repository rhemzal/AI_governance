# ADR 0003: RAG Notes Are Advisory, Not Normative

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status
Accepted

## Context
LLMs can produce plausible but ungrounded architectural explanations.
Curated theory notes (RAG-style) help:
- reduce reliance on a model’s training set
- keep trade-offs consistent

However, a RAG corpus can also become a false authority.

## Decision
Content in `architecture/rag/` is **advisory**.

- Governance rules live in `constitution/` and are normative.
- Decision guidance lives in `architecture/` and is process-normative.
- RAG notes explain concepts and trade-offs, but MUST NOT override governance.

## Consequences
- We can ground reasoning in stable concepts without turning references into dogma.

## Enforcement
- Any AI reasoning that uses RAG notes MUST cite the concept used and explain its relevance.
- RAG notes MUST include “when this fails” / failure modes.
