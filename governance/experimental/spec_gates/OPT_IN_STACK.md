# Full opt-in stack install (adopter template)

Operator guide for copying the **experimental** full stack: kit readopt (optional),
Superpowers + governed-work, Spec Kit preset/workflow with post-implement acceptance,
spec-gates **0.5.1**, Cursor Stop hook, and a local `specify` venv.

This material is **not** in import bundles. Copy scripts from a pinned kit checkout or
run them from `KIT_SOURCE` after authorization (ADR + overlay acceptance command).

**Before tier C:** [Adoption scope, authorization, and hosts](../../../usage/ADOPTION_SCOPE_AND_HOSTS.md).

## Before you start

1. Choose **`ADOPTER_VERIFY_COMMAND`** — the shell command that checks task acceptance
   (same string for workflow `verify` input, `TASK_ACCEPTANCE_CMD`, and spec-gates policy).
   Pick it **before** the agent runs; do not use `true` or `exit 0`.
2. Record the decision in host `governance/LOCAL_OVERLAY.md` and an ADR when scope includes
   spec-gates or Stop hooks.
3. Install host tools: Git, `curl`, `jq`, `sha256sum`, [uv](https://docs.astral.sh/uv/),
   **mikefarah** [yq](https://github.com/mikefarah/yq) in `~/.local/bin`.

Kit dogfood on this repository (no `vendor/AI_governance`):

```bash
export ADOPTER_VERIFY_COMMAND="bash ci/kit_maintenance_acceptance_cmd.sh"
export KIT_SOURCE="$(git rev-parse --show-toplevel)"
export KIT_REVISION="$(git rev-parse HEAD)"
bash governance/experimental/spec_gates/install-opt-in-stack.sh --stack-only
```

First install (no `vendor/AI_governance` yet). The default command imports
**standard** and **research**, copies the Superpowers pin with `cp -aL`, seeds
`governance/LOCAL_OVERLAY.md` and an `AGENTS.md` block only when those files are
absent, then installs the stack. It does not delete an existing snapshot.

```bash
export KIT_SOURCE=/path/to/AI_governance
export KIT_REVISION=<full-sha>
export ADOPTER_VERIFY_COMMAND="timeout 300s python -m pytest tests/your_scope -q"

bash "$KIT_SOURCE/governance/experimental/spec_gates/install-opt-in-stack.sh"
```

`--bootstrap` stops after the snapshot, pin, overlay, and `AGENTS.md` block
(no spec-gates download and no `specify` venv). Manifest conversion uses
mikefarah `yq` when it is installed, otherwise `python3-yaml`.

Adopter with existing `vendor/AI_governance` snapshot:

```bash
export KIT_SOURCE=/path/to/AI_governance
export KIT_REVISION=<full-sha>
export PREVIOUS_KIT_SHA=<previous-import-sha>
export ADOPTER_VERIFY_COMMAND="timeout 300s python -m pytest tests/your_scope -q"

bash "$KIT_SOURCE/governance/experimental/spec_gates/install-opt-in-stack.sh"
# Review vendor/AI_governance.readopt-report.md
bash "$KIT_SOURCE/governance/experimental/spec_gates/install-opt-in-stack.sh" --switch-snapshot
```

Optional: `ADOPTER_BUNDLES="standard research"` (default) for readopt when you need
`research/experiments/spec_kit_spec_gates/dependencies.txt` under vendor.

## After install

```bash
source scripts/activate-governance-specify-env.sh
export TASK_ACCEPTANCE_CMD="bash ci/adopter_task_acceptance_cmd.sh"

bash .specify/gates/verify.sh --boundary git
bash governance/experimental/spec_gates/check-opt-in-stack.sh
specify workflow run ai-governance \
  --input spec="…" \
  --input verify="bash ci/adopter_task_acceptance_cmd.sh"
```

On headless Linux, the installer runs `agent sandbox disable` when `agent` is on PATH.

Git commits with projected hooks: `git commit -F msg.txt` (no `Co-Authored-By` trailer).

### Verifying native Cursor Stop (optional)

`check-opt-in-stack.sh` reporting **Cursor Stop hook configured** only means `.cursor/hooks.json`
declares a `stop` step — not that Cursor has ever **dispatched** it during a real agent turn.

| What counts as evidence                                                                                                      | What does not                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| A new line in `.cursor/hooks/stop-invocations.jsonl` after a normal agent completion (Stop) while the recorder marker exists | Running `bash .cursor/hooks/kit-verify-stop.sh` by hand from a shell                     |
| Hooks output channel / Cursor hooks diagnostics showing the `stop` command executed                                          | `python3 -m unittest … test_stop_hook_contract` alone (contract test, not host dispatch) |
| A short note in your overlay or ops doc with host Cursor version + one pasted JSON line                                      | Harbor or `cursor agent --print` runs (they do not prove IDE Stop)                       |

**Recorder (recommended for one trial):** create an empty file
`.cursor/hooks/record-stop-invocations`. When the hook runs, the Stop script appends one JSON
object per invocation to `.cursor/hooks/stop-invocations.jsonl` (see
`.cursor/hooks/kit-verify-stop.sh`). Remove the marker when done; keep the log out of version
control or copy a row into an internal note. The kit may gitignore the live `jsonl` when present.

Use the **Cursor IDE** workspace for this check — that is where Stop hooks are expected to fire
at end-of-turn. Host behavior varies by Cursor build; see scaffold and examples in
[`research/experiments/cursor-stop/README.md`](../../../research/experiments/cursor-stop/README.md)
(also under `vendor/AI_governance/research/experiments/cursor-stop/` after bundle import).

## Intuitive agent execution (no `/governed-work` ritual)

Skills under `.cursor/skills/` are **optional** in Cursor: the model may never load
`governed-work` unless you type `/governed-work`. That feels like a second “start AEP”
step even when `AGENTS.md` already grants an autonomous mandate.

**Principle:** put the execution contract in an **always-on project rule**, not only in
a skill.

| Mechanism                                                          | Role                                                                                                         |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| `AGENTS.md` + overlay                                              | **Authority** — what the operator already authorized                                                         |
| `.cursor/rules/autonomous-aep-execution.mdc` (`alwaysApply: true`) | **Behavior** — phrases like “finish all AEP items” run inline via `executing-plans`                          |
| `.cursor/skills/governed-work/SKILL.md`                            | **Optional** routing doc; not required when the rule is present                                              |
| `vendor/superpowers/v7.0.2/`                                       | **Procedures** — `executing-plans`, TDD, debugging (installer does **not** copy this pin; see Phase B below) |

The stack installer copies
[`templates/autonomous-aep-execution.mdc.template`](./templates/autonomous-aep-execution.mdc.template)
to `.cursor/rules/autonomous-aep-execution.mdc` when that file does not exist. Customize
ledger paths and ADR references for your project, then add one sentence in `AGENTS.md`
that natural-language AEP requests are sufficient (see mechweave dogfood).

Reload the Cursor workspace after adding or changing rules.

### Cursor warning on `speckit-checklist` (5000+ tokens)

`specify init --integration cursor-agent` installs a monolithic `SKILL.md` (~22 KB) from
upstream Spec Kit. Cursor flags skills whose **SKILL.md** exceeds ~5000 tokens. The kit
ships a split skill (`SKILL.md` + `checklist-full-procedure.md`) and
`install-opt-in-stack.sh` **overlays** it after spec-gates install. Refresh an existing
repo with `--stack-only` and `SKIP_READOPT=1` / `SKIP_SPEC_GATES=1` if you only need the
skill fix, or copy the two files from `KIT_SOURCE/.cursor/skills/speckit-checklist/`.

## Installation completeness

Install phases are **not** one button unless you completed every prerequisite. Partial
install is common (readopt stopped for review, bundle imported without procedures, stack
refreshed without Superpowers pin). **`check-opt-in-stack.sh`** prints what is missing and
what will not work:

```bash
bash governance/experimental/spec_gates/check-opt-in-stack.sh
bash governance/experimental/spec_gates/check-opt-in-stack.sh --strict   # exit 1 on any gap
```

| Gap                                             | Typical symptom                                                                 |
| ----------------------------------------------- | ------------------------------------------------------------------------------- |
| No `vendor/superpowers/v7.0.2`                  | Inline AEP / `executing-plans` paths missing; governed-work points at empty pin |
| No `.cursor/rules/autonomous-aep-execution.mdc` | You must invoke `/governed-work`; “udělej AEP” behaves like normal chat         |
| No `AGENTS.md` mandate merge                    | Agent has no standing authority to run the full chain                           |
| `vendor/AI_governance.next` not switched        | Policy snapshot stale; readopt incomplete                                       |
| No `.tools/specify-venv`                        | `specify workflow run` fails                                                    |
| No projected `.specify/gates/`                  | Pre-commit / Stop verify missing                                                |
| No acceptance wrapper in `ci/`                  | Workflow `verify-acceptance` and gates `adopter-verify` fail                    |

The installer runs this check after a successful `--stack-only` / full install (non-strict).
Treat **`[missing]`** lines before expecting production-like governance UX.

### What this check does not prove

| Non-goal                                                                  | Operator mitigation                                                                                                                  |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Agent cannot run install scripts or fill gitignored dirs (e.g. `.tools/`) | Overlay + mandate; disk quotas; explicit authorization per script                                                                    |
| PyPI name collisions (e.g. unrelated `pychrono` vs Project Chrono)        | Product docs + overlay row; never `pip install` the wrong name into `.venv`                                                          |
| `vendor/AI_governance/` matches the `KIT_SOURCE` used for `--stack-only`  | Readopt and cite one SHA in overlay; run check from **vendor** copy after readopt                                                    |
| Every commit ran workflow `verify-acceptance`                             | Use workflow for gated tasks; require `bash ci/run_task_acceptance_check.sh` before push when using inline AEP                       |
| Native Stop blocked mid-session shell                                     | Documented gap; see [POST_INCIDENT_AGENT_HOST_BOUNDARY_20261105.md](../../../research/POST_INCIDENT_AGENT_HOST_BOUNDARY_20261105.md) |

When **`autonomous-aep-execution.mdc`** is present, add overlay text that **push/merge**
requires recorded acceptance (same command as `ADOPTER_VERIFY_COMMAND`), even when the
agent does not invoke `/governed-work`.

## Files produced in the host repo

| Path                                         | Role                                                          |
| -------------------------------------------- | ------------------------------------------------------------- |
| `governance/experimental/spec_gates/`        | Adapter copy + `policy.adopter.json`                          |
| `ci/adopter_task_acceptance_cmd.sh`          | Generated wrapper for `ADOPTER_VERIFY_COMMAND`                |
| `ci/run_task_acceptance_check.sh`            | Evidence runner (from kit)                                    |
| `.specify/gates/`                            | Projected spec-gates runtime                                  |
| `.tools/specify-venv/`                       | Pinned Spec Kit CLI                                           |
| `scripts/activate-governance-specify-env.sh` | PATH helper                                                   |
| `.cursor/rules/autonomous-aep-execution.mdc` | Optional alwaysApply rule (template; customize mandate paths) |

**Why so many files:** the table above is only a short list of roots; the projected spec-gates tree and kit snapshot contain **many small files** — see [Adoption footprint (file counts and impact by tier)](../../../usage/ADOPTION_REPO_FOOTPRINT.md).

## Related

- [**Full opt-in adoption playbook** (humans + agents)](../../../usage/FULL_OPT_IN_ADOPTION_PLAYBOOK.md)
- [Adoption footprint (file counts and impact by tier)](../../../usage/ADOPTION_REPO_FOOTPRINT.md)
- [HOW_TO_IMPORT.md](../../../usage/HOW_TO_IMPORT.md) § Opt-in work procedures
- [FOR_EXISTING_PROJECTS.md](../../../usage/FOR_EXISTING_PROJECTS.md) named downstream trial
- [README.md](./README.md) adapter details
