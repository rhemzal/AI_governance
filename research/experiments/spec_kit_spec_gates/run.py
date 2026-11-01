#!/usr/bin/env python3
"""Opt-in, disposable integration experiment; not a kit/adopter CI gate.

Requires an isolated Specify 1.2.5 installation built from the pinned source.
Creates only the explicitly supplied, previously absent output directory.
The retained workspaces are synthetic and suitable for native-agent follow-up.
"""

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys


SPEC_KIT = "4572a67fe0e72a6837e2d7bb0fda875bc41482e5"
SPEC_GATES = "8a5a0e8a58aa548ad3dbba6f61e772c73cde50ae"
KIT_BASE = "873df7e982ed953181d6526e7866b0bd34d2fa0d"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-kit-source", required=True, type=Path)
    parser.add_argument("--spec-gates-source", required=True, type=Path)
    parser.add_argument("--specify", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    kit = Path(__file__).resolve().parents[3]
    sources = [args.spec_kit_source.resolve(), args.spec_gates_source.resolve()]
    specify = args.specify.absolute()
    output = args.output.resolve()
    # Do not let a fixture become part of any of the source checkouts.
    if any(output == root or root in output.parents for root in [kit, *sources]):
        parser.error("--output must be outside the source repositories")
    output.mkdir(parents=True, exist_ok=False)
    (output / "logs").mkdir()
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("GIT_", "GATES_", "CLAUDE_"))}
    env.update(NO_COLOR="1", TERM="dumb", PYTHONUNBUFFERED="1")
    env["PATH"] = str(specify.parent) + os.pathsep + env.get("PATH", "")
    records = []

    def clean(text):
        for path, label in [(output, "<OUTPUT>"), (kit, "<KIT>"),
                            (sources[0], "<SPEC_KIT>"), (sources[1], "<SPEC_GATES>"),
                            (specify.parent, "<VENV_BIN>")]:
            text = text.replace(str(path), label)
        return text

    def run(name, command, cwd, expected=0, stdin=None, timeout=60,
            kind="assertion", predicate=None):
        try:
            result = subprocess.run([str(s) for s in command], cwd=cwd, env=env,
                                    input=stdin, text=True, capture_output=True,
                                    timeout=timeout)
            rc, stdout, stderr = result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired as error:
            rc = 124
            stdout = (error.stdout or b"").decode(errors="replace")
            stderr = "Experiment command exceeded its wall-clock limit."
        passed = rc == expected and (predicate is None or predicate(stdout))
        log = f"logs/{len(records) + 1:02d}-{name}.txt"
        (output / log).write_text(clean(
            f"argv: {json.dumps([str(s) for s in command])}\n"
            f"cwd: {cwd}\nexpected_exit: {expected}\nactual_exit: {rc}\n"
            f"stdout:\n{stdout}\nstderr:\n{stderr}"))
        records.append({"id": name, "kind": kind, "expected_exit": expected,
                        "actual_exit": rc, "matched": passed, "log": log})
        print(f"{'PASS' if passed else 'FAIL'} {name} (exit {rc})", flush=True)
        return passed, stdout

    def observation(name, passed, detail):
        records.append({"id": name, "kind": "assertion", "matched": bool(passed),
                        "detail": detail})
        print(f"{'PASS' if passed else 'FAIL'} {name}", flush=True)

    def write_json(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n")

    def finish():
        result = {"schema_version": 1, "scope": "deterministic disposable fixtures",
                  "spec_kit_commit": SPEC_KIT, "spec_gates_commit": SPEC_GATES,
                  "kit_base_commit": KIT_BASE, "python": platform.python_version(),
                  "platform": platform.system(),
                  "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  "validator_sha256": hashlib.sha256((kit / "ci/validate_test_evidence.py").read_bytes()).hexdigest(),
                  "native_agent_execution": "NOT_RUN",
                  "ci_service_execution": "NOT_RUN",
                  "records": records,
                  "matched": sum(r["matched"] for r in records), "total": len(records)}
        write_json(output / "results.json", result)
        print(f"Evidence: {output / 'results.json'}")
        return 0 if all(r["matched"] for r in records) else 1

    for root, sha, name in [(sources[0], SPEC_KIT, "spec-kit"),
                            (sources[1], SPEC_GATES, "spec-gates")]:
        ok, _ = run(name + "-pin", ["git", "rev-parse", "HEAD"], root,
                    predicate=lambda s, sha=sha: s.strip() == sha)
        clean_source, _ = run(name + "-unchanged", ["git", "diff", "--exit-code", "HEAD"], root)
        if not ok or not clean_source:
            return finish()
    ok, _ = run("specify-version", [specify, "version"], output,
                predicate=lambda s: "1.2.5" in s)
    if not ok:
        return finish()

    sentinels = {"AGENTS.md": "# Host instructions\nHOST-AGENTS-KEEP\n",
                 "CLAUDE.md": "# Host instructions\nHOST-CLAUDE-KEEP\n",
                 ".specify/memory/constitution.md": "# Host constitution\nHOST-CONSTITUTION-KEEP\n"}
    host_settings = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "true"}]}]},
                     "permissions": {"deny": ["Read(.env)"]}}
    for integration, skill_dir in [("claude", ".claude/skills"),
                                   ("codex", ".agents/skills"),
                                   ("cursor-agent", ".cursor/skills")]:
        root = output / "workspaces" / integration
        root.mkdir(parents=True)
        for name, text in sentinels.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        write_json(root / ".claude/settings.json", host_settings)
        run(integration + "-git-init", ["git", "init", "-q", "-b", "pilot"], root)
        ok, _ = run(integration + "-init", [specify, "init", "--here", "--force",
                    "--non-interactive", "--integration", integration, "--ignore-agent-tools",
                    "--extension", sources[1] / "extension"], root)
        observation(integration + "-preserve-instructions",
                    all((root / n).read_text() == t for n, t in sentinels.items()),
                    "Byte equality of host AGENTS.md, CLAUDE.md and constitution after initialization.")
        observation(integration + "-skills-installed", bool(list((root / skill_dir).glob("*/SKILL.md"))),
                    "Generated skill files exist; native agent loading is not tested.")
        if not ok:
            return finish()

    root = output / "workspaces/claude"
    gates = root / ".specify/gates"
    policy = {"hooks": {"verify-quality": {"orchestrator": "none", "severity": "error",
              "gates": {
                  "real-check": {"command": "python3 -c \"from pathlib import Path; assert Path('fixture.txt').read_text() == 'approved\\n', 'fixture mismatch'\"", "timeout_s": 15},
                  "test-evidence": {"command": "python3 validate_test_evidence.py --expected expected.json --report report.json", "timeout_s": 15}}}},
              "git": {"block_main_commits": True, "conventional_commits": True,
                      "forbid_ai_isms": False, "protected_change_trailer": False},
              "spec": {"enabled": False}, "attestation": {"enabled": True, "parity": "error"}}
    expected = {"schema_version": 1, "run_id": "synthetic-pilot",
                "tested_state": {"fixture": "synthetic-v1"},
                "required_checks": ["required-check"], "cleanup_required": True}
    good = {"schema_version": 1, "run_id": "synthetic-pilot",
            "tested_state": {"fixture": "synthetic-v1"},
            "execution": {"status": "completed", "exit_code": 0},
            "checks": [{"id": "required-check", "status": "passed", "evidence": ["synthetic-observation"]}],
            "cleanup": "complete"}
    write_json(gates / "policy.json", policy)
    write_json(root / "expected.json", expected)
    write_json(root / "report.json", good)
    (root / "fixture.txt").write_text("approved\n")
    shutil.copyfile(kit / "ci/validate_test_evidence.py", root / "validate_test_evidence.py")
    original_policy = (gates / "policy.json").read_bytes()
    ok, _ = run("project-and-canaries", ["bash", ".specify/extensions/gates/runtime/project.sh"], root,
                timeout=90, predicate=lambda s: "18 run," in s and "0 accepted," in s)
    # Upstream exit status rejects missing policy-enabled checks. Optional linters
    # may be present on another host; their skipped/blocked counts remain in logs.
    if not ok:
        return finish()
    observation("policy-preserved", (gates / "policy.json").read_bytes() == original_policy,
                "Projection did not rewrite the approved experimental policy.")
    settings = json.loads((root / ".claude/settings.json").read_text())
    observation("host-settings-preserved", settings["permissions"] == host_settings["permissions"]
                and host_settings["hooks"]["Stop"][0] in settings["hooks"]["Stop"],
                "Existing deny permission and harmless Stop hook remain after merge.")
    run("projection-check", ["bash", ".specify/gates/project.sh", "--check"], root)
    run("projected-write-refused", ["bash", ".specify/gates/project.sh"], root, expected=2)
    run("projection-reapply", ["bash", ".specify/extensions/gates/runtime/project.sh"], root, timeout=90)
    observation("projection-no-duplicate-hooks", json.loads((root / ".claude/settings.json").read_text()) == settings,
                "Reapplying the same version does not duplicate merged hooks; not an upgrade test.")

    def verify(label, exit_code, kind="assertion", gate=None):
        for boundary in ("agent", "git", "ci"):
            def predicate(text):
                data = json.loads(text)
                return gate is None or any(g["name"] == gate and g["status"] == "fail" for g in data["gates"])
            run(label + "-" + boundary, ["bash", ".specify/gates/verify.sh", "--boundary", boundary, "--json"],
                root, expected=exit_code, kind=kind, predicate=predicate)

    verify("valid", 0)
    # Install a real baseline commit. All Git writes stay in the synthetic host.
    run("stage-fixture", ["git", "add", "."], root)
    commit = ["git", "-c", "user.name=Governance pilot", "-c", "user.email=pilot@example.invalid", "commit"]
    run("git-commit-valid", [*commit, "-qm", "test: initialize synthetic fixture"], root)
    initial_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True)
    (root / "fixture.txt").write_text("invalid\n")
    verify("real-check-failed", 2, gate="real-check")
    hook = ["bash", ".claude/hooks/gates/verify-quality.sh"]
    run("stop-first-failure", hook, root, expected=2, stdin='{"stop_hook_active":false}')
    run("stop-loop-guard", hook, root, expected=0, stdin='{"stop_hook_active":true}', kind="known-limit")
    run("stage-invalid", ["git", "add", "fixture.txt"], root)
    run("git-commit-blocked", [*commit, "-qm", "test: reject invalid fixture"], root, expected=1)
    observation("git-head-unchanged", subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True) == initial_head,
                "Rejected commit did not advance the synthetic repository HEAD.")
    noop = copy.deepcopy(policy)
    noop["hooks"]["verify-quality"]["gates"]["real-check"]["command"] = "true"
    write_json(gates / "policy.json", noop)
    verify("noop-does-not-prove-coverage", 0, kind="known-limit")
    write_json(gates / "policy.json", policy)
    (root / "fixture.txt").write_text("approved\n")
    run("restore-staged-fixture", ["git", "add", "fixture.txt"], root)

    for label, field, value in [("stale-evidence", "tested_state", {"fixture": "older"}),
                                ("missing-check", "checks", []),
                                ("incomplete-cleanup", "cleanup", "unknown")]:
        bad = copy.deepcopy(good)
        bad[field] = value
        write_json(root / "report.json", bad)
        verify(label, 2, gate="test-evidence")
    write_json(root / "report.json", good)
    for label, command in [("missing-command", "pilot-command-that-does-not-exist"),
                           ("gate-timeout", "python3 -c 'import time; time.sleep(3)'")]:
        changed = copy.deepcopy(policy)
        changed["hooks"]["verify-quality"]["gates"]["real-check"] = {"command": command, "timeout_s": 1}
        write_json(gates / "policy.json", changed)
        verify(label, 2, gate="real-check")
    (gates / "policy.json").write_text("{invalid json\n")
    run("invalid-policy-ci", ["bash", ".specify/gates/verify.sh", "--boundary", "ci", "--json"], root, expected=1)
    run("invalid-policy-stop-allows", hook, root, stdin="{}", kind="known-limit")
    write_json(gates / "policy.json", policy)
    runtime = gates / "verify.sh"
    runtime.rename(gates / "verify.saved")
    try:
        run("missing-runtime-stop-allows", hook, root, stdin="{}", kind="known-limit")
    finally:
        (gates / "verify.saved").rename(runtime)
    original_runtime = runtime.read_bytes()
    runtime.write_bytes(original_runtime + b"\n# locally edited experimental sentinel\n")
    run("local-runtime-edit-refused", ["bash", ".specify/gates/project.sh", "--check"], root, expected=3)
    observation("local-runtime-edit-retained", runtime.read_bytes() != original_runtime,
                "Projection refusal did not silently discard the local edit.")
    runtime.write_bytes(original_runtime)
    verify("restored", 0)
    observation("host-instructions-after-gates", all((root / n).read_text() == t for n, t in sentinels.items()),
                "Original instructions and constitution still match after the complete experiment.")
    return finish()


if __name__ == "__main__":
    sys.exit(main())
