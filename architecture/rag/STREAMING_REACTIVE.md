# Streaming / Reactive Architecture (Continuous Data Flow) — Advisory Note (Entry Point)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Coverage Level
**Advisory** — The kit's boundary model applies to stream operator design and a Streaming/Reactive column is included in the trade-off matrix. Stream-processing framework specifics (Kafka Streams, Flink, Spark Streaming, Akka Streams, RxJava) are out of scope.

## Core Idea
Streaming/Reactive architecture treats **continuous data flow as the primary paradigm**. The system is built around unbounded sequences of data items (streams) that are transformed, filtered, aggregated, and routed by a pipeline of operators.

### Key distinction from event-driven architecture
- **Event-driven** (which this kit covers): events are an **integration mechanism** between components; individual events represent discrete facts; components are decoupled via event topics/queues.
- **Streaming/Reactive**: continuous data flow **IS the primary paradigm**; the system is designed around stream topology and data transformation semantics (windowing, aggregation, stateful operators).

A system can be both: event-driven for integration between bounded contexts, and streaming internally within a context.

## Why Teams Choose It
- Processing high-throughput, unbounded data streams in near real-time (IoT telemetry, clickstreams, financial ticks).
- Stateful aggregations over time windows (hourly counts, rolling averages, sessionization).
- Continuous ETL (Extract, Transform, Load) pipelines with low latency requirements.
- Reactive UIs and data-binding systems where the UI reacts to data changes automatically.

## When to Choose It
- Data is inherently unbounded (never "done") and must be processed continuously.
- Latency from data arrival to processing must be low (seconds or sub-second).
- Complex aggregation logic over time windows is a core requirement.
- The system needs to handle backpressure: producers can generate data faster than consumers can process it.

## When NOT to Choose It
- Data volumes are low and batch processing is sufficient; streaming adds infrastructure cost and complexity without benefit.
- The problem is fundamentally request/response (synchronous call-response); streaming semantics add unnecessary indirection.
- Team lacks operational expertise for stream-processing platforms; the operational overhead is significant.
- Exactly-once processing semantics are required and cannot be guaranteed by the chosen platform.

## Common Failure Modes
- **Backpressure management failures**: producers outpace consumers; without explicit backpressure signaling (Reactive Streams), buffers overflow or data is silently dropped.
- **Windowing complexity**: time windows (tumbling, sliding, session) interact with out-of-order data and late arrivals in non-obvious ways; incorrect window configuration causes incorrect aggregations.
- **Exactly-once processing**: achieving exactly-once semantics requires coordination between source, processing, and sink; most systems provide at-least-once by default; silent duplicates cause incorrect results.
- **Stateful stream operator management**: stateful operators (aggregations, joins) accumulate state that must be checkpointed, restored on failure, and migrated on topology changes; state management is a major operational concern.
- **Out-of-order data**: event time ≠ processing time; events arrive out of order due to network delays; systems that do not handle watermarks and late data will produce incorrect results.
- **Schema evolution in stream records**: changing the schema of records in a stream breaks downstream consumers that have not yet been updated; without a schema registry and evolution policy, schema changes cause cascading failures.

## Heuristics
- Separate stream topology (operator graph) from business logic (pure transformation functions); test transformation functions independently of the stream runtime.
- Define explicit backpressure semantics before choosing a platform.
- Treat event time vs. processing time as a first-class concern; design watermark policies deliberately.
- Apply the same schema evolution discipline to stream record schemas as to API schemas (see `SCHEMA_EVOLUTION_AND_VERSIONING.md`).
- Design for at-least-once delivery and make downstream processing idempotent; exactly-once is expensive and fragile.

## How This Kit's Boundary Model Applies
- **Core** = stream transformation logic (pure functions: filter, map, aggregate, join); these MUST be deterministic and testable without the stream runtime.
- **Boundary contracts** = stream record schemas (the contract between producers and consumers of a stream).
- **Integration boundaries** = source connectors (reading from Kafka, Kinesis, database CDC) and sink connectors (writing to databases, queues, external APIs).

Stream operator implementations are adapters. Business logic (aggregation rules, enrichment logic) belongs in the core. Source/sink connectors are integration boundaries and should be thin and independently testable.

## Entry Points in This Kit
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` §1 — latency/throughput-centric axis
- `architecture/rag/EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md` — event-driven (the complementary integration pattern)
- `architecture/rag/STATE_VS_EVENT_MODEL.md` — state vs. event reasoning
- `architecture/SOLUTION_CLASS_TAXONOMY.md` — coverage map

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- `architecture/rag/EVENT_DRIVEN_RATIONALE_AND_FAILURE_MODES.md`
- `architecture/rag/STATE_VS_EVENT_MODEL.md`
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`
- `architecture/rag/CONSISTENCY_MODELS.md`
- `constitution/AI_RULES.md`
