# ADR 0014: Claim Card Registry

_Provenance: This ADR originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Status

Proposed

## Context

Theses from other projects enter this kit as prose. Reference validators already have positive and negative fixtures for a few checks. A new sentence can still land in `constitution/` or in advisory guidance with no record of what would falsify it, and a green doc-hygiene run does not close that gap.

Constraints: no new workflow, no adopter mandate, no agent runner, and no second task form beside the Autonomous Execution Plan (AEP). Python standard library only. `constitution/` stays the normative source; this registry must not copy rules into a parallel policy.

## Decision

Keep one advisory registry, `ci/claim_cards.json`, of claims that are already visible in this repo or are proposed for absorption. Each card names the claim, its layer, the kind of check that could falsify it (`canary`, `declaration`, `scenario`, or `none`), the status of that check, a pass that still would not prove the claim, and an anchor that must appear in a repository file.

`ci/validate_claim_cards.py` checks that shape and these promotion rules:

- `none` stays `research` or `advisory`, and `open`
- `integrated` is a `canary` whose evidence path is a `ci/gate_tests/*.py` file and whose anchor is a `def test_` line that unittest collects from that file. A mention of the name is not enough. The checker does not run the test.
- `normative` is allowed only as an integrated canary
- a `scenario` may be `open` or `probed` and is not `integrated`

The existing `doc-hygiene` job already runs `ci/gate_tests`. Extend that job's path filters so a registry-only or validator-only edit starts the same job. Do not add a workflow or a required adopter check.

An edit under constitution/ that adds a thesis and does not change the claim-card registry still passes this checker.

Out of scope: scanning prose for unregistered sentences, running B5–B8, grading whether a probed result is true, and promoting any current card to `normative`.

## Alternatives Considered

- Prose in `usage/AGENT_EVALUATION.md` only. Reviewable, and it does not fail when a card drops its anchor or promotes itself without a canary.
- A new benchmark service or mandatory gate on every constitution edit. Duplicates host and kit runners and pretends the checker can see semantic novelty. Deferred until a concrete false adoption shows the registry is not enough.
- Permanently red CI for known holes. That blocks unrelated repair. Known holes stay `open` or `probed` cards whose status is pinned by the regression test.

## Trade-Offs

The registry makes an absorbed thesis reviewable and stops a normative promotion that has no canary. Maintaining a card is cheaper than a new platform and more durable than a pilot note alone.

The checker validates declarations and anchors, not reality. A probed scenario card can assert an observation the checker never reruns. Fabricated prose inside the required fields passes. The constitution blind spot above is deliberate: closing it needs a different check, and this decision does not pretend the registry is that check.

## Sensitivity Points & Risks

- Anchors shorter than the enforced minimum can latch onto incidental wording. The checker requires sixteen characters.
- Renaming a test or editing a cited sentence breaks the card until the anchor is updated. That is the intended latch.
- Authors can set `probed` without a new run. The standing-card test pins the initial statuses so a silent upgrade fails this suite.
- A collected canary shows the test is in the suite. It does not run the test, and it does not prove the assertion matches the claim.

## Points of No Return

No service, bundle schema change, or adopter migration is introduced. Rollback is deleting the registry, validator, regression test, path-filter entries, and the advisory paragraphs that point at them. Constitutional rules stay as they are.

## Consequences

Standard and full imports receive the registry and checker through the existing `ci/` selection. Minimal stays documentation-only. Importing the files does not activate a gate. Kit `doc-hygiene` runs the regression tests; adopters do not.

Initial cards record limits that are already written down, including the checker's failure to see an unregistered constitution sentence. None start as `normative`.

The DOC DELTA and governance-waiver advisories are integrated canaries. A warning still exits 0. Neither card is normative, and neither becomes an adopter requirement. Doc hygiene root-file, Provenance header, new-doc link, and bundled cross-ref steps are also integrated canaries. The cross-ref canary supplies the path list that yq would print; it does not run the pinned yq binary or lychee.

## Enforcement

- Checker: `ci/validate_claim_cards.py`
- Regressions: `ci/gate_tests/test_claim_cards.py`, invoked by the existing `doc-hygiene` job
- Path filters: `.github/workflows/doc-hygiene.yml` includes the checker and the registry
- Human rule: `usage/AGENT_EVALUATION.md`; absorption template: `research/EXTERNAL_PROJECT_EVALUATIONS.md`
- Status map: `usage/ENFORCEMENT_MATRIX.md`

## Documentation Impact

- Source of truth for the promotion rule: this ADR, implemented by `ci/validate_claim_cards.py`
- Docs updated: `usage/AGENT_EVALUATION.md`, `usage/ENFORCEMENT_MATRIX.md`, `usage/AI_ENGINEERING_METHODS.md`, `research/EXTERNAL_PROJECT_EVALUATIONS.md`, `research/SPEC_KIT_SPEC_GATES_PILOT.md`, `DEVELOPMENT.md`, `README.md`, `CHANGELOG.md`, `adr/README.md`
- Docs removed: none
- Generated docs: no

## Governance Change

- Is this a governance change? yes — advisory reference check and kit path filters; constitutional rules unchanged
- Imported kit upgrade: no
- Local overlay impact: none
- Enforcement impact: kit `doc-hygiene` runs additional regressions in the existing test step. No new required status and no adopter CM change
- Migration: none. Downstream pins move only if a host chooses to copy the checker; copying it does not scan that host's constitution

## References

- `usage/AGENT_EVALUATION.md`
- `adr/ADR_0011_Gate_Input_Validation.md`
- `adr/ADR_0013_Test_Evidence_And_Runner_Conformance.md`
- `research/SPEC_KIT_SPEC_GATES_PILOT.md`
