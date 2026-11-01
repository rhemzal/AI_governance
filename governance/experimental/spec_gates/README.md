# Experimental spec-gates adapter (kit repo)

Advisory integration layer evaluated in `research/SPEC_KIT_SPEC_GATES_PILOT.md` and local handoff `notes/local/spec-gates-adopter-slice/HANDOFF_4_5.md`.

## Policy source of truth

Edit **`policy.kit.json`** only. Deploy to the projected runtime with:

```bash
bash governance/experimental/spec_gates/sync-policy.sh
```

Never weaken gates in `.specify/gates/policy.json` without a human policy decision; the sync script overwrites the projected copy from this file.

## Approved checks wired today

| Gate id | Command | Matches |
| --- | --- | --- |
| `kit-gate-tests` | `timeout 120s python3 -m unittest discover -s ci/gate_tests -v` | `DEVELOPMENT.md` / `doc-hygiene` reference gate suite |

Attestation parity remains enabled; optional upstream formatters stay disabled until explicitly added to `policy.kit.json`.

## Materialize runtime (one-time)

```bash
bash governance/experimental/spec_gates/install-and-project.sh
bash governance/experimental/spec_gates/sync-policy.sh
```

Requires: Linux, Git, `uv`, Python 3.12, pinned upstream (see script headers).

## Cursor

Project hooks call the same `verify.sh --boundary agent` entrypoint. Clear stray `CLAUDE_PROJECT_DIR` / `CURSOR_PROJECT_DIR` when testing from a shell — they override the git root.

## CI

See `.github/workflows/spec-gates-kit-advisory.yml`. Promote to a required check only after native stop evidence and a negative control in GHA.

## Git hygiene

Root `.gitignore` excludes machine-local Spec Kit state (`.specify-dev/`, `feature.json`, integration packages, `.specify/memory/`). Runtime gate attestations stay out via `.specify/gates/.gitignore` (`attestations.jsonl`, `.lock/`).

**Suggested commits (review order):**

1. **Adapter** — `governance/experimental/spec_gates/**`, `.cursor/hooks.json`, `.cursor/hooks/kit-verify-stop.sh`, `.github/workflows/spec-gates-kit-advisory.yml`, `.gitignore` updates.
2. **Projected runtime** — `.specify/**`, `.claude/**`, `.cursor/skills/**` from `install-and-project.sh` (regenerate after pinned upstream bumps; do not hand-edit projected copies).

Re-run `sync-policy.sh` after changing `policy.kit.json`; never treat `.specify/gates/policy.json` as the source of truth.

**Local git hooks:** after commit 2, `project.sh` installs spec-gates into `.git/hooks/`. The commit-msg gate rejects `Co-Authored-By:` trailers (spec-gates default). Cursor may inject `Co-authored-by: Cursor …` on commit — use a one-line message via `git commit -F file` without that trailer, or `--no-verify` only when you accept skipping the git boundary for that commit.
