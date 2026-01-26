# How to Use With Visual Studio Code (AI-Heavy Workflow)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Practical Recommendations (As of 2025-12-28)
This document is intentionally practical and time-stamped.
VS Code and AI integrations evolve quickly; treat this as a workflow pattern, not a guarantee of specific UI features.

## Scope
Applies to:
- GitHub Copilot in VS Code
- AI-assisted workflows that operate on a repo as the source of truth
- Optional use of MCP (Model Context Protocol) servers

## What Belongs in This Repo vs Your VS Code Setup
This repo stores:
- governance rules (`constitution/`)
- decision records (`adr/`)
- practical workflows (`usage/`)

Your VS Code setup stores:
- extensions
- tasks
- local settings

Avoid “documenting every click”. Prefer stable, tool-agnostic habits.

## Recommended Extensions (Minimal Set)
Keep the set small to reduce cognitive load.

- **GitHub Copilot**: code completion.
- **GitHub Copilot Chat**: interactive changes and review-style questions.
- **GitHub Pull Requests and Issues** (optional but high leverage): keeps PR/issue context close to the code.
- **Markdown tooling** (lint/preview) (optional): reduces docs drift and broken links.

Add language-specific tools only when the codebase needs them (linters, formatters, test adapters).

## MCP (Model Context Protocol): When It Helps
MCP is useful when you want the assistant to reliably consult external context (docs, tickets, diagrams, catalogs) instead of guessing.

### Good MCP use-cases
- retrieving architecture decisions (ADRs) and linking them to changes
- referencing internal standards / policies
- pulling issue context for implementation constraints

### Avoid MCP when
- it expands the scope unpredictably
- it introduces sensitive data into broad contexts
- it replaces local repo sources-of-truth

Governance rule: repo documents remain the source of truth; external context is advisory unless adopted via ADR.

## How to Ask the AI in VS Code (High-Leverage Patterns)
The most reliable results come from **bounded, inspectable tasks**.

### 1) Always start with constraints
Paste one of:
- `constitution/AI_ENFORCEMENT_DAILY.md` (most work)
- `constitution/AI_ENFORCEMENT.md` (high-risk changes)

### 2) Use “selection-first” questions
When you select code in the editor, ask:
- “Explain what this does and which layer it belongs to. List boundary risks.”
- “Propose the smallest change to achieve X. Include tests and docs updates.”

### 3) Ask for diffs and file lists
Prefer:
- “List files you will change and why.”
- “Make the change with a minimal diff; avoid refactors.”

### 4) Force verification
Ask:
- “Run the narrowest tests relevant to this change.”
- “If tests don’t exist, propose where they should live by layer.”

### 5) Make documentation part of the request
For behavior changes, require:
- `### DOC DELTA` (template lives in `usage/HOW_TO_USE_WITH_COPILOT.md`)

### 6) Protect working notes from accidental edits (Optional)
If your repo uses a `notes/` parking-lot, explicitly instruct the assistant not to “clean up” or rewrite it during unrelated tasks.

Example prompt line you can add:
- “Treat `notes/**` as non-canonical working notes. Do not edit them unless I explicitly ask. If asked, prefer append/link updates.”

Tool-specific (Cursor) suggestion:
- Create a local Cursor rule that enforces the same behavior for `notes/**` in your project. Keep it local/team-controlled; do not treat it as part of the imported kit baseline.

## Workflow Notes (Avoid Duplication)
Team process guidance (parallel vs serial work, definition of done, Doc Delta discipline) is maintained in:
- `usage/HOW_TO_USE_WITH_COPILOT.md`

This document stays focused on VS Code/editor setup and prompting patterns.

## Related Documents
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md` and `constitution/AI_ENFORCEMENT_DAILY.md`
- `adr/ADR_TEMPLATE.md`
- `ci/DOC_GATES.md`
