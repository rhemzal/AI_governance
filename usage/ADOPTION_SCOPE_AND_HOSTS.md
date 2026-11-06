# Adoption scope, authorization, and hosts

_Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance)._

This page answers: **where does only the agnostic kit belong**, **where may full opt-in run**, and **what authorization is required**. It does not replace `usage/HOW_TO_IMPORT.md` or `usage/FOR_EXISTING_PROJECTS.md`; it **routes** operators and agents before they pick an install mode.

---

## Is the thesis correct?

**Mostly yes**, with three important corrections:

| Claim                                                                                                 | Verdict                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Full opt-in needs explicit authorization and a chosen working mode (acceptance command, ADR, mandate) | **Yes** — not a default import.                                                                                                                                 |
| Many repos should stay on the **bundle-only, project-agnostic** baseline                              | **Yes** — `minimal` / `standard` snapshot + host `AGENTS.md` + overlay is the default path ([Adoption bundles](./ADOPTION_BUNDLES.md)).                         |
| Full opt-in is tied to **one named machine** (for example slm01)                                      | **No** — eligibility is **repository + operator authorization + host capabilities**, not a hostname allowlist. A recorded dogfood host is evidence, not policy. |
| “Basic kit” means zero Cursor or agent tooling                                                        | **No** — optional **procedure pin** (Superpowers + `governed-work`) is still agnostic relative to spec-gates; see tier table below.                             |

Agents **must not** run `install-opt-in-stack.sh`, wire Stop hooks, or treat disposable fixture runs as downstream adoption without matching authorization in this document.

---

## Three adoption tiers

| Tier                                   | What you install                                                                                                                      | Typical CI Maturity                                                 | Authorization                                                                                                                                                                                                                                                              |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A — Agnostic snapshot**              | `vendor/AI_governance/` via bundle import; host entry point + `governance/LOCAL_OVERLAY.md`; optional CM workflows from contract      | **CM0** first; product tests at **CM1** when they already exist     | Project maintainer; no cross-repo mandate                                                                                                                                                                                                                                  |
| **B — Work procedures (opt-in copy)**  | Tier A + `vendor/superpowers/v7.0.2/` + `.cursor/skills/governed-work/` + optional Spec Kit preset                                    | Same as tier A                                                      | Same; [HOW_TO_IMPORT § Opt-in work procedures](./HOW_TO_IMPORT.md#opt-in-work-procedures). **Does not** install spec-gates or Stop hook                                                                                                                                    |
| **C — Full experimental opt-in stack** | Tier A + B layers + spec-gates **0.5.1**, Cursor Stop hook, `ai-governance` workflow, post-implement acceptance, local `specify` venv | Host declares CM; acceptance command is **real** shell (not `true`) | **Named downstream trial** or equivalent host ADR **before** install ([FOR_EXISTING_PROJECTS § Named downstream trial](./FOR_EXISTING_PROJECTS.md#named-downstream-trial-operator-authorization-required), [ADR-0017](../adr/ADR_0017_Opt_In_Stack_Installer_Template.md)) |

Tier C material lives under `governance/experimental/` and is **excluded from import bundles** ([experimental spec-gates README](../governance/experimental/spec_gates/README.md), [ADR-0017](../adr/ADR_0017_Opt_In_Stack_Installer_Template.md)). Copy or invoke scripts only from a pinned `KIT_SOURCE` checkout after review.

**Middle ground:** Tier B plus always-on `.cursor/rules/autonomous-aep-execution.mdc` is common for intuitive AEP UX; that is still **not** tier C unless spec-gates, Stop hook, and workflow acceptance are authorized and installed.

**Expected repo size:** Tier A is mostly `vendor/AI_governance/` (bundle-dependent). Tier C adds spec-gates projection, hooks, and related trees — often **hundreds of tracked paths** in one adoption. That is normal, not a failed install; see [Adoption footprint (file counts and impact by tier)](./ADOPTION_REPO_FOOTPRINT.md).

---

## Repository eligibility (where tier C may run)

### Allowed when all are true

1. **Operator authorization** — written mandate: repository, kit pin (`KIT_REVISION`), one acceptance command, scope (spec-gates / Stop / workflow), and whether merge/push/deploy is in scope.
2. **Host authority** — you may change that repository’s `.cursor/`, `.specify/`, `ci/`, and `governance/` per host `AGENTS.md` and overlay.
3. **Acceptance chosen before stack install** — `ADOPTER_VERIFY_COMMAND` recorded in overlay; propagated to policy and `ci/adopter_task_acceptance_cmd.sh`.
4. **Review path** — ADR (or equivalent) for experimental stack; readopt report reviewed when bumping `vendor/AI_governance/`.

Execute tier C using [FULL_OPT_IN_ADOPTION_PLAYBOOK.md](./FULL_OPT_IN_ADOPTION_PLAYBOOK.md) and [OPT_IN_STACK.md](../governance/experimental/spec_gates/OPT_IN_STACK.md).

### Default to tier A (or B only) when any apply

| Situation                                                                   | Use                                                                                                                                                              |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Evaluation, URL assessment, Recipe D/E only                                 | Tier A; no experimental scripts                                                                                                                                  |
| Third-party or shared repo without explicit owner approval                  | Tier A only; **stop** — [FOR_EXISTING_PROJECTS](./FOR_EXISTING_PROJECTS.md)                                                                                      |
| Production runtime, customer-facing deploy hosts, CI runners without Cursor | Tier A (+ host CI); **not** tier C on that machine                                                                                                               |
| “Try governed-work” with one task                                           | Tier B + [HOW_TO_IMPORT § One live-project trial](./HOW_TO_IMPORT.md#one-live-project-trial) — **no** spec-gates, Stop, or `specify workflow run` for that trial |
| Disposable fixture / gate test workspace                                    | Structural evidence only; **not** a named downstream checkout                                                                                                    |
| Reference URL in docs without adoption mandate                              | Tier A assessment; do not install tier C “because the kit mentions a repo”                                                                                       |

Claiming downstream adoption in research or CHANGELOG requires the **named checkout** to complete the authorized task with recorded evidence — not an agent install on an unapproved repo.

---

## Host and environment (machines)

Policy is **capability-based**, not “only slm01”.

### Tier C host should have

- Git, `python3`, `jq`, `sha256sum`, `curl`, [uv](https://docs.astral.sh/uv/), **mikefarah** [yq](https://github.com/mikefarah/yq) on `PATH` (often `~/.local/bin`)
- Network to install pinned Spec Kit CLI (`specify` v1.2.5) unless you pre-seed `.tools/specify-venv/`
- **Cursor** (or compatible agent session) when validating Stop hook behavior — workflow acceptance can run headless; native Stop dispatch is a separate observation ([research/SPEC_KIT_SPEC_GATES_PILOT.md](../research/SPEC_KIT_SPEC_GATES_PILOT.md))
- Sufficient disk and time for `install-and-project.sh` (maintainer projection on kit repo; adopter copy under `governance/experimental/spec_gates/`)

The installer may run `agent sandbox disable` on headless Linux when `agent` is on PATH ([OPT_IN_STACK.md](../governance/experimental/spec_gates/OPT_IN_STACK.md)).

### Special case: this kit repository (upstream)

There is no `vendor/AI_governance/` here. Maintainers may run **`install-opt-in-stack.sh --stack-only`** with `ADOPTER_VERIFY_COMMAND=bash ci/kit_maintenance_acceptance_cmd.sh` for **dogfood** of tier C ([ADR-0017](../adr/ADR_0017_Opt_In_Stack_Installer_Template.md)). That does not authorize tier C on every adopter clone.

### Recorded dogfood (non-normative examples)

These are **documented trials**, not an exclusive allowlist:

| Host role                               | Example use                                                                             |
| --------------------------------------- | --------------------------------------------------------------------------------------- |
| Operator dev workstation                | Interactive Cursor, full stack install, workflow runs                                   |
| Headless dev server (e.g. team `slm01`) | SSH install, acceptance via `make test` / `make check-go`, push from authorized mandate |
| Laptop / igpu01                         | Kit development, CI parity tests — tier C only when mandate covers that repo            |

If tier C fails on a host (missing uv, no Cursor for Stop proof), fix prerequisites or **defer** Stop/workflow claims — do not downgrade authorization rules.

### Tier C does not contain the agent shell

Full opt-in **does not sandbox** Cursor (or other) agent runtime. Gates primarily target
**git commits**, **projected policy**, and **Spec Kit workflow** steps — not every shell
command, ignored working-tree download, or side-environment `pip` install.

| Operator assumption              | Actual kit behavior                                                                                                                     |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Green `verify.sh --boundary git` | Staged/projected checks passed; **ignored** trees (e.g. `.tools/mamba-root/`) are out of scope                                          |
| `check-opt-in-stack` OK          | Stack **files** present; **not** vendor pin freshness, PyPI homonyms, or agent discipline                                               |
| Stop hook installed              | Runs on configured **Stop**; mid-session downloads are **not** blocked by spec-gates                                                    |
| Autonomous AEP rule              | Inline completion **without** `/governed-work`; **does not** replace `verify-acceptance` unless overlay mandates acceptance before push |
| Real acceptance command wired    | Enforced when **`run_task_acceptance_check.sh`** / workflow **`verify-acceptance`** runs — **not** on every ad-hoc agent commit         |

Record host effects (multi-GB toolchains, conda, unpinned `curl | tar`) in **project overlay**
and task mandate. Maintainer post-incident notes:
[POST_INCIDENT_AGENT_HOST_BOUNDARY_20261105.md](../research/POST_INCIDENT_AGENT_HOST_BOUNDARY_20261105.md).

---

## Agent stop conditions

Stop tier C work when:

- No written authorization for that **repository** and **effects** (commit/push/merge/deploy)
- `ADOPTER_VERIFY_COMMAND` unset or placeholder
- Readopt report conflicts require human merge and operator has not decided
- Request is assessment-only or another person’s repo without approval

Continue tier A/B read-only assessment when authorized.

---

## Related documents

- [HOW_TO_IMPORT.md](./HOW_TO_IMPORT.md) — import, opt-in copy, full stack pointer
- [FOR_EXISTING_PROJECTS.md](./FOR_EXISTING_PROJECTS.md) — maintainer sequence, named downstream trial
- [FULL_OPT_IN_ADOPTION_PLAYBOOK.md](./FULL_OPT_IN_ADOPTION_PLAYBOOK.md) — ordered tier C steps
- [ADOPTION_BUNDLES.md](./ADOPTION_BUNDLES.md) — what bundles include (and exclude)
- [ADOPTION_ENFORCEMENT_CONTRACT.md](./ADOPTION_ENFORCEMENT_CONTRACT.md) — CM0–CM3 gates
- [research/EXTERNAL_PROJECT_EVALUATIONS.md](../research/EXTERNAL_PROJECT_EVALUATIONS.md) — recorded downstream outcomes
- [research/POST_INCIDENT_AGENT_HOST_BOUNDARY_20261105.md](../research/POST_INCIDENT_AGENT_HOST_BOUNDARY_20261105.md) — tier C vs agent shell (advisory)
- [ADOPTION_REPO_FOOTPRINT.md](./ADOPTION_REPO_FOOTPRINT.md) — file-count expectations and impact by tier A–C
