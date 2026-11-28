"""Synthetic checks for a green stop that leaves an assignment unfinished.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "research/experiments/overlay-selector-continuation.patch"
SELECTOR = ROOT / "ci/select_overlay_rows.py"
OVERLAY = ROOT / "governance/LOCAL_OVERLAY.md"
STOP_FIXTURE = Path(__file__).resolve().parent / "fixtures/continuation_stop_allow.json"
BASELINE_RULE = (
    ROOT
    / "governance/experimental/spec_gates/templates/autonomous-aep-execution.baseline.mdc.template"
)
AGENTS_ONLY = """# AGENTS.md — AI Governance Projection

Produce an Autonomous Execution Plan for HIGH-risk work.
Follow the task mandate in constitution/AI_ENFORCEMENT.md.
"""
COPY_PATH = "opt-in/copy/CONTENT.txt"
DOC_PATH = "usage/ADOPTION_SCOPE_AND_HOSTS.md"
EXPECTED_COPY_SOURCES = ["`no_symlinks`, `readopt_destination`"]


class ContinuationSynthetic(unittest.TestCase):
    def test_allow_pass_with_unmet_criterion_is_an_unfinished_stop(self):
        from ci.gate_tests.continuation_synthetic import classify_stop

        recorded = json.loads(STOP_FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(
            classify_stop(recorded["stop"], recorded["unmet_criterion"]),
            "unfinished-stop",
        )
        self.assertEqual(classify_stop(recorded["stop"], ""), "closed")

    def test_prompt_bundle_reports_the_baseline_sentence_only_when_present(self):
        from ci.gate_tests.continuation_synthetic import classify_prompt

        self.assertEqual(classify_prompt(AGENTS_ONLY), "ABSENT")
        rule_text = BASELINE_RULE.read_text(encoding="utf-8")
        self.assertIn("Do not require", rule_text)
        self.assertIn("`/governed-work` or any second startup ritual.", rule_text)
        self.assertEqual(classify_prompt(rule_text), "PRESENT")

    def test_library_only_repair_fails_public_json_and_complete_repair_passes(self):
        from ci.gate_tests.continuation_synthetic import public_json_sources

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            both = root / "both"
            library_only = root / "library-only"
            complete = root / "complete"
            for tree in (both, library_only, complete):
                (tree / "ci").mkdir(parents=True)
                shutil.copy(SELECTOR, tree / "ci/select_overlay_rows.py")
            subprocess.run(
                ["patch", "-p1", "-d", str(both), "-i", str(PATCH)],
                check=True,
                capture_output=True,
                text=True,
                timeout=15,
            )
            shutil.copy(
                both / "ci/select_overlay_rows.py",
                library_only / "ci/select_overlay_rows.py",
            )
            library_text = (library_only / "ci/select_overlay_rows.py").read_text(
                encoding="utf-8"
            )
            library_text = library_text.replace(
                '"copy" in lw',
                '"copies" in lw or "symlink" in lw or "cp -a" in lw',
                1,
            )
            (library_only / "ci/select_overlay_rows.py").write_text(
                library_text, encoding="utf-8"
            )

            partial = public_json_sources(library_only / "ci/select_overlay_rows.py", OVERLAY, COPY_PATH)
            self.assertNotEqual(partial, EXPECTED_COPY_SOURCES)
            finished = public_json_sources(complete / "ci/select_overlay_rows.py", OVERLAY, COPY_PATH)
            self.assertEqual(finished, EXPECTED_COPY_SOURCES)
            self.assertEqual(
                public_json_sources(complete / "ci/select_overlay_rows.py", OVERLAY, DOC_PATH),
                [],
            )


if __name__ == "__main__":
    unittest.main()
