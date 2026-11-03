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
- `integrated` is a `canary` whose evidence path is a `ci/gate_tests/*.py` file and whose anchor is a `def test_` line that unittest collects from that file and whose body asserts something. A mention of the name, a collected method that does not assert, an assertion made only of literals, or a name assigned from a literal in that straight-line block is not enough. The checker does not run the test. A value produced by a call can still be constant at runtime.
- `normative` is allowed only as an integrated canary
- a `scenario` may be `open` or `probed` and is not `integrated`

The existing `doc-hygiene` job already runs `ci/gate_tests`. Extend that job's path filters so a registry-only or validator-only edit starts the same job. Do not add a workflow or a required adopter check.

An edit under constitution/ that adds a thesis and does not change the claim-card registry still passes this checker. Kit `doc-hygiene` is a separate path coupling: a pull request that changes `constitution/` fails unless `ci/claim_cards.json` is added or modified in that diff and is present at the tested revision. A typo needs the same touch. The touch does not prove the new sentence has a meaningful card. Adopters do not run this step.

## Closure

Self-test for this repo is closed when the coupling above is in kit `doc-hygiene`, every claim card is an integrated canary, and the limits below stay accepted.

Accepted limits that do not block closure:

- The checker does not execute canaries. `ci/gate_tests` does.
- The checker does not fold values returned by calls.
- The ADR presence check does not judge rationale.
- The evidence helper does not open evidence paths or prove a runner wrote the report.
- The finding comparator does not launch a scanner.
- AEP schema version 1 has no method field.
- A green doc-hygiene result does not close an audit finding.
- Unit tests run lychee offline. Online URL checks stay in CI.
- The recorded native stop session is not re-run.
- Scenarios B5–B8 have no matched trial in this repo.
- Constitution prose is not classified sentence by sentence.
- No claim card is normative.
- There is no new adopter gate.

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

The DOC DELTA and governance-waiver advisories are integrated canaries. A warning still exits 0. Neither card is normative, and neither becomes an adopter requirement. Doc hygiene root-file, Provenance header, new-doc link, bundled cross-ref, and manifest path steps are also integrated canaries. Stub yq canaries supply the path list. A separate canary runs the yq release named in the workflow against this repo's manifest. Another runs the named lychee release offline against the hub files and a missing local link. Offline mode does not prove remote URLs. The Cursor stop script is an integrated canary of its stdin contract, including the fail-open paths. That call does not show that the native host dispatched the hook. The ADR presence check is an integrated canary that a numbered file whose body is only TODO still passes. Exit 0 does not judge the rationale. The test-evidence helper is an integrated canary that hand-written JSON assesses as VERIFIED without a runner or an evidence file. Schema version 1 is an integrated canary that a READY plan with no method field still passes. PASS does not show that a method was compared. The finding comparator is an integrated canary that hand-written reports with no new identity pass and are not modified. That pass does not show that a scanner ran. An unregistered file under constitution/ is an integrated canary that the checker still passes and does not copy the new sentence into a card. Closing that hole would be a different check. A passing doc-hygiene root-file step is an integrated canary that an open-finding note stays unchanged. Exit 0 is not release readiness. The recorded native stop session, the absence of a B5–B8 trial record, and the unwired provable-enforcement fragment are integrated canaries of those limits. None of them re-runs the host, a matched trial, or the fragment.

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
- Enforcement impact: kit `doc-hygiene` runs the claim-card regressions and, on pull requests, the constitution-to-registry path coupling. No new workflow, no new required status, and no adopter CM change
- Migration: none. Downstream pins move only if a host chooses to copy the checker; copying it does not scan that host's constitution

## References

- `usage/AGENT_EVALUATION.md`
- `adr/ADR_0011_Gate_Input_Validation.md`
- `adr/ADR_0013_Test_Evidence_And_Runner_Conformance.md`
- `research/SPEC_KIT_SPEC_GATES_PILOT.md`
