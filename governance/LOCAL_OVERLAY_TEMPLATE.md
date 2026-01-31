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

### LOW-RISK Execution Continuity (Do Not Stall)
- If the AI has sufficient context to proceed safely, it MUST continue to execution (read/search/edit/run tests) rather than stopping after describing what it would do.
- The AI SHOULD only pause to ask questions when the task is genuinely blocked (missing credentials, missing inputs, high-risk ambiguity).

### LOW-RISK Scope Continuity
- Adding a small helper, test, or doc update required by the same change is not considered scope expansion.
- If scope truly expands into a new module/area, the AI must announce the expansion and update the touched-file list.

### Compliance Output Compatibility
- For low-risk work, a short compliance footer is sufficient (e.g., `## COMPLIANCE` + `Decision: PROCEED|STOP`).
- For high-risk work, the full `## COMPLIANCE REPORT` requirements apply.

### National-Language Notes Allowance
- National language is allowed in local notes areas (e.g., `notes/local/**`).
- Canonical governance documents remain English-first.

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
Keep this prompt as a single source of truth and link to it (avoid duplication):
- `usage/RISK_PREFLIGHT_PROMPT.md`

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
