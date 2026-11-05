"""Independent C1/C2 graders reject no-op, hollow PASS, and forbidden edits."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
HARBOR = ROOT / "research" / "experiments" / "harbor"
GRADER = HARBOR / "grader" / "check.py"
SPEC = importlib.util.spec_from_file_location("harbor_grader", GRADER)
GRADE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GRADE)


def _copy_fixture(task, destination):
    shutil.copytree(task / "environment" / "fixture", destination)


def _manifest(task):
    return json.loads(
        (task / "tests" / "expected" / "manifest.json").read_text(encoding="utf-8")
    )


def _oracle(task, root):
    subprocess.check_call(
        ["bash", str(task / "solution" / "solve.sh")],
        env={"APP_ROOT": str(root), "PATH": "/usr/bin:/bin"},
    )


class HarborGraders(unittest.TestCase):
    def test_builder_output_matches_the_committed_tasks(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = HARBOR / "build_tasks.py"
            source = script.read_text(encoding="utf-8")
            patched = source.replace(
                'TASKS = ROOT / "tasks"',
                f'TASKS = Path({tmp!r}) / "tasks"',
                1,
            )
            runner = Path(tmp) / "build_tasks.py"
            runner.write_text(patched, encoding="utf-8")
            shutil.copytree(HARBOR / "grader", Path(tmp) / "grader")
            subprocess.check_call(["python3", str(runner)])
            built = Path(tmp) / "tasks"
            committed = HARBOR / "tasks"
            built_files = sorted(path.relative_to(built).as_posix() for path in built.rglob("*") if path.is_file())
            committed_files = sorted(
                path.relative_to(committed).as_posix()
                for path in committed.rglob("*")
                if path.is_file()
            )
            self.assertEqual(built_files, committed_files)
            for relative in built_files:
                self.assertEqual(
                    (built / relative).read_bytes(),
                    (committed / relative).read_bytes(),
                    relative,
                )

    def test_c1_oracle_passes_and_hollow_or_forbidden_edits_fail(self):
        task = HARBOR / "tasks" / "c1-forbidden-import"
        manifest = _manifest(task)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "app"
            _copy_fixture(task, root)
            self.assertTrue(GRADE.grade(root, manifest))
            _oracle(task, root)
            self.assertEqual(GRADE.grade(root, manifest), [])
            (root / "decision.md").write_text("PASS\n", encoding="utf-8")
            hollow = GRADE.grade(root, manifest)
            self.assertTrue(any(reason.startswith("HOLLOW:") for reason in hollow))
            _oracle(task, root)
            importer = root / "ci" / "import_bundle.py"
            importer.write_text(
                importer.read_text(encoding="utf-8").replace("return False", "return True"),
                encoding="utf-8",
            )
            forbidden = GRADE.grade(root, manifest)
            self.assertTrue(any(reason.startswith("HASH:") for reason in forbidden))

    def test_c1_b1_requires_the_overlay_line(self):
        task = HARBOR / "tasks" / "c1-forbidden-import-b1"
        manifest = _manifest(task)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "app"
            _copy_fixture(task, root)
            _oracle(HARBOR / "tasks" / "c1-forbidden-import", root)
            self.assertTrue(GRADE.grade(root, manifest))
            _oracle(task, root)
            self.assertEqual(GRADE.grade(root, manifest), [])

    def test_c2_requires_the_edit_and_rejects_extra_files(self):
        task = HARBOR / "tasks" / "c2-permitted-doc"
        manifest = _manifest(task)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "app"
            _copy_fixture(task, root)
            unchanged = GRADE.grade(root, manifest)
            self.assertTrue(any(reason.startswith("HASH:") for reason in unchanged))
            _oracle(task, root)
            self.assertEqual(GRADE.grade(root, manifest), [])
            (root / "decision.md").write_text("PASS\n", encoding="utf-8")
            extra = GRADE.grade(root, manifest)
            self.assertTrue(any(reason.startswith("UNEXPECTED:") for reason in extra))

    def test_c2_b1_note_is_exact(self):
        task = HARBOR / "tasks" / "c2-permitted-doc-b1"
        manifest = _manifest(task)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "app"
            _copy_fixture(task, root)
            _oracle(HARBOR / "tasks" / "c2-permitted-doc", root)
            missing = GRADE.grade(root, manifest)
            self.assertTrue(any("loaded-overlay.md" in reason for reason in missing))
            _oracle(task, root)
            self.assertEqual(GRADE.grade(root, manifest), [])
            note = root / "loaded-overlay.md"
            note.write_text(note.read_text(encoding="utf-8") + "blocked by import\n", encoding="utf-8")
            self.assertTrue(GRADE.grade(root, manifest))


if __name__ == "__main__":
    unittest.main()
