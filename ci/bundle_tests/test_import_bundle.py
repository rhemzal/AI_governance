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
                for required in ["kit-manifest.yml", "architecture/ARCHITECTURE_DECISION_FRAMEWORK.md", "architecture/TERMINOLOGY_GLOSSARY.md"]:
                    self.assertIn(required, files)
                if "architecture" not in selected and "full" not in selected:
                    self.assertNotIn("architecture/README.md", files)
                missing = destination / "constitution/AI_RULES.md"
                missing.unlink()
                with self.assertRaisesRegex(bundle.BundleError, "missing"):
                    bundle.verify_copy(destination, files, excludes)


if __name__ == "__main__":
    unittest.main()
