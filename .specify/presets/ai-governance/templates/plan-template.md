## Method and continuation

Record these in the existing Autonomous Execution Plan or task record. Do not
add a new form.

- **Baseline:** what fails or what evidence is missing, and on which revision.
- **Acceptance observation:** the command and result that would show the fix,
  including a known-bad case when a passing run could be misleading. On this kit repo,
  record native output from `bash ci/run_task_acceptance_check.sh` or the workflow
  `verify` input after `implement`; do not use `true` or an agent summary as the check.
- **Smallest method:** the pinned procedure from `.cursor/skills/governed-work/SKILL.md`,
  or the current check if it is enough.
- **Uncertainty:** what evidence would change that choice.

An already authorized plan does not wait for approval between tasks. Stop
only for the human decisions in the spec template's Mandate continuation
section. A documentation-only task does not require a failing test first.
