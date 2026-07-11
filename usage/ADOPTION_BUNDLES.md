# Adoption Bundles (Human Guide)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This is the human companion to `kit-manifest.yml`. Use the manifest for automation; use this page to choose the right scope.

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

**Typical next step:** run Recipe D/E from `usage/QUICKGUIDE.md`, then upgrade to `standard` when you are ready for CI gate principles and full usage workflows.

### standard — serious solo / multi-agent project

Everything in **minimal**, plus:

- Root meta docs: `kit-manifest.yml`, `VERSIONING.md`, `DEVELOPMENT.md`, `CHANGELOG.md` (referenced by `usage/` import, versioning, and hygiene workflows)
- Full `constitution/`, `ci/`, `adr/`, `usage/`
- Local overlay template (`governance/LOCAL_OVERLAY_TEMPLATE.md`)

**This is the recommended default** for repos where AI agents do regular multi-file work.

**Enforcement defaults:** see `usage/ADOPTION_ENFORCEMENT_CONTRACT.md` (CM0–CM3 Required / Advisory / Deferred per level).

### architecture — architecture decisions

Add when you need decision support, not just enforcement:

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
| Skip agent projections | Include `minimal` (or ensure `AGENTS.md` / Copilot instructions exist). |
| Import `research/` as rules | Treat `research/` as advisory; normative rules stay in `constitution/` and `ci/`. |

## Machine-readable source

- Bundle paths, `extends` / `composes`, and `exclude` rules: `kit-manifest.yml`
- Import mechanics (Copy / Submodule / Fork): `usage/HOW_TO_IMPORT.md`
- Version policy after import: `VERSIONING.md`

## Related Documents

- `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- `kit-manifest.yml`
- `usage/HOW_TO_IMPORT.md`
- `usage/QUICKGUIDE.md`
- `VERSIONING.md`
