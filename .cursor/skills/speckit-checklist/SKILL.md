---
name: "speckit-checklist"
description: "Generate a custom checklist for the current feature based on user requirements. Use when the user invokes /speckit-checklist."
disable-model-invocation: true
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/checklist.md (SKILL split — see checklist-full-procedure.md)"
---

# speckit-checklist

Generate reviewer-owned **requirements-quality** checklists (unit tests for the spec, not implementation QA).

**User input:** consider `$ARGUMENTS` before any steps.

## What to do

1. Read **`checklist-full-procedure.md`** in this skill directory (same folder as this file).
2. Execute that procedure **in full** — pre/post extension hooks, `check-prerequisites.sh`, clarifying questions, generation rules, report.
3. Never mark generated checklist items `[x]`; leave them `[ ]` for the reviewer.

Do not shorten or skip sections in the procedure file to save context.
