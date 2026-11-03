# Ledger: opt-in transfer recipe

The procedure is [usage/HOW_TO_IMPORT.md](../../usage/HOW_TO_IMPORT.md) § Opt-in work procedures.
The executable copy, repeat stop, upgrade, and rollback are `ci/gate_tests/test_work_procedures.py`.
This file is the feature record. Do not add a second procedure, spec, plan, task list, contract, or checklist here.

Ruling: the adoption note asked for `specs/002-operational-adoption/`. The native `specify` 1.2.5 run created this directory. Keep this path. The decision record stays `research/EXTERNAL_PROJECT_EVALUATIONS.md`.

Ruling: run `c37bf147` timed out while `state.json` still said `running`, and resume refused it. That is not a completed native workflow. Run `b6a246fd` finished `implement` for a plan-and-tasks input and did not execute the recipe. Disposable run `8ecad04d` in `/tmp/wf-implement` finished specify, plan, tasks, and implement for an input that asked to change `calc.py`. The unittest exited 0 and `deploy.sh` did not run. B6/B7 and the later pair show no gain. spec-gates stays deferred. A named downstream checkout was not authorized.

Ruling: 2026-11-03 shrink — the operator continued the audit of the ten-document recipe. Those files restated the procedure and left stale sentences (open-task instructions, a 7-test baseline, a contract that required a governance snapshot the recipe does not). Git history keeps them. This directory now has this ledger only. Cost if wrong: a later session looks for `tasks.md` and finds this pointer.

## Evidence

`timeout 60s python3 -m unittest ci.gate_tests.test_work_procedures -q` after activation smoke: **16 tests, OK**. Includes `test_activation_smoke_after_opt_in_copy`.

A pin or entry that already exists and differs is a manual stop in the recipe. No automated merge of a local edit was added.

## Unmet

- A named downstream checkout with a useful task was not authorized.
- Native Cursor Stop dispatch remains unobserved (separate from workflow run `8ecad04d`).

Activation smoke for a disposable adopter (entry skill, pin paths, proportionality
routing) is `WorkProcedures.test_activation_smoke_after_opt_in_copy`. An operator
session in a real adopter host is still optional.
