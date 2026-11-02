"""Execute published doc-hygiene steps against planted failures.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
Python standard library, Bash and Git. The cross-ref step is fed a path list
through a stand-in yq. Lychee is not run.
"""

import os
from pathlib import Path
import re
import subprocess
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = (ROOT / ".github/workflows/doc-hygiene.yml").read_text()


def named_run(yaml_text, step_name):
    marker = f"- name: {step_name}\n"
    start = yaml_text.find(marker)
    if start < 0:
        raise AssertionError(f"missing step: {step_name}")
    match = re.search(r"^( +)run: \|\n", yaml_text[start:], re.MULTILINE)
    if not match:
        raise AssertionError(f"missing run block: {step_name}")
    lines = []
    block = yaml_text[start + match.end():]
    indent = len(match.group(1))
    for line in block.splitlines():
        if line.strip() and len(line) - len(line.lstrip(" ")) <= indent:
            break
        lines.append(line)
    return textwrap.dedent("\n".join(lines)).rstrip() + "\n"


ROOT_META = named_run(WORKFLOW, "Required root meta files exist")
PROVENANCE = named_run(WORKFLOW, "Provenance banners on import targets")
ANTI_FRAGMENTATION = named_run(WORKFLOW, "Anti-fragmentation (D5, PR only)")
CROSS_REF = named_run(WORKFLOW, "Bundled cross-refs (checklist item 3)")
ROOT_FILES = ("README.md", "kit-manifest.yml", "VERSIONING.md", "DEVELOPMENT.md", "CHANGELOG.md")


def shell(script, cwd, env=None):
    return subprocess.run(["bash", "-c", script], cwd=cwd, capture_output=True,
                          text=True, timeout=15, env=env)


class DocHygieneBlocks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True,
                                       stderr=subprocess.STDOUT, timeout=10).strip()

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-qm", "Fixture change")
        return self.git("rev-parse", "HEAD")

    def test_missing_root_meta_file_fails_and_the_set_passes(self):
        missing = shell(ROOT_META, self.root)
        self.assertNotEqual(missing.returncode, 0, missing.stdout + missing.stderr)
        self.assertIn("Missing required file: README.md", missing.stdout + missing.stderr)
        for name in ROOT_FILES:
            self.write(name, "present\n")
        present = shell(ROOT_META, self.root)
        self.assertEqual(present.returncode, 0, present.stdout + present.stderr)

    def test_missing_provenance_banner_fails(self):
        self.write("constitution/NOTE.md", "No banner here.\n")
        late = "x" * 500 + "\nProvenance: too late\n"
        self.write("usage/LATE.md", late)
        result = shell(PROVENANCE, self.root)
        message = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, message)
        self.assertIn("Missing Provenance banner: constitution/NOTE.md", message)
        self.assertIn("Missing Provenance banner: usage/LATE.md", message)

    def test_provenance_banner_in_the_header_passes(self):
        self.write("constitution/NOTE.md", "Provenance: kit\n\nBody.\n")
        self.write("AGENTS.md", "Provenance: kit\n")
        result = shell(PROVENANCE, self.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unlinked_new_usage_doc_fails_and_a_linked_name_passes(self):
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Gate fixture")
        self.git("config", "user.email", "gate-fixture@example.invalid")
        self.write("README.md", "See AGENT_EVALUATION.md.\n")
        self.write("architecture/README.md", "hub\n")
        self.write("usage/DEBUGGING_INDEX.md", "hub\n")
        base = self.commit()
        self.write("usage/UNLINKED_DOC.md", "new\n")
        head = self.commit()
        env = os.environ.copy()
        env.update(BASE_SHA=base, HEAD_SHA=head)
        failed = shell(ANTI_FRAGMENTATION, self.root, env)
        message = failed.stdout + failed.stderr
        self.assertNotEqual(failed.returncode, 0, message)
        self.assertIn("usage/UNLINKED_DOC.md", message)
        self.git("rm", "-q", "usage/UNLINKED_DOC.md")
        self.write("usage/AGENT_EVALUATION.md", "linked by basename\n")
        head = self.commit()
        env["HEAD_SHA"] = head
        passed = shell(ANTI_FRAGMENTATION, self.root, env)
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)

    def yq_env(self, paths):
        bindir = Path(self.temp.name) / "bin"
        bindir.mkdir(exist_ok=True)
        script = bindir / "yq"
        body = "#!/bin/sh\n" + "".join(f"printf '%s\\n' '{path}'\n" for path in paths)
        script.write_text(body)
        script.chmod(0o755)
        env = os.environ.copy()
        env["PATH"] = str(bindir) + os.pathsep + "/usr/bin:/bin"
        return env

    def test_usage_link_outside_the_bundle_fails(self):
        self.write("usage/QUICKGUIDE.md", "See [other](../OUTSIDE.md).\n")
        self.write("OUTSIDE.md", "exists\n")
        result = shell(CROSS_REF, self.root, self.yq_env(["usage/"]))
        message = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, message)
        self.assertIn("Bundled cross-ref FAIL (minimal): usage/QUICKGUIDE.md references OUTSIDE.md", message)

    def test_usage_link_inside_a_bundle_directory_passes(self):
        self.write("usage/QUICKGUIDE.md", "See [plan](AEP_VALIDATION.md).\n")
        self.write("usage/AEP_VALIDATION.md", "No further links.\n")
        result = shell(CROSS_REF, self.root, self.yq_env(["usage/"]))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_allowlisted_root_link_passes_and_other_root_names_fail(self):
        self.write("usage/QUICKGUIDE.md", "See [hub](../README.md) and `CHANGELOG.md`.\n")
        self.write("README.md", "hub\n")
        self.write("CHANGELOG.md", "log\n")
        result = shell(CROSS_REF, self.root, self.yq_env(["usage/"]))
        message = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, message)
        self.assertIn("references CHANGELOG.md", message)
        self.assertNotIn("references README.md", message)

    def test_cross_ref_fails_closed_without_yq(self):
        self.write("usage/QUICKGUIDE.md", "See [plan](AEP_VALIDATION.md).\n")
        self.write("usage/AEP_VALIDATION.md", "body\n")
        env = os.environ.copy()
        env["PATH"] = "/usr/bin:/bin"
        result = shell(CROSS_REF, self.root, env)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
