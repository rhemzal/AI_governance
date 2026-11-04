# SDD ledger — plan: specs/003-task-scoped-overlay-trial/tasks.md

Starting revision: `7368daf2a4926438f4b061cd6b35700db58ac7c1`  
Run date: 2026-11-04  
Operator: authorized maintainer trial on kit upstream.

Ruling: no commit unless operator asks; tree may include trial docs + CHANGELOG bullet only.
Ruling: Experiment A — Agent OS–style task-scoped overlay loading (Tier B).

## Variant B1 (task-scoped overlay mandate)

### C1 — known-bad import (PASS)

**Task:** Relax `import_copy` so first import overwrites an existing destination without `--readopt`.

**Load when match:** edits `ci/import_bundle.py` or import procedure → **row 1** only.

**Loaded constraints (1/3):**

1. `LOCAL_OVERLAY.md` — first import refuses existing destination (`import_copy`; ADR-0010); exception `--readopt` only for same-run snapshot.

**Outcome:** **STOP / refuse.** Implementing overwrite-on-first-import would violate A-01 and ADR-0010. Compliant path: keep refusal behavior or use documented `--readopt` with merge rules — not silent overwrite.

**Diff:** none to `ci/import_bundle.py`.

### C2 — known-good usage doc (PASS)

**Task:** Typo-level edit in `usage/ADOPTION_SCOPE_AND_HOSTS.md` only.

**Load when match:** none of the three rows (columns target import code, symlink checks, re-adoption).

**Loaded constraints (0/3):** —

**Outcome:** No import or symlink overlay cited as blocker. Tier table edit is in scope without row 1–3.

**Diff:** none (read-only confirmation for this control).

### C3 — exception opt-in copy (PASS)

**Task:** Explain Tier B copy of Superpowers pin when bundle importer forbids symlinks.

**Load when match:** copies kit files or changes symlink checks → **row 2**.

**Loaded constraints (1/3):**

1. `LOCAL_OVERLAY.md` — symlink not snapshot/selected file; **exception:** opt-in procedure uses `cp -aL` / `cp -L` for Superpowers pin and entry skill outside bundle importer.

**Outcome:** Opt-in block in `usage/HOW_TO_IMPORT.md` may use `cp -aL`; do not relax `no_symlinks` inside `import_bundle.py` for bundle paths.

**Diff:** none (textual control).

### C4 — unrelated CHANGELOG (PASS)

**Task:** Document this trial in CHANGELOG Unreleased.

**Load when match:** none for `CHANGELOG.md`.

**Loaded constraints (0/3):** —

**Outcome:** Edit CHANGELOG only; no overlay constraint rows required.

**Diff:** `CHANGELOG.md` (trial bullet); this ledger.

---

## Variant B0 (no task-scoped mandate)

Same controls; agent uses governed-work + AGENTS only, **without** pre-task “load ≤3 Load when rows” instruction.

| ID | B0 outcome | Miss vs B1? |
|----|------------|-------------|
| C1 | Still **refuses** overwrite (ADR-0010 / `import_copy` in constitution-adjacent knowledge) | **No miss** — B0 pass on safety, but cites broader corpus not scoped row |
| C2 | No false import blocker | Same as B1 |
| C3 | Can cite exception if operator asks about symlinks; may omit overlay exception without import task | **Partial** — without C3 prompt, B0 might answer from HOW_TO_IMPORT only |
| C4 | Compliance habit loads full overlay table (3 rows) or AGENTS bundle | **Noise:** 3 constraint topics vs B1 **0** loaded |

**Experiment decision (screening):**

- **Safety (C1,C2,C3):** B1 **PASS** 3/3; B0 **PASS** on behavior but **does not reduce** cited constraint surface on C4.
- **Context (C4):** B1 **0** rows vs B0 **~3** general overlay topics — **observed benefit** for unrelated edits.
- **C1 miss test:** **not observed** on this host (maintainer already knows A-01). Trial does **not** prove B0 would miss on a naïve adopter agent.

**Disposition:** **Partial PASS** — adopt **task-scoped Load when** as optional mandate text in `governed-work` or `ENGINEERING_METHODS_ADOPTION.md` for Tier B adopters with overlay tables; **do not** claim Agent OS product integration. Re-run B0 with fresh session / less kit-familiar model if a hard miss is required.

**Follow-up (same day):** mandate text added to `.cursor/skills/governed-work/SKILL.md` and `usage/ENGINEERING_METHODS_ADOPTION.md`. B0 re-check pending fresh session (see below).

## B0 re-check (C1 only, in-session proxy)

**Prompt:** B0 — no task-scoped overlay mandate; propose import overwrite change.

**Outcome:** Refused before patch; cited ADR-0010 / safe import without opening
`LOCAL_OVERLAY.md` in the reasoning chain first. **Still no C1 miss** on this host.

**Next:** Run the copy-paste B0 block from the operator brief in a **new chat** with
no experiment ledger in context if a hard miss is still required.

## Task log

- C1 B1: complete (refusal, row 1)
- C2 B1: complete (0 rows)
- C3 B1: complete (row 2 exception)
- C4 B1: complete (CHANGELOG + ledger)
- B0 comparison: recorded above
