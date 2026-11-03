# Host checks — 2026-11-03

Cleaned record for the checks that can run on this machine. No tokens, account
mail, or raw model transcript. Disposable directories only. This is not native
stop verification and it does not promote the adapter.

## Native hooks

| Piece | Value |
| --- | --- |
| Cursor Agent CLI | `2026.10.01-e373342` |
| Running Cursor server | 3.27.22, `b1aa50cb6db84fd3e8c808259cb172ea73425c10` |
| Runs | Two `agent --print --trust --force --sandbox disabled` calls. Stdout was `DONE`. |

`.cursor/hooks.json` registered `sessionStart`, `beforeShellExecution`, and
`stop`. A Claude `Stop` command appended a line only if that host invoked it.

Observed:

- `sessionStart` ran both times. The CLI analytics event was
  `cli.hook.executed` with `hookStep` `sessionStart`, `hookSource` `project`,
  and exit 0.
- `stop` did not run. The second run used a wrapper that logs before
  `kit-verify-stop.sh`. That line was not written, and
  `stop-invocations.jsonl` was not created. The log has no `hookStep` `stop`.
- Both turns ended on the NAL loop at `interactionUpdate:turnEnded`.
- The Claude `Stop` probe did not run. Stop coexistence was not observed.

Repair budget: 2. The second run only changed the stop command so a silent
script could not hide a real invocation. There is no CLI flag in this build
that selects a local stop loop instead of NAL. Blocker: `--print` completes
the turn in the NAL client and does not invoke the local stop hook.

## Release zip

Spec Kit v1.2.5 and v1.2.6 publish no release assets. There is no Spec Kit
zip to verify. Peeled tag v1.2.5 is
`4572a67fe0e72a6837e2d7bb0fda875bc41482e5`.

spec-gates v0.5.0 `gates-0.5.0.zip`:

- sha256 `f2d6677bed7e038a95092520a03228dbde0b501b14876a582dc8f8d346787893`
- The published `.sha256` file and the sigstore bundle digest match that value.
- Certificate SAN:
  `https://github.com/schwichtgit/spec-gates/.github/workflows/release.yml@refs/tags/v0.5.0`
- Issuer: `sigstore-intermediate`.
- `cosign` 3.1.4 `verify-blob` with the upstream identity regexp and
  `https://token.actions.githubusercontent.com` printed `Verified OK`.

`specify extension add --from` does not check that signature. After the
upgrade below, the installed extension tree matched this verified zip.

There is no spec-gates release newer than v0.5.0. The version step was
0.4.2 to 0.5.0. Peeled tag v0.5.0 is
`8a5a0e8a58aa548ad3dbba6f61e772c73cde50ae`.

## Upgrade and removal

Disposable git repository, Spec Kit CLI 1.2.5 built from
`4572a67fe0e72a6837e2d7bb0fda875bc41482e5`. Policy was the 0.4.2
`policy-template.json`. This repository was not modified.

| Step | Result |
| --- | --- |
| `project.sh` for 0.4.2 | Wrote the runtime and recorded version 0.4.2. Canaries: 16 run, 13 blocked, 0 accepted, 3 skipped. Exit 1. The three skips are prettier, markdownlint, and shellcheck, which that template enables and this host does not have. Git hook probes reached the gates hooks. |
| Local edit | Appended `# LOCAL-SENTINEL` to `.specify/gates/verify.sh`. The file still parses. |
| `extension remove --keep-config`, then add the verified 0.5.0 zip | Remove exited 0. Add exited 0. `diff -rq` against the verified zip was clean. `policy.json` stayed. |
| `project.sh` with the sentinel and no decision | Exit 3. Wrote nothing. Version stayed 0.4.2. Sentinel stayed. |
| `project.sh --keep-local .specify/gates/verify.sh` | Recorded version 0.5.0. Sentinel stayed. Canaries: 18 run, 13 blocked, 2 accepted, 3 skipped. Exit 1. Accepted: the project-gate canary (`verify.sh` exit 0 at ci) and the covered-script canary. |
| `extension remove --force` | Exit 0. `.specify/extensions/gates` was removed. `.specify/gates/verify.sh` and `policy.json` remained. |
| Add 0.5.0 again and `project.sh` | Add exited 0. Project exited 3 again because the sentinel was still a local edit. |

The upgrade path keeps policy and a local runtime edit, and it refuses to
overwrite that edit until `--keep-local` or `--take-upstream`. Removal does
not delete the projected runtime. The canary suite did not pass on this host.
