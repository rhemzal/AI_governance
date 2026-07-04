# Documentation CI Gates (Principles)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose
Prevent “documentation drift” and duplicated, conflicting rules.

See `constitution/ADAPTIVE_GOVERNANCE.md` for guidance on which level each gate is appropriate for.

## Gate: D1 — Single Source of Truth

- **Recommended from level:** 2
- **Mandatory from level:** 3
- **Risk mitigated:** Governance rules duplicated in multiple places leading to conflicting or stale copies; confusion about which document is authoritative.
- **Local alternative:** At Level 0–1, the developer maintains a single canonical location by convention, with no automated check required.
- **Cost:** Low. A grep or link check is sufficient. Enforce only for `constitution/` at Level 2.
- **Failure action:** At Level 3+, fail if governance rules are duplicated outside `constitution/`. At Level 2, warn and require consolidation as a follow-up.

Fail if governance rules are duplicated outside `constitution/`.

## Gate: D2 — Docs Updated with Behavior

- **Recommended from level:** 2
- **Mandatory from level:** 3
- **Risk mitigated:** Behavior changes that leave documentation stale; usage docs or ADRs that contradict the actual system behavior.
- **Local alternative:** At Level 1–2, the developer (or AI agent) states in the commit which docs were checked and whether any update is needed.
- **Cost:** Low. A PR checklist item or commit message requirement covers this without automation.
- **Failure action:** At Level 3+, block merge if behavior-changing PRs omit required doc updates. At Level 2, warn and require a follow-up issue.

If a PR changes behavior that affects:
- interface usage
- public contracts
- architecture boundaries

Then require updates to:
- `usage/` docs and/or ADRs

## Gate: D3 — Broken Links / Missing Files

- **Recommended from level:** 1
- **Mandatory from level:** 2
- **Risk mitigated:** Dead links in documentation that mislead readers; referenced ADRs or files that do not exist.
- **Local alternative:** Run `make check-links` or a simple markdown link checker locally before commit.
- **Cost:** Very low. Link checkers are fast and cheap. This is one of the most cost-effective documentation gates.
- **Failure action:** Fail the pipeline. Broken links MUST be fixed or removed before merge.

Fail if:
- markdown links point to missing files
- referenced ADRs do not exist

## Gate: D4 — Reproducible Documentation Generation

- **Recommended from level:** 2
- **Mandatory from level:** 3
- **Risk mitigated:** Generated documentation that cannot be reproduced; manual edits to generated outputs that diverge from the source.
- **Local alternative:** At Level 1–2, document the generation command in a `notes/` file or README section. Require the developer or AI agent to rerun it before committing.
- **Cost:** Low if the generation process is already defined. The cost is in discipline, not tooling.
- **Failure action:** At Level 3+, block merge if generated documentation was manually edited without updating the source or generator.

If any documentation is declared as generated (by tooling or AI-assisted generation), require:
- a clear source-of-truth reference
- a repeatable regeneration process (documented in PR or in the repo)

## Gate: D5 — Anti-Fragmentation

- **Recommended from level:** 2
- **Mandatory from level:** 3
- **Risk mitigated:** Documentation sprawl; new files added without integration into the navigation structure; overlapping topics creating confusion.
- **Local alternative:** At Level 1–2, the developer (or AI agent) checks that any new doc file is linked from `README.md` or a known index before commit.
- **Cost:** Low. A grep for the new filename in `README.md` is sufficient at Level 2.
- **Failure action:** At Level 3+, fail (or warn then fail) if a new documentation file is added without a link from `README.md` or without a consolidation justification for overlapping topics.

Fail (or warn, then fail) if:
- a new documentation file is added without being linked from `README.md`
- a new documentation file overlaps an existing topic without consolidation justification

## Related Documents
- `constitution/AI_RULES.md`
- `constitution/ADAPTIVE_GOVERNANCE.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `adr/ADR_TEMPLATE.md`

