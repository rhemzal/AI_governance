# Experimental spec-gates adapter (kit repo)

Advisory integration layer evaluated in `research/SPEC_KIT_SPEC_GATES_PILOT.md` and local handoff `notes/local/spec-gates-adopter-slice/HANDOFF_4_5.md`.

## Policy source of truth

Edit **`policy.kit.json`** only. Deploy to the projected runtime with:

```bash
bash governance/experimental/spec_gates/sync-policy.sh
```

Never weaken gates in `.specify/gates/policy.json` without a human policy decision; the sync script overwrites the projected copy from this file.

## Approved checks wired today

| Gate id          | Command                                                         | Matches                                               |
| ---------------- | --------------------------------------------------------------- | ----------------------------------------------------- |
| `kit-gate-tests` | `timeout 120s python3 -m unittest discover -s ci/gate_tests -v` | `DEVELOPMENT.md` / `doc-hygiene` reference gate suite |

Attestation parity remains enabled; optional upstream formatters stay disabled until explicitly added to `policy.kit.json`.

## Materialize runtime (one-time)

```bash
bash governance/experimental/spec_gates/install-and-project.sh
bash governance/experimental/spec_gates/sync-policy.sh
```

Requires: Linux, Git, `curl`, `jq`, `uv`, Python 3.12, pinned upstream **v0.5.1** (see script headers). The script verifies the release zip checksum, runs `specify extension remove/add` from that zip (confirm the untrusted-source prompt), then `project.sh`. After install, `.specify/gates/.runtime-version` should read `0.5.1`. `.specify/gates/.upgrade-holds` records deliberate omissions of upstream `ci:canary` and `ci:pr` template steps in the advisory workflow. Qualify with `ci/gate_tests/test_spec_gates_git_environment.py` before linked-worktree Git-hook use.

## Cursor

`.cursor/hooks.json` registers a `stop` command. On Cursor IDE 3.27.22 the host continues the agent only when stdout is `{"followup_message":"..."}`. Exit code 2 does not do that: the host drops the reason and uses `{}`, so the agent is allowed to stop. The script therefore always exits 0 and emits that JSON object.

`loop_count` in stdin starts at 0. `loop_limit` 2 skips the script once that counter reaches 2, which caps automatic repair follow-ups. `stop_hook_active` is not sent by this Cursor version; the script treats it as a Claude-compatible loop guard if a caller sets it.

The script prefers `CURSOR_PROJECT_DIR`, then the git root. It unsets `CLAUDE_PROJECT_DIR` and `CURSOR_PROJECT_DIR` before `verify.sh`, because that entrypoint treats `CLAUDE_PROJECT_DIR` as the project root. Clear those variables when invoking the script from a shell that inherited another project.

A gate failure (`verify.sh` exit 2) emits `followup_message`. When `verify.sh` is missing or exits with any other code, `loop_count` 0 emits a `followup_message` that tells the agent to report the work as UNVERIFIED. A later `loop_count` allows the stop (`{}`). `stop_hook_active` still allows the stop. The notice does not prove the agent complied. `ci/gate_tests/test_stop_hook_contract.py` calls the script with a fake verifier. A direct call is not native host dispatch.

Cursor IDE 3.27.22 runs `.cursor/hooks.json` and `.claude/settings.json` `Stop` hooks in parallel. For `followup_message`, the later response wins, and the Claude project hook is later than the Cursor project hook. The projected Claude `verify-quality.sh` still uses exit 2, which this host turns into `{}` and therefore does not replace a Cursor `followup_message`. Both hooks can still run `verify.sh` on the same stop. Do not skip git hooks to avoid that overlap.

## VS Code + GitHub Copilot (Preview)

`.github/hooks/ai-governance.json` registers the `agentStop` adapter at
`.github/hooks/kit-verify-stop.py`. It runs `.specify/gates/verify.sh --boundary agent`,
blocks on a failing or unavailable verifier, and allows the stop after a successful
verification. Its input/output contract is distinct from Cursor's `stop` hook.

The VS Code hook feature is Preview. `check-opt-in-stack.sh` validates configuration and
reports whether an invocation log exists; neither that check nor
`ci/gate_tests/test_vscode_stop_hook_contract.py` proves native dispatch. Verify a fresh
Copilot agent session and correlate the Copilot Hooks output with a new line in the
optional `.github/hooks/stop-invocations.jsonl` recorder log. See
[`OPT_IN_STACK.md`](./OPT_IN_STACK.md#verifying-native-vs-code-copilot-agentstop-optional)
for the manual procedure and evidence limits.

## CI

See `.github/workflows/spec-gates-kit-advisory.yml`. It is advisory. Branch protection is unchanged.

## Git hygiene

Root `.gitignore` excludes machine-local Spec Kit state (`.specify-dev/`, `feature.json`, integration packages, `.specify/memory/`). Runtime gate attestations stay out via `.specify/gates/.gitignore` (`attestations.jsonl`, `.lock/`).

**Suggested commits (review order):**

1. **Adapters** — `governance/experimental/spec_gates/**`, `.cursor/hooks.json`, `.cursor/hooks/kit-verify-stop.sh`, `.github/hooks/ai-governance.json`, `.github/hooks/kit-verify-stop.py`, `.github/workflows/spec-gates-kit-advisory.yml`, `.gitignore` updates.
2. **Projected runtime** — `.specify/gates/**`, `.specify/extensions/gates/{extension.yml,runtime/**}`, registry, and integration manifest from `install-and-project.sh` (regenerate after pinned upstream bumps; do not hand-edit projected copies). Do not commit upstream `README.md` / `LICENSE` / `CHANGELOG.md` under the extension tree (kit link gate); they stay gitignored.

Re-run `sync-policy.sh` after changing `policy.kit.json`; never treat `.specify/gates/policy.json` as the source of truth.

**Local git hooks:** after the projected runtime is installed, `project.sh` installs spec-gates into `.git/hooks/`. The commit-msg gate rejects `Co-Authored-By:` trailers (spec-gates default). Pass a message file that does not contain that trailer (`git commit -F file`). Skipping the git hook is not the way to resolve that conflict.

## Full opt-in stack (adopter template)

For readopt + procedures + spec-gates + Stop hook + specify venv in one reviewed flow, see **[OPT_IN_STACK.md](./OPT_IN_STACK.md)** and run **`install-opt-in-stack.sh`** with host **`ADOPTER_VERIFY_COMMAND`**. After install, run **`check-opt-in-stack.sh`** for gaps. Intuitive inline AEP execution uses **`.cursor/rules/autonomous-aep-execution.mdc`** (see OPT_IN_STACK § Intuitive agent execution).
