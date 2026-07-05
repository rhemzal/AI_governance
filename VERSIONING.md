# Kit Versioning Policy

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This policy helps consumers answer: **which kit version do I have, and what kind of update is this?**

## Version scheme

| Series | Meaning |
| --- | --- |
| **0.x** | Experimental. Breaking governance changes are allowed. Bundle composition and file layout may change. |
| **1.0+** | Stable adoption contract: bundle names, core file paths, and normative document roles remain compatible unless marked breaking. |

The kit version is recorded in:

- `kit-manifest.yml` → `version` (bundle manifest schema + kit release series)
- Git tags (recommended): `v0.1.0`, `v1.0.0`, …
- `CHANGELOG.md` (human-readable release notes)

Record **all three** in your import ADR when they differ (common on `main` between tags).

## Current release mapping

| Git tag | Manifest `version` | Adoption contract | Notes |
| --- | --- | --- | --- |
| `v1.0.0` (2025-12-31) | *(no manifest file)* | Pre-bundle baseline | Public-ready kit without `kit-manifest.yml` bundles. |
| `main` (ahead of `v1.0.0`) | `0.1` | Experimental (`0.x`) | Bundles (`minimal` … `full`), `VERSIONING.md`, architecture entry point — see `CHANGELOG.md` **Unreleased**. |

**Rule:** Pin imports by **git tag and/or commit SHA**. Read `kit-manifest.yml` `version` from the **same** commit you copy or submodule-pin. Do not mix a release tag with a manifest from a newer branch.

When `main` is ahead of the latest tag, treat **Unreleased** changelog entries as the delta from the last tag until a new tag is published.

## After you import

Record the import in an ADR (see `usage/HOW_TO_IMPORT.md` → Governance Versioning):

- import date
- bundle(s) imported (`minimal`, `standard`, `architecture`, `research`, `full`)
- source tag and/or commit SHA
- whether you use Copy, Submodule, or Fork

Example ADR fields:

```text
Kit: AI_governance
Bundle: standard + architecture
Source: tag v0.2.0 (commit abc1234)
Manifest version: 0.1
Strategy: Copy
```

## Upgrade decision guide

| Changelog label | Action for importers |
| --- | --- |
| **Advisory-only** | Optional refresh. No rule enforcement change expected. |
| **Import bundle change** | Review `kit-manifest.yml` and `usage/ADOPTION_BUNDLES.md`; adjust copied paths or overlay. |
| **Governance-impacting** | Read affected `constitution/` / `ci/` docs; update local overlay if needed; rerun verification. |
| **Breaking rule change** | Treat as a governance dependency upgrade: ADR required, diff review, re-validate CI/doc gates. |

## Submodule / fork consumers

- **Submodule:** pin SHA; upgrade via PR with changelog review and a doc hygiene review appropriate for the downstream repository.
- **Copy:** re-copy changed paths or merge manually; preserve provenance banners; record old → new version in an ADR.
- **Fork:** maintain your own tags; document upstream cherry-pick policy.

## Relationship to manifest `version`

`kit-manifest.yml` `version` tracks the **manifest schema and bundle contract**, not every doc edit.

- Manifest `0.1` → initial bundle definitions (`minimal`, `standard`, `architecture`, `research`, `full`)
- Future manifest bumps should appear in `CHANGELOG.md` under **Import bundle change**

## Related Documents

- `CHANGELOG.md`
- `kit-manifest.yml`
- `usage/HOW_TO_IMPORT.md`
- `usage/ADOPTION_BUNDLES.md`
- `adr/ADR_TEMPLATE.md`
