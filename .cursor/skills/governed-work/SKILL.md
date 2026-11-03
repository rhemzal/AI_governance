---
name: governed-work
description: Use when debugging a failure, executing an already authorized plan, verifying a result, resuming interrupted work, or reviewing a change in this kit. Routes that work to pinned Superpowers procedures without making documentation edits follow test-driven development.
---

# Governed work

Use this skill before the pinned Superpowers texts. Those texts are procedures.
`constitution/AI_ENFORCEMENT.md` §§1.2–1.4 remains the authority. A skill cannot
widen the mandate, demand a commit, or replace an acceptance criterion.

The pin is Superpowers v7.0.1, commit `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`,
under `vendor/superpowers/v7.0.1/` (MIT). Active skill directories in
`.cursor/skills/` point at that pin. Hashes are `vendor/superpowers/v7.0.1/SHA256SUMS`.

## Which procedure

| Observed need | Read and follow | Skip it when |
| --- | --- | --- |
| A failure, unexpected test result, or behavior you do not yet understand | `systematic-debugging` | The edit only changes wording and nothing fails |
| Several dependent steps of an outcome the operator already authorized | `executing-plans`, including the vendored scripts it calls | The outcome itself is not authorized |
| You are about to say the work passes, is fixed, or is complete | `verification-before-completion` | Do not skip this for a behavior claim |
| A change should be read against its spec by a fresh reviewer | `requesting-code-review` and `code-reviewer.md` | There is no spec and no diff |
| A behavior change or bug fix | `test-driven-development` | The change is documentation or a registry sentence only |

`writing-plans` is the shape of an `executing-plans` plan. In this kit that
plan is the feature's Spec Kit `tasks.md`. Do not also create
`docs/superpowers/plans/`.

## Proportionality

A documentation or registry-text change does not require a red-green test.
The operator already made that exception. Do not ask again, and do not treat
the upstream "always use TDD" line as a new approval gate.

A behavior change still starts from a test you have seen fail for the
expected reason.

## Continuation and stops

An authorized mandate continues through the remaining tasks without asking
after each one. The default Spec Kit workflow's `review-spec` and `review-plan`
gates do not apply to `.specify/workflows/ai-governance/workflow.yml`.

Stop for a person only when the next action is irreversible or destructive,
security-sensitive, outside the authorized worktree (merge, push, publish,
deploy, production data, a shared device), or when every remaining path is a
guess. Those stops match Autonomous Execution Plan `approval_required`.

Do not run `finishing-a-development-branch` unless the operator asked to open
a pull request. Do not create a git worktree when the operator assigned the
current checkout. Record both as rulings in the ledger.

## Resume

The ledger is the memory. On a new session, read the ledger's plan path, then
the working tree and `git status`. A task line `Task N: complete` is done:
do not redo its edits. If a file named in the ledger has a different hash
than the recorded verification, the recorded pass is stale. Mark it stale,
rerun the command, and keep the current tree if the rerun still passes. Do
not restore an older file just to make the old hash match.

`subagent-driven-development` is not an active skill. No separate orchestrator
is added unless a later task shows that inline execution lost completed work
or kept a stale result.
