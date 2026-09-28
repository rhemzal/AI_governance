# AI Engineering Methods: Evidence and Adoption Decisions

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If copied, preserve this line._

## Scope and research method

Reviewed **2026-09-28**, following PR #38 at `e33cc87dc1fa98bed0a74bf50a0e589c85ff2da6`.
This is advisory research, not a new source of mandatory policy.

Question: which changes improve reasoning, accepted software quality, and adoption in
existing repositories, at a maintenance cost appropriate to the project?

The review sampled primary empirical studies, vendor engineering reports, and maintained
implementation documentation. It sought both supporting and contrary evidence for context,
specification, execution, evaluation, and adoption. This is a targeted review, not an exhaustive
systematic survey. Vendor reports demonstrate feasibility; they do not establish universal
causal effects. Observational throughput studies do not establish product quality. Distinguish
the source's result from the **kit adaptation** below. Recheck live documentation when upgrading.

## Evidence ledger

| ID / primary source | What the source supports | Limit / contrary evidence | Kit adaptation |
| --- | --- | --- | --- |
| E1 — [OpenAI, Harness engineering, 2026-02-11](https://openai.com/index/harness-engineering/) | An agent-built product used repository knowledge, inspectable runtime state, and mechanical boundary checks. | Greenfield internal case study. Its estimated speedup, architecture, merge policy and cleanup machinery cannot be transferred as proven defaults to legacy products. | Trial the missing feedback capability on one existing slice; preserve the host's architecture and release controls. |
| E2 — [Anthropic, Effective harnesses for long-running agents, 2025-11-26](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Incremental progress and durable handoff artifacts help work span context windows. | A particular harness/model setup, not proof every task needs initializer agents or extra state files. | Reuse the existing task record for resumable work; verify actual state on resume. |
| E3 — [Anthropic, Harness design, 2026-03-24](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Evaluator feedback and observable acceptance exposed application defects. The author removed some scaffolding as models improved. | Qualitative application experiments; larger scope and budgets complicate comparisons. Evaluators required calibration and still missed bugs. | Test both adding and removing a component. Extra reviewers are a task-dependent cost, not an unconditional quality multiplier. |
| E4 — [Anthropic, Context engineering, 2025-09-29](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Selective retrieval, compact state, and carefully scoped tools are practical ways to manage limited context. | Engineering guidance, not a controlled proof that any repository map improves task success. | Keep unusual commands/constraints discoverable; retrieve evidence for the current question, not the entire corpus. |
| E5 — [Gloaguen et al., Evaluating AGENTS.md, v2, 2026-06-23](https://arxiv.org/abs/2602.11988v2) | Across studied agents/tasks, context files did not generally improve success and increased inference cost by over 20% on average. Non-standard practices remained a useful purpose. | Benchmark and repository selection limit generalization. This does not justify removing safety requirements or all instructions. | Evaluate instruction changes; avoid automatically generated repository summaries and repeated rules. Retain task-critical constraints. |
| E6 — [METR, experienced developer randomized study, 2025-07-10](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) | Sixteen developers working on 246 tasks in familiar mature repositories took 19% longer with the studied early-2025 tools. Perceived gains differed from measurement. | Specific developers, tools and period; not a claim about all agents or current productivity. | Include review, repair and integration in the local baseline, not just generation speed. |
| E7 — [METR, experiment-design update, 2026-02-24](https://metr.org/blog/2026-02-24-uplift-update/) | Later data suggested improvement, but participation/task selection and concurrent time measurement made the effect unreliable. | Neither the old slowdown nor the newer raw estimates are a current universal multiplier. | Retain failed/cancelled tasks and selection caveats; separate elapsed time from human attention. |
| E8 — [Murphy-Hill et al., Microsoft CLI rollout, 2026-07-01](https://arxiv.org/abs/2607.01418) | The observational rollout study reports approximately 24% more merged PRs among adopters; peer usage helped adoption. | PRs are an output proxy, explicitly not delivered value. Organizational rollout evidence is not a controlled method comparison. | Make a useful pilot discoverable to peers; judge acceptance, regressions and rework alongside throughput. |
| E9 — [Anthropic, Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Outcome-based grading, regression versus capability cases, and repeated trials expose different aspects of reliability. | Model graders need calibration; success in one of many attempts differs from consistent success. | Pair known-good and known-bad controls; keep the acceptance oracle separate from self-assessment and record all trials. |
| E10 — [GitHub Spec Kit, maintained repository](https://github.com/github/spec-kit) | Implements specification/planning and distinct bug-fixing and assessment entry points. | Tool documentation demonstrates an available implementation, not comparative productivity or correctness evidence. | Reuse existing issues/contracts/tests; do not require a second constitution or spec workflow for each bug fix. |
| E11 — [GitLab AI-assisted development playbook](https://handbook.gitlab.com/handbook/engineering/workflow/ai-assisted-development/) | A practical organizational model connecting agent work, harness readiness and verification. | Organizational policy is not a universal requirement for solo or legacy projects. | Keep the verification principle; adapt the process to G/CM and the available host commands. |

## What changes the quality of reasoning

These are kit design inferences, not measured effect sizes:

| Failure in reasoning | Smallest intervention | Disconfirming observation / stop condition |
| --- | --- | --- |
| First plausible explanation becomes the fix | Separate observed facts, assumptions and one competing explanation; choose a discriminating probe | The predicted signal does not change: reject or revise the hypothesis, not the acceptance criterion |
| Code and generated tests share the same mistaken interpretation | Derive an oracle from a contract, reported failure, independent implementation or known-good behavior | A deliberately wrong result passes: repair the oracle before relying on it |
| Design is elaborate because the agent can generate it | Compare the existing mechanism, one small extension and any proposed new component | No concrete failure/risk requires the component: defer it |
| Old behavior is mistaken for intended behavior | Characterize the touched boundary, then distinguish compatibility commitments from defects | A recorded output conflicts with the agreed requirement: document the intentional change |
| Context contains plausible but stale instructions | Resolve the actual revision, local override and active command | A summary disagrees with repository/runtime evidence: refresh only affected context |
| More iterations are mistaken for more confidence | Declare the observation that would change the decision and the repair budget | Repeated retries bring no new evidence: stop the affected attempt |

Store the short rationale and observations in the existing AEP/task record. Do not demand
an internal reasoning transcript, extra essays, or a new checklist for trivial work.

## Method decisions

- **Use as the default decision process:** observable intent, bounded discovery, smallest
  credible verification, explicit uncertainty, revision-bound evidence. These properties
  complement existing engineering practice; tests, contracts and incremental refactoring
  were not invented by AI.
- **Pilot when a specific bottleneck exists:** structured runtime diagnostics, record/replay,
  characterization/differential tests, reusable skills, clean-context review, isolated
  parallel work, stronger specifications, and durable handoff state.
- **Promote selectively:** deterministic checks for stable invariants with reproducible
  positive/negative controls and acceptable noise. Enforce the outcome, not tool usage.
- **Defer absent evidence:** universal MCP servers, multi-agent topologies, vector databases
  for repository search, full specification frameworks, organization-wide dashboards,
  blanket architecture rewrites, and hooks for every recommendation.
- **Retire when obsolete:** duplicated prompts, redundant wrappers, and model-specific
  workarounds whose removal preserves outcomes. Preserve authority and security controls.

## Brownfield gap in the first wave

PR #38 added six advisory guides and hub links. It did not change constitutional behavior,
agent projections, the minimal import selection, downstream overlays or executable controls.
Consequently a pinned old copy could remain unaware of the layer; even a current reader
could acknowledge it without changing verification behavior.

The second wave therefore distinguishes:

1. **Availability:** a reviewed pinned upgrade brings the selector and adoption guide to
   minimal adopters too; optional deeper guides remain optional.
2. **Behavior:** a compact constitutional obligation makes non-trivial method/verification
   choices explicit in the already-required task evidence.
3. **Capability:** the host supplies one real verification path for the selected slice.
4. **Enforcement:** a proven local invariant can use existing CI or a local command. The
   optional finding-set comparator supports legacy debt without masking new violations.
5. **Effectiveness:** pilot evidence determines keep/change/remove, not mere file presence.

This PR implements upstream support. It does not update downstream pins, install their
scanners, validate their runtime behavior, or measure a productivity gain in NVRM or dutpilot.

## Re-evaluation

Revisit the relevant evidence after a model/tool upgrade, changed task mix, recurring
verification failure, or excessive review noise. A small local trial is preliminary.
Do not convert published case studies into promised speedups or forced tool adoption.

## Related Documents

- [Method selection](../usage/AI_ENGINEERING_METHODS.md)
- [Existing-project adoption](../usage/ENGINEERING_METHODS_ADOPTION.md)
- [Agent evaluation](../usage/AGENT_EVALUATION.md)
- [Earlier playbook research](RESEARCH_ENGINEERING_PLAYBOOKS.md)
- [Adaptive governance](../constitution/ADAPTIVE_GOVERNANCE.md)
