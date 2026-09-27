# ADR 0008: Bounded Agent Execution and Revision-Bound Evidence

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status
Proposed — implemented on this review branch; acceptance occurs through maintainer review/merge.

## Context
The kit already supports autonomous verification and repair, but its overlay says to stop on any unexpected step failure. File-count planning and blanket high-risk stops also conflate technical risk with action authority. Evidence blocks do not explicitly bind results to tested revisions, and audit findings quotas can encourage invented or inflated findings.

## Decision
Two changes to the existing contract:
1. Define a bounded task mandate, adaptive planning, repair budget, and action-specific stop conditions in `constitution/AI_ENFORCEMENT.md` §§1.1–1.3. Existing authorization remains valid; preparing a change and applying its external effects are separate actions.
2. Define evidence and continuity in §1.4: revisions/environment, independent acceptance evidence, compact state/handoff, resource ownership, and explicit task outcomes.

Routine reversible work uses a concise scope/verification statement. Full plans apply to HIGH-risk work, dependent non-trivial steps, handoff, and concurrency. Reviewer findings have no count or severity quota; audits instead record coverage and substantiated results.

## Alternatives Considered
- Keep blanket stops and rely on local exceptions: preserves contradictory agent instructions and recurring operator interruptions.
- Require a complete orchestration platform: disproportionate for a reusable kit; defer.
- Allow unrestricted autonomy: fails to distinguish authorized preparation from irreversible external effects; reject.

## Trade-Offs
Adopters must reconcile existing overlays and distinguish risk from authority. The kit specifies evidence and behavior, not vendor-specific enforcement. Platform/tool isolation and permissions must be configured by the adopter; natural-language mandates alone cannot enforce them.

## Sensitivity Points & Risks
Incorrect applicability or authority classification remains a review risk. Correlated agent self-review is not independent proof. Existing CI and acceptance criteria remain in force; changes to governance cannot silently authorize bypassing them.

## Points of No Return
No runtime deployment or data migration. Roll back the imported revision and associated projections together if the pilot worsens outcomes; retain task evidence and authorization history.

## Consequences
Align agent projections, overlays, debugging prompts, audit guidance, and evidence templates. Keep specialized context loaded on demand. AI-authored source prose is distinguished from mechanically generated artifacts. Development-time observability is permitted where it supports verification.

## Enforcement
Review authority and acceptance; keep existing product gates. Test AEP declaration shape separately under ADR-0009. Pilot old/new guidance on matched tasks with fixed models, tools, initial state, and budgets; record outcomes, corrections, interruptions, and cost. This change does not claim measured productivity improvement before that pilot.

## Documentation Impact
Canonical source: `constitution/AI_ENFORCEMENT.md`; projections in `AGENTS.md`, `.github/copilot-instructions.md`, and the overlay; operational template in `usage/AI_RUN_EVIDENCE.md`. Consolidate duplicated STOP rules and remove audit quotas. These are authored documents, not generated outputs.

## Governance Change
- Governance-impacting: yes; replaces file-count applicability and blanket high-risk/failure stops with the bounded mandate and evidence rules.
- Local overlays: review explicit overrides before adopting; old overrides remain visible and must be reconciled deliberately.
- Rollout: import on a branch, compare the changed rules/projections, verify existing gates, pilot bounded tasks, then review adoption. No automatic merge/deploy authority is added.
- Kit risk: G3 released/reusable guidance; retain existing reference checks. No new enterprise approval structure.

## Related Documents
- `constitution/AI_ENFORCEMENT.md`
- `constitution/ADAPTIVE_GOVERNANCE.md`
- `usage/AEP_VALIDATION.md`
- `usage/AI_RUN_EVIDENCE.md`
- `tooling/BENCHMARK_SCENARIOS.md` (upstream kit if not imported)
