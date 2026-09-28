"""Execute the copyable boundary/ADR checks against disposable failure fixtures.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
Python standard library, Bash and Git; no product code or imported code executes.
"""

import os
from pathlib import Path
import re
import subprocess
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[2]
RECIPES = (ROOT / "usage/BOUNDARY_GATE_RECIPES.md").read_text()
STARTERS = (ROOT / "usage/CI_STARTER_WORKFLOWS.md").read_text()
ADR_WORKFLOW = (ROOT / ".github/workflows/adr-required.yml").read_text()


def section_block(text, heading, language):
    section = text.split(heading, 1)[1]
    return section.split("```" + language + "\n", 1)[1].split("```", 1)[0]


def run_block(yaml_text):
    # Extract a single literal run block without adding a YAML runtime dependency.
    match = re.search(r"^( +)run: \|\n", yaml_text, re.MULTILINE)
    if not match:
        raise AssertionError("Expected one literal run block")
    lines = []
    for line in yaml_text[match.end():].splitlines():
        if line.strip() and len(line) - len(line.lstrip(" ")) <= len(match[1]):
            break
        lines.append(line)
    return textwrap.dedent("\n".join(lines)).rstrip() + "\n"


PYTHON_RECIPE = section_block(RECIPES, "## Python\n", "bash")
GO_RECIPE = section_block(RECIPES, "## Go\n", "bash")
PYTHON_STARTER = run_block(section_block(STARTERS, "### 3a)", "yaml"))
GO_STARTER = run_block(section_block(STARTERS, "### 3c)", "yaml"))
ADR_STARTER_YAML = section_block(STARTERS, "## 4)", "yaml")
ADR_CHECKS = (run_block(ADR_WORKFLOW), run_block(ADR_STARTER_YAML))


def shell(script, cwd, **kwargs):
    return subprocess.run(["bash", "-c", script], cwd=cwd, capture_output=True,
                          text=True, timeout=10, **kwargs)


class BoundaryRecipes(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def source(self, relative, contents):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents)
        return path

    def assert_checks(self, checks, passes, **kwargs):
        for script in checks:
            with self.subTest(script=script[:80]):
                result = shell(script, self.root, **kwargs)
                message = result.stdout + result.stderr
                if passes:
                    self.assertEqual(result.returncode, 0, message)
                    self.assertIn("PASS:", message)
                else:
                    self.assertNotEqual(result.returncode, 0, message)
                    self.assertTrue(message.strip(), "Failure needs a diagnostic")

    def test_copyable_boundary_blocks_match_the_recipes(self):
        self.assertEqual(PYTHON_RECIPE, PYTHON_STARTER)
        self.assertEqual(GO_RECIPE, GO_STARTER)

    def test_python_rejects_direct_from_indented_relative_and_multiline_imports(self):
        examples = (
            "import infra", "from infra import database", "from infra.database import connect",
            "import os, adapters.http as transport", "from myapp.infra import database",
            "def f():\n    import infra", "from .infra import database", "from .. import adapters",
            "from . import (\n    infra as storage,\n)", "from myapp import (ports, infra)",
        )
        for code in examples:
            with self.subTest(code=code):
                self.source("src/myapp/domain/nested/rules.py", code + "\n")
                self.assert_checks((PYTHON_RECIPE, PYTHON_STARTER), False)

    def test_python_allows_core_imports_and_ignores_comments_and_strings(self):
        self.source("src/myapp/domain/rules.py",
                    'from ..ports import clock\nimport infra_tools\n'
                    '# import infra\nexample = "from adapters import http"\n'
                    'raise RuntimeError("must not execute source")\n')
        self.assert_checks((PYTHON_RECIPE, PYTHON_STARTER), True)

    def test_python_missing_empty_invalid_and_symlinked_sources_fail(self):
        self.assert_checks((PYTHON_RECIPE, PYTHON_STARTER), False)
        root = self.root / "src/myapp/domain"
        root.mkdir(parents=True)
        self.assert_checks((PYTHON_RECIPE, PYTHON_STARTER), False)
        source = self.source("src/myapp/domain/rules.py", "def broken(\n")
        self.assert_checks((PYTHON_RECIPE, PYTHON_STARTER), False)
        source.unlink()
        source.symlink_to(self.source("elsewhere.py", "pass\n"))
        self.assert_checks((PYTHON_RECIPE, PYTHON_STARTER), False)

    @unittest.skipUnless(os.name == "posix" and os.geteuid() != 0,
                         "Requires an unprivileged POSIX runner; root bypasses chmod")
    def test_python_unreadable_source_and_directory_fail(self):
        source = self.source("src/myapp/domain/nested/rules.py", "pass\n")
        self.root.chmod(0o755)
        for path in (source, source.parent):
            path.chmod(0)
            try:
                self.assert_checks((PYTHON_RECIPE, PYTHON_STARTER), False)
            finally:
                path.chmod(0o755 if path.is_dir() else 0o644)

    def test_go_rejects_ordinary_alias_raw_and_subpackage_paths(self):
        for code in ('import "example.com/myapp/internal/infra"',
                     'import db "example.com/myapp/internal/infra/database"',
                     'import (\n  "example.com/myapp/internal/infra"\n)',
                     'import `example.com/myapp/internal/infra`'):
            with self.subTest(code=code):
                self.source("pkg/domain/rules.go", "package domain\n" + code + "\n")
                self.assert_checks((GO_RECIPE, GO_STARTER), False)

    def test_go_allows_other_paths_and_rejects_missing_and_empty_roots(self):
        self.assert_checks((GO_RECIPE, GO_STARTER), False)
        (self.root / "pkg/domain").mkdir(parents=True)
        self.assert_checks((GO_RECIPE, GO_STARTER), False)
        self.source("pkg/domain/rules.go", 'package domain\nimport "example.com/myapp/ports"\n')
        self.assert_checks((GO_RECIPE, GO_STARTER), True)

    def test_go_scanner_exit_two_fails_even_when_running_as_root(self):
        self.source("pkg/domain/rules.go", "package domain\n")
        scanner = self.source("bin/grep", "#!/bin/sh\necho 'Injected scanner error' >&2\nexit 2\n")
        scanner.chmod(0o755)
        env = {**os.environ, "PATH": str(scanner.parent) + os.pathsep + os.environ["PATH"]}
        for script in (GO_RECIPE, GO_STARTER):
            result = shell(script, self.root, env=env)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Boundary scan failed", result.stderr)

    @unittest.skipUnless(os.name == "posix" and os.geteuid() != 0,
                         "Requires an unprivileged POSIX runner; root bypasses chmod")
    def test_go_scanner_error_is_not_an_allowed_import(self):
        source = self.source("pkg/domain/rules.go", "package domain\n")
        self.root.chmod(0o755)
        source.chmod(0)
        try:
            for script in (GO_RECIPE, GO_STARTER):
                result = shell(script, self.root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Boundary scan failed", result.stderr)
        finally:
            source.chmod(0o644)


class AdrGate(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Gate fixture")
        self.git("config", "user.email", "gate-fixture@example.invalid")
        self.write("constitution/RULES.md", "Original rule\n")
        self.write("adr/ADR_0001_Existing.md", "# Existing decision\n\nAccepted rationale.\n")
        self.base = self.commit()

    def git(self, *args, cwd=None):
        return subprocess.check_output(["git", *args], cwd=cwd or self.root,
                                       stderr=subprocess.STDOUT, text=True, timeout=10).strip()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-qm", "Fixture change")
        return self.git("rev-parse", "HEAD")

    def check(self, passes, head=None, cwd=None):
        env = {**os.environ, "BASE_SHA": self.base, "HEAD_SHA": head or self.commit()}
        for script in ADR_CHECKS:
            result = shell(script, cwd or self.root, env=env)
            with self.subTest(script=script[:60]):
                if passes:
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                else:
                    self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_starter_and_workflow_share_check_and_full_history_configuration(self):
        self.assertEqual(*ADR_CHECKS)
        for text in (ADR_STARTER_YAML, ADR_WORKFLOW):
            self.assertRegex(text, r"uses: actions/checkout@v4\n\s+with:\n\s+fetch-depth: 0\n")
            self.assertIn("BASE_SHA: ${{ github.event.pull_request.base.sha }}", text)
            self.assertIn("HEAD_SHA: ${{ github.sha }}", text)

    def test_governance_change_without_adr_fails(self):
        self.write("constitution/RULES.md", "Changed rule\n")
        self.check(False)

    def test_deleted_numbered_adr_does_not_satisfy_gate(self):
        self.write("constitution/RULES.md", "Changed rule\n")
        (self.root / "adr/ADR_0001_Existing.md").unlink()
        self.check(False)

    def test_template_only_does_not_satisfy_gate(self):
        self.write("constitution/RULES.md", "Changed rule\n")
        self.write("adr/ADR_TEMPLATE.md", "# Decision template\n")
        self.check(False)

    def test_rename_away_or_renumber_alone_does_not_satisfy_gate(self):
        for target in ("archived.md", "adr/ADR_0002_Renumbered.md"):
            with self.subTest(target=target):
                self.git("reset", "--hard", self.base)
                self.write("constitution/RULES.md", "Changed rule\n")
                self.git("mv", "adr/ADR_0001_Existing.md", target)
                self.check(False)

    def test_added_and_updated_numbered_regular_records_pass(self):
        for target in ("adr/ADR_0002_New.md", "adr/ADR_0001_Existing.md"):
            with self.subTest(target=target):
                self.git("reset", "--hard", self.base)
                self.write("constitution/RULES.md", "Changed rule\n")
                self.write(target, "# Explicit decision\n\nNew reason and enforcement.\n")
                self.check(True)

    def test_unchanged_adr_and_untracked_worktree_decision_do_not_count(self):
        self.write("constitution/RULES.md", "Changed rule\n")
        head = self.commit()
        self.write("adr/ADR_0002_Untracked.md", "# Working tree only\n")
        self.check(False, head=head)

    def test_symlink_and_type_change_are_not_decision_updates(self):
        for target in ("adr/ADR_0002_Link.md", "adr/ADR_0001_Existing.md"):
            with self.subTest(target=target):
                self.git("reset", "--hard", self.base)
                self.write("constitution/RULES.md", "Changed rule\n")
                path = self.root / target
                if path.exists():
                    path.unlink()
                path.symlink_to("../constitution/RULES.md")
                self.check(False)

    def test_renaming_out_of_governance_still_triggers_check(self):
        self.git("mv", "constitution/RULES.md", "RULES.md")
        self.check(False)

    def test_usage_only_changes_skip_requirement(self):
        self.write("usage/example.md", "Documentation only\n")
        self.check(True)

    def test_shallow_pr_merge_needs_history_and_full_fetch_restores_it(self):
        self.git("checkout", "-qb", "feature")
        self.write("constitution/RULES.md", "Changed rule\n")
        self.write("adr/ADR_0002_New.md", "# New decision\n")
        self.commit()
        self.git("checkout", "-q", "main")
        self.write("README.md", "Base advances independently\n")
        self.base = self.commit()
        self.git("merge", "--no-ff", "-qm", "PR merge fixture", "feature")
        head = self.git("rev-parse", "HEAD")
        clone = Path(self.temp.name) / "shallow"
        self.git("clone", "-q", "--depth=1", self.root.as_uri(), str(clone))
        self.assertEqual(self.git("rev-parse", "--is-shallow-repository", cwd=clone), "true")
        self.check(False, head=head, cwd=clone)
        # Equivalent history availability to the documented checkout fetch-depth: 0.
        self.git("fetch", "-q", "--unshallow", cwd=clone)
        self.check(True, head=head, cwd=clone)


if __name__ == "__main__":
    unittest.main()
