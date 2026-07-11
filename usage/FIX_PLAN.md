# Fix Plan — AI_governance kit

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

Date: 2026-07-05
Context: Generated after full re-run of `usage/AUDIT_PLAYBOOK.md` (see `usage/AUDIT_REPORT.md`).
**Implementation status (2026-07-11):** Deep enforcement phase complete — `ADOPTION_ENFORCEMENT_CONTRACT`, `GOVERNANCE_WAIVERS`, `BOUNDARY_GATE_RECIPES`, ADR-0006, extended kit CI (doc-delta, waiver advisory, AEP field checks, D5 error). Prior roadmap + ADR-0005 remain Done. See `usage/AUDIT_REPORT.md` and `usage/RELEASE_READINESS.md`.

## Immediate Fixes (Required Before Next Release Tag)

### 1) Align bundles with cross-referenced root docs (A-01) — **High** — **Done**
- **Why**: Bundled `usage/` docs reference `VERSIONING.md`, `DEVELOPMENT.md`, and `kit-manifest.yml`, but no bundle copies them; copy importers get broken links and lose version policy.
- **Change**: In `kit-manifest.yml`, add root paths to `standard` (minimum: `kit-manifest.yml`, `VERSIONING.md`, `DEVELOPMENT.md`). Optionally add `CHANGELOG.md` to `full`. Update `usage/HOW_TO_IMPORT.md` Option A to say “resolve paths from manifest” instead of a parallel folder list.
- **Verify**: Resolve `standard` and `full` bundles; every `usage/*.md` link to a root `.md` file targets a path in the resolved set (or doc explicitly says “upstream kit repo only”).

### 2) Resolve version label ambiguity (A-03) — **High** — **Done**
- **Why**: `CHANGELOG.md` shows `v1.0.0` plus large Unreleased `[Import bundle change]` block; `kit-manifest.yml` is `0.1`; importers cannot record a single authoritative version.
- **Change**: Either tag a new release from current `main` and move Unreleased entries into it, or add a mapping subsection to `VERSIONING.md` (git tag ↔ manifest `version` ↔ adoption contract). Add one sentence to `README.md` if `main` is ahead of latest tag.
- **Verify**: Importer can fill ADR fields (tag, manifest version, bundle) without ambiguity.

### 3) Restore enforceable doc hygiene contract (A-02) — **High** — **Done**
- **Why**: Python doctor script removed; no CI workflows; `DEVELOPMENT.md` allows “AI-assisted review” without a required checklist artifact.
- **Change**: Add a numbered, tool-agnostic doc hygiene checklist to `DEVELOPMENT.md` (manifest paths, hub links, provenance on import targets, terminology spot-check). Reference it from `usage/PROACTIVE_TRIGGER_MAP.md` automation table. Optional: extend `usage/CI_STARTER_WORKFLOWS.md` with a downstream doc-gate job example.
- **Verify**: Maintainer completes checklist in one sitting; output can be pasted into PR or `usage/AI_RUN_EVIDENCE.md` block.

## Recommended Next Fixes (Ordered by Severity)

### 4) Improve audit and maintenance findability (A-04, A-05) — **Medium** — **Done**
- Add `usage/AUDIT_PLAYBOOK.md` to `README.md` top links.
- Add audit Recipe to `usage/QUICKGUIDE.md` (points to playbook AI prompt).
- Add `architecture/README.md` to `AUDIT_PLAYBOOK.md` mandatory inputs.

### 5) Provenance on agent projections (A-07) — **Medium** — **Done**
- Add provenance banner to `AGENTS.md` and `.github/copilot-instructions.md` (minimal bundle entry points).

### 6) Non-interactive gate in agent projections (A-10) — **Low** — **Done**
- One Quick rules bullet in `AGENTS.md` and `.github/copilot-instructions.md` pointing to `constitution/AI_RULES.md` §6.2.

### 7) Downstream CI adoption (A-06) — **Done** (kit repo reference)
- Kit repo: `.github/workflows/doc-hygiene.yml` (L0, shell/`yq`/`lychee`, no Python scripts).
- Adopters: progressive gates per `usage/CI_MINIMUM_ADOPTION.md`; copy starters from `usage/CI_STARTER_WORKFLOWS.md`.

### 8) Boundary and AEP enforcement (standing drift scenarios) — **Done** (reference starters)
- `usage/CI_STARTER_WORKFLOWS.md` §3 (boundary), §4 (ADR-required), §5 (AEP advisory) — shell/GitHub Actions only.
- Downstream: implement stack-specific boundary tooling and make jobs required when prerequisites exist.

## Suggested PR Themes (One Theme per PR)

| PR theme | Files (primary) | Findings |
| --- | --- | --- |
| Bundle + import alignment | `kit-manifest.yml`, `usage/HOW_TO_IMPORT.md`, `usage/ADOPTION_BUNDLES.md` | A-01, A-05 |
| Versioning clarity | `VERSIONING.md`, `CHANGELOG.md`, `README.md` | A-03 |
| Doc hygiene contract | `DEVELOPMENT.md`, `usage/PROACTIVE_TRIGGER_MAP.md` | A-02 |
| Navigation + audit | `README.md`, `usage/QUICKGUIDE.md`, `usage/AUDIT_PLAYBOOK.md` | A-04, A-05 |
| Agent projections | `AGENTS.md`, `.github/copilot-instructions.md` | A-07, A-10 |

## Immediate Fixes from Prior Audit (2025-12-28)

- Prior run: none required.
- Standing downstream recommendations (CI wiring, boundary checks, ADR-required CI) remain valid; see items 7–8 above.
