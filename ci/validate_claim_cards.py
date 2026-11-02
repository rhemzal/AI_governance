#!/usr/bin/env python3
"""Validate claim-card shape and promotion. Do not execute scenarios or grade truth.

Provenance: AI_governance (https://github.com/rhemzal/AI_governance), MIT.
Human rules: usage/AGENT_EVALUATION.md. Decision: adr/ADR_0014_Claim_Card_Registry.md.
The constitution blind spot is card unregistered-constitution-sentence.
"""

import argparse
import ast
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path, PurePosixPath


class ClaimError(ValueError):
    """The registry is malformed or breaks its promotion rule."""


CARD_FIELDS = (
    "id",
    "statement",
    "source",
    "layer",
    "oracle",
    "status",
    "positive",
    "negative",
    "known_pass_that_is_not_proof",
    "path",
    "anchor",
    "rerun_when",
)
LAYERS = ("research", "advisory", "normative")
ORACLES = ("canary", "declaration", "scenario", "none")
STATUSES = ("open", "probed", "integrated")
PLACEHOLDERS = {"tbd", "todo", "later", "as needed", "etc", "n/a", "none", "...", "-"}


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ClaimError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_registry(text):
    try:
        return json.loads(text, object_pairs_hook=_object)
    except json.JSONDecodeError as exc:
        raise ClaimError(f"registry is not JSON: {exc}") from exc


def _bare(value, label):
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ClaimError(f"{label}: expected non-empty text without surrounding space")
    if value.casefold().rstrip(".") in PLACEHOLDERS:
        raise ClaimError(f"{label}: unresolved text")


def _text(value, label):
    _bare(value, label)
    if len(value) < 16:
        raise ClaimError(f"{label}: unresolved or too-short text")


def _fields(value, names, label):
    if not isinstance(value, dict):
        raise ClaimError(f"{label}: expected an object")
    missing = set(names) - value.keys()
    extra = value.keys() - set(names)
    if missing or extra:
        raise ClaimError(f"{label}: missing={sorted(missing)}, unknown={sorted(extra)}")


def _repo_file(value, label, root):
    _bare(value, label)
    if "\\" in value or value.startswith("/"):
        raise ClaimError(f"{label}: use a repository-relative POSIX path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ClaimError(f"{label}: use a repository-relative POSIX path")
    candidate = root.joinpath(*path.parts).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ClaimError(f"{label}: path escapes the repository") from exc
    if not candidate.is_file():
        raise ClaimError(f"{label}: expected a file")
    return candidate


def _defined_test(body, anchor, name):
    if not re.fullmatch(r"def test_[A-Za-z0-9_]+", anchor):
        raise ClaimError(f"{name}: integrated anchor must be a def test_ name")
    pattern = re.compile(re.escape(anchor) + r"\(.*\):\s*(?:#.*)?\Z")
    if not any(pattern.fullmatch(line.strip()) for line in body.splitlines()):
        raise ClaimError(f"{name}: anchor is not a test definition line")
    return anchor.removeprefix("def ")


def _body_asserts(path, test_name):
    """Return whether the test asserts, and whether that assertion reads a runtime value.

    A name assigned once from a literal in the same straight-line block is still a literal.
    Names loaded from calls, attributes, or branches are runtime. The test is not executed.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == test_name:
            return _scan_stmts(node.body, {})
    return False, False


def _scan_stmts(stmts, consts):
    has_assert = False
    observes = False
    for stmt in stmts:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        found, saw_runtime = _scan_stmt(stmt, consts)
        has_assert = has_assert or found
        observes = observes or saw_runtime
    return has_assert, observes


def _scan_stmt(stmt, consts):
    if isinstance(stmt, ast.Assign):
        _bind(stmt.targets, stmt.value, consts)
        return False, False
    if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
        _mark(stmt.target.id, stmt.value is not None and _constant(stmt.value, consts), consts)
        return False, False
    if isinstance(stmt, ast.AugAssign) and isinstance(stmt.target, ast.Name):
        _mark(stmt.target.id, False, consts)
        return False, False
    if isinstance(stmt, ast.Assert):
        return True, not _constant(stmt.test, consts)
    if isinstance(stmt, ast.Expr) and _is_assert_call(stmt.value):
        return True, _call_observes(stmt.value, consts)
    if isinstance(stmt, ast.With):
        for item in stmt.items:
            if item.optional_vars is not None:
                _bind([item.optional_vars], None, consts)
        return _scan_stmts(stmt.body, consts)
    if isinstance(stmt, ast.If):
        return _scan_copies((stmt.body, stmt.orelse), consts)
    if isinstance(stmt, ast.For):
        _bind([stmt.target], None, consts)
        return _scan_copies((stmt.body, stmt.orelse), consts)
    if isinstance(stmt, ast.While):
        return _scan_copies((stmt.body, stmt.orelse), consts)
    if isinstance(stmt, ast.Try):
        parts = [stmt.body, stmt.orelse, stmt.finalbody]
        parts.extend(handler.body for handler in stmt.handlers)
        return _scan_copies(parts, consts)
    return False, False


def _scan_copies(parts, consts):
    has_assert = False
    observes = False
    for part in parts:
        found, saw_runtime = _scan_stmts(part, dict(consts))
        has_assert = has_assert or found
        observes = observes or saw_runtime
    return has_assert, observes


def _bind(targets, value, consts):
    for target in targets:
        if isinstance(target, ast.Name):
            _mark(target.id, value is not None and _constant(value, consts), consts)
        elif isinstance(target, (ast.Tuple, ast.List)):
            if isinstance(value, (ast.Tuple, ast.List)) and len(target.elts) == len(value.elts):
                for elt, item in zip(target.elts, value.elts):
                    _bind([elt], item, consts)
            else:
                for elt in target.elts:
                    _bind([elt], None, consts)


def _mark(name, is_const, consts):
    if is_const:
        consts[name] = True
    else:
        consts.pop(name, None)


def _is_assert_call(node):
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr.startswith("assert")
    )


def _constant(node, consts):
    if node is None:
        return False
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, ast.Name):
        return consts.get(node.id) is True
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.Not, ast.UAdd, ast.USub)):
        return _constant(node.operand, consts)
    if isinstance(node, ast.BinOp):
        return _constant(node.left, consts) and _constant(node.right, consts)
    if isinstance(node, ast.BoolOp):
        return all(_constant(item, consts) for item in node.values)
    if isinstance(node, ast.Compare):
        return _constant(node.left, consts) and all(_constant(item, consts) for item in node.comparators)
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return all(_constant(item, consts) for item in node.elts)
    if isinstance(node, ast.Dict):
        pairs = zip(node.keys, node.values)
        return all(key is not None and _constant(key, consts) and _constant(value, consts)
                   for key, value in pairs)
    return False


def _call_observes(node, consts):
    parts = list(node.args) + [item.value for item in node.keywords]
    return any(not _constant(part, consts) for part in parts)


def _suite_names(suite):
    names = set()
    pending = [suite]
    while pending:
        item = pending.pop()
        if isinstance(item, unittest.TestSuite):
            pending.extend(list(item))
        else:
            method = getattr(item, "_testMethodName", "")
            if method:
                names.add(method)
    return names


def _collected_test_names(path, cache):
    key = str(path.resolve())
    if key in cache:
        return cache[key]
    module_name = "claim_canary_" + re.sub(r"\W", "_", path.stem)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ClaimError(f"{path.name}: cannot load canary module")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise ClaimError(f"{path.name}: canary module failed to import: {exc}") from exc
    cache[key] = _suite_names(unittest.defaultTestLoader.loadTestsFromModule(module))
    return cache[key]


def _promotion(card):
    name = card["id"]
    oracle, layer, status, path = card["oracle"], card["layer"], card["status"], card["path"]
    if oracle == "none" and (layer == "normative" or status != "open"):
        raise ClaimError(f"{name}: oracle none stays research or advisory, and open")
    if status == "integrated":
        if oracle != "canary" or not path.startswith("ci/gate_tests/") or not path.endswith(".py"):
            raise ClaimError(f"{name}: integrated status requires a canary under ci/gate_tests/")
        if not card["anchor"].startswith("def test_"):
            raise ClaimError(f"{name}: integrated anchor must be a def test_ line")
    if layer == "normative" and not (oracle == "canary" and status == "integrated"):
        raise ClaimError(f"{name}: normative claims require an integrated canary")
    if oracle == "scenario" and status not in ("open", "probed"):
        raise ClaimError(f"{name}: a scenario card cannot be integrated")


def validate_registry(document, root):
    """Return the cards. root is the repository root used to resolve source and path."""
    if not isinstance(root, Path):
        root = Path(root)
    if not root.is_dir():
        raise ClaimError("root must be a directory")
    _fields(document, ("schema_version", "cards"), "registry")
    if type(document.get("schema_version")) is not int or document["schema_version"] != 1:
        raise ClaimError("schema_version must be integer 1")
    cards = document["cards"]
    if not isinstance(cards, list) or not cards:
        raise ClaimError("cards: expected a non-empty list")
    seen = set()
    integrated_anchors = set()
    collected = {}
    for index, card in enumerate(cards):
        label = f"cards[{index}]"
        _fields(card, CARD_FIELDS, label)
        name = card["id"]
        if not isinstance(name, str) or not _id_ok(name):
            raise ClaimError(f"{label}.id: expected lowercase hyphenated words")
        if name in seen:
            raise ClaimError(f"duplicate card id: {name}")
        seen.add(name)
        if card["layer"] not in LAYERS:
            raise ClaimError(f"{name}: layer must be research, advisory, or normative")
        if card["oracle"] not in ORACLES:
            raise ClaimError(f"{name}: oracle must be canary, declaration, scenario, or none")
        if card["status"] not in STATUSES:
            raise ClaimError(f"{name}: status must be open, probed, or integrated")
        for field in ("statement", "positive", "negative", "known_pass_that_is_not_proof",
                      "anchor", "rerun_when"):
            _text(card[field], f"{name}.{field}")
        _promotion(card)
        _repo_file(card["source"], f"{name}.source", root)
        evidence = _repo_file(card["path"], f"{name}.path", root)
        try:
            body = evidence.read_text(encoding="utf-8")
        except UnicodeError as exc:
            raise ClaimError(f"{name}.path: evidence file is not UTF-8 text") from exc
        if card["status"] == "integrated":
            if card["anchor"] in integrated_anchors:
                raise ClaimError(f"{name}: duplicate integrated anchor")
            integrated_anchors.add(card["anchor"])
            test_name = _defined_test(body, card["anchor"], name)
            if test_name not in _collected_test_names(evidence, collected):
                raise ClaimError(f"{name}: {test_name} is not collected by unittest")
            has_assert, observes = _body_asserts(evidence, test_name)
            if not has_assert:
                raise ClaimError(f"{name}: {test_name} does not assert anything")
            if not observes:
                raise ClaimError(f"{name}: {test_name} assertions only restate constants")
        elif card["anchor"] not in body:
            raise ClaimError(f"{name}: anchor is not in the evidence file")
    return cards


def _id_ok(value):
    parts = value.split("-")
    return len(parts) >= 2 and all(part.isalnum() and part == part.casefold() and part[:1].isalpha()
                                   for part in parts)


def validate_default(root=None):
    registry = Path(__file__).resolve().parent / "claim_cards.json"
    root = Path(__file__).resolve().parents[1] if root is None else Path(root)
    cards = validate_registry(load_registry(registry.read_text(encoding="utf-8")), root)
    return len(cards)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate ci/claim_cards.json")
    parser.add_argument("--root", type=Path, help="repository root (default: parent of ci/)")
    args = parser.parse_args(argv)
    try:
        count = validate_default(args.root)
    except ClaimError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: {count} claim cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
