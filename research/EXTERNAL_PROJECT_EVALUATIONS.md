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

**Verdict**: INSPIRATION ONLY for the landscape; DEFERRED for production adoption.
Spec Kit + spec-gates received an isolated executable pilot below. No other project
in this entry was installed or benchmarked during this investigation.

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
| [schwichtgit/spec-gates](https://github.com/schwichtgit/spec-gates/tree/v0.5.0), v0.5.0                                                        |                    3 | Shared gate runtime, Claude hooks, Git hooks, CI projections, custom checks and planted-violation canaries. Closes an actual integration gap despite low popularity.                                                             | **DEFERRED**: retain as a pilot candidate; native hooks, CI wiring and upgrade behavior remain to prove.                                                                                                                                                                     |
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
  qualification. Git/CI controls still need actual wiring.
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

| Layer in AI_governance                                                                                  | Decision                        | Candidate / acceptance condition                                                                                                         |
| ------------------------------------------------------------------------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Normative policy, action authority, proportional G/CM levels, architecture tradeoffs and ADR discipline | Keep                            | No reviewed tool proved equivalent coverage or decision quality.                                                                         |
| Instructions, templates and workflow distribution                                                       | Pilot replacement               | Spec Kit; preserve host instructions and one source of policy truth.                                                                     |
| Repeated hook dispatch, projection bookkeeping and basic negative canaries                              | Pilot replacement               | spec-gates; prove host lifecycle, Git/CI wiring, safe reapply/upgrade and local-change preservation.                                     |
| Required evidence schema and acceptance decisions                                                       | Keep; invoke through an adapter | Existing `ci/validate_test_evidence.py`; upstream command success alone cannot establish coverage, authenticity or fresh test execution. |
| Debugging/TDD task recipes                                                                              | Optional comparison             | Superpowers on the same task and host, measuring missed failures and operator intervention.                                              |
| Persistent context and multi-agent architecture                                                         | Defer                           | GSD/Elephant Goldfish/Ruflo only against a demonstrated task need.                                                                       |

**Concrete adoption from this investigation**: the research record, an opt-in
experiment and its results. No candidate is activated by importing the kit.
Visible limits from the pilot are claim cards `stop-hook-fail-open` and
`native-stop-dispatch-unobserved`.

**Next decision**: the 2026-11-01 investment remains the Spec Kit + spec-gates
pilot in [the pilot record](SPEC_KIT_SPEC_GATES_PILOT.md). The 2026-11-03
follow-up is the pinned work-procedure slice above, not a framework migration
and not a claim that the Stop hook dispatches. A native-agent trial of that
hook is still open.

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

## Related Documents

- `research/PROFESSIONAL_STANDARDS_AND_REFERENCES.md`
- `constitution/AI_RULES.md`
- `adr/ADR_0004_Tooling_Is_Experimental.md`
- [Spec Kit + spec-gates pilot](SPEC_KIT_SPEC_GATES_PILOT.md)
- [Engineering-method evidence review](AI_ENGINEERING_METHODS_EVIDENCE.md)
