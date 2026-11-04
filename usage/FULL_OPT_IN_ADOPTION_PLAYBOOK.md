# Full opt-in adoption playbook (humans + agents)

_Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance)._

This playbook is the **single end-to-end path** from zero (or legacy layout) to:

- pinned `vendor/AI_governance/` snapshot (standard + research),
- Superpowers pin + governed-work + always-on AEP Cursor rule,
- **full experimental stack**: spec-gates 0.5.1, Cursor Stop hook, Spec Kit workflow with post-implement acceptance, `specify` venv.

Normative detail stays in `usage/HOW_TO_IMPORT.md`, `governance/experimental/spec_gates/OPT_IN_STACK.md`, and `usage/FOR_EXISTING_PROJECTS.md`. **Eligibility (which repo/host/tier):** [ADOPTION_SCOPE_AND_HOSTS.md](./ADOPTION_SCOPE_AND_HOSTS.md). This document **orders** those steps and records safe defaults.

---

## For agents (execute when the operator authorized full opt-in)

**Mandate shape:** one repository, one reviewed `KIT_REVISION`, acceptance command chosen **before** install, no `true` / empty verify.

**Order (do not skip):**

1. **Prerequisites on the host:** `git`, `python3`, `jq`, `sha256sum`, `curl`, [uv](https://docs.astral.sh/uv/), **mikefarah yq** in `~/.local/bin`, `export PATH="$HOME/.local/bin:$PATH"`.
2. **Kit checkout:** `KIT_SOURCE` = clean `AI_governance` at `KIT_REVISION`; `git -C "$KIT_SOURCE" diff --exit-code HEAD --`.
3. **Snapshot:** If no `vendor/AI_governance/` → first import (`import_bundle.py` `--bundle standard --bundle research` to `vendor/AI_governance`, then `--check`). If legacy root `constitution/` or old submodule → `--readopt --previous <old-sha>` to project root, review `vendor/AI_governance.readopt-report.md`, switch `.next` → active. If snapshot exists and pin bumps → readopt + `--switch-snapshot` via installer or manual switch.
4. **Choose `ADOPTER_VERIFY_COMMAND`** (shell, real project check). Write it in `governance/LOCAL_OVERLAY.md` before stack install.
5. **Host entry:** merge `usage/templates/AGENTS_GOVERNANCE_OPT_IN_BLOCK.md` into host `AGENTS.md` (do not replace file). Ensure `.cursor/rules/autonomous-aep-execution.mdc` exists (installer copies template if missing).
6. **Stack install:**

   ```bash
   export KIT_SOURCE KIT_REVISION
   export ADOPTER_VERIFY_COMMAND='…'
   export SKIP_READOPT=1   # when snapshot already active
   bash "$KIT_SOURCE/governance/experimental/spec_gates/install-opt-in-stack.sh" --stack-only
   ```

7. **Completeness:** `bash "$KIT_SOURCE/governance/experimental/spec_gates/check-opt-in-stack.sh"` — fix every `[missing]`; accept `[gap]` only if operator declined that layer.
8. **Record:** host ADR (scope, pin, acceptance command, CM level). Do not merge/push/deploy unless authorized.

**Stop only for:** missing authorization, failed verify with exhausted repair budget, readopt report conflicts requiring human merge, or security/destructive effects outside mandate.

---

## For humans (operator checklist)

### Before you start

| Decision                                         | Record where                       |
| ------------------------------------------------ | ---------------------------------- |
| Kit pin (`KIT_REVISION` full SHA)                | ADR, `governance/LOCAL_OVERLAY.md` |
| Bundles (default **standard + research**)        | overlay                            |
| **Acceptance command** (one shell pipeline)      | overlay + `ADOPTER_VERIFY_COMMAND` |
| CI Maturity (usually **CM0** first)              | overlay                            |
| Full opt-in authorized? (spec-gates + Stop hook) | ADR                                |

**Acceptance must be real:** e.g. `timeout 600s make test`, not `true`.

### Phase map

| Phase               | You get                                        | Common mistake                                                    |
| ------------------- | ---------------------------------------------- | ----------------------------------------------------------------- |
| A — Bundle import   | `vendor/AI_governance/`                        | Importing only submodule or root `constitution/` without snapshot |
| B — Superpowers pin | `vendor/superpowers/v7.0.1/`                   | Expecting stack installer to copy pin (it does **not**)           |
| C — Host files      | `AGENTS.md`, overlay, AEP rule                 | Relying on `/governed-work` instead of always-on rule             |
| D — Stack install   | gates, Stop, workflow, venv                    | Running install without `ADOPTER_VERIFY_COMMAND`                  |
| E — Verify          | `check-opt-in-stack.sh` green on required rows | Declaring done after import only                                  |

### One-command stack refresh (after A–C)

Add `scripts/install-governance-opt-in.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
export KIT_SOURCE="${KIT_SOURCE:-$HOME/AI_governance}"
export KIT_REVISION="${KIT_REVISION:-<pin-sha>}"
export ADOPTER_VERIFY_COMMAND="${ADOPTER_VERIFY_COMMAND:-<your-cmd>}"
exec bash "$KIT_SOURCE/governance/experimental/spec_gates/install-opt-in-stack.sh" "$@"
```

Then:

```bash
source scripts/activate-governance-specify-env.sh   # after install
bash governance/experimental/spec_gates/check-opt-in-stack.sh
export TASK_ACCEPTANCE_CMD="bash ci/adopter_task_acceptance_cmd.sh"
bash .specify/gates/verify.sh --boundary git
```

### Intuitive agent UX

Phrases like “finish all open AEP items” should work **without** `/governed-work` when:

- `AGENTS.md` grants the mandate, and
- `.cursor/rules/autonomous-aep-execution.mdc` has `alwaysApply: true`.

Reload Cursor after rule changes.

### Safety

- Readopt: never delete `vendor/AI_governance` to “retry”; use `.next` + report + switch.
- Git commits with projected hooks: `git commit -F msgfile` (no `Co-Authored-By`).
- Headless Linux: installer runs `agent sandbox disable` when `agent` is on PATH.
- Partial install: run `check-opt-in-stack.sh` — see OPT_IN_STACK § Installation completeness.

### Downstream examples (dogfood)

| Repository                                        | Notes                                              |
| ------------------------------------------------- | -------------------------------------------------- |
| [mechweave](https://github.com/rhemzal/mechweave) | Full trial ADR 0023, `docs/GOVERNANCE_OPERATOR.md` |
| nvrm-ptzsim                                       | .NET `make test` acceptance                        |
| ipcsim                                            | Readopt from 873df7e; `make check-go` acceptance   |

---

## Related

- [ADOPTION_SCOPE_AND_HOSTS.md](./ADOPTION_SCOPE_AND_HOSTS.md)
- [HOW_TO_IMPORT.md](./HOW_TO_IMPORT.md)
- [FOR_EXISTING_PROJECTS.md](./FOR_EXISTING_PROJECTS.md)
- [OPT_IN_STACK.md](../governance/experimental/spec_gates/OPT_IN_STACK.md)
- Template: [AGENTS_GOVERNANCE_OPT_IN_BLOCK.md](./templates/AGENTS_GOVERNANCE_OPT_IN_BLOCK.md)
