# Pipeline / Batch Architecture — Advisory Note

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Coverage Level
**Advisory** — The kit's trade-off matrix includes a Pipeline/Batch column. The boundary model applies to operator/stage design. Pipeline-framework-specific tooling (Apache Beam, Spark, dbt, Airflow) and scheduler infrastructure are out of scope.

## Core Idea
Pipeline/Batch architecture organizes a system as a **sequence of discrete processing stages** that transform data from a source to a sink. Each stage accepts an input, applies a transformation, and passes the result to the next stage. The execution is **bounded**: there is a defined start, a finite input set, and a clear completion point.

The defining characteristic is that **data flows through the pipeline in finite chunks (batches)**, as opposed to the continuous, unbounded data flow of streaming architectures.

## Why Teams Choose It
- Simple mental model: data enters, transformations are applied in order, results are produced.
- Easy to test: each stage is a pure transformation on a finite input; stages can be tested independently.
- Predictable resource usage: batch runs have a defined scope; resource consumption is bounded and plannable.
- Decoupled stages: a stage only depends on its input contract, not on the other stages' implementations.
- Operationally mature: scheduling, retry, and monitoring tooling (cron, Airflow, dbt, Spark) is well-established.

## When to Choose It
- Bulk data processing that does not need to react to events in real time (ETL, nightly reports, data migrations).
- Workflows where the full input set is known before processing begins (file ingestion, daily database snapshots).
- AI/ML training pipelines where stages (preprocessing, feature engineering, training, evaluation) must run in order with checkpoints.
- Systems where reproducibility and auditability of each processing run are important.

## When NOT to Choose It
- When results must be available within seconds of data arriving — use Streaming/Reactive instead.
- When the input data is unbounded and never "complete" (IoT telemetry, user clickstreams).
- When stages have complex interdependencies that are not expressible as a linear or DAG flow — consider an Orchestration/Saga approach.
- When per-record latency matters more than throughput — batch introduces inherent latency equal to the scheduling interval.

## Common Failure Modes
- **Accidental statefulness between runs**: a stage leaks state across batch executions (shared files, global variables), causing non-idempotent, order-dependent results.
- **Monolithic pipeline**: all stages are fused into a single script or function with no separation of concerns; impossible to test or reuse stages individually.
- **No idempotency**: re-running a failed batch produces duplicate records or corrupted state instead of safely resuming.
- **Schema drift at stage boundaries**: upstream stage changes its output schema; downstream stage breaks silently at runtime.
- **Unmonitored silent failure**: a stage completes with exit code 0 but produces empty or incorrect output; downstream stages process the wrong data without error.
- **Excessive batch size**: a single batch processes too much data, making failures expensive and recovery slow; lack of checkpointing means re-processing from scratch.

## Heuristics
- Design each stage as a **pure transformation**: given the same input, always produce the same output. This enables safe retry and reproducible runs.
- Validate input schema at each stage boundary before processing begins (fail-fast at the boundary, not mid-run).
- Make every batch run **idempotent**: running it twice should produce the same result as running it once (use upsert/overwrite semantics, not append-only).
- Checkpoint between stages: write intermediate results durably so that a failure in a later stage does not require re-running earlier stages.
- Emit explicit run metadata (record counts, checksums, run ID, timestamp) as a contract artifact for each run.

## How This Kit's Boundary Model Applies
The kit's boundary model (`AI_RULES.md` §1) maps onto pipeline stages cleanly:
- **Core** = the transformation logic within each stage (pure functions: filter, map, aggregate, validate). These MUST be deterministic and independently testable without the pipeline runner.
- **Boundary contracts** = the schema of data flowing between stages (the "port" between a producer stage and a consumer stage). Treat inter-stage schemas with the same discipline as API contracts (see `SCHEMA_EVOLUTION_AND_VERSIONING.md`).
- **Integration boundaries** = source connectors (reading from databases, files, cloud storage) and sink connectors (writing results to databases, object stores, downstream queues). These are adapters and should be thin and independently testable.

Each pipeline stage is an adapter/operator. Keep business/transformation logic in the core. Source/sink I/O belongs in integration boundaries.

## Entry Points in This Kit
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` §1 — workflow-centric axis (pipeline/batch is a workflow)
- `architecture/ARCHITECTURE_STYLE_MATRIX.md` — trade-off comparison including Pipeline/Batch column
- `architecture/rag/CONFIG_DRIVEN_PIPELINES.md` — declarative variant where the pipeline topology is expressed in configuration
- `architecture/SOLUTION_CLASS_TAXONOMY.md` — coverage map

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/ARCHITECTURE_STYLE_MATRIX.md`
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- `architecture/rag/CONFIG_DRIVEN_PIPELINES.md`
- `architecture/rag/STREAMING_REACTIVE.md`
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`
- `architecture/rag/STATE_VS_EVENT_MODEL.md`
- `constitution/AI_RULES.md`
