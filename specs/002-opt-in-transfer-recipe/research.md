# Research: Opt-In Governed Work Transfer Recipe

**Feature**: `specs/002-opt-in-transfer-recipe/spec.md`  
**Date**: 2026-11-03

## Decision: Opt-in uses regular-file copy, not `ci/import_bundle.py`

**Rationale**: The kit's active Superpowers skills under `.cursor/skills/` are symlinks into `vendor/superpowers/v7.0.1/`. `ci/import_bundle.py` rejects symlinks by design. Bundling those paths would weaken import safety or fail adoption copies.

**Alternatives considered**:

- Add a bundle selection that includes symlinked skills — rejected; conflicts with importer contract and FR-004.
- Relax symlink rejection for procedure paths only — rejected; high-risk change to mandatory import behavior.
- Vendor only documentation and instruct manual symlink creation — rejected; breaks adopter hosts that disallow or mishandle symlinks in imports.

## Decision: Default manifest selections omit the work profile

**Rationale**: `kit-manifest.yml` bundle selections (minimal through full) target governance baseline and optional research; the pinned procedure pin, Cursor skill links, presets, and workflows are repository-local pilot paths documented in ADR-0015.

**Alternatives considered**:

- Extend `full` to include all `.cursor/skills/*` symlinks — rejected until a reproducible opt-in path is proven in disposable fixtures (spec assumption).
- New mandatory bundle for procedures — rejected; FR-009 requires additive advisory adoption, not new constitutional requirements.

## Decision: Disposable fixture tests mirror the documented shell recipe

**Rationale**: `ci/gate_tests/test_work_procedures.py` implements `_copy_procedures()` aligned with `usage/HOW_TO_IMPORT.md` § Opt-in work procedures. Gate tests give SC-001–SC-004 evidence without a named downstream repository.

**Alternatives considered**:

- Integration test only in a external adopter repo — deferred; requires separate operator authorization (FR-008, progress ledger).

## Decision: Native Spec Kit workflow completion is out of this feature's closure scope

**Rationale**: Operational adoption AEP P0 (native `specify workflow run` trace) is blocked on run `c37bf147` status `running` with resume refused. The transfer recipe deliverable does not require workflow engine acceptance; progress.md records the blocker separately.

**Alternatives considered**:

- Edit `.specify/workflows/runs/.../state.json` — rejected by governed-work ledger rules.
- Block recipe publication until native run completes — rejected; spec scopes deliverable to transfer and activation documentation, not engine certification.

## Decision: Activation target is Cursor-class hosts first

**Rationale**: Entry point is `.cursor/skills/governed-work/SKILL.md`; proportionality and continuation rules assume Cursor skill discovery. Other hosts are documented as unsupported unless explicitly tested later (spec assumption).

**Alternatives considered**:

- Generic AGENTS-only routing without skill host — insufficient for procedure pin resolution paths tested today.
