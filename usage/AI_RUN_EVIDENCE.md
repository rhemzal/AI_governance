# AI Run Evidence (Minimal Block for PRs)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

Use this guidance when PRs include AI-assisted implementation.
Keep evidence practical, high-signal, and free of secrets.

This block complements (not replaces) `### DOC DELTA`.

## Minimal evidence block (copy/paste)

```markdown
### AI RUN EVIDENCE
- Model/tooling context (high level, no secrets):
  - Assistant/tool:
  - Execution mode (interactive/agent/CI assist):
  - Key constraints/rules consulted:
- Checks run:
  - Command/check:
  - Result:
- Artifacts/logs:
  - CI run URL:
  - Relevant job/log URL(s):
  - Local evidence (if any):
- Assumptions:
  - 
- Known limitations:
  - 
```

## Practical rules
- Do not include tokens, secrets, private prompts, or sensitive raw logs.
- Prefer links to CI artifacts/logs over large pasted output.
- Keep assumptions explicit so reviewers can challenge them quickly.

## Related Documents
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `constitution/AI_ENFORCEMENT.md`
