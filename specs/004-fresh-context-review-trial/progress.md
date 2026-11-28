# Ledger — specs/004-fresh-context-review-trial/tasks.md

Starting revision: `b4c6b1e`  
Review target: content-aware `ci/uncommitted_diff_identity.py` (merged #53).

## B0 — author-context review (simulated)

**Stance:** “PR #53 fixed porcelain-only hash; tests pass.”

**Findings:**

- Confirms blob hashing for regular file content (`test_dirty_tree_identity_reflects_file_content`).
- Notes ADR-0016 amendment present.
- **Miss:** no test that **symlink** dirty paths produce stable `link:` markers (implementation supports symlinks; tests only vary regular file bytes).
- **Miss:** docstring does not state that purely **index-stage** states identical to worktree hash the worktree blob (limitation vs index object).

## B1 — fresh-context review (PASS detection)

**Packet only:** ADR-0016 amendment + `uncommitted_diff_identity.py` + test file names from acceptance criteria.

**Findings (confirmed):**

1. **Test gap:** `_blob_marker` returns `link:{target}` for symlinks, but `RunTaskAcceptanceCheck` never exercises a dirty symlink; regression could revert symlink handling unnoticed.
2. **Doc gap:** Module docstring claims content-aware identity but does not document `unknown`/`clean`/`hash-failed` outcomes or rename `orig` column in canonical payload (reader cannot verify contract from doc alone).

**False positives:** 0 on “regular file content distinguishes edits” (already tested).

## Comparison

| Finding          | B0      | B1    |
| ---------------- | ------- | ----- |
| Symlink test gap | Miss    | Found |
| Doc completeness | Partial | Found |

**Experiment B screening:** **PASS** — B1 found ≥1 verified gap B0 skim missed; cost one read-only review pass.

**Disposition:** Optional follow-up: add `test_dirty_tree_identity_for_symlink` (low priority). Do **not** install EGM; pattern is “separated review packet” only.

**Follow-up (2026-11-05):** `test_dirty_tree_identity_reflects_symlink_target` added; docstring clarified in `ci/uncommitted_diff_identity.py`. Experiment B screening closed.

## Task log

- Task 1 B0: complete (documented misses)
- Task 2 B1: complete
- Task 3: complete (PASS screening)

## Scope pairs (2026-11-28)

Four self-contained pairs in
`research/experiments/fresh-context-review/scope-2026-11-28/`. B0 carries an
author "ship it" sentence. B1 does not. Each review was a separate `grok-4.7`
ask session whose workspace held only that packet.

B1 repeated B0 on all four pairs. Both found the whitespace `ValueError` gap
and both restated the missing ADR. Both stayed quiet on the covered
implementation and on the wording edit. The author sentence hid nothing in
this pass. The ADR finding is the same fact the existing architecture gate
already fails. Elephant Goldfish Model stays uninstalled. Record:
`research/experiments/fresh-context-review/scope-2026-11-28/RESULTS.md`.
