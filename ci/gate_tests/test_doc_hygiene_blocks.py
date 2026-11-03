"""Execute published doc-hygiene steps against planted failures.

Provenance: AI_governance kit (https://github.com/rhemzal/AI_governance).
Python standard library, Bash and Git. Some steps use a stand-in yq path list.
One canary runs the pinned yq release, and one runs the pinned lychee release
offline. Offline lychee does not resolve remote URLs.
"""

import os
from pathlib import Path
import re
import shlex
import subprocess
import tarfile
import tempfile
import textwrap
import urllib.request
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
MANIFEST_PATHS = named_run(WORKFLOW, "Manifest explicit paths exist")
COUPLING = named_run(WORKFLOW, "Constitution edits touch the claim-card registry")
ROOT_FILES = ("README.md", "kit-manifest.yml", "VERSIONING.md", "DEVELOPMENT.md", "CHANGELOG.md")


def pinned_yq():
    """Return the yq release named in doc-hygiene, cached outside the repo."""
    match = re.search(
        r"https://github.com/mikefarah/yq/releases/download/(v\d+\.\d+\.\d+)/yq_linux_amd64",
        WORKFLOW,
    )
    if not match:
        raise AssertionError("doc-hygiene no longer names a pinned linux yq release")
    version, url = match.group(1), match.group(0)
    bindir = Path("/tmp") / f"ai-governance-yq-{version}"
    binary = bindir / "yq"
    if not binary.is_file():
        bindir.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(url, headers={"User-Agent": "ai-governance-gate-test"})
        with urllib.request.urlopen(request, timeout=30) as response:
            binary.write_bytes(response.read())
        binary.chmod(0o755)
    env = os.environ.copy()
    env["PATH"] = str(bindir) + os.pathsep + "/usr/bin:/bin"
    return binary, env, version


def pinned_lychee():
    """Return the lychee release and hub arguments named in doc-hygiene."""
    match = re.search(r"lycheeVersion:\s*(v\d+\.\d+\.\d+)\s*\n\s*args:\s*(.+)", WORKFLOW)
    if not match:
        raise AssertionError("doc-hygiene no longer names a lychee version and args")
    version, tokens = match.group(1), shlex.split(match.group(2).strip())
    flags = [token for token in tokens if token.startswith("-")]
    hubs = [token for token in tokens if not token.startswith("-")]
    bindir = Path("/tmp") / f"ai-governance-lychee-{version}"
    binary = bindir / "lychee"
    if not binary.is_file():
        bindir.mkdir(parents=True, exist_ok=True)
        archive = bindir / "lychee.tar.gz"
        if not archive.is_file():
            url = (
                "https://github.com/lycheeverse/lychee/releases/download/"
                f"lychee-{version}/lychee-x86_64-unknown-linux-gnu.tar.gz"
            )
            request = urllib.request.Request(url, headers={"User-Agent": "ai-governance-gate-test"})
            with urllib.request.urlopen(request, timeout=60) as response:
                archive.write_bytes(response.read())
        with tarfile.open(archive) as tar:
            member = next(
                item for item in tar.getmembers()
                if Path(item.name).name == "lychee" and item.isfile()
            )
            extracted = tar.extractfile(member)
            binary.write_bytes(extracted.read())
        binary.chmod(0o755)
    return binary, flags, hubs, version


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

    def test_passing_hygiene_does_not_close_findings(self):
        findings = "A-08 remains open.\n"
        self.write("usage/FIX_PLAN.md", findings)
        for name in ROOT_FILES:
            self.write(name, "present\n")
        result = shell(ROOT_META, self.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(findings, (self.root / "usage/FIX_PLAN.md").read_text(encoding="utf-8"))
        self.assertNotIn("closed", result.stdout.casefold())
        self.assertNotIn("FIX_PLAN", WORKFLOW)

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

    def yq_env(self, paths, fail=False):
        bindir = Path(self.temp.name) / "bin"
        bindir.mkdir(exist_ok=True)
        script = bindir / "yq"
        if fail:
            body = "#!/bin/sh\nexit 2\n"
        else:
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

    def test_missing_manifest_directory_fails(self):
        self.write("usage/keep.md", "ok\n")
        result = shell(MANIFEST_PATHS, self.root, self.yq_env(["usage/", "missing-dir/"]))
        message = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, message)
        self.assertIn("Missing directory (minimal): missing-dir/", message)

    def test_missing_manifest_file_fails_and_present_paths_pass(self):
        missing = shell(MANIFEST_PATHS, self.root, self.yq_env(["absent.yml"]))
        message = missing.stdout + missing.stderr
        self.assertNotEqual(missing.returncode, 0, message)
        self.assertIn("Missing path (minimal): absent.yml", message)
        self.write("usage/keep.md", "ok\n")
        self.write("README.md", "hub\n")
        present = shell(MANIFEST_PATHS, self.root, self.yq_env(["usage/", "README.md"]))
        self.assertEqual(present.returncode, 0, present.stdout + present.stderr)

    def test_manifest_paths_fail_closed_when_yq_fails(self):
        result = shell(MANIFEST_PATHS, self.root, self.yq_env([], fail=True))
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_real_yq_reads_the_manifest_and_rejects_a_planted_gap(self):
        binary, env, version = pinned_yq()
        identity = subprocess.run([str(binary), "--version"], capture_output=True, text=True, timeout=15)
        self.assertEqual(identity.returncode, 0, identity.stderr)
        self.assertIn(version, identity.stdout + identity.stderr)
        present = shell(MANIFEST_PATHS, ROOT, env)
        self.assertEqual(present.returncode, 0, present.stdout + present.stderr)
        linked = shell(CROSS_REF, ROOT, env)
        self.assertEqual(linked.returncode, 0, linked.stdout + linked.stderr)
        self.write("kit-manifest.yml", (ROOT / "kit-manifest.yml").read_text())
        self.write("usage/QUICKGUIDE.md", "See [other](../NOT_IN_BUNDLE.md).\n")
        self.write("NOT_IN_BUNDLE.md", "exists\n")
        rejected = shell(MANIFEST_PATHS, self.root, env)
        message = rejected.stdout + rejected.stderr
        listed = subprocess.run(
            [str(binary), "-r", ".bundles.minimal.paths[]", str(self.root / "kit-manifest.yml")],
            capture_output=True, text=True, timeout=15, check=False,
        )
        self.assertEqual(listed.returncode, 0, listed.stderr)
        missing = next(
            path for path in listed.stdout.splitlines()
            if path and not (self.root / path.rstrip("/")).exists()
        )
        kind = "directory" if missing.endswith("/") else "path"
        self.assertNotEqual(rejected.returncode, 0, message)
        self.assertIn(f"Missing {kind} (minimal): {missing}", message)
        outside = shell(CROSS_REF, self.root, env)
        outside_message = outside.stdout + outside.stderr
        self.assertNotEqual(outside.returncode, 0, outside_message)
        self.assertIn("references NOT_IN_BUNDLE.md", outside_message)

    def test_lychee_rejects_a_missing_local_hub_link(self):
        binary, flags, hubs, version = pinned_lychee()
        identity = subprocess.run([str(binary), "--version"], capture_output=True, text=True, timeout=15)
        self.assertEqual(identity.returncode, 0, identity.stderr)
        self.assertIn(version.lstrip("v"), identity.stdout + identity.stderr)
        self.write("README.md", "See [gone](./missing.md) and <mailto:a@example.invalid>.\n")
        broken = subprocess.run(
            [str(binary), *flags, "--offline", "./README.md"],
            cwd=self.root, capture_output=True, text=True, timeout=30,
        )
        message = broken.stdout + broken.stderr
        self.assertNotEqual(broken.returncode, 0, message)
        self.assertIn("File not found", message)
        self.assertNotIn("mailto:", message)
        self.write("present.md", "here\n")
        self.write("README.md", "See [here](./present.md).\n")
        good = subprocess.run(
            [str(binary), *flags, "--offline", "./README.md"],
            cwd=self.root, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
        hubs_result = subprocess.run(
            [str(binary), *flags, "--offline", *hubs],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(hubs_result.returncode, 0, hubs_result.stdout + hubs_result.stderr)

    def _coupling_repo(self):
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Gate fixture")
        self.git("config", "user.email", "gate-fixture@example.invalid")
        self.write("constitution/RULES.md", "Original rule\n")
        self.write("ci/claim_cards.json", "{\"schema_version\": 1}\n")
        self.write("README.md", "hub\n")
        return self.commit()

    def _coupling(self, base, head):
        env = os.environ.copy()
        env.update(BASE_SHA=base, HEAD_SHA=head)
        return shell(COUPLING, self.root, env)

    def test_constitution_edit_without_registry_fails(self):
        base = self._coupling_repo()
        self.write("constitution/RULES.md", "Changed thesis\n")
        head = self.commit()
        failed = self._coupling(base, head)
        message = failed.stdout + failed.stderr
        self.assertNotEqual(failed.returncode, 0, message)
        self.assertIn("without an added or modified ci/claim_cards.json", message)
        self.git("rm", "-q", "ci/claim_cards.json")
        deleted = self.commit()
        absent = self._coupling(base, deleted)
        absent_message = absent.stdout + absent.stderr
        self.assertNotEqual(absent.returncode, 0, absent_message)
        self.assertIn("absent at HEAD", absent_message)

    def test_constitution_edit_with_registry_passes(self):
        base = self._coupling_repo()
        self.write("constitution/RULES.md", "Changed thesis\n")
        self.write("ci/claim_cards.json", "{\"schema_version\": 1, \"cards\": []}\n")
        paired = self._coupling(base, self.commit())
        self.assertEqual(paired.returncode, 0, paired.stdout + paired.stderr)
        self.assertIn("coupling ok", paired.stdout)
        self.git("reset", "--hard", base)
        self.write("README.md", "unrelated\n")
        unrelated = self._coupling(base, self.commit())
        self.assertEqual(unrelated.returncode, 0, unrelated.stdout + unrelated.stderr)

    def test_cross_ref_fails_closed_without_yq(self):
        self.write("usage/QUICKGUIDE.md", "See [plan](AEP_VALIDATION.md).\n")
        self.write("usage/AEP_VALIDATION.md", "body\n")
        env = os.environ.copy()
        env["PATH"] = "/usr/bin:/bin"
        result = shell(CROSS_REF, self.root, env)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
