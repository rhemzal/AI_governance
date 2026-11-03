"""Executable limits for the claim cards that had no planted check.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
Python standard library. These tests read recorded evidence and kit entry
points. They do not launch Cursor, run B5–B8, or execute the spec-gates fragment.
"""

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "research/experiments/spec_kit_spec_gates/cursor_native_2026-11-01"
SCENARIOS = ROOT / "tooling/BENCHMARK_SCENARIOS.md"
FRAGMENT = (
    ROOT / ".specify/extensions/gates/constitution/fragments/governance/provable-enforcement.md"
)


def load_trials():
    path = ROOT / "ci/benchmark_trials.py"
    spec = importlib.util.spec_from_file_location("benchmark_trials", path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OpenClaimLimits(unittest.TestCase):
    def test_recorded_native_stop_log_stayed_empty(self):
        record = EXPERIMENT.joinpath("README.md").read_text(encoding="utf-8")
        pilot = (ROOT / "research/SPEC_KIT_SPEC_GATES_PILOT.md").read_text(encoding="utf-8")
        self.assertIn("`stop-invocations.jsonl` stayed empty.", record)
        self.assertIn("The invocation log stayed empty.", pilot)
        self.assertEqual(list(EXPERIMENT.rglob("stop-invocations.jsonl")), [])
        self.assertIn("that call is not native dispatch", record)

    def test_historical_absence_allows_later_trial_files(self):
        trials = load_trials()
        text = SCENARIOS.read_text(encoding="utf-8")
        section = text.split("## Agent-execution scenarios", 1)[1]
        section = section.split("## Related Documents", 1)[0]
        for label in ("B5:", "B6:", "B7:", "B8:"):
            self.assertIn(label, section)
        self.assertEqual(section.count(trials.HISTORICAL_ABSENCE), 1)
        self.assertNotIn("Trial result", section)
        self.assertNotIn("observed outcome", section.casefold())
        self.assertEqual(trials.tree_errors(ROOT / "research/benchmark_trials"), [])

        good = "scenario: B5\nrevision: abcdef0\noutcome: pass\n"
        self.assertEqual(trials.trial_errors(good), [])
        cancelled = "scenario: B7\nrevision: abcdef0\noutcome: cancelled\n"
        self.assertEqual(trials.trial_errors(cancelled), [])
        blocked = "scenario: B8\nrevision: abcdef0\noutcome: blocked\n"
        self.assertEqual(trials.trial_errors(blocked), [])
        self.assertTrue(trials.trial_errors("scenario: B5\noutcome: pass\n"))
        self.assertTrue(trials.trial_errors("scenario: B5\nrevision: abc def\noutcome: pass\n"))
        self.assertTrue(trials.trial_errors("scenario: B5\nrevision: abcdef0\noutcome:\n"))
        self.assertTrue(trials.trial_errors("scenario: B5\nrevision: abcdef0\noutcome: nope\n"))
        self.assertTrue(trials.trial_errors("scenario: B50\nrevision: abcdef0\noutcome: pass\n"))
        duplicate = "scenario: B5\nscenario: B6\nrevision: abcdef0\noutcome: pass\n"
        self.assertTrue(any("duplicate" in item for item in trials.trial_errors(duplicate)))

        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.assertEqual(trials.tree_errors(directory / "absent"), [])
            self.assertEqual(trials.tree_errors(directory), [])
            (directory / "README.md").write_text("not a trial\n", encoding="utf-8")
            self.assertEqual(trials.tree_errors(directory), [])
            (directory / "b5.md").write_text(good, encoding="utf-8")
            self.assertEqual(trials.tree_errors(directory), [])
            (directory / "bad.md").write_text("scenario: B5\n", encoding="utf-8")
            self.assertTrue(trials.tree_errors(directory))

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
