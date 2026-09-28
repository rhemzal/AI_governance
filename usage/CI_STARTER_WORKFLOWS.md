# CI Starter Workflows (Reference Implementations)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This guide provides **ready-to-copy GitHub Actions starter examples** for the gate categories in this kit.

These are **reference implementations**, not mandatory stack-specific prescriptions. Adapt tooling, commands, and paths to your repository.

**Kit repo living reference:** `.github/workflows/doc-hygiene.yml`, `aep-advisory.yml`, `adr-required.yml`, `doc-delta-advisory.yml`, `governance-waiver-advisory.yml` (inline shell/Python + `yq` + `lychee`; AEP uses a Python standard-library reference validator).

Adopters adapt selected `run:` blocks and project paths deliberately. Kit-wide catalog checks are maintainer-only. The scoped snapshot importer/checker (ADR-0010) and AEP validator (ADR-0009) must each match the pinned kit revision; keep imported kit files separate from host-owned workflow/template entry points.

## 1) Documentation hygiene gate (starter)

Use this project-owned pattern after the selected import has been verified as in `usage/HOW_TO_IMPORT.md`. Do not transplant the upstream all-bundle job into a partial import. Merge with an existing host workflow instead of overwriting it:

```yaml
name: doc-hygiene
on:
  pull_request:
    paths: ['**.md', '**/kit-manifest.yml']
  push:
    branches: [main]
    paths: ['**.md', '**/kit-manifest.yml']

concurrency:
  group: doc-hygiene-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}

jobs:
  hygiene:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4

      - name: Provenance banners (import targets)
        run: |
          set -euo pipefail
          fail=0
          KIT_ROOT=vendor/AI_governance
          test -d "$KIT_ROOT/constitution" || { echo 'Missing imported baseline'; exit 1; }
          while IFS= read -r f; do
            head -c 500 "$f" | grep -q 'Provenance' || { echo "Missing Provenance: $f"; fail=1; }
          done < <(find "$KIT_ROOT/constitution" -name '*.md' -type f)
          exit "$fail"

      - name: Markdown link check (hub docs)
        uses: lycheeverse/lychee-action@v2
        with:
          args: --no-progress './README.md'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # Verify the declared selected copy against its pinned source (section 1b).
      # The upstream all-bundle catalog check is NOT an adopter check.
```

Gate intent: `ci/DOC_GATES.md` (D1–D3, D5 warning). Manual checklist: `DEVELOPMENT.md`. Matrix: `usage/ENFORCEMENT_MATRIX.md`.

## 1b) Selected-bundle verification versus kit catalog checks

For an adopter, keep a clean checkout of the recorded upstream SHA available as `KIT_SOURCE`. Convert its manifest with yq v4.44.3 and invoke `ci/import_bundle.py --check` with the declared destination and **the same selected bundles** used at import, following `usage/HOW_TO_IMPORT.md`. Run it from the pinned source, not a potentially modified imported checker. It detects missing, changed and unexpected selected-copy files without writing to the project. A manual comparison is acceptable where the CM0 contract allows local evidence.

The upstream `.github/workflows/doc-hygiene.yml` intentionally checks all catalog bundles and bundled references in the complete kit repository. Retain that maintainer check upstream; do not require unselected architecture/research paths in minimal or standard adopters. It does not replace semantic review of required/optional context or project-owned links.

## 2) Deterministic test gate (starter with timeout)

```yaml
name: deterministic-tests
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - name: Run deterministic tests (non-interactive)
        timeout-minutes: 15
        run: |
          echo "Use repo-local canonical test command."
          echo "Examples: make test OR your stack's headless test runner"
```

## 3) Boundary integrity gate (starter)

```yaml
name: boundary-integrity
on: [pull_request]
jobs:
  boundary:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - name: Run boundary checks
        run: |
          set -euo pipefail
          echo "Implement per ecosystem (ci/ARCHITECTURE_GATES.md Gate A1):"
          echo "- Python: import-linter or custom import allow/deny checks"
          echo "- TypeScript: dependency-cruiser / eslint import boundaries"
          echo "- JVM: ArchUnit tests"
          echo "- Go: package dependency checks + architectural tests"
          # Example: fail if a forbidden import pattern appears
          # if grep -R "from domain.internal" src/; then exit 1; fi
          exit 0
```

Full stack-specific inline examples: `usage/BOUNDARY_GATE_RECIPES.md` and below.

### 3a) Python — static forbidden imports (inline)

Same check and limitations as `usage/BOUNDARY_GATE_RECIPES.md`; configure the root and forbidden components before adoption.

```yaml
      - name: Python boundary syntax check (example)
        run: |
          set -euo pipefail
          python3 - <<'PYTHON'
          import ast
          import os
          import tokenize
          from pathlib import Path

          # Adapt the root and forbidden module components to the declared boundaries.
          root = Path("src/myapp/domain")
          forbidden = {"infra", "adapters"}
          if not root.is_dir() or root.is_symlink():
              raise SystemExit(f"Invalid source directory: {root}")

          def scan_error(error):
              raise error  # os.walk otherwise ignores directory-read failures

          count = 0
          violations = []
          for directory, dirs, files in os.walk(root, onerror=scan_error):
              dirs.sort()
              for name in sorted(dirs + files):
                  if (Path(directory) / name).is_symlink():
                      raise SystemExit(f"Unsupported source symlink: {Path(directory) / name}")
              for name in sorted(files):
                  if not name.endswith(".py"):
                      continue
                  path = Path(directory) / name
                  with tokenize.open(path) as source:
                      tree = ast.parse(source.read(), filename=str(path))
                  count += 1
                  for node in ast.walk(tree):
                      if isinstance(node, ast.Import):
                          imports = [alias.name for alias in node.names]
                      elif isinstance(node, ast.ImportFrom):
                          imports = [node.module or ""]
                          imports += [(node.module or "") + "." + alias.name for alias in node.names]
                      else:
                          continue
                      if any(forbidden.intersection(name.split(".")) for name in imports):
                          violations.append(f"{path}:{node.lineno}: forbidden infrastructure import")
          if not count:
              raise SystemExit(f"No Python source files found: {root}")
          if violations:
              raise SystemExit("\n".join(violations))
          print(f"PASS: checked {count} Python source files")
          PYTHON
```

### 3b) TypeScript — dependency-cruiser (inline invoke)

```yaml
      - name: TS boundary (dependency-cruiser)
        run: |
          set -euo pipefail
          npx --yes dependency-cruiser@16 --config .dependency-cruiser.cjs src
```

### 3c) Go — forbidden quoted import path (inline)

Conservative text tripwire; review the limitations in `usage/BOUNDARY_GATE_RECIPES.md` before using it as boundary evidence.

```yaml
      - name: Go boundary path scan (example)
        run: |
          set -euo pipefail
          # Adapt the directory and escaped module prefix. This is a text scan, not a Go parser.
          ROOT=./pkg/domain
          test -d "$ROOT" || { echo "Missing source directory: $ROOT" >&2; exit 1; }
          SOURCE="$(find "$ROOT" -type f -name '*.go' -print -quit)"
          test -n "$SOURCE" || { echo "No Go source files found: $ROOT" >&2; exit 1; }
          status=0
          grep -rEn --include='*.go' '["`]example\.com/myapp/internal/infra(/[^"`]*)?["`]' "$ROOT" || status=$?
          case "$status" in
            0) echo "Boundary violation: domain references infrastructure" >&2; exit 1 ;;
            1) echo "PASS: no forbidden quoted import path found" ;;
            *) echo "Boundary scan failed (grep exit $status)" >&2; exit "$status" ;;
          esac
```

## 4) ADR-required check for architecture-impacting paths

Python 3 standard library and Git only. The comparison uses the PR base and tested merge revision. Full history makes both revisions available; a missing revision is a check failure. Keep the inline check synchronized with `.github/workflows/adr-required.yml` at the pinned kit revision.

```yaml
name: adr-required
on: [pull_request]
permissions:
  contents: read
jobs:
  adr:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false
      - name: Require ADR when governance paths change
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
          HEAD_SHA: ${{ github.sha }}
        run: |
          set -euo pipefail
          python3 - "$BASE_SHA" "$HEAD_SHA" <<'PYTHON'
          import re
          import subprocess
          import sys

          base, head = sys.argv[1:]

          def changed(*options):
              output = subprocess.check_output(
                  ["git", "diff", "--name-only", "-z", *options, base, head, "--"])
              return output.split(b"\0")[:-1]

          # Include both sides of moves when deciding whether governance was touched.
          prefixes = (b"constitution/", b"ci/", b"architecture/", b"interface/", b"adr/")
          if not any(path.startswith(prefixes) for path in changed("--no-renames")):
              print("SKIP: no governance-impacting paths changed")
              sys.exit(0)

          # A deletion, detected rename, template, symlink or type change is not a decision update.
          for path in changed("--find-renames=50%", "--diff-filter=AM"):
              if not re.fullmatch(rb"adr/ADR_[0-9]+_[^/]+\.md", path):
                  continue
              entry = subprocess.check_output(["git", "ls-tree", "-z", head, "--", path])
              metadata = entry.split(b"\t", 1)[0].split()
              if len(metadata) == 3 and metadata[:2] in ([b"100644", b"blob"], [b"100755", b"blob"]):
                  print("PASS: added/modified numbered ADR exists at HEAD; content still needs review")
                  sys.exit(0)
          raise SystemExit("Governance-impacting paths changed without an added/modified numbered ADR")
          PYTHON
```

Governance prefixes match the kit workflow: `constitution/`, `ci/`, `architecture/`, `interface/`, `adr/`. Usage-only edits do not trigger this check's ADR requirement. An eligible record is an added or modified numbered `adr/ADR_<number>_<name>.md` regular file present at the tested revision. Deletions, templates, symlinks, type changes and Git-detected renames do not qualify. A move alone records no new decision; add/update a decision separately. Git's similarity classification is a heuristic, so substantial rewrites/moves and the decision's meaning still require review. The check does not validate ADR content or prove approval.

## 5) AEP declaration validation

Applicability is based on risk, dependent non-trivial steps, handoff, and concurrency (`usage/AEP_VALIDATION.md`). File count is only an advisory prompt to review applicability. Missing declarations warn; an explicitly declared plan must satisfy the structured format, even in a one-file PR.

Merge the upstream `.github/workflows/aep-advisory.yml` into a host-owned workflow and point its validator/test paths to the declared kit root (for example `vendor/AI_governance/ci/validate_aep.py`). Use the workflow and validator from the **same pinned kit revision**. Copy `ci/tests/` as well if retaining the reference workflow's regression-test step. The standard bundle includes `ci/`; minimal adopters can read/copy these files from the upstream kit. No external Python packages are needed.

The validation step is:

```yaml
- name: Validate AEP declaration
  env:
    PR_BODY: ${{ github.event.pull_request.body }}
    CHANGED_FILES: ${{ steps.diff.outputs.count }}
  run: python3 ci/validate_aep.py --changed-files "$CHANGED_FILES"
```

Use a read-only `contents` token and non-persistent checkout credentials, as in the reference workflow. Keep PR text in an environment variable; do not interpolate it into shell source or execute commands from the declaration. The reference workflow runs on pull_request events, not privileged pull_request_target.

The checker validates declared data, not authority, feasibility, completion, or correctness. Review those separately. Migrate legacy `AEP Status` plans using the structured example in `usage/AEP_VALIDATION.md`; the old whole-body grep is no longer the reference.

## 6) Governance waiver label advisory

When a PR uses label `governance-waiver`, require the waiver block in the PR body (`usage/GOVERNANCE_WAIVERS.md`). Kit repo reference: `.github/workflows/governance-waiver-advisory.yml`.

```yaml
name: governance-waiver-advisory
on:
  pull_request:
    types: [opened, edited, synchronize, labeled]
jobs:
  waiver:
    if: contains(github.event.pull_request.labels.*.name, 'governance-waiver')
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Require waiver block in PR body
        env:
          PR_BODY: ${{ github.event.pull_request.body }}
        run: |
          set -euo pipefail
          if ! printf '%s' "$PR_BODY" | grep -qi 'Governance waiver'; then
            echo "::warning::PR has governance-waiver label but no Governance waiver section (see usage/GOVERNANCE_WAIVERS.md)"
          fi
          for field in 'Gate ID' Owner Expiration 'Compensating control'; do
            if ! printf '%s' "$PR_BODY" | grep -qi "$field"; then
              echo "::warning::Waiver block missing field: $field"
            fi
          done
```

## 7) DOC DELTA advisory (behavior-changing PRs)

Warn when non-documentation paths change without a `DOC DELTA` block in the PR body. CM2+ adopters may promote to `exit 1` via overlay. Kit repo: `.github/workflows/doc-delta-advisory.yml`.

```yaml
name: doc-delta-advisory
on:
  pull_request:
    types: [opened, edited, synchronize]
jobs:
  doc-delta:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Warn when code paths change without DOC DELTA
        env:
          PR_BODY: ${{ github.event.pull_request.body }}
        run: |
          set -euo pipefail
          BASE="${{ github.event.pull_request.base.sha }}"
          HEAD="${{ github.sha }}"
          CHANGED="$(git diff --name-only "$BASE" "$HEAD")"
          NON_DOC="$(echo "$CHANGED" | grep -Ev '^(.*\.md$|docs/|usage/|adr/)' || true)"
          if [ -z "$NON_DOC" ]; then exit 0; fi
          if printf '%s' "$PR_BODY" | grep -qiE 'DOC DELTA|### DOC DELTA'; then exit 0; fi
          echo "::warning::Non-doc paths changed without DOC DELTA (ci/DOC_GATES.md D2)"
```

## Notes for adopters
- Keep this file as a **starter pack**; adapt commands to your stack.
- Prefer **inline CI `run:` steps** and existing CI actions over custom repository scripts (`adr/ADR_0004_Tooling_Is_Experimental.md`).
- Keep rule text canonical in:
  - `ci/DOC_GATES.md`
  - `ci/TEST_GATES.md`
  - `ci/ARCHITECTURE_GATES.md`
  - `constitution/AI_ENFORCEMENT.md`

## Related Documents
- `.github/workflows/doc-hygiene.yml` (kit repo reference)
- `.github/workflows/aep-advisory.yml` (kit repo reference)
- `.github/workflows/adr-required.yml` (kit repo reference)
- `usage/CI_MINIMUM_ADOPTION.md`
- `usage/GOVERNANCE_WAIVERS.md`
- `usage/BOUNDARY_GATE_RECIPES.md`
- `.github/workflows/doc-delta-advisory.yml`
- `.github/workflows/governance-waiver-advisory.yml`
- `usage/AEP_VALIDATION.md`
- `ci/DOC_GATES.md`
- `ci/TEST_GATES.md`
- `ci/ARCHITECTURE_GATES.md`
- `constitution/AI_ENFORCEMENT.md`
