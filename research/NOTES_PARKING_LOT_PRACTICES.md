# Notes / Parking-Lot Practices (Advisory Research)

_Provenance: This research note was added to the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Purpose
Summarize established practices for handling “working notes” in software projects:
- keep notes low-friction (avoid derailing active work)
- prevent notes from becoming accidental sources of truth
- support both personal and shared note-taking

This document is **advisory**. Normative rules live in `constitution/`.

## Key patterns observed

### 1) Split notes into “shared vs personal”
Common practice is to keep two classes of notes:
- **Shared/committed**: relevant to the team and worth versioning.
- **Personal/local**: scratchpad, temporary lists, prototypes — useful for the individual, but not worth PR noise.

This maps well to a two-tier structure:
- `notes/committed/` (tracked)
- `notes/local/` (untracked)

### 2) Keep local notes close to the project, but excluded from version control
A common approach is to keep a notes directory **inside** the project (so it’s always at hand), but exclude it from version control via ignore rules (global ignore or local excludes).

Source: “Project notes” recommends a globally-ignored `.note/` directory kept inside the project tree for convenience.
- `https://localheinz.com/articles/2019/10/25/project-notes/`

### 3) Use Git ignore mechanisms intentionally (shared vs local-only)
Git supports multiple scopes for ignore rules:
- **Repo-wide shared ignore** via committed `.gitignore` (applies to all clones).
- **Local-only ignore** via `.git/info/exclude` (not committed).
- **Global ignore** (applies to all repos on the machine).

Source: GitHub Docs “Ignoring files” (sections on `.gitignore`, global ignores, and `.git/info/exclude`).
- `https://docs.github.com/articles/ignoring-files`

### 4) Separate “working notes” from canonical decision records
Teams commonly distinguish:
- **RFCs**: speculative proposals for discussion (multiple options).
- **ADRs**: records of decisions that reflect the current implementation.

Working notes are neither RFCs nor ADRs; they should not silently become architectural authority.

Sources:
- `https://docs.wellcomecollection.org/architecture-decision-records-adr`
- `https://candost.blog/adrs-rfcs-differences-when-which/`

### 5) Isolate exploratory work from review-ready artifacts
While not “notes” directly, the scratchpad-branch workflow illustrates a consistent principle:
keep exploratory history separate, then produce a clean, reviewable artifact.

Source: Scratchpad branches workflow.
- `https://julien.ponge.org/posts/a-workflow-for-experiments-in-git-scratchpad-branches/`

## Recommendations for this governance kit
To keep “parking-lot notes” usable in AI-heavy workflows:
- Provide both `notes/committed/` and `notes/local/`.
- Prevent accidental commits of personal notes via ignore rules.
- Treat `notes/**` as **non-canonical** by default (working notes), and avoid rewriting them during unrelated tasks.
- For committed notes, prefer **append-only and link-first**: add a new line + link to the Issue/ADR/PR where something was resolved.

## Related Documents
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
- `usage/LOCAL_OVERLAY_AND_PRECEDENCE.md`
- `usage/HOW_TO_IMPORT.md`

