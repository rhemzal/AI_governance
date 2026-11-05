"""Merge Harbor job directories for post-retry result gates."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "research/experiments/harbor/merge_harbor_jobs.py"
)
SPEC = importlib.util.spec_from_file_location("merge_harbor_jobs", SCRIPT)
MERGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MERGE)

GATE_SCRIPT = Path(__file__).resolve().parents[1] / "check_harbor_results.py"
GATE_SPEC = importlib.util.spec_from_file_location("harbor_results", GATE_SCRIPT)
GATE = importlib.util.module_from_spec(GATE_SPEC)
GATE_SPEC.loader.exec_module(GATE)


def _trial(job: Path, name: str, task: str, reward=1):
    trial_dir = job / name
    trial_dir.mkdir(parents=True)
    (trial_dir / "result.json").write_text(
        json.dumps(
            {
                "task_name": task,
                "trial_name": name,
                "finished_at": "2026-11-05T12:00:00+00:00",
                "exception_info": None,
                "agent_info": {"name": "cursor-cli", "version": "v1"},
                "verifier_result": {"rewards": {"reward": reward}},
            }
        ),
        encoding="utf-8",
    )


class MergeHarborJobs(unittest.TestCase):
    def test_merge_replaces_dropped_trials(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = root / "base"
            overlay = root / "overlay"
            out = root / "merged"
            base.mkdir()
            overlay.mkdir()
            _trial(base, "good__a", "ai-governance/t1")
            _trial(base, "bad__b", "ai-governance/t1", reward=0)
            _trial(overlay, "fix__c", "ai-governance/t1")
            MERGE.merge(
                base,
                overlay,
                out,
                drop=["bad__b"],
                add=["fix__c"],
                force=False,
            )
            self.assertTrue((out / "good__a").is_dir())
            self.assertFalse((out / "bad__b").exists())
            self.assertTrue((out / "fix__c").is_dir())
            prov = json.loads((out / "merge-provenance.json").read_text())
            self.assertEqual(prov["dropped_trials"], ["bad__b"])
            result = GATE.assess(
                out,
                {
                    "tasks": ["ai-governance/t1"],
                    "attempts": 2,
                    "agent_name": "cursor-cli",
                    "reward": 1,
                },
            )
            self.assertEqual(result["outcome"], "ACCEPT")


if __name__ == "__main__":
    unittest.main()
