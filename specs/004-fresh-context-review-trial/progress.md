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

| Finding | B0 | B1 |
|---------|----|----|
| Symlink test gap | Miss | Found |
| Doc completeness | Partial | Found |

**Experiment B screening:** **PASS** — B1 found ≥1 verified gap B0 skim missed; cost one read-only review pass.

**Disposition:** Optional follow-up: add `test_dirty_tree_identity_for_symlink` (low priority). Do **not** install EGM; pattern is “separated review packet” only.

## Task log

- Task 1 B0: complete (documented misses)
- Task 2 B1: complete
- Task 3: complete (PASS screening)
