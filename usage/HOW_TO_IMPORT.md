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

## Kit root, project root, and file ownership

The **kit root** holds the imported snapshot, normally `vendor/AI_governance/`. All manifest paths and references to kit documents are relative to that root. The **project root** owns application code, test commands, task paths, project ADRs, the active `governance/LOCAL_OVERLAY.md`, and agent/workflow entry points. Do not run the kit's maintainer commands as if they were the project's test suite.

| Material | Destination / action |
| --- | --- |
| Selected kit files, including its agent projections and root meta docs | Fresh kit root, preserving paths inside that root |
| Host `AGENTS.md` and `.github/copilot-instructions.md` | Preserve existing content; merge a short entry point after resolving policy conflicts |
| Host `CHANGELOG.md`, `DEVELOPMENT.md`, `VERSIONING.md` | Remain project-owned; kit copies stay below the kit root |
| Active overlay and project adoption/architecture ADRs | Project-owned paths outside the imported snapshot |
| PR template and workflow YAML | Upstream-only setup inputs from the **same pinned revision**; merge/adapt into host-owned files only when adopting the gate |

A full manifest catalog is included in every baseline. Record the actual selected bundles separately in the host entry point/overlay; catalog membership does not mean an optional bundle was imported. Minimal includes the architecture framework and glossary required by the constitution; the remaining architecture corpus and trigger map are optional upstream/add-on context.

## Option A: Copy into a fresh kit directory

Choose `minimal` or `standard`, with declared optional add-ons. Use `full` only with the justification in `usage/ADOPTION_BUNDLES.md`. Resolve recursive `extends` / `composes`, union/deduplicate paths, and honor `exclude`. Never recursively copy the kit over the project root or an existing kit directory.

The reference tool `ci/import_bundle.py` is in the **pinned upstream checkout** (and standard/full imports). It requires Python 3.9+ and Git; convert the manifest with yq v4.44.3. Minimal imports remain documentation-only: running the upstream import tool does not add Python scripts to the imported bundle.

Before copying:

1. Obtain a reviewed, clean kit checkout at a specific commit; do not rely on a floating branch or an unverified advertised tag.
2. Identify the project root, selected bundles and unused destination. Inspect existing host agent instructions, overlay, workflow/PR template, ADRs and root meta files. List conflicts and the intended manual integration; copying does not authorize overriding them.
3. Use exclusive ownership of the target directory during the copy. The helper refuses existing targets, symlinks, traversal paths and non-regular selected Git entries. It is not a sandbox against a concurrent process changing filesystem paths.

Set `KIT_SOURCE`, `KIT_REVISION` (full commit SHA), and `PROJECT_ROOT` to the reviewed checkout/revision and existing target project directory. Run from a shell with yq v4.44.3 available:

```bash
set -euo pipefail
: "${KIT_SOURCE:?Set the pinned upstream checkout path}"
: "${KIT_REVISION:?Set its reviewed full commit SHA}"
: "${PROJECT_ROOT:?Set the existing target project directory}"
test -d "$PROJECT_ROOT"
test "$(git -C "$KIT_SOURCE" rev-parse HEAD)" = "$KIT_REVISION"
git -C "$KIT_SOURCE" diff --exit-code HEAD --
KIT_IMPORT_JSON=$(mktemp)
trap 'rm -f "$KIT_IMPORT_JSON"' EXIT
yq -o=json '.' "$KIT_SOURCE/kit-manifest.yml" > "$KIT_IMPORT_JSON"
python3 "$KIT_SOURCE/ci/import_bundle.py" \
  --manifest-json "$KIT_IMPORT_JSON" --source "$KIT_SOURCE" \
  --destination "$PROJECT_ROOT/vendor/AI_governance" --bundle standard
python3 "$KIT_SOURCE/ci/import_bundle.py" \
  --manifest-json "$KIT_IMPORT_JSON" --source "$KIT_SOURCE" \
  --destination "$PROJECT_ROOT/vendor/AI_governance" --bundle standard --check
```

Use the same selection for copy and check. Change `--bundle standard` to `--bundle minimal` for the small baseline, or append `--bundle architecture` / `--bundle research` as declared. `--bundle full` is used alone. The helper reads **Git-tracked working-tree files** from the source; the clean-revision check above binds them to the recorded SHA. Untracked files are never imported. The JSON input must be converted from that checkout's manifest; the helper does not fetch or infer an upstream revision.

A successful check means selected file inventory, contents and executable bits match that source (executable-bit comparison is omitted on Windows). It does not validate the semantic quality of the source rules, activate CI, establish adoption precedence, or prove host instructions were merged correctly. Review those separately. No imported code or instructions are executed by the helper.

A failed or interrupted copy can leave its **new** destination incomplete. The tool never deletes or repairs a target and refuses retries into existing directories. Inspect the failed copy and clean up only the directory owned by that attempt, or choose a fresh staging path. Do not reset unrelated project changes.

### Integrate host entry points deliberately

After snapshot verification, merge a small block like this into the existing host `AGENTS.md` and, when used, `.github/copilot-instructions.md`. Keep all existing constraints, project commands and provenance; reconcile any conflicts explicitly in the adoption decision/overlay before making the kit a baseline.

```markdown
## Governance baseline
- Kit root: `vendor/AI_governance/`.
- Selected bundles and upstream commit: record the reviewed selection and full SHA here.
- Read `vendor/AI_governance/AGENTS.md` and its core references as applicable.
- For non-trivial work apply AI_RULES §6.5 in existing task evidence. Follow the
  project's adopted verification controls; use the kit method selector when needed.
- Kit-document references resolve under that kit root; project source, test commands,
  task paths, project ADRs and the active local overlay resolve from this project.
- Existing project instructions remain in effect; approved policy overrides are
  recorded explicitly in `governance/LOCAL_OVERLAY.md`.
```

Replace the selection/SHA instruction with actual values during integration. Add project README links to the imported daily enforcement and ADR template using the real kit-root prefix. Keep the imported snapshot unchanged and put project decisions/overrides outside it; otherwise the source comparison will intentionally fail.

### Post-import enforcement setup

For `standard`/`full`, use the imported overlay template to create or merge the **project's** active overlay and declare CI Maturity (CM). Fetch the PR template and any chosen workflow from the same upstream revision; neither is silently included by the manifest. Preserve existing host files and adapt paths/triggers, including the prefix of any retained validator.

The upstream `doc-hygiene` job validates the **entire kit**. Its all-bundle manifest and cross-reference checks must not be copied into a partial adopter unchanged. Use the selected-source comparison above or the corresponding manual inventory review; check actual project links/provenance separately. See `usage/CI_STARTER_WORKFLOWS.md` §1 and `usage/ADOPTION_ENFORCEMENT_CONTRACT.md` for CM defaults. Product tests are introduced at CM1 when they exist, not invented during CM0 import.

Record adoption in the project's decision record: kit root, source SHA, manifest version, selected bundles, CI maturity, retained host constraints and any approved overrides. Confirm that the agent can find required baseline documents through the merged entry point, and that no host metadata/test command was replaced with the kit's own content.

### Existing root-layout imports and updates

This layout change does not automatically migrate or delete an older import. Inventory ownership and local edits first. Prepare a new namespaced snapshot from the reviewed revision, compare old/new rules, and reconcile host entry points/overlays in a migration PR. Remove old kit copies only after proving they are kit-owned and that references have moved; preserve host-authored content and history.

For later updates, build and verify a fresh candidate directory outside the active kit root, then review old/new content and the host integration. Replacing the active snapshot is a separate reviewed update, not an overwrite mode of the importer. Local modifications indicate a fork/overlay decision; do not discard them to satisfy a byte comparison.

### Verify behavior after a governance upgrade

The update is incomplete until the active host instruction route, local overrides and
selected verification commands agree with the reviewed pin. Use
[Engineering Methods Adoption](ENGINEERING_METHODS_ADOPTION.md) to pilot one real task,
record the existing command's outcome, and decide what becomes a local requirement.
Old copies and forks do not receive new behavior automatically. A successful byte comparison
proves snapshot integrity only; it does not prove agent compliance or effective adoption.

## Option B: Git Submodule
Use when you want upstream updates.

High-level steps:
1. Add the reviewed source as a submodule at an unused kit-root path; preserve existing project files.
2. Merge host entry points using the kit/project-root distinction above. A submodule contains the whole upstream tree; declare which governance material is adopted, and do not use the selected-copy inventory check against an unfiltered submodule.
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

