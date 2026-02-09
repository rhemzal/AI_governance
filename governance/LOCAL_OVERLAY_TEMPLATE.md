# LOCAL GOVERNANCE OVERLAY (TEMPLATE)

_This file is a template from the AI_governance kit. Copy it into your target repository as `governance/LOCAL_OVERLAY.md` and customize it. Keep a short provenance note (source repo + version/SHA) so audits can trace the baseline._

## Purpose
- Why this overlay exists (org policy, deployment constraints, tooling, risk posture).

## Scope
- What it applies to (modules, services, teams, repositories).

## Precedence
- This overlay overrides/adds to the imported kit.
- Conflicts are resolved by: overlay wins.

## Additions (Additive Rules)

### Risk Semantics (LOW vs HIGH)
- In Git workflows, most internal edits are reversible. Treat changes as **HIGH risk** primarily when they have external side effects, non-trivial blast radius, or create complexity/review explosion.
- HIGH risk is **not** triggered by the mere possibility of an incorrect internal edit.

**HIGH risk (STOP and confirm before edits)** when work involves:
- external services/integrations, registrations, credentials, billing/payment steps, or any data-handling/exfiltration risk
- public contracts/interfaces/boundaries, cross-service protocols, schema/migrations, or security-sensitive behavior
- canonical governance/gates (`constitution/`, `ci/`, `usage/`, `architecture/`, `adr/`, `interface/`)
- large cross-cutting refactors spanning multiple modules/areas (complexity/review explosion)

**LOW risk (proceed to execution)** when work stays within:
- a single module/component area
- no new dependencies
- no public contract/interface changes
- no external integrations or sensitive data handling
- changes remain reviewable (small helper/test/doc updates required by the same change are allowed)

### LOW-RISK Execution Continuity (Do Not Stall)
- If the AI has sufficient context to proceed safely, it MUST continue to execution (read/search/edit/run tests) rather than stopping after describing what it would do.
- The AI SHOULD only pause to ask questions when the task is genuinely blocked (missing credentials, missing inputs, high-risk ambiguity).

### Operator Steering (“do not stop” / “do not pause”)
- If the operator expresses general intent like “do not stop” / “do not pause”, interpret it as: continue within the current objective if safe; only stop on hard gates or if risk is HIGH/unclear after read-only discovery.
- This MUST NOT be interpreted as permission to bypass hard stops.
- If a STOP happens anyway, the AI MUST respond with:
  - the exact gate/reason (1–2 lines)
  - a minimal “unblock menu” (2–3 concrete reply options)
  - a one-line scope boundary update the operator can paste verbatim

Example “unblock menu” options:
- “Proceed, but keep scope limited to: {module/component}; no new deps; no public contract changes.”
- “Expand scope to include: {new area/files}; still no new deps; confirm?”
- “Confirm HIGH-risk change: {what}; accepted risk: {summary}; proceed.”

### LOW-RISK Scope Continuity
- Adding a small helper, test, or doc update required by the same change is not considered scope expansion.
- If scope truly expands into a new module/area, the AI must announce the expansion and update the touched-file list.

### Compliance Output Compatibility
- For low-risk work, a short compliance footer is sufficient (e.g., `## COMPLIANCE` + `Decision: PROCEED|STOP`).
- For high-risk work, the full `## COMPLIANCE REPORT` requirements apply.

### National-Language Notes Allowance
- National language is allowed in local notes areas (e.g., `notes/local/**`).
- Canonical governance documents remain English-first.

### Test Execution Path (Example)
This is a recommended addition to make test execution explicit and discoverable.

- **Test Command**: `[Specify your canonical test command here]`
  - Example: `make test` or `.venv/bin/python -m pytest` or `docker compose run --rm test`
- **Do not assume global pytest**: Always use repo-local virtual environment or make/docker workflow.
- **Preferred order**: make targets → repo-local venv → docker fallback
- **Reference**: See `usage/HOW_TO_USE_WITH_COPILOT.md` for detailed test execution guidance.

## Overrides (If Any)
Only use overrides when unavoidable.

- Override:
  - Imported rule reference (path + section)
  - Replacement text
  - Rationale
  - Risk accepted / mitigation

## Verification
- What checks prove compliance (CI gates, tests, audits)

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
If HIGH/unclear: STOP and ask for confirmation."

## Common Mistakes to Avoid
- Writing a second “rules doc” that rephrases the constitution.
- Overriding silently (no rationale, no explicit replacement).
- Mixing normative requirements into advisory notes.

## Related Documents
- `usage/HOW_TO_IMPORT.md`
- `usage/LOCAL_OVERLAY_AND_PRECEDENCE.md`
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
- `ci/ARCHITECTURE_GATES.md`
- `ci/TEST_GATES.md`
