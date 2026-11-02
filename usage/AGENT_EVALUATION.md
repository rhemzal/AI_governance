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

## Keep the comparison honest

- State the task selection before running. Include failures, timeouts, cancellations and
  review/rework, not only accepted runs. A few tasks can expose a defect but do not establish
  a universal productivity multiplier.
- Hold starting revision, environment, acceptance and allowed effects constant. Record
  model/version, configuration and tools. Avoid learning leakage from one variant into the
  next; use independent clean task state and alternate order when useful.
- Repeat representative cases when agent variability affects the decision. Report the
  number of trials and the budget, not just the best run. One success among many attempts
  answers a different question from consistent first-attempt completion.
- Verify the grader with known-good and known-bad controls. Model-based judgments require
  calibration against accepted/rejected examples; agreement between agents is not proof.
- Separate process compliance, artifact quality, downstream regressions and efficiency.
  Measure human attention separately from elapsed runtime during concurrent work.
- Inspect unnecessary changes and abstraction/maintenance burden, not just passing tests.
  Predeclare what justifies adoption and what would cause rollback or removal.

Use existing task evidence as the seed. A new benchmark service, global dashboard or large
suite is unnecessary until the decisions require it. Published benchmark results and vendor
case studies do not substitute for the project's task mix. Evidence caveats and primary
sources: optional `research/AI_ENGINEERING_METHODS_EVIDENCE.md` in the upstream/research bundle.

## Regression suite principle

A small stable set of representative tasks can become an **agent engineering regression suite**. Use it to detect whether a new model, tool, skill, hook, or instruction projection removes friction without silently reducing correctness.

Do not freeze the suite forever. Add a task when a real failure reveals an important missing capability; retire cases that no longer represent project work.

Theses absorbed from other work are recorded as claim cards. The Claim cards section is the rule; `ci/claim_cards.json` is the checked list.

## Small debugging pilot

Use a few representative historical failures before building a benchmark platform.
Include a product defect and an instrument/environment trap such as a missing fixture,
empty selection, stale report or cancellation that leaves a child alive. Clearly label
synthetic controls; they are useful but not evidence of resolving a historical incident.

Give the agent the symptom, starting revision, allowed effects and acceptance criteria
without leaking the intended patch. Observe whether it selects a useful diagnostic,
distinguishes the cause, produces a minimal reproduction, repairs the right boundary and
verifies the result. Record failures and unnecessary changes as well as successful runs.

A tool response corpus or direct service test verifies that interface; it does not measure
an agent performing this debugging loop. Keep those existing tests and add a small actual
task trial only when evaluating the agent workflow. If runtime access is unavailable,
report that limitation; a simulation is not a live integration result.

Compare accepted outcomes first, then reproduction attempts, repair iterations, human
interventions and measured effort. Small pilot results support a local adoption decision,
not a general productivity claim.

## Claim cards

A thesis that this kit absorbs gets one card in `ci/claim_cards.json`. The checker is `ci/validate_claim_cards.py`. It checks the card's shape and the promotion rules below. It does not run scenarios, and it does not read `constitution/` looking for new sentences.

The oracle is the kind of check that could falsify the claim:

- `canary` — a planted violation exercised by a test under `ci/gate_tests/`
- `declaration` — a shape or presence check; a matching document can still be untrue
- `scenario` — a bounded task whose acceptance is fixed before the run
- `none` — no executable check; the card keeps the gap visible

Record what a hollow pass looks like in `known_pass_that_is_not_proof`. `path` points at the evidence file, and `anchor` is a sentence or test line that must remain in that file.

Promotion, as enforced by the checker:

- `none` stays `research` or `advisory`, and `open`
- `integrated` is a `canary` whose path is a `ci/gate_tests/*.py` file and whose anchor is a `def test_` line that unittest collects from that file. A comment, string, bare function, collected method that does not assert, or an assertion made only of literals does not count. A name assigned from a literal in that same straight-line block counts as a literal. The checker does not run the test. A value produced by a call can still be constant at runtime.
- `normative` is allowed only as that integrated canary
- a `scenario` may be `open` or `probed`, and it is not `integrated`

Copy a thesis into `constitution/`, or into a new required CI check, only together with a normative integrated canary. Until that card exists, keep the thesis in `research/` or in advisory `usage/`. The checker rejects a normative card that has no canary. An unregistered constitution edit can still merge; that limit is card `unregistered-constitution-sentence` and `adr/ADR_0014_Claim_Card_Registry.md`.

The initial cards are limits this repo already states. Their recorded status stays until the evidence anchor and `ci/gate_tests/test_claim_cards.py` change together. Adding a thesis means adding a card in the same registry. A rejected external project that copies nothing into `constitution/` or required CI does not need a card.

## Independent evaluator

A second agent or reviewer is optional. Use it when it improves detection of unsupported claims or unmet criteria for the task class. Measure the extra cost and false-positive burden.

## Related Documents

- [AI Engineering Methods](AI_ENGINEERING_METHODS.md)
- [Agent Harness Engineering](AGENT_HARNESS_ENGINEERING.md)
- `tooling/BENCHMARK_SCENARIOS.md`
- `tooling/AI_TOOL_OPTIMIZATION.md`
- `usage/AI_PRODUCTIVITY_CALIBRATION.md`
- `ci/claim_cards.json`
- `adr/ADR_0014_Claim_Card_Registry.md`
