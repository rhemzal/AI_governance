# AGENTS.md — AI Governance Projection

This is a short agent-facing projection. The source of truth remains the governance kit documents.

## Required context
- Core rules: `constitution/AI_RULES.md`
- Daily work: `constitution/AI_ENFORCEMENT_DAILY.md`
- High-risk changes: `constitution/AI_ENFORCEMENT.md`
- Adaptive governance: `constitution/ADAPTIVE_GOVERNANCE.md`

## Working rules
- Keep scope explicit and diffs small.
- Preserve normative/advisory separation: `constitution/` and `ci/` define rules and gates; `usage/`, `research/`, and `notes/` are guidance unless adopted by local policy.
- Prefer updating existing documents over adding new large documents.
- Before assuming CI enforcement, check the applicable governance level. If CI is not adopted yet, use local verification and PR evidence for the same expectations.

## Verification
- Prefer existing repo-local commands and guidance in `DEVELOPMENT.md`.
- Do not assume global test runners.

## Related Documents
- `README.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
