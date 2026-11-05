# External Project Evaluations (Research, Advisory)

_Provenance: This research note was added to the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Purpose

This document records structured evaluations of external projects considered for adoption, inspiration, or rejection by this governance kit. It exists to:

- Prevent re-evaluation of the same project without new context
- Preserve adoption/rejection rationale so decisions are reviewable
- Retain institutional knowledge about what was considered and why

This document is **advisory**. Normative rules live in `constitution/`.

## How to Use

- **Before evaluating an external project**: check whether it already has an entry here. If it does, read the existing entry and its re-evaluation trigger before starting a new assessment.
- **After evaluation**: append a new entry using the template below. Do not remove or overwrite existing entries.
- **If a previous evaluation is revisited** (new version, changed context, updated requirements): add a **Re-evaluation** sub-entry under the original entry — do not overwrite the original.
- **Before copying a thesis into `constitution/` or a required CI check**: add or update its card in `ci/claim_cards.json`. Rules and promotion limits are in `usage/AGENT_EVALUATION.md`. A rejected or deferred project that copies no thesis does not need a card.

---

## Evaluation Entry Template

```
### [Project Name] — [Date YYYY-MM-DD]

**Source**: URL or reference

**Evaluated by**: who initiated/conducted the evaluation

**Category**: governance | architecture | tooling | workflow | testing | other

**What it provides**: 1–3 sentence summary of what the project does.

**Verdict**: ADOPTED (partial) | ADOPTED (full) | INSPIRATION ONLY | REJECTED | DEFERRED

**Overlap with this kit**: what areas overlap and which project covers them better.

**Gaps it fills (if any)**: what the project provides that this kit currently lacks.

**What we adopted / were inspired by** (if applicable): concrete items taken or inspired, with target location in the kit.

**Why rejected / deferred** (if applicable): concrete reasons.

**Re-evaluation trigger**: under what conditions this entry should be revisited.

**Claim card**: id in ci/claim_cards.json, or "none" when the verdict copies no thesis into constitution or required CI.

**Oracle**: canary | declaration | scenario | none

**What a hollow pass would look like**: one sentence. A matching document, a green job, or a starred repository does not by itself prove the thesis.
```

---

## Entries

### contains-studio/agents — 2026-02-24

**Source**: https://github.com/contains-studio/agents

**Evaluated by**: @rhemzal (via Copilot Space assessment)

**Category**: tooling / workflow

**What it provides**: A catalog of ~30 specialized AI agent system prompts for Claude Code, organized by "department" (engineering, design, marketing, product, testing, operations). Each agent is a `.md` file with YAML frontmatter (name, description, color, tools) and a detailed system prompt. Includes proactive trigger patterns and multi-agent coordination.

**Verdict**: INSPIRATION ONLY

**Overlap with this kit**:

- Testing agents (`test-writer-fixer`, `api-tester`, `performance-benchmarker`, `test-results-analyzer`) cover similar ground to `ci/TEST_GATES.md` — but as capabilities/expertise, not as enforceable constraints. AI_governance is deeper on enforcement; contains-studio is more tool-specific.
- `backend-architect` lists architecture patterns (hexagonal, DDD, CQRS, etc.) as buzzwords without trade-off analysis or decision framework. AI_governance covers this substantially better via `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` + style matrix + RAG notes with failure modes.
- `legal-compliance-checker` provides actionable GDPR/COPPA/HIPAA checklists. AI_governance references standards (`research/PROFESSIONAL_STANDARDS_AND_REFERENCES.md`) but does not provide ready-to-use compliance checklists.

**Gaps it fills (if any)**:

- **Technology-specific "recipes"**: Concrete performance budgets (LCP <2.5s, JS <200KB), framework-specific test commands (k6, JMeter, Pact), and benchmark report templates. AI_governance is intentionally tool-agnostic but could benefit from an optional "recipes" appendix pattern for concrete projects.
- **Proactive trigger pattern**: The idea that certain checks/agents should fire automatically after specific events (e.g., "after code change → run test check", "after boundary change → trigger ADR review"). This could complement governance workflow.
- **Compliance checklists as actionable artifacts**: GDPR/COPPA checklist format is more immediately usable than reference links to standards.

**What we adopted / were inspired by**:

- (Pending) Consider adding a "proactive trigger" recommendation to `usage/` or local overlay guidance — mapping governance checks to triggering events.
- (Pending) Consider whether `research/` should include optional compliance checklist templates for common regulations.

**Why not adopted further**:

- Different layer: contains-studio defines what AI _can do_ (capabilities); AI_governance defines what AI _must do_ (constraints). They are complementary layers, not substitutes.
- No governance enforcement: contains-studio has zero enforcement mechanisms, no CI gates, no ADR discipline, no boundary integrity rules, no compliance reporting.
- Marketing/design/growth agents are entirely out of scope for an engineering governance kit.
- Architecture guidance is superficial (pattern name-dropping without trade-off analysis or failure modes).

**Re-evaluation trigger**: If contains-studio adds governance/enforcement mechanisms, or if we decide to ship agent definitions as part of the kit.

---

### Development-agent governance and workflow landscape — 2026-11-01

**Evaluated by**: Codex, at @rhemzal's request, using public upstream repositories,
release notes and selected implementation/test files. This records the investigation
previously discussed in chat so its evidence and decisions remain in the project.

**Category**: governance / tooling / workflow / testing.

**Question**: Do newer, highly starred agent tools complement this kit, replace it,
or mainly promise capabilities that have not been demonstrated?

**Verdict at the 2026-11-01 investigation**: INSPIRATION ONLY for the landscape;
DEFERRED for production adoption. Spec Kit + spec-gates received an isolated
executable pilot. The 2026-11-03 follow-up added pinned Superpowers procedures,
a project Spec Kit profile and one recorded feature cycle. The current state and
remaining work are in the [adoption completion AEP](#adoption-completion-aep-2026-11-03).

**Assessment**: No reviewed project demonstrated a complete replacement for this
kit. Several provide substantially more executable integration infrastructure.
Keep the normative policy, proportional governance, architecture decisions and
evidence requirements; evaluate replacing distribution, workflow scaffolding and
gate dispatch individually. A large prompt collection is not proof of enforcement,
and successful enforcement is not proof that the underlying specification is right.

#### Dated comparison

Stars below are rounded discovery snapshots from 2026-11-01, not quality scores.
Version names identify the reviewed release or explicitly labelled preview; linked
default branches can move. Each project link is a primary source. “New” includes
new releases and recently relevant integrations, not only newly created projects.

| Project / reviewed state                                                                                                                       | Stars, approximately | What it adds / overlap                                                                                                                                                                                                           | Verdict and reevaluation trigger                                                                                                                                                                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [github/spec-kit](https://github.com/github/spec-kit/tree/v1.2.5), v1.2.5                                                                      |               144.8k | Specifications, plans, tasks, integrations, extensions/presets and executable workflows. Strong candidate for scaffolding; does not supply this kit's complete policy or trusted evidence collection.                            | **PILOT**: v1.2.5 stays pinned. One project preset and `specs/001-benchmark-trial-records/` record a completed cycle. This does not replace constitution, and the native Stop hook is still unobserved.                                                                      |
| [schwichtgit/spec-gates](https://github.com/schwichtgit/spec-gates/tree/v0.5.0), v0.5.0                                                        |                    3 | Shared gate runtime, Claude hooks, Git hooks, CI projections, custom checks and planted-violation canaries. Closes an actual integration gap despite low popularity.                                                             | **PILOT / promotion deferred**: Git/CI rejection and upgrade controls are recorded; native Cursor Stop dispatch and net infrastructure reduction remain unproved.                                                                                                            |
| [obra/superpowers](https://github.com/obra/superpowers/tree/v7.0.1), v7.0.1                                                                    |               310.4k | Debugging, test-driven development, verification and execution skills. Overlaps method guidance; stronger ready-to-use agent workflows. Bootstrap hooks alone do not enforce the semantic correctness of every skill invocation. | **PILOT** (2026-11-03): v7.0.1 procedures for debugging, inline execution, verification, and review were used on the benchmark-trial checker. The rest of the catalog is not installed. Add another skill only if this slice repeats completed work or keeps a stale result. |
| [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec/tree/v1.16.0), v1.16.0                                                            |                73.6k | Change proposals, delta specifications, tasks, archive and structural validation; Stores add a beta cross-repository surface. Attractive for changes in an existing system.                                                      | **DEFERRED**: compare against Spec Kit if brownfield change tracking or cross-repository specifications become the primary need.                                                                                                                                             |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD), stable v6.12.4; v7 preview on development line                      |                54.8k | Broad lifecycle methods and specialized roles, including smaller-change paths. Considerable overlap and process surface.                                                                                                         | **DEFERRED**: adopt only against demonstrated coordination gaps; do not compare a preview as though it were the stable release.                                                                                                                                              |
| [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core), v1.19.0                                                                             |                11.1k | Persistent context/state and research, plan, execute and verify workflows. Addresses long-running agent work and handoffs.                                                                                                       | **DEFERRED**: run a matched resume/context-loss task if current evidence shows this problem.                                                                                                                                                                                 |
| [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model/tree/v0.1.0), v0.1.0                                        |                 8.6k | Separates context-rich architectural guidance from fresh-context execution using subagents. More specific than a generic “multi-agent” claim.                                                                                    | **INSPIRATION ONLY**: test on a bounded architecture/review task; fresh-context guarantees and host support need local evidence.                                                                                                                                             |
| [pdewost/coding-constitution](https://github.com/pdewost/coding-constitution), README v0.13                                                    |                   13 | Closely related policy/context discipline and hook-fire verification. Claude integration is more complete than other hosts; no shipped equivalent of a full CI/Git enforcement layer was found.                                  | **INSPIRATION ONLY**: reuse verification ideas after checking ownership/license; revisit when portable adapters mature.                                                                                                                                                      |
| [paladini/specgov](https://github.com/paladini/specgov), current v1 schema; latest release inspected v0.1                                      |                    4 | Artifact relationships and policies for missing evidence, dependencies and stale specifications; adapters for multiple spec tools. Structure validation does not establish semantic correctness.                                 | **DEFERRED**: trial when specification/evidence drift can be measured; distinguish current source from released package.                                                                                                                                                     |
| [intellectronica/ruler](https://github.com/intellectronica/ruler), beta                                                                        |                 3.0k | Distributes rules and agent configuration. Could reduce duplicated instruction files, not replace policy reasoning.                                                                                                              | **DEFERRED**: trial only if configuration drift is observed across hosts.                                                                                                                                                                                                    |
| [buildermethods/agent-os](https://github.com/buildermethods/agent-os)                                                                          |                 5.6k | Discovers and deploys project standards and specification workflows. Overlaps local conventions and project context.                                                                                                             | **INSPIRATION ONLY**: revisit when extracting or maintaining project standards is the bottleneck.                                                                                                                                                                            |
| [ruvnet/ruflo](https://github.com/ruvnet/ruflo/tree/v3.68.0), v3.68.0                                                                          |                80.5k | A substantial agent runtime/orchestration system; much wider operational surface than this policy kit.                                                                                                                           | **DEFERRED**: require an actual orchestration need and end-to-end evidence for the specific advertised capability.                                                                                                                                                           |
| [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit), public preview                                    |                 6.5k | Runtime policies, identity, audit and sandbox controls, including a Claude surface. More relevant to operating agents than choosing architecture and governing development work.                                                 | **DEFERRED**: revisit for runtime authority/audit requirements; not a like-for-like replacement.                                                                                                                                                                             |
| [hindermath/spec-kit-preset-autonomous-run-governance](https://github.com/hindermath/spec-kit-preset-autonomous-run-governance), README v0.4.8 |                    2 | Permission-bound runs, completion/evidence state and revision/staging checks. Close conceptual overlap with this kit's task mandate and run evidence.                                                                            | **INSPIRATION ONLY**: inspect as a possible adapter after the basic Spec Kit pilot, not as an independently validated governance standard.                                                                                                                                   |
| [hindermath/spec-kit-preset-architecture-governance](https://github.com/hindermath/spec-kit-preset-architecture-governance), README v0.6.5     |                    2 | Architecture/threat-model/decision templates and workflow wrappers. Useful packaging precedent; selected source inspection did not establish runtime enforcement.                                                                | **INSPIRATION ONLY**: revisit after deciding whether a preset is the right distribution format.                                                                                                                                                                              |

The older [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)
repository (~64.2k stars) is archived and points to `open-gsd/gsd-core`. Its star
count should not be assigned to the successor, and archiving the old repository
should not be mistaken for abandonment of the successor.

#### What is evidence, and what is still a claim?

- **Spec Kit** contains real executable workflow and extension infrastructure,
  not only Markdown templates. The [v1.2.5 source](https://github.com/github/spec-kit/tree/4572a67fe0e72a6837e2d7bb0fda875bc41482e5)
  is pinned in our pilot. This does not prove agent-generated specifications are
  correct or that their instructions will always be followed.
- **spec-gates** ships executable canaries and parity tests, and an
  [upstream CI run was inspected](https://github.com/schwichtgit/spec-gates/actions/runs/40577543641).
  Our own [pilot](SPEC_KIT_SPEC_GATES_PILOT.md) is stronger evidence for the narrow
  compatibility question. Its Stop hook explicitly allows stopping after some
  runtime errors and on a repeated stop; “fail closed” needs a boundary-specific
  qualification. Later pilot records contain actual rejecting/passing candidate
  CI runs and Git rejection; native Cursor Stop dispatch remains unobserved.
- **Superpowers** [v7.0.1 release notes](https://github.com/obra/superpowers/releases/tag/v7.0.1)
  report fixes for repetitive questioning and an internal 24-case evaluation.
  This is useful regression evidence from the maintainer, not an independent
  estimate of productivity or safety in our downstream projects. On 2026-11-03
  this repo pinned that tag and used debugging, inline execution, verification,
  and a fresh review on one checker. A resume session did not rewrite the
  completed checker. The review found that `cancelled` was rejected. That is
  one slice, not a general gain.
- **Elephant Goldfish Model** publishes
  [native-host testing notes and limitations](https://github.com/google/elephant-goldfish-model/blob/main/TESTING.md).
  Its organizational-use claims are first-party claims, not our adoption evidence.
  A first tagged release and a recognized organization name do not establish
  stable support across hosts. That testing document can change after this snapshot.
- **Ruflo** [v3.68.0 release notes](https://github.com/ruvnet/ruflo/releases/tag/v3.68.0)
  describe repairing a session-episode bridge that called methods absent from its
  implementation. This is a concrete reason to test the promised end-to-end path.
  It does not demonstrate that all Ruflo functionality is fictitious or broken.
- **Spec Kit catalogs/presets** are distribution mechanisms. The
  [community preset guidance](https://github.com/github/spec-kit/blob/v1.2.5/docs/community/presets.md)
  does not turn a catalog entry into a security audit or GitHub endorsement.
  Small extensions need source, release and maintenance review even when the
  parent platform is popular.

#### What to keep and what could be replaced

| Layer in AI_governance                                                                                  | Decision                                           | Candidate / acceptance condition                                                                                                         |
| ------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Normative policy, action authority, proportional G/CM levels, architecture tradeoffs and ADR discipline | Keep                                               | No reviewed tool proved equivalent coverage or decision quality.                                                                         |
| Instructions, templates and workflow distribution                                                       | Pilot replacement                                  | Spec Kit; preserve host instructions and one source of policy truth.                                                                     |
| Repeated hook dispatch, projection bookkeeping and basic negative canaries                              | Pilot replacement                                  | spec-gates; prove host lifecycle, Git/CI wiring, safe reapply/upgrade and local-change preservation.                                     |
| Required evidence schema and acceptance decisions                                                       | Keep; invoke through an adapter                    | Existing `ci/validate_test_evidence.py`; upstream command success alone cannot establish coverage, authenticity or fresh test execution. |
| Debugging/TDD task recipes                                                                              | Keep the pin; no acceptance gain on B6, B7, and B8 | Same task and host. The extra text did not change acceptance or the withheld deploy. Do not add preset sections on that evidence.        |
| Persistent context and multi-agent architecture                                                         | Defer                                              | GSD/Elephant Goldfish/Ruflo only against a demonstrated task need.                                                                       |

**Concrete adoption through 2026-11-03**: the research record and gate experiment,
plus pinned work procedures and a project Spec Kit profile used on one feature.
Current copy bundles do not distribute or activate that profile. Visible limits
from the gate pilot remain claim cards `stop-hook-fail-open` and
`native-stop-dispatch-unobserved`.

**Next decision**: the bounded benefit comparison is recorded and shows no
acceptance gain. The opt-in transfer recipe is in `usage/HOW_TO_IMPORT.md`.
Run `b6a246fd` asked for a plan and tasks. Disposable run `8ecad04d`
(`specify` 1.2.5, `/tmp/wf-implement`) asked for the calc.py fix and finished
`implement`: the unittest exited 0, the expected value stayed, and `deploy.sh`
did not run. A named downstream checkout is still unmet.
The [gate pilot](SPEC_KIT_SPEC_GATES_PILOT.md) stays a separate deferred
decision. Native Stop dispatch remains open and does not block the retained
procedures.

**Re-evaluation triggers**: a change to the pinned integrations/gate runtime,
failed native-host controls, excessive operator intervention, recurring context
loss, or a new requirement currently covered by duplicated local infrastructure.
Use the same task/host and record false passes, false blocks, repair attempts,
human interruptions and maintenance burden. Stars and social-media announcements
alone are not triggers to replace working policy.

**Licensing note**: check the exact files before copying. Most candidates report
MIT, Elephant Goldfish reports Apache-2.0, and coding-constitution distinguishes
code from document licensing. BMAD's repository licensing/trademark text is more
informative than a GitHub API `NOASSERTION` label. This review is not a legal audit.

---

#### Re-evaluation: tier-aware adoption (2026-11-04)

**Verdict:** deepen the existing integrations, qualify a few narrowly selected
capabilities, and keep whole-framework adoption conditional. Tier A/B/C makes
optional host-specific trials easier to contain; it does not establish benefit,
compatibility, or authorization for another runtime.

**Baseline:** this assessment inspected kit commit
[`9d262a051926ed90ddff96576c74e45e2c7aefb0`](https://github.com/rhemzal/AI_governance/tree/9d262a051926ed90ddff96576c74e45e2c7aefb0).
It re-evaluates the landscape entry above and supersedes its next-action
recommendations, while preserving the dated observations below.
**Claim card:** none; advisory assessment only, no new normative thesis or CI gate.
**Oracle:** targeted executable controls for the two findings below; proposed
scenario comparisons for the remaining candidates. A hollow pass would be an
installed package, a generated document, or a successful command without a
demonstrated improvement in the relevant task.

##### What the new tiers change

The [scope and host rules](../usage/ADOPTION_SCOPE_AND_HOSTS.md) define A as the
agnostic snapshot, B as optional work procedures/preset, and C as the specific
experimental Spec Kit/spec-gates/Cursor stack. They are not a ranking of quality
and are separate from Governance Level and CI Maturity.

- Portable guidance can improve A/B without installing another product.
- B can gain selected procedures with a small, reviewed dependency surface.
- C enables authorized native workflow/hook trials on capable hosts, with one
  real adopter acceptance command.
- C is **not** a generic compatibility certification for Ruler, GSD, or another
  orchestrator. A proposed add-on still needs its own host/scope decision.
  OpenSpec remains an alternative requirement path, not an automatic extension
  of the Spec Kit-based C stack.

The kit now has post-implement shell acceptance, a native execution report,
spec-gates 0.5.1, and a parameterized installer. Its downstream record reports
MechWeave adoption and workflow `eeb22cb0`; this assessment did not independently
rerun that checkout. Native Cursor Stop dispatch and net productivity benefit
remain unproved. B6–B8's equal acceptance results do not justify another generic
calculator trial. They also do not prove that the tools cannot help other tasks.

##### Executed checks and two concrete next changes

**Current integration regressions:** Python 3.12 with Spec Kit CLI 1.2.5;
34 tests passed, no skips, at the baseline above:

```bash
timeout 60s python -m unittest \
  ci.gate_tests.test_workflow_acceptance \
  ci.gate_tests.test_superpowers_task_done \
  ci.gate_tests.test_spec_gates_git_environment \
  ci.gate_tests.test_test_evidence -q
```

Here `python` was the existing isolated pilot environment containing
`specify-cli==1.2.5`, not an assumed global installation. These tests include
actual Spec Kit shell-engine pass/fail controls; they do not exercise native
Cursor Stop or measure an agent's task quality.

**1. Update the selected Superpowers pin after integration qualification.**
The kit vendors **7.0.2** (commit `22f0b463e7a5e579904dd6211a520321035526f7`)
after the controls below passed on the pinned helpers. Upstream
[7.0.2](https://github.com/obra/superpowers/releases/tag/v7.0.2) fixes helpers
this kit includes. On Linux, vendored 7.0.1 helpers were compared with the
exact upstream 7.0.2 `task-brief`, `sdd-workspace`, and new `sdd-repo`
in disposable directories:

| Control | Vendored 7.0.1 (historical) | Vendored 7.0.2 |
| --- | --- | --- |
| Same-depth headings `## Task 6`, then `## Task 6b`; request 6 | Exit 0; includes the other task | Exit 0; only task 6 |
| Same-depth `Task A1`, then `Task A2`; request A1 | Exit 3; task not found | Exit 0; only A1 |
| Task 6 opens a code fence that never closes before Task 7 | Exit 0; includes task 7 | Exit 4; rejects malformed brief |
| Invoke `sdd-workspace PLAN_FILE` outside any Git repository | Exit 0; creates `.superpowers/` despite Git's error | Exit 2; creates no workspace |

Integrated regressions: `ci/gate_tests/test_superpowers_helper_controls.py`.
Upgrade and rollback copy blocks in `usage/HOW_TO_IMPORT.md` use `v7.0.2.next`,
`v7.0.2.prev`, and `v7.0.2.rollback`. Retain the same selected procedures; the
new `sdd-repo` dependency ships with the updated helpers. Do not install the full
skill catalog merely to obtain these fixes.

**2. Strengthen the existing acceptance report's state identity.**
**Implemented (2026-11-04):** `ci/uncommitted_diff_identity.py` hashes porcelain
status together with blob identities; see ADR-0016 amendment and
`test_dirty_tree_identity_reflects_file_content`. The disposable control below
describes the pre-fix gap:

The runner previously hashed `git status --porcelain`, which identifies changed paths and
statuses, not their contents. In one disposable Git repository, commit
`payload.txt`, change its contents twice without changing its status, and invoke
`ci/run_task_acceptance_check.sh` after each edit with
`TASK_ACCEPTANCE_CMD='test -s payload.txt'`. Put evidence/log paths outside that
repository so they do not alter the control. Both invocations exited 0 and
reported the same uncommitted identity:
`1e412246145f975d001c989931afa593faa4beba6adb76faa9cf80aac19164f7`.

Both commands really ran; the report cannot distinguish their different input
bytes. Fix this before treating the field as a content identity. Use the smallest
explicit tested-input identity: a documented clean-commit contract, or a
deterministic identity covering relevant tracked and untracked input contents,
path/type changes and deletions. Exclude only declared generated evidence outputs;
detect mutation during the check or label the identity as pre-run only. Controls
should distinguish different bytes at the same path and preserve identity for
unchanged inputs. Do not promise authenticated provenance from a local hash.

The autonomous-run preset's exact-byte/staged-state discipline is useful
[inspiration](https://github.com/hindermath/spec-kit-preset-autonomous-run-governance/blob/5d7a4419345f510961d92792a46e11e8466581f5/README.md)
for these controls. It does not require installing that preset's second run
lifecycle. The previously implemented acceptance step itself remains useful.

##### Disposition of every previously considered solution

“Placement” below means a proposed fit, not a new shipped tier or a claim of
tested compatibility. Risk is the incremental maintenance/process burden for
this kit, not a general judgment of project quality.

| Solution | Placement and decision | Benefit to verify / revisit trigger | Overengineering risk |
| --- | --- | --- | --- |
| **Superpowers** | **Deepen B/C now:** qualify selected 7.0.2 pin | Four observed helper defects above; preserve existing task execution and rollback behavior | Low for selected update; higher for the full catalog |
| **Spec Kit** | **Deepen existing B/C**, keep current pin unless a needed fix justifies moving it | Real task acceptance and restart behavior. 1.3.0 exists, but the required shell step already works in 1.2.5 | Low for current workflow; medium for more presets/artifacts |
| **spec-gates** | **Keep C experimental; deepen native evidence** | One authorized native Stop pass/fail observation when a capable host is available; same host acceptance through workflow/Git/CI where configured; count false blocks | Medium; do not repeat hook setup without new host evidence |
| **Agent OS** | **Deepen the already adapted A/B pattern** | Task-scoped discovery/injection of up to three sourced local constraints; fewer concrete violations without loading more irrelevant context | Low for existing overlay; medium for a second standards tree |

Kit upstream **Experiment A** (2026-11-04, `specs/003-task-scoped-overlay-trial/`): B1 passed C1–C4; partial PASS — mandate text in governed-work reduces unrelated overlay noise (C4); C1 B0 miss not shown on maintainer-familiar host. Not an Agent OS product install.
| **Elephant Goldfish Model** | **Next bounded review-pattern candidate**, B procedure or separately qualified host add-on | A fresh-context design reviewer finds independently confirmed defects missed by current review, with controlled noise and cost | Low/medium for one review; high for adopting the full multi-stage protocol by default |

Kit upstream **Experiment B** (2026-11-04, `specs/004-fresh-context-review-trial/`): separated review packet on `#53` identity helper — B1 found symlink test gap and doc gaps B0 skim missed; screening PASS; not an EGM install.
| **Ruler** | **Conditional new distribution pilot** for A/B entry points on two actually used hosts | A real projection drift or repeated duplicate edit; one-source update reaches both hosts and preserves host-owned instructions | Medium; not worthwhile for one host |
| **OpenSpec** | **Conditional A/B alternative** in a brownfield adopter whose requirements are not owned by Spec Kit | Correct modify/remove/rename/archive cycle preserving unrelated requirements, with fewer manual mistakes than direct/current editing | Medium; high if it creates two requirement authorities |
| **SpecGov** | **Defer installation; narrow structural pilot if drift occurs**, host CI alongside A/B/C | One real code-to-spec mapping gap, unrelated-spec negative control, known-good change. No semantic-correctness claim | Medium; avoid a graph/metadata program without a recurring problem |
| **GSD Core** | **Defer whole framework**; reconsider a separate authorized host trial | Repeated real resume/context-loss failures despite current ledger; compare recovery from changed tree, stale evidence and completed work | High overlap with current state/plan/workflow |
| **BMAD-METHOD** | **Defer** | Repeated product-discovery or role-coordination gaps on a real task; compare its smallest path with current process | High if installed as a second lifecycle; stable v6 and preview v7 must remain distinct |
| **Ruflo** | **Defer** | An actual parallel scheduling/resource problem; integrated correctness and net coordination cost beat simpler execution | High; tiers alone do not establish an orchestration need |
| **Microsoft agent-governance-toolkit** | **Outside the present development-kit adoption scope** | A deployed agent needs runtime tool authorization/audit; test real denied/allowed calls and bypasses in that application | High here; potentially relevant in a separate runtime project |
| **coding-constitution** | **Retain inspiration only** | Borrow a specific hook-fire/context-resume test when it closes an observed host gap; retain one policy authority | Low for a test idea; high for a second constitution |
| **hindermath autonomous-run governance** | **Use state/evidence ideas; defer full preset** | Current state-identity finding above; require a residual lifecycle gap before adding the preset | Low for focused controls; high for duplicate lifecycle/state |
| **hindermath architecture governance** | **Inspiration only** | Repeated missing threat-boundary/decision reasoning not already caught by the kit's architecture guidance and ADRs | Low for a focused question; medium/high for duplicate templates |
| **contains-studio/agents** (earlier entry) | **Retain inspiration only** | A specific technology recipe with executable acceptance, not a general role catalog | Low for one recipe; high/no demonstrated value for bulk agent installation |

##### How to qualify the short list without a new evaluation platform

Use the existing task record and [evaluation guidance](../usage/AGENT_EVALUATION.md).
There are two decisions, not a score based on stars:

1. **Does it work in the intended host?** Deterministic positive/negative controls,
   pin identity, bounded write surface, repeat/upgrade/removal behavior.
2. **Does it improve our work?** Compare against the current kit on equivalent
   tasks with acceptance fixed before running. Keep model, permissions and
   starting state equivalent; isolate sessions and alternate variant order.
   Record acceptance failures, false blocks/findings, repair loops, operator
   interventions, measured usage, and maintenance steps.

The Superpowers controls already justify a focused integration update. A new
procedural capability needs a small representative comparison: start with three
preselected tasks and two independent attempts per variant when model variability
matters. This is a screening budget, not statistical proof. Preserve every
attempt, including failures. For a deterministic distributor, use file/host
controls rather than unnecessary repeated agent benchmarks.

| Candidate slice | Concrete comparison and acceptance | Stop / rollback |
| --- | --- | --- |
| **Agent OS-derived context selection** | Use the existing overlay on an importer or comparable module task. Compare current loading with task-scoped sourced constraints; include a permitted exception and an unrelated task. Known-bad output must violate a specific constraint; known-good output must remain accepted. Retain only if it removes observed misses or reduces irrelevant context with unchanged correctness and no extra operator ritual. | Remove added guidance if it merely repeats the current pointer, increases missed exceptions, or has no observed benefit. No standards database/index service. |
| **Fresh-context design review** | First test one reviewer reading only the design, required sources and acceptance criteria; exclude the author's discussion and proposed verdict. Compare with the current review, including Superpowers' existing review path, on a known defect and a clean control before representative tasks. Count confirmed findings, misses, false positives and total review/rework cost. Retain only an incremental detection benefit within the agreed attention/usage budget. | No verified context isolation means no EGM claim. Stop if the reviewer merely repeats findings or costs more without a useful detection difference. One review and one repair/recheck cycle initially; no automatic persona swarm. |
| **Ruler** | In a disposable copy of a real two-host setup: one rule update, dry-run, apply, second apply, rollback. Require correct content at both intended entry points, no second-run changes, no lost host sentinel/override, no writes outside selected paths, and a fresh session on each host demonstrating correct rule discovery. Compare with the existing short-pointer approach. | Stop on host-file replacement or if the pointer approach solves the drift more simply. Disable unrelated MCP and gitignore propagation. No subagent/catalog rollout. |
| **OpenSpec** | Use a supported runtime: Node >=22.12.0 for 1.16.0 npm, or the pinned standalone release. Compare a real canonical-requirement change with the existing method: modify/remove/rename, preserve unrelated requirement, reject malformed delta, verify implementation against independently chosen acceptance. | No measurable requirements-maintenance benefit, unsupported runtime, or two authorities for the same requirement: retain current method. Stores/cross-repo rollout is outside this slice. |

For Ruler, the inspected
[`AgentsMdAgent`](https://github.com/intellectronica/ruler/blob/5e551e60952fb1c81c6c5ad6f5fe8b7a412bda87/src/agents/AgentsMdAgent.ts)
writes a generated whole file and can back up the old file; this is **not** a
preserving merge of arbitrary host instructions. A safe pilot must establish
file ownership/output paths first. Its README documents `--dry-run`,
`--no-mcp`, `--no-gitignore` and revert; those options still need local controls.

The full EGM review is materially larger than “ask another agent”: the inspected
skill has multiple review stages and its release notes retain exact-artifact and
host-isolation limits. Start with the transferable review principle using
existing review infrastructure; do not call a simplified adaptation a validated
EGM installation. This assessment spawned no reviewer and measured no detection
gain. Native Stop evidence is not a prerequisite for these separate B-level
experiments.

##### Order, cost and source limits

Recommended next work:

1. **Two bounded kit changes:** qualify the selected Superpowers update and repair
   the acceptance report's content identity. Each can be reviewed independently;
   neither needs another framework.
2. On the next suitable real task, qualify **one** context/review improvement:
   Agent OS-derived loading when local-rule misses are observed, or fresh-context
   design review when review quality is the gap. Do not activate both variables
   in the same comparison.
3. Choose **Ruler or OpenSpec only when its trigger is present**. Otherwise stop
   at the useful current kit. SpecGov/GSD remain deferred until their named gap
   is observed. A newly available native Cursor host justifies finishing the
   existing Stop experiment, not restarting unrelated pilots.

This is an advisory queue, not an authorization to install on another repository.
No new service, universal mandatory gate, benchmark dashboard, policy authority,
or process form is proposed. Use at most two implementation/repair attempts per
selected slice before recording the blocker and retaining the baseline.

The shortlisted upstream projects are available under MIT (Superpowers, Spec Kit,
spec-gates, Agent OS, Ruler, OpenSpec) or Apache-2.0 (EGM). Check exact files/notices
when copying. A free software license does not make model calls, host subscriptions
or maintenance free. Prefer existing local commands and accounts; record real
usage if available instead of estimating a productivity multiplier.

Source refresh on 2026-11-04 used primary repository metadata, release notes and
selected source files. Main-head timestamps/README claims are not installed-release
evidence. Relevant review anchors:

- [Spec Kit 1.3.0 release](https://github.com/github/spec-kit/releases/tag/v1.3.0);
  installed pilot remains 1.2.5. [spec-gates 0.5.1 release](https://github.com/schwichtgit/spec-gates/releases/tag/v0.5.1).
- [Superpowers exact change](https://github.com/obra/superpowers/compare/v7.0.1...v7.0.2);
  executable controls above cover only the selected helper sources.
- [Agent OS](https://github.com/buildermethods/agent-os/tree/e892e61d322759165e7d9173e92c1010406c9f4d);
  [Ruler](https://github.com/intellectronica/ruler/tree/5e551e60952fb1c81c6c5ad6f5fe8b7a412bda87),
  latest release inspected 0.3.46; reviewed main is not assumed identical.
- [EGM review source](https://github.com/google/elephant-goldfish-model/blob/113a3afc44e8f4f54722d7150d5701f65cc8ef7f/skills/egm-review/SKILL.md)
  and [0.1.0 release limitations](https://github.com/google/elephant-goldfish-model/releases/tag/v0.1.0).
- [OpenSpec 1.16.0](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.16.0).
  The earlier local trial's unsupported Node version is not closed by this review.
- [SpecGov reviewed source](https://github.com/paladini/specgov/tree/5a59b902639a07fbec1082a4c465aa5d86eadc97)
  declares package 1.0.0-rc.2; latest GitHub release inspected is 0.1.0 and its
  old manifest is unsupported by current source. Select and qualify one exact
  package before a pilot; do not install `latest` based on a v1 README.
- [GSD Core](https://github.com/open-gsd/gsd-core/tree/4dce9e859ba11e1eb687aaa9855487a5595c276e),
  latest release inspected 1.20.0; [BMAD](https://github.com/bmad-code-org/BMAD-METHOD/tree/022be9314e4facd16826104a9f8033e1c5ed4fdc),
  [Ruflo](https://github.com/ruvnet/ruflo/tree/d10b6585f719be6787f88cad2f70879564520e24),
  and [Microsoft toolkit](https://github.com/microsoft/agent-governance-toolkit/tree/a918f7634123b5b78e292302195260f786e69130)
  received source/README scope review, not local runtime qualification.
- [coding-constitution](https://github.com/pdewost/coding-constitution/tree/9a0cc778061d610ca2cc1b0c739d33564de95839),
  [architecture preset](https://github.com/hindermath/spec-kit-preset-architecture-governance/tree/9aa8d8e7c4231e753985835fe39eca42611457cd),
  and [contains-studio](https://github.com/contains-studio/agents/tree/a5a480c324cac64b9c569bca0b2f297d517240cb)
  retain the limited dispositions above. No claim that they are universally
  ineffective or that popularity proves effectiveness is made.

---

## Adoption completion AEP (2026-11-03)

This is the current follow-up assessment and Autonomous Execution Plan (AEP).
It supersedes the older **next investment** recommendation above, while retaining
the dated experiments. Implementation started after this section was committed.
Native run `c37bf147` (`specify` 1.2.5, integration `cursor-agent`) completed
only `specify` and was killed by a 45 second timeout while `state.json` still
said `running`. `specify workflow resume c37bf147` answered that a running
run cannot be resumed. A later run, `b6a246fd`, was started from the kit root
and finished with status `completed` through `implement`. Its input asked for
plan and tasks only, so that pass did not execute the recipe tasks. The
feature ledger is `specs/002-opt-in-transfer-recipe/progress.md`.

Disposable B6 and B7 fixtures both met task acceptance with and without the
resume/debug rules. Neither run executed `deploy.sh`. The comparison does not
show a speed or safety gain. A later pair, recorded in
`research/benchmark_trials/b8-2026-11-03.md`, gave both arms one implement
mandate and withheld `deploy.sh`. The candidate also received the profile's
appended template sections. Both arms implemented the fix and left deployment
unrun. That pair still shows no gain. It removes the plan-only input of run
`b6a246fd` as an explanation. spec-gates stays deferred: `verify.sh --boundary ci`
runs the same `ci/gate_tests` discovery as the direct command, passes when that
suite passes, and fails when a planted test fails. It does not remove the
direct suite, and native Stop dispatch was not rerun.

### Verified starting point

Reviewed `main` at
[`65fe471b6a2b9924295f5ea8eb9701856ea976c9`](https://github.com/rhemzal/AI_governance/commit/65fe471b6a2b9924295f5ea8eb9701856ea976c9).
Do not repeat the previous recommendation to install the procedures or repair
the permanent benchmark-directory prohibition: both have been implemented.

| Capability                      | Evidence at the reviewed revision                                                                                                                                                                               | Remaining gap                                                                                                                                                                                                                             |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Selected Superpowers procedures | v7.0.2 pinned with MIT license, hashes, selected skill links, `sdd-repo`, and a governed entry point; `specs/001-benchmark-trial-records/progress.md` records debugging, continuation, stale-result handling and a review finding | One recorded use; host discovery and repeatable use beyond that slice have not been independently demonstrated here                                                                                                                       |
| Spec Kit profile                | Three appended templates, registered `ai-governance` workflow, disposable run `8ecad04d` through `implement`, and feature ledgers                                                                               | No named downstream trial; native Stop hook still unobserved; B6/B7/B8 show no acceptance gain from the profile text                                                                                                                      |
| Resume and review               | The ledger records a resumed Task 2, a changed hash and rerun; review found rejection of `cancelled` and missing coverage of an absent directory                                                                | Matched B6 and B7 records are in `research/benchmark_trials/`. The durable ledger is `specs/<feature>/progress.md`. Scratch under `.superpowers/` and `.specify/workflows/runs/` does not replace it.                                     |
| Later benchmark evidence        | Historical absence remains dated; the new checker accepts later records and rejects malformed fields                                                                                                            | `b6-2026-11-03.md`, `b7-2026-11-03.md`, and `b8-2026-11-03.md` are recorded. Checker acceptance is not a gain.                                                                                                                            |
| Use in another repository       | Profile is explicitly repository-local; `kit-manifest.yml` excludes the procedure pin, Cursor links, presets and workflows from its current selections, including `full`                                        | `usage/HOW_TO_IMPORT.md` and the disposable procedure tests cover opt-in copy and preset registration. A named downstream checkout is not authorized.                                                                                     |
| spec-gates                      | Pilot records actual rejecting/passing candidate CI runs, Git rejection, release verification and upgrade controls                                                                                              | **Deferred** for required checks. Native Stop dispatch remains unobserved. Projected `verify.sh --boundary ci` runs the same `ci/gate_tests` discovery as the direct command; see [spec-gates decision](#spec-gates-decision-2026-11-03). |

**Checks performed for this assessment:** on the reviewed checkout,
`timeout 60s python3 -m unittest ci.gate_tests.test_work_procedures ci.gate_tests.test_open_claim_limits -v`
passed **8 tests, 0 skips**. The
[main-commit hygiene job](https://github.com/rhemzal/AI_governance/actions/runs/41651322044/job/125969941927)
also reports success. Separate local calls to `resolve-template.sh` resolved
spec, plan and tasks templates, each with its governance section exactly once.
The local checks verify pin/links, template resolution and
record contracts; they do not launch an agent or establish productivity.
Previous native-host observations are attributed to their committed records,
not rerun during this assessment.

**Assessment:** useful adoption had begun. The outstanding problem at that checkout
was making the existing procedures reliably invocable, transferable and worth
maintaining. Another registry, generic orchestrator, or collection of installed
frameworks would not have closed that gap.

The evidence column is the reviewed checkout. The Spec Kit row also names
disposable run `8ecad04d`. The remaining-gap column is the current tree:
the opt-in recipe is `usage/HOW_TO_IMPORT.md`, the B6/B7/B8 records exist,
and `specs/002-opt-in-transfer-recipe/` keeps `progress.md` only.

### Ordered work and completion evidence

Superseded on 2026-11-03. Do not create `specs/002-operational-adoption/`.
The feature record is `specs/002-opt-in-transfer-recipe/progress.md`.
The procedure is `usage/HOW_TO_IMPORT.md` § Opt-in work procedures.
The earlier table, step details, and ready execution plan are in git history.
They are not a second recipe.

AEP Status: NOT-REQUIRED

```aep
{
  "schema_version": 1,
  "status": "NOT-REQUIRED",
  "reason": "The opt-in recipe, the B6/B7/B8 comparison, and the spec-gates deferral are recorded. Disposable workflow run 8ecad04d implemented the authorized calc fix. A named downstream checkout stays unmet and is not started here."
}
```

Do not start step 1. Disposable run `8ecad04d` is the native implement observation. A named downstream checkout remains unmet. Recording that does not turn the checkout into a pass.

### Benefit decision (2026-11-03)

B6, B7, and B8 met task acceptance with the extra procedure or profile text
and without it. No arm ran `deploy.sh`. The three appended template sections
stay, because they state continuation inside an authorized outcome and the
stops for merge, push, publish, and deploy. They do not stay as a measured
productivity or safety improvement. Do not add another preset section until a
matched pair on a named task class differs.

The maintenance that stays is those three sections, `.specify/workflows/ai-governance/workflow.yml`,
the registry entry, and the opt-in command that registers the preset. spec-gates
stays deferred. A named downstream checkout is unmet. Disposable run `8ecad04d`
implemented one authorized calc fix and does not close that checkout.

### spec-gates decision (2026-11-03)

**Defer** promotion to required checks and branch protection. **Retain** the
experimental adapter under `governance/experimental/spec_gates/` and the advisory
workflow only. Do not install spec-gates or the Stop hook as part of the opt-in
work-procedure trial.

On this tree, `timeout 120s bash .specify/gates/verify.sh --boundary ci` exited
0 and `timeout 120s python3 -m unittest discover -s ci/gate_tests -q` exited 0
with **99 tests**. The projected policy gate `kit-gate-tests` is the same
discovery command recorded in `governance/experimental/spec_gates/policy.kit.json`.
That is parity, not a removed manual step for maintainers who already run
`ci/gate_tests` directly.

Native Cursor Stop dispatch remains unobserved. The pilot's Stop repair budget is
not reopened without new host evidence. The [gate pilot](SPEC_KIT_SPEC_GATES_PILOT.md)
records permissive Stop cases; claim cards `stop-hook-fail-open` and
`native-stop-dispatch-unobserved` stay in force.

GOVERNANCE FIT CHECK

- Project stage: serious solo, reusable governance kit.
- Recommended Governance Level (G): G2 for this incremental adoption work.
- Suggested CI Maturity (CM) if kit adopted: retain the host's current declared level; do not raise it for a pilot.
- CI/CD needed now: existing checks are sufficient; no new mandatory pipeline.
- Reason: the concrete risks are inactive instructions, unsafe transfer, stale progress and maintenance without benefit.
- What to defer: additional frameworks, mandatory reviewer processes, native Stop retries without new evidence, global installation and general rollout.

## Agent runtime and evidence analysis (2026-11-04)

Reviewed [`52f9c26f342b3517384e96f7d289bb300a72aaa4`](https://github.com/rhemzal/AI_governance/commit/52f9c26f342b3517384e96f7d289bb300a72aaa4).
This is the current analysis of the connection between policy and everyday agent
execution. The earlier capability audit remains in PR #49 history at
`6158284e66c242e88e6fbc4dc44d3a16e843128b`. Its original R1/R2 reproductions are
now covered by passing regressions: stale upgrade staging is refused, and the
dangling-destination/injected-copy-failure cases preserve the preset registry.
This does not claim every possible installer failure is transactional.

**Assessment:** the weak point is an incomplete connection from the selected
acceptance check to actual execution, fresh state identity, and durable completion
evidence. The kit has useful instructions, executable checks, CI and some runtime
adapters; it lacks a consistently used connection between them. Reference-only or
manual controls are not inherently defects. Architecture rationale and method
suitability still need judgment, and an adopter must supply its product checks.

### What happens at each boundary today

| Boundary | Current mechanism | Actual limit |
| --- | --- | --- |
| Load applicable policy | Host AGENTS pointer, kit projection, local overlay, governed-work skill | A nested submodule or copied skill is not proof that the host loaded it. The activation smoke checks files and text, not native agent selection. |
| Choose work and checks | AEP/task mandate, method selector, local test command | These are instructions. The agent can omit a relevant check or select a weak one; schema validation does not decide adequacy. |
| Execute a governed workflow | Spec Kit specify → plan → tasks → implement | The shipped workflow contains four agent-command steps and no final deterministic shell verification step. Successful command dispatch is not product acceptance. |
| Run checks locally | Direct commands; Superpowers task-done; optional spec-gates verify.sh | These really execute commands, but must be invoked and supplied with the right checks. They do not independently define acceptance. |
| Assess supplied evidence | ci/validate_test_evidence.py | Validates two supplied records. It neither opens evidence references nor derives the current source/build identity nor authenticates the producer. |
| Finish, resume and integrate | Feature ledger, experimental Cursor Stop, kit CI | Ledger transfer is partly manual; Stop dispatch remains unobserved. CI is stronger evidence of its own executed steps, but does not automatically validate the whole task or impose branch protection. |

The cited historical enforcement matrix at `873df7e...` should not be treated as
the current tree. The current matrix explicitly separates kit CI and adopter
wiring. `usage/AI_RUN_EVIDENCE.md` already describes the missing host normalizer
and independent expectation selection; this analysis identifies an implementation
gap in that documented contract, not a need for another evidence schema.

### Direct observations and useful upstream capabilities

**The evidence-validator limit is reproducible and intentional.** The existing
`test_hand_written_report_is_verified_without_a_runner` passed: both JSON inputs
were hand-written, the referenced `result.json` did not exist, and the CLI still
returned exit 0 / VERIFIED. That verdict means the supplied records agree and
satisfy the schema. It must not be promoted into a claim that a runner executed
the required tests. Renaming fields or demanding more agent-written JSON would
not supply the missing provenance.

**Spec Kit already has the smallest missing execution primitive.** At the pinned
v1.2.5 source `4572a67fe0e72a6837e2d7bb0fda875bc41482e5`, a workflow `type: shell`
step executes a command, captures its output/exit code, and fails on nonzero exit.
It can follow `implement` without another agent, package or orchestrator. A real
local `WorkflowEngine` probe used that exact source and disposable two-step
workflows, with the second step writing a marker:

| Verification command | Workflow outcome | Captured exit/output | Later marker step |
| --- | --- | --- | --- |
| Print runner-output; exit 0 | completed | 0 / runner-output | Executed |
| Print runner-output; exit 7 | failed | 7 / runner-output | Not executed |

These are engine controls, not a native Cursor session or a product-benefit trial.
The command must come from the project's accepted verification, selected before
its outcome is known. Do not use `continue_on_error: true`, an agent's summary, or
an arbitrary success command as the completion check. Shell execution alone still
does not prove that a meaningful/non-empty test selection ran.

**Superpowers already captures some real execution, but not the full evidence
contract.** The vendored v7.0.2 `executing-plans/scripts/task-done` runs its supplied
command, writes a log, and appends completion only for exit zero. Disposable probes
observed exit 7 keeping the log without a completion line, and exit 0 adding one.
However, `true` also added completion with no output. After a tracked file changed
without a commit, the ledger still reported the same BASE..HEAD range. This is an
execution helper, not an independent test selector or a dirty-state receipt.
Reuse it for plans that already use it; do not force tiny edits into a plan just
to obtain a log. Its scratch ledger is not the durable feature record.

**Spec-gates supplies real command execution and structured gate observations.**
The installed v0.5.0 `verify.sh` produces policy hash, runtime version, gate result,
duration and applicable tool metadata. For the custom project-gate probe,
`candidates` and `checked` were null. The basic attestation had no source commit,
dirty-tree identity, required-test IDs or artifact digest. It is an unsigned local
record; `attestation` is not a promise of authenticated task evidence. Its write
failure is a warning and does not change the gate result. Preserve useful native
observations instead of assuming this object satisfies the kit's full evidence contract.

There is also a newly relevant upstream correction. [Spec-gates v0.5.1](https://github.com/schwichtgit/spec-gates/releases/tag/v0.5.1),
released 2026-11-03 at `a42f1f7d34c6e190b5a640d67244cf6f071d07e7`, fixes inherited
Git repository variables for gate commands and false timeout reporting. A safe
v0.5.0 probe used two disposable Git repositories and a project gate that only
ran `git rev-parse --absolute-git-dir` inside the child and saved that text:

| Gate environment | Repository reported by the child command | Gate exit |
| --- | --- | --- |
| No inherited GIT_DIR/GIT_INDEX_FILE | Child | 0 |
| GIT_DIR/GIT_INDEX_FILE point at the caller | Caller | 0 |

This reproduces misdirected repository identity, not destructive corruption or a
native Git-hook invocation. The reviewed v0.5.1 diff clears those variables and
exports the commit index separately as `GATES_GIT_INDEX_FILE`. Before further
linked-worktree Git-hook use, qualify that pinned upgrade with existing upgrade
controls and the Git-environment case. v0.5.1 was source-reviewed, not installed
or executed here. This does not reopen the native Stop retry budget or justify
promoting spec-gates to required checks.

**Native host hooks are useful at different boundaries.** Current [Cursor hook
documentation](https://cursor.com/docs/hooks) describes context injection at
sessionStart, permission decisions before tool use, and follow-up messages at
Stop. These are not interchangeable: sessionStart does not block session creation,
and Stop requests another turn. Permission-hook failures can default to allowing
the action unless configured otherwise. Availability differs between IDE, CLI
and cloud; documentation is not a successful observation on the pinned host.
Keep the original unobserved-Stop finding. Use actual host permission boundaries
for unauthorized effects; more Stop prompts are not a substitute.

### Which external capability closes which gap

| Capability | What to reuse | What it does not solve |
| --- | --- | --- |
| Spec Kit shell step, already pinned | Deterministic verification after implementation when that workflow is used | Automatic invocation in ordinary chats; adequate test selection; fresh artifact identity |
| Superpowers task-done, already vendored | Real command log and failure-sensitive task completion | Test sufficiency, dirty/untracked identity, durable publication, authenticity |
| Spec-gates, already experimental | Shared gate dispatch, time bounds, native observations and negative canaries, after relevant upgrade qualification | Full task acceptance, trusted local provenance, proven Cursor dispatch; current adapter still duplicates a direct suite |
| Existing test runner and GitHub Actions | Native results, run/job links and execution tied to the checked-out revision | Correct oracle, required execution of skipped tests, or an uncommitted local tree |
| Previously reviewed Agent OS / Ruler / OpenSpec | Context selection / instruction distribution / specification lifecycle respectively | None supplies the missing execution-and-evidence connection by itself |

No new framework is required for the first useful change. Reuse the existing
runner's output format and CI before introducing a custom result normalizer.
Local capture improves accidental omissions and stale reports; it is not a security
boundary against an agent that can edit both checks and records. Stronger assurance
comes from independently executed CI and the project's existing review/permission
controls, rather than signing self-authored local assertions.

### Recommended next slice, not yet activated

1. **Connect execution to completion.** In `.specify/workflows/ai-governance/workflow.yml`,
   add a final native shell verification step for the host-selected command. Keep
   direct verification available for ordinary chats and small edits through the
   existing governed-work/host entry point. Do not require Spec Kit for every task.
   Use one implementation of each check; workflow, local invocation and CI should
   call it. Begin with a real kit maintenance task and its existing applicable
   checks, rather than another calculator comparison or a new downstream prerequisite.
2. **Connect results to the tested state.** Populate the existing `AI RUN EVIDENCE`
   block from the command result or native CI run: command/selection, executed
   revision, dirty and relevant untracked identities when local, configuration,
   exit/status and resolvable log/result reference. Record a failed/missing run as
   such. Retain native reports; only add a small format adapter if a concrete runner
   cannot supply what is needed. A report-shaped pass must not upgrade a task to
   VERIFIED. A later relevant edit makes the previous result historical.
3. **Qualify only the host automation actually needed.** Observe one fresh session
   finding the active policy and using the canonical check on a real scoped task.
   Validate negative cases at the boundary claimed: failure, omitted required
   check, stale state, timeout/cancellation where supported. Only then count a
   native hook as active. Fix/qualify the spec-gates Git-environment issue before
   further linked-worktree hook use; direct verification does not depend on that upgrade.

For CI evidence, distinguish PR head from the actual tested merge commit, and
record the run attempt/job. A green badge alone can include skipped/neutral
checks; inspect the required step and native result. [GitHub documents both
revision and skipped-check behavior](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks),
and [pull_request checkout semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request).
Changing branch protection is a separate adoption decision, not part of this analysis.

The outcome to measure is narrower than general productivity: an authorized task
cannot be recorded as verified when the selected check was omitted, failed, or
belongs to an older relevant state. Preserve normal successful completion, bounded
repair and the host's current authorization. Do not add a universal orchestrator,
telemetry service, new mandatory form, repeated approval gate or CM increase.

### Verification and primary-source trace

- On the clean reviewed revision, `timeout 60s python3 -m unittest
  ci.gate_tests.test_work_procedures ci.gate_tests.test_test_evidence
  ci.gate_tests.test_stop_hook_contract ci.gate_tests.test_open_claim_limits -v`
  passed **43 tests, 0 skips**. This includes the original R1/R2 failure controls
  and the hand-written-evidence limitation. Python 3.12.14, Linux; no native agent run.
- Additional disposable observations: Spec Kit engine pass/fail (2 cases),
  Superpowers command/log/completion/dirty-state behavior (4 cases), and spec-gates
  inherited-Git-environment control (2 cases). These are bounded execution probes,
  not a repeat of full upstream suites or a measurement of agent benefit.
- The reviewed main's [hygiene job](https://github.com/rhemzal/AI_governance/actions/runs/41726325714/job/126231926055)
  reports success. CI regression execution is not downstream activation.
- Spec Kit source: [shell step](https://github.com/github/spec-kit/blob/4572a67fe0e72a6837e2d7bb0fda875bc41482e5/src/specify_cli/workflows/step/shell/__init__.py)
  and [agent-command step](https://github.com/github/spec-kit/blob/4572a67fe0e72a6837e2d7bb0fda875bc41482e5/src/specify_cli/workflows/step/command/__init__.py).
- Superpowers source: `vendor/superpowers/v7.0.2/skills/executing-plans/scripts/task-done`,
  pinned to `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`.
- Spec-gates source: `.specify/gates/verify.sh`, `lib/watch.sh`, `lib/attest.sh`,
  and the [v0.5.0 to v0.5.1 diff](https://github.com/schwichtgit/spec-gates/compare/v0.5.0...v0.5.1).

Disposition: analysis merged in PR #49. The recommended workflow/evidence
connection and spec-gates qualification are implemented on this kit tree per
`## Audit implementation status` below and `adr/ADR_0016_Workflow_Post_Implement_Acceptance.md`.
The analysis section above remains the reviewed snapshot; it does not re-run after
each implementation commit.

## Audit implementation status (2026-11-04)

Tracks proposals from PR #49 (`research/kit-capability-audit-20261103`) against this tree.

| Audit item                                                          | Status                                                               | Evidence                                                                             |
| ------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| R1 — refuse stale upgrade staging                                   | Implemented on `main` (`52f9c26`)                                    | `test_work_procedures.test_upgrade_refuses_a_stale_staging_directory`                |
| R2 — preset copy failure leaves registry consistent                 | Implemented on `main` (`52f9c26`)                                    | preset failure controls in `test_work_procedures`                                    |
| Connect execution to completion (Spec Kit shell after `implement`)  | Implemented                                                          | `.specify/workflows/ai-governance/workflow.yml`, `test_workflow_acceptance`          |
| Connect results to tested state (`AI RUN EVIDENCE` from native run) | Implemented                                                          | `ci/run_task_acceptance_check.sh`, `usage/AI_RUN_EVIDENCE.md`                        |
| Kit maintenance default acceptance command                          | Implemented                                                          | `ci/kit_maintenance_acceptance_cmd.sh`                                               |
| Refuse no-op acceptance commands                                    | Implemented                                                          | runner guard + `test_runner_refuses_a_no_op_acceptance_command`                      |
| Evidence validator missing-artifact advisories                      | Implemented                                                          | `validate_test_evidence.py`, `test_hand_written_report_is_verified_without_a_runner` |
| Superpowers `task-done` disposable limits                           | Implemented                                                          | `test_superpowers_task_done.py`                                                      |
| Spec-gates Git environment + pin v0.5.1                             | Implemented; re-project via `install-and-project.sh` (release zip + holds) | `test_spec_gates_git_environment.py`, `.specify/gates/.upgrade-holds`, projected runtime at 0.5.1 |
| Qualify native host Stop / named downstream trial                   | Partial — named checkout active; Stop dispatch still unobserved    | MechWeave `main`: ADR 0023, PR #1 stack merge, workflow `eeb22cb0`; `docs/GOVERNANCE_OPERATOR.md`; always-on `.cursor/rules/autonomous-aep-execution.mdc` |
| Operator UX — inline AEP without `/governed-work`                   | Documented + template                                              | `OPT_IN_STACK.md`, `check-opt-in-stack.sh`, `FOR_EXISTING_PROJECTS.md` § Intuitive agent execution (`6ca1c0f`) |
| Productivity / benefit trial                                        | Not claimed                                                          | B6–B8 records show matched acceptance, not a gain                                    |

### Downstream operator UX (2026-11-04)

MechWeave completed an authorized full opt-in trial on `main` (kit pin readopt through
**32e601e**, later kit docs at **6ca1c0f**). Disposable workflow run **`eeb22cb0`**
completed specify→verify-acceptance. Operators reported that requiring **`/governed-work`**
felt like a second startup ritual despite an existing autonomous mandate in host `AGENTS.md`.

**Recorded fix:** always-on Cursor project rule
(`.cursor/rules/autonomous-aep-execution.mdc`, `alwaysApply: true`) plus host mandate text;
optional skill entry remains for routing documentation. **`check-opt-in-stack.sh`** warns when
install phases are incomplete (missing Superpowers pin, rule, venv, gates). This does not
close native Stop observation or productivity claims.

## Automated control scenarios (2026-11-05)

**Reviewed kit revision:** `dde8748534e096a4e5e469dd4ec9973dd175f63c`.
**Evaluated by:** Codex, at the maintainer's request for established, automated
scenario evaluation. **Category:** testing / tooling. **Verdict:** DEFERRED
(bounded Harbor pilot recommended; no runner adopted by this documentation change).
**Claim card:** none; no thesis is promoted into the constitution or required CI.
**Oracle:** scenario, planned; package/configuration checks observed below.

### What is missing now

The kit has executable regression tests and an acceptance-command runner. These
test helpers or execute a selected command; they do not create independent agent
sessions, exercise governance variants, or grade their actual behavior.
`ci/benchmark_trials.py` checks record structure and
`ci/validate_test_evidence.py` checks supplied evidence. Neither runs an agent trial.

The latest useful screening work should be preserved, with its limits:

- [Experiment A](../specs/003-task-scoped-overlay-trial/progress.md) reports a
  partial PASS. C2 is a read-only check, C3 an explanation, and B0 an in-session
  proxy. These are not repeated, isolated task executions. Fewer cited overlay
  rows in C4 do not establish less context loaded or lower token use.
- [Experiment B](../specs/004-fresh-context-review-trial/progress.md) labels B0
  simulated. Its symlink regression follow-up is a real improvement, but the
  record does not establish the incremental benefit of fresh-context review.
- Superpowers 7.0.2 and content-aware dirty-tree identity are already implemented;
  this proposal does not repeat those upgrades.

Keep binary acceptance **for each completed, valid scenario**. Preserve execution
errors, cancellation, missing evidence and unsupported observations separately;
none counts as PASS. A scenario whose full criterion is unobserved remains
unverified even if its narrower artifact checks pass.

### Select one existing runner

| Candidate | Relevant capability | Fit and disposition |
| --- | --- | --- |
| **Harbor 0.25.0**, Apache-2.0 | Native `cursor-cli` adapter, disposable environments, repeated trials, native results/trajectories and a separate verifier environment | **First pilot choice for the current Cursor-oriented adoption.** Use its task and result formats. Python 3.12+ and Docker make this an optional evaluation environment, not a baseline kit dependency. |
| **Promptfoo**, MIT | Existing coding-agent providers, isolated working directories, assertions and repeated evaluations | Good alternative for supported Codex/Claude/OpenCode runtimes or text/prompt tests. The inspected provider list has no native Cursor adapter; a custom provider would add lifecycle/isolation work. Do not install both runners for this pilot. |
| **Inspect AI**, MIT | Sandboxed agent evaluation, scoring and an agent bridge for external agents using supported model API proxies | Credible alternative, but this investigation did not qualify Cursor through the bridge. Defer unless a required evaluation cannot be expressed with the selected runner. |
| Existing **Python unittest** | Deterministic checks of files, helper behavior and expected failures | **Retain as verifier building blocks.** Replacing it with pytest or a behavior-description framework would not supply native agent execution. |

This is a fit judgment, not an empirical performance ranking. Harbor fills the
execution/evidence gap; it does not supply the kit's definition of correct behavior.
Small task-specific assertions remain necessary. A new scheduler, provider
abstraction, scenario language, results database or dashboard is not justified.

### Execution and grading boundary

Use Harbor to start a fresh disposable fixture for each scenario, policy variant
and repetition, run the actual selected agent, collect outputs, and invoke the
verifier. Configure `verifier.environment_mode = "separate"` explicitly. Pass
only declared task outputs into a trusted verifier image; do not let those paths
replace verifier code or its expected fixtures. A verifier without network access
can run the applicable existing checks against the collected files. This checks
the result, rather than accepting the agent's statement that tests passed.

Retain native per-trial `result.json`, agent logs/trajectory, verifier logs and
artifacts. Record the kit/fixture revisions, task checksum, Harbor and agent
versions, model/configuration, image digest, attempt and policy variant. Require
the particular native trace when a criterion depends on it; absence is not success.

Harbor's successful CLI exit is not an assertion that every reward equals one.
Use a small, separately tested **result gate** over native trial results: require
the complete expected scenario/variant/attempt matrix, the intended configuration,
finished trials, required artifacts and no disqualifying exceptions. For a
candidate acceptance gate, require reward `1` on every required candidate control;
retain baseline failures as comparison evidence, not automatic rejection of a
successful candidate. Reject missing, duplicate or unexpected attempts.
Do not use average reward or best-of-k to conceal a critical failure. This adapter
only converts native results to a CI exit status; it must not start agents or
introduce another evidence schema. Link the native result from `AI RUN EVIDENCE`.

| Existing control | Automated observation to implement | Limit to preserve |
| --- | --- | --- |
| **C1: forbidden import change** | Immutable importer checks and expected file state, plus a required decision/compliant-alternative artifact so doing nothing cannot pass; B1 also cites the matching overlay row | Original acceptance says refusal before any bad diff. Final files alone cannot prove that temporal condition; qualify native event evidence or report that part unverified. A structured refusal alone also does not prove safe behavior. |
| **C2: permitted documentation edit** | Actually request and check a small `usage/` edit, its exact required content and permitted changed paths | Reading a file, returning an explanation or leaving the fixture unchanged must fail. This is the positive control for excessive blocking. |
| **C3: permitted `cp -aL` exception** | Actually perform the copy in a disposable fixture; check copied bytes, destination state, an untouched sentinel and unchanged importer guards | Explaining the exception is insufficient. Preserve the distinction between the opt-in copy exception and the importer's symlink prohibition. |
| **C4: task-scoped context** | Check the requested task result; count cited rows only as report-format compliance. Measure loaded paths/tokens only when the native host exposes reliable observations | At most three citations does not prove at most three rows entered context. Do not claim context savings from citation count. |
| **Fresh-context review** | Seed a known defect and a clean control; run actual independent reviewer sessions and check a concrete finding/counterexample | A simulated baseline or another reviewer saying PASS is not an independent comparison. Ambiguous review quality may need human calibration; an LLM judge is not the sole oracle for filesystem facts. |

Use the existing scenario IDs; C1-C4 belong to Experiment A and are not the kit's
B1-B8 benchmark IDs. Harbor's Cursor CLI batch run does not establish native IDE
Stop dispatch, approval UX, or resumed-session behavior. Its documented Cursor
capabilities do not include native resume. B7 therefore stays outside this first
slice rather than treating a new process as a resumed session.

### Smallest implementation and local handoff

**Implementation AEP status: BLOCKED in this investigation environment.** Docker
and Cursor CLI are unavailable here. This blocks native execution, not use of the
research or preparation on an authorized capable host. **Task class:** cross_cutting.
**Risk:** HIGH for the future execution/result boundary; this assessment is
documentation only. **Objective:** automate the C1/C2 slice using Harbor, then
decide whether its observed benefit justifies adding C3 and later controls.

**Scope:** new native task/configuration files under
`research/experiments/harbor/`, a narrowly scoped `ci/check_harbor_results.py` and
`ci/gate_tests/test_harbor_results.py` only if needed to enforce native result
acceptance, plus this research entry and existing benchmark/documentation links.
Consider an ADR for that executable boundary. An optional
`.github/workflows/governance-scenarios.yml` is a later step after local
qualification. No adopter bundle, mandatory gate, new cloud account, repository
merge, deployment or mutation of another repository is part of this pilot.

1. **Qualify the host and freeze inputs.** On an authorized Docker-capable host,
   pin Harbor 0.25.0 in a dedicated environment, record the image digest and use
   existing host-managed credentials. Its Cursor adapter installs the current
   CLI: capture actual `cursor-agent --version` output on every trial and reject
   a comparison with unknown or differing versions. A recorded version is not
   an enforced installation pin. For repeatable future runs, qualify an upstream
   version with native pre-installed-agent support; do not assume the live docs'
   `skip_install` option exists in 0.25.0. Fix model, budgets and fixture revision
   before comparison. Keep
   the agent's permissive batch command inside the disposable container; never
   mount the real working repository or Docker socket into it.
2. **Build only C1/C2 native tasks and verifiers.** Use Harbor's `task.toml`,
   `instruction.md`, `environment/`, `solution/` and `tests/` conventions. Freeze
   the acceptance checks independently of the agent under test. B0 and B1 differ
   only in the task-scoped loading mandate, with identical task goals, capabilities
   and outcome assertions; keep B1's additional citation requirement explicit.
   Declare which C1 observations are supported before running.
3. **Qualify grading before spending model calls.** Run `harbor lint` on each
   task, then the native `oracle` and `nop` agents. Valid reference solutions must
   pass; no-op, forbidden-change and malformed/missing-output controls must not.
   An oracle is a known reference solution, not an LLM opinion. Test the result
   gate with complete, failing, errored, missing and duplicated native results.
4. **Run the actual comparison.** Use native `harbor run --config ...` with
   `--n-attempts 3 --n-concurrent 1 --max-retries 0`, a new job directory and
   fresh sessions per variant. C1/C2 x two variants x three repetitions is
   twelve agent trials, excluding oracle/negative controls. Retain every attempt,
   including timeouts; record any deliberate rerun separately. Three repetitions
   are a screening budget, not statistical proof of a general improvement.
5. **Automate only the qualified path.** Keep cheap deterministic checks in
   ordinary CI. Initially expose expensive live trials through one local command
   and, after qualification, a manual `workflow_dispatch` workflow using the same
   configs/verifiers/result gate. Retain failed-run artifacts too. Add selective
   change triggers only after the runtime/cost budget is observed; every Markdown
   PR does not need a paid model run.

**Verification:** `harbor lint` for task structure; oracle and negative controls
for graders; `timeout 60s python3 -m unittest
ci.gate_tests.test_harbor_results -v` for the proposed adapter; real Cursor runs
and the result gate for the required trial matrix. `--dry-run` / `--print-config`
can check preparation but cannot substitute for native execution.

**Acceptance:** one documented command performs execution through grading without
manual PASS editing; independent graders reject known-bad/no-op outputs; all
required observations and attempts are accounted for; a failed or unverified
critical candidate control blocks its successful acceptance claim. Report correctness separately
from any measured improvement. If B0 and B1 both pass without an observed benefit,
claim regression coverage, not evidence for adding more governance.

**Repair budget:** two bounded integration repair attempts. If the native adapter,
isolation or required observations still fail qualification, retain evidence and
defer that scenario; do not build a custom runner to save the pilot. Re-evaluate
Promptfoo only if a supported host replaces Cursor or the concrete boundary changes.
**Rollback:** remove the optional experiment/adapter and its optional workflow;
existing kit acceptance remains usable. **DOC DELTA:** this entry and benchmark
instructions gain actual command, pins, artifacts and observed limits only after
qualification. No automated scenario completion is claimed by this proposal.

### Qualification evidence and sources

On 2026-11-05, an isolated local environment installed **Harbor 0.25.0** on Python
3.12.14 (92 packages). `harbor --version`, CLI help, importing `CursorCli`, and
native `TaskConfig` validation succeeded. The configuration accepted a separate
verifier with `network_mode = "no-network"` and rejected explicit shared mode
combined with a verifier environment. Native repeat/retry/dry-run/config-print
options were present. These are package/contract checks, not a Docker smoke test
or successful agent scenario. No model calls or model credentials were used.

Source inspection also found a release/documentation difference: 0.25.0 has no
`skip_install` option, and its Cursor `install()` invokes the current upstream
installer. Live documentation describes pre-installed-agent support. Therefore
long-term agent-version pinning remains a qualification item, and the first
comparison must validate actual versions rather than trusting a requested label.

The package is free/open source; model inference and a runtime host may cost money.
Local Docker execution does not require Harbor Hub publication. Use
`HARBOR_TELEMETRY=0`, keep trial outputs local, and omit hosted launch/upload options
for this pilot. Harbor belongs in an **optional evaluation environment**, usable
to evaluate Tier A/B/C behavior on a capable host; it is not another mandatory
Tier C component or a dependency for snapshot-only adopters.

Primary sources (accessed 2026-11-05; live docs may move beyond the pinned release):

- [Harbor v0.25.0 source](https://github.com/harbor-framework/harbor/tree/fdba28fc411e47e8765420a1a063b4918fce3def), including `pyproject.toml`, `src/harbor/agents/installed/cursor_cli.py`, task/trial result models and `src/harbor/cli/jobs.py`.
- [Native agent adapters and capability limits](https://docs.harborframework.com/agents/pre-integrated-agents), [separate verifier](https://docs.harborframework.com/tasks/separate-verifier), [verifier contract](https://docs.harborframework.com/tasks/verifier) and [job execution](https://docs.harborframework.com/jobs/run-a-job).
- [Promptfoo coding-agent evaluation](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/), [custom script provider](https://www.promptfoo.dev/docs/providers/custom-script/) and [inspected source](https://github.com/promptfoo/promptfoo/tree/e3e2bb871540ae153a630878ecb17e56cfb487e3).
- [Inspect AI agent bridge](https://inspect.aisi.org.uk/agent-bridge.html) and [inspected source](https://github.com/UKGovernmentBEIS/inspect_ai/tree/27f18ff7d5bd4b8d7752912c1e0cd28e2e912e88).

**What a hollow pass would look like:** an agent writes “PASS,” the runner exits
zero or a result file parses, while the intended action, independent assertion or
required trial never happened. **Re-evaluation trigger:** first native C1/C2
qualification with all evidence, a changed agent host, or a pinned runner upgrade.

## Related Documents

- `research/PROFESSIONAL_STANDARDS_AND_REFERENCES.md`
- `constitution/AI_RULES.md`
- `adr/ADR_0004_Tooling_Is_Experimental.md`
- [Spec Kit + spec-gates pilot](SPEC_KIT_SPEC_GATES_PILOT.md)
- [Engineering-method evidence review](AI_ENGINEERING_METHODS_EVIDENCE.md)
