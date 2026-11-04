# ADR 0017: Opt-In Stack Installer Template

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it, preserve this line._

## Status

Accepted — 2026-11-04.

## Context

Named downstream trials (for example MechWeave on branch `trial/governance-full-opt-in`)
need a repeatable way to deploy **all** opt-in layers: kit readopt, Superpowers +
governed-work, Spec Kit preset/workflow with post-implement acceptance, experimental
spec-gates, Cursor Stop hook, and a local Spec Kit CLI venv.

`usage/HOW_TO_IMPORT.md` documents manual copy blocks for procedures only. Operators
otherwise reimplemented the same sequence by hand. Policy and acceptance commands
are **host-specific**; the kit must not bake in one adopter's pytest scope or product
commands.

ADR-0016 added workflow acceptance and kit maintenance defaults. ADR-0004 keeps
spec-gates experimental and outside import bundles.

## Decision

1. Add **`governance/experimental/spec_gates/install-opt-in-stack.sh`** — parameterized
   installer driven by **`ADOPTER_VERIFY_COMMAND`**, optional readopt
   (`PREVIOUS_KIT_SHA`, `ADOPTER_BUNDLES`), and kit pin env vars.
2. Generate host files: `policy.adopter.json`, `ci/adopter_task_acceptance_cmd.sh`,
   copied adapter under `governance/experimental/spec_gates/`, and standard opt-in
   procedure paths from the pinned `KIT_SOURCE`.
3. Document operators in **`OPT_IN_STACK.md`**; link from `HOW_TO_IMPORT.md` and
   `FOR_EXISTING_PROJECTS.md`.
4. Add **`ci/gate_tests/test_install_opt_in_stack.py`** for installer syntax and
   policy shape smoke checks only (no live spec-gates install in CI).

Out of scope: mandatory adopter adoption, changing import bundles, promoting
spec-gates to required checks, or claiming downstream trial outcomes.

## Consequences

Authorized adopters can copy or invoke one script after choosing an acceptance command.
The kit dogfood repo can run `--stack-only` with `ci/kit_maintenance_acceptance_cmd.sh`.
Experimental material remains outside standard bundle copies.

## References

- `governance/experimental/spec_gates/OPT_IN_STACK.md`
- `adr/ADR_0016_Workflow_Post_Implement_Acceptance.md`
- `usage/HOW_TO_IMPORT.md` § Opt-in work procedures
