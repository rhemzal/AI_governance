# Audit Report — AI_governance kit

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Current audit — 2026-09-27

**Scope:** quarterly audit, Steps 1–5 and Waves 0–7 of `usage/AUDIT_PLAYBOOK.md`; release closure is deferred.

**Pinned baseline:** [768e2028eaabf943cb6b68e077d891db16f90332](https://github.com/rhemzal/AI_governance/commit/768e2028eaabf943cb6b68e077d891db16f90332), merged PR #34. Source locations and baseline probe results below refer to this revision, not the later audit-document commit.

**Outcome:** review complete; **not audit-clean**. **17 open findings: 1 High, 13 Medium, 3 Low.** The July report is preserved below as history; its PASS conclusion does not validate this revision.

The main concerns are unsafe copy-import instructions, checks that can report success without checking the claimed condition, and contradictions between canonical rules and their projections. PR #34 improved bounded execution and declaration validation, but its new AEP parser has a reproducible detection gap (A-07). Recent changes are included in the audit.

Severity follows demonstrated impact: **High** can replace an adopter's existing project instructions or records; **Medium** can invalidate governance evidence, break adoption, or lead to conflicting engineering decisions; **Low** is localized stale guidance or navigation/process wording. Counts are outcomes, not targets. IDs A-01–A-17 below belong to the **2026-09-27** audit; matching historical IDs remain separate.

### Finding index

| ID | Severity | Finding |
| --- | --- | --- |
| A-01 | High | Copy import can overwrite adopter instructions and project records |
| A-02 | Medium | Baseline bundles omit required context; upstream manifest check is not adopter-aware |
| A-03 | Medium | Boundary recipes pass on missing directories and common forbidden Python imports |
| A-04 | Medium | Deleting an ADR satisfies the added/updated ADR gate |
| A-05 | Medium | ADR starter diffs a base revision absent from its shallow checkout |
| A-06 | Medium | Empty waiver and DOC DELTA templates count as present evidence |
| A-07 | Medium | Alternate Markdown fences bypass declared AEP validation |
| A-08 | Medium | Required-check language does not match repository enforcement or trigger coverage |
| A-09 | Medium | Canonical gate mapping omits gates and conflicts with timing and authority |
| A-10 | Medium | Proportional workflow conflicts with universal reporting/adoption requirements |
| A-11 | Medium | Quality-attribute example reverses the intended dependency prohibition |
| A-12 | Medium | Style matrix unnecessarily requires exactly-once semantics for all streaming |
| A-13 | Medium | Release mapping names an unavailable tag |
| A-14 | Low | VS Code setup recommends the deprecated separate Copilot extension |
| A-15 | Low | Two release-readiness ADR links are broken and outside the link-check scope |
| A-16 | Medium | Interface gate forbids interactive defaults even when automation mode exists |
| A-17 | Low | Audit Step 3 still specifies a finding quota |

### Coverage and limitations

| Wave | Examined material and evidence | Review result / closure |
| --- | --- | --- |
| 0 | README, hub indexes, manifest, version/release metadata; 115 tracked Markdown files inventoried | Topics located; stale release mapping and two broken links |
| 1 | Constitution, adaptive governance, glossary, adoption contract, CI maturity guide | Scales exist; unqualified interface levels and conflicting applicability remain |
| 2 | All four `ci/*_GATES.md` documents, enforcement matrix, adoption contract | Missing A4/A5/I5 and conflicting interface/ADR timing |
| 3 | Recursive manifest resolution; minimal (9 files) and standard (60 files) materialized in fixtures; import guide and manifest check | Copy collisions and missing prerequisites reproduced |
| 4 | AGENTS, Copilot projection, daily/full enforcement, overlay precedence/template | Risk/authority and repair-budget sections align; reporting/applicability contradictions remain |
| 5 | All five workflows, validator/tests, PR template, waiver guide, starters and boundary recipes | Negative probes expose gaps despite successful main CI |
| 6 | Architecture framework/style matrix/taxonomy/index; three RAG notes: `QUALITY_ATTRIBUTES.md`, `STREAMING_REACTIVE.md`, `LAYERED_RATIONALE_AND_FAILURE_MODES.md` | Dependency-direction and streaming-selection contradictions; remaining RAG corpus not substantively audited |
| 7 | Import collision, missing boundary path, forbidden imports, ADR deletion/shallow fetch, empty evidence, alternate AEP fences | More than three scenarios exercised; **closure criterion unmet** because A-01 remains High |
| 8 | Release-readiness status reviewed only | **Deferred**; no release approval, tag, or manifest promotion |

Targeted review also covered debugging/test-execution guidance and research/tool setup references. This was not a line-by-line validation of every catalog, an execution pilot with real coding agents, a full dependency/security assessment, or compliance certification. No downstream repository was modified. Mutation probes used disposable fixtures. No productivity improvement is claimed.

**Scavenger results:** all five topics were found: high-risk changes in `AGENTS.md` and `constitution/AI_ENFORCEMENT.md`; ADR contents in `adr/ADR_TEMPLATE.md`; hybrid selection in `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`; schema/versioning guidance in `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md` and `VERSIONING.md`; non-interactive execution/timeouts in `constitution/AI_RULES.md` §6.2. This records findability, not a measured sub-60-second result. Finding a document does not establish that it is included in an adopter bundle (A-02).

### Verification record

Environment: Linux, Python 3.12.14, Bash, Git, yq 4.44.3, lychee 0.24.2. Published recipe/workflow shell bodies were executed unchanged except for fixture base/head SHAs and the local yq executable path. The temporary audit harness used PyYAML to read workflow blocks; this is not a new kit dependency.

| Check at pinned baseline | Observed result |
| --- | --- |
| `timeout 60s python3 -m unittest discover -s ci/tests -v` | 12 existing validator tests pass; A-07 is outside their coverage |
| Main doc-hygiene [run 36305844156](https://github.com/rhemzal/AI_governance/actions/runs/36305844156) | Success; does not establish absence of the findings |
| Offline lychee scan of all 115 tracked Markdown files | 255 occurrences: 136 successful, 117 external occurrences excluded, 2 errors (A-15); 107 unique targets |
| Recursive manifest expansion, honoring exclusions | Minimal: 9 files; standard: 60; missing prerequisites listed in A-02 |
| Standard copy over five existing product documents | All five sentinel contents replaced (A-01) |
| Kit manifest-existence step inside standard-only import | Exit 1: `Missing path (architecture): architecture/README.md` |
| Python boundary recipe, directory absent | Exit 0, no diagnostic |
| Same recipe with `from infra import database` or `import infra` | Exit 0 for both forbidden imports |
| Control: `from infra.database import connect` | Exit 1 with boundary violation diagnostic |
| Governance edit without changed ADR | Exit 1 (control) |
| Same edit plus deletion of existing numbered ADR | Exit 0 (A-04) |
| ADR starter in depth-1 fixture clone | Exit 128: `fatal: bad object` for base SHA |
| Invalid READY AEP with canonical fence | Exit 1, required fields missing |
| Identical AEP with three-space indentation, tilde fence, or four backticks | Exit 0 and `WARN: no AEP declaration; review applicability` in all three cases |
| Empty waiver template with placeholder expiration | Exit 0, **zero warnings** |
| Code change with only an empty DOC DELTA heading | Exit 0, `DOC DELTA present.` |

The offline scan excludes network links; it is not an external-link health claim. Public release/branch metadata and selected external technical claims were checked separately on 2026-09-27. Unconfigured test and boundary starter placeholders also returned 0 without checking anything. Their adaptation is explicitly required by the wiring checklist, so that expected scaffolding behavior is a limitation, not an additional finding. Activation should still include a negative control proving that a real check runs.

### Findings

#### A-01 — Copy import can overwrite project-owned files

- **ID**: A-01
- **Severity**: High
- **Category**: enforceability
- **Evidence**: `usage/HOW_TO_IMPORT.md:119` says to “copy every listed path”; `kit-manifest.yml:29–55` includes `AGENTS.md`, `.github/copilot-instructions.md`, `CHANGELOG.md`, `DEVELOPMENT.md`, and `VERSIONING.md`. Literal standard-bundle copying over a fixture containing all five replaced every sentinel. The PR-template step mentions merging, but no equivalent collision policy protects these files.
- **Impact**: Adoption can replace agent constraints, test commands, release policy, and changelog with kit content. Git can recover tracked files, but the instructions do not require review before replacement.
- **Fix proposal**: Require a collision inventory and explicit merge for project-owned files in `usage/HOW_TO_IMPORT.md` and `usage/ADOPTION_BUNDLES.md`. Give kit metadata a distinct destination or retained upstream reference; reconcile manifest/import semantics. Never prescribe unconditional replacement of host instructions.
- **Verification**: Import into empty and existing-project fixtures. Host sentinel contents survive, collisions are surfaced before writes, and imported governance references resolve.

#### A-02 — Bundle closure and adopter validation disagree

- **ID**: A-02
- **Severity**: Medium
- **Category**: contradiction
- **Evidence**: `constitution/AI_RULES.md:10` requires architecture selection “using `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`”, absent from minimal and standard. The glossary requirement (§6.3) has the same gap. Daily enforcement says “consult `usage/PROACTIVE_TRIGGER_MAP.md`” (:15), absent from minimal. Standard includes `ci/INTERFACE_GATES.md` but omits its primary interface reference. The kit manifest step loops over “minimal standard architecture research full” (`.github/workflows/doc-hygiene.yml:61`) and fails inside a valid standard-only import on an optional architecture path.
- **Impact**: Agents must choose between a normative dependency and the projection's instruction to skip missing context. Kit-wide checks cannot be transplanted as adopter checks unchanged. AGENTS also labels optional architecture context “standard+”.
- **Fix proposal**: Reconcile required context with bundle contents or explicit applicability. Distinguish upstream manifest integrity from checks of the declared imported bundle in starter/import guidance. Mark separately fetched PR templates/workflows as upstream inputs.
- **Verification**: Materialize each supported baseline/optional combination. Applicable references resolve, valid partial imports pass, and missing required selected-bundle files fail.

#### A-03 — Boundary recipes fail open

- **ID**: A-03
- **Severity**: Medium
- **Category**: enforceability
- **Evidence**: `usage/BOUNDARY_GATE_RECIPES.md:38` uses `if grep ... 2>/dev/null` and requires a dot after the forbidden package. Missing `src/myapp/domain/`, `from infra import database`, and `import infra` all return 0; the dotted-import control returns 1. Starter §3a repeats the construction; the Go recipe also suppresses errors inside the conditional.
- **Impact**: Renaming the checked directory or using ordinary import syntax can leave a green boundary job that checks nothing or misses the forbidden dependency. Shell fail-fast does not make a failing conditional predicate fatal.
- **Fix proposal**: Validate configured paths, distinguish scanner errors from no matches, and use import-aware checks or explicitly bounded patterns with stated exclusions. Synchronize recipe and starter.
- **Verification**: Missing/unreadable paths and direct/from/indented/relative forbidden imports fail; allowed imports pass. Retain a real violation as a negative control.

#### A-04 — ADR deletion satisfies the gate

- **ID**: A-04
- **Severity**: Medium
- **Category**: enforceability
- **Evidence**: `.github/workflows/adr-required.yml:32–35` uses `git diff --name-only` and accepts any matching numbered ADR path although its diagnostic says “added or updated”. A governance edit fails alone but passes when an existing ADR is deleted in the same diff.
- **Impact**: Removing decision evidence can satisfy the automated presence check. This structural bypass is separate from semantic review.
- **Fix proposal**: Check appropriate added/modified statuses and existence of the eligible ADR at head; exclude templates, deletions, and rename-away records. Apply the same rule in starter §4.
- **Verification**: No-ADR, deleted-ADR and template-only cases fail; qualifying added/updated ADR passes. Test rename behavior too.

#### A-05 — ADR starter lacks required history

- **ID**: A-05
- **Severity**: Medium
- **Category**: enforceability
- **Evidence**: `usage/CI_STARTER_WORKFLOWS.md:163` uses `actions/checkout@v4` without a fetch-depth override, then diffs the base SHA (:167–169). The depth-1 fixture returns “fatal: bad object”. Checkout defaults to one fetched commit [S2]; the working kit workflow already specifies `fetch-depth: 0`.
- **Impact**: The copied starter can fail before evaluating governance, encouraging adopters to disable it.
- **Fix proposal**: Copy reference history setup or fetch exact comparison revisions. Align starter/reference path and status handling without unintentionally broadening required gates.
- **Verification**: Execute the starter in a PR-style shallow checkout with an older base and positive/no-ADR/deletion cases. No comparison fails due to an unavailable SHA.

#### A-06 — Empty evidence suppresses advisories

- **ID**: A-06
- **Severity**: Medium
- **Category**: enforceability
- **Evidence**: `.github/workflows/governance-waiver-advisory.yml:20–26` greps the whole body for “Gate ID”, “Owner”, “Expiration”, and “Compensating control”. The empty template with `Expiration: YYYY-MM-DD` produces zero warnings. `.github/workflows/doc-delta-advisory.yml:36–38` prints “DOC DELTA present.” for only an empty heading in a code-changing fixture.
- **Impact**: Default PR scaffolding silences reminders about missing ownership/expiry and behavior documentation. Advisory exit 0 is intentional; failure to warn is the defect.
- **Fix proposal**: Check non-empty, non-placeholder values inside the relevant section, an interpretable waiver expiry, and substantive DOC DELTA content. Preserve advisory severity unless explicitly promoted.
- **Verification**: Empty/copied templates and matching words in unrelated prose emit warnings; populated sections do not. Intended label/doc-only exemptions remain.

#### A-07 — Markdown fence variants bypass new AEP validation

- **ID**: A-07
- **Severity**: Medium
- **Category**: enforceability
- **Evidence**: `ci/validate_aep.py:114–121` recognizes exactly three opening backticks at column zero. `usage/AEP_VALIDATION.md:83` says “Declared plans are checked even for one-file PRs.” The payload `{"schema_version":1,"status":"READY"}` fails with a canonical fence but exits 0 as missing with three-space indentation, `~~~aep`, or four backticks. All are valid GitHub Markdown fence forms [S3].
- **Impact**: A visually declared invalid plan becomes an advisory absence through formatting. This gap was introduced in PR #34 and is not covered by its 12 tests. It is a detection failure, not a claim that AEP proves authorization.
- **Fix proposal**: Recognize supported Markdown variants, or explicitly detect and reject unsupported declaration forms with migration guidance. Add variant, mixed/multiple-block, and unfinished-fence regressions.
- **Verification**: Identical invalid payloads fail across all four forms. Valid supported declarations pass; genuinely absent plans retain advisory behavior.

#### A-08 — CI execution and merge enforcement are conflated

- **ID**: A-08
- **Severity**: Medium
- **Category**: contradiction
- **Evidence**: `usage/ENFORCEMENT_MATRIX.md:53,58` calls kit doc hygiene “Required (always on)” and ADR checks “Required”. On 2026-09-27 main reported `protected: false`, required-status enforcement `off`, no required contexts, and no repository rulesets. Both workflows also have PR path filters: doc hygiene omits Python-only changes; ADR runs only for selected governance prefixes.
- **Impact**: A maintainer policy is not an automated merge barrier. Making path-filtered workflows universally required can instead leave out-of-scope PRs waiting for a check that never starts [S1]. This is not evidence of an unauthorized merge.
- **Fix proposal**: Label policy, check execution, and branch enforcement separately. Keep branch policy a maintainer choice consistent with adaptive governance. If required checks are chosen, emit a status for every applicable PR and conditionally perform checks inside the job.
- **Verification**: Documentation matches dated branch/ruleset state. Governance, usage-only, and Python-only PRs receive the intended status without waiting for a filtered required workflow.

#### A-09 — Gate timing, completeness, and authority drift

- **ID**: A-09
- **Severity**: Medium
- **Category**: contradiction
- **Evidence**: The matrix calls itself the “single source of truth” for timing (`usage/ENFORCEMENT_MATRIX.md:5`), but omits A4/A5/I5 and collapses I1–I4 into G2/G3. Interface definitions use differing bare levels: I1/I3 1/2, I2 2/3, I4/I5 3/4. A3 is mandatory at G4 (`ci/ARCHITECTURE_GATES.md:48`) but blocks at G3+ (:53). The matrix points interface gates to a proposal, while `CONTRIBUTING.md:10` calls `interface/` normative and its proposal document (:5) explicitly says it is not.
- **Impact**: The same change appears optional, blocking, or proposed depending on the entry document. Missing gates cannot be traced through the canonical adoption table.
- **Fix proposal**: Decide A3 timing explicitly; enumerate every gate with qualified G/CM values. Point normative interface enforcement to `ci/INTERFACE_GATES.md` and retain proposal-only status for `interface/`.
- **Verification**: Compare the complete gate-ID set and timing across definitions, matrix, and contract. Every ID has one applicable meaning; proposal promotion remains a separate decision.

#### A-10 — Universal requirements undermine proportional execution

- **ID**: A-10
- **Severity**: Medium
- **Category**: contradiction
- **Evidence**: `constitution/AI_ENFORCEMENT.md:161` requires every change response to end with the full compliance report; daily enforcement (:28) and AGENTS prescribe a mini-report for routine work. The overlay's exception is under “Additions”, although precedence guidance requires explicit “Overrides” for conflicts. `constitution/AI_RULES.md:10–11` universally requires architecture selection/ADR, while adaptive governance discourages mandatory ADRs for small reversible decisions. `usage/HOW_TO_IMPORT.md:107` requires immediate deterministic tests; the contract defers them to CM1 when tests exist.
- **Impact**: Highest-priority text can impose full reports, ADRs, and tests on routine/CM0 work despite the proportional workflow. Optional overlays do not repair the baseline contract.
- **Fix proposal**: Define report/architecture-decision applicability once in the constitution, including lightweight existing-project adoption; update projections. Align the post-import checklist with maturity and distinguish an initial architecture decision from every implementation change.
- **Verification**: G0 scratch, a reversible G1 edit, CM0 import without tests, and a high-risk boundary change each have one consistent minimum output and verification requirement.

#### A-11 — Worked example reverses the boundary check

- **ID**: A-11
- **Severity**: Medium
- **Category**: theory
- **Evidence**: `architecture/rag/QUALITY_ATTRIBUTES.md:62` recommends “no adapter imports from core”. `constitution/AI_RULES.md:37–38` requires inward dependencies and prohibits core dependencies on integration details.
- **Impact**: Read literally, the example bans adapters importing core while omitting the prohibition on core importing adapters. It can produce the opposite architectural test.
- **Fix proposal**: State **no core imports from adapters/infrastructure** and reference the canonical rule. Make the importing and imported module unambiguous.
- **Verification**: Adapter-to-core import is allowed; core-to-adapter is rejected. Wording agrees with Gate A1 and the constitution.

#### A-12 — Streaming has an unjustified exactly-once prerequisite

- **ID**: A-12
- **Severity**: Medium
- **Category**: theory
- **Evidence**: `architecture/ARCHITECTURE_STYLE_MATRIX.md:52` says to avoid streaming “when exactly-once semantics cannot be guaranteed”. The RAG note (`architecture/rag/STREAMING_REACTIVE.md:33`) conditions this on exactly-once being required; :48 supports at-least-once plus idempotency. Flink documentation also distinguishes guarantees and idempotent upserts [S5].
- **Impact**: The summary excludes suitable designs whose criteria tolerate duplicates or use idempotency. A processing guarantee is not automatically an end-to-end guarantee.
- **Fix proposal**: Restore the requirement-dependent condition; assess source, processing, sink, replay, and idempotency together in architecture decision evidence.
- **Verification**: At-least-once/idempotent designs meeting their criteria remain eligible; designs needing unsupported end-to-end exactly-once are rejected or redesigned.

#### A-13 — Release metadata advertises a missing tag

- **ID**: A-13
- **Severity**: Medium
- **Category**: contradiction
- **Evidence**: `README.md:7` says “Latest release: `v0.3.0`”; `VERSIONING.md:28–29` maps that git tag. On 2026-09-27, `git ls-remote --tags origin` lists only `v0.2.0` and `v1.0.0` (plus the annotated-tag dereference), and the releases API returns no releases. The release checklist says v0.3.0 is pending. ADR-0008/0009 retain “Proposed — implemented on this review branch” after merge.
- **Impact**: Adopters cannot pin the advertised baseline. A changelog section, accepted decision, tag, and GitHub release are different states.
- **Fix proposal**: Describe v0.3.0 as an untagged planned cut until deliberately released; provide an actual available pin. Reconcile merged ADR statuses with the acceptance decision. Do not create/rewrite tags just to make stale documentation true.
- **Verification**: Advertised tags resolve to intended commits; README, version mapping, changelog, ADR status, and checklist agree. A GitHub release is not required if policy uses tags only.

#### A-14 — VS Code extension guidance is stale

- **ID**: A-14
- **Severity**: Low
- **Category**: findability
- **Evidence**: `usage/HOW_TO_USE_WITH_VSCODE.md:33–34` recommends separate GitHub Copilot completion and Copilot Chat extensions. VS Code's January 2026 notes deprecate the separate Copilot extension and move its functionality into Copilot Chat [S4].
- **Impact**: Adopters receive an obsolete installation model and may troubleshoot the wrong extension.
- **Fix proposal**: Update to the supported unified model with official setup references and a verification date; keep governance principles independent of product UI.
- **Verification**: Installation steps and extension identifiers match current official guidance.

#### A-15 — Release-readiness ADR links are broken

- **ID**: A-15
- **Severity**: Low
- **Category**: findability
- **Evidence**: `usage/RELEASE_READINESS.md:9–10` links to `adr/ADR_0005_Kit_CI_Dogfooding.md` and `adr/ADR_0006_Adopter_Enforcement_Contract.md` relative to `usage/`, resolving to nonexistent `usage/adr/`. The full offline scan reports both errors; the four-entry-document CI scan misses this page.
- **Impact**: Release reviewers cannot follow decision links; hub-only CI does not establish whole-repository local-link health.
- **Fix proposal**: Use `../adr/…` for both targets and add a cheap local-link pass over tracked Markdown, keeping network checks separately scoped.
- **Verification**: Full offline scan has zero local-link errors; narrower online checks state their file scope.

#### A-16 — Interface gate rejects a legitimate interactive default

- **ID**: A-16
- **Severity**: Medium
- **Category**: interface
- **Evidence**: `ci/INTERFACE_GATES.md:20` forbids blocking in “non-interactive mode” and requires an alternative flag/mode, but :23 also rejects waiting for input in “default mode”. Its purpose includes GUI/CLI/TUI interfaces.
- **Impact**: An interactive tool with a working automation mode meets the stated mitigation but fails the default-mode bullet.
- **Fix proposal**: Scope failure to automation/non-interactive invocation; define prompt-free handling of missing required input, timeouts, and meaningful exit codes.
- **Verification**: Interactive invocation may prompt; automation invocation completes or fails promptly without stdin. A tool lacking that mode fails.

#### A-17 — Residual audit finding quota

- **ID**: A-17
- **Severity**: Low
- **Category**: contradiction
- **Evidence**: `usage/AUDIT_PLAYBOOK.md:137` asks for “3–5 rules” that are unenforceable, while its opening section makes findings outcomes rather than quotas and permits zero findings.
- **Impact**: Step-by-step execution can still pressure a reviewer to manufacture findings after PR #34 removed the incentive elsewhere.
- **Fix proposal**: Request examined rules, evidence, detected gaps (possibly none), and suitable options. Retain the separate three-scenario coverage requirement.
- **Verification**: An evidenced zero-defect audit satisfies every instruction while exercising required scenarios and recording limitations.

### Minimal reproduction guide

Use a disposable checkout of the pinned baseline, never an adopter's working repository for mutation probes.

1. **Import:** recursively resolve manifest extends/composes, union tracked files, honor excludes, and materialize standard into a temporary directory. Repeat over sentinel copies of the five A-01 paths. Run the workflow's manifest-existence shell body inside the copy with yq 4.44.3.
2. **Boundary:** execute the Python Bash block from `usage/BOUNDARY_GATE_RECIPES.md` in an empty temporary directory, then with `src/myapp/domain/example.py` containing each import in the verification table. Record exits and diagnostics.
3. **ADR:** create two-commit fixtures with a constitution file and numbered ADR. Change only the constitution in one; also delete the ADR in the other. Execute the workflow run block with fixture base/head SHAs. For the starter-history case, clone through a `file://` URL with depth 1 and use the older base SHA.
4. **AEP:** pipe the A-07 two-field JSON through `python3 ci/validate_aep.py --changed-files 2` inside each fence variant, with `PR_BODY` unset. Compare with canonical fencing.
5. **Advisories:** set `PR_BODY` to the empty waiver template and execute its run block; then use only the DOC DELTA heading with a code-changing two-commit fixture. Count warnings as well as exits; exit 0 alone is correct for an advisory.
6. **Links:** run lychee 0.24.2 with `--offline --no-progress --include-mail=false` over an argument array from `git ls-files '*.md'`. Keep the full file scope distinct from the four-hub CI check.

### External evidence checked on 2026-09-27

- **S1:** [GitHub required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks): path-filtered workflows can leave required checks pending; conditional skipped jobs report success.
- **S2:** [actions/checkout](https://github.com/actions/checkout): fetch-depth default and comparison history.
- **S3:** [GitHub Flavored Markdown fenced code blocks](https://github.github.com/gfm/#fenced-code-blocks): tildes/backticks, longer fences, and up to three spaces of indentation.
- **S4:** [VS Code v1.109 — Copilot extension deprecated](https://code.visualstudio.com/updates/v1_109#_copilot-extension-deprecated): unified functionality in Copilot Chat.
- **S5:** [Apache Flink — Upsert Kafka consistency guarantees](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/table/upsert-kafka/#consistency-guarantees): delivery guarantees and idempotent upserts. Used for semantics, not to recommend a particular connector version.

Repository state was read from the GitHub main-branch, repository rulesets, and releases APIs plus `git ls-remote --tags origin`. Remote state is a dated observation and may change independently.

### Audit disposition

[FIX_PLAN.md](FIX_PLAN.md) orders focused repairs and regression criteria. This audit changes only the report, plan, and audit/matrix/navigation status in [RELEASE_READINESS.md](RELEASE_READINESS.md). Findings remain open until repaired and retested. No normative rule, CI implementation, branch setting, version tag, or downstream content changed.

---

## Historical audit — 2026-07-11

Preserved as recorded. Its closure and PASS claims describe the earlier audit, not the September baseline. Current findings above supersede its current-state conclusions.

<details>
<summary>July 2026 report (historical record)</summary>

Date: 2026-07-11 (full consistency audit — **closed**)  
Scope: `release` per `usage/AUDIT_PLAYBOOK.md` — Waves 0–8.  
ADR: `adr/ADR_0007_Governance_Level_vs_CI_Maturity.md`

## Wave status

| Wave | Focus | Status |
| --- | --- | --- |
| 0 | Baseline & scavenger | **Done** |
| 1 | Level taxonomy (G vs CM) | **Done** |
| 2 | Gate × maturity alignment | **Done** |
| 3 | Bundle & import graph | **Done** |
| 4 | Agent projections parity | **Done** |
| 5 | Enforceability & dogfooding | **Done** |
| 6 | Theory & architecture corpus | **Done** |
| 7 | Red-team retest | **Done** |
| 8 | Release closure (changelog cut) | **Done** (git tag pending maintainer) |

## Result summary

| Step | Status | Notes |
| --- | --- | --- |
| Scavenger test | **PASS** | Hub links, G/CM glossary, enforcement contract findable |
| Consistency scan | **PASS** | H-01–H-03 closed (ADR-0007, matrix, minimal bundle) |
| Enforceability review | **PASS** | Kit dogfood exceptions documented; AEP doc-only escape |
| Theory validation | **PASS** | See theory-bridge notes below (advisory gaps only) |
| Red-team drift | **PASS** | Scenarios retested; standing items documented |
| Doc hygiene CI | **PASS** | Kit repo |

**Release gate:** No open **High** findings. Manifest `1.0` promotion still requires stable bundle cycle + git tag per `usage/RELEASE_READINESS.md`.

---

## Closed findings (waves 1–5)

| ID | Severity | Resolution |
| --- | --- | --- |
| H-01 | High | G0–G4 and CM0–CM3 in glossary; ADAPTIVE_GOVERNANCE relabeled; ADR-0007 |
| H-02 | High | Canonical gate table in `ENFORCEMENT_MATRIX.md`; `ci/*.md` G + CM columns |
| H-03 | High | Minimal bundle extended; bundle-aware `AGENTS.md` / Copilot |
| M-01 | Medium | G×CM orientation map; CM0 cheap hygiene vs G2 anti-bloat explained |
| M-02 | Medium | Overlay line in agent COMPLIANCE footers |
| M-03 | Medium | AEP verification escape for doc-only repos |
| M-04 | Medium | Standing risk — overlay precedence documented in red-team table |
| M-05 | Medium | Kit vs adopter table in `ENFORCEMENT_MATRIX.md` |
| L-01 | Low | README duplicate heading removed |
| L-02 | Low | VERSIONING mapping documents v1.0.0 → v0.x lineage |
| L-03 | Low | Copilot points to `AGENTS.md` for full method triage |
| C-01 | Low | Accepted — DOC DELTA advisory in kit repo by design |

---

## Step 6 — Theory validation (Wave 6)

Spot-check of `architecture/SOLUTION_CLASS_TAXONOMY.md` vs `architecture/rag/`:

| Topic | Taxonomy | RAG coverage | Bridge gap |
| --- | --- | --- | --- |
| Feature flags | Advisory | `FEATURE_FLAGS_PROGRESSIVE_DELIVERY.md` | OK |
| Observability | Advisory | `OBSERVABILITY_AS_ARCHITECTURE.md` | OK |
| Offline-first | Mentioned | `CONSISTENCY_MODELS.md` partial | **Standing** — sync/conflict specifics out of scope (documented in taxonomy) |
| Schema evolution | Advisory | `SCHEMA_EVOLUTION_AND_VERSIONING.md` | OK |

No normative contradiction found. Optional follow-up: expand offline-first RAG note (low priority).

---

## Red-Team Drift Scenarios (Wave 7 retest)

| Scenario | Status |
| --- | --- |
| Standard import without CM declaration | **Mitigated** — overlay template + HOW_TO_IMPORT |
| Silent gate bypass | **Mitigated** — `GOVERNANCE_WAIVERS.md` + PR block |
| Phantom AEP | **Partially mitigated** — `aep-advisory` field grep |
| Boundary skip at CM2 | **Standing** — adopter must wire `BOUNDARY_GATE_RECIPES` |
| Level scale confusion (G2 vs CM2) | **Mitigated** — glossary + matrix + ADR-0007 |
| Minimal bundle phantom refs | **Mitigated** — bundle paths + bundle-aware agents |
| Overlay weakens constitution silently | **Standing** — requires explicit Overrides + review; no CI check |

---

## Related Documents

- `usage/AUDIT_PLAYBOOK.md`
- `usage/FIX_PLAN.md`
- `usage/RELEASE_READINESS.md`
- `adr/ADR_0007_Governance_Level_vs_CI_Maturity.md`

</details>
