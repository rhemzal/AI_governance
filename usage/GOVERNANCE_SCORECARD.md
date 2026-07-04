# Governance KPI Scorecard (Recommended)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This guide provides a lightweight KPI scorecard for governance adoption and outcomes.
Use it as advisory reporting unless your local policy makes specific metrics mandatory.

## Recommended KPI Set
- `% PRs with DOC DELTA` (behavior-changing PRs)
- `% architecture-impacting PRs with ADR`
- `% PRs with AEP when required`
- CI gate pass rate by category (doc/test/boundary/interface)
- test flakiness trend (rolling window)
- median PR cycle time (open to merge)
- governance exceptions/waivers open vs closed

## Collection cadence (suggested)
- Weekly: tactical signals (gate failures, flakiness, blockers)
- Monthly: trend review (adoption, waivers, cycle time)
- Quarterly: policy/overlay adjustments based on evidence

## Copy-paste template

```markdown
## Governance Scorecard
- Period:
- Scope (repo/service/team):

### Adoption KPIs
- PRs with DOC DELTA: `x/y` (`z%`)
- Architecture-impacting PRs with ADR: `x/y` (`z%`)
- PRs with required AEP present: `x/y` (`z%`)

### Enforcement KPIs
- Doc gate pass rate: `z%`
- Deterministic test gate pass rate: `z%`
- Boundary integrity gate pass rate: `z%`
- Interface gate pass rate (if applicable): `z%`

### Outcome KPIs
- Test flakiness trend (last 30 days):
- Median PR cycle time:
- Governance waivers open/closed:

### Notes / actions
- Top failure mode:
- Next corrective action:
- Owner + due date:
```

## Related Documents
- `usage/AUDIT_PLAYBOOK.md`
- `usage/CI_MINIMUM_ADOPTION.md`
- `constitution/AI_ENFORCEMENT.md`
