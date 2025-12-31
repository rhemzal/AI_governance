# Layered Architecture — Rationale and Failure Modes (Advisory)

## Core Idea
Organize code into layers with a clear dependency direction (outer → inner). Often:
- interface/presentation
- application/service
- domain
- infrastructure

## Why It Helps
- low cognitive load and easy onboarding
- clear separation of concerns when enforced
- works well for many CRUD (Create, Read, Update, Delete) / business apps

## When to Choose It
- the domain is not extremely complex
- you want a simple default structure
- you can enforce dependency direction

## Common Failure Modes
- “everything goes in service layer” → the layer becomes a dumping ground
- dependency direction not enforced → random coupling across layers
- domain becomes infrastructure-shaped (ORM leakage: Object-Relational Mapper concerns bleed into the domain model)

## Heuristics
- enforce import rules (CI gate)
- keep domain logic independent of IO even in layered style

## Related Documents
- `architecture/ARCHITECTURE_STYLE_MATRIX.md`
- `ci/ARCHITECTURE_GATES.md`
