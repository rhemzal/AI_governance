# ADR 0012: Outcome-Based Engineering Method Adoption

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If copied, preserve this line._

## Status

Proposed — acceptance is the maintainer's merge decision.

## Context

PR #38 introduced six advisory method guides without changing task behavior or providing
an adoption path for pinned legacy repositories. A method catalog can remain unused;
mandating every tool would increase cost and couple governance to changing agent capabilities.
The evidence review distinguishes empirical findings from vendor cases and does not establish
a universal productivity improvement for any complete workflow.

This is a G2-sized kit change under existing maintainer CI. It supports existing projects
without activating downstream controls or creating a new maturity model.

## Decision

1. Add one proportionate behavioral obligation in AI_RULES §6.5: non-trivial work records
   baseline/gap, acceptance observation, smallest sufficient method and decision-relevant
   uncertainty in existing AEP/task evidence. No new schema or standalone report is required.
2. Include the concise method selector and rollout guide in minimal. Keep focused guides,
   tools and research optional according to selection; preserve host instructions and pins.
3. Pilot one useful outcome on one slice, then optionally promote it in the existing overlay
   with a host verification command, evidence, owner and review trigger. Use existing G/CM,
   waiver, verification and authority mechanisms. Allow justified retirement of scaffolding.
4. Supply one optional Python standard-library comparator for successful, revision-bound
   finding sets. Reuse native scanner baseline support first. The comparator has no scanner,
   command executor, updater, baseline writer, plugin system or automatic CI installation.
   Its tests join the kit's existing doc-hygiene workflow; no new adopter gate is mandated.

## Alternatives Considered

- **Documentation-only catalog:** lowest maintenance, but does not address activation,
  legacy upgrade, verification or the distinction between method use and useful outcomes.
- **Mandatory full harness / method-compliance platform:** central visibility and uniformity,
  but poor proportionality, duplicate evidence and model/tool lock-in. Rejected.
- **Immediately fail all historic findings:** simple, but can freeze unrelated development
  and encourage disabling checks. Use where already required; permit scoped migration only
  with the existing policy/waiver authority.
- **Compare finding counts:** cheap, but one resolved defect can conceal a new defect.
  Compare stable identities instead; require identical scope and scanner contracts.
- **Advisory selector only in standard:** keeps minimal smaller, but misses the old/small
  projects this change is intended to help. Add two documents, not the research corpus.

## Trade-Offs

- A small behavioral obligation makes method choice reviewable without forcing technology.
- Two extra minimal documents increase import size; agents consult selected sections only.
- The comparator adds a small maintained contract and tests. Host scanners remain host-owned.
- A baseline permits declared historical debt, not a claim of cleanliness or a policy waiver.

## Sensitivity Points & Risks

- A generated test may share the implementation's mistake: use independent expectations
  and selective good/bad controls. Passing declarations cannot establish semantic quality.
- Finding identity must distinguish violations but avoid incidental line shifts. The host
  owns this trade-off; normalizer/rule/scope changes trigger explicit rebaselining review.
- A fake empty report or candidate-edited baseline defeats comparison. Obtain reports from
  trusted clean revisions and protect the comparator and scanner/configuration through existing review/CI.
- A fixed historical baseline can allow resolved debt back in: recompute from the trusted
  target revision or deliberately advance the reviewed baseline after merge.
- Local commands/hooks are not guaranteed execution. Binding to required CI/merge status
  is a separate authorized host decision; no branch-protection changes occur here.
- A tiny pilot does not prove reliable agent improvement. Record trial limits and review cost.

## Points of No Return

None introduced in downstream projects. No production/data migration occurs. Import/policy
updates are reviewable commits; revert the pin and matching host integration together if
needed. Do not remove existing required protections as part of rollback.

## Consequences

Existing pinned copies are unchanged until upgraded. A project can satisfy the behavioral
minimum with its current commands and no new tools. A selected stable invariant may later
use a scoped ratchet while unrelated legacy debt is handled separately. A project cannot
claim effective adoption from a copied document or green comparator alone.

## Enforcement

- Semantic review of existing AEP/task evidence for §6.5; no schema validation claim.
- Active AGENTS/Copilot/daily projections route to the same rule and optional methods.
- Real bundle imports verify minimal availability and preserve host sentinels.
- CLI tests cover unchanged debt, removals, additions, equal-count replacement, scanner
  failure/skip, stale revision, changed rules/scope, invalid JSON/types and no file writes.
- Existing maintainer gates continue unchanged in meaning; run their regression suites.

## Documentation Impact

Sources of truth: AI_RULES §6.5 (behavior); ENGINEERING_METHODS_ADOPTION (rollout and comparator
input contract); ratchet_findings.py (comparison); evidence review (source claims/limitations).
Update method guides, import/bundle/quick guides, projections, overlay template, enforcement
matrix, trigger map, README, DEVELOPMENT and CHANGELOG. No generated documentation.

## Governance Change

- Governance change: yes; explicitly reviewable tightening of non-trivial method rationale.
- Upstream starting point: `e33cc87dc1fa98bed0a74bf50a0e589c85ff2da6` after PR #38.
- Local overlay impact: optional practice rollout table; reconcile existing overrides.
- Enforcement impact: existing task evidence; optional host finding comparison, no new
  mandatory adopter job, reviewer, branch protection or AEP schema.
- Migration: reviewed pin → preserved host instruction integration → one scoped pilot →
  local promotion/defer/retire decision. No automatic downstream repository modifications.

## References

- [Evidence review](../research/AI_ENGINEERING_METHODS_EVIDENCE.md)

## Related Documents
- [Adoption and comparator contract](../usage/ENGINEERING_METHODS_ADOPTION.md)
- [Adaptive governance](../constitution/ADAPTIVE_GOVERNANCE.md)
- [ADR-0010 safe import](ADR_0010_Safe_Bundle_Import.md)
