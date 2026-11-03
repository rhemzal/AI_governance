"""Pin, preset, and workflow checks for the routine work procedures.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
These tests do not execute Superpowers and do not run a benchmark trial.
"""

import hashlib
import subprocess
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
