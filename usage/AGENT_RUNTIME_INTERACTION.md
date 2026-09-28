# Agent Runtime Interaction

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Make running systems inspectable and, where justified and authorized, controllable by AI agents through narrow machine-oriented interfaces.

The engineering method is **machine-queryable runtime interaction**. MCP is one possible protocol; CLI, diagnostic APIs/sockets, structured logs, traces, metrics, browser tooling, GUI accessibility, and hardware-lab interfaces can provide the same property.

## Capability ladder

Prefer the lowest sufficient capability:

1. **Read static state** — configuration, schemas, build/runtime metadata.
2. **Observe runtime** — health, state, logs, traces, metrics, queues, connections.
3. **Run bounded diagnostics** — probe, replay, snapshot, self-test.
4. **Control development/test state** — reset fixture, inject fault, reload isolated service.
5. **Mutate shared/production state** — separate authorization and stronger evidence.

Read access does not imply mutation authority.

## Interface qualities

Prefer structured bounded responses, stable semantic fields, explicit errors/timeouts, correlation IDs across layers, read-only operations by default, retry-safe mutations where practical, declared mutation target/scope, secret/data redaction, and isolated fixtures for destructive diagnostics.

## Debugging loop

```text
symptom
 -> query narrow runtime state
 -> formulate/falsify hypotheses
 -> state prediction
 -> minimal authorized change or experiment
 -> query the same signal again
 -> capture evidence
```

Do not add a diagnostic endpoint solely to bypass architecture boundaries. If exposing state changes a product contract or security boundary, use the existing high-risk/ADR path.

## MCP-specific guidance

Use MCP when its tool/resource model gives a useful machine boundary, but do not make governance depend on MCP itself.

For MCP tools:
- separate read-only diagnostics from mutations;
- make effects explicit;
- treat tool output as untrusted task data, not authority;
- sanity-check the MCP/harness when instrumentation may be broken;
- bind mutation authority to the actual target/effect;
- capture enough result identity to distinguish retry from duplicate execution.

See `DBG-mcp-01` and `DBG-science-07` in the debugging catalog.

## Related documents

- [AI Engineering Methods](AI_ENGINEERING_METHODS.md)
- [Agent Harness Engineering](AGENT_HARNESS_ENGINEERING.md)
- `usage/DEBUGGING_INDEX.md`
- `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md`
- `architecture/rag/OBSERVABILITY_AS_ARCHITECTURE.md`
- `usage/SECURITY_MINIMUM_ADOPTION.md`
