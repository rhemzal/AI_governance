# AI Governance Spec Kit profile

This preset is installed in this kit repository at `.specify/presets/ai-governance/`
and enabled from `.specify/presets/.registry`. It is not a Spec Kit catalog
entry and it is not part of the minimal or standard copy sets. The adopter
command in `usage/HOW_TO_IMPORT.md` copies the directory and adds the registry
entry. A copied directory with no registry entry is not applied when a valid
registry already exists.

It appends three sections to the core Spec Kit templates. It does not replace
those templates and it does not copy rules out of `constitution/`.

Use workflow `.specify/workflows/ai-governance/workflow.yml` when the operator
has already authorized the outcome. That workflow is specify, plan, tasks,
implement, with no `review-spec` or `review-plan` gate. The bundled `speckit`
workflow still has those two gates for a mandate that is not yet given.

Continue without asking when the next edit stays inside the authorized
outcome and acceptance criteria. Stop for a person when the next action is a
new objective, an unresolved scope or authority choice, an irreversible or
destructive action, a security-sensitive action, or an effect outside the
worktree: merge, push, publish, deploy, production data, or a shared device.
A plan that cannot be executed without guessing also stops.

Routine task-to-task continuation is not one of those stops. The pinned
executor for that continuation is `.cursor/skills/governed-work/SKILL.md`.

This profile does not make a documentation edit follow test-driven development.
A behavior change still needs a test that has been seen to fail.
