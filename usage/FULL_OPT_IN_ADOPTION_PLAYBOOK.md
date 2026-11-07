# Full opt-in adoption playbook (humans + agents)

_Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance)._

This playbook is the **single end-to-end path** from zero (or legacy layout) to:

- pinned `vendor/AI_governance/` snapshot (standard + research),
- one shared Superpowers pin + a `governed-work` entry and instruction route for each selected IDE,
- **full experimental stack**: spec-gates 0.5.1, Cursor Stop and VS Code Copilot `agentStop` adapters, Spec Kit workflow with post-implement acceptance, `specify` venv.

Normative detail stays in `usage/HOW_TO_IMPORT.md`, `governance/experimental/spec_gates/OPT_IN_STACK.md`, and `usage/FOR_EXISTING_PROJECTS.md`. **Eligibility (which repo/host/tier):** [ADOPTION_SCOPE_AND_HOSTS.md](./ADOPTION_SCOPE_AND_HOSTS.md). This document **orders** those steps and records safe defaults.

---

## For agents (execute when the operator authorized full opt-in)

**Mandate shape:** one repository, one reviewed `KIT_REVISION`, acceptance command chosen **before** install, no `true` / empty verify.

**Order (do not skip):**

1. **Prerequisites on the host:** `git`, `python3`, `jq`, `sha256sum`, `curl`, [uv](https://docs.astral.sh/uv/), **mikefarah yq** in `~/.local/bin`, `export PATH="$HOME/.local/bin:$PATH"`.
2. **Kit checkout:** `KIT_SOURCE` = clean `AI_governance` at `KIT_REVISION`; `git -C "$KIT_SOURCE" diff --exit-code HEAD --`.
3. **Snapshot:** If no `vendor/AI_governance/`, run the installer with no mode flag. It performs the first import (`standard` + `research` by default), checks the copy, and copies the Superpowers pin. If a snapshot exists and the pin bumps → readopt + `--switch-snapshot`. Do not delete `vendor/AI_governance` to retry; the importer refuses an existing destination.
4. **Choose `ADOPTER_VERIFY_COMMAND`** (shell, real project check). Write it in `governance/LOCAL_OVERLAY.md` before stack install.
5. **Host entries:** merge `usage/templates/AGENTS_GOVERNANCE_OPT_IN_BLOCK.md` into host `AGENTS.md` (do not replace it), then verify the route for each IDE in use. The installer copies the VS Code Copilot skill and merges its instruction route; it also installs the Copilot `agentStop` adapter. For Cursor, the optional always-on AEP rule is `.cursor/rules/autonomous-aep-execution.mdc`. See [IDE adapters](ADOPTION_SCOPE_AND_HOSTS.md#ide-adapters). Preserve existing host instructions and inspect the install report.
6. **Stack install:**

   ```bash
   export KIT_SOURCE KIT_REVISION
   export ADOPTER_VERIFY_COMMAND='…'
   export SKIP_READOPT=1   # when snapshot already active
   bash "$KIT_SOURCE/governance/experimental/spec_gates/install-opt-in-stack.sh" --stack-only
   ```

7. **Completeness:** `bash "$KIT_SOURCE/governance/experimental/spec_gates/check-opt-in-stack.sh"` — fix every `[missing]`; accept `[gap]` only if operator declined that layer.
8. **Native Stop (host-specific):** green checks only prove configuration. To record real dispatch, follow the applicable section in [OPT_IN_STACK.md](../governance/experimental/spec_gates/OPT_IN_STACK.md): use a Cursor session for Cursor Stop, or a fresh VS Code Copilot agent session for `agentStop`. VS Code hooks are Preview. Do not infer dispatch or always-on behavior from another IDE, tests, or files on disk.
9. **Record:** host ADR (scope, pin, acceptance command, CM level). Do not merge/push/deploy unless authorized.

**Stop only for:** missing authorization, failed verify with exhausted repair budget, readopt report conflicts requiring human merge, or security/destructive effects outside mandate.

---

## For humans (operator checklist)

### Before you start

| Decision                                                  | Record where                       |
| --------------------------------------------------------- | ---------------------------------- |
| Kit pin (`KIT_REVISION` full SHA)                         | ADR, `governance/LOCAL_OVERLAY.md` |
| Bundles (default **standard + research**)                 | overlay                            |
| **Acceptance command** (one shell pipeline)               | overlay + `ADOPTER_VERIFY_COMMAND` |
| CI Maturity (usually **CM0** first)                       | overlay                            |
| Full opt-in authorized? (spec-gates + host Stop adapters) | ADR                                |

**Acceptance must be real:** e.g. `timeout 600s make test`, not `true`.

### Phase map

| Phase               | You get                                                | Common mistake                                                                   |
| ------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------- |
| A — Bundle import   | `vendor/AI_governance/`                                | Importing only submodule or root `constitution/` without snapshot                |
| B — Superpowers pin | `vendor/superpowers/v7.0.2/`                           | The installer copies the pin when that path is absent. It does not overwrite it. |
| C — Host files      | `AGENTS.md`, overlay, per-IDE instruction/skill routes | Assuming a route or always-on rule is shared by every IDE                        |
| D — Stack install   | gates, Stop, workflow, venv                            | Running install without `ADOPTER_VERIFY_COMMAND`                                 |
| E — Verify          | `check-opt-in-stack.sh` green on required rows         | Declaring done after import only                                                 |

**Large `git status` after phases A–D:** Tier C often produces **hundreds of new or changed paths** in one review pass (vendored snapshot + projected spec-gates + hooks). That is expected; see [ADOPTION_REPO_FOOTPRINT.md](./ADOPTION_REPO_FOOTPRINT.md).

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

Phrases like “finish all open AEP items” should work **without** `/governed-work` only when:

- `AGENTS.md` grants the mandate, and
- that IDE has a supported, always-on instruction route that was verified in a fresh session.

For Cursor, the documented rule is `.cursor/rules/autonomous-aep-execution.mdc` with
`alwaysApply: true`. For VS Code + Copilot, use `.github/copilot-instructions.md` to route
work to `.github/skills/governed-work/SKILL.md`; verify activation instead of assuming
that file presence is sufficient. Reload the relevant IDE after changes.

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
- [ADOPTION_REPO_FOOTPRINT.md](./ADOPTION_REPO_FOOTPRINT.md)
- [HOW_TO_IMPORT.md](./HOW_TO_IMPORT.md)
- [FOR_EXISTING_PROJECTS.md](./FOR_EXISTING_PROJECTS.md)
- [OPT_IN_STACK.md](../governance/experimental/spec_gates/OPT_IN_STACK.md)
- Template: [AGENTS_GOVERNANCE_OPT_IN_BLOCK.md](./templates/AGENTS_GOVERNANCE_OPT_IN_BLOCK.md)
