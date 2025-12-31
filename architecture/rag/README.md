# RAG Notes (Advisory)

## Purpose
Short, curated theory notes to support architecture reasoning.

Rules:
- Advisory only (see `adr/ADR_0003_RAG_Is_Advisory_Not_Normative.md`).
- Each note includes failure modes (“when this fails”).
- Prefer actionable heuristics over academic depth.
- Prefer extending an existing note over creating a new micro-note.

Recommended usage:
- Link the note in an ADR when its concept is used.
- Never treat notes as authority; treat them as prompts for better reasoning.

Related documents:
- `adr/ADR_0003_RAG_Is_Advisory_Not_Normative.md`
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`

## Notes Index
Architecture styles:
- [HEXAGONAL_RATIONALE_AND_FAILURE_MODES.md](HEXAGONAL_RATIONALE_AND_FAILURE_MODES.md)
- [LAYERED_RATIONALE_AND_FAILURE_MODES.md](LAYERED_RATIONALE_AND_FAILURE_MODES.md)
- [EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md](EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md)
- [MODULAR_MONOLITH.md](MODULAR_MONOLITH.md)
- [MICROSERVICES_WHEN_NOT_TO.md](MICROSERVICES_WHEN_NOT_TO.md)
- [DISTRIBUTED_MONOLITH.md](DISTRIBUTED_MONOLITH.md)
- [CQRS_WHEN_AND_WHEN_NOT.md](CQRS_WHEN_AND_WHEN_NOT.md)

Data & consistency:
- [STATE_VS_EVENT_MODEL.md](STATE_VS_EVENT_MODEL.md)
- [CONSISTENCY_MODELS.md](CONSISTENCY_MODELS.md)
- [DATA_STORE_SELECTION.md](DATA_STORE_SELECTION.md)
- [SCHEMA_EVOLUTION_AND_VERSIONING.md](SCHEMA_EVOLUTION_AND_VERSIONING.md)

General theory & decision support:
- [QUALITY_ATTRIBUTES.md](QUALITY_ATTRIBUTES.md)
- [INFORMATION_HIDING.md](INFORMATION_HIDING.md)
- [CONWAYS_LAW.md](CONWAYS_LAW.md)
- [MEASURED_PERFORMANCE.md](MEASURED_PERFORMANCE.md)
