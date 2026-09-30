# AI Run Evidence (Minimal Block for PRs)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

Use this guidance when PRs include AI-assisted implementation.
Keep evidence practical, high-signal, and free of secrets.

This block complements (not replaces) `### DOC DELTA`.

## Minimal evidence block (copy/paste)

```markdown
### AI RUN EVIDENCE
- Model/tooling context (high level, no secrets):
  - Assistant/tool:
  - Execution mode (interactive/agent/CI assist):
  - Key constraints/rules consulted:
- Task outcome: VERIFIED / PARTIAL / BLOCKED / CANCELLED
- Acceptance criteria: criterion → evidence / unmet reason
- Tested state:
  - Repository and exact commit(s):
  - Uncommitted diff identity (if any):
  - Environment, relevant configuration, hardware/fixture identity:
- Checks run:
  - Command/check:
  - Result:
- Artifacts/logs:
  - CI run URL:
  - Relevant job/log URL(s):
  - Local evidence (if any):
- Assumptions:
  - 
- Known limitations:
  - 
- Unverified or stale checks, and why:
- Merge/deployment authorization (separate from verification):
```

## Practical rules
- Do not include tokens, secrets, private prompts, or sensitive raw logs.
- Prefer links to CI artifacts/logs over large pasted output.
- Keep assumptions explicit so reviewers can challenge them quickly.
- Bind every check to the state it tested. A later commit, configuration change, or integration may invalidate evidence; rerun affected checks and preserve the earlier result as historical.
- Report `VERIFIED` only when all agreed acceptance criteria have supporting evidence. Missing device access or a running soak is `PARTIAL`/`BLOCKED`, not a pass.
- Capture outputs that can be independently checked. Do not rely solely on an author's self-assessment or another agent's agreement.

## Optional machine-readable test assessment

`ci/validate_test_evidence.py` is a Python standard-library reference helper, available in
the standard/full bundle through `ci/`. It assesses declared observations against a
separate expectation file. It does not run tests, inspect artifacts, authenticate reports,
grant permissions or install an adopter gate. Existing native formats remain authoritative.

A host integration resolves the expected run, tested identities and required behavior
checks independently, before execution. It normalizes native observations into the report.
Do not derive the required set from whichever tests happened to pass. Do not copy expected
identities into a report as a substitute for observing the executable and fixtures actually
used. Protect the normalizer and expected inputs through the existing review/trust boundary.

Example `expected.json` (illustrative identities, not evidence of a real run):

```json
{
  "schema_version": 1,
  "run_id": "fixture-run-1",
  "tested_state": {"source": "commit-a", "build": "binary-a", "fixture": "seek-fixture-v1", "oracle": "seek-contract-v1"},
  "required_checks": ["seek.click", "seek.frame"],
  "cleanup_required": true
}
```

Matching `report.json`:

```json
{
  "schema_version": 1,
  "run_id": "fixture-run-1",
  "tested_state": {"source": "commit-a", "build": "binary-a", "fixture": "seek-fixture-v1", "oracle": "seek-contract-v1"},
  "execution": {"status": "completed", "exit_code": 0},
  "checks": [
    {"id": "seek.click", "status": "passed", "evidence": ["native-result.json#seek.click"]},
    {"id": "seek.frame", "status": "passed", "evidence": ["native-result.json#seek.frame"]}
  ],
  "cleanup": "complete"
}
```

Schema version 1 uses exactly the fields shown in each object. Both documents have a
non-empty `run_id` and identity map `tested_state`; these must match exactly. Identity
values are opaque strings, not authenticated provenance. Use actual immutable commit,
binary, configuration, fixture and oracle identities where relevant; a supplied source
label does not establish the identity of an already-built executable.

- `required_checks`: non-empty unique check IDs, selected from the acceptance criteria.
- `cleanup_required`: boolean; the host sets it for runs that own processes/resources.
- `execution.status`: `completed`, `failed`, `timed_out` or `cancelled`.
- `execution.exit_code`: integer or null; `completed` requires an integer.
- `checks`: unique IDs with status `passed`, `failed`, `error`, `skipped` or `not_run`.
  Each has an `evidence` list of unique references; a pass requires at least one reference.
- `cleanup`: `complete`, `failed`, `unknown` or `not_required`. Required cleanup passes
  only when observed complete; an explicit cleanup failure always prevents verification.

Text values are non-empty, trimmed, at most 2048 characters and contain no control
characters below U+0020. Unresolved identity values `unknown`, `unavailable`, `tbd` and
`todo` are rejected case-insensitively. Each input is a UTF-8 JSON file of at most 1 MiB;
duplicate keys, non-finite numbers, unknown fields and malformed shapes are rejected.

From the kit root:

```bash
python3 ci/validate_test_evidence.py --expected expected.json --report report.json
timeout 60s python3 -m unittest discover -s ci/gate_tests -p 'test_test_evidence.py' -v
```

Exit **0** / `VERIFIED` means only that the supplied observations satisfy the supplied
expectations: completed execution, exit zero, all required checks passed, no reported
failure/error and applicable cleanup complete. Exit **1** reports `PARTIAL` or `CANCELLED`;
exit **2** reports `BLOCKED` for invalid/incomparable data. Optional skipped checks remain
visible. Empty execution cannot pass a non-empty required set. If adopted as a check, both
nonzero codes fail that check; the helper's verdict is not the whole task's outcome.

An invented report can still satisfy this schema. Test the native-result normalizer and
supervising runner with known-good, missing/failed/skipped, stale-result and cancellation
controls from `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`. The helper cannot prove that
a referenced artifact exists, a required assertion really ran, or a descendant stopped.

## Minimal task-state / handoff record

For long-running, resumed, or concurrent work, keep this compact record in the task's designated state location. A small task does not need a separate file. Do not edit unrelated personal notes to create one.

```markdown
### TASK STATE
- Objective and acceptance criteria:
- Mandate: allowed repositories/environments/effects; approval still required:
- Task owner; integration owner (if concurrent):
- Current branch/commit(s); uncommitted changes:
- Verified results and evidence links; stale/unverified checks:
- Open hypotheses and blockers:
- Repair budget used/remaining; last attempt and new evidence:
- Running jobs; resource/device lease owner and expiry (if applicable):
- External mutations already attempted and observed outcome:
- Next authorized action:
- Outcome: VERIFIED / PARTIAL / BLOCKED / CANCELLED
```

On resume, reconcile this record with the actual repository, jobs, and resource ownership. Do not repeat an external mutation until its outcome has been checked. On cancellation, identify pending work, release resources when authorized, and preserve the record. After parallel changes are integrated, verify the combined state.

## Device/integration example (advisory)

For a test spanning a backend, GUI, and shared embedded device, record each tested commit, deployed build/configuration, fixture or video identity, device ownership, command, and observed result. A local unit-test pass does not establish that the device scenario passed. Keep device credentials and sensitive logs out of the record.

## Related Documents
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `constitution/AI_ENFORCEMENT.md`
