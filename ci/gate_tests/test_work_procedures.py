"""Pin, preset, workflow, and opt-in copy checks for the routine work procedures.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
These tests do not execute Superpowers and do not run a benchmark trial.
"""

import hashlib
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PIN = ROOT / "vendor/superpowers/v7.0.1"
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
        self.assertIn("2ce8aa15d05bd57213e6f746f953aafb7ded7a8b", text)

    def test_governed_workflow_has_no_approval_gate(self):
        governed = (
            ROOT / ".specify/workflows/ai-governance/workflow.yml"
        ).read_text(encoding="utf-8")
        bundled = (ROOT / ".specify/workflows/speckit/workflow.yml").read_text(encoding="utf-8")
        self.assertNotIn("type: gate", governed)
        self.assertEqual(bundled.count("type: gate"), 2)
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
            pin = adopter / "vendor/superpowers/v7.0.1"
            self.assertFalse(entry.is_symlink())
            self.assertFalse((pin / "skills/executing-plans/SKILL.md").is_symlink())
            entry_text = entry.read_text(encoding="utf-8")
            self.assertIn("2ce8aa15d05bd57213e6f746f953aafb7ded7a8b", entry_text)
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

    def test_upgrade_then_rollback_restores_the_pin_and_overlay(self):
        with tempfile.TemporaryDirectory() as tmp:
            adopter = Path(tmp)
            overlay = adopter / "governance" / "LOCAL_OVERLAY.md"
            overlay.parent.mkdir()
            overlay.write_text("OVERLAY-SENTINEL\n", encoding="utf-8")
            _copy_procedures(ROOT, adopter)
            active = adopter / "vendor/superpowers/v7.0.1"
            original = (active / "PIN.md").read_bytes()
            staged = adopter / "vendor/superpowers/v7.0.1.next"
            shutil.copytree(active, staged, symlinks=False)
            pin_md = staged / "PIN.md"
            pin_md.write_text(pin_md.read_text(encoding="utf-8") + "\nupgrade-marker\n", encoding="utf-8")
            _rewrite_sums(staged)
            check = subprocess.run(
                ["sha256sum", "-c", "SHA256SUMS"],
                cwd=staged,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            _activate_staged_pin(adopter)
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


def _rewrite_sums(pin):
    lines = []
    for path in sorted(item for item in pin.rglob("*") if item.is_file() and item.name != "SHA256SUMS"):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(pin).as_posix()}")
    (pin / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _activate_staged_pin(adopter):
    base = adopter / "vendor/superpowers"
    active = base / "v7.0.1"
    staged = base / "v7.0.1.next"
    previous = base / "v7.0.1.prev"
    if not staged.is_dir():
        raise FileNotFoundError(staged)
    if previous.exists():
        raise FileExistsError(previous)
    active.rename(previous)
    staged.rename(active)


def _rollback_pin(adopter):
    base = adopter / "vendor/superpowers"
    active = base / "v7.0.1"
    previous = base / "v7.0.1.prev"
    if not previous.is_dir():
        raise FileNotFoundError(previous)
    if active.exists():
        shutil.rmtree(active)
    previous.rename(active)


def _copy_procedures(kit, adopter):
    """Regular-file copy used by usage/HOW_TO_IMPORT.md. Refuse an existing pin."""
    pin_dest = adopter / "vendor/superpowers/v7.0.1"
    if pin_dest.exists():
        raise FileExistsError(pin_dest)
    pin_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(kit / "vendor/superpowers/v7.0.1", pin_dest, symlinks=False)
    entry_dir = adopter / ".cursor/skills/governed-work"
    entry_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        kit / ".cursor/skills/governed-work/SKILL.md",
        entry_dir / "SKILL.md",
    )
    preset_dest = adopter / ".specify/presets/ai-governance"
    shutil.copytree(
        kit / ".specify/presets/ai-governance",
        preset_dest,
        symlinks=False,
    )
