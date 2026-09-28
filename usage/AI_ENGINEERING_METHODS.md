# AI Engineering Methods — Agent-First Development Index

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If copied, preserve this line._

## Purpose and authority

Select the smallest method that improves an observable engineering outcome. This selector
is advisory; the behavioral minimum is `constitution/AI_RULES.md` §6.5. It requires a
proportionate rationale and evidence, not a particular tool, framework or new CI gate.

Both this selector and [Engineering Methods Adoption](ENGINEERING_METHODS_ADOPTION.md)
are in **minimal**. Focused guides named below are **standard** / optional upstream context
from the same pinned revision. Research is optional in `research/AI_ENGINEERING_METHODS_EVIDENCE.md`;
`tooling/` references are upstream-only (not included by the copy-import manifest).
Do not load missing optional guides or the whole catalog for every task.

## Start with a decision, not a catalog

For non-trivial work, use existing AEP discovery/reason/verification/acceptance fields:

1. **Observe:** what fails or costs effort, on which revision/environment? Separate facts
   from assumptions. If no baseline can run, name the gap.
2. **Define success:** what observation could distinguish a fix from an attractive but
   incorrect implementation? Preserve relevant compatibility and authority boundaries.
3. **Choose:** keep the current mechanism, extend it, or add one capability. State why
   the smallest option suffices and what evidence would change the decision.
4. **Verify and learn:** compare behavior, disclose limits, and keep/change/remove the
   method according to benefit and maintenance cost.

Start with **one primary method and at most one supporting method** as a working budget,
not a quota. Expand only for a concrete unresolved risk. Routine reversible edits need
only the existing concise scope/verification statement. No reasoning transcript is required.

## Method selection

| Observed need | Smallest candidate / optional focused guide | Evidence it helps | Defer / stop when |
| --- | --- | --- | --- |
| Repeated inability to inspect or verify behavior | Repair the missing harness capability; `AGENT_HARNESS_ENGINEERING.md` | A representative task now reaches a credible observation | No recurring friction or material risk; existing tool suffices |
| Fresh agent misses a non-obvious command or constraint | Short active instruction pointer, task-scoped retrieval | Fresh task finds and uses the correct source/command | More context merely repeats discoverable code or rules |
| Ambiguous requirement / weak correctness oracle | Example, contract, property or executable scenario; `SPEC_DRIVEN_AI_DEVELOPMENT.md` | Known-bad behavior fails and accepted behavior passes | Full spec framework adds no useful discrimination |
| Existing behavior must survive a legacy change | Characterization plus contract/differential verification | Intentional differences are explained; compatibility controls pass | Snapshot just blesses an existing defect |
| Runtime, GUI or device state matters | Narrow CLI/log/socket/API probe; `AGENT_RUNTIME_INTERACTION.md` | Same signal reproduced before/after on relevant runtime | New MCP endpoint adds access surface without diagnostic value |
| A reliable procedure repeats | Existing command, then small wrapper or skill | Fewer procedural failures on comparable tasks | One-off task, redundant abstraction or stale model workaround |
| Stable invariant is repeatedly violated | Existing deterministic verifier; scoped gate when justified | Positive and negative controls; bounded noise/runtime | Rule has no reliable oracle or creates only declaration theater |
| Investigation has independent branches | Bounded delegation if authorized; `AGENT_PARALLEL_EXECUTION.md` | More useful evidence after integration cost | Dependency, shared mutation or coordination dominates |
| Concurrent writers / shared runtime | Isolated workspaces and explicit resource ownership | Integrated revision verifies; resources are released | Isolation costs more than serial work; worktrees alone do not isolate services |
| Self-review misses defects | Independent falsification check for selected risk | Concrete counterexample or detection benefit | Reviewer repeats the same assumptions or generates low-value noise |
| Model/tool/instructions change | Matched representative tasks; `AGENT_EVALUATION.md` | Acceptance first; repair, review, time/cost second | Tiny/cherry-picked sample is presented as a general gain |
| Context loss / resumed work | Compact task state and actual-state reconciliation | Next session resumes without replaying or duplicating effects | Another state file duplicates the existing tracker |
| Harness complexity grows | Remove one redundant component and compare | Required outcomes preserved with lower burden | Removal weakens permissions, required checks or useful signal |

Most underlying techniques predate AI. The shift is that agents also operate the feedback
loop: intent, context, tools, observable behavior, verification and recovery. Keep product
contracts independent of a particular agent implementation.

## Reasoning quality and verification

A method choice should connect **observed problem → intervention → expected signal →
acceptance → cost/retirement condition**. If the expected signal is absent, revisit the
hypothesis. More explanation, generated code, tests or agent votes is not evidence by itself.

For consequential changes, check a plausible alternative explanation or counterexample.
Prefer a source of expected behavior independent of the newly generated implementation.
A clean-context reviewer may help; it is not automatically an independent oracle.
Do not force a new test onto a trivial prose edit or repeatedly run unrelated suites.

## Adoption in existing projects

Use [the rollout guide](ENGINEERING_METHODS_ADOPTION.md): inspect the actual pin and host
instructions, establish one baseline, pilot one slice, promote a proven outcome locally,
and periodically retire ineffective scaffolding. Existing debt is explicit; new violations
are not hidden by a lower total count. Never use an advisory method or legacy baseline to
silently override a mandatory rule.

Tool availability does not expand authority. Method uptake is demonstrated by actual task
behavior and verified outcomes, not imported files, an adoption badge or a self-report.

## Related Documents

- [Existing-project adoption](ENGINEERING_METHODS_ADOPTION.md)
- Baseline: `constitution/AI_RULES.md`, `constitution/AI_ENFORCEMENT.md`,
  `constitution/ADAPTIVE_GOVERNANCE.md`, `usage/AEP_VALIDATION.md`
- Standard / optional upstream: `usage/AGENT_HARNESS_ENGINEERING.md`,
  `usage/AGENT_RUNTIME_INTERACTION.md`, `usage/SPEC_DRIVEN_AI_DEVELOPMENT.md`,
  `usage/AGENT_PARALLEL_EXECUTION.md`, `usage/AGENT_EVALUATION.md`,
  `usage/DEBUGGING_INDEX.md`, `usage/AI_RUN_EVIDENCE.md`,
  `usage/AI_PRODUCTIVITY_CALIBRATION.md`
- Optional research: `research/AI_ENGINEERING_METHODS_EVIDENCE.md`
- Upstream-only: `tooling/BENCHMARK_SCENARIOS.md`
