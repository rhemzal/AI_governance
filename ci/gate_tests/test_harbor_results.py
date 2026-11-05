"""Candidate acceptance over native Harbor trial results.

The gate reads result files. It does not start an agent, and a reward of 1
does not hide a missing, duplicated, unfinished, or errored trial.
"""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "check_harbor_results.py"
SPEC = importlib.util.spec_from_file_location("harbor_results", SCRIPT)
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

TASKS = (
    "ai-governance/c1-forbidden-import",
    "ai-governance/c1-forbidden-import-b1",
    "ai-governance/c2-permitted-doc",
    "ai-governance/c2-permitted-doc-b1",
)


def expected(attempts=1):
    return {
        "tasks": list(TASKS),
        "attempts": attempts,
        "agent_name": "cursor-cli",
        "reward": 1,
    }


def trial(task, name, **overrides):
    record = {
        "task_name": task,
        "trial_name": name,
        "finished_at": "2026-11-05T09:00:00+00:00",
        "exception_info": None,
        "step_results": None,
        "agent_info": {
            "name": "cursor-cli",
            "version": "2026.10.22-27dcf5f",
        },
        "verifier_result": {"rewards": {"reward": 1}},
    }
    record.update(overrides)
    return record


def write_job(root, records):
    root = Path(root)
    for index, record in enumerate(records):
        trial_dir = root / f"trial-{index}"
        trial_dir.mkdir()
        (trial_dir / "result.json").write_text(
            json.dumps(record), encoding="utf-8"
        )
    return root


class HarborResultGate(unittest.TestCase):
    def test_complete_reward_matrix_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = [
                trial(task, f"{task}-a") for task in TASKS
            ]
            records[0]["verifier_result"] = {"rewards": {"reward": 1.0}}
            result = GATE.assess(write_job(tmp, records), expected())
        self.assertEqual(result["outcome"], "ACCEPT")
        self.assertEqual(result["reasons"], [])

    def test_agent_authored_pass_file_is_not_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "trial-a").mkdir()
            (root / "trial-a" / "result.json").write_text("PASS\n", encoding="utf-8")
            result = GATE.assess(root, expected())
        self.assertEqual(result["outcome"], "REJECT")
        self.assertTrue(any(reason.startswith("ERROR:") for reason in result["reasons"]))

    def test_reward_without_the_rest_of_the_matrix_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = GATE.assess(
                write_job(tmp, [trial(TASKS[0], "only-one")]),
                expected(),
            )
        self.assertEqual(result["outcome"], "REJECT")
        self.assertTrue(any(reason.startswith("MISSING:") for reason in result["reasons"]))

    def test_missing_result_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_job(tmp, [trial(task, f"{task}-a") for task in TASKS])
            (root / "unfinished").mkdir()
            result = GATE.assess(root, expected())
        self.assertEqual(result["outcome"], "REJECT")
        self.assertIn("MISSING: unfinished", result["reasons"])

    def test_exception_with_reward_one_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = [trial(task, f"{task}-a") for task in TASKS]
            records[0]["exception_info"] = {
                "exception_type": "AgentTimeoutError",
                "exception_message": "timed out",
            }
            result = GATE.assess(write_job(tmp, records), expected())
        self.assertEqual(result["outcome"], "REJECT")
        self.assertTrue(any(reason.startswith("EXCEPTION:") for reason in result["reasons"]))

    def test_non_numeric_reward_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = [trial(task, f"{task}-a") for task in TASKS]
            records[0]["verifier_result"] = {"rewards": {"reward": "PASS"}}
            result = GATE.assess(write_job(tmp, records), expected())
        self.assertEqual(result["outcome"], "REJECT")
        self.assertTrue(any(reason.startswith("REWARD:") for reason in result["reasons"]))

    def test_zero_reward_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = [trial(task, f"{task}-a") for task in TASKS]
            records[1]["verifier_result"] = {"rewards": {"reward": 0}}
            result = GATE.assess(write_job(tmp, records), expected())
        self.assertEqual(result["outcome"], "REJECT")
        self.assertTrue(any(reason.startswith("REWARD:") for reason in result["reasons"]))

    def test_duplicate_and_unexpected_trials_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_job(tmp, [trial(task, f"{task}-a") for task in TASKS])
            duplicate = root / "same-trial-name"
            duplicate.mkdir()
            (duplicate / "result.json").write_text(
                json.dumps(trial(TASKS[0], f"{TASKS[0]}-a")),
                encoding="utf-8",
            )
            unexpected = root / "c3-dir"
            unexpected.mkdir()
            (unexpected / "result.json").write_text(
                json.dumps(trial("c3-not-in-pilot", "c3-a")),
                encoding="utf-8",
            )
            result = GATE.assess(root, expected())
        self.assertEqual(result["outcome"], "REJECT")
        self.assertTrue(any(reason.startswith("DUPLICATE:") for reason in result["reasons"]))
        self.assertTrue(any(reason.startswith("UNEXPECTED:") for reason in result["reasons"]))

    def test_version_must_be_present_and_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = [trial(task, f"{task}-a") for task in TASKS]
            records[2]["agent_info"] = {"name": "cursor-cli", "version": "other"}
            mismatched = GATE.assess(write_job(tmp, records), expected())
        self.assertEqual(mismatched["outcome"], "REJECT")
        self.assertTrue(any(reason.startswith("VERSION:") for reason in mismatched["reasons"]))

        with tempfile.TemporaryDirectory() as tmp:
            records = [trial(task, f"{task}-a") for task in TASKS]
            records[0]["agent_info"] = {"name": "cursor-cli", "version": ""}
            blank = GATE.assess(write_job(tmp, records), expected())
        self.assertEqual(blank["outcome"], "REJECT")

    def test_wrong_agent_name_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = [trial(task, f"{task}-a") for task in TASKS]
            records[0]["agent_info"] = {
                "name": "oracle",
                "version": "2026.10.22-27dcf5f",
            }
            result = GATE.assess(write_job(tmp, records), expected())
        self.assertEqual(result["outcome"], "REJECT")
        self.assertTrue(any(reason.startswith("AGENT:") for reason in result["reasons"]))

    def test_unfinished_trial_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = [trial(task, f"{task}-a") for task in TASKS]
            records[0]["finished_at"] = None
            result = GATE.assess(write_job(tmp, records), expected())
        self.assertEqual(result["outcome"], "REJECT")
        self.assertTrue(any(reason.startswith("INCOMPLETE:") for reason in result["reasons"]))

    def test_three_attempts_require_three_distinct_trials(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = []
            for task in TASKS:
                for index in (1, 2):
                    records.append(trial(task, f"{task}-{index}"))
            result = GATE.assess(write_job(tmp, records), expected(attempts=3))
        self.assertEqual(result["outcome"], "REJECT")
        self.assertTrue(any("attempts" in reason for reason in result["reasons"]))


if __name__ == "__main__":
    unittest.main()
