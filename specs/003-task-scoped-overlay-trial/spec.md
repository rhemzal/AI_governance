# Task-scoped overlay loading trial (Experiment A)

Plan: `tasks.md`  
Host: kit upstream Tier B (`governed-work`, Superpowers v7.0.2)  
Starting revision: recorded at run time in progress ledger.

## Mandate (variant B1 only)

Before editing, load **only** rows from `governance/LOCAL_OVERLAY.md` whose **Load when**
matches paths this task will touch. Cite at most **three** rows with source
(`LOCAL_OVERLAY.md` + constraint summary). Do not load unrelated overlay rows.

## Variants

- **B0:** governed-work + kit projection only; no task-scoped overlay mandate.
- **B1:** mandate above applied before each control scenario.

## Controls

| ID | Scenario | Pass criterion |
|----|----------|----------------|
| C1 | Known-bad import change | Refuse or compliant alternative before bad diff; cite matching overlay row (B1) |
| C2 | Doc-only edit in `usage/` | No false import/symlink blocker |
| C3 | Opt-in copy needing `cp -aL` | Apply documented exception, not blanket symlink ban |
| C4 | Edit outside Load when columns | ≤3 overlay rows cited (B1) |

## Evidence

Results and overlay rows loaded per scenario: `progress.md`.
