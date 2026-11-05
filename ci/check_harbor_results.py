#!/usr/bin/env python3
"""Turn a native Harbor job directory into a candidate accept/reject status.

Provenance: AI_governance (https://github.com/rhemzal/AI_governance).
This reads Harbor trial result.json files. It does not start an agent, grade
files, or treat a reward of 1 as proof that every required trial happened.
"""

import argparse
import json
from pathlib import Path
import sys


class GateError(ValueError):
    """The expectation file itself cannot be used."""


def _tasks(value):
    if not isinstance(value, list) or not value:
        raise GateError("tasks: expected a non-empty list")
    names = []
    for item in value:
        if not isinstance(item, str) or not item or item != item.strip():
            raise GateError("tasks: expected non-empty task names")
        names.append(item)
    if len(set(names)) != len(names):
        raise GateError("tasks: duplicate task names")
    return names


def _expectation(value):
    if not isinstance(value, dict):
        raise GateError("expected: expected an object")
    allowed = {"tasks", "attempts", "agent_name", "reward"}
    if set(value) != allowed:
        raise GateError("expected: expected tasks, attempts, agent_name, reward")
    tasks = _tasks(value["tasks"])
    attempts = value["attempts"]
    if type(attempts) is not int or attempts < 1:
        raise GateError("attempts: expected a positive integer")
    agent_name = value["agent_name"]
    if not isinstance(agent_name, str) or not agent_name or agent_name != agent_name.strip():
        raise GateError("agent_name: expected non-empty text")
    reward = value["reward"]
    if type(reward) is not int or isinstance(reward, bool):
        raise GateError("reward: expected an integer")
    return {
        "tasks": tasks,
        "attempts": attempts,
        "agent_name": agent_name,
        "reward": reward,
    }


def _load_result(path):
    if path.is_symlink() or not path.is_file():
        return None, f"ERROR: {path.parent.name} result is not a regular file"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, f"ERROR: {path.parent.name} {error.__class__.__name__}"
    if not isinstance(data, dict):
        return None, f"ERROR: {path.parent.name} result is not an object"
    return data, None


def _reward_value(record):
    verifier = record.get("verifier_result")
    if not isinstance(verifier, dict):
        return None
    rewards = verifier.get("rewards")
    if not isinstance(rewards, dict) or "reward" not in rewards:
        return None
    return rewards["reward"]


def _exceptions(record):
    found = []
    if record.get("exception_info"):
        found.append("trial")
    steps = record.get("step_results")
    if isinstance(steps, list):
        for step in steps:
            if isinstance(step, dict) and step.get("exception_info"):
                found.append("step")
    return found


def assess(job_dir, expected):
    """Return ACCEPT only for a complete, clean candidate matrix."""
    expected = _expectation(expected)
    job_dir = Path(job_dir)
    reasons = []
    if not job_dir.is_dir():
        return {"outcome": "REJECT", "reasons": [f"ERROR: {job_dir} is not a directory"]}

    trials = []
    for child in sorted(job_dir.iterdir(), key=lambda path: path.name):
        if child.is_symlink() or not child.is_dir():
            continue
        result_path = child / "result.json"
        if not result_path.exists():
            reasons.append(f"MISSING: {child.name}")
            continue
        record, error = _load_result(result_path)
        if error:
            reasons.append(error)
            continue
        record["_directory"] = child.name
        trials.append(record)

    seen_names = {}
    by_task = {task: [] for task in expected["tasks"]}
    for record in trials:
        task_name = record.get("task_name")
        trial_name = record.get("trial_name")
        directory = record["_directory"]
        if not isinstance(task_name, str) or not isinstance(trial_name, str):
            reasons.append(f"ERROR: {directory} missing task_name or trial_name")
            continue
        if task_name not in by_task:
            reasons.append(f"UNEXPECTED: {task_name}")
            continue
        if trial_name in seen_names:
            reasons.append(f"DUPLICATE: {trial_name}")
            continue
        seen_names[trial_name] = directory
        by_task[task_name].append(record)

        if not record.get("finished_at"):
            reasons.append(f"INCOMPLETE: {trial_name}")
        if _exceptions(record):
            reasons.append(f"EXCEPTION: {trial_name}")
        reward = _reward_value(record)
        if type(reward) is bool or type(reward) not in (int, float) or float(reward) != expected["reward"]:
            reasons.append(f"REWARD: {trial_name}")
        agent = record.get("agent_info")
        if not isinstance(agent, dict):
            reasons.append(f"AGENT: {trial_name}")
            reasons.append(f"VERSION: {trial_name}")
            continue
        if agent.get("name") != expected["agent_name"]:
            reasons.append(f"AGENT: {trial_name}")
        version = agent.get("version")
        if not isinstance(version, str) or not version.strip():
            reasons.append(f"VERSION: {trial_name}")

    versions = []
    for task, records in by_task.items():
        count = len(records)
        if count != expected["attempts"]:
            kind = "MISSING" if count < expected["attempts"] else "UNEXPECTED"
            reasons.append(f"{kind}: {task} attempts {count}/{expected['attempts']}")
        for record in records:
            agent = record.get("agent_info")
            if isinstance(agent, dict) and isinstance(agent.get("version"), str) and agent["version"].strip():
                versions.append(agent["version"])
    if len(set(versions)) > 1:
        reasons.append("VERSION: agent versions differ")

    outcome = "ACCEPT" if not reasons else "REJECT"
    return {"outcome": outcome, "reasons": reasons}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job", type=Path, required=True)
    parser.add_argument("--expected", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        expected = json.loads(args.expected.read_text(encoding="utf-8"))
        result = assess(args.job, expected)
    except (GateError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(json.dumps({"outcome": "BLOCKED", "reasons": [str(error)]}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0 if result["outcome"] == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main())
