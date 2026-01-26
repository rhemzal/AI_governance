# Local Overlay & Precedence (When Importing This Kit)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This kit is intended to be a **single source of truth** for governance rules and gates.
When you import it into another repository, you will often need **project-specific additions**.
This document defines a minimal, auditable way to do that **without creating conflicting rule sources**.

## Core Principle
- Do not fork the canonical rules by copy-pasting them into multiple places.
- Add local constraints as a **small overlay** that explicitly states what it adds or overrides.

## Precedence Rules (Hard)
Use this precedence order (highest wins):
1. **Local overlay** (repo-specific constraints)
2. This kit’s constitution and enforcement documents
3. Everything else (notes, examples, non-normative guidance)

## Language Policy & Translations (Recommended)
This kit is English-first for canonical governance so AI and humans share a stable baseline.

Downstream repos MAY add language exceptions via a local overlay (recommended), for example:
- a different shared language for `notes/committed/**`
- a policy for translations (where they live, who maintains them)

Recommended pattern:
- Keep canonical governance documents in English.
- Allow translations only as explicitly subordinate artifacts under `translations/<lang>/...`.
  - Each translation should point to the canonical English source (path + version/SHA when possible).
  - Translations must not override canonical rules.

Within the imported kit, treat these as highest priority:
- `constitution/AI_RULES.md` (normative rules)
- `constitution/AI_ENFORCEMENT.md` (how rules are enforced and what evidence is required)

Local overlays MUST:
- be short
- be explicit about scope
- state whether they are additive or overriding
- be reviewable in PRs

## How to Handle Conflicts (Hard)
If your overlay conflicts with the imported kit:
- Use an explicit **Overrides** entry (template section below).
- Reference the exact imported document path and the section name.
- Provide rationale and the risk accepted (or mitigation).

If you cannot explain the conflict and risk, do not override: add an **Additions** rule instead.

## Where to Put the Overlay
Recommended:
- governance/LOCAL_OVERLAY.md (or docs/governance/LOCAL_OVERLAY.md) in the target repo.

Avoid:
- editing imported kit files directly (unless you intentionally fork)
- scattering extra rules across multiple team docs

## Overlay Template (Copy/Paste)
Use this template in the target repo.

# LOCAL GOVERNANCE OVERLAY

## Purpose
- Why this overlay exists (org policy, deployment constraints, tooling, risk posture).

## Scope
- What it applies to (modules, services, teams, repositories).

## Precedence
- This overlay overrides/adds to the imported kit.
- Conflicts are resolved by: overlay wins.

## Additions (Additive Rules)
- Rule ID / short name:
  - What is required
  - Evidence expected in PR/CI

## Overrides (If Any)
Only use overrides when unavoidable.
- Override:
  - Imported rule reference (path + section)
  - Replacement text
  - Rationale
  - Risk accepted / mitigation

## Verification
- What checks prove compliance (CI gates, tests, audits)

## Change Control
- Changes to this overlay require an ADR (recommended) when they affect boundaries/contracts or enforcement.

Recommended ADR trigger examples:
- you weaken or change enforcement evidence requirements
- you change architectural boundary expectations
- you introduce exceptions to non-interactive execution/time limits

## Common Mistakes to Avoid
- Writing a second “rules doc” that rephrases the constitution.
- Overriding silently (no rationale, no explicit replacement).
- Mixing normative requirements into advisory notes.

## Related Documents
- `usage/HOW_TO_IMPORT.md`
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
- `ci/ARCHITECTURE_GATES.md`
- `ci/TEST_GATES.md`
