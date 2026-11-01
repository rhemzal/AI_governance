# Spec Kit + spec-gates pilot — 2026-11-01

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This is an advisory experiment, not an adoption decision or a new mandatory gate.
Its purpose is to determine whether upstream scaffolding and gate execution can
replace some locally maintained integration infrastructure while preserving this
kit's policy, host instructions and evidence contract.

## Outcome and replacement decision

**Overall status: PARTIAL.** The deterministic integration slice is VERIFIED in
the environment below. Native coding-agent lifecycle, execution on a CI service,
downstream usefulness and cross-version upgrades are NOT RUN. This is sufficient
to keep the candidates, not to adopt them in production or retire this kit.

The observed result is **65/65 expected observations matched**. This count includes
setup checks and **six observations of known permissive behavior**, not 65 security
guarantees. The upstream projection ran 18 canaries: 15 violations were blocked,
zero were accepted and three optional formatter/linter canaries were skipped.

| Decision | What the evidence supports |
| --- | --- |
| Keep AI_governance policy and architecture guidance | Installation preserved sentinel instructions, but no experiment established equivalent reasoning, action authority or proportional governance in either candidate. |
| Keep the existing test-evidence validator | spec-gates successfully invokes it as a named custom gate. The validator contributes rejection of stale or incomplete observations; the dispatcher does not independently supply those semantics. |
| Candidate replacement: scaffolding and instruction/skill distribution | Spec Kit initialized Claude, Codex and Cursor integrations while preserving host files in these fixtures. This can reduce custom distribution code if the native hosts load the resulting files correctly. |
| Candidate replacement: repetitive hook dispatch and projection management | spec-gates projected working Git/Claude hooks, retained existing settings, rejected a real commit and preserved local runtime edits. Reapplying the same version was idempotent. |
| Defer production activation | Native-host behavior, CI enforcement, policy ownership, actual workflow benefit and upgrade/removal recovery still require a bounded local/adopter trial. No current infrastructure is deleted or replaced by this experiment. |

This answers the testing question: a mostly documentary governance kit does not
need invented application code or a broad application test suite for a market
review. An executable-integration recommendation does need **behavioral tests of
the recommended tools**. A disposable repository containing a text-file check,
synthetic evidence records and existing validator code is sufficient for this
first slice. Real application changes belong in the later adopter trial.

## Tested inputs and environment

| Input | Exact identity / scope |
| --- | --- |
| AI_governance base | `873df7e982ed953181d6526e7866b0bd34d2fa0d` |
| Spec Kit | v1.2.5, commit `4572a67fe0e72a6837e2d7bb0fda875bc41482e5` |
| spec-gates | v0.5.0, commit `8a5a0e8a58aa548ad3dbba6f61e772c73cde50ae` |
| Host | Linux; Python 3.12.14; Git 2.51.1; jq 1.7; Bash; isolated Python environment installed with uv 0.13.4 |
| Installation | Actual Specify wheel built from the pinned source; extension installed by `specify init --extension <pinned-source>/extension`. No manual runtime transplant or upstream source patch. |
| Dependency snapshot | [dependencies.txt](experiments/spec_kit_spec_gates/dependencies.txt); transitive versions observed in this run, not an ongoing security-maintenance promise |
| Runner / evidence helper | SHA-256 values recorded in [evidence.json](experiments/spec_kit_spec_gates/evidence.json); the existing helper was copied byte-for-byte into the fixture |
| Native executables | Claude Code, Codex and Cursor were unavailable. `--ignore-agent-tools` tests scaffolding only. |

The extension's source-directory installation path was tested, not the downloaded
release ZIP, its signature, or catalog trust flow. The pinned upstream checkouts
were checked for tracked modifications before the run. Gates ran in a synthetic
Claude fixture; Codex and Cursor received scaffolding/preservation checks only.

The approved experimental policy enabled two custom checks: an actual text-file
assertion and the existing evidence validator. Optional formatting/Markdown/shell
lint and continuous specification acceptance were not enabled. Attestation and
parity checks remained enabled. Branding and protected-change-trailer preferences
were disabled in this synthetic policy; this is not a proposed downstream policy.
Upstream canaries exercise some of those features independently.

## Results and limits

All command invocations, exit codes and output are retained in
[evidence.json](experiments/spec_kit_spec_gates/evidence.json). Its `results.records`
reference transcript keys in `transcripts`. The evidence contains synthetic
fixtures, not production data. “Agent/Git/CI labels” below mean direct runtime
invocations with the corresponding boundary argument, unless an actual hook or
Git command is explicitly named.

| Check | Observed outcome | Meaning / limit |
| --- | --- | --- |
| Initialization for Claude, Codex and Cursor | Exit 0; skills exist; host `AGENTS.md`, `CLAUDE.md` and constitution preserved byte-for-byte | File generation works; no proof that a live agent loads or follows them. |
| Projection and same-version reapply | Exit 0; existing deny permission and Stop hook remain; no duplicate hooks; policy bytes preserved | Supports an adapter/distribution pilot. Not a version upgrade, uninstall or existing third-party hook-manager test. |
| Upstream canaries | 18 run: 15 blocked, 0 accepted, 3 skipped | Prettier, markdownlint and shellcheck absent and not policy-enabled. They were not counted as passing checks. |
| Correct text fixture and synthetic complete evidence | Exit 0 at all three boundary labels | A positive control for execution and schema assessment. Synthetic reports do not assert real tests happened. |
| Actual text-file assertion fails | Exit 2 at all three labels | Named command executes and its failure propagates. |
| Stale state / missing required check / incomplete required cleanup | Exit 2 at all three labels | Existing validator rejection propagates through spec-gates. Expected state was independently supplied by the fixture runner. |
| Missing executable / command exceeds gate timeout | Exit 2 at all three labels | These controls were not silently skipped or converted into success. |
| Actual Git commit | Valid fixture commits; invalid fixture commit exits 1; HEAD unchanged | Real local Git invocation reaches the projected hook. Git hooks remain locally bypassable; a separate CI boundary is still needed. |
| Direct Stop hook, first failed stop | Exit 2 | Shell-level hook contract blocks; actual host dispatch/recovery remains untested. |
| Direct Stop hook, `stop_hook_active=true` | Exit 0 despite the failing fixture | **Known limit:** loop guard allows another stop; do not equate session termination with verified completion. |
| Invalid policy | Direct CI-labelled runtime exits 1; Stop hook exits 0 with a diagnostic | **Known limit:** runtime refusal can allow the agent to stop. A failed gate and an unavailable gate are different states. |
| Missing executable runtime | Stop hook exits 0 | **Known limit:** an unprojected/broken installation does not itself block completion at this boundary. |
| Replace real check with `true`, keep invalid text fixture | Exit 0 at all three labels | **Known limit:** dispatchers and self-reported evidence cannot prove meaningful coverage or authentic execution. A trusted runner and reviewed policy are still necessary. |
| Local runtime edit | Projection check exits 3 and retains the edit | Local modifications are not silently overwritten; policy for resolving them still needs a human/adopter decision. |
| Restored inputs | All three labels return exit 0; original instruction files intact | Negative fixtures were repaired and the retained host is usable for follow-up. |

The six permissive observations above (three no-op successes and three Stop-hook
cases) match documented/implemented behavior. They are not repaired by weakening
the acceptance criteria, and they prevent a claim of universal enforcement.
Direct `--boundary ci` execution does not prove GitHub Actions is configured,
required for merging, or protected from modification.

**Repair record:** initial run had one harness error: it attempted a write through
the projected `project.sh` instead of the installed extension copy. Upstream
correctly refused with exit 2. Repair attempt 1 used the documented installed path,
retained refusal as a negative control and reran the complete fixture. The canary
assertion was also made tolerant of optional installed linters; actual skipped
counts remain recorded. No upstream code or kit validator changed. Initial results
and the refusal transcript are retained in `repair_attempts`; one of two allowed
repair attempts was used.

**Kit regression check:** `timeout 60s python3 -m unittest discover -s ci/gate_tests -v`
ran 35 tests: 33 passed, two permission-specific cases skipped because this host
runs as root. See [kit-gate-tests.txt](experiments/spec_kit_spec_gates/kit-gate-tests.txt).
An unprivileged CI runner is required to exercise those two cases. This suite
checks the existing reference gates, not native coding agents.

## Reproduce the deterministic slice

Use a Linux/WSL shell with Python 3.12, uv, Git, Bash, jq, `timeout`, `cmp` and
SHA-256 utilities. Start in an AI_governance checkout containing this report and
runner. This creates a fresh directory outside that checkout; it installs no
global tool and does not activate hooks in AI_governance or an adopter repository.
Review the pinned sources before executing their installers/hooks.

```bash
set -euo pipefail
kit_root="$(git rev-parse --show-toplevel)"
pilot_root="$(mktemp -d "${TMPDIR:-/tmp}/ai-governance-pilot.XXXXXX")"
timeout 90s git clone --depth 1 --branch v1.2.5 \
  https://github.com/github/spec-kit.git "$pilot_root/spec-kit"
timeout 90s git clone --depth 1 --branch v0.5.0 \
  https://github.com/schwichtgit/spec-gates.git "$pilot_root/spec-gates"
test "$(git -C "$pilot_root/spec-kit" rev-parse HEAD)" = \
  4572a67fe0e72a6837e2d7bb0fda875bc41482e5
test "$(git -C "$pilot_root/spec-gates" rev-parse HEAD)" = \
  8a5a0e8a58aa548ad3dbba6f61e772c73cde50ae
uv venv --python 3.12 "$pilot_root/venv"
timeout 120s uv pip install --python "$pilot_root/venv/bin/python" \
  --constraint "$kit_root/research/experiments/spec_kit_spec_gates/dependencies.txt" \
  "$pilot_root/spec-kit"
timeout 240s "$pilot_root/venv/bin/python" \
  "$kit_root/research/experiments/spec_kit_spec_gates/run.py" \
  --spec-kit-source "$pilot_root/spec-kit" \
  --spec-gates-source "$pilot_root/spec-gates" \
  --specify "$pilot_root/venv/bin/specify" \
  --output "$pilot_root/run"
```

The runner refuses an existing output directory or output inside a source
repository. It verifies source revisions, uses bounded commands, leaves raw logs,
`results.json` and synthetic repositories in `$pilot_root/run`, and exits nonzero
on unexpected observations. Optional linters on a different host can change the
canary skipped/blocked split; inspect the transcript rather than comparing only a
headline count. Release-archive verification is a separate future check.

## Local handoff: actual agent lifecycle and one adopter slice

The repository research and deterministic work can be completed remotely. The
following work belongs on the machine with the actual agent installation and its
normal project permissions. Record its product/version, OS, installed integration,
the AI_governance revision, input state and raw outputs. Do not reuse the synthetic
evidence JSON as evidence that a native agent ran tests.

### Local handoff record (Cursor, 2026-11-01)

Kit-repo follow-up on a disposable fixture and `/tmp` adopter slice. **Reviewable integration:** [PR #42](https://github.com/rhemzal/AI_governance/pull/42) (`governance/experimental/spec_gates/`). Operator notes remain in gitignored `notes/local/spec-gates-adopter-slice/`.

| Handoff step | Status | Evidence boundary |
| --- | --- | --- |
| 1 Deterministic slice | DONE | Pilot runner 65/65 (prior session) |
| 2 Native prompt (fixture) | PARTIAL | Shell + stop **script** exit 2/0; **Cursor IDE `stop` dispatch NOT RUN** |
| 3 Malformed policy + resumed | DONE (shell) | Fail-open stop vs CI `refused`; not adoption VERIFIED |
| 4 B4 adopter slice | DONE (`/tmp` only) | Baseline vs candidate `kit-gate-tests`; not merged to `main` without PR |
| 5 Adapter + CI negative | PARTIAL | `verify.sh --boundary ci` rejection observed locally; **GHA advisory job green on PR #42**; not a required check |

**Promotion:** merge of PR #42 adds an **experimental** adapter only; it does not satisfy the pilot’s native stop or required-merge CI promotion conditions by itself.

1. Reproduce the commands above. Open only
   `$pilot_root/run/workspaces/claude` in Claude Code. Put
   `$pilot_root/venv/bin` on that process's PATH. Review `.claude/settings.json`
   and confirm the native host reports the hooks as loaded. Codex/Cursor skill
   generation does **not** imply those hosts support Claude Stop hooks.
2. Give the native agent the prompt below. Capture its transcript and actual
   hook invocation, including the first failed Stop and the corrected rerun.
   Check whether the host invokes the hook at all, returns the refusal to the
   agent, runs the custom check and refrains from claiming VERIFIED prematurely.
3. Repeat with malformed policy and with a resumed session. Preserve the expected
   distinction: the host may be allowed to stop, but the work must be reported as
   unverified when the gate cannot run. A host transcript that calls this VERIFIED
   fails the adoption criterion even though the shell-level pilot matched.
4. If the synthetic native trial passes, select one small documentation change in
   an adopter, using existing benchmark scenarios B4/B6/B7. Compare the current
   setup with the candidate on matched tasks and the same host. Bind actual test
   observations to the changed revision; do not manually manufacture the report.
   Measure missed failures, false blocks, repairs, operator interruptions and
   maintenance work. Two repair attempts per failure, then retain the blocker.
5. Before activating the candidate in that adopter, prepare a reviewed adapter
   that invokes existing approved checks, defines one policy source, and projects
   an actual required CI job. Demonstrate rejection in CI, not just via its label.
   Check release ZIP provenance, third-party hook coexistence and upgrade/removal
   recovery. Return the native evidence and integration diff for a separate
   adoption decision; this research PR does not authorize a downstream rollout.

Native-agent prompt for step 2:

```text
This is a disposable governance integration fixture. Read the existing host
instructions; preserve AGENTS.md, CLAUDE.md, the constitution, gate policy and
validator. Change only fixture.txt. First put "invalid" plus a newline in it,
run the configured verification and observe the failure. Demonstrate the native
Stop hook once, if this host supports it, without claiming the task is verified.
Then repair fixture.txt to "approved" plus a newline, rerun verification, and
report the command, observed exit code and host-hook evidence. The report.json
file is explicitly synthetic and cannot be cited as proof of real test execution.
Do not commit, weaken the checks, disable hooks or edit other files. If the host
cannot demonstrate its own hook lifecycle, report that criterion as NOT RUN.
```

**Promotion condition:** adopt only the smallest layer with observed benefit and
passing native/CI negative controls; retain this kit's normative source and
evidence semantics. A full replacement or a new mandatory dependency requires a
separate decision. If the wrapper adds recurring manual repair or duplicated
policy without eliminating meaningful infrastructure, keep the current setup.

## Execution plan

```aep
{
  "schema_version": 1,
  "status": "READY",
  "objective": "Preserve the external-project investigation and run an isolated, reproducible Spec Kit + spec-gates compatibility pilot.",
  "discovery": [
    "AI_governance baseline is 873df7e982ed953181d6526e7866b0bd34d2fa0d; existing evaluations and test-evidence validator are available.",
    "Spec Kit v1.2.5 and spec-gates v0.5.0 are pinned source checkouts. Python, Bash, Git and jq are available; native Claude Code, Codex and Cursor executables are absent.",
    "LOW risk: changes are advisory research and an opt-in experiment; all hook execution is confined to disposable repositories. Canonical policy, kit CI and downstream projects are outside the change scope."
  ],
  "risk": "LOW",
  "scope": {
    "paths": ["research/EXTERNAL_PROJECT_EVALUATIONS.md", "research/SPEC_KIT_SPEC_GATES_PILOT.md", "research/experiments/spec_kit_spec_gates/**", "README.md", "CHANGELOG.md"],
    "allowed_effects": ["Create isolated temporary repositories and an isolated Python environment", "Install pinned candidate tools in that environment", "Run bounded positive and negative controls", "Edit, verify and publish a task branch and pull request"],
    "approval_required": ["Merge the pull request", "Activate hooks or change policy in a downstream project"]
  },
  "steps": [
    {"paths": ["research/EXTERNAL_PROJECT_EVALUATIONS.md"], "action": "Record the dated comparative investigation and primary sources", "reason": "Keep the assessment reviewable and available for later reevaluation"},
    {"paths": ["research/experiments/spec_kit_spec_gates/**"], "action": "Install pinned upstream tools and exercise disposable host fixtures", "reason": "Distinguish implemented behavior from documentation claims"},
    {"paths": ["research/SPEC_KIT_SPEC_GATES_PILOT.md"], "action": "Record results, limits, replacement decision and native-agent handoff", "reason": "Prevent a deterministic script test from being mistaken for downstream operational proof"},
    {"paths": ["README.md", "CHANGELOG.md"], "action": "Link the research and explain its advisory scope; verify and open a pull request", "reason": "Make the investigation discoverable without changing adoption defaults"}
  ],
  "verification": [
    {"command": "Run the experiment runner in research/experiments/spec_kit_spec_gates/ against the pinned source checkouts and isolated Specify executable", "expected": "Record installation, instruction preservation, passing/failing gate controls, failure modes and any blocked criteria"},
    {"command": "timeout 60s python3 -m unittest discover -s ci/gate_tests -v", "expected": "Existing validator regression suite passes; report any skips"},
    {"command": "git diff --check; validate the PR AEP; review local links and existing PR checks", "expected": "No whitespace errors, valid declaration and truthful evidence boundaries"}
  ],
  "acceptance": [
    "Prior investigation is preserved with dated primary-source links and differentiated evidence strength.",
    "Candidate behavior is tested where feasible without modifying upstream sources or weakening assertions.",
    "Passing, negative and unavailable native-host results are distinguished; raw reproducible evidence accompanies the report.",
    "A concrete keep/replace/defer decision and executable local handoff are recorded; no production integration is activated."
  ],
  "blocking_questions": [],
  "budget": {"max_repair_attempts": 2, "on_exhaustion": "Stop the affected experiment, retain its failure evidence and hand off the unresolved check; continue independent documentation work."},
  "doc_delta": "Extend the existing advisory evaluation record, add this focused pilot and opt-in fixtures, and link them from the README and changelog. No normative rule or mandatory gate changes."
}
```

## Related Documents

- [External project evaluations](EXTERNAL_PROJECT_EVALUATIONS.md)
- [Engineering-method evidence](AI_ENGINEERING_METHODS_EVIDENCE.md)
- [Test/run evidence contract](../usage/AI_RUN_EVIDENCE.md)
- [Matched-task benchmark scenarios](../tooling/BENCHMARK_SCENARIOS.md)
- [AEP validation](../usage/AEP_VALIDATION.md)
