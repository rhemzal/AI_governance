# Development Guide

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Documentation Hygiene (Kit Repo)

This kit repo ships **reference CM0–CM1 workflows** under `.github/workflows/` (inline shell + `yq` + `lychee` — **no repository scripts**). Maintainers run stricter dogfood than default adopter CM0 — see `usage/ENFORCEMENT_MATRIX.md`. Adopters copy/adapt YAML blocks from `usage/CI_STARTER_WORKFLOWS.md` into their CI platform.

Before PRs that touch documentation or import bundles, complete the **Doc Hygiene Checklist** below (or rely on CI when it covers the same checks). Paste results into the PR or `usage/AI_RUN_EVIDENCE.md` when running manually.

See `ci/DOC_GATES.md` for gate principles, `usage/ENFORCEMENT_MATRIX.md` for what is automated vs manual, and `usage/PROACTIVE_TRIGGER_MAP.md` for path-prefix triggers.

### CI vs manual checklist (kit repo)

| Checklist item | Kit CI (`doc-hygiene`) | Manual / other CI |
| --- | --- | --- |
| 1. Manifest paths | Yes | — |
| 2. Hub links | Yes (lychee) | — |
| 3. Bundled cross-refs | Yes (inline shell) | — |
| 4. Provenance | Yes | — |
| 5. Terminology | — | Review |
| 6. Related Documents | — | Review |
| 7. Import bundle change | — | Review + `CHANGELOG.md` |
| D5 anti-fragmentation | Error (PR, new `usage/` / `architecture/` docs) | — |

**Other kit workflows:** `aep-advisory.yml`, `adr-required.yml`, `doc-delta-advisory.yml`, `governance-waiver-advisory.yml`.

### Local verification (tool-agnostic)

No repository scripts are required. Before opening a PR you may:

1. Run the checklist steps manually (grep, link checker, manifest review).
2. On GitHub Actions: push a branch and inspect workflow results.
3. Copy individual `run:` blocks from `.github/workflows/doc-hygiene.yml` into your shell if your environment has `bash`, `yq`, and `grep`.

Adopters should not depend on kit-specific script paths — only on **documented CI patterns** in `usage/CI_STARTER_WORKFLOWS.md`.

### Doc Hygiene Checklist (tool-agnostic)

Complete all steps; record **PASS / FAIL** and any failed paths.

1. **Manifest paths** — Every explicit path in `kit-manifest.yml` bundles exists on disk (files and directories).
2. **Hub links** — Relative markdown links in `README.md`, `usage/HOW_TO_IMPORT.md`, `usage/ADOPTION_BUNDLES.md`, and `architecture/README.md` resolve to existing files.
3. **Bundled cross-refs** — For each bundle (`minimal`, `standard`, `full`), every root-level `.md` file referenced from bundled `usage/*.md` is included in that bundle’s resolved path set (or the doc says “read from upstream kit repo only”).
4. **Provenance** — Import-target files under `constitution/`, `ci/`, `adr/`, `usage/`, `architecture/`, `governance/LOCAL_OVERLAY_TEMPLATE.md`, `AGENTS.md`, and `.github/copilot-instructions.md` include a Provenance banner in the first ~500 characters.
5. **Terminology** — New or changed acronyms in normative docs match `architecture/TERMINOLOGY_GLOSSARY.md` or are expanded on first use.
6. **Related Documents** — Significant new or changed docs include `## Related Documents` with valid paths.
7. **Import bundle change** — If `kit-manifest.yml` bundle composition changed: `usage/ADOPTION_BUNDLES.md` aligned and `CHANGELOG.md` entry under `[Import bundle change]`.

**Checklist output template** (paste into PR):

```markdown
## Doc Hygiene Checklist
- Date:
- Commit/PR:
1. Manifest paths: PASS / FAIL — notes:
2. Hub links: PASS / FAIL — notes:
3. Bundled cross-refs: PASS / FAIL — notes:
4. Provenance: PASS / FAIL — notes:
5. Terminology: PASS / FAIL — notes:
6. Related Documents: PASS / FAIL — notes:
7. Import bundle change: PASS / FAIL / N/A — notes:
```

Review scope also includes: ambiguous acronym usage per `architecture/TERMINOLOGY_GLOSSARY.md` and normative/advisory separation for `architecture/rag/` edits.

**Automation (kit repo):** CI job `doc-hygiene` covers checklist items 1–4 and D5 warning; `aep-advisory` and `adr-required` cover cross-cutting gates. Complete items 5–7 manually when not automated. See `usage/ENFORCEMENT_MATRIX.md`.

## Testing Quickstart

This section provides a concise reference for running tests in repositories that adopt this governance kit.

### Virtual Environment Setup

Before running tests, ensure you have a repository-local virtual environment:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -e .[dev]      # or pip install -r requirements-dev.txt
```

### Canonical Test Commands

Use these commands in order of preference:

1. **Make targets** (if available):
   ```bash
   make test              # Run all tests
   make test-unit         # Run unit tests only
   make test-integration  # Run integration tests only
   ```

2. **Repo-local virtual environment** (Python projects):
   ```bash
   .venv/bin/python -m pytest           # Run all tests
   .venv/bin/python -m pytest tests/    # Run specific directory
   .venv/bin/python -m pytest -v        # Verbose output
   ```

3. **Docker fallback** (if provided):
   ```bash
   docker compose run --rm test
   ```

### Important Notes

- **Never assume global pytest or global test runners.** Always use repo-local commands.
- **Check the project README or CONTRIBUTING.md** for project-specific test instructions.
- **Prefer make targets** when available—they provide a stable interface.

### For More Details

For detailed testing guidance, architecture gates, and enforcement principles, see:
- [usage/HOW_TO_USE_WITH_COPILOT.md](usage/HOW_TO_USE_WITH_COPILOT.md) — Test execution canonical path
- [usage/AI_PRODUCTIVITY_CALIBRATION.md](usage/AI_PRODUCTIVITY_CALIBRATION.md) — AI productivity phases and ledger (advisory)
- [ci/TEST_GATES.md](ci/TEST_GATES.md) — Test CI gates and principles
- [constitution/AI_ENFORCEMENT_DAILY.md](constitution/AI_ENFORCEMENT_DAILY.md) — Daily AI enforcement checklist

## Related Documents
- `.github/workflows/doc-hygiene.yml`
- `.github/workflows/aep-advisory.yml`
- `.github/workflows/adr-required.yml`
- `.github/workflows/doc-delta-advisory.yml`
- `.github/workflows/governance-waiver-advisory.yml`
- `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- `usage/GOVERNANCE_WAIVERS.md`
- `usage/CI_STARTER_WORKFLOWS.md`
- `usage/ENFORCEMENT_MATRIX.md`
- `usage/PROACTIVE_TRIGGER_MAP.md`
- `usage/AI_PRODUCTIVITY_CALIBRATION.md`
- `ci/DOC_GATES.md`
