# How to Import This Kit Into Another Repo

_Provenance note: Imported copies should preserve origin information. This kit includes a short “Provenance” banner at the top of import-target documents; keep it to retain traceability._

This kit is documentation-first governance: you import it to make AI-assisted changes enforceable (rules, gates, ADR discipline, and auditability).

## Import Bundles (Machine-Readable)

Do not import everything by default. Use `kit-manifest.yml` at the kit root to select a bundle:

| Bundle | When to use |
| --- | --- |
| `minimal` | Fastest useful adoption: agent projections, core rules, daily enforcement, quick recipes, ADR template. |
| `standard` | Recommended baseline: `minimal` plus full `constitution/`, `ci/`, `adr/`, `usage/`, and the local overlay template. |
| `architecture` | Architecture selection and advisory RAG notes (decision framework, style matrix, taxonomy, data modeling, terminology, `architecture/rag/`). |
| `research` | Advisory research and external playbook references (`research/`). |
| `full` | Complete copy import (Option A below): composes `standard` + `architecture` + `research`, plus `interface/`, `notes/`, and full `governance/`. |

Bundle paths use `extends` / `composes` resolution (union, deduplicated). Importers must honor `exclude` entries (e.g. `notes/local/**`).

For humans: start with `minimal` or `standard`, then add bundles as needed.
For agents and automation: read `kit-manifest.yml` first; use `usage/ADOPTION_BUNDLES.md` for human-oriented bundle selection.

## Choose an Import Strategy (When to Use What)
Pick based on two questions:
1) Do you want **upstream updates**?
2) Will you **customize** the governance baseline?

### Quick Decision Guide
- Choose **Copy** if you want a stable snapshot and fast adoption (most teams).
- Choose **Git Submodule** if you want upstream updates with explicit version pinning.
- Choose **Fork** if you will materially change rules/gates and want to own the baseline.

### Signs You Should Prefer Each Option

**Prefer Copy when**:
- You need the fastest path to “working governance” (days, not weeks).
- You want a stable baseline and you do not plan frequent governance changes.
- Your organization restricts submodules or has tooling friction around them.

**Prefer Git Submodule when**:
- You want upstream improvements over time.
- You can handle occasional merge/rebase effort for docs.
- You can enforce a pinned commit SHA (avoid "floating" governance).

**Prefer Fork when**:
- You will rewrite or extend the constitution/gates materially (org-specific policy).
- You need language/jurisdiction-specific compliance wording.
- You want to keep your governance changes private or controlled.

## Core Principle (Regardless of Option)
Avoid duplication: have one canonical source for each rule/gate.
When you must add local rules, add them as **project-specific overlays** and clearly state precedence.

See:
- `usage/LOCAL_OVERLAY_AND_PRECEDENCE.md`

This kit provides a ready-to-copy overlay template:
- `governance/LOCAL_OVERLAY_TEMPLATE.md` (copy to `governance/LOCAL_OVERLAY.md` in the target repo and customize)

## If You Already Have Governance
Decide which of these this kit will be in your repo:
- **Upstream baseline**: this kit is the canonical source for rules/gates; your repo adds a local overlay.
- **Reference only**: this kit is informational; your existing governance remains canonical.

Do not run with two sources of truth.

Recommended: record the decision as an ADR using `adr/ADR_TEMPLATE.md` (title suggestion: “Governance Baseline: Imported Kit vs Local”).

If you want an AI to assess what to adopt (and in what order), see:
- `usage/QUICKGUIDE.md` (Recipe D/E: adoption assessment prompts)

## Governance Versioning (Recommended)
To keep governance auditable over time, record which kit version you imported.

See `VERSIONING.md` for version series (`0.x` vs `1.0+`) and changelog label meanings (`Governance-impacting`, `Advisory-only`, `Import bundle change`, `Breaking rule change`).

**If you Copy**:
- Record the import as an ADR (what was imported, date, and source commit/tag if known).
   - Do not remove the “Provenance” banner from imported documents.

**If you use a Submodule**:
- Pin to a commit SHA.
- Treat updates as dependency upgrades and record upgrades as an ADR (old SHA → new SHA, why, what enforcement changed).
 - Do not remove the “Provenance” banner from documents.

**If you Fork**:
- Maintain your own version tags.
- Keep a policy for upstream cherry-picks (optional but recommended).
 - If you relicense or materially rewrite the kit, update the provenance banner accordingly.

## Post-Import Enforcement Setup (`standard` bundle)

After copying `standard` (or `full`), complete within one PR:

1. Copy `governance/LOCAL_OVERLAY_TEMPLATE.md` → `governance/LOCAL_OVERLAY.md` and declare **enforcement maturity** (`L0` minimum; see `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`).
2. Copy `.github/pull_request_template.md` (or merge governance checks into your existing template).
3. Copy CI starter §1 from `usage/CI_STARTER_WORKFLOWS.md` → `.github/workflows/doc-hygiene.yml` (adapt paths).
4. Record import ADR: git tag and/or SHA, `kit-manifest.yml` `version`, bundle name, declared maturity level.

See `usage/ADOPTION_ENFORCEMENT_CONTRACT.md` for Required vs Advisory vs Deferred per level.

## Post-Import Sanity Checklist (Fast)
After importing, verify these within one PR:
- README links to daily enforcement and ADR template.
- If you use a local overlay: precedence is explicit and the overlay is reviewable.
- Minimum CI is enabled (at least doc hygiene + deterministic tests).
- Architecture selection is recorded (ADR) and boundary terms are consistent (core/boundary contracts/integration boundaries).
- No duplicate “rules docs” were created during import.

Recommended (when adopting Copilot/AI agents):
- Add a repo-specific overlay using `governance/LOCAL_OVERLAY_TEMPLATE.md` and include a low-risk execution continuity rule.

## Option A: Copy (Simplest)
Resolve and copy the **`full` bundle** from `kit-manifest.yml` (composes `standard` + `architecture` + `research`, plus `interface/`, `notes/`, and `governance/`).

Do not maintain a parallel folder list — the manifest is the single source of truth for copy paths. For smaller adoption, resolve `minimal`, `standard`, or `standard` + `architecture` / `research` instead of `full`.

After resolution, copy every listed path (files and directories) into your target repo, preserving relative paths. The `standard` bundle includes root meta docs (`kit-manifest.yml`, `VERSIONING.md`, `DEVELOPMENT.md`, `CHANGELOG.md`) referenced by `usage/` workflows.

Then link imported paths from your main README.

### When Copy Is the Right Choice
Copy is the right choice when you want a proven baseline and your main work is enforcing it in your repo (not co-developing the kit).

### Minimal Integration Steps (Recommended)
1. Resolve bundle paths from `kit-manifest.yml` and copy them.
2. In your repo README, add a “Governance” section that links to:

   - `constitution/AI_ENFORCEMENT_DAILY.md`
   - `constitution/AI_ENFORCEMENT.md`
   - `adr/ADR_TEMPLATE.md`
3. Decide where architectural enforcement lives:

   - keep `ci/*_GATES.md` as principles, and implement them in your CI/tooling, or
   - keep them as human-review gates (temporary fallback) until CI exists.
4. Adopt CI progressively to avoid noisy failures in early projects:
   - start with `usage/CI_MINIMUM_ADOPTION.md` (L0 doc hygiene → L1 tests → L2 boundary integrity → L3 risk signals)
5. Enable a low-friction parking-lot for work-in-progress notes:
   - use `notes/committed/` for shared notes
   - use `notes/local/` for personal notes (intentionally ignored by `.gitignore`)

### Common Failure Modes (Copy)
- Teams copy again later and create duplicates (“v2 folder”), causing drift.
- Teams edit the copied kit without recording what changed (rules diverge silently).

## Option B: Git Submodule
Use when you want upstream updates.

High-level steps:
1. Add as submodule.
2. Reference the kit paths from your repo docs.
3. Decide whether CI gates live in the kit or your repo.

### When Submodule Is the Right Choice
Submodule is right when governance is a living dependency and you want improvements (new gates, clarified rules, better auditability) without re-copying.

### Operational Guidance (Submodule)
- Pin to a known commit SHA and update intentionally (e.g., monthly).
- Treat governance updates like dependency updates:

  - create a PR
  - run your doc/CI checks
  - review diffs to rules/gates carefully
- Keep project-specific overlays in your repo (not inside the submodule), so updates stay mergeable.

### Common Failure Modes (Submodule)
- Teams “vendor” a second copy and stop updating the submodule.
- Teams edit inside the submodule path locally (changes get lost or conflict).

## Option C: Fork
Use when you want a customized governance baseline.

### When Fork Is the Right Choice
Fork is right when your organization will maintain a long-lived variant:
- different enforcement constraints
- different audit requirements
- different required output formats

### Common Failure Modes (Fork)
- Fork diverges without a clear policy for upstream cherry-picks.
- Teams over-customize early and lose the benefits of a shared baseline.

## Where Architecture Is Defined (For the AI)
This kit is architecture-neutral by default. The selected architecture (and any hybrids) is defined by:
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` (decision + hybrid rules)
- ADRs written in `adr/` using `adr/ADR_TEMPLATE.md`

Enforcement is style-agnostic and expressed as boundary rules (core vs boundary contracts vs integration boundaries) in:
- `constitution/AI_RULES.md`
- `ci/ARCHITECTURE_GATES.md` and `ci/TEST_GATES.md`

## Related Documents
- `kit-manifest.yml`
- `usage/ADOPTION_BUNDLES.md`
- `VERSIONING.md`
- `README.md`
- `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- `usage/GOVERNANCE_WAIVERS.md`
- `usage/LOCAL_OVERLAY_AND_PRECEDENCE.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `adr/ADR_TEMPLATE.md`

