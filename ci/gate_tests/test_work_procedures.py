"""Pin, preset, workflow, and opt-in copy checks for the routine work procedures.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
These tests do not execute Superpowers and do not run a benchmark trial.
"""

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PIN = ROOT / "vendor/superpowers/v7.0.2"
ACTIVE = (
    "systematic-debugging",
    "verification-before-completion",
    "writing-plans",
    "test-driven-development",
    "requesting-code-review",
    "executing-plans",
)


class WorkProcedures(unittest.TestCase):
    def test_pin_hashes_match_the_vendored_files(self):
        sums = (PIN / "SHA256SUMS").read_text(encoding="utf-8")
        seen = []
        for line in sums.splitlines():
            digest, relative = line.split("  ", 1)
            path = PIN / relative
            self.assertTrue(path.is_file(), relative)
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, actual, relative)
            seen.append(relative)
        self.assertIn("skills/executing-plans/SKILL.md", seen)
        self.assertIn("skills/systematic-debugging/SKILL.md", seen)
        self.assertNotIn(
            "skills/subagent-driven-development/SKILL.md",
            seen,
        )

    def test_active_skills_are_the_pinned_files(self):
        for name in ACTIVE:
            link = ROOT / ".cursor/skills" / name
            self.assertTrue(link.is_symlink(), name)
            self.assertEqual(
                (link / "SKILL.md").read_bytes(),
                (PIN / "skills" / name / "SKILL.md").read_bytes(),
            )
        orchestrator = ROOT / ".cursor/skills/subagent-driven-development"
        self.assertFalse((orchestrator / "SKILL.md").exists())
        self.assertTrue((orchestrator / "scripts/sdd-workspace").is_file())

    def test_documentation_exception_is_in_the_entry_point(self):
        text = (ROOT / ".cursor/skills/governed-work/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("documentation or registry-text change does not require", text)
        self.assertIn("22f0b463e7a5e579904dd6211a520321035526f7", text)

    def test_governed_workflow_has_no_approval_gate(self):
        governed = (
            ROOT / ".specify/workflows/ai-governance/workflow.yml"
        ).read_text(encoding="utf-8")
        bundled = (ROOT / ".specify/workflows/speckit/workflow.yml").read_text(encoding="utf-8")
        self.assertNotIn("type: gate", governed)
        self.assertEqual(bundled.count("type: gate"), 2)
        self.assertIn("verify-acceptance", governed)
        self.assertIn("bash ci/run_task_acceptance_check.sh", governed)
        self.assertRegex(governed, r"id: implement[\s\S]*id: verify-acceptance")
        self.assertIn("ai-governance", (ROOT / ".specify/workflows/workflow-registry.json").read_text(encoding="utf-8"))

    def test_preset_appends_continuation_to_the_core_spec_template(self):
        result = subprocess.run(
            ["bash", str(ROOT / ".specify/scripts/bash/resolve-template.sh"), "spec-template"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertIn("# Feature Specification:", result.stdout)
        self.assertIn("## Mandate continuation", result.stdout)
        self.assertIn("Automatic continuation", result.stdout)

    def test_opt_in_copy_keeps_host_files_and_refuses_a_repeat(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            agents = adopter / "AGENTS.md"
            overlay = adopter / "governance" / "LOCAL_OVERLAY.md"
            agents.write_text("HOST-SENTINEL\n", encoding="utf-8")
            overlay.parent.mkdir()
            overlay.write_text("OVERLAY-SENTINEL\n", encoding="utf-8")
            _copy_procedures(ROOT, adopter)
            self.assertEqual(agents.read_text(encoding="utf-8"), "HOST-SENTINEL\n")
            self.assertEqual(overlay.read_text(encoding="utf-8"), "OVERLAY-SENTINEL\n")
            entry = adopter / ".cursor/skills/governed-work/SKILL.md"
            pin = adopter / "vendor/superpowers/v7.0.2"
            self.assertFalse(entry.is_symlink())
            self.assertFalse((pin / "skills/executing-plans/SKILL.md").is_symlink())
            entry_text = entry.read_text(encoding="utf-8")
            self.assertIn("22f0b463e7a5e579904dd6211a520321035526f7", entry_text)
            self.assertIn("vendor/AI_governance/constitution/AI_ENFORCEMENT.md", entry_text)
            self.assertIn("install spec-gates or a Stop hook", entry_text)
            check = subprocess.run(
                ["sha256sum", "-c", "SHA256SUMS"],
                cwd=pin,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            with self.assertRaises(FileExistsError):
                _copy_procedures(ROOT, adopter)
            self.assertFalse((adopter / ".specify/presets/ai-governance").exists())

    def test_activation_smoke_after_opt_in_copy(self):
        """SC-002 disposable adopter: entry, pin, and routing need no path repair."""
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            _copy_procedures(ROOT, adopter)
            entry = adopter / ".cursor/skills/governed-work/SKILL.md"
            pin = adopter / "vendor/superpowers/v7.0.2"
            debug = pin / "skills/systematic-debugging/SKILL.md"
            self.assertTrue(entry.is_file())
            self.assertFalse(entry.is_symlink())
            self.assertTrue(debug.is_file())
            text = entry.read_text(encoding="utf-8")
            self.assertIn("documentation or registry-text change does not require", text)
            self.assertIn("| A failure, unexpected test result", text)
            self.assertIn("systematic-debugging", text)
            self.assertIn("vendor/superpowers/v7.0.2/", text)
            self.assertTrue((pin / "SHA256SUMS").is_file())

    def test_copy_refuses_a_dangling_skill_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            entry = adopter / ".cursor/skills/governed-work/SKILL.md"
            entry.parent.mkdir(parents=True)
            entry.symlink_to("missing")
            with self.assertRaises(FileExistsError):
                _copy_procedures(ROOT, adopter)
            self.assertTrue(entry.is_symlink())
            self.assertFalse((adopter / "vendor/superpowers/v7.0.2").exists())

    def test_upgrade_and_rollback_are_separate_commands(self):
        text = (ROOT / "usage/HOW_TO_IMPORT.md").read_text(encoding="utf-8")
        fences = []
        inside = False
        current = []
        for line in text.splitlines():
            if line.startswith("```"):
                if inside:
                    fences.append("\n".join(current))
                    current = []
                inside = not inside
                continue
            if inside:
                current.append(line)
        upgrade = [block for block in fences if "v7.0.2.next" in block]
        rollback = [block for block in fences if "v7.0.2.rollback" in block]
        self.assertEqual(len(upgrade), 1)
        self.assertEqual(len(rollback), 1)
        self.assertNotIn("rollback", upgrade[0])
        self.assertNotIn("rm -rf", upgrade[0])
        self.assertIn("test ! -e vendor/superpowers/v7.0.2.next", upgrade[0])
        self.assertIn("test ! -L vendor/superpowers/v7.0.2.next", upgrade[0])
        self.assertIn("test ! -e vendor/superpowers/v7.0.2.prev", upgrade[0])
        self.assertIn("test ! -L vendor/superpowers/v7.0.2.prev", upgrade[0])
        self.assertIn("test ! -e vendor/superpowers/v7.0.2.rollback", rollback[0])
        self.assertIn("test ! -L vendor/superpowers/v7.0.2.rollback", rollback[0])
        self.assertIn("rm -rf vendor/superpowers/v7.0.2.rollback", rollback[0])
        copy = [block for block in fences if "cp -L" in block and "governed-work/SKILL.md" in block]
        self.assertEqual(len(copy), 1)
        self.assertIn("test ! -L .cursor/skills/governed-work/SKILL.md", copy[0])

    def test_copy_refuses_an_existing_skill_without_a_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            entry = adopter / ".cursor/skills/governed-work/SKILL.md"
            entry.parent.mkdir(parents=True)
            entry.write_text("LOCAL-SKILL\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                _copy_procedures(ROOT, adopter)
            self.assertEqual(entry.read_text(encoding="utf-8"), "LOCAL-SKILL\n")
            self.assertFalse((adopter / "vendor/superpowers/v7.0.2").exists())

    def test_rollback_without_a_previous_pin_leaves_the_active_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            _copy_procedures(ROOT, adopter)
            pin = adopter / "vendor/superpowers/v7.0.2/PIN.md"
            original = pin.read_bytes()
            with self.assertRaises(FileNotFoundError):
                _rollback_pin(adopter)
            self.assertEqual(pin.read_bytes(), original)

    def test_upgrade_then_rollback_restores_the_pin_and_overlay(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            overlay = adopter / "governance" / "LOCAL_OVERLAY.md"
            overlay.parent.mkdir()
            overlay.write_text("OVERLAY-SENTINEL\n", encoding="utf-8")
            _copy_procedures(ROOT, adopter)
            active = adopter / "vendor/superpowers/v7.0.2"
            original = (active / "PIN.md").read_bytes()
            new_kit = Path(tmp) / "new-kit"
            candidate = new_kit / "vendor/superpowers/v7.0.2"
            shutil.copytree(active, candidate, symlinks=False)
            pin_md = candidate / "PIN.md"
            pin_md.write_text(pin_md.read_text(encoding="utf-8") + "\nupgrade-marker\n", encoding="utf-8")
            _rewrite_sums(candidate)
            env = os.environ.copy()
            env["NEW_KIT"] = str(new_kit)
            upgraded = _run_upgrade_block(adopter, env)
            self.assertEqual(upgraded.returncode, 0, upgraded.stdout + upgraded.stderr)
            self.assertIn("upgrade-marker", (active / "PIN.md").read_text(encoding="utf-8"))
            self.assertEqual(overlay.read_text(encoding="utf-8"), "OVERLAY-SENTINEL\n")
            _rollback_pin(adopter)
            self.assertEqual((active / "PIN.md").read_bytes(), original)
            self.assertEqual(overlay.read_text(encoding="utf-8"), "OVERLAY-SENTINEL\n")
            restored = subprocess.run(
                ["sha256sum", "-c", "SHA256SUMS"],
                cwd=active,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)

    def test_upgrade_refuses_a_stale_staging_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            _copy_procedures(ROOT, adopter)
            active = adopter / "vendor/superpowers/v7.0.2"
            original = (active / "PIN.md").read_bytes()
            shutil.copytree(active, adopter / "vendor/superpowers/v7.0.2.next", symlinks=False)
            new_kit = Path(tmp) / "new-kit"
            candidate = new_kit / "vendor/superpowers/v7.0.2"
            shutil.copytree(active, candidate, symlinks=False)
            pin_md = candidate / "PIN.md"
            pin_md.write_text(pin_md.read_text(encoding="utf-8") + "\nupgrade-marker\n", encoding="utf-8")
            _rewrite_sums(candidate)
            env = os.environ.copy()
            env["NEW_KIT"] = str(new_kit)
            upgraded = _run_upgrade_block(adopter, env)
            self.assertNotEqual(upgraded.returncode, 0, upgraded.stdout + upgraded.stderr)
            self.assertEqual((active / "PIN.md").read_bytes(), original)
            nested = active / "v7.0.2"
            self.assertFalse(nested.is_dir(), "upgrade must not nest the new pin under the active tree")

    def test_preset_copy_leaves_registry_unchanged_when_destination_is_a_dangling_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            registry = adopter / ".specify/presets/.registry"
            registry.parent.mkdir(parents=True)
            original = '{"schema_version":"1.0","presets":{}}\n'
            registry.write_text(original, encoding="utf-8")
            dest = adopter / ".specify/presets/ai-governance"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.symlink_to("missing-preset")
            env = os.environ.copy()
            env["KIT"] = str(ROOT)
            copied = _run_preset_copy(adopter, env)
            self.assertNotEqual(copied.returncode, 0, copied.stdout + copied.stderr)
            self.assertEqual(registry.read_text(encoding="utf-8"), original)
            self.assertTrue(dest.is_symlink())

    def test_preset_copy_leaves_registry_unchanged_when_copy_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            registry = adopter / ".specify/presets/.registry"
            registry.parent.mkdir(parents=True)
            original = '{"schema_version":"1.0","presets":{}}\n'
            registry.write_text(original, encoding="utf-8")
            _install_core_spec_template(adopter)
            fake_bin = Path(tmp) / "bin"
            fake_bin.mkdir()
            (fake_bin / "cp").write_text(
                "#!/bin/sh\n"
                'case "$*" in\n'
                '  *ai-governance*) exit 28 ;;\n'
                'esac\n'
                'exec /bin/cp "$@"\n',
                encoding="utf-8",
            )
            (fake_bin / "cp").chmod(0o755)
            env = os.environ.copy()
            env["KIT"] = str(ROOT)
            env["PATH"] = f"{fake_bin}:{env['PATH']}"
            copied = _run_preset_copy(adopter, env)
            self.assertEqual(copied.returncode, 28, copied.stdout + copied.stderr)
            self.assertEqual(registry.read_text(encoding="utf-8"), original)
            self.assertFalse((adopter / ".specify/presets/ai-governance").exists())

    def test_preset_copy_activates_against_an_empty_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            registry = adopter / ".specify/presets/.registry"
            registry.parent.mkdir(parents=True)
            registry.write_text(
                '{"schema_version":"1.0","presets":{}}\n',
                encoding="utf-8",
            )
            _install_core_spec_template(adopter)
            env = os.environ.copy()
            env["KIT"] = str(ROOT)
            copied = _run_preset_copy(adopter, env)
            self.assertEqual(copied.returncode, 0, copied.stdout + copied.stderr)
            data = json.loads(registry.read_text(encoding="utf-8"))
            self.assertTrue(data["presets"]["ai-governance"]["enabled"])
            resolved = _resolve_spec_template(adopter)
            self.assertEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)
            self.assertIn("# Feature Specification:", resolved.stdout)
            self.assertIn("## Mandate continuation", resolved.stdout)

    def test_command_only_preset_does_not_drop_the_governance_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            _install_core_spec_template(adopter)
            shutil.copytree(
                ROOT / ".specify/presets/ai-governance",
                adopter / ".specify/presets/ai-governance",
            )
            lean = adopter / ".specify/presets/lean"
            (lean / "commands").mkdir(parents=True)
            (lean / "preset.yml").write_text(
                "schema_version: '1.0'\n"
                "preset:\n"
                "  id: lean\n"
                "provides:\n"
                "  templates:\n"
                "    - type: command\n"
                "      name: speckit.specify\n"
                "      file: commands/speckit.specify.md\n",
                encoding="utf-8",
            )
            (lean / "commands/speckit.specify.md").write_text(
                "Ask the user for the feature directory.\n",
                encoding="utf-8",
            )
            registry = adopter / ".specify/presets/.registry"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "presets": {
                            "lean": {"enabled": True, "priority": 1, "version": "1.0.0", "source": "project"},
                            "ai-governance": {"enabled": True, "priority": 10, "version": "1.0.0", "source": "project"},
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            resolved = _resolve_spec_template(adopter)
            self.assertEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)
            self.assertIn("# Feature Specification:", resolved.stdout)
            self.assertIn("## Mandate continuation", resolved.stdout)
            self.assertNotIn("Ask the user", resolved.stdout)

    def test_preset_copy_keeps_an_existing_registry_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            registry = adopter / ".specify/presets/.registry"
            registry.parent.mkdir(parents=True)
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "presets": {
                            "local-preset": {
                                "version": "0.1.0",
                                "enabled": True,
                                "priority": 2,
                                "source": "project",
                            }
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            _install_core_spec_template(adopter)
            env = os.environ.copy()
            env["KIT"] = str(ROOT)
            copied = _run_preset_copy(adopter, env)
            self.assertEqual(copied.returncode, 0, copied.stdout + copied.stderr)
            data = json.loads(registry.read_text(encoding="utf-8"))
            self.assertEqual(data["presets"]["local-preset"]["version"], "0.1.0")
            self.assertTrue(data["presets"]["ai-governance"]["enabled"])
            resolved = _resolve_spec_template(adopter)
            self.assertEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)
            self.assertIn("# Feature Specification:", resolved.stdout)
            self.assertIn("## Mandate continuation", resolved.stdout)
            again = _run_preset_copy(adopter, env)
            self.assertNotEqual(again.returncode, 0, again.stdout + again.stderr)
            self.assertEqual(
                json.loads(registry.read_text(encoding="utf-8"))["presets"]["local-preset"]["version"],
                "0.1.0",
            )


def _install_core_spec_template(adopter):
    templates = adopter / ".specify/templates"
    templates.mkdir(parents=True)
    shutil.copyfile(ROOT / ".specify/templates/spec-template.md", templates / "spec-template.md")


def _run_preset_copy(adopter, env):
    return subprocess.run(
        ["bash", "-c", _preset_copy_block()],
        cwd=adopter,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )


def _run_upgrade_block(adopter, env):
    return subprocess.run(
        ["bash", "-c", _upgrade_block()],
        cwd=adopter,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )


def _upgrade_block():
    text = (ROOT / "usage/HOW_TO_IMPORT.md").read_text(encoding="utf-8")
    fences = []
    inside = False
    current = []
    for line in text.splitlines():
        if line.startswith("```"):
            if inside:
                fences.append("\n".join(current))
                current = []
            inside = not inside
            continue
        if inside:
            current.append(line)
    matches = [block for block in fences if "v7.0.2.next" in block and "NEW_KIT" in block]
    if len(matches) != 1:
        raise AssertionError("expected one upgrade command")
    return matches[0]


def _resolve_spec_template(adopter):
    return subprocess.run(
        ["bash", str(ROOT / ".specify/scripts/bash/resolve-template.sh"), "spec-template"],
        cwd=adopter,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )


def _preset_copy_block():
    text = (ROOT / "usage/HOW_TO_IMPORT.md").read_text(encoding="utf-8")
    fences = []
    inside = False
    current = []
    for line in text.splitlines():
        if line.startswith("```"):
            if inside:
                fences.append("\n".join(current))
                current = []
            inside = not inside
            continue
        if inside:
            current.append(line)
    matches = [
        block
        for block in fences
        if 'cp -aL "$KIT/.specify/presets/ai-governance"' in block
    ]
    if len(matches) != 1:
        raise AssertionError("expected one preset copy command")
    return matches[0]


def _rewrite_sums(pin):
    lines = []
    for path in sorted(item for item in pin.rglob("*") if item.is_file() and item.name != "SHA256SUMS"):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(pin).as_posix()}")
    (pin / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _rollback_pin(adopter):
    base = adopter / "vendor/superpowers"
    active = base / "v7.0.2"
    previous = base / "v7.0.2.prev"
    holding = base / "v7.0.2.rollback"
    if not previous.is_dir() or not active.is_dir():
        raise FileNotFoundError(previous)
    if _path_present(holding):
        raise FileExistsError(holding)
    active.rename(holding)
    previous.rename(active)
    shutil.rmtree(holding)


def _path_present(path):
    return path.is_symlink() or path.exists()


def _copy_procedures(kit, adopter):
    """Regular-file copy used by usage/HOW_TO_IMPORT.md. Refuse an existing pin or skill."""
    pin_dest = adopter / "vendor/superpowers/v7.0.2"
    entry = adopter / ".cursor/skills/governed-work/SKILL.md"
    if _path_present(pin_dest):
        raise FileExistsError(pin_dest)
    if _path_present(entry):
        raise FileExistsError(entry)
    pin_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(kit / "vendor/superpowers/v7.0.2", pin_dest, symlinks=False)
    entry.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(kit / ".cursor/skills/governed-work/SKILL.md", entry)
