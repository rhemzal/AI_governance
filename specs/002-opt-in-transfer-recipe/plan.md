# Implementation Plan: Opt-In Governed Work Transfer Recipe

**Branch**: `002-opt-in-transfer-recipe` | **Date**: 2026-11-03 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-opt-in-transfer-recipe/spec.md`

**Plan status**: Phase 0–1 design artifacts complete; **implementation closure** tracked in [tasks.md](./tasks.md). Refreshed by `/speckit-implement` on 2026-11-03 (**plan + tasks only** — no T001–T020 execution, commit, or push in that pass).

## Summary

Close a **pinned opt-in transfer recipe** so adopters install governed-work procedures (entry skill, vendored Superpowers pin, optional preset) without overwriting host instructions or local policy. The verified mechanism is **regular-file copy** in `usage/HOW_TO_IMPORT.md` § Opt-in work procedures, mirrored by `_copy_procedures()` in `ci/gate_tests/test_work_procedures.py`.

**Baseline at plan refresh (2026-11-03, this session):**

| Area | Status |
| --- | --- |
| Shell copy + upgrade/rollback blocks | Present in `usage/HOW_TO_IMPORT.md` § Opt-in work procedures (~L189–231); may include **uncommitted** edits in the working tree |
| Fixture tests SC-001, SC-003, SC-004 | `test_opt_in_copy_*`, `test_upgrade_then_rollback_*` — **7/7 OK** (`timeout 120s python3 -m unittest ci.gate_tests.test_work_procedures -v`, Ran 7 tests in ~0.14s) |
| Phase 0 `research.md` | All technical unknowns resolved |
| Phase 1 `data-model.md`, `contracts/opt-in-recipe.md`, `quickstart.md` | Present; contract matches `_copy_procedures` copy set |
| FR-005 activation, FR-010 bundle cross-ref, ownership table, minimum baseline, edited-file edge case, SC-005 checklist | **Not yet in normative docs** — no `Activation` / host-vs-kit table in HOW_TO_IMPORT; no Opt-in pointer in `ADOPTION_BUNDLES.md`; `checklists/recipe-readiness.md` **missing** — closure tasks T005–T015, T011 |
| Native workflow run `c37bf147`, B6/B7, spec-gates, named downstream trial | **Out of feature closure** — [progress.md](./progress.md) |

**Target shape for § Opt-in work procedures (after T005–T013):** keep existing copy/upgrade/rollback blocks; add subsections **Activation**, **Host-owned vs kit-added**, **Minimum kit baseline**, **AGENTS.md merge example**, **Repeat install and operator edits** (idempotency + edited transferred file policy). Do not duplicate bundle import steps from earlier HOW_TO_IMPORT sections.

## Technical Context

**Language/Version**: Python 3 (stdlib `unittest`); Markdown adoption docs  
**Primary Dependencies**: `usage/HOW_TO_IMPORT.md`, `usage/ADOPTION_BUNDLES.md`, ADR-0015, host `sha256sum`  
**Storage**: N/A (adopter repo file layout)  
**Testing**: `timeout 120s python3 -m unittest ci.gate_tests.test_work_procedures -v`  
**Target Platform**: Cursor-class agent hosts first; Linux/macOS shell for copy recipe  
**Project Type**: Governance kit documentation + CI gate tests  
**Performance Goals**: N/A  
**Constraints**: Do not weaken `ci/import_bundle.py` symlink rejection; FR-009 (additive, non-mandatory); no commit/push unless operator authorizes  
**Scale/Scope**: One documented opt-in path; optional manifest/bundle change only after proven gap (spec assumption)

## Constitution Check

*GATE: Passed before Phase 0. Re-checked after Phase 1 design.*

Kit governance applies (`.specify/memory/constitution.md` is a Spec Kit placeholder; normative rules remain in `constitution/` and adoption contracts).

| Check | Status | Notes |
| --- | --- | --- |
| Normative vs advisory separation | Pass | Recipe is opt-in; enforcement authority unchanged (FR-009) |
| Import safety contract | Pass | Copy path uses regular files; importer symlink rejection unchanged |
| HIGH-risk touchpoints | Pass with care | Adoption docs + CI gate tests — use AEP JSON below |
| DOC DELTA on doc/behavior changes | Required | CHANGELOG + external adoption record when recipe text closes |
| Verification before completion claims | Required | Green `test_work_procedures` + quickstart §1 before claiming SC-001–SC-004 |

**Post-design re-check**: `contracts/opt-in-recipe.md` and `data-model.md` match research decisions; no unjustified complexity or constitution violations.

## Project Structure

### Documentation (this feature)

```text
specs/002-opt-in-transfer-recipe/
├── spec.md
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1 validation guide
├── contracts/opt-in-recipe.md
├── checklists/requirements.md
├── checklists/recipe-readiness.md   # SC-005 — create in tasks (T011)
├── progress.md          # Durable ledger (implementation updates)
└── tasks.md             # Executable closure steps
```

### Source Code (repository root)

```text
usage/HOW_TO_IMPORT.md
usage/ADOPTION_BUNDLES.md
usage/AI_ENGINEERING_METHODS.md
ci/gate_tests/test_work_procedures.py
.cursor/skills/governed-work/SKILL.md
vendor/superpowers/v7.0.1/
.specify/presets/ai-governance/
adr/ADR_0015_Pinned_Work_Procedures.md
research/EXTERNAL_PROJECT_EVALUATIONS.md
CHANGELOG.md
```

**Structure Decision**: No new runtime package; extend existing kit paths and gate tests only.

## Complexity Tracking

No constitution violations requiring justification.

## Gap map (spec → evidence)

| ID | Requirement / outcome | Current evidence | Closure task(s) |
| --- | --- | --- | --- |
| FR-001 | Explicit what is added / never overwritten | Partial (copy block + one-line AGENTS/overlay) | T008, T013 |
| FR-002 | Host + overlay precedence | Stated; not tabulated | T006, T008 |
| FR-003 | Coherent pin + entry + verify | Copy block + gate tests | T003–T004 (confirm sync) |
| FR-004 | Import/bundle primary path | § Opt-in + research | T009, T010 |
| FR-005 | Activation / discovery | Missing dedicated subsection | T005, T007 |
| FR-006 | Repeat install behavior | Doc + `FileExistsError` test | T013–T014 |
| FR-007 | Upgrade / rollback | Doc + gate test | T015 |
| FR-008 | Disposable fixture verification | Gate tests | T002, T019 |
| FR-009 | Non-mandatory procedures | ADR + spec | T011 (checklist item) |
| FR-010 | Single source of truth vs bundles | Generic HOW_TO_IMPORT links only | T009 |
| SC-001–SC-004 | Fixture outcomes | Tests pass at plan time | T002, T019 |
| SC-005 | Two readers, ten items | Checklist file missing | T011 + quickstart §4 |

## User story → phase mapping

| Story | Priority | Phase in tasks.md | Independent test |
| --- | --- | --- | --- |
| US1 — Adopter enables governed work | P1 | Phase 3 | Fixture sentinels + activation smoke (SC-001, SC-002) |
| US2 — Maintainer repeatable recipe | P1 | Phase 4 | Artifact table + bundle cross-ref + SC-005 checklist |
| US3 — Repeat install / upgrade / rollback | P2 | Phase 5 | Existing gate tests + edited-file policy |

## Method and continuation

```aep
{
  "schema_version": 1,
  "status": "READY",
  "objective": "Finish normative recipe documentation and SC-005 checklist so maintainer and adopter readers can close the feature from disposable-fixture evidence alone.",
  "discovery": [
    "spec.md and checklists/requirements.md are complete.",
    "HOW_TO_IMPORT § Opt-in work procedures and _copy_procedures agree on pin, entry skill, preset.",
    "python3 -m unittest ci.gate_tests.test_work_procedures -v: 7 passed (2026-11-03 plan refresh, this session).",
    "progress.md records native workflow, B6/B7, spec-gates, and named downstream trial as out of scope unless operator expands mandate."
  ],
  "risk": "HIGH",
  "scope": {
    "paths": [
      "specs/002-opt-in-transfer-recipe/**",
      "usage/HOW_TO_IMPORT.md",
      "usage/ADOPTION_BUNDLES.md",
      "usage/AI_ENGINEERING_METHODS.md",
      "ci/gate_tests/test_work_procedures.py",
      "adr/ADR_0015_Pinned_Work_Procedures.md",
      "research/EXTERNAL_PROJECT_EVALUATIONS.md",
      "CHANGELOG.md"
    ],
    "allowed_effects": [
      "Edit documentation and gate tests in this checkout",
      "Run non-interactive unit tests",
      "Update feature ledger progress.md"
    ],
    "approval_required": [
      "Merge",
      "Push",
      "Publish",
      "Named downstream repository trial"
    ]
  },
  "steps": [
    {"paths": ["specs/002-opt-in-transfer-recipe/progress.md"], "action": "Record baseline test output and remaining doc gaps", "reason": "Ledger for resume"},
    {"paths": ["usage/HOW_TO_IMPORT.md"], "action": "Add activation, ownership table, minimum baseline, edited-file policy", "reason": "FR-001, FR-005, FR-006, US1–US3"},
    {"paths": ["usage/ADOPTION_BUNDLES.md"], "action": "Point to § Opt-in work procedures for profile transfer", "reason": "FR-010"},
    {"paths": ["specs/002-opt-in-transfer-recipe/checklists/recipe-readiness.md"], "action": "Publish ten-item SC-005 checklist", "reason": "SC-005"},
    {"paths": ["ci/gate_tests/test_work_procedures.py"], "action": "Extend only if doc promises new automated behavior", "reason": "FR-006, FR-008"},
    {"paths": ["CHANGELOG.md", "research/EXTERNAL_PROJECT_EVALUATIONS.md"], "action": "DOC DELTA on closure", "reason": "Kit doc impact rule"}
  ],
  "verification": [
    {"command": "timeout 120s python3 -m unittest ci.gate_tests.test_work_procedures -v", "expected": "Exit 0"},
    {"command": "Manual: specs/002-opt-in-transfer-recipe/quickstart.md §1–3", "expected": "Gate pass; smoke steps match T005 text"},
    {"command": "Manual: two readers complete checklists/recipe-readiness.md from recipe text only", "expected": "Matching 10/10 for SC-005"}
  ],
  "acceptance": [
    "SC-001 through SC-004 satisfied via gate tests and HOW_TO_IMPORT",
    "SC-005 satisfied via recipe-readiness checklist with two matching readers",
    "progress.md maps FR-001–FR-010 and SC-001–SC-005 to doc sections and test names",
    "Native workflow, B6/B7, spec-gates, named downstream remain explicitly unmet or out of scope"
  ],
  "blocking_questions": [],
  "budget": {"max_repair_attempts": 3, "on_exhaustion": "Stop; report last command output and next operator decision."},
  "doc_delta": "HOW_TO_IMPORT opt-in section, ADOPTION_BUNDLES cross-ref, recipe-readiness checklist, CHANGELOG, EXTERNAL_PROJECT_EVALUATIONS step-2 status."
}
```

**Execution**: Run [tasks.md](./tasks.md) via governed-work `executing-plans` (entry: `.cursor/skills/governed-work/SKILL.md`). Documentation tasks skip TDD red-green. **Do not commit or push** unless the operator asks.

## Phase artifacts (this command)

| Artifact | Path | State |
| --- | --- | --- |
| Research | [research.md](./research.md) | Complete |
| Data model | [data-model.md](./data-model.md) | Complete |
| Contract | [contracts/opt-in-recipe.md](./contracts/opt-in-recipe.md) | Complete; align after doc edits (T012) |
| Quickstart | [quickstart.md](./quickstart.md) | Complete; §3 tracks T005/T007 |
| Tasks | [tasks.md](./tasks.md) | Ready for implementation (T001–T020); none marked complete until a full implement pass |
| Recipe readiness (SC-005) | [checklists/recipe-readiness.md](./checklists/recipe-readiness.md) | **Create in T011** |

## Handoff (next implement pass)

1. Run governed-work **executing-plans** against [tasks.md](./tasks.md) in order (Phases 1–2 before US doc bursts).
2. Prefer **one edit session** on `usage/HOW_TO_IMPORT.md` for T005, T006, T008, T010, T013 to avoid merge conflicts.
3. Do **not** commit, push, or edit `.specify/workflows/runs/c37bf147/state.json` unless the operator expands mandate.
4. Record evidence in [progress.md](./progress.md) via T001–T002, T019–T020; SC-005 §4 still needs two human readers after T011.
