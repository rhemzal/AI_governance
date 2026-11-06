# Adoption footprint: file counts and repo impact by tier

_Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance)._

Operators often see **hundreds of new or changed paths** after adoption and ask whether that is an install defect. It usually is not: **the footprint grows with the adoption tier** and with **bundle selection**. This page maps **tier → what lands in the tree → typical scale → behavioral impact**, so you can set expectations before review and commit.

**Related:** [Adoption scope, authorization, and hosts](./ADOPTION_SCOPE_AND_HOSTS.md) (tiers A–C), [Adoption bundles](./ADOPTION_BUNDLES.md) (what each bundle adds), [FULL_OPT_IN_ADOPTION_PLAYBOOK.md](./FULL_OPT_IN_ADOPTION_PLAYBOOK.md) (order of operations).

---

## Summary table (tier vs footprint vs impact)

| Tier | What you add to the project repo (high level) | Typical **tracked** file count (order of magnitude) | Main **behavioral** impact on the repo |
| --- | --- | --- | --- |
| **A — Agnostic snapshot** | `vendor/AI_governance/` from chosen bundles; host `AGENTS.md` merge; `governance/LOCAL_OVERLAY.md` | **`minimal`:** low tens of files · **`standard`:** low hundreds (often ~150–220) · **`standard` + `research`:** mid hundreds (often ~240–280) · **`full`:** largest bundle path | Agents and humans resolve kit docs under `vendor/AI_governance/`; governance text and optional CM workflows; **no** project-local spec-gates runtime |
| **B — Work procedures** | Tier A + `vendor/superpowers/v7.0.2/` + one native `governed-work` skill entry per selected IDE (+ optional Spec Kit preset if you add it separately) | Tier A **+** on the order of **tens** more (Superpowers pin + skill entries) | Procedure library for skills (e.g. executing-plans path); **still does not** install spec-gates 0.5.1 or Stop hook by itself ([HOW_TO_IMPORT § Opt-in work procedures](./HOW_TO_IMPORT.md#opt-in-work-procedures)) |
| **C — Full experimental opt-in stack** | Tier A + B layers + `governance/experimental/spec_gates/` adapter, **projected** `.specify/gates/`, Cursor Stop hook files, `ai-governance` workflow bits, `ci/*` wrappers, `.cursor/rules/` (e.g. autonomous AEP), local `specify` venv under **`.tools/specify-venv/`** | Often **~400–550+ tracked files** in one adoption commit (varies with bundle size and upstream spec-gates projection). Example shape: ~250–270 under `vendor/AI_governance/` (`standard` + `research`), ~20 under `vendor/superpowers/`, ~140–170 under `.specify/`, small trees under `.cursor/`, `.claude/` (hooks merged from projection), plus a few `ci/` / `governance/experimental/` / `scripts/` | **Git and agent stops** can invoke `verify.sh` and your **adopter acceptance** command; Spec Kit workflow `verify-acceptance`; **largest** review surface and ongoing merge cost when bumping pins |

Counts are **illustrative**: run `git status` / `git ls-files` after install on your host; exact numbers follow bundle lines and spec-gates release layout.

The `.cursor/skills/governed-work/` path in the Tier B row is the Cursor example.
VS Code + Copilot uses `.github/skills/governed-work/`; add one entry per IDE while
sharing the same pin. Tier C's documented native Stop integration is Cursor-specific.

---

## Why Tier C inflates the diff (expected layout)

Full opt-in is designed to be **reproducible**: the project keeps a **pinned policy snapshot**, a **pinned procedure pin**, and a **vendored spec-gates runtime** (projected under `.specify/gates/`). That necessarily adds many small files (shell helpers, JSON schema, hooks).

Rough **components** (not additive strict sums — overlap is path-level):

| Area | Role | Typical scale |
| --- | --- | --- |
| `vendor/AI_governance/` | Imported kit snapshot ([bundles](./ADOPTION_BUNDLES.md)) | **`standard`:** ~150–220 files · **`research`:** adds ~80–110 more (often required for Tier C `dependencies.txt` used by the `specify` venv constraint) |
| `vendor/superpowers/v7.0.2/` | Pinned Superpowers tree | ~20–25 files |
| `.specify/gates/` and related | Projected spec-gates **0.5.1** runtime + hooks installed into `.git/hooks/` | Often **~140–180** tracked files under `.specify/` (varies by upstream) |
| `.cursor/` | Stop hook, `hooks.json`, rules, skills overlays | Often ~20–35 files |
| `.claude/` | Merged agent hooks from projection | Often single-digit to low tens |
| `governance/experimental/spec_gates/` | Adapter scripts + `policy.adopter.json` | Often ~10–20 files |
| `ci/` | `adopter_task_acceptance_cmd.sh`, `run_task_acceptance_check.sh`, helpers | Few files |

**Local tool root:** `.tools/specify-venv/` holds the pinned Spec Kit CLI. It is **many files** and may appear in `git status` unless the host adds `.tools/` to `.gitignore`; the stack check expects that venv to exist for `specify workflow run` ([OPT_IN_STACK.md](../governance/experimental/spec_gates/OPT_IN_STACK.md)). Teams that gitignore it trade a smaller repo for a **per-clone** install step.

---

## Impact classes (what actually “governs” behavior)

Use this when reviewing a large diff:

1. **Policy and enforcement (high)** — `.specify/gates/policy.json`, git hooks, `verify.sh`, Stop hook, `ci/adopter_task_acceptance_cmd.sh`. These tie **commits and stop events** to your `ADOPTER_VERIFY_COMMAND`.
2. **Pin and reproducibility (high for maintenance)** — `vendor/AI_governance/` and `vendor/superpowers/`; bump via readopt / reviewed pin changes.
3. **Agent UX (medium)** — `.cursor/rules/*.mdc`, skills; affects defaults, not CI, unless you wire them that way.
4. **Documentation-only under vendor (lower merge conflict risk)** — most of `vendor/AI_governance/` is **reference text**; day-to-day product conflicts are less common than with application code, but **snapshot bumps** still need review.

---

## Reducing footprint (without calling Tier C a bug)

- **Prefer Tier A or B** if you do not need spec-gates + Stop + workflow acceptance on every host ([ADOPTION_SCOPE_AND_HOSTS.md](./ADOPTION_SCOPE_AND_HOSTS.md)).
- **Shrink Tier A** by choosing **`minimal`** or **`standard`** only; add **`research`** when you need that bundle’s paths or when Tier C’s constraint file must live in the snapshot ([ADOPTION_BUNDLES.md](./ADOPTION_BUNDLES.md)).
- **After Tier C**, if `.tools/specify-venv/` should not be tracked, add `.tools/` to `.gitignore` and document the **local** `uv` / reinstall step in `DEVELOPMENT.md` or overlay (trade-off: clones are not self-contained for `specify` until that step runs).

---

## Related

- [OPT_IN_STACK.md § Files produced in the host repo](../governance/experimental/spec_gates/OPT_IN_STACK.md#files-produced-in-the-host-repo)
- [OPT_IN_STACK.md § Installation completeness](../governance/experimental/spec_gates/OPT_IN_STACK.md#installation-completeness) (`check-opt-in-stack.sh` gaps)
- [ADR-0017](../adr/ADR_0017_Opt_In_Stack_Installer_Template.md) — opt-in installer template and scope
