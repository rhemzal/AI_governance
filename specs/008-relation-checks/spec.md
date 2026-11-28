# Relation checks (008)

Plan: `tasks.md`  
AEP: `aep.md`  
Scope: three local checks for gaps left by the 2026-11-28 defect-seeding survey. Not a new verification product, not an adopter-mandatory gate, and not property-based testing, fuzzing, mutation tooling, or chaos.

## Objective

Make three techniques executable the way bebugging already is: one metamorphic relation on bundle selection, the two local checks that survey named and did not build, and byte parity of the two skill trees.

## Rulings

- Ruling: the metamorphic check calls `ci.import_bundle.resolve_paths`. It does not add a YAML parser or a PyYAML dependency. `ci/import_bundle.py` reads JSON only. A yq-versus-PyYAML differential is out of scope.
- Ruling: the fixture dict uses the same edges as `kit-manifest.yml`: `standard` extends `minimal`, `full` composes `standard`, `architecture`, and `research`. The test also asserts those words are present in `kit-manifest.yml`.
- Ruling: the requirement cross-check is a pure function of two token lists. It does not scan the repository for `REQ-` strings. Prose specs are not a token registry.
- Ruling: the resume checker parses ledger lines of the form `` - `path` sha256 `64 hex digits` ``, matching `specs/001-benchmark-trial-records/progress.md`. A different hash is stale. A path the ledger does not name is quiet. The unit test uses a fixture ledger. It does not fail the suite when an old feature ledger has drifted.
- Ruling: parity compares bytes of paths that exist on both `.cursor/skills/` and `.github/skills/`. The governed-work pair must exist on both sides. Files that exist only under `.github/skills/` are the pinned procedure copies (19 files on 2026-11-28) and are not drift.
- Ruling: the 2026-11-28 verdict sentences stay in `ci/gate_tests/bebugging_seeds.py` `VERDICTS` and in `research/EXTERNAL_PROJECT_EVALUATIONS.md`. The seed tests that assert the three checks are absent change to assert that each check catches its plant and stays quiet on the benign control. A follow-up paragraph records that the checks now exist.

## Checks

| Technique | Plant | Benign control | Home |
| --- | --- | --- | --- |
| Metamorphic relation | `standard` does not extend `minimal`, so minimal paths are not a subset of standard paths | Kit-shaped fixture: two `resolve_paths` calls on `minimal` return the same paths and excludes; `minimal` paths ⊆ `standard` paths ⊆ `full` paths; the exclude list does not change with the baseline; `architecture/rag/` is absent from `minimal` and present in `full` | `ci/gate_tests/test_bundle_relations.py` calling `resolve_paths` |
| Requirement / behavior tokens | `REQ-GONE` is in the spec list only; `BEHAVE-NEW` is in the code list only | `REQ-KEEP` and `REQ-UNRELATED` are in both lists and produce no finding | `ci/spec_token_check.py` `cross_check(spec_ids: list[str], code_tokens: list[str]) -> dict[str, list[str]]` with keys `missing_from_code` and `missing_from_spec` |
| Resume hash | Listed path whose bytes hash differently from the recorded sha256 | Listed path whose hash matches, plus an unlisted path whose bytes differ | `ci/resume_ledger.py` `stale_paths(ledger_text: str, read_bytes) -> list[str]` |
| Skill-copy parity | One shared relative path with different bytes | Identical shared bytes; the real governed-work pair is equal | `ci/skill_copies.py` `differing_shared_paths(left: Path, right: Path) -> list[str]` |

`cross_check` is the single implementation. `ci.gate_tests.bebugging_seeds.local_spec_findings` delegates to it. After that module exists, `current_spec_findings` returns `["checker-present"]` because the module contains both result keys.

`stale_paths` docstring contains the phrases `progress.md` and `different hash`, which is what `resume_hash_is_executable` already searches for under `ci/`.

The parity test file other than `test_bebugging_seeds.py` contains both of these source strings, because `parity_check_exists` searches for them:

```text
.cursor/skills/governed-work/SKILL.md").read_bytes()
.github/skills/governed-work/SKILL.md").read_bytes()
```

Those calls compare the real files. `differing_shared_paths` covers the plant, the benign pair, and every shared path in the two skill trees.

## Documents

- `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`: a "Metamorphic relations" section immediately after "Defect seeding (bebugging)", plus one short paragraph each for the token cross-check, the resume hash, and skill-copy parity, pointing at the modules above.
- `usage/AI_ENGINEERING_METHODS.md`: one selector row after the defect-seeding row: observed need "No exact expected value, but a relation between two runs is known"; candidate "One metamorphic relation and one benign control"; evidence "The relation fails when broken and holds for the accepted pair"; stop "The relation is true of both good and bad implementations".
- `architecture/TERMINOLOGY_GLOSSARY.md`: under Testing, after the Mutation testing entry, define metamorphic testing as checking a relation between two runs when the exact expected value is not enumerated.
- `CHANGELOG.md` Unreleased: one advisory bullet naming the three checks and stating that no adopter gate was added.
- `research/EXTERNAL_PROJECT_EVALUATIONS.md`: a follow-up after the 2026-11-28 seed verdicts. Keep every existing verdict sentence.
- `adr/ADR_0020_Local_Oracle_Relations.md`: the decision to add these checks under existing `ci/gate_tests` discovery. Status Proposed. No constitution change, no new workflow, no new dependency.

## Acceptance

- The four test modules pass, and `ci.gate_tests.test_bebugging_seeds` still passes.
- `current_spec_findings` reports the checker, `resume_hash_is_executable` is true, and `parity_check_exists` is true.
- Each plant fails the check and each benign control stays quiet.
- `kit-manifest.yml` still shows `extends: minimal` and a `full` composes list of `standard`, `architecture`, and `research`.
- Historical verdict sentences remain. The follow-up says the three checks exist.
- `python3 ci/validate_aep.py < specs/008-relation-checks/aep.md` prints `PASS: READY`.

## Out of scope

Property-based generators, fuzzing, a mutation-testing tool, chaos, scanning every spec for requirement tokens, forcing the two skill trees to contain the same file list, a second manifest reader, a claim card, and installing OpenSpec, SpecGov, GSD Core, or Ruler.
