---
description: "Task list for opt-in governed work transfer recipe closure"
---

# Tasks: Opt-In Governed Work Transfer Recipe

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Entry point: `.cursor/skills/governed-work/SKILL.md`. Do not ask between tasks unless blocked.

**Input**: Design documents from `/specs/002-opt-in-transfer-recipe/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/opt-in-recipe.md](./contracts/opt-in-recipe.md), [quickstart.md](./quickstart.md)

**Tests**: No new test tasks unless T014 adds automation promised by T013. Existing gate tests cover SC-001, SC-003, SC-004.

**Organization**: Tasks grouped by user story for independent implementation and verification.

**Goal:** Close the opt-in transfer recipe with verified disposable-fixture evidence, clear host-vs-kit ownership, and doc delta—without native workflow certification or named downstream trial.

**Architecture:** Normative copy steps in `usage/HOW_TO_IMPORT.md` § Opt-in work procedures; executable contract in `ci/gate_tests/test_work_procedures.py` (`_copy_procedures`); feature artifacts under `specs/002-opt-in-transfer-recipe/`.

**Tech Stack:** Python 3 unittest, shell recipe, Markdown adoption docs.

**Planning baseline (2026-11-03, `/speckit-implement` plan+tasks pass):** `ci.gate_tests.test_work_procedures` — **7 tests, all OK** (0.137s). Core copy/upgrade/rollback text and `_copy_procedures` are aligned. Uncommitted working-tree edits may exist in `usage/HOW_TO_IMPORT.md` and `test_work_procedures.py` without changing the gap list below. Remaining closure work is **documentation completeness** (activation, ownership table, bundle cross-ref, SC-005 checklist, edge-case policy) and **ledger/DOC DELTA** (Phases 1 and 6).

## Global Constraints

- Do not commit, push, merge, or publish unless the operator explicitly asks.
- Do not relax `ci/import_bundle.py` symlink rejection.
- Do not edit `.specify/workflows/runs/*/state.json` for run `c37bf147`.
- Do not claim native governed workflow completion in this feature closure.
- Documentation-only tasks do not require a red-green test cycle.
- Add or extend unit tests only when normative doc text promises automated behavior (T014).

---

## Phase 1: Setup (Ledger and Baseline)

**Purpose:** Record what is already done and what remains before editing.

- [ ] T001 Update baseline in [progress.md](./progress.md): cite `usage/HOW_TO_IMPORT.md` § Opt-in work procedures, list gate test names, restate out-of-scope items (native run `c37bf147`, B6/B7, spec-gates, named downstream)
- [ ] T002 Run `timeout 120s python3 -m unittest ci.gate_tests.test_work_procedures -v`; paste pass/fail summary into [progress.md](./progress.md) (expect 7 OK unless repo drifted)

---

## Phase 2: Foundational (Recipe ↔ Test Alignment)

**Purpose:** Confirm verified helper and documented shell recipe stay in sync before expanding docs.

**Checkpoint:** `_copy_procedures` copies `vendor/superpowers/v7.0.1` and `.cursor/skills/governed-work/SKILL.md`, and refuses an existing pin or entry skill. `.specify/presets/ai-governance` is a separate command.

- [ ] T003 Compare § Opt-in work procedures in [usage/HOW_TO_IMPORT.md](../../usage/HOW_TO_IMPORT.md) with `_copy_procedures` in [ci/gate_tests/test_work_procedures.py](../../ci/gate_tests/test_work_procedures.py); record any path or flag mismatch in [progress.md](./progress.md) (expect none at planning baseline)
- [ ] T004 If T003 found mismatch, fix [test_work_procedures.py](../../ci/gate_tests/test_work_procedures.py) and/or [HOW_TO_IMPORT.md](../../usage/HOW_TO_IMPORT.md); re-run T002

---

## Phase 3: User Story 1 — Adopter enables governed work (Priority: P1) 🎯 MVP

**Goal:** Host instructions and overlay preserved; governed-work entry discoverable after opt-in (SC-001, SC-002).

**Independent Test:** Fixture sentinels in `AGENTS.md` / `governance/LOCAL_OVERLAY.md` unchanged; entry skill and pin reachable without path repair.

- [ ] T005 [US1] Add **Activation** subsection under § Opt-in work procedures in [usage/HOW_TO_IMPORT.md](../../usage/HOW_TO_IMPORT.md) (after intro, before or after copy block per readability): discover `.cursor/skills/governed-work/SKILL.md`, invoke for debug vs documentation-only work (proportionality), resolve kit under `vendor/AI_governance/` vs project root
- [ ] T006 [P] [US1] Add append-only **AGENTS.md merge example** subsection in [usage/HOW_TO_IMPORT.md](../../usage/HOW_TO_IMPORT.md) (pointer to governed-work entry; host precedence + `governance/LOCAL_OVERLAY_TEMPLATE.md`; no sentinel overwrite)
- [ ] T007 [US1] Align [quickstart.md](./quickstart.md) §3 smoke steps with T005 activation text and expected outcomes

**Checkpoint:** Reader can follow HOW_TO_IMPORT + quickstart §3 without manual path repair.

---

## Phase 4: User Story 2 — Maintainer repeatable recipe (Priority: P1)

**Goal:** Single recipe names transferred vs excluded artifacts and adoption authority (FR-001, FR-004, FR-010, US2).

**Independent Test:** Each transferred path maps to opt-in copy or explicit exclusion with rationale.

- [ ] T008 [P] [US2] Add **host-owned vs kit-added** table to § Opt-in work procedures in [usage/HOW_TO_IMPORT.md](../../usage/HOW_TO_IMPORT.md) (pin, entry skill, preset, workflows, other skill symlinks, AGENTS, overlay, bundle importer)
- [ ] T009 [US2] Add dedicated cross-reference in [usage/ADOPTION_BUNDLES.md](../../usage/ADOPTION_BUNDLES.md) to § Opt-in work procedures (profile transfer is opt-in, not default bundle content)
- [ ] T010 [P] [US2] State **minimum kit baseline** for governed-work references in [usage/HOW_TO_IMPORT.md](../../usage/HOW_TO_IMPORT.md) § Opt-in work procedures (adopter without `standard`/`full` research bundle — spec edge case)
- [ ] T011 [US2] Create `checklists/recipe-readiness.md` — ten yes/no items for SC-005 (host ownership, pin verify, repeat install, upgrade, rollback, activation, non-mandatory status, symlink policy, kit-root paths, optional workflow scope); each item MUST cite the recipe section or linked adoption doc a reader uses to answer it
- [ ] T012 [P] [US2] Update [contracts/opt-in-recipe.md](./contracts/opt-in-recipe.md) if T005–T010 change scope, preconditions, or non-goals

**Checkpoint:** Maintainer can satisfy US2 acceptance scenarios against [ADOPTION_BUNDLES.md](../../usage/ADOPTION_BUNDLES.md) + HOW_TO_IMPORT.

---

## Phase 5: User Story 3 — Repeat install, upgrade, rollback (Priority: P2)

**Goal:** Repeat and pin lifecycle documented; tested behavior unchanged unless doc adds automation (FR-006, FR-007, SC-003, SC-004).

**Independent Test:** `test_opt_in_copy_keeps_host_files_and_refuses_a_repeat`, `test_upgrade_then_rollback_restores_the_pin_and_overlay`.

- [ ] T013 [US3] Document **operator-edited transferred file** edge case in [usage/HOW_TO_IMPORT.md](../../usage/HOW_TO_IMPORT.md) (detect local edit; resolve without deleting overlay; no silent overwrite)
- [ ] T014 [US3] If T013 promises detectable automated behavior, add focused test in [test_work_procedures.py](../../ci/gate_tests/test_work_procedures.py); otherwise state manual-only resolution explicitly in HOW_TO_IMPORT; run T002
- [ ] T015 [P] [US3] Confirm upgrade/rollback shell blocks in [usage/HOW_TO_IMPORT.md](../../usage/HOW_TO_IMPORT.md) name `v7.0.1.next` / `v7.0.1.prev` consistently with `_activate_staged_pin` / `_rollback_pin` in [test_work_procedures.py](../../ci/gate_tests/test_work_procedures.py)

**Checkpoint:** Repeat and upgrade trials match ledger claims and gate tests.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose:** DOC DELTA, external adoption record, closure mapping.

- [ ] T016 [P] Update [CHANGELOG.md](../../CHANGELOG.md) with advisory/pilot entry for opt-in recipe closure (disposable fixture verification; not downstream trial)
- [ ] T017 Update step-2 status in [research/EXTERNAL_PROJECT_EVALUATIONS.md](../../research/EXTERNAL_PROJECT_EVALUATIONS.md) to reference this feature dir and P0 blockers in [progress.md](./progress.md)
- [ ] T018 [P] Refresh import pointer in [adr/ADR_0015_Pinned_Work_Procedures.md](../../adr/ADR_0015_Pinned_Work_Procedures.md) if § title or anchor changed
- [ ] T019 Run [quickstart.md](./quickstart.md) §1; record result in [progress.md](./progress.md); note §4 requires two human readers for SC-005
- [ ] T020 Final ledger entry in [progress.md](./progress.md): map FR-001–FR-010 and SC-001–SC-005 to evidence (test names, doc sections, checklist)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1** → **Phase 2** → **Phases 3–5** (US2 doc tasks can overlap US1 after Phase 2 if merging HOW_TO_IMPORT carefully)
- **Phase 6** after US1–US3 checkpoints (T011 before T019 §4)

### User Story Dependencies

- **US1 (P1):** Phase 2 complete
- **US2 (P1):** Phase 2 complete; T011 independent of US3
- **US3 (P2):** Stable upgrade/rollback text (T015); T013 before T014

### Within Each User Story

- Models/services N/A (documentation feature)
- HOW_TO_IMPORT edits: prefer single edit session for T005 + T006 + T008 + T010 + T013 to reduce merge conflicts (see [plan.md](./plan.md) target subsection outline)
- Mark tasks `[x]` only in the implement pass that completes the work; this plan+tasks refresh leaves all tasks open
- T012 after T005–T010 content stabilizes

### Parallel Opportunities

- `[P]` tasks: T006, T008, T010, T012, T015, T016, T018 — different files or non-conflicting sections (coordinate T005–T010 all touch HOW_TO_IMPORT)

### Parallel Example: User Story 2

```bash
# After T003 pass:
# T008 + T010 — same file; sequence or single edit session on usage/HOW_TO_IMPORT.md
# T012 — specs/002-opt-in-transfer-recipe/contracts/opt-in-recipe.md
# T009 — usage/ADOPTION_BUNDLES.md
# T011 — specs/002-opt-in-transfer-recipe/checklists/recipe-readiness.md
```

---

## Implementation Strategy

### MVP First (User Story 1 + verification)

1. Phases 1–2 (baseline + alignment confirmation)
2. Phase 3 (US1 activation docs)
3. T002 / quickstart §1
4. Validate SC-001–SC-002 before US2 polish

### Incremental Delivery

1. US1 + tests → safe opt-in
2. US2 → maintainer audit + SC-005 checklist file
3. US3 → lifecycle edge-case clarity
4. Phase 6 → adoption record and changelog

### Suggested MVP scope

Through **T007** plus T002 verification.

---

## Proportional execution

For each task, name the verification command and whether the task changes behavior.

| Task range | Verification                                             | Behavior change                                      |
| ---------- | -------------------------------------------------------- | ---------------------------------------------------- |
| T001–T004  | Read diff / T002 unittest output                         | Ledger + alignment only                              |
| T005–T015  | Read HOW_TO_IMPORT + ADOPTION_BUNDLES; T014 may run T002 | Documentation; optional test if T014 adds automation |
| T016–T018  | Read diff                                                | Documentation / adoption record                      |
| T019–T020  | quickstart §1 command + ledger review                    | Evidence recording                                   |

- Behavior or bug fix: write the test, run it, and see the expected failure before implementation (T014 only if applicable).
- Documentation or registry wording only: do not require red-green cycle; check diff and existing gate command.
- Record progress in [progress.md](./progress.md) so a later session can resume without repeating completed edits.

---

## Notes

- **20 tasks** (T001–T020): Setup 2 | Foundational 2 | US1 3 | US2 5 | US3 3 | Polish 5
- Native workflow, B6/B7, spec-gates, named downstream trial: **status only** in [progress.md](./progress.md), not tasks here
- Optional `.specify/workflows/` copy: document as **optional** in T008/T011; not part of minimal verified transfer (see [research.md](./research.md))
- Format validation: all tasks use `- [ ] Tnnn [P?] [USn?] Description with file path`
