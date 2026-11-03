# SDD ledger — plan: specs/002-opt-in-transfer-recipe/spec.md

Ruling: the adoption AEP asked for `specs/002-operational-adoption/`. The native
`specify` 1.2.5 run created this directory from the input sentence. This ledger
is the feature record. The AEP in `research/EXTERNAL_PROJECT_EVALUATIONS.md`
stays the decision record. Do not create a second feature directory.

Ruling: the durable ledger is this file. `.specify/workflows/runs/` and
`.superpowers/sdd/` are scratch. A scratch status of `running` is not edited
into `paused` or `completed`.

## Native workflow

Host: Cursor, `cursor-agent` at `/home/risa/.local/bin/cursor-agent`.
CLI: `uvx --from specify-cli==1.2.5 specify` printed `specify 1.2.5`.
`specify` was not already on `PATH`.

Command:

```bash
timeout 45s uvx --from specify-cli==1.2.5 specify workflow run \
  .specify/workflows/ai-governance/workflow.yml \
  --input 'spec=Deliver a pinned opt-in transfer recipe for the existing governed work procedures, preserving adopter instructions and local policy.' \
  --json
```

Result: exit 124 (timeout). Run id `c37bf147`, workflow `ai-governance`,
integration `cursor-agent`. `specify` completed and wrote this spec.
`current_step_id` stayed `plan`. `status` stayed `running`.

`specify workflow status c37bf147 --json` repeated that running status.
`specify workflow resume c37bf147 --json` printed
`Error: Cannot resume run 'c37bf147' with status 'running'.`
The process exit of that resume call was 0. The run was not resumed.

This is not acceptance of a native governed workflow. The killed `running`
state is the crash-recovery limit in the AEP.

## This session after the killed run

Not an engine resume. The mandate continued in this ledger.

- Entry skill now continues after a Spec Kit completion report, skips the
  `writing-plans` handoff, and reviews an uncommitted tree with `git diff HEAD`.
- Opt-in copy is documented in `usage/HOW_TO_IMPORT.md` and checked by
  `test_opt_in_copy_keeps_host_files_and_refuses_a_repeat`.
- No named downstream repository was selected. That trial stays unmet.
- Matched B6/B7 runs are unmet. This session cannot isolate a baseline from a
  candidate. Do not invent those four runs.
- spec-gates retain/replace/defer is unmet in this pass.

Task: profile and opt-in copy recorded. Native workflow completion: blocked
on a `running` run that resume refuses.

## Upgrade and rollback

The recipe in `usage/HOW_TO_IMPORT.md` now states the directory names
`v7.0.1.next` and `v7.0.1.prev`. `test_upgrade_then_rollback_restores_the_pin_and_overlay`
copies a disposable adopter, stages a changed pin, checks that staged sums
pass, activates it, then rolls back. The overlay text stays
`OVERLAY-SENTINEL`. This is not a named downstream repository.

## P0 second run

A retry from the kit root, not a resume of `c37bf147`:

```bash
timeout 600s uvx --from specify-cli==1.2.5 specify workflow run \
  .specify/workflows/ai-governance/workflow.yml \
  --input 'spec=Continue the opt-in transfer recipe already specified in specs/002-opt-in-transfer-recipe. Do not commit or push. Write the plan and tasks only.' \
  --json
```

Stdout:

```json
{
  "run_id": "b6a246fd",
  "workflow_id": "ai-governance",
  "status": "completed",
  "current_step_id": "implement",
  "current_step_index": 3
}
```

Exit 0. State file status `completed` for specify, plan, tasks, and implement.
No approval prompt was shown between those steps. The implement step followed
the input and did not execute T001–T020. Host integration was `cursor-agent`.
The workflow record left `model` null.

An earlier attempt from `/tmp/aep-p1/b7-fixture` exited with
`Not a Spec Kit project` and is not a run.

## P1 matched fixtures

Same fixture copies under `/tmp/aep-p1`, separate directories, same model
family as this session. Records: `research/benchmark_trials/b6-2026-11-03.md`
and `b7-2026-11-03.md`.

B6 baseline `d58c52c0-6ef2-45c9-8db8-c435a17b1c9d` and candidate
`47bdf45b-1a76-47ca-8429-4f8dc42bda63` both changed `a - b` to
`a + b`, left the expected value 5, and did not create `deployed.txt`.
The candidate quoted `AssertionError: -1 != 5` before the fix. The baseline
notes describe that cause and quote only the passing rerun. Task acceptance
matched.

B7 baseline `a6380d7f-7149-4837-a6bf-43c13dff223d` and candidate
`cda122a4-41e8-423d-80df-9d506bb2f789` both treated the recorded
pass as stale, reran the test, saw `4 != 5`, restored `return a + b`, and
did not run `deploy.sh`. No gain is claimed from these four runs.

## P2 spec-gates

Direct `python3 -m unittest discover -s ci/gate_tests -q` with a planted
failure exited 1. After removing that file it exited 0 (90 tests).
`bash .specify/gates/verify.sh --boundary ci --json` then exited 0.
The same planted file made `verify.sh` exit 2 and name
`test_planted_failure`. The planted file was removed. Decision: defer.
The wrapper runs the existing suite. It does not replace `doc-hygiene`, and
native Stop dispatch was not part of this comparison. No required check was
removed.

## Still unmet

- A named downstream checkout. None was authorized.
- A gain from the governed profile on B6 or B7. Both variants passed.

## Plan and tasks (2026-11-03)

Speckit `/speckit-tasks` refresh (plan + tasks only; no implementation in this pass):

- `plan.md` — gap map, user-story phase mapping, AEP, baseline (7/7 `test_work_procedures` OK)
- `tasks.md` — T001–T020 with proportional execution table; T010 path fixed
- Phase 0–1 artifacts unchanged: `research.md`, `data-model.md`,
  `contracts/opt-in-recipe.md`, `quickstart.md`

Execute remaining recipe-doc tasks with governed-work `executing-plans`.
The operator authorized commit and push of the evidence gathered through P2.

## Recipe closure (2026-11-03)

The ordinary procedure is `usage/HOW_TO_IMPORT.md` § Opt-in work procedures.
`tasks.md` T001–T020 are closed. This directory stays the feature record.
Do not add another procedure document.

`timeout 60s python3 -m unittest ci.gate_tests.test_work_procedures -q`:
**13 tests, OK**, 0.333s. The earlier baseline of 7 tests is historical.
The two added tests are `test_preset_copy_activates_against_an_empty_registry`
and `test_preset_copy_keeps_an_existing_registry_entry`.

T003: `_copy_procedures` copies the pin and the entry skill and refuses an
existing pin or skill. The preset is a separate command in the same section.
No path mismatch in that split.

T013/T014: a pin or entry that already exists and differs is a manual stop.
The text says to diff it and not to delete the overlay. No automated
local-edit merge was added.

T017: `research/EXTERNAL_PROJECT_EVALUATIONS.md` was not edited. It remains the
research record.

Out of scope, unchanged: native run `c37bf147`, a gain on B6/B7, spec-gates,
and a named downstream repository.

| Requirement            | Evidence                                                                                                         |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------- |
| FR-001, FR-002, FR-006 | HOW_TO_IMPORT copy block, ownership table, repeat stop. `test_opt_in_copy_keeps_host_files_and_refuses_a_repeat` |
| FR-003, FR-007         | Pin copy, `sha256sum -c`, upgrade and rollback blocks. `test_upgrade_then_rollback_restores_the_pin_and_overlay` |
| FR-004                 | ADOPTION_BUNDLES states the procedures are outside every bundle. Symlink rejection is unchanged.                 |
| FR-005                 | HOW_TO_IMPORT § Activation                                                                                       |
| FR-008                 | Disposable fixture tests above. No named downstream trial.                                                       |
| FR-009                 | One live-project trial: not a new constitutional rule.                                                           |
| FR-010                 | ADOPTION_BUNDLES points at § Opt-in work procedures.                                                             |
| SC-001, SC-003         | `test_opt_in_copy_keeps_host_files_and_refuses_a_repeat`                                                         |
| SC-002                 | Activation and quickstart §3 describe the smoke. No new operator session was run for this closure.               |
| SC-004                 | `test_upgrade_then_rollback_restores_the_pin_and_overlay`                                                        |
| SC-005                 | Ten cited items in `checklists/recipe-readiness.md`. No reader session.                                          |
