# Adoption Bundles (Human Guide)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This is the human companion to `kit-manifest.yml`. Use the manifest for bundle selection. Paths describe a kit snapshot under its own root, normally `vendor/AI_governance/`, not permission to overwrite project files. Follow `usage/HOW_TO_IMPORT.md` for fresh-destination copying and deliberate host entry-point integration.

**Do not copy the whole kit by default.** Pick one baseline bundle, then add optional bundles only when you need them.

## Quick picker

| Bundle | One-line purpose | Choose when |
| --- | --- | --- |
| **minimal** | Fastest useful adoption | You want agent projections + core rules in an existing repo with minimal friction. |
| **standard** | Serious solo / multi-agent baseline | You want enforceable governance: constitution, CI gate principles, ADRs, usage workflows, overlay template. |
| **architecture** | Architecture decision support | You need structured architecture selection, taxonomy, data modeling, terminology, and advisory RAG notes. |
| **research** | Advisory grounding | You want external playbook research and adaptation references (non-normative). |
| **full** | Complete governance dependency | The repo will treat this kit as its governance baseline (copy-import Option A). |

## Bundle details

### minimal — quick adoption

Smallest useful set for “try it this week”:

- Agent projections (`AGENTS.md`, `.github/copilot-instructions.md`)
- Core rules, high-risk enforcement, adaptive governance (G0–G4), and daily enforcement
- AEP validation spec (`usage/AEP_VALIDATION.md`)
- Quick recipes (`usage/QUICKGUIDE.md`)
- ADR template
- Manifest catalog, architecture decision framework and terminology glossary required by the constitution

**Typical next step:** run Recipe D/E from `usage/QUICKGUIDE.md`, then upgrade to `standard` when you are ready for CI gate principles and full usage workflows.

### standard — serious solo / multi-agent project

Everything in **minimal**, plus:

- Kit-root meta docs: `VERSIONING.md`, `DEVELOPMENT.md`, `CHANGELOG.md` (the manifest is already in minimal). Keep these inside the kit root; they describe the kit, not the host project.
- Full `constitution/`, `ci/`, `adr/`, `usage/` (incl. `usage/AI_PRODUCTIVITY_CALIBRATION.md`, `usage/templates/`)
- Local overlay template and calibration summary template (`governance/LOCAL_OVERLAY_TEMPLATE.md`, `governance/AI_CALIBRATION_SUMMARY.template.md`)

**This is the recommended default** for repos where AI agents do regular multi-file work.

**Enforcement defaults:** see `usage/ADOPTION_ENFORCEMENT_CONTRACT.md` (CM0–CM3 Required / Advisory / Deferred per level).

### architecture — architecture decisions

Add when you need extended decision support beyond the baseline framework/glossary:

- Entry point: `architecture/README.md`
- Architecture decision framework, copy-paste prompt (`architecture/ARCHITECTURE_DECISION_PROMPT.md`), style matrix, solution taxonomy
- Data modeling guide (incl. `DATA MODEL DECISION RECORD` mini-template) and terminology glossary
- Advisory notes under `architecture/rag/` (incl. `architecture/rag/RAG_NOTE_TEMPLATE.md` for new notes)

Does **not** replace ADRs. Use it to inform ADRs written in your repo.

### research — advisory grounding

Add when you want playbook research and external evaluation notes:

- `research/` (non-normative; does not override `constitution/` or `ci/`)

Skip this bundle if you only want operational governance, not research context.

### full — governance dependency

Use only when the target repo adopts the kit as its **governance baseline**:

- Composes **standard** + **architecture** + **research**
- Adds `interface/`, `notes/`, and full `governance/`

**Warning:** This is the largest bundle. If the goal is “see if the kit helps,” start with **minimal** or **standard** instead.

## Bundle triage (anti-overload)

Before import or bundle expansion, run **bundle triage** — do not recommend `full` for a trial without explicit governance-baseline justification.

**Corpus budget:**
- **1 baseline** bundle: `minimal` or `standard` (pick one with rationale).
- **Max 1 optional** add-on: `architecture` or `research` (not both unless HIGH-risk need documented).
- **`full`** only when the repo will treat this kit as its **governance baseline** (not “try it out”).

Output template:

```text
ADOPTION BUNDLE TRIAGE
- Repo context (one line):
- Baseline bundle:
- Optional add-on (max 1):
- Deferred bundles (why):
- full justified: yes/no
- Next step (Recipe D/E):
```

See `usage/QUICKGUIDE.md` Recipes D and E.

## Common mistakes

| Mistake | Better approach |
| --- | --- |
| Copy entire repo / all folders | Pick `minimal` or `standard`; add bundles deliberately. |
| Import `full` for a quick trial | Use `minimal`; expand after Recipe D assessment. |
| Replace host agent instructions | Keep projections under the kit root; merge a short entry point into existing host instructions after conflict review. |
| Import `research/` as rules | Treat `research/` as advisory; normative rules stay in `constitution/` and `ci/`. |

## Machine-readable source

- Bundle paths, `extends` / `composes`, and `exclude` rules: `kit-manifest.yml`
- Import mechanics (Copy / Submodule / Fork): `usage/HOW_TO_IMPORT.md`
- Version policy after import: `VERSIONING.md`

## Agent-execution / AEP upgrade note

The updated constitution distinguishes action authority from technical risk and supports bounded repair and handoff. Review local overrides when importing it; an old blanket STOP rule may still override the new behavior.

The `standard` bundle carries the scoped importer/checker (`ci/import_bundle.py`, ADR-0010) and its separate `ci/bundle_tests/` suite, plus `ci/validate_aep.py` and its regression tests through the existing `ci/` directory inclusion. Bundle names and manifest schema are unchanged, but copied contents change. The `minimal` bundle remains documentation-only unless the adopter explicitly imports the AEP CI gate. Upgrade the workflow, validator, and PR declaration format together from one pinned revision (`usage/AEP_VALIDATION.md`).

## Safe import upgrade (ADR-0010)

New copies use a fresh kit directory and reject existing destinations. Existing root-layout imports are not moved or overwritten automatically: inventory host/kit ownership and merge reviewed differences in a migration PR. Minimal stays documentation-only; run import tooling from the pinned upstream checkout when needed. Baseline framework/glossary availability does not require importing the RAG corpus. Workflow YAML and the PR template are upstream-only inputs, fetched from that same revision when a corresponding gate is adopted.

## Related Documents

- `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- `kit-manifest.yml`
- `usage/HOW_TO_IMPORT.md`
- `usage/QUICKGUIDE.md`
- `VERSIONING.md`
