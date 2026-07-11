# Governance Waivers (Exceptions)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This guide defines **auditable, time-boxed exceptions** when a CI gate or Required practice from `usage/ADOPTION_ENFORCEMENT_CONTRACT.md` cannot be satisfied yet.

Waivers are **not** silent rule bypass. They are recorded exceptions with owner, expiration, and compensating control.

## When a waiver is appropriate

| Situation | Example | Prefer instead |
| --- | --- | --- |
| Prerequisite missing | No test suite yet at L1 | Stay at L0; defer gate |
| Tooling not ready | Boundary lint not configured | Informational CI + waiver with fix date |
| Emergency fix | Production hotfix | Short expiration + follow-up PR |
| False positive | CI bug | Fix CI or narrow scope |

**Not appropriate:** permanent avoidance of a gate without overlay promotion or ADR.

## Required waiver fields

Every waiver MUST include:

| Field | Description |
| --- | --- |
| **Gate ID** | e.g. `T1`, `A1`, `D2`, `AEP`, `A3` (from `ci/` or contract) |
| **Owner** | Person or team accountable |
| **Expiration** | Date (ISO) — max 90 days recommended for first waiver |
| **Compensating control** | What manual check replaces automation |
| **PR/issue link** | Where waiver was recorded |

Optional: `governance-waiver` label on PR for CI advisory check (`usage/CI_STARTER_WORKFLOWS.md` §6).

## PR template block

```markdown
### Governance waiver (only if gate bypassed)
- Gate ID:
- Owner:
- Expiration: YYYY-MM-DD
- Compensating control:
- PR/issue:
```

## Overlay registry

Copy open waivers to `governance/LOCAL_OVERLAY.md` waiver registry table. Close rows when gate is wired or expiration passes.

## Review cadence

- **Weekly:** any waiver expiring within 7 days
- **Monthly:** count open waivers (`usage/GOVERNANCE_SCORECARD.md`)
- **Quarterly:** no permanent waivers without ADR + overlay update

## Security findings

Security scan waivers follow additional triage in `usage/SECURITY_MINIMUM_ADOPTION.md`. This document covers **governance gates** (doc, test, boundary, AEP, ADR).

## Related Documents

- `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- `usage/GOVERNANCE_SCORECARD.md`
- `usage/SECURITY_MINIMUM_ADOPTION.md`
- `governance/LOCAL_OVERLAY_TEMPLATE.md`
- `.github/pull_request_template.md`
