# Full opt-in stack install (adopter template)

Operator guide for copying the **experimental** full stack: kit readopt (optional),
Superpowers + governed-work, Spec Kit preset/workflow with post-implement acceptance,
spec-gates **0.5.1**, Cursor Stop hook, and a local `specify` venv.

This material is **not** in import bundles. Copy scripts from a pinned kit checkout or
run them from `KIT_SOURCE` after authorization (ADR + overlay acceptance command).

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
specify workflow run ai-governance \
  --input spec="…" \
  --input verify="bash ci/adopter_task_acceptance_cmd.sh"
```

On headless Linux, the installer runs `agent sandbox disable` when `agent` is on PATH.

Git commits with projected hooks: `git commit -F msg.txt` (no `Co-Authored-By` trailer).

## Files produced in the host repo

| Path | Role |
| --- | --- |
| `governance/experimental/spec_gates/` | Adapter copy + `policy.adopter.json` |
| `ci/adopter_task_acceptance_cmd.sh` | Generated wrapper for `ADOPTER_VERIFY_COMMAND` |
| `ci/run_task_acceptance_check.sh` | Evidence runner (from kit) |
| `.specify/gates/` | Projected spec-gates runtime |
| `.tools/specify-venv/` | Pinned Spec Kit CLI |
| `scripts/activate-governance-specify-env.sh` | PATH helper |

## Related

- [HOW_TO_IMPORT.md](../../../usage/HOW_TO_IMPORT.md) § Opt-in work procedures
- [FOR_EXISTING_PROJECTS.md](../../../usage/FOR_EXISTING_PROJECTS.md) named downstream trial
- [README.md](./README.md) adapter details
