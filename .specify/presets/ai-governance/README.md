# AI Governance Spec Kit profile

This preset is installed in this kit repository at `.specify/presets/ai-governance/`
and enabled from `.specify/presets/.registry`. It is not a Spec Kit catalog
entry and it is not part of the minimal or standard copy sets. The adopter
command in `usage/HOW_TO_IMPORT.md` copies the directory and adds the registry
entry. A copied directory with no registry entry is not applied when a valid
registry already exists.

It appends three sections to the core Spec Kit templates. It does not replace
those templates and it does not copy rules out of `constitution/`.

Do not enable the bundled Spec Kit Lean preset on this workflow. At Spec Kit
`4572a67fe0e72a6837e2d7bb0fda875bc41482e5` its five files are command
replacements, not templates. A registered command-only preset still leaves
this append on `spec-template`. The Lean specify command does not load that
template: it asks for a feature directory and writes `spec.md` directly. Its
plan, tasks, and implement commands load `.specify/memory/constitution.md`,
not `constitution/`. Compact work stays a direct edit. Lean is not a shorter
form of this profile.

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

Matched B6, B7, and B8 runs met the same acceptance with this text and without
it. None of those runs is a productivity or safety gain. Keep the three
appended sections. Do not add another section until a matched pair on a named
task class differs. The record is `research/benchmark_trials/`.
