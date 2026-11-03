# Quickstart: Validate the Opt-In Transfer Recipe

Disposable validation only. No named downstream repository required (FR-008).

## Prerequisites

- Python 3 with stdlib (same as kit CI).
- Kit checkout at repo root `/home/risa/AI_governance` (adjust paths if elsewhere).
- `sha256sum` available (used in documented recipe and tests).

## 1. Gate tests (primary evidence)

From kit root:

```bash
timeout 120s python3 -m unittest ci.gate_tests.test_work_procedures -v
```

**Expected**: All tests pass, including:

- `test_opt_in_copy_keeps_host_files_and_refuses_a_repeat`
- `test_upgrade_then_rollback_restores_the_pin_and_overlay`

## 2. Manual shell recipe (optional cross-check)

In a temporary directory acting as adopter root, with `KIT` set to the kit checkout, run the block in `usage/HOW_TO_IMPORT.md` § Opt-in work procedures.

**Expected**:

- Host files you create before copy remain unchanged.
- Second run stops when pin directory exists.
- Upgrade/rollback block restores pin without changing overlay sentinel text.

## 3. Smoke activation (SC-002, operator session)

After copy in a disposable adopter (or this kit repo):

1. Confirm `.cursor/skills/governed-work/SKILL.md` is discoverable.
2. Invoke governed work for a documentation-only task (e.g., edit a spec sentence) and confirm proportionality text applies (no spurious TDD demand).
3. Invoke governed work for a failing gate test and confirm routing to systematic debugging is stated in the entry table.

**Expected**: No manual repair of relative paths to `vendor/superpowers/v7.0.1/` or governance docs for these smoke steps.

## 4. Ownership checklist

`checklists/recipe-readiness.md` cites the recipe section for each item. There is no reader session.

## Out of scope for this quickstart

- Native workflow run completion (see `progress.md`).
- Matched B6/B7 benchmark trials.
- spec-gates retain/replace/defer decision.
- Commit, push, or downstream production trial.
