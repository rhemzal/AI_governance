# Adopting This Kit in Existing Projects

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

Use the current import path. Do not copy `constitution/` into the project root and do not turn on CI gates as part of copying files.

An earlier draft of this page told adopters to add `constitution/` and optional warning gates first. That conflicted with the snapshot importer and the adoption contract.

## Where rules live

| Location                                                                           | Role                                                     |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Host `AGENTS.md`, `.github/copilot-instructions.md`, `governance/LOCAL_OVERLAY.md` | Project authority. Read these first.                     |
| Kit snapshot (`vendor/AI_governance/` or your recorded root layout)                | Imported baseline. Paths in kit documents resolve there. |
| `notes/local/**`                                                                   | Optional human notes; not a second policy tree.          |

Do not run with two sources of truth. Record baseline vs reference-only in an ADR ([How to import](HOW_TO_IMPORT.md#if-you-already-have-governance)).

## Agent context (each task)

1. **Mandate** — Use the host entry point and overlay before loading kit `constitution/` files. The kit projection in `AGENTS.md` does not replace host instructions.
2. **Local conventions** — In `governance/LOCAL_OVERLAY.md`, load only the **Local constraints** rows whose **Load when** column matches the files you will edit. Do not load the other rows. If no row matches and the module is unfamiliar, run at most one discovery pass on that module ([Discover local constraints](ENGINEERING_METHODS_ADOPTION.md#discover-local-constraints)). Write at most three rows; do not add an `agent-os/standards/` tree.
3. **Corpus budget** — Use [Proactive trigger map](PROACTIVE_TRIGGER_MAP.md) before bulk-reading `architecture/` or `research/`. Import and overlay docs beat optional corpora for adoption work.
4. **Requirement changes** — Pick one path for a given change: Spec Kit profile, OpenSpec delta, or a direct edit with existing checks. Do not give the same change both a `specs/<feature>/` tree and an OpenSpec change ([Choosing a requirement path](SPEC_DRIVEN_AI_DEVELOPMENT.md#choosing-a-requirement-path)).

Pinned Superpowers procedures and the project Spec Kit preset are **not** in import bundles. Copy them only from [How to import](HOW_TO_IMPORT.md#opt-in-work-procedures) when you want governed-work routing; that copy does not install spec-gates or a Stop hook.

## Maintainer sequence

1. **Snapshot** — [How to import](HOW_TO_IMPORT.md) Option A (or submodule/fork). Use `--readopt` for an already-imported tree; do not delete `vendor/AI_governance` to force a first import again.
2. **Entry point** — Merge the governance baseline block into existing `AGENTS.md`; do not replace the file.
3. **Overlay** — Copy [LOCAL_OVERLAY_TEMPLATE.md](../governance/LOCAL_OVERLAY_TEMPLATE.md) to `governance/LOCAL_OVERLAY.md`. Declare CI Maturity (CM) and the project test command. Leave the constraints table empty until discovery writes rows.
4. **Methods** — Roll out one practice at a time ([Engineering methods adoption](ENGINEERING_METHODS_ADOPTION.md)).
5. **Optional profile** — Opt-in copy for `vendor/superpowers/v7.0.1/` and `.cursor/skills/governed-work/SKILL.md` when the team wants the pinned procedure pin; register the preset separately if Spec Kit templates should append kit mandate text.

Product tests start at CI Maturity CM1 when the project already has tests. A CM0 import does not invent them.

## Named downstream trial (operator authorization required)

Do not pick or modify another person's repository without explicit approval. When authorized:

1. Record repository, revision, and one task with acceptance criteria **before** the agent starts.
2. Use [How to import](HOW_TO_IMPORT.md) and [Opt-in work procedures](HOW_TO_IMPORT.md#opt-in-work-procedures) if the trial needs the procedure pin; use [FOR_EXISTING_PROJECTS](FOR_EXISTING_PROJECTS.md) agent context for overlay rows.
3. Write outcomes to an existing ledger (`specs/<feature>/progress.md`) or the research record. Do not add a parallel procedure tree.
4. Treat a disposable fixture or gate test as structural evidence only. Claim real downstream adoption only when the named checkout completes the authorized task.

Native Cursor **Stop** dispatch is separate from workflow runs and opt-in copy. The shell contract is in `ci/gate_tests/test_stop_hook_contract.py`; proving host dispatch needs a wired Cursor session (`research/SPEC_KIT_SPEC_GATES_PILOT.md`, claim card `native-stop-dispatch-unobserved`).

## Related documents

- [How to import](HOW_TO_IMPORT.md)
- [Adoption bundles](ADOPTION_BUNDLES.md)
- [Local overlay and precedence](LOCAL_OVERLAY_AND_PRECEDENCE.md)
- [QUICKGUIDE](QUICKGUIDE.md) (Recipes D/E for adoption assessment prompts)
