"""Shape, promotion, and standing-limit regressions for the claim-card registry."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "validate_claim_cards.py"
SPEC = importlib.util.spec_from_file_location("validate_claim_cards", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

ROOT = Path(__file__).resolve().parents[2]
STANDING = {
    "stop-hook-fail-open": ("research", "scenario", "probed"),
    "native-stop-dispatch-unobserved": ("research", "scenario", "probed"),
    "adr-presence-is-not-rationale": ("advisory", "declaration", "probed"),
    "fabricated-test-evidence": ("advisory", "declaration", "probed"),
    "doc-hygiene-does-not-close-findings": ("advisory", "none", "open"),
    "benchmark-scenarios-unrun": ("advisory", "scenario", "open"),
    "method-rationale-is-unchecked-prose": ("advisory", "declaration", "probed"),
    "doc-delta-section-value": ("advisory", "canary", "integrated"),
    "waiver-section-values": ("advisory", "canary", "integrated"),
    "doc-hygiene-bundle-cross-ref": ("advisory", "canary", "integrated"),
    "doc-hygiene-planted-failures": ("advisory", "canary", "integrated"),
    "provable-enforcement-not-kit-wide": ("research", "none", "open"),
    "ratchet-does-not-run-scanners": ("advisory", "declaration", "probed"),
    "unregistered-constitution-sentence": ("advisory", "none", "open"),
}


def card(**overrides):
    base = {
        "id": "sample-limit",
        "statement": "A sample claim records the check that would falsify it.",
        "source": "notes/source.md",
        "layer": "advisory",
        "oracle": "declaration",
        "status": "open",
        "positive": "The declared good case passes the referenced check.",
        "negative": "The declared bad case fails the referenced check.",
        "known_pass_that_is_not_proof": "A hollow artifact can still satisfy the declared check.",
        "path": "notes/evidence.md",
        "anchor": "sample evidence anchor",
        "rerun_when": "The referenced check or the evidence sentence changes.",
    }
    base.update(overrides)
    return base


class ClaimCardRegistry(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def ready(self, **overrides):
        self.write("notes/source.md", "source file\n")
        self.write("notes/evidence.md", "prefix sample evidence anchor suffix\n")
        return {"schema_version": 1, "cards": [card(**overrides)]}

    def test_open_declaration_and_integrated_canary_pass(self):
        self.assertEqual(1, len(VALIDATOR.validate_registry(self.ready(), self.root)))
        self.write("ci/gate_tests/test_canary.py", (
            "import unittest\n"
            "class Planted(unittest.TestCase):\n"
            "    def test_planted_violation(self):\n"
            "        pass\n"
        ))
        document = self.ready(
            id="planted-canary",
            layer="normative",
            oracle="canary",
            status="integrated",
            path="ci/gate_tests/test_canary.py",
            anchor="def test_planted_violation",
            source="ci/gate_tests/test_canary.py",
        )
        cards = VALIDATOR.validate_registry(document, self.root)
        self.assertEqual("planted-canary", cards[0]["id"])

    def test_missing_extra_placeholder_and_short_fields_fail(self):
        document = self.ready()
        del document["cards"][0]["negative"]
        with self.assertRaises(VALIDATOR.ClaimError):
            VALIDATOR.validate_registry(document, self.root)
        document = self.ready()
        document["cards"][0]["extra"] = "nope"
        with self.assertRaises(VALIDATOR.ClaimError):
            VALIDATOR.validate_registry(document, self.root)
        for value in ("TODO", "later", "n/a", "short text"):
            with self.subTest(value=value):
                with self.assertRaises(VALIDATOR.ClaimError):
                    VALIDATOR.validate_registry(self.ready(statement=value), self.root)

    def test_promotion_without_an_integrated_canary_fails(self):
        cases = [
            {"oracle": "none", "layer": "normative", "status": "open"},
            {"oracle": "none", "status": "probed"},
            {"oracle": "scenario", "status": "integrated", "anchor": "def test_not_a_file"},
            {"oracle": "declaration", "status": "integrated", "anchor": "def test_wrong_oracle"},
            {"layer": "normative", "oracle": "declaration", "status": "probed"},
            {"layer": "normative", "oracle": "canary", "status": "open",
             "path": "ci/gate_tests/test_canary.py", "anchor": "def test_planted_violation"},
        ]
        for overrides in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaises(VALIDATOR.ClaimError):
                    VALIDATOR.validate_registry(self.ready(**overrides), self.root)

    def test_mentioned_or_uncollected_def_is_not_an_integrated_canary(self):
        mentioned = (
            "import unittest\n"
            "class Planted(unittest.TestCase):\n"
            "    def test_real(self):\n"
            "        note = \"def test_planted_violation():\"\n"
            "        # def test_planted_violation():\n"
        )
        bare = "def test_planted_violation():\n    pass\n"
        for text in (mentioned, bare):
            with self.subTest(text=text.splitlines()[0]):
                self.write("ci/gate_tests/test_canary.py", text)
                document = self.ready(
                    id="planted-canary",
                    oracle="canary",
                    status="integrated",
                    path="ci/gate_tests/test_canary.py",
                    anchor="def test_planted_violation",
                    source="ci/gate_tests/test_canary.py",
                )
                with self.assertRaises(VALIDATOR.ClaimError):
                    VALIDATOR.validate_registry(document, self.root)

    def test_integrated_canary_outside_gate_tests_fails(self):
        self.write("ci/test_canary.py", "def test_planted_violation():\n    pass\n")
        document = self.ready(
            oracle="canary",
            status="integrated",
            path="ci/test_canary.py",
            anchor="def test_planted_violation",
        )
        with self.assertRaises(VALIDATOR.ClaimError):
            VALIDATOR.validate_registry(document, self.root)

    def test_duplicate_id_unknown_enum_escape_and_missing_anchor_fail(self):
        document = self.ready()
        document["cards"].append(card())
        self.write("notes/source.md", "source file\n")
        self.write("notes/evidence.md", "prefix sample evidence anchor suffix\n")
        with self.assertRaises(VALIDATOR.ClaimError):
            VALIDATOR.validate_registry(document, self.root)
        with self.assertRaises(VALIDATOR.ClaimError):
            VALIDATOR.validate_registry(self.ready(oracle="benchmark"), self.root)
        with self.assertRaises(VALIDATOR.ClaimError):
            VALIDATOR.validate_registry(self.ready(path="../secret.md"), self.root)
        with self.assertRaises(VALIDATOR.ClaimError):
            VALIDATOR.validate_registry(self.ready(anchor="missing evidence anchor"), self.root)

    def test_duplicate_json_key_fails(self):
        text = '{"schema_version": 1, "schema_version": 1, "cards": []}'
        with self.assertRaises(VALIDATOR.ClaimError):
            VALIDATOR.load_registry(text)

    def test_live_registry_keeps_recorded_limits(self):
        cards = VALIDATOR.validate_registry(
            VALIDATOR.load_registry((ROOT / "ci/claim_cards.json").read_text(encoding="utf-8")),
            ROOT,
        )
        actual = {item["id"]: (item["layer"], item["oracle"], item["status"]) for item in cards}
        self.assertEqual(STANDING, actual)
        self.assertTrue(all(item["layer"] != "normative" for item in cards))

    def test_cli_accepts_the_repo_registry(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn(f"PASS: {len(STANDING)} claim cards", completed.stdout)
