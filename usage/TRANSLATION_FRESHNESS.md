# Translation Freshness Guidance

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This guidance applies to subordinate translations under `translations/**`.
It does not change the English-first canonical policy in `constitution/AI_RULES.md`.

## Required source reference metadata (per translated file)
Include at top of each translation:
- canonical source path (English document path)
- canonical source commit SHA or tag/version used for translation
- translation last-reviewed date

Example:

```markdown
_Translation source: constitution/AI_RULES.md @ <commit-sha-or-tag>_
_Translation reviewed: YYYY-MM-DD_
```

## Freshness review cadence (recommended)
- Minimum: monthly review for actively used governance docs.
- Triggered review: when canonical source changes in a relevant section.

## Drift handling process
1. Detect source change in canonical English document.
2. Mark translation as `stale` (issue/PR label or note in file header).
3. Update translation to match canonical meaning.
4. Update source SHA/tag and reviewed date metadata.
5. If conflict exists, English canonical text remains authoritative.

## Related Documents
- `constitution/AI_RULES.md`
- `usage/LOCAL_OVERLAY_AND_PRECEDENCE.md`
