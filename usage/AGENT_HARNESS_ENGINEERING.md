# Agent Harness Engineering

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Treat the agent's environment as an engineering surface. A harness is the environment and control loop around an agent: context, tools, state, execution limits, runtime access, verification, evidence, and recovery.

This document is advisory. It does not introduce an orchestration platform requirement.

## Harness layers

A useful harness can provide, as needed:

1. **Intent** — bounded objective and acceptance criteria.
2. **Navigation** — repository map and canonical sources of truth.
3. **Tools** — file, code, test, runtime, browser, MCP, lab, or deployment interfaces appropriate to the mandate.
4. **Isolation** — sandbox/workspace/resource ownership.
5. **Observation** — structured failures, logs, traces, metrics, screenshots, state queries.
6. **Verification** — deterministic tests, contracts, scenarios, measurable budgets.
7. **Repair loop** — bounded diagnose → predict → change → rerun.
8. **Continuity** — compact task state, revision binding, resume/handoff.
9. **Evidence** — what was tested, where, and with what result.
10. **Authority** — technical capability never expands authorized effects.

## Harness-first diagnostic

When an agent repeatedly fails, classify the deficiency before adding prompt text:

```text
knowledge?      -> repository source of truth / map
navigation?     -> discoverability / stable entry point
tool access?    -> CLI / API / MCP / skill
visibility?     -> probe / structured logs / traces / metrics
oracle?         -> test / contract / executable specification
repeatability?  -> fixture / sandbox / record-replay
procedure?      -> script / skill / playbook
mandatory rule? -> hook / gate / wrapper
context load?   -> progressive disclosure / bounded delegation
concurrency?    -> isolation / ownership / lease
```

Improve the smallest durable layer that explains repeated friction.

## Progressive disclosure

Do not front-load every document, rule, trace, and tool description into agent context. Prefer a small entry map that points to task-relevant sources of truth and loads deeper playbooks only when triggered.

## Verification ergonomics

Codebases used by agents benefit from cheap, composable verification: stable repo-local commands, smallest-scope tests before full suites, machine-readable status and diagnostics, deterministic fixtures, explicit timeouts, measurable budgets where meaningful, and reproducible field failures.

A harness should make the correct action easier, not merely document it.

## Harness debt

Warning signs include duplicated canonical docs, obsolete model workarounds, hooks with no material risk benefit, agent-specific APIs leaking into product contracts, test-only paths diverging from production semantics, and overlapping mutation authority.

Periodically remove one redundant scaffold at a time and evaluate the effect with matched tasks.

## Evidence

```text
HARNESS CHANGE EVIDENCE
- Task class / observed friction:
- Existing failure mode:
- Harness layer changed:
- New capability or signal:
- Representative verification:
- Authority/security impact:
- Maintenance cost:
- Re-evaluation trigger:
```

## Related documents

- [AI Engineering Methods](AI_ENGINEERING_METHODS.md)
- [Agent Runtime Interaction](AGENT_RUNTIME_INTERACTION.md)
- [Agent Evaluation](AGENT_EVALUATION.md)
- `constitution/AI_ENFORCEMENT.md`
- `tooling/AI_TOOL_OPTIMIZATION.md`
- `tooling/BENCHMARK_SCENARIOS.md`
