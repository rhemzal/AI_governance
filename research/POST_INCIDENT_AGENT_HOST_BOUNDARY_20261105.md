# Post-incident notes: agent host boundary vs tier C gates (2026-11-05)

_Provenance: AI_governance kit maintainer record. Case study: authorized downstream dogfood
(MechWeave) on a headless dev host; optional Project Chrono install under a repo-local
`.tools/` tree. **No operational changes** to the downstream repository are implied by this
document._

## Summary verdict

**Tier C governance (spec-gates, pre-commit, Stop hook, workflow `verify-acceptance`,
`check-opt-in-stack`) does not reliably prevent agent-driven host file effects** such as
multi-gigabyte downloads into the working tree, `pip` into a side environment, or commits
that never ran workflow acceptance in the same session.

Green **`verify.sh --boundary git`** and a passing **`check-opt-in-stack`** mean **stack
files and policy wiring look complete**, not that the agent runtime is contained.

## Observed gap (what happened)

| Event class | Kit / gate visibility | Why gates did not block |
| --- | --- | --- |
| `curl \| tar` + conda env under `.tools/` (~GB scale) | Ignored paths; not staged for commit | Pre-commit and projected verify target **git boundary**, not disk use or ignored trees |
| `pip install` into conda env (deps for probe scripts) | Outside git | No kit hook on agent shell mid-session |
| Commits on default branch with inline AEP | Pre-commit may pass | **`block_main_commits`: false** in typical adopter policy; **`verify-acceptance`** binds to **Spec Kit workflow**, not every agent commit |
| Always-on autonomous AEP rule | By design | Reduces `/governed-work` friction; increases risk of **skipping** workflow-shaped acceptance |
| PyPI package also named `pychrono` | Product code may detect `wrong_package` | Not a kit gate; **`pip install pychrono`** into project `.venv` is still an agent shell action |
| Vendor kit pin older than operator's separate kit clone | Overlay cites pin SHA | **`check-opt-in-stack` in vendor** missing until readopt; running check from **`KIT_SOURCE`** elsewhere reports OK while **vendor** is stale |

Native **Cursor Stop** on the kit host dispatched once on 2026-11-05
(`decision` allow, verifier exit 0; see
[cursor-stop/host-2026-11-05](./experiments/cursor-stop/host-2026-11-05/OBSERVATION.md)).
That allow does not block a mid-session shell or a gitignored download. This
incident matches that limit.

## What tier C still provides (do not discard)

- Refusal of **no-op** acceptance commands and wiring of a **real** `ADOPTER_VERIFY_COMMAND`
- Deterministic **post-implement** shell step when **`specify workflow run`** is used
- Git **pre-commit / commit-msg** parity with projected spec-gates
- Importer **symlink / readopt** controls (orthogonal to host conda installs)
- Structured **authorization** narrative (ADR, overlay, mandate) for operators

## Lessons for kit maintainers

1. **Label tier C honestly** — [ADOPTION_SCOPE_AND_HOSTS.md](../usage/ADOPTION_SCOPE_AND_HOSTS.md)
   and [OPT_IN_STACK.md](../governance/experimental/spec_gates/OPT_IN_STACK.md) must state
   that tier C is **commit/workflow governance**, not **agent sandboxing**.
2. **`check-opt-in-stack` scope** — Document explicit **non-goals**: Chrono/conda trees,
   PyPI homonyms, vendor pin freshness vs `KIT_SOURCE`, agent shell allowlists.
3. **Inline AEP + acceptance** — When `autonomous-aep-execution.mdc` is used, mandate
   **`run_task_acceptance_check.sh` (or equivalent) before push** in overlay; the kit cannot
   enforce Cursor session shape.
4. **Overlay template** — Extend repo-local write boundary guidance for **gitignored tool
   roots** (`.tools/`) and **install scripts that download third-party runtimes**; add
   optional constraint rows for homonymous PyPI packages when the product documents them.
5. **Pin drift** — Treat “operator ran check from `$HOME/AI_governance`” as **insufficient**
   when `vendor/AI_governance/` is the declared baseline; readopt is the fix path.
6. **Future eval** — Harbor (or similar) scenarios for “agent authorized to run install
   script?” and “commit without acceptance evidence?” grade **behavior**, not file presence.

## Related kit documents

- [ADOPTION_SCOPE_AND_HOSTS.md](../usage/ADOPTION_SCOPE_AND_HOSTS.md) — tier C limits
- [OPT_IN_STACK.md](../governance/experimental/spec_gates/OPT_IN_STACK.md) — completeness vs containment
- [LOCAL_OVERLAY_TEMPLATE.md](../governance/LOCAL_OVERLAY_TEMPLATE.md) — host write boundary
- [EXTERNAL_PROJECT_EVALUATIONS.md](./EXTERNAL_PROJECT_EVALUATIONS.md) — MechWeave downstream record

## Status

**Advisory maintainer record.** No new CI gate, pin, or constitution change is activated
by this file alone.
