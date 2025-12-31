# Hexagonal Architecture — Rationale and Failure Modes (Advisory)

## Core Idea
Protect the core (domain/application) from volatility at the edges by using **ports** and **adapters**.

## Why It Helps
- Testability: core logic can be tested without IO.
- Modifiability: swap adapters without rewriting policy.
- Explicit contracts: ports define what the core needs.

## Common Failure Modes
- “Everything is a port” → complexity explosion.
- Adapters bypass ports “just this once” → boundary erosion.
- Domain becomes persistence-shaped (ORM leakage: Object-Relational Mapper concerns bleed into the domain model).
- Overkill for simple CRUD (Create, Read, Update, Delete) where domain rules are thin.

## Heuristics
- Introduce ports only at volatility points.
- Keep adapter logic thin and focused on translation.
- Treat interface layer as an adapter (GUI/CLI/TUI/headless).
