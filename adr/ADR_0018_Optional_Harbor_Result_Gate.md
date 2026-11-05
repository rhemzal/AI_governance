# ADR 0018: Optional Harbor result gate for maintainer scenarios

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status

Accepted (2026-11-05 amendments: C3/C4; H5 qualification; specs/007 workflow and overlay helper). Required kit CI still does not call Harbor on every pull request.

## Context

Experiment A recorded C1–C4 from in-session screening. A written PASS, a parsed record, or a runner exit code can look like acceptance when the trial never finished or the protected files changed. The 2026-11-05 assessment selects Harbor as an optional maintainer runner for the current Cursor host and keeps the kit's own definition of a correct result.

The stable boundary is that separation. Harbor may start an agent and store a native `result.json`. A small standard-library gate may only read those files and say whether the expected candidate matrix is complete. It must not become another agent runner or a second evidence schema.

This repository is the kit source, with maintainer doc-hygiene already in CI. Adopters do not need Harbor to import a bundle. The priorities are truthful failure, testability of hollow passes, and low maintenance cost.

## Decision

- Add `ci/check_harbor_results.py` as an optional candidate gate. It accepts a job only when every expected task has the expected number of distinct finished trials, the declared agent name and one recorded agent version, no trial or step exception, and a numeric verifier reward equal to the expected value. Missing directories, unreadable results, duplicates, unexpected tasks, blank versions, and a reward of 1 beside an exception are rejections. A file that only says PASS is an error.
- Keep C1 and C2 graders inside the Harbor task tests. Those graders hash the fixture and require the refusal or the documentation edit. They do not execute agent output.
- Ship the tasks under `research/experiments/harbor/`. They are maintainer scenarios, not a required workflow and not an adopter dependency. Promptfoo and Inspect AI stay unused for this pilot. Live `cursor-cli` comparison stays a separate paid maintainer command (see amendment).
- Do not treat final files as proof that a refusal happened before a bad diff. That timing stays unverified until a native event trace is part of the grader.

## Amendment (2026-11-05) — C3/C4 maintainer tasks

- Add Harbor tasks `c3-opt-in-copy` (+ B1 citation) and `c4-changelog-scope` (+ B1 overlay note) from `research/experiments/harbor/build_tasks.py`. C3 requires materialized `cp -aL` copy bytes and report text; explanation without copy fails. C4 requires a CHANGELOG-only edit with optional B1 `loaded-overlay.md` format compliance.
- Extend the shared grader manifest with optional `allow_symlink_paths` so a C3 fixture symlink may remain while copied bytes are hashed separately.
- Extend `expect-oracle.json` and `expect-candidate.json` to eight `ai-governance/*` package ids; maintainer jobs use `c1-c4-*` names.
- Extend `ci/gate_tests/test_harbor_graders.py` for C3/C4. Required kit CI still does not invoke Harbor on pull requests.
- Live `cursor-cli` comparison (three attempts per task) remains a separate paid maintainer command.

## Amendment (2026-11-05) — H5 cursor-cli qualification

- Record maintainer paid runs in `specs/006-harbor-scenario-backlog/progress.md`; required kit CI still does not invoke Harbor on pull requests.
- Fence C2/C4 task instructions in `build_tasks.py` so agent-facing meta lines are not copied into `/app`.
- Add maintainer job configs `job.cursor-mini.yaml`, `job.cursor-retry.yaml`, and matching `expect-candidate-*.json` files; pin `composer-2.5` on `job.cursor.yaml`.
- Add `research/experiments/harbor/merge_harbor_jobs.py` to replace failed trial directories with retry trials and write `merge-provenance.json`; the result gate still reads only trial `result.json` files and does not validate provenance.
- Add `ci/gate_tests/test_merge_harbor_jobs.py` for the merge helper against the existing gate assessor.

## Amendment (2026-11-05) — Post-qualification closure (specs/007)

- Add `.github/workflows/governance-scenarios.yml` with `workflow_dispatch` only (`oracle-nop` default; optional paid `cursor-matrix` when `CURSOR_API_KEY` is configured). Not a required pull-request gate.
- Add optional `ci/select_overlay_rows.py` and `ci/gate_tests/test_select_overlay_rows.py` to filter LOCAL_OVERLAY **Load when** rows by touched paths; the helper does not load model context.
- Document image digest capture and Cursor CLI install limits in research assessment and harbor README; publish manual scaffolds for Experiment B and native Stop under `research/experiments/fresh-context-review/` and `research/experiments/cursor-stop/`.

## Alternatives Considered

- Extend `ci/validate_test_evidence.py` with Harbor fields. That helper's schema is for declared observations, and folding Harbor's result shape into it would hide which tool produced the evidence.
- Required CI on every documentation pull request. Model runs cost money and Docker is not part of the current doc-hygiene runner.
- A custom scheduler or a second runner. The assessment already rejected that.

## Trade-Offs

The gate trusts the `result.json` bytes it is given. A person who forges a complete matrix can obtain ACCEPT without a trial. The task grader, run by Harbor in a separate verifier, is what rejects a bad workspace. The gate's job is to reject incomplete and exceptional jobs, not to re-grade files.

Separate verification sees declared `/app` artifacts, not an undeclared extra path outside that tree. The grader fails closed on unexpected files inside `/app`.

## Sensitivity Points & Risks

- Harbor's trial directory layout is the input. An extra child directory without `result.json` rejects the job. A future Harbor release that adds a bookkeeping directory needs an explicit allowlist, not a silent skip.
- `ci/` is included in import bundles, so adopters receive the script. Nothing invokes it unless they choose to. Required kit CI does not call Harbor.
- Agent version is recorded and compared inside one job. It is not an installation pin. Harbor 0.25.0 still installs the current Cursor CLI when that agent is selected.

## Points of No Return

Removing the script and `research/experiments/harbor/` restores the previous maintainer surface. Existing acceptance commands stay valid. No adopter workflow is added.

## Consequences

Maintainers can lint and run oracle/nop controls without a model call. A live Cursor comparison remains a separate, paid command using the same tasks and the same gate; maintainer qualification for that comparison is recorded in specs/006, not in required CI.

## Related Documents

- `research/EXTERNAL_PROJECT_EVALUATIONS.md`
- `research/experiments/harbor/README.md`
- `specs/006-harbor-scenario-backlog/spec.md`
- `ci/check_harbor_results.py`
- `adr/ADR_0013_Test_Evidence_And_Runner_Conformance.md`
