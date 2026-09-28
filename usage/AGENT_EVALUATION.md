# Agent Evaluation — Engineering Regression Tasks

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Evaluate changes to models, tools, instructions, skills, hooks, harnesses, or autonomy using representative engineering tasks rather than subjective impressions.

This document complements `tooling/BENCHMARK_SCENARIOS.md`; it does not create a mandatory benchmark suite for every adopter.

## Evaluation unit

A useful task case contains:

```text
task id / class
starting revision or fixture
bounded objective
acceptance criteria
allowed effects
verification path
expected evidence
optional known traps
```

Do not encode the intended implementation when alternative correct solutions are acceptable.

## Candidate task classes

- local bug fix;
- local feature;
- test/harness repair;
- API or adapter boundary change;
- cross-cutting change;
- runtime diagnosis;
- GUI diagnosis;
- regression localization;
- documentation/governance task.

Projects should choose tasks representative of their actual work.

## Measurements

Prefer directly observed measurements:
- acceptance criteria satisfied/unmet;
- authority boundary respected/violated;
- verification completed/unverified;
- repair iterations;
- necessary and unnecessary human interventions;
- active agent time and lead time when measurable;
- cost/token use when available;
- unnecessary diff/scope expansion;
- later corrections or regressions.

Never invent missing human baselines or costs.

## Matched-task comparison

When comparing two harness/model/policy variants:
1. use equivalent starting state and task;
2. keep acceptance criteria and authority constant;
3. change the intended variable where practical;
4. record environmental differences;
5. compare task outcomes before efficiency metrics;
6. call small samples preliminary.

Quality and authority are acceptance conditions; lower cost or time does not compensate for incorrect or unauthorized work.

## Regression suite principle

A small stable set of representative tasks can become an **agent engineering regression suite**. Use it to detect whether a new model, tool, skill, hook, or instruction projection removes friction without silently reducing correctness.

Do not freeze the suite forever. Add a task when a real failure reveals an important missing capability; retire cases that no longer represent project work.

## Independent evaluator

A second agent or reviewer is optional. Use it when it improves detection of unsupported claims or unmet criteria for the task class. Measure the extra cost and false-positive burden.

## Related documents

- [AI Engineering Methods](AI_ENGINEERING_METHODS.md)
- [Agent Harness Engineering](AGENT_HARNESS_ENGINEERING.md)
- `tooling/BENCHMARK_SCENARIOS.md`
- `tooling/AI_TOOL_OPTIMIZATION.md`
- `usage/AI_PRODUCTIVITY_CALIBRATION.md`
