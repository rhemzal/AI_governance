# LOCAL GOVERNANCE OVERLAY (TEMPLATE)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). Copy it into your target repository as `governance/LOCAL_OVERLAY.md` and customize it. Keep this line to preserve traceability._

## Purpose
- Why this overlay exists (org policy, deployment constraints, tooling, risk posture).

## Scope
- What it applies to (modules, services, teams, repositories).

## Precedence
- This overlay overrides/adds to the imported kit.
- Conflicts are resolved by: overlay wins.

## Additions (Additive Rules)

### Task Mandate and Planning

Follow `constitution/AI_ENFORCEMENT.md` §§1.1–1.4; do not duplicate or contradict its stop/repair rules here.

Record per non-trivial task (in the task record or AEP):
- Outcome and independently checkable acceptance criteria.
- Authorized repositories, branches, environments, tools, and effects.
- Actions requiring separate approval (for example merge, deploy, publish, or shared-device mutation), and any approval already granted for those exact actions/targets.
- Known affected paths, bounded discovery steps, verification commands, and plan changes.
- Repair-attempt budget and what to report on exhaustion; cost/runtime limits when relevant.
- Task-state location, resource owner, and integration owner when work is handed off or concurrent.

AEP is required for HIGH-risk work, dependent non-trivial steps, handoff, or concurrency. Routine reversible work may use a concise scope and verification statement. The structured PR form is in `usage/AEP_VALIDATION.md`.

### Risk and Authority

HIGH risk includes public contracts, architecture boundaries, migrations, security behavior, canonical governance/gates, and significant external effects. It requires proportionate verification and ADR consideration. It does not require asking again for actions already authorized.

Supporting helpers/tests/docs within the same mandate are permitted; update the affected-file list. Obtain approval before a new objective or an effect outside the mandate. Preparing an isolated patch does not authorize applying a migration or deploying it.

### Failure, Resume, and Handoff

- Use the bounded AVR loop on ordinary verification failures. Preserve evidence and replan when an assumption is falsified.
- Stop the affected action on missing authorization, unavailable required inputs, a hard-boundary conflict, or exhausted repair budget. State the blocker and smallest next decision; continue independent authorized work.
- On resume, check actual revisions, uncommitted changes, running jobs, and held resources. Reconcile already-applied external effects before retrying.
- Use isolated working copies or explicit non-overlapping ownership for concurrent writers. Name an integration owner and rerun affected checks after integration.
- Report task outcome `VERIFIED`, `PARTIAL`, `BLOCKED`, or `CANCELLED`, with evidence tied to revisions/environment (`usage/AI_RUN_EVIDENCE.md`).

### Operator Steering

“Continue” or “do not stop” means continue within the existing mandate. It does not expand tool permissions or authorize a new external effect. Prior explicit approval covering an action remains valid; ask only for the missing decision.

### Compliance Output Compatibility
- For low-risk work, a short compliance footer is sufficient (e.g., `## COMPLIANCE` + `Decision: PROCEED|STOP`).
- For high-risk work, the full `## COMPLIANCE REPORT` requirements apply.

### National-Language Notes Allowance
- National language is allowed in local notes areas (e.g., `notes/local/**`).
- Canonical governance documents remain English-first.

## Verification
- What checks prove compliance (CI gates, tests, audits)

## Enforcement maturity (declare after import)

Record the active **CI Maturity (CM)** level for this repository. Defaults per bundle: `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`. **Governance Level (G)** is assessed per task — see `constitution/ADAPTIVE_GOVERNANCE.md`.

- **CM level**: `CM0` | `CM1` | `CM2` | `CM3`
- **Declared**: `YYYY-MM-DD`
- **Next review**: `YYYY-MM-DD`
- **Bundle baseline**: `minimal` | `standard` (+ optional: `architecture` | `research`)

### Required gates (check when active at this CM level)

Copy the row for your CM level from `usage/ADOPTION_ENFORCEMENT_CONTRACT.md` and mark CI job or review habit when wired:

```markdown
- [ ] CM0 doc hygiene (D3, manifest, provenance, bundled cross-refs)
- [ ] CM1 deterministic tests (T1) — job: ___
- [ ] CM1 canonical test command documented below
- [ ] CM2 DOC DELTA on behavior-changing PRs
- [ ] CM2 boundary integrity (A1) when tooling exists — job: ___
- [ ] CM3 ADR on governance paths — job: ___
```

### Canonical test command (required from CM1)

- **Command**: `[Specify your canonical test command here]`
  - Example: `make test` or `.venv/bin/python -m pytest` or `docker compose run --rm test`
- **Do not assume global pytest**: Always use repo-local virtual environment or make/docker workflow.
- **Preferred order**: make targets → repo-local venv → docker fallback
- **Reference**: See `usage/HOW_TO_USE_WITH_COPILOT.md` and `DEVELOPMENT.md`.

### Waiver registry

Temporary gate exceptions must follow `usage/GOVERNANCE_WAIVERS.md`. Track open waivers here:

| Gate ID | Owner | Expiration | PR/issue | Compensating control | Status |
| --- | --- | --- | --- | --- | --- |
| | | | | | open / closed |

### Filesystem Write Boundary (Repo-Local Writes Only)
- AI MUST treat the repository working tree as the default writable boundary.
- AI MUST prefer repo-local paths for any generated files, caches, logs, artifacts, or intermediate outputs.
- AI MUST NOT write outside the repository (e.g. `/tmp`, home directory, parent directories, arbitrary absolute external paths) unless the operator explicitly requests it.
- If a command or tool would write outside the repo by default, the AI MUST redirect it to a repo-local path when feasible.
- If such redirection is not feasible, the AI MUST STOP and request confirmation.
- Recommended repo-local scratch directories: `.tmp/`, `tmp/`, `.artifacts/`, `.cache/` (follow repo convention; ephemeral outputs should be gitignored).

### AI productivity calibration (optional)

Declare when using `usage/AI_PRODUCTIVITY_CALIBRATION.md`:

```markdown
- **Calibration phase:** Phase 0 | Phase 1 | Phase 2 | Phase 3
- **Declared:** YYYY-MM-DD
- **Local ledger:** notes/local/ai-productivity/ledger.md (gitignored; copy from usage/templates/AI_PRODUCTIVITY_LEDGER.template.md)
- **Team summary (optional):** governance/AI_CALIBRATION_SUMMARY.md (aggregates only; copy from governance/AI_CALIBRATION_SUMMARY.template.md)
- **Min sample before class-specific ranges:** N ≥ 10 per task_class
```

Promote Phase 0–1 “no calendar ETA” to required here if your team wants strict enforcement.

## Overrides (If Any)
Only use overrides when unavoidable.

- Override:
  - Imported rule reference (path + section)
  - Replacement text
  - Rationale
  - Risk accepted / mitigation

## Change Control
- Changes to this overlay require an ADR (recommended) when they affect boundaries/contracts or enforcement.

Recommended ADR trigger examples:
- you weaken or change enforcement evidence requirements
- you change architectural boundary expectations
- you introduce exceptions to non-interactive execution/time limits

## User Prompt (Copy/Paste): Quick LOW vs HIGH Risk Check
"Do a risk preflight before changes:
- List exact files you will touch
- Confirm whether any boundary contract/interface, adapter/integration, architecture decision, security behavior, CI/gates, or canonical governance docs are affected
Return: `Risk: LOW|HIGH` + 1–2 sentence justification.
If LOW: proceed to execution.
If HIGH: use proportionate verification and check the existing mandate. Continue authorized preparation; ask only before an unauthorized effect or when a genuinely blocking ambiguity remains."

## Common Mistakes to Avoid
- Writing a second “rules doc” that rephrases the constitution.
- Overriding silently (no rationale, no explicit replacement).
- Mixing normative requirements into advisory notes.

## Related Documents
- `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- `usage/GOVERNANCE_WAIVERS.md`
- `usage/HOW_TO_IMPORT.md`
- `usage/LOCAL_OVERLAY_AND_PRECEDENCE.md`
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
- `ci/ARCHITECTURE_GATES.md`
- `ci/TEST_GATES.md`
