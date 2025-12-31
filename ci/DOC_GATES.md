# Documentation CI Gates (Principles)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
Prevent “documentation drift” and duplicated, conflicting rules.

## Gate D1: Single Source of Truth
Fail if governance rules are duplicated outside `constitution/`.

## Gate D2: Docs Updated with Behavior
If a PR changes behavior that affects:
- interface usage
- public contracts
- architecture boundaries

Then require updates to:
- `usage/` docs and/or ADRs

## Gate D3: Broken Links / Missing Files
Fail if:
- markdown links point to missing files
- referenced ADRs do not exist

## Gate D4: Reproducible Documentation Generation
If any documentation is declared as generated (by tooling or AI-assisted generation), require:
- a clear source-of-truth reference
- a repeatable regeneration process (documented in PR or in the repo)

## Gate D5: Anti-Fragmentation
Fail (or warn, then fail) if:
- a new documentation file is added without being linked from `README.md`
- a new documentation file overlaps an existing topic without consolidation justification

## Related Documents
- `constitution/AI_RULES.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `adr/ADR_TEMPLATE.md`

