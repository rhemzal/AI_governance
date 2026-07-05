# RAG Notes (Advisory)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._


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
- [SERVERLESS_FAAS.md](SERVERLESS_FAAS.md) _(Advisory)_
- [ORCHESTRATION_SAGA_WORKFLOW.md](ORCHESTRATION_SAGA_WORKFLOW.md) _(Advisory)_
- [STREAMING_REACTIVE.md](STREAMING_REACTIVE.md) _(Advisory)_

Pipeline & catalog patterns:
- [CONFIG_DRIVEN_PIPELINES.md](CONFIG_DRIVEN_PIPELINES.md)
- [PIPELINE_BATCH.md](PIPELINE_BATCH.md)
- [TEMPLATE_CATALOG.md](TEMPLATE_CATALOG.md)

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

Additional solution classes (Acknowledged — entry-point notes):
- [PLUGIN_EXTENSION_ARCHITECTURE.md](PLUGIN_EXTENSION_ARCHITECTURE.md)
- [EDGE_MULTI_TIER_DEPLOYMENT.md](EDGE_MULTI_TIER_DEPLOYMENT.md)

Repo & project structure patterns (Acknowledged — entry-point notes):
- [MONOREPO_PATTERNS.md](MONOREPO_PATTERNS.md)
- [LIBRARY_SDK_REPO.md](LIBRARY_SDK_REPO.md)
- [CONTRACT_FIRST_API_FIRST.md](CONTRACT_FIRST_API_FIRST.md)

Coverage map & taxonomy:
- [SOLUTION_CLASS_TAXONOMY.md](../SOLUTION_CLASS_TAXONOMY.md)
