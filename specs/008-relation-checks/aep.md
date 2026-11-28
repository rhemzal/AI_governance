# Autonomous Execution Plan — 008 relation checks

AEP Status: READY

```aep
{
  "schema_version": 1,
  "status": "READY",
  "objective": "Add a metamorphic bundle relation, a requirement/behavior token cross-check, a resume-ledger hash compare, and skill-copy byte parity, as local checks only.",
  "discovery": [
    "specs/008-relation-checks/spec.md records the rulings. The 2026-11-28 seed in ci/gate_tests/bebugging_seeds.py already asserts that the token checker, the resume hash compare, and the skill parity test are absent.",
    "ci/import_bundle.resolve_paths unions extends and composes. kit-manifest.yml has standard extends minimal and full composes standard, architecture, and research. The importer reads JSON, so a second YAML reader is not a current dual path.",
    "On 2026-11-28 the 20 paths shared by .cursor/skills and .github/skills had equal bytes. Nineteen further files exist only under .github/skills and are pinned procedure copies.",
    "A progress ledger line in specs/001-benchmark-trial-records/progress.md has the form - `path` sha256 `64 hex digits`.",
    "ci/ and architecture/ are adr-required paths. Risk is HIGH because those governance paths change. The added behavior is deterministic tests plus advisory text. No constitution edit and no new workflow."
  ],
  "risk": "HIGH",
  "scope": {
    "paths": [
      "specs/008-relation-checks/**",
      "adr/ADR_0020_Local_Oracle_Relations.md",
      "ci/spec_token_check.py",
      "ci/resume_ledger.py",
      "ci/skill_copies.py",
      "ci/gate_tests/test_bundle_relations.py",
      "ci/gate_tests/test_spec_token_check.py",
      "ci/gate_tests/test_resume_ledger.py",
      "ci/gate_tests/test_skill_copies.py",
      "ci/gate_tests/bebugging_seeds.py",
      "ci/gate_tests/test_bebugging_seeds.py",
      "usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md",
      "usage/AI_ENGINEERING_METHODS.md",
      "architecture/TERMINOLOGY_GLOSSARY.md",
      "research/EXTERNAL_PROJECT_EVALUATIONS.md",
      "CHANGELOG.md"
    ],
    "allowed_effects": [
      "Add advisory procedure text, one glossary entry, and one method-selector row",
      "Add standard-library checks and unit tests under ci/",
      "Update the three bebugging assertions that currently require those checks to be absent",
      "Add ADR-0020 and a follow-up paragraph that keeps the 2026-11-28 verdict sentences"
    ],
    "approval_required": ["Commit", "Merge", "Push"]
  },
  "steps": [
    {
      "paths": ["adr/ADR_0020_Local_Oracle_Relations.md"],
      "action": "Write ADR-0020 as Proposed: local checks under existing unittest discovery, no new adopter workflow, no new dependency",
      "reason": "ci/ and architecture/ edits fail adr-required unless a numbered ADR is added in the same change"
    },
    {
      "paths": ["ci/gate_tests/test_bundle_relations.py", "usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md"],
      "action": "Lock the resolve_paths relation from spec.md and add the Metamorphic relations section after Defect seeding",
      "reason": "Bebugging stops when a class has no exact oracle; this relation is the kit-sized instance"
    },
    {
      "paths": ["ci/spec_token_check.py", "ci/gate_tests/test_spec_token_check.py", "ci/gate_tests/bebugging_seeds.py", "ci/gate_tests/test_bebugging_seeds.py"],
      "action": "Add cross_check, delegate local_spec_findings to it, and expect current_spec_findings to report checker-present",
      "reason": "The seed named this as the smallest spec-drift check and still asserts that no such module exists"
    },
    {
      "paths": ["ci/resume_ledger.py", "ci/gate_tests/test_resume_ledger.py", "ci/gate_tests/test_bebugging_seeds.py"],
      "action": "Add stale_paths for the ledger hash line and expect resume_hash_is_executable to be true",
      "reason": "The governed-work skill states the stale-hash rule and no ci/ function compares the hash"
    },
    {
      "paths": ["ci/skill_copies.py", "ci/gate_tests/test_skill_copies.py", "ci/gate_tests/test_bebugging_seeds.py"],
      "action": "Add differing_shared_paths, compare the real governed-work copies with the two read_bytes strings the seed searches for, and expect parity_check_exists to be true",
      "reason": "The seed showed the two skill copies can drift with no parity test outside the seed file"
    },
    {
      "paths": ["usage/AI_ENGINEERING_METHODS.md", "architecture/TERMINOLOGY_GLOSSARY.md", "CHANGELOG.md", "research/EXTERNAL_PROJECT_EVALUATIONS.md", "usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md", "specs/008-relation-checks/progress.md"],
      "action": "Add the selector row, glossary entry, changelog bullet, and external follow-up, then record verification. Keep every 2026-11-28 verdict sentence",
      "reason": "The historical seed record must stay true while the new checks become findable"
    }
  ],
  "verification": [
    {
      "command": "python3 ci/validate_aep.py < specs/008-relation-checks/aep.md",
      "expected": "Exit 0 and the first line starts with PASS: READY"
    },
    {
      "command": "python3 -m unittest ci.gate_tests.test_bundle_relations ci.gate_tests.test_spec_token_check ci.gate_tests.test_resume_ledger ci.gate_tests.test_skill_copies ci.gate_tests.test_bebugging_seeds -q",
      "expected": "Exit 0 and unittest reports OK"
    }
  ],
  "acceptance": [
    "resolve_paths is idempotent on minimal, monotone across minimal, standard, and full, and stable in its exclude list; a standard bundle that drops kit-manifest.yml is not monotone",
    "cross_check reports REQ-GONE and BEHAVE-NEW and stays quiet for REQ-KEEP and REQ-UNRELATED; current_spec_findings returns checker-present",
    "stale_paths reports a listed path whose bytes changed, and stays quiet for a matching listed path and for an unlisted path",
    "differing_shared_paths reports one differing shared path, returns empty for identical bytes, and returns empty for the real .cursor/skills and .github/skills trees; the governed-work pair matches",
    "Historical verdict sentences remain in VERDICTS and in research/EXTERNAL_PROJECT_EVALUATIONS.md, and a follow-up states that these checks exist",
    "No constitution edit, no new workflow, no new dependency, and no commit unless the operator asks"
  ],
  "blocking_questions": [],
  "budget": {
    "max_repair_attempts": 2,
    "on_exhaustion": "Stop the affected task, keep the failing command output in specs/008-relation-checks/progress.md, and report the next decision."
  },
  "doc_delta": "Advisory metamorphic procedure, one glossary entry, one method-selector row, changelog bullet, and a research follow-up. ADR-0020 records that the checks are local and add no adopter gate."
}
```
