# AEP Validation Specification

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

An Autonomous Execution Plan (AEP) records the next executable steps and their bounds. Normative applicability and authority are defined in `constitution/AI_ENFORCEMENT.md` §§1.1–1.4. A valid declaration is not evidence that work was executed or its results are correct.

## Applicability and readiness

- Required: HIGH-risk changes, non-trivial work with dependent steps, handoff, or concurrent agents.
- Routine reversible work may use a concise scope and verification statement, including necessary helper/test/doc edits. File count alone does not determine risk or require a full plan.
- `READY`: the next planned actions are authorized and have no unresolved blocking questions. Bounded discovery is permitted; specify known paths/inputs and the decision or evidence it must produce.
- `BLOCKED`: record the actual missing input, authority, or decision. Stop the affected action; independent authorized work may continue.
- `NOT-REQUIRED`: explain why a concise plan is sufficient. This is an applicability declaration, not an exemption from verification or authority checks.
- Update the plan as evidence changes within the mandate. A new objective or unauthorized effect needs approval before that action. Record budget changes explicitly; do not silently restart exhausted repair loops.

## Required content

READY/BLOCKED plans contain an objective, discovery evidence/assumptions, risk, scope and effects, ordered steps with known paths and reasons, explicit verification, acceptance criteria, blocking questions, repair budget, and documentation impact. A BLOCKED plan has at least one concrete blocker; READY has none.

Conversational plans may be concise prose. When submitting an AEP to the kit PR validator, serialize it as a single fenced `aep` JSON block. This avoids ambiguous parsing of Markdown headings and unrelated PR prose.

## Structured PR format (schema version 1)

````markdown
```aep
{
  "schema_version": 1,
  "status": "READY",
  "objective": "Correct the adoption example so it matches the documented command.",
  "discovery": ["Read README.md and DEVELOPMENT.md; this is a documentation-only change."],
  "risk": "LOW",
  "scope": {
    "paths": ["README.md"],
    "allowed_effects": ["Edit and verify the task branch"],
    "approval_required": ["Merge", "Deploy"]
  },
  "steps": [
    {"paths": ["README.md"], "action": "Correct the adoption example", "reason": "Align with the documented command"}
  ],
  "verification": [
    {"command": "git diff --check", "expected": "Exit 0; manually compare the example with DEVELOPMENT.md"}
  ],
  "acceptance": ["Example matches the documented command; no unrelated changes."],
  "blocking_questions": [],
  "budget": {"max_repair_attempts": 2, "on_exhaustion": "Stop the affected action and report evidence plus the next decision."},
  "doc_delta": "Correct README adoption example; no runtime behavior change."
}
```
````

This example shows serialization; the routine change described would normally need only a concise scope/verification statement.

For an inapplicable full AEP, the complete block is:

````markdown
```aep
{"schema_version": 1, "status": "NOT-REQUIRED", "reason": "Routine reversible spelling correction; no dependent steps, handoff, or concurrency."}
```
````

## Machine-checkable contract

The reference validator is `ci/validate_aep.py` (Python 3 standard library, included in the `standard` bundle through `ci/`; minimal adopters can read it from the upstream kit or copy it explicitly).

| Field | Shape |
| --- | --- |
| `schema_version` | Integer `1` |
| `status` | `READY`, `BLOCKED`, or `NOT-REQUIRED` |
| `objective`, `doc_delta` | Non-empty text; describe no documentation impact with a reason |
| `discovery`, `acceptance` | Non-empty lists of non-empty strings |
| `risk` | `LOW` or `HIGH`; justify it in discovery |
| `scope` | Exactly `paths`, `allowed_effects`, `approval_required`; lists of strings; only approval_required may be empty |
| `steps` | Non-empty list of objects with `paths` (non-empty list), `action`, `reason` |
| `verification` | Non-empty list of objects with `command`, `expected`; both non-empty text |
| `blocking_questions` | List; empty for READY, non-empty for BLOCKED |
| `budget` | `max_repair_attempts` (non-negative integer), `on_exhaustion` (non-empty text) |
| `reason` | Only for NOT-REQUIRED; non-empty text; no full-plan fields in this form |

Paths use repository-relative POSIX paths or globs. For multi-repository work, use logical repository prefixes (for example `backend/src/**`) and map them to actual checkouts in the task record. New paths need not exist yet. Path-to-step scope containment and the checkout mapping require review.

The validator rejects duplicate JSON keys, unknown/missing fields, unsupported schema versions/statuses, malformed or multiple `aep` blocks, empty required values, readiness/blocker contradictions, and entire text values that are unresolved placeholders (`TBD`, `TODO`, `later`, `as needed`, `etc.`, `...`). Mentioning these words inside a concrete sentence or outside the AEP is valid. Commands for documentation checks are valid; a test-runner name is not required.

An optional plain `AEP Status: READY` marker must agree with the structured block. A legacy marker without a block fails with migration guidance. Missing declarations remain advisory: multi-file PRs receive a warning to review applicability. Declared plans are checked even for one-file PRs. BLOCKED and NOT-REQUIRED may pass structural validation; neither grants execution authority.

## Verification and limits

```bash
timeout 60s python3 -m unittest discover -s ci/tests -v
python3 ci/validate_aep.py --changed-files 2 < pr-body.md
```

`PR_BODY`, when set, supplies the body instead of stdin. Output starts with PASS, FAIL, WARN, or SKIP; malformed declarations exit 1. The validator reads declaration data only: it never runs supplied verification commands, changes permissions, or authorizes a merge.

Review still checks applicability, risk justification, real authorization, path containment, feasibility, acceptance quality, and whether claimed evidence matches the tested revision/environment. Do not call this semantic validation or proof of correctness. Changes to the validator/gates need governance review under current controls; an agent cannot approve its own weakened checker.

## Migration from the grep gate

Update `.github/workflows/aep-advisory.yml`, the reference validator, and the PR template together, pinned to the same kit revision. Convert legacy PR plans to the structured block. Copy-importers using only the YAML starter must also copy `ci/validate_aep.py`; existing minimal imports do not gain a Python requirement unless they opt into this gate. The machine-readable format change is breaking for repositories using the old gate; review the Unreleased changelog before upgrading.

## Related Documents
- `constitution/AI_ENFORCEMENT.md`
- `governance/LOCAL_OVERLAY_TEMPLATE.md`
- `usage/AI_RUN_EVIDENCE.md`
- `usage/CI_STARTER_WORKFLOWS.md`
- `usage/ENFORCEMENT_MATRIX.md`
- `adr/ADR_0009_Structured_AEP_Validation.md` (upstream kit if not imported)
