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
2. **Entry points** — Merge the governance baseline block into existing `AGENTS.md` and add a short route to each IDE's native instruction file (for example `.github/copilot-instructions.md` for VS Code + GitHub Copilot); do not replace host files. See [IDE adapters](ADOPTION_SCOPE_AND_HOSTS.md#ide-adapters).
3. **Overlay** — Copy [LOCAL_OVERLAY_TEMPLATE.md](../governance/LOCAL_OVERLAY_TEMPLATE.md) to `governance/LOCAL_OVERLAY.md`. Declare CI Maturity (CM) and the project test command. Leave the constraints table empty until discovery writes rows.
4. **Methods** — Roll out one practice at a time ([Engineering methods adoption](ENGINEERING_METHODS_ADOPTION.md)).
5. **Optional profile** — Copy `vendor/superpowers/v7.0.2/` once and add a regular-file `governed-work` entry at each selected IDE's documented skill path (for example Cursor `.cursor/skills/` or VS Code/Copilot `.github/skills/`). Register the preset separately if Spec Kit templates should append kit mandate text.

Product tests start at CI Maturity CM1 when the project already has tests. A CM0 import does not invent them.

## Intuitive agent execution and install completeness

Importing the kit snapshot or copying `governed-work` does **not** prove that an IDE loads the skill.
For each IDE, use its documented project-level skill/instruction paths and verify activation in a
fresh session with one bounded task. For operators who already granted autonomous AEP completion
in host `AGENTS.md`:

1. For Cursor, install **`.cursor/rules/autonomous-aep-execution.mdc`** (`alwaysApply: true`) from
   [`templates/autonomous-aep-execution.mdc.template`](../governance/experimental/spec_gates/templates/autonomous-aep-execution.mdc.template)
   (the full-stack installer copies it when absent).
2. For VS Code + GitHub Copilot, merge a short route in `.github/copilot-instructions.md` to
   `.github/skills/governed-work/SKILL.md`; workspace Agent Skills are on-demand, so confirm the
   skill is actually selected in a fresh session. Do not claim Cursor Stop behavior from this route.
3. Keep the shared authorization sentence in `AGENTS.md` and ensure **`vendor/superpowers/v7.0.2/`**
   exists (procedure pin; not copied by the stack installer alone).

After any partial install, run
**[`check-opt-in-stack.sh`](../governance/experimental/spec_gates/check-opt-in-stack.sh)** and fix
reported gaps. Details: [`OPT_IN_STACK.md`](../governance/experimental/spec_gates/OPT_IN_STACK.md)
§ Intuitive agent execution and § Installation completeness; [`HOW_TO_IMPORT.md`](HOW_TO_IMPORT.md)
§ Activation.

**Named downstream example:** MechWeave documents operator practice in
`docs/GOVERNANCE_OPERATOR.md` (trial merged on `main`, workflow run `eeb22cb0`, always-on AEP rule).

## Named downstream trial (operator authorization required)

**Scope and hosts:** Before tier C (full opt-in stack), read [Adoption scope, authorization, and hosts](./ADOPTION_SCOPE_AND_HOSTS.md). Default adoption is tier A (agnostic snapshot); tier B adds procedures without spec-gates.

Do not pick or modify another person's repository without explicit approval. When authorized:

1. Record repository, revision, and one task with acceptance criteria **before** the agent starts.
2. Use [How to import](HOW_TO_IMPORT.md) and [Opt-in work procedures](HOW_TO_IMPORT.md#opt-in-work-procedures) if the trial needs the procedure pin; use [FOR_EXISTING_PROJECTS](FOR_EXISTING_PROJECTS.md) agent context for overlay rows.
3. Write outcomes to an existing ledger (`specs/<feature>/progress.md`) or the research record. Do not add a parallel procedure tree.
4. Treat a disposable fixture or gate test as structural evidence only. Claim real downstream adoption only when the named checkout completes the authorized task.

Full opt-in stack installer (experimental): [`governance/experimental/spec_gates/OPT_IN_STACK.md`](../governance/experimental/spec_gates/OPT_IN_STACK.md). End-to-end sequence: [`FULL_OPT_IN_ADOPTION_PLAYBOOK.md`](./FULL_OPT_IN_ADOPTION_PLAYBOOK.md).

When using workflow `ai-governance`, supply the task's pre-selected shell verification in
the workflow `verify` input or set `TASK_ACCEPTANCE_CMD` before calling
`bash ci/run_task_acceptance_check.sh` directly. Read `specs/<feature>/acceptance-run-evidence.md`
after the workflow's final shell step.

Native Cursor **Stop** dispatch is separate from workflow runs and opt-in copy. The shell contract is in `ci/gate_tests/test_stop_hook_contract.py`; proving host dispatch needs a wired Cursor session (`research/SPEC_KIT_SPEC_GATES_PILOT.md`, claim card `native-stop-dispatch-unobserved`). Other IDE Stop integrations are not implied and need their own adapter and evidence.

## Related documents

- [How to import](HOW_TO_IMPORT.md)
- [Adoption bundles](ADOPTION_BUNDLES.md)
- [Local overlay and precedence](LOCAL_OVERLAY_AND_PRECEDENCE.md)
- [QUICKGUIDE](QUICKGUIDE.md) (Recipes D/E for adoption assessment prompts)
