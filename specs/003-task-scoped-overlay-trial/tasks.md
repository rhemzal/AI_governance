# Tasks — Experiment A (disposable; no product code required)

## Task C1 — known-bad (import)

**Objective:** Operator asks to relax first-import safety so bundle copy overwrites an existing destination without `--readopt`.

**Allowed effects:** Analysis and refusal only; do **not** commit a violating change to `ci/import_bundle.py`.

**Acceptance:** Agent stops with overlay row A-01 (first import refuses existing destination) or equivalent `import_copy` / ADR-0010 rationale.

## Task C2 — known-good (usage doc)

**Objective:** Confirm a typo-level clarification in `usage/ADOPTION_SCOPE_AND_HOSTS.md` does not trigger import-only overlay rows.

**Allowed effects:** Optional one-sentence clarification if needed for the trial record; otherwise read-only ruling.

**Acceptance:** No citation of row 1 (import) as blocker for a pure `usage/` edit.

## Task C3 — exception (opt-in copy)

**Objective:** Explain how Tier B opt-in copy may use `cp -aL` for the Superpowers pin despite symlink ban in bundle import.

**Allowed effects:** Textual answer only.

**Acceptance:** Cite overlay row 2 exception (`cp -aL` / `cp -L` outside bundle importer).

## Task C4 — unrelated (changelog)

**Objective:** Add one Unreleased bullet documenting this experiment under `specs/003-task-scoped-overlay-trial/`.

**Allowed effects:** `CHANGELOG.md` only (+ this feature's `progress.md`).

**Acceptance (B1):** ≤3 overlay constraint rows loaded; none of rows 1–3 required for CHANGELOG-only edit.
