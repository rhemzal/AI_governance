"""Import-boundary regressions: disposable Git sources and adopter repositories."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "ci/import_bundle.py"
spec = importlib.util.spec_from_file_location("import_bundle", TOOL)
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, text=True, timeout=15).stdout


class ImportSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "kit"
        self.source.mkdir()
        git(self.source, "init", "-q")
        self.manifest = {
            "exclude": ["notes/local/**", ".git/"],
            "bundles": {
                "minimal": {"paths": ["AGENTS.md", "constitution/"]},
                "standard": {"extends": "minimal", "paths": ["CHANGELOG.md", "ci/"]},
                "architecture": {"paths": ["architecture/"]},
                "research": {"paths": ["research/"]},
                "full": {"composes": ["standard", "architecture", "research"], "paths": ["notes/"]},
            },
        }
        for name in ["AGENTS.md", "constitution/rules.md", "CHANGELOG.md", "ci/gate.py",
                     "architecture/framework.md", "research/context.md", "notes/README.md",
                     "notes/local/private.md"]:
            self.write(name, "KIT: " + name + "\n")
        git(self.source, "add", ".")
        # Untracked files must not enter a snapshot through directory expansion.
        self.write("constitution/untracked.md", "not part of pinned inventory")
        self.project = self.root / "product"
        self.project.mkdir()
        self.destination = self.project / "vendor/AI_governance"
        self.manifest_file = self.root / "manifest.json"

    def write(self, name, text):
        path = self.source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def cli(self, *args, selections=("standard",)):
        self.manifest_file.write_text(json.dumps(self.manifest))
        command = [sys.executable, str(TOOL), "--manifest-json", str(self.manifest_file),
                   "--source", str(self.source), "--destination", str(self.destination)]
        for selected in selections:
            command.extend(["--bundle", selected])
        return subprocess.run(command + list(args), text=True, capture_output=True, timeout=20)

    def test_existing_host_files_survive_namespaced_import(self):
        sentinels = ["AGENTS.md", ".github/copilot-instructions.md", "CHANGELOG.md",
                     "DEVELOPMENT.md", "VERSIONING.md", ".github/workflows/doc-hygiene.yml"]
        for name in sentinels:
            path = self.project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("HOST: " + name)
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in sentinels:
            self.assertEqual((self.project / name).read_text(), "HOST: " + name)
        self.assertEqual(self.cli("--check").returncode, 0)

    def test_existing_empty_destination_is_refused(self):
        self.destination.mkdir(parents=True)
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Refusing existing destination", result.stderr)
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_exclude_drops_governance_local_overlay_from_snapshot(self):
        self.manifest["exclude"].append("governance/LOCAL_OVERLAY.md")
        self.manifest["bundles"]["minimal"]["paths"].append("governance/")
        self.write("governance/LOCAL_OVERLAY.md", "HOST OVERLAY\n")
        self.write("governance/LOCAL_OVERLAY_TEMPLATE.md", "TEMPLATE\n")
        git(self.source, "add", "governance")
        files, _ = bundle.snapshot(self.source, self.manifest, ["minimal"])
        self.assertIn("governance/LOCAL_OVERLAY_TEMPLATE.md", files)
        self.assertNotIn("governance/LOCAL_OVERLAY.md", files)

    def test_deleted_snapshot_file_is_not_restored_when_the_previous_revision_has_it(self):
        snap = self.project / "vendor/AI_governance/constitution"
        snap.mkdir(parents=True)
        other = snap / "other.md"
        other.write_text("local other\n")
        other.chmod(0o640)
        new = {
            "constitution/rules.md": (b"new rules\n", 0o755),
            "constitution/other.md": (b"new other\n", 0o755),
        }
        previous = {
            "constitution/rules.md": b"old rules\n",
            "constitution/other.md": b"base other\n",
        }
        merged, report = bundle.merge_readopt(self.project, new, previous)
        self.assertNotIn("constitution/rules.md", merged)
        self.assertIn("kept deletion: constitution/rules.md", report)
        self.assertEqual(merged["constitution/other.md"][0], b"local other\n")
        self.assertEqual(merged["constitution/other.md"][1], 0o640)

    def test_absent_snapshot_file_is_reported_when_the_previous_revision_is_unknown(self):
        snap = self.project / "vendor/AI_governance/constitution"
        snap.mkdir(parents=True)
        (snap / "other.md").write_text("kept body")
        new = {
            "constitution/rules.md": (b"new rules\n", 0o644),
            "constitution/other.md": (b"kept body", 0o644),
        }
        merged, report = bundle.merge_readopt(self.project, new, None)
        self.assertEqual(merged["constitution/rules.md"][0], b"new rules\n")
        self.assertIn("absent from the active snapshot (previous revision unknown): constitution/rules.md", report)

    def test_unknown_previous_revision_is_refused(self):
        names = {"AGENTS.md": (b"kit\n", 0o644)}
        with self.assertRaises(bundle.BundleError):
            bundle._previous_files(self.source, "not-a-sha", names)
        with self.assertRaises(bundle.BundleError):
            bundle._previous_files(self.source, "deadbeef" * 5, names)

    def test_missing_path_in_a_real_previous_commit_is_not_an_unknown_revision(self):
        git(self.source, "-c", "user.email=test@example.com", "-c", "user.name=test",
            "commit", "-q", "-m", "pin")
        revision = git(self.source, "rev-parse", "HEAD").strip()
        found = bundle._previous_files(self.source, revision, {"constitution/rules.md": (b"x", 0o644),
                                                                "not/in/commit.md": (b"x", 0o644)})
        self.assertIn("constitution/rules.md", found)
        self.assertNotIn("not/in/commit.md", found)
        snap = self.project / "vendor/AI_governance"
        snap.mkdir(parents=True)
        (snap / "AGENTS.md").write_text("local agents")
        new = {"not/in/commit.md": (b"brand new\n", 0o644), "AGENTS.md": (b"kit agents\n", 0o644)}
        merged, report = bundle.merge_readopt(self.project, new, found)
        self.assertEqual(merged["not/in/commit.md"][0], b"brand new\n")
        self.assertIn("not in previous revision", report)
        self.assertNotIn("previous revision unknown", report)

    def test_conflict_report_keeps_the_upstream_text(self):
        snap = self.project / "vendor/AI_governance"
        snap.mkdir(parents=True)
        adopted = snap / "AGENTS.md"
        adopted.write_text("local agents\n")
        adopted.chmod(0o644)
        new = {"AGENTS.md": (b"upstream agents\n", 0o755)}
        merged, report = bundle.merge_readopt(self.project, new, {"AGENTS.md": b"base agents\n"})
        self.assertEqual(merged["AGENTS.md"], (b"local agents\n", 0o644))
        self.assertIn("local agents", report)
        self.assertIn("upstream agents", report)

    def test_root_layout_lists_a_file_outside_the_selection(self):
        rules = self.project / "constitution"
        rules.mkdir()
        (rules / "AI_RULES.md").write_text("OLD ROOT KIT")
        (rules / "rules.md").write_text("local rules")
        (rules / "LOCAL_ONLY.md").write_text("project only\n")
        (self.project / "AGENTS.md").write_text("HOST")
        self.destination = self.project
        result = self.cli("--readopt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((rules / "rules.md").read_text(), "local rules")
        self.assertEqual((rules / "AI_RULES.md").read_text(), "OLD ROOT KIT")
        staged = self.project / "vendor/AI_governance/constitution/rules.md"
        self.assertEqual(staged.read_text(), "local rules")
        report = (self.project / "vendor/AI_governance.readopt-report.md").read_text(encoding="utf-8")
        self.assertIn("constitution/LOCAL_ONLY.md", report)
        self.assertIn("upstream", report)

    def test_root_layout_absence_takes_upstream_instead_of_a_deletion(self):
        rules = self.project / "constitution"
        rules.mkdir()
        (rules / "AI_RULES.md").write_text("OLD")
        new = {
            "constitution/rules.md": (b"new rules\n", 0o644),
            "constitution/other.md": (b"other\n", 0o644),
        }
        previous = {
            "constitution/rules.md": b"old rules\n",
            "constitution/other.md": b"old other\n",
        }
        merged, report = bundle.merge_readopt(self.project, new, previous)
        self.assertEqual(merged["constitution/rules.md"][0], b"new rules\n")
        self.assertIn("not in the root layout, took upstream: constitution/rules.md", report)
        self.assertNotIn("kept deletion", report)

    def test_readopt_rejects_an_unknown_previous_sha(self):
        self.destination = self.project
        result = self.cli("--readopt", "--previous", "deadbeef" * 5)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("not a commit", result.stderr)
        self.assertFalse((self.project / "vendor").exists())

    def test_readopt_check_is_refused(self):
        self.destination = self.project
        result = self.cli("--readopt", "--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not support --check", result.stderr)
        self.assertFalse((self.project / "vendor").exists())

    def test_symlink_in_the_active_snapshot_is_refused(self):
        snap = self.project / "vendor/AI_governance"
        snap.mkdir(parents=True)
        outside = self.project / "outside.txt"
        outside.write_text("secret")
        (snap / "AGENTS.md").symlink_to(outside)
        with self.assertRaises(bundle.BundleError) as caught:
            bundle.merge_readopt(self.project, {"AGENTS.md": (b"kit\n", 0o644)}, {})
        self.assertIn("Symlink", str(caught.exception))

    def test_symlink_snapshot_directory_is_refused(self):
        real = self.project / "real-rules"
        real.mkdir()
        (real / "AGENTS.md").write_text("elsewhere")
        link = self.project / "vendor/AI_governance"
        link.parent.mkdir()
        link.symlink_to(real, target_is_directory=True)
        self.destination = self.project
        result = self.cli("--readopt")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Symlink", result.stderr)
        self.assertFalse((self.project / "vendor/AI_governance.next").exists())
        self.assertEqual((real / "AGENTS.md").read_text(), "elsewhere")

    def test_orphan_staged_snapshot_without_an_active_tree_is_refused(self):
        staged = self.project / "vendor/AI_governance.next"
        staged.mkdir(parents=True)
        (staged / "AGENTS.md").write_text("stale")
        self.destination = self.project
        result = self.cli("--readopt")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("orphan staged snapshot", result.stderr)
        self.assertFalse((self.project / "vendor/AI_governance").exists())

    def test_existing_readopt_report_is_refused_before_writing(self):
        self.assertEqual(self.cli().returncode, 0)
        report = self.project / "vendor/AI_governance.readopt-report.md"
        report.write_text("stale report\n", encoding="utf-8")
        self.destination = self.project
        result = self.cli("--readopt")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Refusing existing re-adoption report", result.stderr)
        self.assertFalse((self.project / "vendor/AI_governance.next").exists())

    def test_symlink_root_constitution_is_refused(self):
        outside = self.project / "outside-rules"
        outside.mkdir()
        (outside / "AI_RULES.md").write_text("SECRET RULE")
        (outside / "rules.md").write_text("secret rules")
        (self.project / "constitution").symlink_to(outside, target_is_directory=True)
        self.destination = self.project
        result = self.cli("--readopt")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Symlink", result.stderr)
        self.assertFalse((self.project / "vendor").exists())
        self.assertEqual((outside / "rules.md").read_text(), "secret rules")

    def test_failed_readopt_removes_only_the_new_snapshot(self):
        self.assertEqual(self.cli().returncode, 0)
        active = self.project / "vendor/AI_governance/AGENTS.md"
        active.write_text("LOCAL SNAPSHOT EDIT")
        self.destination = self.project

        def fail_after_create(source, destination, files, excludes):
            destination.mkdir()
            (destination / "partial.md").write_text("partial")
            raise OSError("disk full")

        original = bundle.import_copy
        bundle.import_copy = fail_after_create
        self.manifest_file.write_text(json.dumps(self.manifest))
        try:
            code = bundle.main([
                "--manifest-json", str(self.manifest_file),
                "--source", str(self.source),
                "--destination", str(self.project),
                "--bundle", "standard",
                "--readopt",
            ])
        finally:
            bundle.import_copy = original
        self.assertEqual(code, 1)
        self.assertEqual(active.read_text(), "LOCAL SNAPSHOT EDIT")
        self.assertFalse((self.project / "vendor/AI_governance.next").exists())

    def test_failed_root_readopt_retries_against_the_root_rules(self):
        rules = self.project / "constitution"
        rules.mkdir()
        (rules / "AI_RULES.md").write_text("OLD ROOT")
        (rules / "rules.md").write_text("local rules")
        git(self.source, "-c", "user.email=test@example.com", "-c", "user.name=test",
            "commit", "-q", "-m", "pin")
        revision = git(self.source, "rev-parse", "HEAD").strip()
        self.destination = self.project

        def fail_after_create(source, destination, files, excludes):
            destination.mkdir(parents=True)
            raise OSError("disk full")

        original = bundle.import_copy
        bundle.import_copy = fail_after_create
        self.manifest_file.write_text(json.dumps(self.manifest))
        try:
            code = bundle.main([
                "--manifest-json", str(self.manifest_file),
                "--source", str(self.source),
                "--destination", str(self.project),
                "--bundle", "standard",
                "--readopt",
                "--previous", revision,
            ])
        finally:
            bundle.import_copy = original
        self.assertEqual(code, 1)
        self.assertFalse((self.project / "vendor/AI_governance").exists())
        result = self.cli("--readopt", "--previous", revision)
        self.assertEqual(result.returncode, 0, result.stderr)
        staged = self.project / "vendor/AI_governance/constitution/rules.md"
        self.assertEqual(staged.read_text(), "local rules")
        self.assertEqual((rules / "rules.md").read_text(), "local rules")

    def test_matching_bytes_keep_the_local_mode(self):
        snap = self.project / "vendor/AI_governance"
        snap.mkdir(parents=True)
        adopted = snap / "AGENTS.md"
        adopted.write_text("same\n")
        adopted.chmod(0o755)
        merged, _report = bundle.merge_readopt(
            self.project, {"AGENTS.md": (b"same\n", 0o644)}, None,
        )
        self.assertEqual(merged["AGENTS.md"], (b"same\n", 0o755))

    def test_binary_conflict_points_at_the_kit_source(self):
        snap = self.project / "vendor/AI_governance"
        snap.mkdir(parents=True)
        (snap / "AGENTS.md").write_bytes(b"local \xff\n")
        merged, report = bundle.merge_readopt(
            self.project,
            {"AGENTS.md": (b"upstream \xff\n", 0o644)},
            {"AGENTS.md": b"base\n"},
        )
        self.assertEqual(merged["AGENTS.md"][0], b"local \xff\n")
        self.assertIn("upstream bytes remain in the kit source", report)

    def test_merge_keeps_a_changed_local_rule_and_takes_upstream_when_unedited(self):
        snap = self.project / "vendor/AI_governance/constitution"
        snap.mkdir(parents=True)
        (snap / "rules.md").write_text("local rule")
        (self.project / "vendor/AI_governance/CHANGELOG.md").write_text("KIT: CHANGELOG.md\n")
        new = {
            "constitution/rules.md": (b"new kit rule\n", 0o644),
            "CHANGELOG.md": (b"new changelog\n", 0o644),
        }
        previous = {
            "constitution/rules.md": b"base\n",
            "CHANGELOG.md": b"KIT: CHANGELOG.md\n",
        }
        merged, report = bundle.merge_readopt(self.project, new, previous)
        self.assertEqual(merged["constitution/rules.md"][0], b"local rule")
        self.assertEqual(merged["CHANGELOG.md"][0], b"new changelog\n")
        self.assertIn("kept local rule", report)
        self.assertIn("took upstream: CHANGELOG.md", report)

    def test_readopt_stages_beside_a_previous_snapshot(self):
        (self.project / "AGENTS.md").write_text("HOST")
        root_rules = self.project / "constitution" / "AI_RULES.md"
        root_rules.parent.mkdir()
        root_rules.write_text("OLD ROOT KIT")
        self.assertEqual(self.cli().returncode, 0)
        (self.destination / "AGENTS.md").write_text("LOCAL SNAPSHOT EDIT")
        self.destination = self.project
        result = self.cli("--readopt")
        self.assertEqual(result.returncode, 0, result.stderr)
        staged = self.project / "vendor/AI_governance.next"
        self.assertEqual((self.project / "AGENTS.md").read_text(), "HOST")
        self.assertEqual(root_rules.read_text(), "OLD ROOT KIT")
        self.assertEqual((self.project / "vendor/AI_governance/AGENTS.md").read_text(), "LOCAL SNAPSHOT EDIT")
        self.assertEqual((staged / "AGENTS.md").read_text(), "LOCAL SNAPSHOT EDIT")
        report = (self.project / "vendor" / "AI_governance.readopt-report.md").read_text(encoding="utf-8")
        self.assertIn("kept local rule", report)
        self.destination = staged
        self.assertIn("Refusing existing destination", self.cli().stderr)

    def test_readopt_keeps_root_rules_and_stages_a_snapshot(self):
        root_rules = self.project / "constitution" / "AI_RULES.md"
        root_rules.parent.mkdir()
        root_rules.write_text("OLD ROOT KIT")
        (self.project / "AGENTS.md").write_text("HOST")
        self.destination = self.project
        result = self.cli("--readopt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(root_rules.read_text(), "OLD ROOT KIT")
        self.assertEqual((self.project / "AGENTS.md").read_text(), "HOST")
        staged = self.project / "vendor" / "AI_governance"
        self.assertTrue((staged / "AGENTS.md").read_text().startswith("KIT:"))
        report = (self.project / "vendor" / "AI_governance.readopt-report.md").read_text(encoding="utf-8")
        self.assertIn("constitution/AI_RULES.md", report)
        self.assertIn("host file unchanged: AGENTS.md", report)

    def test_direct_import_into_host_and_repeated_import_are_refused(self):
        self.destination = self.project
        (self.project / "AGENTS.md").write_text("KEEP HOST RULES")
        self.assertEqual(self.cli().returncode, 1)
        self.assertEqual((self.project / "AGENTS.md").read_text(), "KEEP HOST RULES")
        self.destination = self.project / "vendor/AI_governance"
        self.assertEqual(self.cli().returncode, 0)
        (self.destination / "AGENTS.md").write_text("reviewed local modification")
        self.assertEqual(self.cli().returncode, 1)
        self.assertEqual((self.destination / "AGENTS.md").read_text(), "reviewed local modification")

    def test_missing_source_file_fails_before_any_destination_write(self):
        (self.source / "constitution/rules.md").unlink()
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.destination.parent.exists())

    def test_unknown_and_cyclic_selections_fail_before_writes(self):
        self.assertEqual(self.cli(selections=("standard", "unknown")).returncode, 1)
        self.manifest["bundles"]["minimal"]["extends"] = "standard"
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn("cycle", result.stderr)
        self.assertFalse(self.destination.exists())

    def test_ambiguous_baselines_are_rejected(self):
        for selections in [("architecture",), ("minimal", "standard"), ("full", "research")]:
            with self.subTest(selections=selections):
                self.assertEqual(self.cli(selections=selections).returncode, 1)
        self.assertFalse(self.destination.exists())

    def test_traversal_and_absolute_manifest_paths_are_rejected(self):
        for bad in ["../outside.md", "/tmp/outside.md", "C:/outside.md", "dir/../../outside", "dir\\file"]:
            with self.subTest(path=bad):
                self.manifest["bundles"]["standard"]["paths"] = [bad]
                self.assertEqual(self.cli().returncode, 1)
        self.assertFalse(self.destination.exists())

    def test_destination_symlink_and_symlink_parent_are_refused(self):
        outside = self.root / "outside"
        outside.mkdir()
        self.destination.parent.mkdir()
        self.destination.symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.cli().returncode, 1)
        self.destination.unlink()
        self.destination.parent.rmdir()
        self.destination.parent.symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.cli().returncode, 1)
        self.assertEqual(list(outside.iterdir()), [])

    def test_source_symlink_is_refused(self):
        path = self.source / "constitution/rules.md"
        path.unlink()
        path.symlink_to(self.source / "AGENTS.md")
        self.assertEqual(self.cli().returncode, 1)
        self.assertFalse(self.destination.exists())

    def test_exclusions_and_untracked_files_are_not_copied(self):
        self.assertEqual(self.cli(selections=("full",)).returncode, 0)
        self.assertFalse((self.destination / "notes/local/private.md").exists())
        self.assertFalse((self.destination / "constitution/untracked.md").exists())
        self.assertEqual(self.cli("--check", selections=("full",)).returncode, 0)

    def test_missing_changed_extra_and_symlink_target_fail_read_only_verification(self):
        self.assertEqual(self.cli().returncode, 0)
        path = self.destination / "AGENTS.md"
        original = path.read_bytes()
        path.unlink()
        self.assertEqual(self.cli("--check").returncode, 1)
        self.assertFalse(path.exists())
        path.write_text("modified")
        self.assertEqual(self.cli("--check").returncode, 1)
        self.assertEqual(path.read_text(), "modified")
        path.write_bytes(original)
        extra = self.destination / "extra.md"
        extra.write_text("extra")
        self.assertEqual(self.cli("--check").returncode, 1)
        extra.unlink()
        path.unlink()
        path.symlink_to(self.source / "AGENTS.md")
        self.assertEqual(self.cli("--check").returncode, 1)
        self.assertTrue(path.is_symlink())

    def test_filenames_with_spaces_and_executable_mode_survive(self):
        self.write("constitution/space name.md", "with spaces")
        gate = self.source / "ci/gate.py"
        gate.chmod(0o755)
        git(self.source, "add", "constitution/space name.md", "ci/gate.py")
        self.assertEqual(self.cli().returncode, 0)
        self.assertEqual((self.destination / "constitution/space name.md").read_text(), "with spaces")
        self.assertTrue((self.destination / "ci/gate.py").stat().st_mode & 0o111)
        self.assertEqual(self.cli("--check").returncode, 0)
        (self.destination / "ci/gate.py").chmod(0o644)
        result = self.cli("--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("executable bit", result.stderr)


class RealManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest_path = os.environ.get("KIT_MANIFEST_JSON")
        if not manifest_path:
            raise RuntimeError("Set KIT_MANIFEST_JSON to the yq JSON conversion of kit-manifest.yml")
        cls.manifest = json.loads(Path(manifest_path).read_text())

    def test_all_supported_selections_are_complete_and_preserve_existing_host(self):
        selections = [("minimal",), ("standard",), ("minimal", "architecture"),
                      ("minimal", "research"), ("standard", "architecture"),
                      ("standard", "research"), ("standard", "architecture", "research"), ("full",)]
        for selected in selections:
            with self.subTest(selected=selected), tempfile.TemporaryDirectory() as temp:
                project = Path(temp)
                for name in ["AGENTS.md", ".github/copilot-instructions.md", "CHANGELOG.md", "DEVELOPMENT.md", "VERSIONING.md"]:
                    path = project / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("HOST: " + name)
                files, excludes = bundle.snapshot(REPO, self.manifest, selected)
                destination = project / "vendor/AI_governance"
                bundle.import_copy(REPO, destination, files, excludes)
                bundle.verify_copy(destination, files, excludes)
                for name in ["AGENTS.md", ".github/copilot-instructions.md", "CHANGELOG.md", "DEVELOPMENT.md", "VERSIONING.md"]:
                    self.assertEqual((project / name).read_text(), "HOST: " + name)
                for required in ["kit-manifest.yml", "architecture/ARCHITECTURE_DECISION_FRAMEWORK.md", "architecture/TERMINOLOGY_GLOSSARY.md",
                                 "usage/AI_ENGINEERING_METHODS.md", "usage/ENGINEERING_METHODS_ADOPTION.md"]:
                    self.assertIn(required, files)
                if "architecture" not in selected and "full" not in selected:
                    self.assertNotIn("architecture/README.md", files)
                if selected[0] == "minimal":
                    self.assertNotIn("ci/ratchet_findings.py", files)
                    self.assertNotIn("usage/AGENT_EVALUATION.md", files)
                else:
                    self.assertIn("ci/ratchet_findings.py", files)
                missing = destination / "constitution/AI_RULES.md"
                missing.unlink()
                with self.assertRaisesRegex(bundle.BundleError, "missing"):
                    bundle.verify_copy(destination, files, excludes)


if __name__ == "__main__":
    unittest.main()
