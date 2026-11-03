"""Executable limits for the claim cards that had no planted check.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
Python standard library. These tests read recorded evidence and kit entry
points. They do not launch Cursor, run B5–B8, or execute the spec-gates fragment.
"""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "research/experiments/spec_kit_spec_gates/cursor_native_2026-11-01"
SCENARIOS = ROOT / "tooling/BENCHMARK_SCENARIOS.md"
FRAGMENT = (
    ROOT / ".specify/extensions/gates/constitution/fragments/governance/provable-enforcement.md"
)


class OpenClaimLimits(unittest.TestCase):
    def test_recorded_native_stop_log_stayed_empty(self):
        record = EXPERIMENT.joinpath("README.md").read_text(encoding="utf-8")
        pilot = (ROOT / "research/SPEC_KIT_SPEC_GATES_PILOT.md").read_text(encoding="utf-8")
        self.assertIn("`stop-invocations.jsonl` stayed empty.", record)
        self.assertIn("The invocation log stayed empty.", pilot)
        self.assertEqual(list(EXPERIMENT.rglob("stop-invocations.jsonl")), [])
        self.assertIn("that call is not native dispatch", record)

    def test_b5_through_b8_have_no_recorded_trial(self):
        text = SCENARIOS.read_text(encoding="utf-8")
        section = text.split("## Agent-execution scenarios", 1)[1]
        section = section.split("## Related Documents", 1)[0]
        for label in ("B5:", "B6:", "B7:", "B8:"):
            self.assertIn(label, section)
        self.assertNotIn("Trial result", section)
        self.assertNotIn("observed outcome", section.casefold())
        self.assertFalse((ROOT / "research/benchmark_trials").exists())

    def test_provable_enforcement_fragment_does_not_drive_kit_gates(self):
        fragment = FRAGMENT.read_text(encoding="utf-8")
        self.assertIn("Every gate class re-proves itself", fragment)
        entry_points = [
            ROOT / ".github/workflows/doc-hygiene.yml",
            ROOT / ".github/workflows/adr-required.yml",
            ROOT / ".github/workflows/aep-advisory.yml",
            ROOT / "ci/validate_claim_cards.py",
            ROOT / "ci/validate_aep.py",
        ]
        entry_points.extend((ROOT / "constitution").glob("*.md"))
        for path in entry_points:
            body = path.read_text(encoding="utf-8")
            self.assertNotIn(
                "provable-enforcement",
                body,
                f"{path.relative_to(ROOT)} references the fragment",
            )
