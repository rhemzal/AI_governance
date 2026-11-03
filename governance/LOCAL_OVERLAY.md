# LOCAL GOVERNANCE OVERLAY — kit upstream

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). It applies only to this upstream repository. Adopters copy `LOCAL_OVERLAY_TEMPLATE.md` to `governance/LOCAL_OVERLAY.md` in their project root. This file is excluded from import bundles via `kit-manifest.yml`._

## Purpose

Maintainer policy for the kit repository: where agents load local import constraints, and how this repo differs from an adopter layout.

## Imported baseline

This repository **is** the kit source. Kit root and project root coincide. There is no `vendor/AI_governance/` snapshot here.

## Precedence

`AGENTS.md`, this overlay, and host decisions in `governance/` override kit defaults only where this overlay says so. Canonical rules remain under `constitution/`. Pinned work procedures route through `.cursor/skills/governed-work/SKILL.md`.

## Enforcement maturity

See `usage/ENFORCEMENT_MATRIX.md` (kit repo vs adopter). Maintainers run stricter reference CI than default adopter **CM0**.

- **CM level**: maintainer dogfood (doc-hygiene, adr-required, gate regressions)
- **Declared**: 2026-11-03
- **Canonical test command**: `python3 -m unittest discover -s ci/gate_tests -q` (see `DEVELOPMENT.md`)

## Local constraints

Procedure: `usage/ENGINEERING_METHODS_ADOPTION.md`, Discover local constraints. A task loads only rows whose **Load when** column matches the files it edits.

| Constraint                                                                                                                                                                          | Sources                              | Reason                                                                | Exception                                                                                                                             | Load when                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| A first import refuses an existing destination, including an empty directory, and does not delete it.                                                                               | `import_copy`; ADR-0010              | A-01 replaced host files by copying onto an existing tree.            | `--readopt` may remove only the snapshot that the same failed run created, and only when that path did not exist before the run.      | The task edits `ci/import_bundle.py` or the import procedure. |
| A symlink is not a snapshot, a root-layout directory, or a selected file. Do not relax `no_symlinks` so a copy can succeed.                                                         | `no_symlinks`, `readopt_destination` | The importer rejects links so a copy cannot escape the selected tree. | The opt-in procedure copies the Superpowers pin and entry skill with `cp -aL` / `cp -L`. Those paths are outside the bundle importer. | The task copies kit files or changes symlink checks.          |
| Re-adoption writes the joined snapshot only. A host file in `HOST_OWNED` stays at the project root. A local rule stays when the previous revision is unknown or both sides changed. | `HOST_OWNED`, `merge_readopt`        | Host instructions and local policy are not kit files.                 | When the previous SHA shows the local bytes still match that revision, the joined snapshot takes the upstream bytes.                  | The task changes re-adoption or host-owned paths.             |

## Verification

Before PRs that touch documentation, import bundles, or gate runtime: `DEVELOPMENT.md` doc hygiene checklist and `ci/gate_tests` as applicable.
