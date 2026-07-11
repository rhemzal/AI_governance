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

## Security finding triage (AI-assisted)

When dependency or code scans report findings, **triage before bulk upgrades**. Do not implement mass dependency bumps without classification. Corpus budget: max **3** actionable items per iteration; defer the rest to backlog with rationale.

Copy-paste prompt:

```
Load usage/SECURITY_MINIMUM_ADOPTION.md (this section + waiver guidance).

Task: Triage security scan findings. Do NOT implement mass upgrades in this step.

Findings:
<PASTE FINDING LIST — ID, severity, package/path, summary>

Requirements:
1. Risk preflight: LOW or HIGH per finding (justify). HIGH → note STOP before production changes without review.
2. Classify each finding: fix | waiver | defer | false_positive — with evidence.
3. Action budget: select max 3 items to act on this iteration; backlog the rest with one-line reason.
4. For waiver: require owner, expiration, compensating controls (see Waiver guidance above).
5. Do not weaken security gates or delete findings to make scans green.
6. Evidence output (mandatory):

### Evidence output
```text
SECURITY FINDING TRIAGE
- Scan source:
- Total findings:
- Actions this iteration (max 3):
  1) <ID> — severity — action — rationale
  2) ...
- Backlog (deferred):
- Waivers proposed (owner, expiration):
- False positives:
- Product code change warranted: yes/no (justify)
- HIGH risk / STOP: yes/no
```
```

## Related Documents
- `usage/CI_MINIMUM_ADOPTION.md`
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`
