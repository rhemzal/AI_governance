#!/usr/bin/env python3
"""Documentation hygiene checks for the AI governance kit (constraints in checks, not prompts)."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "kit-manifest.yml"
README_PATH = ROOT / "README.md"

PROVENANCE_RE = re.compile(r"(?i)provenance")
RELATED_SECTION_RE = re.compile(r"^##\s+Related Documents\s*$", re.MULTILINE)
MD_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
BACKTICK_MD_RE = re.compile(r"`([^`]+\.md(?:#[^`]+)?)`")

BARE_DORA_RE = re.compile(r"\bDORA\b")
DORA_ALLOWED_RE = re.compile(
    r"DORA\s+metrics|EU\s+DORA|DORA\s*\(EU\)|DORA\s+software|DORA\s+Software",
    re.IGNORECASE,
)

TDF_RE = re.compile(r"\bTDF\b")

IMPORT_TARGET_PREFIXES = (
    "constitution/",
    "ci/",
    "adr/",
    "usage/",
    "architecture/",
    "governance/",
    "research/",
    "interface/",
    "notes/committed/",
)

PROVENANCE_EXEMPT = {
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "LICENSE",
    "LICENSE-CODE",
}

SIGNIFICANT_DOC_PREFIXES = (
    "constitution/",
    "ci/",
    "usage/",
    "architecture/",
    "governance/",
    "interface/",
)

SIGNIFICANT_DOC_EXEMPT_SUFFIXES = (
    "/README.md",
)

SIGNIFICANT_DOC_EXEMPT_NAMES = (
    "usage/AUDIT_PLAYBOOK.md",
    "usage/AUDIT_REPORT.md",
    "usage/FIX_PLAN.md",
)

TERMINOLOGY_GLOSSARY = "architecture/TERMINOLOGY_GLOSSARY.md"

README_REQUIRED_LINKS = (
    "constitution/AI_RULES.md",
    "constitution/AI_ENFORCEMENT_DAILY.md",
    "constitution/AI_ENFORCEMENT.md",
    "usage/HOW_TO_IMPORT.md",
    "usage/QUICKGUIDE.md",
    "kit-manifest.yml",
    "usage/ADOPTION_BUNDLES.md",
    "VERSIONING.md",
    "AGENTS.md",
    ".github/copilot-instructions.md",
    "usage/AEP_VALIDATION.md",
    "usage/CI_MINIMUM_ADOPTION.md",
    "adr/ADR_TEMPLATE.md",
    "architecture/ARCHITECTURE_DECISION_FRAMEWORK.md",
)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def repo_rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_markdown_files() -> list[Path]:
    skip_dirs = {".git", ".github/ISSUE_TEMPLATE"}
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.md")):
        rel = repo_rel(path)
        if any(part.startswith(".") and part not in {".github"} for part in path.parts):
            if ".github" not in path.parts:
                continue
        if "notes/local" in rel.replace("\\", "/"):
            continue
        files.append(path)
    return files


def is_import_target(rel: str) -> bool:
    name = Path(rel).name
    if name in PROVENANCE_EXEMPT:
        return False
    if rel in {"AGENTS.md", ".github/copilot-instructions.md"}:
        return False
    return any(rel.startswith(prefix) for prefix in IMPORT_TARGET_PREFIXES)


def is_significant_doc(rel: str) -> bool:
    if rel in SIGNIFICANT_DOC_EXEMPT_NAMES:
        return False
    if any(rel.endswith(suffix) for suffix in SIGNIFICANT_DOC_EXEMPT_SUFFIXES):
        return False
    if not any(rel.startswith(prefix) for prefix in SIGNIFICANT_DOC_PREFIXES):
        return False
    if rel.startswith("architecture/rag/"):
        return False
    return True


def load_manifest() -> dict:
    try:
        import yaml  # type: ignore
    except ImportError:
        return _load_manifest_fallback()
    data = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("kit-manifest.yml must parse to a mapping")
    return data


def _load_manifest_fallback() -> dict:
    """Minimal parser when PyYAML is unavailable."""
    text = MANIFEST_PATH.read_text(encoding="utf-8")
    bundles: dict[str, dict] = {}
    current: str | None = None
    section: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        bundle_match = re.match(r"^  (\w+):\s*$", line)
        if bundle_match:
            current = bundle_match.group(1)
            bundles[current] = {"paths": []}
            section = None
            continue
        if current is None:
            continue
        if line.strip() == "paths:":
            section = "paths"
            continue
        if line.strip() in {"extends:", "composes:"} or re.match(r"^    (extends|composes):", line):
            key = line.strip().split(":")[0]
            section = key
            bundles[current].setdefault(key, [])
            continue
        if section == "paths" and line.strip().startswith("- "):
            bundles[current]["paths"].append(line.strip()[2:].strip())
        elif section in {"extends", "composes"} and line.strip().startswith("- "):
            bundles[current].setdefault(section, []).append(line.strip()[2:].strip())
        elif re.match(r"^    extends:\s*(\w+)", line):
            bundles[current]["extends"] = re.match(r"^    extends:\s*(\w+)", line).group(1)
        elif line.strip().startswith("purpose:"):
            bundles[current]["purpose"] = line.split(":", 1)[1].strip()
    return {"bundles": bundles}


def resolve_bundle_paths(manifest: dict, bundle_name: str, seen: set[str] | None = None) -> list[str]:
    seen = seen or set()
    if bundle_name in seen:
        return []
    seen.add(bundle_name)
    bundles = manifest.get("bundles", {})
    bundle = bundles.get(bundle_name, {})
    paths: list[str] = []

    for key in ("extends",):
        parent = bundle.get(key)
        if isinstance(parent, str):
            paths.extend(resolve_bundle_paths(manifest, parent, seen))

    composes = bundle.get("composes", [])
    if isinstance(composes, list):
        for child in composes:
            if isinstance(child, str):
                paths.extend(resolve_bundle_paths(manifest, child, seen))

    for item in bundle.get("paths", []):
        if isinstance(item, str):
            paths.append(item)

    deduped: list[str] = []
    for item in paths:
        if item not in deduped:
            deduped.append(item)
    return deduped


def path_exists(rel: str) -> bool:
    target = ROOT / rel
    return target.exists()


def check_manifest_paths(report: Report, manifest: dict) -> None:
    for bundle_name in manifest.get("bundles", {}):
        for rel in resolve_bundle_paths(manifest, bundle_name):
            if not path_exists(rel):
                report.fail(f"kit-manifest.yml [{bundle_name}] missing path: {rel}")


def check_markdown_links(report: Report) -> None:
    for md_path in iter_markdown_files():
        rel_file = repo_rel(md_path)
        text = md_path.read_text(encoding="utf-8")
        for _, target in MD_LINK_RE.findall(text):
            target = target.strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            resolved = (md_path.parent / path_part).resolve()
            if not resolved.exists():
                report.fail(f"broken markdown link in {rel_file}: {target}")


def check_provenance_banners(report: Report) -> None:
    for md_path in iter_markdown_files():
        rel = repo_rel(md_path)
        if not is_import_target(rel):
            continue
        head = "\n".join(md_path.read_text(encoding="utf-8").splitlines()[:15])
        if not PROVENANCE_RE.search(head):
            report.fail(f"missing provenance banner in import-target doc: {rel}")


def check_readme_links(report: Report) -> None:
    if not README_PATH.exists():
        report.fail("README.md not found")
        return
    readme = README_PATH.read_text(encoding="utf-8")
    for required in README_REQUIRED_LINKS:
        if required not in readme:
            report.fail(f"README.md missing link/reference to: {required}")


def check_bare_dora(report: Report) -> None:
    for md_path in iter_markdown_files():
        rel = repo_rel(md_path)
        if rel == TERMINOLOGY_GLOSSARY:
            continue
        for lineno, line in enumerate(md_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not BARE_DORA_RE.search(line):
                continue
            if DORA_ALLOWED_RE.search(line):
                continue
            report.fail(f"bare 'DORA' in {rel}:{lineno} (disambiguate: DORA metrics / EU DORA)")


def check_tdf(report: Report) -> None:
    for md_path in iter_markdown_files():
        rel = repo_rel(md_path)
        if rel == TERMINOLOGY_GLOSSARY:
            continue
        for lineno, line in enumerate(md_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not TDF_RE.search(line):
                continue
            if "project-local" in line.lower():
                continue
            report.fail(f"TDF used outside allowed context in {rel}:{lineno}")


def check_related_documents(report: Report) -> None:
    for md_path in iter_markdown_files():
        rel = repo_rel(md_path)
        if not is_significant_doc(rel):
            continue
        text = md_path.read_text(encoding="utf-8")
        if not RELATED_SECTION_RE.search(text):
            report.fail(f"significant doc missing '## Related Documents': {rel}")


def main() -> int:
    report = Report()
    manifest = load_manifest()
    check_manifest_paths(report, manifest)
    check_markdown_links(report)
    check_provenance_banners(report)
    check_readme_links(report)
    check_bare_dora(report)
    check_tdf(report)
    check_related_documents(report)

    for warning in report.warnings:
        print(f"WARN: {warning}")
    for error in report.errors:
        print(f"FAIL: {error}")

    if report.errors:
        print(f"\nDoctor: {len(report.errors)} failure(s), {len(report.warnings)} warning(s)")
        return 1

    print(f"Doctor: OK ({len(report.warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
