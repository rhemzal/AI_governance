# Boundary Gate Recipes (Advisory)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

**Advisory only** — implements `ci/ARCHITECTURE_GATES.md` Gate A1 in stack-specific ways. Normative boundary rules remain in `constitution/AI_RULES.md` and `ci/ARCHITECTURE_GATES.md`.

Adopters copy **inline `run:` blocks** into CI (see `usage/CI_STARTER_WORKFLOWS.md` §3). These boundary recipes require no kit scripts; the separate AEP gate has a small reference validator.

## Contract default

| Maturity | Boundary A1 |
| --- | --- |
| CM0–CM1 | **Deferred** |
| CM2+ | **Required when tooling exists** |

If tooling is not ready, use `usage/GOVERNANCE_WAIVERS.md` — do not silently skip.

## Recipe index

| Stack | Mechanism | Prerequisites |
| --- | --- | --- |
| Python | Static import syntax check or [import-linter](https://pypi.org/project/import-linter/) | Package layout (`domain/`, `infra/`) |
| TypeScript | [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) or ESLint `import/no-restricted-paths` | Layer folders under `src/` |
| Go | Quoted-path text scan or ArchUnit-style tests in `_test.go` | Module path conventions |
| JVM | ArchUnit in test job | ArchUnit dependency, package naming |

---

## Python

**Goal:** Core/domain code must not import infrastructure/adapters.

**Inline static check** (Python 3 standard library; no imported code is executed):

```bash
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

This conservative name policy rejects `infra` or `adapters` as any component of a static import, including `from . import infra`, aliases, indented and multiline imports. Adapt those names to your layout. A same-named ordinary symbol can be a false positive. Dynamic imports, re-exports and transitive dependencies need a dependency-aware tool/review. Missing/empty roots, symlinks, unreadable sources and invalid Python syntax fail visibly.

**Stronger:** configure `import-linter` in `pyproject.toml` and run `lint-imports` in CI.

---

## TypeScript

**Goal:** `src/domain` must not depend on `src/infrastructure`.

**dependency-cruiser** (`.dependency-cruiser.cjs` required in repo):

```bash
npx --yes dependency-cruiser@16 --config .dependency-cruiser.cjs src
```

**ESLint alternative:** `import/no-restricted-paths` zones in `eslint.config.js`.

---

## Go

**Goal:** `pkg/domain` must not import internal infrastructure packages.

```bash
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

The scan covers ordinary quoted/raw import paths, aliases and subpackages. It is a conservative text tripwire: comments/string examples may be false positives, and escaped import literals are not decoded. It does not prove the Go dependency graph. Use regular source trees (no symlinked sources); missing/empty roots and scanner errors fail. For complete syntax/build-tag coverage, use architectural tests or a configured dependency checker.

**Stronger:** architectural tests in Go test files (run via CM1 test job, not a kit script).

---

## JVM (ArchUnit)

Boundary checks belong in the **test gate** (T1), not a separate shell step:

- Add ArchUnit test class enforcing layer rules
- Run with `./mvnw test` or `./gradlew test`

See `ci/TEST_GATES.md` — boundary validation is often expressed as architectural tests.

---

## Wiring checklist (CM2)

1. Agree layer names in ADR or overlay
2. Pick one mechanism from this doc
3. Add inline step to `boundary-integrity` workflow (§3 starter)
4. Remove `exit 0` placeholder; make job required on PRs
5. Record test command in `governance/LOCAL_OVERLAY.md`

## Related Documents

- `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`
- `usage/CI_STARTER_WORKFLOWS.md`
- `ci/ARCHITECTURE_GATES.md`
- `usage/GOVERNANCE_WAIVERS.md`
