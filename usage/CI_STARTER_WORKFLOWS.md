# CI Starter Workflows (Reference Implementations)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This guide provides **ready-to-copy GitHub Actions starter examples** for the gate categories in this kit.

These are **reference implementations**, not mandatory stack-specific prescriptions. Adapt tooling, commands, and paths to your repository.

## 1) Documentation hygiene gate (starter)

```yaml
name: doc-hygiene
on:
  pull_request:
  push:
    branches: [ main ]
jobs:
  docs:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - name: Validate markdown links (example)
        run: |
          echo "Replace with your checker (e.g., link/doc consistency scripts)."
          echo "Gate intent: ci/DOC_GATES.md"
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
          echo "Examples: make test OR .venv/bin/python -m pytest"
```

## 3) Boundary integrity gate (starter placeholders)

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
          echo "Implement per ecosystem:"
          echo "- Python: import-linter / custom import allow-deny checks"
          echo "- TypeScript: dependency-cruiser / eslint import boundaries"
          echo "- JVM: ArchUnit tests"
          echo "- Go: package dependency checks + architectural tests"
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

## Notes for adopters
- Keep this file as a **starter pack**; adapt commands to your stack.
- Keep rule text canonical in:
  - `ci/DOC_GATES.md`
  - `ci/TEST_GATES.md`
  - `ci/ARCHITECTURE_GATES.md`
  - `constitution/AI_ENFORCEMENT.md`

## Related Documents
- `usage/CI_MINIMUM_ADOPTION.md`
- `ci/DOC_GATES.md`
- `ci/TEST_GATES.md`
- `ci/ARCHITECTURE_GATES.md`
- `constitution/AI_ENFORCEMENT.md`
