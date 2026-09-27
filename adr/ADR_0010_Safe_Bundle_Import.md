# ADR 0010: Safe Namespaced Bundle Imports

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status
Accepted on merge to `main`. On a review branch this is the proposed decision; merging the introducing change records maintainer acceptance.

## Context
September audit A-01 reproduced replacement of five host-owned files by literal bundle copying. A-02 found required architecture context missing from both baselines and an upstream all-bundle check failing inside a valid partial import. A catalog of available bundles is not a record of what an adopter selected.

## Decision
Copy selected kit snapshots into a fresh namespaced directory, normally `vendor/AI_governance/`. Preserve relative paths inside that kit root. Existing destinations, including empty directories, are refused. Host agent instructions, workflow/PR entry points, changelog, test commands, version policy, active overlay and project decisions remain project-owned. Merge a short host entry point only after reviewing conflicts; copied projections do not authorize policy overrides.

Distinguish kit-document references from project paths. Kit references resolve under the declared kit root; project source, commands, task paths, ADR outputs and the active overlay resolve under the project root. Existing root-layout imports require a reviewed migration with an ownership inventory, not automatic deletion or movement.

Every baseline includes its manifest catalog, architecture framework and glossary. The remaining architecture corpus, trigger map and interface proposals are optional/upstream context when absent. Baseline requirements remain binding; a missing required file is an incomplete import, not permission to skip a rule.

Permit one scoped standard-library reference tool, `ci/import_bundle.py`, and its separate `ci/bundle_tests/` regressions. This extends the reference-tool exception in ADR-0009 only for safe snapshot copying and read-only source comparison. It is not a general repository script pack, agent runtime, upgrade manager or policy engine. It executes no imported code, activates no workflows, and has no overwrite/delete/merge mode.

The caller converts the pinned source manifest to JSON with yq. Selection recursively resolves extends/composes, takes the union, honors exclusions, and reads tracked regular files from the source working tree. The documented clean-checkout/SHA precondition binds those contents to the recorded revision. Verification compares the declared selected file inventory, bytes and executable bits; it does not require unselected optional files.

## Alternatives Considered
- Continue root copying with a warning: leaves project/kit ownership ambiguous and invites accidental replacement on upgrades.
- Add overwrite/three-way merge automation: much larger surface; resolving policy precedence is a review decision.
- Require full imports: avoids some missing paths by over-importing the corpus and does not solve collisions.
- Duplicate inline import logic: harder to exercise negative cases consistently than one scoped reference implementation.

## Trade-Offs
Namespacing requires a host entry point and an explicit distinction between kit and project roots. Python 3.9+, Git and yq are needed for the reference procedure, but minimal imported contents remain documentation-only; equivalent reviewed manual staging is possible. Byte comparison intentionally rejects local snapshot edits: put project policy in the overlay or declare a fork.

## Sensitivity Points & Risks
- The source checkout and JSON conversion must represent the reviewed revision; the tool does not fetch or authenticate upstream.
- Exclusive target ownership is required. Path/symlink checks are not a sandbox against a concurrent malicious filesystem writer.
- Interrupted or failed copies may leave only their new destination incomplete. The tool never deletes it and refuses overwrite retries.
- A valid snapshot does not prove semantic governance correctness or proper host entry-point integration.
- Executable-bit verification is omitted on Windows. No Windows-specific runner was used for acceptance; the reference CI runs on Linux.

## Points of No Return
No downstream migration or active snapshot replacement is performed in the kit repair. Roll back a proposed adoption before merge by removing only the newly owned snapshot/entry-point changes after review, preserving host-authored content. Existing adopters can retain their old layout until a deliberate migration.

## Consequences
Minimal gains three documents/catalog entries; standard/full inherit them and include the helper/tests through `ci/`. The manifest schema and bundle names remain unchanged. Workflow YAML and PR templates remain upstream-only setup inputs at the same revision. The kit's all-bundle integrity checks stay upstream; adopter evidence verifies the declared selection. Other September findings remain separate repairs.

## Enforcement
Run the dedicated bundle suite using a JSON conversion of the real manifest. Exercise empty and existing host projects, all supported bundle combinations, existing destinations, missing/tampered/extra files, exclusions, cycles, unknown selections, traversal, symlinks, spaces and executable bits. Retain all existing AEP, ADR and doc-hygiene controls while this decision is reviewed.

## Documentation Impact
Source of truth: `usage/HOW_TO_IMPORT.md` for the adoption procedure and `kit-manifest.yml` for contents. Update projections, normative path-context notes, bundle/CI/overlay guides, development verification, changelog and audit disposition. These are authored sources, not generated documents.

## Governance Change
- Import behavior change: yes; fresh namespaced copies replace the unsafe unconditional root-copy recommendation.
- Normative applicability: unchanged; required baseline context is supplied, and optional references are labeled explicitly.
- Enforcement: add scoped bundle regressions to existing doc hygiene; do not alter branch protection or promote maturity requirements.
- Migration: stage a new snapshot, preserve local ownership/edits, review host integration, then replace only kit-owned material through a separate adoption decision.

## Related Documents
- `usage/HOW_TO_IMPORT.md`
- `usage/ADOPTION_BUNDLES.md`
- `usage/AUDIT_REPORT.md`
- `usage/FIX_PLAN.md`
- `adr/ADR_0009_Structured_AEP_Validation.md`
