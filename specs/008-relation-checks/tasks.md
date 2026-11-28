# Tasks — 008 relation checks

Execute from `spec.md`. Do not change `resolve_paths` unless a relation in Task 2 fails. Do not delete the 2026-11-28 verdict sentences.

## Task 1 — ADR-0020

Add `adr/ADR_0020_Local_Oracle_Relations.md` from `adr/ADR_TEMPLATE.md`. Status Proposed. Decision: the three checks in `spec.md`, existing unittest discovery, no new adopter workflow and no new dependency. Alternatives rejected: a mutation tool, a YAML parser, and a repository-wide spec linter.

## Task 2 — Metamorphic relation

Create `ci/gate_tests/test_bundle_relations.py`.

- Kit-shaped fixture from the spec: two `resolve_paths(..., ["minimal"])` calls return equal paths and excludes.
- Minimal paths are a subset of standard paths, which are a subset of full paths.
- The exclude list is the same for `minimal`, `standard`, and `full`.
- `architecture/rag/` is absent from minimal and present in full.
- A fixture whose `standard` bundle does not extend `minimal` and omits `kit-manifest.yml` is not monotone.
- `kit-manifest.yml` contains `extends: minimal` and the full bundle composes `standard`, `architecture`, and `research`.

Add the "Metamorphic relations" section to `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` immediately after "Defect seeding (bebugging)".

Run: `python3 -m unittest ci.gate_tests.test_bundle_relations -q`  
Expected: OK.

## Task 3 — Requirement and behavior tokens

Create `ci/spec_token_check.py` with `cross_check(spec_ids: list[str], code_tokens: list[str]) -> dict[str, list[str]]` and the keys `missing_from_code` and `missing_from_spec`.

Create `ci/gate_tests/test_spec_token_check.py` for the plant and the benign control in `spec.md`. Point `local_spec_findings` at `cross_check`.

In `ci/gate_tests/test_bebugging_seeds.py`, expect `current_spec_findings(ROOT)` to be `["checker-present"]`. Keep the token assertions. Rename that test to `test_spec_drift_is_caught_by_cross_check`.

Run: `python3 -m unittest ci.gate_tests.test_spec_token_check ci.gate_tests.test_bebugging_seeds.BebuggingSeeds.test_spec_drift_is_caught_by_cross_check -q`  
Expected: OK.

## Task 4 — Resume hash

Create `ci/resume_ledger.py` with `stale_paths(ledger_text: str, read_bytes) -> list[str]`. The docstring contains `progress.md` and `different hash`. Parse `` - `path` sha256 `64 hex digits` ``. Return sorted paths whose current sha256 differs.

Create `ci/gate_tests/test_resume_ledger.py` with the plant, the matching listed path, and the unlisted path from `spec.md`. Use a fixture ledger, not `specs/001-benchmark-trial-records/progress.md`.

In `test_bebugging_seeds.py`, expect `resume_hash_is_executable(ROOT)` to be true. Rename that test to `test_stale_resume_hash_is_executable`.

Run: `python3 -m unittest ci.gate_tests.test_resume_ledger ci.gate_tests.test_bebugging_seeds.BebuggingSeeds.test_stale_resume_hash_is_executable -q`  
Expected: OK.

## Task 5 — Skill-copy parity

Create `ci/skill_copies.py` with `differing_shared_paths(left: Path, right: Path) -> list[str]`.

Create `ci/gate_tests/test_skill_copies.py`.

- Temporary trees: one shared path with different bytes is returned; an identical pair returns an empty list; a file on only one side is not returned.
- `differing_shared_paths` on `.cursor/skills` and `.github/skills` is empty.
- The test source contains both `read_bytes()` strings from `spec.md`, and those two real files compare equal.

In `test_bebugging_seeds.py`, expect `parity_check_exists(ROOT)` to be true. Keep the assertion that the two governed-work copies match. Rename that test to `test_instruction_copies_have_a_parity_check`.

Run: `python3 -m unittest ci.gate_tests.test_skill_copies ci.gate_tests.test_bebugging_seeds.BebuggingSeeds.test_instruction_copies_have_a_parity_check -q`  
Expected: OK.

## Task 6 — Procedure index and follow-up

- Add the method-selector row and the glossary entry specified in `spec.md`.
- Add one Unreleased changelog bullet: the three checks exist and no adopter gate was added.
- Add the follow-up paragraph in `research/EXTERNAL_PROJECT_EVALUATIONS.md` after the 2026-11-28 seed verdicts. Do not remove verdict sentences.
- Add the short paragraphs for the token check, resume hash, and parity next to the metamorphic section.

## Task 7 — Ledger

Record commands and results in `progress.md`. Do not commit unless the operator asks.
