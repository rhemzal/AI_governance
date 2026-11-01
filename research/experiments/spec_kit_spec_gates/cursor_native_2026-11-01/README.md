# Cursor stop adapter — host notes (2026-11-01)

Cleaned record for the follow-up in `research/SPEC_KIT_SPEC_GATES_PILOT.md`.
No tokens, account mail, or raw model transcript.

## Host

| Piece | Value |
| --- | --- |
| Running Cursor server | 3.27.22, `b1aa50cb6db84fd3e8c808259cb172ea73425c10` |
| `cursor` binary on `PATH` | 3.24.12, `37b865941ccb31e2fc90c685157534efca87f960` |
| IDE agent harness | `b951911e4476`, built 2026-10-28 |
| Cursor Agent CLI | `2026.10.01-e373342` |
| OS | Linux |

## Stop contract in the running server bundle

`createBlockResponse` for the `stop` step returns `{}` and drops the hook's reason.
`DEFAULT_STOP_HOOK_LOOP_LIMIT` is 5. The skip check is `loop_count >= loop_limit`
(`loop_limit` omitted means 5; `null` means no cap). Stdout must be a JSON object.
`followup_message` is the continuation field. Exit 2 does not produce that field.
`.cursor/hooks.json` and `.claude/settings.json` `Stop` hooks are both scheduled,
in that order, and `followup_message` is last-write-wins.

The IDE harness used by this session executes a step only when
`enableExecuteHookExec` is true and `configuredSteps` contains the step.
The Agent CLI bundle has the same empty-object stop mapping and does not
reference a Claude project-hook loader.

## Dispatch attempts

Budget: 2. Both stopped without a project hook process.

1. Isolated fixture, three directories, real `verify.sh` with a fixture-text
   policy (exit 0 / 2 / 1 checked before the agent). Recording marker
   `.cursor/hooks/record-stop-invocations`. Command: `cursor agent --print
   --trust --force --sandbox disabled` in the success directory. Stdout was
   `DONE`. `stop-invocations.jsonl` stayed empty. CLI log
   `session-2026-11-01T17-01-38-771Z-591286-1.log` records
   `hooks_config_ms` 4 and then `interactionUpdate:turnEnded` on a cloud
   loop. A stdin call of the same script in that fixture did print
   `followup_message`; that call is not native dispatch.
2. Temporary `beforeShellExecution` probe in this IDE workspace, executable,
   writing `/tmp/ide-hook-seen.txt`. A Shell tool call did not create the
   file. The agent-host log for the call has `hookForcesPrompt: false` and
   no hook-firing line. The probe was deleted.

## Advisory CI

Failure, commit `135890313853e53835cf52002e1c9fff185a5a06`:

- Run: https://github.com/rhemzal/AI_governance/actions/runs/41329791882
- Job: https://github.com/rhemzal/AI_governance/actions/runs/41329791882/job/124917281691
- `verify.sh --boundary ci` printed `"failed":1` and exit 2. The gate detail
  was `intentional candidate-job rejection: advisory verify.sh must fail this run`.

The repair run is added after the commit that restores the unit-test command.
