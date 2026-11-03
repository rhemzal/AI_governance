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
| Selected Superpowers procedures | v7.0.1 pinned with MIT license, hashes, six skill links and a governed entry point; `specs/001-benchmark-trial-records/progress.md` records debugging, continuation, stale-result handling and a review finding | One recorded use; host discovery and repeatable use beyond that slice have not been independently demonstrated here                                                                                                                       |
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

## Capability and adoption re-audit (2026-11-03)

**Reviewed revision:** [`fb2cf2d293d39d6894d183c24000468621b7a600`](https://github.com/rhemzal/AI_governance/commit/fb2cf2d293d39d6894d183c24000468621b7a600).
This is the current assessment. It supersedes the capability findings from
PR #49 at `5cab4ccfe943a17c722b348c296765721523dd68`; that earlier report remains
in git history. The adoption-completion section above retains its dated evidence.

Scope: changes since `9fdc6846d60f604c8030c87bfbe7572815dab858`, the kit's
adopter entry points, optional procedure/preset transfer, selected upstream
adaptations, and existing executable regression suites. This is a focused
adoption audit, not release closure or a new audit of every architecture note.
Native agent sessions and the recorded OpenSpec experiment were not rerun.

**Verdict:** the kit now uses more of the research than Spec Kit and Superpowers.
It incorporates Agent OS's local-constraint discovery method and offers an
OpenSpec lifecycle as a conditional alternative. Simplification has materially
improved: the transfer feature is one 26-line ledger instead of ten documents.
However, the optional transfer instructions still contain two reproducible
failure cases. Passing regression suites do not establish safe execution of
every published shell block, host activation, or an agent productivity gain.

### Reassessment of the previous findings

| Previous finding | Current disposition and evidence |
| --- | --- |
| C01: local discovery was only a recommendation | Mechanism implemented in `usage/ENGINEERING_METHODS_ADOPTION.md`, routed from `usage/FOR_EXISTING_PROJECTS.md`, and instantiated in the upstream `governance/LOCAL_OVERLAY.md`. At most three source-backed constraints, exceptions and task-specific loading; no second standards tree. Repeated benefit in another project remains unmeasured. |
| C02: a valid empty preset registry ignored the copied preset | Original failure fixed. The published command now registers it; the existing empty-registry regression passes. R2 below concerns failure recovery, not the old activation defect. |
| C03: ten documents and stale tasks for one transfer recipe | Fixed for this slice. `specs/002-opt-in-transfer-recipe/` contains only `progress.md`; the recipe stays in `usage/HOW_TO_IMPORT.md`. The old executable AEP was retired. Keep direct edits available for small changes. |
| C04: workflow completion was treated as implementation/benefit | The distinction is now explicit. Run `b6a246fd` was plan-only; committed records report actual implementation in disposable run `8ecad04d`. B6/B7/B8 show equal task acceptance, not a gain. These native observations are attributed to the records, not independently repeated here. |
| C05: no practical delta/archive alternative | OpenSpec 1.16.0 has a documented modified/removed/unchanged requirement trial in `usage/SPEC_DRIVEN_AI_DEVELOPMENT.md`. Qualification is partial: the recorded Node 20.19.2 did not meet the package's Node >=22.12.0 requirement. Use a supported engine before a real adoption decision. It is an alternative, not another authority for the same change. |
| C06: portability beyond Cursor unproved | Still a limitation, not a reason to install another framework. The generic host pointer supports manual routing; the copied native entry is Cursor-specific. Evaluate another host only when it is actually needed. |

### R1 — P1: an interrupted upgrade can silently reactivate the old pin

Location: `usage/HOW_TO_IMPORT.md` lines 268–277 at the reviewed revision;
coverage gap in `ci/gate_tests/test_work_procedures.py` lines 195–222.

The upgrade runs `cp -aL SOURCE vendor/superpowers/v7.0.1.next` without first
refusing an existing staging directory. If a previous attempt left a valid old
pin there, `cp` nests the new `v7.0.1/` inside it. The checksum command reads the
old staging manifest and passes. Both renames succeed, leaving the old pin active
and the new pin nested one directory below it. The complete command exits 0.

Reproduction used disposable copies of the pinned source. A candidate `PIN.md`
received an `AUDIT-NEW-PIN` marker and its own SHA256SUMS was regenerated. The
exact upgrade fence was extracted from the published guide and run with `NEW_KIT`
pointing to that candidate, once with no staging directory and once with an old
valid pin already copied to `v7.0.1.next`.

| Initial staging state | Shell exit | New marker in active PIN.md | New pin nested inside active directory |
| --- | --- | --- | --- |
| Absent | 0 | Yes | No |
| Existing valid old pin | 0 | No | Yes |

The current upgrade test constructs a fresh staging directory itself and calls
`_activate_staged_pin`; it does not execute the published upgrade block. The
textual fence test cannot detect this failure either.

Smallest repair: preflight the active/staging/previous paths before copying;
refuse existing or symlink staging/previous destinations without deleting them.
Exercise the actual documented shell block in the existing test module. Keep
one successful upgrade/rollback control and an interrupted-upgrade control;
assert the active marker and preservation of host sentinels, not only exit 0.

### R2 — P2: failed preset copy leaves an enabled registry entry behind

Location: `usage/HOW_TO_IMPORT.md` lines 232–265 at the reviewed revision.

The command writes `.specify/presets/.registry` before copying the preset. Its
destination guard uses `test ! -e` without the dangling-link guard already used
by the procedure copy. With a dangling destination symlink, the guard passes,
the registry changes, and real `cp` fails. The preset is absent but enabled in
the registry. A copy failure after otherwise valid preparation has the same effect.

Both probes used a real reviewed `KIT` and an initially valid empty registry:

| Failure control | Shell exit | Original registry bytes preserved | Preset installed |
| --- | --- | --- | --- |
| Dangling destination symlink; real `cp` | 1 | No | No |
| Injected `cp` executable exiting 28 | 28 | No | No |

The second row is fault injection, not an observation of an actual full disk.
The command reports failure; this is inconsistent recovery state, not silent
successful activation. Existing entries must continue to retain their local policy.

Smallest repair: validate source and destination before changing the registry,
stage and validate the copy, and preserve/restore the registry when publication
fails. Add these failure controls to the tests that already extract the preset
fence. No general installer, new registry schema, or new CI service is needed.

### Evidence limits and small documentation drift

- `test_activation_smoke_after_opt_in_copy` checks files and routing text. It
  neither launches an agent nor observes skill selection. Keep it as a structural
  check; it does not close a native activation or downstream-use criterion.
- The named downstream task remains unperformed. Do not repeat calculator
  experiments to manufacture confidence. On the next actual authorized project
  task, record which rule/procedure the agent used, the resulting change, and its
  normal acceptance check in the existing task record.
- Native Cursor Stop remains unobserved. Deferring spec-gates promotion is
  appropriate: the adapter currently runs the same direct gate suite and has not
  demonstrated infrastructure removal. Its exhausted host retry budget stays closed.
- `DEVELOPMENT.md` line 42 still says B5–B8 have no trial record, without a date.
  B6/B7/B8 records now exist. Date that historical observation and link the current
  ledger. Do not turn this wording correction into another evidence framework.

### What to retain, and what would justify another adoption

| Capability | Decision |
| --- | --- |
| Safe bundle import, host precedence, bounded execution and existing checks | Retain as the kit's foundation. The optional transfer failures above are separate from the snapshot importer's passing tests. |
| Selected Superpowers procedures and three Spec Kit append sections | Retain as optional, bounded adaptations; no claim of demonstrated speed or safety improvement. Keep small edits outside a feature-document cycle. |
| Agent OS discovery/injection idea | Retain the compact overlay method already adapted. Use relevant rows on real work; do not install its whole standards/approval workflow. |
| OpenSpec delta/archive | Conditional alternative for changing canonical requirements; qualify on supported Node before use. Do not add it beside Spec Kit for the same change. |
| Ruler / SpecGov | No new installation now. Revisit Ruler for observed two-host instruction drift; revisit SpecGov for an actual code-to-spec mapping defect. Neither is required to fix R1/R2. |
| Spec Kit Lean / spec-gates promotion / extra orchestrators | Keep deferred under the recorded compatibility, host-evidence and maintenance limits. |

The free upstream capability worth using now is the already adapted local-context
method. Additional installations are not the missing acceptance criterion. A useful
next slice is to repair the two delivery failures and use the existing kit on real
work. No new mandatory checks, process scale, approval loop, or framework is proposed.

### Verification and disposition

Fresh local checks at the reviewed clean revision, Python 3.12.14, Linux, root:

| Command (each with a 60-second timeout) | Result |
| --- | --- |
| `python3 -m unittest discover -s ci/gate_tests -q` | 99 discovered; 97 passed, 2 permission cases skipped under root |
| `python3 -m unittest discover -s ci/tests -q` | 18 passed |
| `python3 -m unittest discover -s ci/ratchet_tests -q` | 13 passed |
| `KIT_MANIFEST_JSON=... python3 -m unittest discover -s ci/bundle_tests -q` | 35 passed, including exclusion of the maintainer overlay |

Total: **163 passed, 2 skipped, 0 failed** in existing suites. The bundle suite
received JSON converted from the real manifest with PyYAML; that conversion is
not a separate verification of yq. The gate suite includes the existing yq and
offline lychee canaries. The bundle suite's two `FAIL: disk full` messages are
expected injected-failure fixtures. The R1/R2 probes above are additional audit
observations, not passing regression tests or fixes. The reviewed main's
[doc-hygiene job](https://github.com/rhemzal/AI_governance/actions/runs/41723621667/job/126222540581)
also reports success.

Priority: fix R1, then R2 in the same optional-transfer area; correct the dated
documentation sentence while there. Acceptance is the real shell blocks passing
good cases and refusing/preserving state in the listed bad cases. Do not restart
the retired adoption AEP or create another feature specification for this audit.

This report changes only research documentation and its README/changelog entry.
Runtime repair is not claimed. No adopter repository was modified. Existing kit
CI is sufficient; Governance Level G2 and the host's current CI Maturity remain
unchanged. A new architecture decision is not needed for this advisory report.

## Related Documents

- `research/PROFESSIONAL_STANDARDS_AND_REFERENCES.md`
- `constitution/AI_RULES.md`
- `adr/ADR_0004_Tooling_Is_Experimental.md`
- [Spec Kit + spec-gates pilot](SPEC_KIT_SPEC_GATES_PILOT.md)
- [Engineering-method evidence review](AI_ENGINEERING_METHODS_EVIDENCE.md)
