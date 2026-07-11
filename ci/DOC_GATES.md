# Documentation CI Gates (Principles)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
Prevent “documentation drift” and duplicated, conflicting rules.

**Level columns:** **Governance Level (G0–G4)** = project maturity (`constitution/ADAPTIVE_GOVERNANCE.md`). **CI Maturity (CM0–CM3)** = adopter automation stage — canonical mapping in `usage/ENFORCEMENT_MATRIX.md`. Do not use bare `L0`–`L3`.

## Gate: D1 — Single Source of Truth

- **Recommended from Governance Level (G):** G2
- **Mandatory from Governance Level (G):** G3
- **Adopter CI Maturity (CM):** Advisory CM2; Required CM3 — see `usage/ENFORCEMENT_MATRIX.md`
- **Risk mitigated:** Governance rules duplicated in multiple places leading to conflicting or stale copies; confusion about which document is authoritative.
- **Local alternative:** At G0–G1, the developer maintains a single canonical location by convention, with no automated check required.
- **Cost:** Low. A grep or link check is sufficient. Enforce only for `constitution/` at Level 2.
- **Failure action:** At G3+, fail if governance rules are duplicated outside `constitution/`. At G2, warn and require consolidation as a follow-up.

Fail if governance rules are duplicated outside `constitution/`.

## Gate: D2 — Docs Updated with Behavior

- **Recommended from Governance Level (G):** G2
- **Mandatory from Governance Level (G):** G3
- **Adopter CI Maturity (CM):** Required CM2 (review); CI automation advisory — see `usage/ENFORCEMENT_MATRIX.md`
- **Risk mitigated:** Behavior changes that leave documentation stale; usage docs or ADRs that contradict the actual system behavior.
- **Local alternative:** At G1–G2, the developer (or AI agent) states in the commit which docs were checked and whether any update is needed.
- **Cost:** Low. A PR checklist item or commit message requirement covers this without automation.
- **Failure action:** At G3+, block merge if behavior-changing PRs omit required doc updates. At G2, warn and require a follow-up issue.

If a PR changes behavior that affects:
- interface usage
- public contracts
- architecture boundaries

Then require updates to:
- `usage/` docs and/or ADRs

**Optional automation (CM2+):** PR body check for `DOC DELTA` when non-doc paths change — see `usage/CI_STARTER_WORKFLOWS.md` §7 and kit `.github/workflows/doc-delta-advisory.yml`. Adopters may promote warning to required via `governance/LOCAL_OVERLAY.md`.

## Gate: D3 — Broken Links / Missing Files

- **Recommended from Governance Level (G):** G1
- **Mandatory from Governance Level (G):** G2
- **Adopter CI Maturity (CM):** Required CM0 — see `usage/ENFORCEMENT_MATRIX.md`
- **Risk mitigated:** Dead links in documentation that mislead readers; referenced ADRs or files that do not exist.
- **Local alternative:** Run `make check-links` or a simple markdown link checker locally before commit.
- **Cost:** Very low. Link checkers are fast and cheap. This is one of the most cost-effective documentation gates.
- **Failure action:** Fail the pipeline. Broken links MUST be fixed or removed before merge.

Fail if:
- markdown links point to missing files
- referenced ADRs do not exist

## Gate: D4 — Reproducible Documentation Generation

- **Recommended from Governance Level (G):** G2
- **Mandatory from Governance Level (G):** G3
- **Adopter CI Maturity (CM):** Deferred CM2+ — see `usage/ENFORCEMENT_MATRIX.md`
- **Risk mitigated:** Generated documentation that cannot be reproduced; manual edits to generated outputs that diverge from the source.
- **Local alternative:** At G1–G2, document the generation command in a `notes/` file or README section. Require the developer or AI agent to rerun it before committing.
- **Cost:** Low if the generation process is already defined. The cost is in discipline, not tooling.
- **Failure action:** At G3+, block merge if generated documentation was manually edited without updating the source or generator.

If any documentation is declared as generated (by tooling or AI-assisted generation), require:
- a clear source-of-truth reference
- a repeatable regeneration process (documented in PR or in the repo)

## Gate: D5 — Anti-Fragmentation

- **Recommended from Governance Level (G):** G2
- **Mandatory from Governance Level (G):** G3
- **Adopter CI Maturity (CM):** Advisory CM2; Required CM3 — see `usage/ENFORCEMENT_MATRIX.md` (kit repo dogfoods D5 error earlier)
- **Risk mitigated:** Documentation sprawl; new files added without integration into the navigation structure; overlapping topics creating confusion.
- **Local alternative:** At G1–G2, the developer (or AI agent) checks that any new doc file is linked from `README.md` or a known index before commit.
- **Cost:** Low. A grep for the new filename in `README.md` is sufficient at G2.
- **Failure action:** At G3+, fail (or warn then fail) if a new documentation file is added without a link from `README.md` or without a consolidation justification for overlapping topics.

Fail (or warn, then fail) if:
- a new documentation file is added without being linked from `README.md`
- a new documentation file overlaps an existing topic without consolidation justification

## Related Documents
- `constitution/AI_RULES.md`
- `constitution/ADAPTIVE_GOVERNANCE.md`
- `usage/ENFORCEMENT_MATRIX.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `adr/ADR_TEMPLATE.md`

