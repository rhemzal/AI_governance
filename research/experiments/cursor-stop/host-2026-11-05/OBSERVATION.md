# Native Stop observation — 2026-11-05

_Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance)._

Authorized experiment from the spec-gates disposition: one pass/fail observation
of native Stop on this host, plus the same acceptance through workflow, Git, and
CI where those paths already run. Harbor and `cursor-cli` are not this
observation. This file does not install a second review framework and does not
change `.cursor/hooks.json`.

## AEP

- Status: READY for the dispatch stimulus (end of the agent turn that armed the recorder).
- Objective: record whether Cursor on this host runs `.cursor/hooks/kit-verify-stop.sh` and whether that decision is allow (`{}`) or follow-up.
- Paths: this directory, `.cursor/hooks/record-stop-invocations`, `.cursor/hooks/stop-invocations.jsonl` (created only if the host runs the script).
- Expected gate decision before dispatch: allow. `verify.sh --boundary agent` exited 0 with `"failed": 0` at 2026-11-05T16:32:22Z.
- Repair budget: 1. A follow-up that reports a real gate failure may fix that failure. Do not change the gate so the stop can succeed. Do not treat a direct script call as dispatch.
- Native result: **allow**. One row, `2026-11-05T16:35:41Z`, Cursor `3.28.7`, `loop_state` `count:0`, `decision` `allow`, `verify_rc` 0, `detail` `pass`. The live log was removed after this copy. No follow-up turn ran. Fail and resume were not observed.

## Host

| Piece | Value |
| --- | --- |
| Machine | Same maintainer host used for Harbor |
| Cursor server | 3.28.7, commit `25b52e7d03ebf2d5608914158e119f7992432a30` |
| Agent host log | `local_loop`, module `c5d5bba6487d`, built 2026-11-04 |
| Kit revision | `6aa2844aa73292362cb06ee01254663877a097db` |
| spec-gates runtime | 0.5.1 |
| Policy sha256 | `8963e59e335b583230d41fd6c5aba7626ec4cea65c6d4d7739febe5f70f5d6d9` |
| Stop command | existing `.cursor/hooks.json` → `.cursor/hooks/kit-verify-stop.sh` (`timeout` 150, `loop_limit` 2) |

Earlier notes on Cursor server 3.27.22 and Agent CLI `2026.10.01-e373342` still
stand: those runs did not dispatch `stop`. This attempt uses the IDE session
on server 3.28.7. CLI output is not reused as evidence.

## Acceptance already configured

| Path | Command | Result |
| --- | --- | --- |
| Agent boundary (what Stop runs) | `bash .specify/gates/verify.sh --boundary agent --json` | exit 0, `failed` 0, `kit-gate-tests` 18s, parity pass. `verify-agent.json` |
| Git boundary | `bash .specify/gates/verify.sh --boundary git --json` | exit 0, `failed` 0, `kit-gate-tests` 17s, parity pass. `verify-git.json` |
| CI boundary | `bash .specify/gates/verify.sh --boundary ci --json` | exit 0, `failed` 0, `kit-gate-tests` 17s, parity pass. `verify-ci.json` |
| Workflow shell step | `env -u TASK_ACCEPTANCE_EVIDENCE -u TASK_ACCEPTANCE_LOG bash ci/run_task_acceptance_check.sh` (empty verify input uses `ci/kit_maintenance_acceptance_cmd.sh`) | exit 0, evidence outcome VERIFIED. `workflow-acceptance.md` |
| Installed Git hook | `bash .git/hooks/pre-commit` with an empty index | exit 0 in well under a second. The projected hook returns before `verify.sh` when nothing is staged (`.specify/gates/hooks/pre-commit`). This is not a second run of the suite. |

False product blocks on those commands: 0.

One invalid workflow run exited 1 before the clean rerun.
`TASK_ACCEPTANCE_LOG` was set in the parent environment, the acceptance
command's unittest inherited it, and
`test_success_writes_evidence_and_exits_zero` looked for `evidence.log` beside
its own evidence file. That is a harness leak, kept as
`workflow-acceptance.invalid-env.md`. It is not a gate failure and not a false
block from spec-gates.

## Resume

`usage/AI_ENGINEERING_METHODS.md` says resumed work reconciles compact task
state with the actual tree and does not replay completed effects. The observed
decision was allow, so this session was not resumed by the hook. That matches
the script's pass contract (`{}`, no new turn). The fail contract
(`followup_message` with the verifier tail) was not exercised. No product false
block occurred on the dispatched run.

## Out of scope

Concurrent uncommitted edits under `CHANGELOG.md`,
`usage/ADOPTION_SCOPE_AND_HOSTS.md`, `governance/LOCAL_OVERLAY_TEMPLATE.md`,
`governance/experimental/spec_gates/OPT_IN_STACK.md`,
`research/EXTERNAL_PROJECT_EVALUATIONS.md`, and
`research/POST_INCIDENT_AGENT_HOST_BOUNDARY_20261105.md` were already in the
worktree. They are not part of this experiment.
