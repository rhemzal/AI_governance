# Changelog

This project follows a lightweight changelog intended for governance-kit consumers.

## Unreleased

### Agent runtime and evidence analysis (2026-11-04)

- [Advisory-only] Analyze `52f9c26f342b3517384e96f7d289bb300a72aaa4`: distinguish instruction loading, actual command execution, evidence validation and CI. Original upgrade/preset failure reproductions now pass their regressions.
- [Verification] 43 focused tests passed. Disposable probes demonstrate the already-pinned Spec Kit shell step, Superpowers completion limits and spec-gates v0.5.0's inherited-Git-environment issue. Review upstream v0.5.1's fix; no runtime upgrade performed.
- [Recommendation] Connect existing verification to workflow completion and state-bound native evidence before adding frameworks. Preserve native-host and downstream evidence limits; no policy or CI activation change.

### Preset activation (2026-11-03)

- [Fix] The opt-in procedure upgrade refuses an existing or dangling `v7.0.1.next` or `v7.0.1.prev` before copying a new pin, so an interrupted upgrade cannot nest the new pin under a stale staging tree and exit successfully with the old pin still active.
- [Fix] The Spec Kit preset command validates the kit source and destination (including dangling symlinks), copies the preset, then updates `.specify/presets/.registry`. A failed copy no longer leaves `ai-governance` enabled without an installed directory. An existing registry entry is kept, and a second run still stops when the directory is already present.
- [Verification] Activation smoke after opt-in copy is automated in `WorkProcedures.test_activation_smoke_after_opt_in_copy`.
- [Docs] `governance/LOCAL_OVERLAY.md` dogfoods the import constraint table for this upstream repo. `kit-manifest.yml` excludes it from bundle copy.
- [Docs] `usage/FOR_EXISTING_PROJECTS.md` adds a named downstream trial checklist and separates native Stop from workflow evidence.
- [Docs] The adoption table's remaining-gap column matches the current tree: B6, B7, and B8 are recorded, the opt-in recipe is tested on disposable fixtures, and a named downstream checkout is still not authorized.
- [Docs] spec-gates promotion stays **deferred**. Fresh parity on this tree: `verify.sh --boundary ci` and direct `ci/gate_tests` discovery both exited 0 (99 tests). The adapter remains experimental; native Stop dispatch is still unobserved.
- [Docs] The opt-in procedure is `usage/HOW_TO_IMPORT.md` § Opt-in work procedures. `specs/002-opt-in-transfer-recipe/` keeps that record in `progress.md` only. Disposable fixture tests are not a named downstream trial.
- [Docs] The adoption plan in `research/EXTERNAL_PROJECT_EVALUATIONS.md` is `NOT-REQUIRED`. It no longer tells an agent to create `specs/002-operational-adoption/` or to restart the transfer recipe. The earlier ready plan remains in git history.
- [Verification] Disposable `specify` 1.2.5 run `8ecad04d` used workflow `ai-governance` with an implement input. Steps specify, plan, tasks, and implement completed. `python3 -m unittest test_calc.py` exited 0, the expected value stayed, and `deploy.sh` did not run. This is not a named downstream trial and not an acceptance gain.
- [Docs] `usage/FOR_EXISTING_PROJECTS.md` states host-first agent context, overlay row loading, one requirement path, and the maintainer sequence after snapshot import.
- [Docs] Existing-project work can record at most three local constraints from one module, with sources, a reason already in the records, and an exception. The pass does not ask for approval per finding and does not add a standards tree. The worked example is the snapshot importer. A task loads only the rows that match the files it edits.
- [Docs] OpenSpec 1.16.0 is an optional path when an existing project's canonical requirements change and Spec Kit is not already their source. A disposable archive modified one requirement, removed one, and left one unchanged. It is not a second authority for this kit. The host Node was older than the package engine.
- [Docs] Spec Kit Lean at `4572a67` replaces the five core commands and does not load this kit's appended templates. A command-only preset registered ahead of `ai-governance` still leaves the mandate section on `spec-template`. Lean stays off the governed workflow.
- [Verification] One matched implement pair, `research/benchmark_trials/b8-2026-11-03.md`, passed with the profile text and without it. Neither arm ran the unauthorized deploy script. The comparison does not show a gain. Run `b6a246fd` remains a plan-and-tasks input, not this pair.
- [Docs] The profile and the pinned procedures stay. B6, B7, and B8 showed no acceptance gain, so no further preset section is added on that evidence. Disposable workflow run `8ecad04d` is the native implement observation; a named downstream checkout remains unmet.

### Re-adoption guard (2026-11-03)

- [Fix] `ci/import_bundle.py --readopt` joins the new snapshot with rules already in the project. A local difference is kept when the previous revision is unknown or both sides changed, and the report includes the upstream text. A file removed from the active snapshot stays removed when that revision still contains it. An unknown `--previous` SHA fails before any write. Host instructions and a root-layout `constitution/AI_RULES.md` are not overwritten. The active snapshot is not replaced.
- [Fix] The procedure upgrade command and the rollback command are separate. Rollback refuses to run when `v7.0.1.rollback` already exists. The first copy also stops when the pin or the entry skill is a dangling symlink.
- [Fix] Re-adoption refuses a symlink used as the adopted snapshot or as a root-layout directory. A failed copy removes only the snapshot that same run created, so the next run still reads the previous rules. Matching bytes keep the local file mode. An orphan `vendor/AI_governance.next` without an active snapshot is refused, and an existing report blocks a new run before any write.

### Opt-in copy guards (2026-11-03)

- [Fix] The procedure copy stops when the entry skill already exists, and rollback deletes the active pin only after `v7.0.1.prev` has been moved back. The Spec Kit preset is a separate command, not part of the one-task copy.

### Live-project procedure trial (2026-11-03)

- [Pilot] The opt-in recipe now says what is copied, what stays host-owned, how to invoke `.cursor/skills/governed-work/SKILL.md`, and how to remove the trial. The entry skill resolves kit policy under `vendor/AI_governance/` when the project root has no `constitution/`. spec-gates, the Stop hook, and `specify workflow run` are outside that trial.

### Audit findings A-08–A-17 (2026-11-03)

- [Fix] Separate kit workflow presence from branch protection. List gates A4, A5, and I1–I5 with Governance Level (G). Routine work uses the short compliance footer. A new architecture ADR follows Gate A3.
- [Fix] Correct the boundary example, the streaming exactly-once line, the unpublished `v0.3.0` tag, Copilot Chat setup, interface automation prompts, the audit finding quota, and the two release-readiness ADR links. Tracked Markdown links are checked in `ci/gate_tests/test_local_links.py`.
- [Fix] `usage/FOR_EXISTING_PROJECTS.md` points at the snapshot importer. `notes/README.md` points at the advisory parking-lot note.

### Adoption completion plan (2026-11-03)

- [Advisory-only] Reassess the implemented work-procedure pilot at `65fe471b6a2b9924295f5ea8eb9701856ea976c9` and preserve a follow-up Autonomous Execution Plan in `research/EXTERNAL_PROJECT_EVALUATIONS.md`. Credit the existing pin, profile, feature cycle and benchmark repair; prioritize native workflow use, safe opt-in transfer, matched debugging/resume observations and a spec-gates simplification decision.
- [Verification] Eight focused existing tests passed without skips; distinguish these checks and the recorded feature evidence from unrun native workflow and downstream trials. This is a plan, with no runtime, default import selection, constitutional rule or required-check change.
- [Pilot] `specify` 1.2.5 started workflow `ai-governance` as run `c37bf147` and finished only `specify`. A 45 second timeout left the run `running`. Resume refused that status. Run `b6a246fd`, started from the kit root, completed specify, plan, tasks, and implement with no approval prompt between them. That input asked for plan and tasks only. The entry skill now continues after a Spec Kit completion report, skips the pinned plan-review handoff, and reviews an uncommitted tree with `git diff HEAD`. The opt-in procedure copy is regular files, not symlinks, and is not a default bundle. A disposable upgrade checks the new pin's sums, then rollback restores the previous pin and leaves the local overlay unchanged.
- [Verification] Disposable B6 and B7 pairs both met the task and did not run the unauthorized deploy script. The governed-profile variant did not outperform the baseline on acceptance. `verify.sh --boundary ci` passes and fails with the direct `ci/gate_tests` discovery. spec-gates stays deferred. Native Stop dispatch was not rerun.

### Cursor stop notice (2026-11-03)

- [Experimental] When `verify.sh` is missing or exits with a code other than 0 or 2, the stop script asks once, at `loop_count` 0, for an UNVERIFIED report. A later `loop_count` allows the stop. `stop_hook_active` still allows the stop. The contract test calls the script directly and is not native host dispatch. Promotion stays deferred.
- [Experimental] On this host the Cursor Agent CLI runs a project `sessionStart` hook and does not run `stop`. The spec-gates v0.5.0 zip verifies with cosign. A disposable 0.4.2 to 0.5.0 upgrade keeps policy and a local edit, and removal leaves the projected runtime. With shellcheck, prettier, and markdownlint-cli2 installed, a clean `verify.sh` makes the canary suite 18 blocked and 0 accepted. See the 2026-11-03 host note.

### Pinned work procedures (2026-11-03)

- [Pilot] Pin Superpowers v7.0.1 for systematic debugging, inline plan execution, verification before a completion claim, and a fresh review. The entry point is `.cursor/skills/governed-work/SKILL.md`. A documentation or registry-wording change does not require test-driven development. `subagent-driven-development` is not installed. ADR-0015 records the decision. No constitutional rule change and no new adopter-mandatory workflow.
- [Pilot] Add a project Spec Kit preset that appends mandate, acceptance, and Autonomous Execution Plan pointers to the core templates. Workflow `ai-governance` runs specify, plan, tasks, and implement with no `review-spec` or `review-plan` gate. The bundled workflow still has those two gates.
- [Fix] The B5–B8 absence is a dated sentence again. `research/benchmark_trials/` may exist. A later trial file must name one scenario, one revision token, and an outcome of pass, fail, cancelled, or blocked. `README.md` is not a trial. A well-formed file is not a matched trial. Card `benchmark-scenarios-unrun` now states that rule.
- [Verification] One cycle is in `specs/001-benchmark-trial-records/`. The original directory prohibition failed with `AssertionError: True is not false`. The new test failed with `FileNotFoundError` before the checker existed, then passed. A later session resumed Task 2 without rewriting the checker and marked a changed scenario-file hash stale. Review found `cancelled` was rejected while the suite was green. The assertion failed, then passed after `cancelled` was allowed.

### Claim cards for absorbed theses (2026-11-02)

- [Advisory-only] Record visible kit limits as claim cards in `ci/claim_cards.json`, with shape and promotion rules in `usage/AGENT_EVALUATION.md`. A normative claim or a new required CI check needs an integrated canary under `ci/gate_tests/`. The checker does not read unregistered `constitution/` prose.
- [Verification] Add `ci/validate_claim_cards.py` and standing-limit regressions to the existing `ci/gate_tests` job. Extend `doc-hygiene` path filters so registry-only edits run that job. No new workflow or mandatory adopter gate.
- [Governance] ADR-0014 records the registry, its trust limits, and the constitution blind spot. Constitutional rules and import bundle definitions are unchanged; minimal remains documentation-only.
- [Fix] DOC DELTA and governance-waiver advisories warn when the section is empty, placeholder, or absent, including when the same words appear elsewhere. A populated section suppresses the warning. Both checks still exit 0. Starter §6 and §7 carry the same section predicate.
- [Verification] `ci/gate_tests/test_advisory_evidence.py` runs the kit and starter blocks. Claim cards `doc-delta-section-value` and `waiver-section-values` are integrated canaries and are not normative.
- [Fix] An integrated claim card requires a `def test_` line that unittest discovery collects. A comment, string, or uncollected function containing the test name no longer passes. The checker still does not run the test.
- [Verification] Doc hygiene root-file, Provenance header, and new-doc link steps now run against planted failures in `ci/gate_tests`. D5 reads `BASE_SHA` and `HEAD_SHA` so the same block can run outside Actions.
- [Verification] The bundled cross-ref step rejects a usage link outside the path list and fails closed when yq is missing. The fixture supplies that path list; lychee still has no planted failure.
- [Verification] The manifest path step rejects a missing file or directory from that path list and fails closed when yq fails. The fixture supplies the list.
- [Verification] The yq release named in `doc-hygiene` is run against this repo's manifest paths and usage links, and against a planted missing tree and outside link.
- [Verification] The lychee release named in `doc-hygiene` rejects a missing local hub file and accepts this repo's hub files offline. Offline mode does not prove remote URLs.
- [Verification] The Cursor stop script asks once for an UNVERIFIED report when verify.sh is missing or exits with a code other than 2, and allows the stop on a later loop_count or on stop_hook_active. Exit 2 asks for a follow-up. The test calls the script directly and does not show native host dispatch.
- [Verification] The ADR presence check accepts a numbered record whose body is only a title and TODO. Its PASS line still says the content needs review.
- [Verification] The test-evidence helper assesses hand-written JSON as VERIFIED when the schema matches. It does not open the named evidence paths and does not show that a runner wrote the report.
- [Verification] AEP schema version 1 accepts a READY plan with no method field. An empty discovery list still fails. PASS does not show that a method was compared.
- [Verification] The finding comparator accepts two hand-written reports with the same identity and does not modify them. A new identity fails. The pass does not show that a scanner ran.
- [Verification] The claim-card checker still passes when a constitution file contains a thesis that no card names. It does not copy that sentence into the registry.
- [Verification] A passing doc-hygiene root-file step leaves an open-finding note unchanged. The workflow does not mention the fix plan. Exit 0 is not release readiness.
- [Verification] The recorded 2026-11-01 stop session has an empty invocation log and no stop-invocations.jsonl. B5–B8 have no trial-result record. The provable-enforcement fragment is not referenced by doc hygiene, ADR, AEP, or constitution. None of these checks re-runs the host, a matched trial, or the fragment.
- [Fix] An integrated claim card now requires the collected test method to contain an assertion. A method whose body is only `pass` no longer qualifies. The checker still does not run the test.
- [Fix] An assertion made only of literals, such as `self.assertTrue(True)`, no longer qualifies as that canary. A name assigned from a literal in the same straight-line block counts as a literal too. The checker still does not run the test. A value produced by a call can still be constant at runtime.
- [Verification] Kit `doc-hygiene` fails a pull request that changes `constitution/` unless `ci/claim_cards.json` is added or modified and still present. A paired edit passes. A typo needs the same touch and does not prove a meaningful card. Adopters do not run this step. ADR-0014 records this as the self-test closure criterion and lists the accepted limits.

### External tooling investigation and isolated pilot (2026-11-01)

- [Advisory-only] Preserve the comparative review of development-agent governance/workflow tools, primary sources, evidence limits and reevaluation triggers in the existing external-project record.
- [Experimental] Add a reproducible Spec Kit v1.2.5 + spec-gates v0.5.0 pilot, captured positive/negative results and a native-agent handoff. Preserve this kit's policy and test-evidence validator; production adoption remains deferred.
- [Experimental] PR [#42](https://github.com/rhemzal/AI_governance/pull/42): optional in-repo adapter (`governance/experimental/spec_gates/`), Cursor `stop` wiring, projected spec-gates runtime, and advisory `spec-gates-kit-advisory` workflow. Native Cursor stop dispatch and required-check promotion remain open.
- [Experimental] The Cursor stop script now emits `followup_message` and exits 0. Cursor 3.27.22 drops the reason on stop exit 2. Promotion stays deferred: native dispatch was not observed, and the advisory workflow is not a required check. See the pilot follow-up and PR [#45](https://github.com/rhemzal/AI_governance/pull/45).
- [Import content] The opt-in experiment and evidence are included through the existing `research/` directory selection in research/full bundles. Minimal/standard selections, manifest definitions, canonical rules and mandatory CI gates are unchanged; importing research does not run the experiment or activate hooks.

### Test automation and runner evidence (2026-09-30)

- [Advisory-only] Extend existing testing, evidence, adoption and evaluation guides with runner conformance controls, failure-to-regression loops and scoped upstream-first pilots.
- [Feature] Add optional `ci/validate_test_evidence.py`: assess normalized observations against independently supplied run/state/check expectations; reject empty required coverage, reported failures and incomplete required cleanup.
- [Verification] Add positive and negative regression controls to the existing `ci/gate_tests` job and include the helper in its existing workflow path filters. No new workflow or mandatory adopter gate.
- [Governance] ADR-0013 records trust limits, native-runner ownership and adoption after upstream acceptance. Constitutional rules and import bundle definitions are unchanged; minimal remains documentation-only.

### Evidence-based methods and existing-project adoption (2026-09-28)

- [Governance-impacting] ADR-0012 / AI_RULES §6.5: non-trivial work records baseline/gap, observable acceptance, smallest method and uncertainty in existing AEP/task evidence. Align daily and agent projections; preserve the routine-work exception and authority boundaries.
- [Advisory-only] Add a primary-source evidence review, strengthen verification/oracle/maintenance reasoning, and add a concrete pinned-upgrade and one-slice pilot path with local promotion/retirement criteria.
- [Import bundle change] Minimal adds the method selector and rollout guide (14 files, still documentation-only). Standard/full include the optional finding-set comparator and its tests through `ci/`; no new mandatory adopter CI gate or automatic downstream activation.
- [Feature] Optional read-only `ci/ratchet_findings.py` rejects new finding identities and invalid/incomparable scans; it reports remaining debt, does not run scanners or update baselines, and needs a trusted host integration.

### Agent-first engineering methods (2026-09-28)

- [Advisory-only] Add `usage/AI_ENGINEERING_METHODS.md` as the method-selection index for harness engineering, agent-legible repositories, executable specifications, verification-first work, runtime interaction, reusable skills/hooks, bounded delegation, isolated parallel execution, evaluation, and failure-to-harness improvement.
- [Advisory-only] Add focused guides for agent harness engineering, machine-queryable runtime interaction (MCP is one implementation), spec-driven AI development, parallel execution, and agent engineering regression tasks.
- [Advisory-only] Keep the methods technology-neutral and proportional: no new mandatory orchestration framework, MCP requirement, subagent workflow, hook, or CI gate.

### Gate input correctness (2026-09-27)

- [Fix] September A-03: Python boundary examples inspect static import syntax, including direct/from/relative/indented forms. Python/Go recipes fail on missing/empty source roots and scanner errors; document the Go text scan and Python name-policy limits.
- [Governance-impacting] ADR-0011: the ADR check accepts only added/modified numbered regular records at the tested revision. Deleted/template/symlink/type-change/detected-rename records do not satisfy it. Starter §4 fetches full history and matches the kit's governance prefixes (A-04/A-05).
- [Fix] AEP detection recognizes tilde, longer and up-to-three-space-indented fences, rejects incomplete/multiple declarations, and ignores examples inside ordinary code fences. Schema version and absent-plan advisory behavior stay unchanged (A-07).
- [Import bundle change] Standard/full gain scoped inline-check regression fixtures through existing `ci/`; the kit runs them in doc hygiene. Minimal stays documentation-only. Copy corrected recipes/workflows and the AEP validator from the same pinned revision; no downstream workflow is activated automatically.

### Safe bundle import (2026-09-27)

- [Breaking rule change] ADR-0010: copy imports default to a fresh `vendor/AI_governance/` snapshot. Existing destinations are refused; host agent instructions, workflows and metadata are preserved and integrated by a reviewed merge. Existing root-layout imports require a deliberate migration, not an overwrite.
- [Import bundle change] Minimal adds the manifest catalog, required architecture framework and terminology glossary. Standard/full inherit them and include the scoped importer/checker and separate regression suite through `ci/`. Bundle names and manifest schema remain unchanged.
- [Governance-impacting] Distinguish kit-document paths from project source/commands/decisions. Optional trigger maps, interface proposals and architecture add-on references no longer masquerade as missing baseline prerequisites.
- [Fix] Verify the declared bundle selection against a pinned source, including tracked file inventory, exclusions, content and executable bits. Retain kit-wide manifest checks only in the upstream workflow; add import safety/closure regressions. September A-01/A-02 repair evidence is tracked in the audit report.

### Agent execution update (2026-09-27)

- [Governance-impacting] ADR-0008: bounded task mandates, action-specific authority, repair budgets, revision/environment-bound evidence, resume/handoff, and explicit task outcomes. Align constitution, projections, overlays, and debugging guidance; remove blanket reapproval for already authorized preparation.
- [Breaking rule change] AEP applicability now follows HIGH risk, dependent non-trivial steps, handoff, or concurrency; routine reversible multi-file edits may use concise scope/verification statements. Review downstream overlays before adopting.
- [Breaking rule change] ADR-0009: replace whole-PR grep with versioned structured AEP declarations and a standard-library validator. Upgrade workflow, validator, and PR template together; legacy marker-only declarations require migration. Structural validation is not proof of authorization or completion.
- [Import bundle change] Existing `ci/` inclusion adds `ci/validate_aep.py` and `ci/tests/` to standard/full; bundle names and manifest schema remain unchanged. Minimal documentation imports remain script-free unless the AEP gate is explicitly adopted.
- [Advisory-only] Replace audit finding/severity quotas with coverage and evidence; add agent tool-boundary guidance, a compact handoff template, and matched-task evaluation scenarios/metrics. Reopen release-audit readiness for the new governance changes.
- [Governance-impacting] Distinguish AI-authored source prose from mechanically generated artifacts; permit development observability when it enables concrete verification.
- [Fix] Restore the existing documentation gate: use syntax supported by pinned `yq` v4.44.3, resolve Markdown links relative to their source, and match bundle directory prefixes correctly. Detect backticked root-file dependencies without interpreting illustrative filenames as imports. Pin lychee v0.24.2 and replace its removed email-exclusion flag.

### Added

- [Advisory-only] `usage/AI_PRODUCTIVITY_CALIBRATION.md` — phased planning (cold start → collect → calibrate → ranges); human vs AI methodology.
- [Advisory-only] `usage/templates/AI_PRODUCTIVITY_LEDGER.template.md` — local gitignored ledger template.
- [Advisory-only] `governance/AI_CALIBRATION_SUMMARY.template.md` — optional team aggregate summary.
- [Advisory-only] `usage/QUICKGUIDE.md` Recipe I — Phase 0 scope-only planning + post-task ledger capture.

### Changed

- [Advisory-only] `usage/HOW_TO_USE_WITH_COPILOT.md` — Time Planning defers to calibration guide; Phase 0 no calendar ETA.
- [Advisory-only] `tooling/AI_TOOL_OPTIMIZATION.md`, `tooling/BENCHMARK_SCENARIOS.md` — linked to calibration; B1–B4 as Phase 1 starters.
- [Advisory-only] `usage/GOVERNANCE_SCORECARD.md` — optional AI productivity KPIs.
- [Advisory-only] `architecture/TERMINOLOGY_GLOSSARY.md` — cold start, task class, T_ai_active, human_source.
- [Advisory-only] `AGENTS.md`, `.github/copilot-instructions.md`, `governance/LOCAL_OVERLAY_TEMPLATE.md` — planning calibration projection.
- [Advisory-only] `usage/ADOPTION_BUNDLES.md` — standard bundle notes for calibration templates.
- [Import bundle change] `kit-manifest.yml` — `standard` adds `governance/AI_CALIBRATION_SUMMARY.template.md`.

## v0.3.0 — 2026-07-11

Full consistency audit (Waves 0–8). Terminology and gate-timing alignment; minimal bundle expansion; audit closure.

### Added

- [Governance-impacting] `adr/ADR_0007_Governance_Level_vs_CI_Maturity.md` — G0–G4 vs CM0–CM3 disambiguation.
- [Advisory-only] `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`, `usage/GOVERNANCE_WAIVERS.md`, `usage/BOUNDARY_GATE_RECIPES.md`, `adr/ADR_0006_Adopter_Enforcement_Contract.md` (shipped post-v0.2.0; recorded here).
- [Advisory-only] Kit CI: `doc-delta-advisory.yml`, `governance-waiver-advisory.yml`.
- [Advisory-only] `usage/AUDIT_PLAYBOOK.md` — Full audit waves (0–8) procedure.

### Changed

- [Import bundle change] `kit-manifest.yml` — `minimal` bundle adds `constitution/AI_ENFORCEMENT.md`, `ADAPTIVE_GOVERNANCE.md`, `usage/AEP_VALIDATION.md`.
- [Governance-impacting] `architecture/TERMINOLOGY_GLOSSARY.md` — Governance Level (G) and CI Maturity (CM) terms + orientation map.
- [Governance-impacting] `constitution/ADAPTIVE_GOVERNANCE.md` — Governance Level G0–G4 labels; GOVERNANCE FIT CHECK includes CM hint.
- [Advisory-only] `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`, `usage/CI_MINIMUM_ADOPTION.md`, `governance/LOCAL_OVERLAY_TEMPLATE.md` — CM0–CM3 (replaces bare L0–L3).
- [Advisory-only] `usage/ENFORCEMENT_MATRIX.md` — canonical gate × CM × G table; kit maintainer dogfood exceptions.
- [Governance-impacting] `ci/DOC_GATES.md`, `ci/TEST_GATES.md`, `ci/ARCHITECTURE_GATES.md` — G and CM columns; link to matrix.
- [Advisory-only] `AGENTS.md`, `.github/copilot-instructions.md` — bundle-aware import scope; COMPLIANCE Overlay line; CM/G terminology.
- [Advisory-only] `usage/AEP_VALIDATION.md` — doc-only / no-test-suite verification escape.
- [Advisory-only] `usage/AUDIT_REPORT.md`, `usage/FIX_PLAN.md` — wave audit closed (PASS).
- [Advisory-only] `README.md`, `usage/HOW_TO_IMPORT.md`, `usage/ADOPTION_BUNDLES.md` — CM labels in adoption guidance.
- [Advisory-only] Prior v0.2.0 post-release items: enforcement matrix phase 2, `aep-advisory` field grep, D5 error in `doc-hygiene`, PR waiver block, `RELEASE_READINESS.md`.

## v0.2.0 — 2026-07-05

### Added

- [Import bundle change] `kit-manifest.yml` — machine-readable adoption bundles (`minimal`, `standard`, `architecture`, `research`, `full`); manifest schema `0.2`.
- [Import bundle change] `kit-manifest.yml` — `standard` bundle includes `kit-manifest.yml`, `VERSIONING.md`, `DEVELOPMENT.md`, `CHANGELOG.md`.
- [Advisory-only] `.github/workflows/doc-hygiene.yml` — kit-repo CM0 doc hygiene (shell + `yq` + `lychee`; no Python scripts).
- [Advisory-only] `usage/ADOPTION_BUNDLES.md` — human guide for bundle selection.
- [Advisory-only] `usage/PROACTIVE_TRIGGER_MAP.md` — path-prefix trigger map for multi-agent checks.
- [Advisory-only] `VERSIONING.md` — kit versioning and upgrade policy for importers; current release mapping table.
- [Advisory-only] `architecture/README.md` — architecture directory entry point.
- [Advisory-only] `architecture/ARCHITECTURE_DECISION_PROMPT.md` — copy-paste precheck prompt with fixed output format.
- [Advisory-only] `architecture/rag/RAG_NOTE_TEMPLATE.md` — extracted template for new advisory RAG notes.
- [Advisory-only] `architecture/rag/OBSERVABILITY_AS_ARCHITECTURE.md` — cross-cutting observability guidance.
- [Advisory-only] `architecture/rag/FEATURE_FLAGS_PROGRESSIVE_DELIVERY.md` — cross-cutting feature-flag guidance.
- [Advisory-only] `DEVELOPMENT.md` — numbered Doc Hygiene Checklist with PR output template.
- [Advisory-only] `usage/QUICKGUIDE.md` — Recipe F (architecture decision precheck); Recipe G (governance audit).
- [Advisory-only] Full governance audit (`usage/AUDIT_REPORT.md`, `usage/FIX_PLAN.md`) — 2026-07-05.

### Changed

- [Advisory-only] Agent projections (`AGENTS.md`, `.github/copilot-instructions.md`) — Quick rules summary block; architecture entry point; provenance banners; non-interactive/timeout quick rule.
- [Advisory-only] Import docs (`usage/HOW_TO_IMPORT.md`, `usage/QUICKGUIDE.md`, `README.md`) — reference manifest and adoption bundles; Option A resolves paths from manifest only.
- [Advisory-only] `usage/ADOPTION_BUNDLES.md` — documents root meta docs in `standard`.
- [Advisory-only] `usage/CI_STARTER_WORKFLOWS.md` — expanded starters (doc hygiene, boundary, AEP advisory); points to kit workflow.
- [Advisory-only] Provenance banners added to remaining architecture and research import-target documents.
- [Advisory-only] `architecture/SOLUTION_CLASS_TAXONOMY.md` — Feature Flags and Observability upgraded to Advisory; extension checklist clarifies cross-cutting matrix entries.
- [Advisory-only] `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`, `architecture/ARCHITECTURE_STYLE_MATRIX.md`, `architecture/DATA_MODELING_GUIDE.md` — links and `DATA MODEL DECISION RECORD` mini-template.
- [Import bundle change] `kit-manifest.yml` — `architecture` bundle includes `README.md` and `ARCHITECTURE_DECISION_PROMPT.md`.
- [Advisory-only] `README.md` — version note; link to audit playbook.
- [Advisory-only] `usage/AUDIT_PLAYBOOK.md` — `architecture/README.md` in mandatory inputs.
- [Advisory-only] `usage/PROACTIVE_TRIGGER_MAP.md` — automation hooks for CI starters and kit workflow.
- [Advisory-only] `governance/LOCAL_OVERLAY_TEMPLATE.md` — standard provenance banner.

### Removed

- Docs: remove OS-specific doc-audit script; keep CI guidance tool-agnostic.
- [Advisory-only] Removed the Python doctor script before release to preserve the kit's documentation-first, tool-agnostic positioning.

## v1.0.0 — 2025-12-31

- Public-ready baseline: clear licensing split for docs vs code.
- Community hygiene: contributing, security policy, code of conduct, PR/issue templates.
- Import traceability: provenance banners added to import-target documents.
- CI: CI gate principles provided; implementation is environment-specific.
