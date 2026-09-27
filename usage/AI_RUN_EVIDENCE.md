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
