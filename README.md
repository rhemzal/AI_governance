# AI-Assisted Development Governance Kit

This repository is a reusable, project-agnostic governance kit for **AI-assisted software development**: rules, enforcement expectations, and adoption workflows that keep AI-driven changes reviewable and enforceable.

Normative sources live in `constitution/` and `ci/`. Advisory reasoning notes live in `architecture/rag/`.

## Quick use (existing project)
If you’re evaluating this kit for an existing repo, start with an assessment prompt before importing anything.

- For ready-to-use prompt recipes, see `usage/QUICKGUIDE.md` (Recipe D/E).

### Copy-paste prompt (URL reference → adoption recommendation)

```
This task is assessment-only. Do not change code/docs.

Context:
- I want to evaluate adopting the AI_governance kit: https://github.com/rhemzal/AI_governance
- My repo may be new or already in progress.

1) Summarize what this kit provides (rules, enforcement, workflows) and what it does NOT provide.
2) Assess what parts are applicable to my repo right now and what to defer.
3) Recommend a staged adoption order (L0 → L3):
   - L0: doc hygiene + daily enforcement prompt
   - L1: deterministic tests
   - L2: boundary integrity
   - L3: risk signals (coverage/flakiness budget/ADR-required checks)
4) Recommend an import approach (Copy vs Submodule vs Fork) and the minimal set of folders to import first.

Output:
- A short assessment.
- A recommended adoption order with prerequisites.
- What to defer (and why).
- Max 3 blocking questions (only if truly necessary).
```

## What changes after adoption (expected AI behavior)
If you actually adopt the kit (import + follow the workflows), you should expect the assistant to:
- consult repo sources of truth first (rules/docs/tests/ADRs) before asking basic questions
- keep scope explicit and diffs small
- escalate to “high-risk mode” (ADR-first + compliance reporting) for boundary/contract changes
- treat CI adoption progressively (high-signal checks first, stricter gates when prerequisites exist)
- keep documentation aligned with behavior (using `DOC DELTA` as PR evidence/metadata)
- treat `notes/**` as non-canonical working notes (do not rewrite unless explicitly instructed)

## Start here (top links)
- Core rules: [constitution/AI_RULES.md](constitution/AI_RULES.md)
- Daily AI work: [constitution/AI_ENFORCEMENT_DAILY.md](constitution/AI_ENFORCEMENT_DAILY.md)
- High-risk changes: [constitution/AI_ENFORCEMENT.md](constitution/AI_ENFORCEMENT.md)
- Import guidance: [usage/HOW_TO_IMPORT.md](usage/HOW_TO_IMPORT.md)
- Quick recipes & prompts: [usage/QUICKGUIDE.md](usage/QUICKGUIDE.md)
- Progressive CI adoption: [usage/CI_MINIMUM_ADOPTION.md](usage/CI_MINIMUM_ADOPTION.md)
- Architecture decision framework: [architecture/ARCHITECTURE_DECISION_FRAMEWORK.md](architecture/ARCHITECTURE_DECISION_FRAMEWORK.md)
- ADR template: [adr/ADR_TEMPLATE.md](adr/ADR_TEMPLATE.md)
- Local overlays & precedence: [usage/LOCAL_OVERLAY_AND_PRECEDENCE.md](usage/LOCAL_OVERLAY_AND_PRECEDENCE.md)

## Repository structure
- `constitution/` — core rules and enforcement contracts
- `ci/` — CI gate principles (implementation varies by stack)
- `adr/` — ADR templates and accepted decisions for this kit
- `usage/` — import and adoption workflows (including prompt recipes)
- `notes/` — committed vs local parking-lot notes
- `architecture/` and `architecture/rag/` — decision guidance and advisory theory notes

## PR Habit: “Doc Delta”
When a PR changes behavior, include the `### DOC DELTA` block from [usage/HOW_TO_USE_WITH_COPILOT.md](usage/HOW_TO_USE_WITH_COPILOT.md).

`DOC DELTA` is PR evidence/metadata: reference the source of truth (code/tests/ADRs) and list which docs were updated/removed.

## Attribution / Traceability
If you copy parts of this kit into another repository, preserve the “Provenance” banner at the top of imported documents so the origin remains traceable.

## Disclaimer
This repository provides governance guidance and reusable documentation. It is not legal advice and does not guarantee compliance with any standard or regulation.

## License
This repository is intended to be publishable and reusable.

- Documentation and other non-code content: **CC BY 4.0** (see `LICENSE`).
- Code (if any): **MIT** (see `LICENSE-CODE`).

## Contributing
See `CONTRIBUTING.md`.

## Security
See `SECURITY.md`.
