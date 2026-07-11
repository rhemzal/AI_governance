# CI Starter Workflows (Reference Implementations)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This guide provides **ready-to-copy GitHub Actions starter examples** for the gate categories in this kit.

These are **reference implementations**, not mandatory stack-specific prescriptions. Adapt tooling, commands, and paths to your repository.

**Kit repo living reference:** `.github/workflows/doc-hygiene.yml`, `aep-advisory.yml`, `adr-required.yml`, `doc-delta-advisory.yml`, `governance-waiver-advisory.yml` (inline shell + `yq` + `lychee` — **no repository scripts**).

Adopters copy **`run:` blocks** from these workflows or the starters below into their CI vendor. Do not rely on a shared script directory in the kit.

## 1) Documentation hygiene gate (starter)

Copy from the kit repo or use this minimal pattern:

```yaml
name: doc-hygiene
on:
  pull_request:
    paths: ['**.md', 'kit-manifest.yml']
  push:
    branches: [main]
    paths: ['**.md', 'kit-manifest.yml']

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
          while IFS= read -r f; do
            head -c 500 "$f" | grep -q 'Provenance' || { echo "Missing Provenance: $f"; fail=1; }
          done < <(find constitution ci adr usage -name '*.md' -type f)
          exit "$fail"

      - name: Markdown link check (hub docs)
        uses: lycheeverse/lychee-action@v2
        with:
          args: --no-progress './README.md'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # Optional: bundled cross-ref check (standard/full adopters with kit-manifest.yml).
      # Full inline step: see .github/workflows/doc-hygiene.yml in the kit repo.
```

Gate intent: `ci/DOC_GATES.md` (D1–D3, D5 warning). Manual checklist: `DEVELOPMENT.md`. Matrix: `usage/ENFORCEMENT_MATRIX.md`.

## 1b) Bundled cross-ref check (inline pattern)

For repos that ship `kit-manifest.yml` and `usage/` docs, add a step that:

1. Resolves `minimal`, `standard`, and `full` bundle path sets via `yq` (including `extends` / `composes` unions).
2. Scans bundled `usage/*.md` for root-level `` `FILE.md` `` / `](FILE.md)` references.
3. Fails when a referenced root `.md` is not in the bundle path set (allowlist target-repo hubs: `README.md`, `CONTRIBUTING.md`).

Copy the complete inline implementation from `.github/workflows/doc-hygiene.yml` (`Bundled cross-refs` step) — do not add a repository script.

```yaml
      - name: Bundled cross-refs (example placeholder)
        run: |
          echo "Copy the Bundled cross-refs step from kit repo doc-hygiene.yml"
```

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

### 3a) Python — forbidden import grep (inline)

```yaml
      - name: Python boundary grep (example)
        run: |
          set -euo pipefail
          # Adapt: core must not import infrastructure
          if grep -rE '^(from|import) (infra|adapters)\.' src/myapp/domain/ 2>/dev/null; then
            echo "Domain layer imports infrastructure"
            exit 1
          fi
```

### 3b) TypeScript — dependency-cruiser (inline invoke)

```yaml
      - name: TS boundary (dependency-cruiser)
        run: |
          set -euo pipefail
          npx --yes dependency-cruiser@16 --config .dependency-cruiser.cjs src
```

### 3c) Go — forbidden import path (inline)

```yaml
      - name: Go boundary grep (example)
        run: |
          set -euo pipefail
          if grep -r '"my/module/internal/infra"' ./pkg/domain/ 2>/dev/null; then
            echo "Domain imports infra path"
            exit 1
          fi
```

## 4) ADR-required check for architecture-impacting paths

```yaml
name: adr-required
on: [pull_request]
jobs:
  adr:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - name: Fail when architecture-impacting paths changed without ADR
        run: |
          set -euo pipefail
          BASE="${{ github.event.pull_request.base.sha }}"
          HEAD="${{ github.sha }}"
          CHANGED="$(git diff --name-only "$BASE" "$HEAD")"
          if echo "$CHANGED" | grep -Eq '^(constitution/|ci/|usage/|architecture/|interface/|adr/)'; then
            if ! echo "$CHANGED" | grep -Eq '^adr/ADR_.*\.md$'; then
              echo "Architecture-impacting paths changed, but no ADR file was added/updated."
              exit 1
            fi
          fi
```

## 5) AEP READY advisory check (multi-file PRs)

Use when agents or humans post AEP blocks in PR descriptions. Advisory until required by local policy (`usage/AEP_VALIDATION.md`).

```yaml
name: aep-advisory
on:
  pull_request:
    types: [opened, edited, synchronize]
jobs:
  aep:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - name: Count changed files
        id: diff
        run: |
          set -euo pipefail
          BASE="${{ github.event.pull_request.base.sha }}"
          HEAD="${{ github.sha }}"
          COUNT="$(git diff --name-only "$BASE" "$HEAD" | wc -l | tr -d ' ')"
          echo "count=$COUNT" >> "$GITHUB_OUTPUT"
      - name: Warn when multi-file PR lacks AEP READY markers
        if: steps.diff.outputs.count >= 2
        env:
          PR_BODY: ${{ github.event.pull_request.body }}
        run: |
          set -euo pipefail
          if ! printf '%s' "$PR_BODY" | grep -q 'AEP Status'; then
            echo "::warning::Multi-file PR without AEP Status field (see usage/AEP_VALIDATION.md)"
          fi
          if printf '%s' "$PR_BODY" | grep -q 'AEP Status: READY'; then
            for token in TBD TODO 'as needed' etc.; do
              if printf '%s' "$PR_BODY" | grep -qi "$token"; then
                echo "::error::AEP READY contains vague placeholder: $token"
                exit 1
              fi
            done
            fail=0
            for field in Objective Steps; do
              if ! printf '%s' "$PR_BODY" | grep -qi "$field"; then
                echo "::error::AEP READY missing required field: $field"
                fail=1
              fi
            done
            if ! printf '%s' "$PR_BODY" | grep -qiE 'test command|Test execution|make test|pytest|npm test'; then
              echo "::error::AEP READY missing explicit test execution reference"
              fail=1
            fi
            exit "$fail"
          fi
```

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
