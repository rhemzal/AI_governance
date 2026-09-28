# AI Engineering Methods — Agent-First Development Index

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Provide an advisory map of engineering methods that become especially valuable when AI agents inspect repositories, operate tools, observe running systems, implement changes, verify results, and hand work off.

This is not a new mandatory process layer. Normative authority, risk, AEP, verification, and evidence rules remain in `constitution/` and `ci/`.

## Core model

Treat effective AI-assisted development as a feedback system, not a prompt-writing exercise:

```text
task / executable intent
        ↓
agent + repository context
        ↓
tools / runtime interfaces
        ↓
implementation or experiment
        ↓
observable system behavior
        ↓
verification / falsification
        ↓
evidence / handoff
        ↺
```

When repeated agent failures are caused by missing context, weak observability, absent verification, or awkward tooling, improve the engineering environment rather than indefinitely expanding prompts.

## Method selection

| Signal | Prefer | Avoid by default |
| --- | --- | --- |
| Agent repeatedly cannot inspect or verify behavior | Harness engineering | Prompt growth without new signal |
| Running-system state is important | Machine-queryable runtime interaction | Human-only log archaeology |
| Requirement is ambiguous or hard to verify | Executable specification | Large implementation before defining success |
| Correctness can be checked cheaply | Verification-first development | Implement-first, verify-last |
| Repo is hard for a fresh agent to navigate | Agent-legible repository | Giant instruction files |
| Same reliable procedure is repeated | Repo-local skill or deterministic wrapper | Re-prompting the whole procedure |
| A rule must always execute | Deterministic hook/gate | Hoping the model remembers |
| Investigation has independent branches | Bounded subagent delegation | Context-heavy serial exploration |
| Multiple agents write concurrently | Isolated workspaces + integration owner | Shared mutable working tree |
| Model/tool/policy change is proposed | Matched-task agent evaluation | Vibe-based model selection |
| A difficult task exposed recurring friction | Failure-to-harness improvement | Treating every failure as model weakness |

## Method families

### 1. Harness engineering
Design the environment around the agent: repository map, tools, state, runtime access, verification, evidence, limits, and recovery. See [AGENT_HARNESS_ENGINEERING.md](AGENT_HARNESS_ENGINEERING.md).

### 2. Agent-legible repository
Keep authoritative knowledge in repository sources of truth and make it progressively discoverable. Entry instructions should be a map, not a duplicated encyclopedia. Prefer stable commands, explicit contracts, local architecture docs, and searchable task evidence.

### 3. Executable specifications
Turn important acceptance criteria into tests, contracts, scenarios, fixtures, assertions, or measurable budgets where practical. See [SPEC_DRIVEN_AI_DEVELOPMENT.md](SPEC_DRIVEN_AI_DEVELOPMENT.md).

### 4. Verification-first development
Before a non-trivial implementation, identify the cheapest credible way to observe success or failure. If no verification path exists, creating a probe, fixture, contract check, or test harness may be the first engineering step.

### 5. Machine-queryable runtime interaction
Expose development-time state through the narrowest suitable interface: MCP, CLI, diagnostic API/socket, structured logs, traces, metrics, browser/GUI automation, or hardware lab control. MCP is a transport/tool boundary, not the method itself. See [AGENT_RUNTIME_INTERACTION.md](AGENT_RUNTIME_INTERACTION.md).

### 6. Repo-local skills and reusable procedures
A repeated task procedure may become a versioned skill, script, command, or playbook when reuse pays for its maintenance. Keep stable constraints separate from model-specific scaffolding; delete obsolete scaffolding when models/tools improve.

### 7. Deterministic hooks and gates
If an invariant must execute reliably, prefer deterministic enforcement at the appropriate boundary. Examples: formatting after edits, contract validation after schema changes, secret checks before publication, or authority checks around mutating tools. Do not turn every recommendation into a hook.

### 8. Bounded subagent delegation
Delegate independent research or verification when it reduces context pressure or wall time. Give each delegate a bounded objective, inputs, authority, expected evidence, and return contract. The parent/integration owner remains responsible for reconciling contradictory results.

### 9. Isolated parallel execution
Concurrent writers need isolated workspaces or explicit non-overlapping ownership. Git worktrees are one implementation, not a requirement. Shared devices and services require ownership/lease discipline. See [AGENT_PARALLEL_EXECUTION.md](AGENT_PARALLEL_EXECUTION.md).

### 10. Independent falsification review
For selected high-value tasks, a clean-context reviewer can search for counterexamples, unmet acceptance criteria, boundary violations, and unsupported claims. An extra reviewer is not automatically useful; measure it for the task class.

### 11. Agent evaluation
Evaluate model/tool/instruction/harness changes on representative tasks with acceptance criteria and authority boundaries. Track repairs, human intervention, active/lead time, cost when available, and later corrections. See [AGENT_EVALUATION.md](AGENT_EVALUATION.md) and `tooling/BENCHMARK_SCENARIOS.md`.

### 12. Failure-to-harness improvement
Classify recurring agent friction and improve the smallest durable layer:

| Repeated failure | Candidate improvement |
| --- | --- |
| Missing project knowledge | Repo map / canonical docs |
| Cannot inspect state | Probe / logs / trace / runtime interface |
| Cannot tell correct from incorrect | Test / executable spec / oracle |
| Repeats a procedure incorrectly | Skill / script / playbook |
| Misses a mandatory invariant | Hook / gate / wrapper |
| Context overload | Progressive disclosure / delegation |
| Concurrent collisions | Isolated workspace / ownership |
| Environment drift | Reproducible sandbox / fixture |

Do not automatically productize a one-off workaround. Require repeated value or material risk reduction.

## Relationship to existing kit mechanisms

- Authority and bounded autonomy: `constitution/AI_ENFORCEMENT.md`
- Daily repair loop: `constitution/AI_ENFORCEMENT_DAILY.md`
- Proportionality: `constitution/ADAPTIVE_GOVERNANCE.md`
- Debug method selection: `usage/DEBUGGING_INDEX.md`
- Scientific debugging: `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md`
- Test diagnostics: `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`
- Run evidence: `usage/AI_RUN_EVIDENCE.md`
- Model/tool benchmarking: `tooling/BENCHMARK_SCENARIOS.md`
- Productivity calibration: `usage/AI_PRODUCTIVITY_CALIBRATION.md`

## Adoption principle

Adopt methods because they remove a demonstrated bottleneck or reduce concrete risk. Do not require MCP, worktrees, subagents, skills, hooks, or an orchestration framework merely because they are available.

Specify the engineering property first and keep the implementation technology replaceable.
