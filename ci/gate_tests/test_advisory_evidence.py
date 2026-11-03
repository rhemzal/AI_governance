"""Execute the DOC DELTA and waiver advisories against empty and populated fixtures.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
Python standard library, Bash and Git. Advisory checks warn and still exit 0.
"""

import os
from pathlib import Path
import re
import subprocess
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[2]
STARTERS = (ROOT / "usage/CI_STARTER_WORKFLOWS.md").read_text()
DOC_WORKFLOW = (ROOT / ".github/workflows/doc-delta-advisory.yml").read_text()
WAIVER_WORKFLOW = (ROOT / ".github/workflows/governance-waiver-advisory.yml").read_text()

EMPTY_DOC = """### DOC DELTA
- Source of truth:
  - Code:
  - Tests:
  - ADRs:
- Docs updated (paths):
- Docs removed/merged (paths):
- Generated docs?
  - yes/no
- Review checklist:
  - Links valid: yes/no
"""
POPULATED_DOC = """### DOC DELTA
- Docs updated (paths): usage/AGENT_EVALUATION.md
"""
EMPTY_WAIVER = """### Governance waiver (only if gate bypassed)
- Gate ID:
- Owner:
- Expiration: YYYY-MM-DD
- Compensating control:
- PR/issue:
"""
POPULATED_WAIVER = """### Governance waiver (only if gate bypassed)
- Gate ID: D2
- Owner: kit maintainer
- Expiration: 2026-12-01
- Compensating control: Reviewer reads the documentation list.
"""


def section_block(text, heading):
    section = text.split(heading, 1)[1]
    return section.split("```yaml\n", 1)[1].split("```", 1)[0]


def run_block(yaml_text):
    match = re.search(r"^( +)run: \|\n", yaml_text, re.MULTILINE)
    if not match:
        raise AssertionError("Expected one literal run block")
    lines = []
    for line in yaml_text[match.end():].splitlines():
        if line.strip() and len(line) - len(line.lstrip(" ")) <= len(match[1]):
            break
        lines.append(line)
    return textwrap.dedent("\n".join(lines)).rstrip() + "\n"


def heredoc(script):
    match = re.search(r"<<'PY'\n(.*)\nPY\n", script, re.S)
    if not match:
        raise AssertionError("Expected a PY heredoc")
    return match.group(1)


DOC_KIT = run_block(DOC_WORKFLOW)
DOC_STARTER = run_block(section_block(STARTERS, "## 7)"))
WAIVER_KIT = run_block(WAIVER_WORKFLOW)
WAIVER_STARTER = run_block(section_block(STARTERS, "## 6)"))


def shell(script, cwd, env):
    return subprocess.run(["bash", "-c", script], cwd=cwd, capture_output=True,
                          text=True, timeout=15, env=env)


class AdvisoryEvidence(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Gate fixture")
        self.git("config", "user.email", "gate-fixture@example.invalid")
        self.write("README.md", "base\n")
        self.base = self.commit()
        self.head = self.base

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True,
                                       stderr=subprocess.STDOUT, timeout=10).strip()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-qm", "Fixture change")
        return self.git("rev-parse", "HEAD")

    def change(self, path, text):
        self.write(path, text)
        self.head = self.commit()

    def invoke(self, script, body):
        env = os.environ.copy()
        env.update(PR_BODY=body, BASE_SHA=self.base, HEAD_SHA=self.head)
        return shell(script, self.root, env)

    def assert_doc_warns(self, result):
        message = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, message)
        self.assertIn("::warning::", result.stdout)
        self.assertNotIn("DOC DELTA present.", result.stdout)

    def assert_doc_present(self, result):
        message = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, message)
        self.assertIn("DOC DELTA present.", result.stdout)
        self.assertNotIn("::warning::", result.stdout)

    def test_section_predicates_match_and_waiver_blocks_match(self):
        self.assertEqual(heredoc(DOC_KIT), heredoc(DOC_STARTER))
        self.assertEqual(WAIVER_KIT, WAIVER_STARTER)

    def test_empty_doc_delta_heading_still_warns(self):
        self.change("src/app.py", "print(1)\n")
        for body in ("", "The notes mention DOC DELTA without a section.\n",
                     "### DOC DELTA\n", EMPTY_DOC):
            for script in (DOC_KIT, DOC_STARTER):
                with self.subTest(body=body[:24], script=script[:12]):
                    self.assert_doc_warns(self.invoke(script, body))

    def test_populated_doc_delta_section_suppresses_the_warning(self):
        self.change("src/app.py", "print(1)\n")
        for script in (DOC_KIT, DOC_STARTER):
            self.assert_doc_present(self.invoke(script, POPULATED_DOC))

    def test_doc_only_change_does_not_require_a_section(self):
        self.change("usage/NOTE.md", "note\n")
        for script in (DOC_KIT, DOC_STARTER):
            result = self.invoke(script, "")
            message = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, message)
            self.assertNotIn("::warning::", result.stdout)

    def test_kit_workflow_prefix_exemption_is_not_in_the_starter(self):
        self.change(".github/workflows/extra.yml", "name: extra\n")
        kit = self.invoke(DOC_KIT, "")
        starter = self.invoke(DOC_STARTER, "")
        self.assertIn("not required", kit.stdout)
        self.assertNotIn("::warning::", kit.stdout)
        self.assert_doc_warns(starter)

    def test_empty_waiver_template_warns(self):
        for body in ("", "Gate ID: D2 is mentioned outside any section.\n", EMPTY_WAIVER):
            result = self.invoke(WAIVER_KIT, body)
            message = result.stdout + result.stderr
            with self.subTest(body=body[:24]):
                self.assertEqual(result.returncode, 0, message)
                self.assertIn("::warning::", result.stdout)

    def test_placeholder_expiration_warns_and_a_real_date_does_not(self):
        bad = POPULATED_WAIVER.replace("2026-12-01", "2026-02-31")
        warned = self.invoke(WAIVER_KIT, bad)
        self.assertEqual(warned.returncode, 0, warned.stderr)
        self.assertIn("Waiver block missing value: Expiration", warned.stdout)
        self.assertNotIn("Gate ID", warned.stdout)
        quiet = self.invoke(WAIVER_KIT, POPULATED_WAIVER)
        self.assertEqual(quiet.returncode, 0, quiet.stderr)
        self.assertNotIn("::warning::", quiet.stdout)
