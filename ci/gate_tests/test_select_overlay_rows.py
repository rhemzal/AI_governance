"""Unit tests for ci/select_overlay_rows.py."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "select_overlay_rows.py"
SPEC = importlib.util.spec_from_file_location("select_overlay_rows", SCRIPT)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

FIXTURE_OVERLAY = """# LOCAL GOVERNANCE OVERLAY — fixture

| Constraint | Load when |
| --- | --- |
| A first import refuses an existing destination, including an empty directory. | The task edits ci/import_bundle.py or the import procedure. |
| A symlink is not a snapshot. Opt-in copy may use cp -aL outside the bundle importer. | The task copies kit files or changes symlink checks. |
"""


class SelectOverlayRows(unittest.TestCase):
    def test_selects_import_row_for_importer_path(self):
        rows = MOD.select_rows(FIXTURE_OVERLAY, ["ci/import_bundle.py"])
        self.assertEqual(len(rows), 1)
        self.assertIn("import", rows[0]["constraint"].lower())

    def test_selects_symlink_row_for_copy_path(self):
        rows = MOD.select_rows(FIXTURE_OVERLAY, ["opt-in/copy/CONTENT.txt"])
        self.assertEqual(len(rows), 1)
        self.assertIn("symlink", rows[0]["constraint"].lower())

    def test_unrelated_path_selects_nothing(self):
        rows = MOD.select_rows(FIXTURE_OVERLAY, ["usage/ADOPTION_SCOPE_AND_HOSTS.md"])
        self.assertEqual(rows, [])

    def test_cli_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            overlay = Path(tmp) / "LOCAL_OVERLAY.md"
            overlay.write_text(FIXTURE_OVERLAY, encoding="utf-8")
            import io
            import contextlib

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = MOD.main(
                    ["--overlay", str(overlay), "--path", "ci/import_bundle.py", "--json"]
                )
            self.assertEqual(code, 0)
            data = json.loads(buf.getvalue())
            self.assertEqual(len(data), 1)


if __name__ == "__main__":
    unittest.main()
