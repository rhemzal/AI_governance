# Contributing

Thanks for helping improve this governance kit.

## What belongs here

This repository is a **project-agnostic** kit. Contributions should be:
- Generalizable across stacks and teams.
- Written as portable documents (mostly Markdown).
- Consistent with the repo's premise: **normative rules** live in `constitution/`, `ci/`, `interface/`; `architecture/rag/` is **advisory**.

## How to contribute

1. Open an issue describing the change and why it is broadly applicable.
2. Propose the smallest change that solves the problem.
3. For rule changes, update both:
   - the **normative** statement (MUST/MUST NOT), and
   - the **enforcement** expectation (how it is verified).
4. Keep documentation changes high-signal:
   - ensure referenced `.md` paths exist
   - avoid duplication (single source of truth)
   - keep the diff minimal and reviewable

## Style and consistency

- Prefer clear MUST/MUST NOT wording in normative docs.
- Avoid duplicating rules: keep a single canonical source and link to it.
- Keep filenames stable; the kit is designed to be copied into other repos.
- Avoid adding binary files or large generated artifacts; link to external references instead.

## Submitting a PR

Use the PR template and include a brief "Doc Delta" describing what changed, why, and how it should be adopted downstream.
