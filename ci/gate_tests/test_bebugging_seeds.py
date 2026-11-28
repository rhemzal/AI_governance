"""Seeds for deferred kits, scored against the checks this repository can run.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
"""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class BebuggingSeeds(unittest.TestCase):
    def test_spec_drift_is_missed_by_current_commands_and_expressible_locally(self):
        from ci.gate_tests.bebugging_seeds import (
            current_spec_findings,
            local_spec_findings,
        )

        spec = ["REQ-KEEP", "REQ-GONE", "REQ-UNRELATED"]
        code = ["REQ-KEEP", "REQ-UNRELATED", "BEHAVE-NEW"]
        self.assertEqual(current_spec_findings(ROOT), [])
        found = local_spec_findings(spec, code)
        self.assertIn("REQ-GONE", found["missing_from_code"])
        self.assertIn("BEHAVE-NEW", found["missing_from_spec"])
        self.assertNotIn("REQ-UNRELATED", found["missing_from_code"])
        self.assertNotIn("REQ-KEEP", found["missing_from_code"])

    def test_stale_resume_is_prose_only(self):
        from ci.gate_tests.bebugging_seeds import (
            file_hash,
            resume_hash_is_executable,
            skill_marks_hash_mismatch_stale,
        )

        self.assertTrue(skill_marks_hash_mismatch_stale(ROOT))
        self.assertFalse(resume_hash_is_executable(ROOT))
        original = b"done\n"
        changed = b"changed\n"
        self.assertNotEqual(file_hash(original), file_hash(changed))

    def test_two_writers_conflict_on_the_same_line(self):
        from ci.gate_tests.bebugging_seeds import two_writer_result

        self.assertEqual(two_writer_result(), "conflict")

    def test_instruction_copies_can_drift_without_a_parity_check(self):
        from ci.gate_tests.bebugging_seeds import (
            instruction_copies_match,
            parity_check_exists,
        )

        self.assertTrue(
            instruction_copies_match(
                ROOT / ".cursor/skills/governed-work/SKILL.md",
                ROOT / ".github/skills/governed-work/SKILL.md",
            )
        )
        self.assertFalse(parity_check_exists(ROOT))

    def test_one_of_two_acceptance_commands_stays_unfinished(self):
        from ci.gate_tests.bebugging_seeds import two_command_result

        self.assertEqual(two_command_result(), "unfinished-stop")

    def test_overlay_selector_keeps_the_unrelated_path_quiet(self):
        from ci.gate_tests.bebugging_seeds import overlay_selection

        required = overlay_selection(ROOT, "ci/import_bundle.py")
        self.assertTrue(required)
        self.assertIn("existing destination", required[0])
        self.assertEqual(
            overlay_selection(ROOT, "usage/ADOPTION_SCOPE_AND_HOSTS.md"),
            [],
        )

    def test_fresh_context_packet_can_reject_a_verdict_but_finds_no_defect(self):
        from ci.gate_tests.bebugging_seeds import (
            packet_excludes_author_verdict,
            review_finds_planted_defect,
        )

        clean = "Diff and acceptance criteria only.\n"
        planted = clean + "Planted defect: the symlink check is gone.\n"
        contaminated = planted + "Author verdict: ship it.\n"
        self.assertTrue(packet_excludes_author_verdict(clean))
        self.assertTrue(packet_excludes_author_verdict(planted))
        self.assertFalse(packet_excludes_author_verdict(contaminated))
        self.assertFalse(review_finds_planted_defect(ROOT))

    def test_verifier_failure_asks_for_a_followup(self):
        from ci.gate_tests.bebugging_seeds import gate_failure_result

        self.assertEqual(gate_failure_result(), "followup")

    def test_running_workflow_resume_is_refused(self):
        from ci.gate_tests.bebugging_seeds import running_resume_result

        result = running_resume_result()
        if result == "unavailable":
            self.skipTest("specify-cli 1.2.5 interpreter is not installed")
        self.assertEqual(result, "refused")

    def test_pinned_superpowers_does_not_compare_a_file_hash(self):
        from ci.gate_tests.bebugging_seeds import superpowers_compares_file_hash

        self.assertFalse(superpowers_compares_file_hash(ROOT))

    def test_content_identity_distinguishes_two_edits_of_one_path(self):
        from ci.gate_tests.bebugging_seeds import content_identity_result

        self.assertEqual(content_identity_result(), "distinct")

    def test_architecture_change_without_an_adr_is_caught(self):
        from ci.gate_tests.bebugging_seeds import architecture_record_result

        self.assertEqual(architecture_record_result("architecture"), "caught")
        self.assertEqual(architecture_record_result("usage"), "quiet")

    def test_denied_command_is_expressible_without_a_runtime_product(self):
        from ci.gate_tests.bebugging_seeds import (
            current_runtime_gate,
            runtime_decision,
        )

        self.assertFalse(current_runtime_gate(ROOT))
        self.assertEqual(runtime_decision("deploy.sh"), "deny")
        self.assertEqual(runtime_decision("python -m unittest"), "allow")

    def test_hook_fire_claim_without_a_record_is_unsupported(self):
        from ci.gate_tests.bebugging_seeds import (
            dispatch_claim_is_enforced,
            dispatch_claim_result,
        )

        self.assertFalse(dispatch_claim_is_enforced(ROOT))
        self.assertEqual(dispatch_claim_result(True, ""), "unsupported")
        self.assertEqual(dispatch_claim_result(True, "{\"decision\":\"allow\"}\n"), "recorded")

    def test_role_without_an_acceptance_command_stays_unchecked(self):
        from ci.gate_tests.bebugging_seeds import (
            catalog_acceptance_is_enforced,
            recipe_acceptance,
        )

        self.assertFalse(catalog_acceptance_is_enforced(ROOT))
        self.assertEqual(recipe_acceptance("You are a role.\n"), "absent")
        self.assertEqual(
            recipe_acceptance("Recipe.\nAcceptance command: python3 -m unittest\n"),
            "present",
        )

    def test_verdict_records_redundant_products_for_every_seed(self):
        from ci.gate_tests.bebugging_seeds import VERDICTS

        evaluation = (
            ROOT / "research/EXTERNAL_PROJECT_EVALUATIONS.md"
        ).read_text(encoding="utf-8")
        for name, verdict in VERDICTS.items():
            self.assertIn(name, evaluation)
            self.assertIn(verdict["result"], evaluation)
            self.assertNotIn(f"vendor/{name}", evaluation)


if __name__ == "__main__":
    unittest.main()
