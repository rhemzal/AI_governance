# ADR 0011: Validate Gate Inputs and Test Copyable Checks

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status
Accepted on merge to `main`. On a review branch this is the proposed decision; merging the introducing change records maintainer acceptance.

## Context
September audit A-03 found boundary recipes passing when the source directory was absent or a normal Python import used a different syntax. A-04 found that deleting an ADR satisfied the decision gate. A-05 reproduced missing comparison history in the copyable ADR workflow. A-07 found that valid alternative Markdown fences made malformed declared plans appear absent. Existing positive tests did not exercise these inputs.

This kit is a documentation/contract product with small reference checks. The stable boundary is the declared gate contract; filesystem, Git and Markdown inputs are failure boundaries. The priorities are truthful failure reporting, reproducible tests and low maintenance cost. Preparing this repair does not promote adopter maturity or activate downstream checks.

## Decision
- Keep boundary and ADR checks inline. Python boundary examples use the standard-library syntax tree without executing source. Configure forbidden import name components; fail visibly on missing/empty/unreadable/invalid sources. Go retains a conservative quoted-path scan, distinguishes scanner error from no match, and states its syntax limitations.
- For governance-prefix changes, require an added/modified numbered regular ADR present at the tested revision. Deleted records, templates, symlinks, type changes and Git-detected renames do not qualify. Include both sides of moves when determining whether governance changed. Fetch full history in the starter, use the same comparison revisions and check as kit CI, and keep PR revision values in environment variables.
- Extend the existing AEP scanner to top-level backtick/tilde fences of at least three characters with up to three leading spaces. Require a complete matching close, reject multiple declarations and explicitly unsupported declaration placement/info. Ignore literal examples inside other fenced blocks. Preserve schema version 1 and advisory handling of genuinely absent plans.
- Permit the scoped `ci/gate_tests/` regression fixtures for the existing inline checks, in addition to ADR-0009/0010's reference-tool exceptions. Run them in existing doc hygiene. This adds no general script pack, runtime gate helper, agent framework or product test requirement.

## Alternatives Considered
- Patch only the original regexes: does not adequately handle ordinary Python syntax or distinguish Markdown declaration content from examples.
- Add general dependency/Markdown/policy frameworks: broader dependencies and maintenance than these demonstrated defects justify. Adopters with complex dependency graphs should use stack-specific tooling.
- Add standalone runtime helpers for all checks: simplifies duplication but expands the kit tool surface. Inline examples plus parity and execution tests suffice for this repair.

## Trade-Offs
Python boundary checks trade a few more lines for static syntax coverage. Their component-name policy can reject an ordinary same-named symbol and does not resolve dynamic or transitive dependencies. The Go scan can flag comments and miss escaped literals; it is a tripwire, not complete architectural proof. ADR checking adds Python to that optional workflow, already available on the reference runner. Inline duplication is retained, with tests enforcing parity.

## Sensitivity Points & Risks
- Gate code and tests remain reviewable PR changes; passing a contributor-modified check is not independent authorization or branch enforcement.
- Git's rename similarity heuristic is not semantic decision detection. Substantial rewrites/moves and ADR content still require review. Filename/status presence alone cannot prove a valid rationale.
- The AEP scanner is not a full Markdown renderer. Use the documented top-level declaration subset, outside HTML/container markup. Keep examples in a separate enclosing code fence.
- Source roots and forbidden names must match the adopter's actual architecture. Exercise a forbidden-import negative control after configuring a recipe.
- Real permission-denial fixtures require an unprivileged POSIX runner. Root-run environments skip those two cases explicitly; CI must supply that evidence. Scanner exit-status injection remains portable across identities.

## Points of No Return
None in this repair: changes are prepared on a review branch. No downstream imports, branch rules, release tags or deployments change. Consumers update their chosen workflow/recipe and validator from one pinned revision after review; retain the previous snapshot for rollback.

## Enforcement
Run `ci/tests/` for canonical/alternate/incomplete/multiple AEP declarations and ordinary fenced examples. Run `ci/gate_tests/` for copied boundary blocks, allowed/forbidden imports, unavailable inputs, scanner errors, ADR addition/modification/deletion/template/rename/type cases, usage-only controls, and a shallow PR-merge fixture repaired by full history. Keep the bundle suite and existing governance/doc controls active.

Acceptance scenarios: an ordinary forbidden import fails while a core dependency passes; deleting or moving an existing ADR fails while adding/updating a numbered decision passes; a shallow comparison fails visibly and works with both revisions fetched; the same invalid READY payload fails under every supported fence form while valid declarations pass.

## Documentation Impact
Canonical procedure/contracts remain `usage/BOUNDARY_GATE_RECIPES.md`, `usage/CI_STARTER_WORKFLOWS.md` and `usage/AEP_VALIDATION.md`; existing gate principles and applicability are unchanged. Update development commands, implementation status, changelog and audit disposition. These are authored sources, not generated documentation.

## Governance Change
- Tighten existing input validation; no new adopter gate or maturity requirement.
- Standard/full include the scoped regression fixtures via their existing `ci/` path; minimal remains documentation-only.
- Meaning, applicability, authority and completion still require review. This scoped retest does not close the release audit.

## Related Documents
- `usage/BOUNDARY_GATE_RECIPES.md`
- `usage/CI_STARTER_WORKFLOWS.md`
- `usage/AEP_VALIDATION.md`
- `usage/ENFORCEMENT_MATRIX.md`
- `usage/AUDIT_REPORT.md`
- `usage/FIX_PLAN.md`
- `adr/ADR_0009_Structured_AEP_Validation.md`
- `adr/ADR_0010_Safe_Bundle_Import.md`
