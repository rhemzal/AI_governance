# Security Minimum Adoption (Start Small, Stay Practical)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This advisory guide mirrors the staged style of `usage/CI_MINIMUM_ADOPTION.md` for security checks.

Unless your local overlay/policy says otherwise, treat this as **recommended adoption guidance**, not a hard mandate.

## Minimum Security Adoption Levels (Suggested)

### S0: Secret scanning baseline
- Enable secret scanning in your platform/toolchain.
- Fail or block when newly introduced active secrets are detected.
- Establish a response routine (revoke/rotate/remove evidence in PR).

### S1: Dependency vulnerability scanning baseline
- Enable dependency vulnerability scanning for your package ecosystems.
- Require triage for high/critical findings.
- Use waiver/risk-acceptance only with expiration and owner.

### S2: Code scanning baseline (where available)
- Enable static/code scanning where supported by language/tools.
- Prioritize high-confidence security findings.
- For unsupported ecosystems, keep this stage advisory and document alternatives.

### S3: Governance + evidence maturity
- Track open security waivers and aging.
- Require PR evidence block for security-relevant changes.
- Review trends regularly (new findings, mean time to remediate).

## Waiver / Risk-Acceptance Guidance
When temporary exception is needed, record:
1. finding identifier and severity
2. business/technical rationale
3. compensating controls
4. owner
5. expiration date and follow-up issue

Avoid permanent waivers without periodic review.

## Related Documents
- `usage/CI_MINIMUM_ADOPTION.md`
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
