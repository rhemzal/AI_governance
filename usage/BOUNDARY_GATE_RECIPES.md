# Boundary Gate Recipes (Advisory)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

**Advisory only** — implements `ci/ARCHITECTURE_GATES.md` Gate A1 in stack-specific ways. Normative boundary rules remain in `constitution/AI_RULES.md` and `ci/ARCHITECTURE_GATES.md`.

Adopters copy **inline `run:` blocks** into CI (see `usage/CI_STARTER_WORKFLOWS.md` §3). No repository scripts in the kit.

## Contract default

| Maturity | Boundary A1 |
| --- | --- |
| CM0–CM1 | **Deferred** |
| CM2+ | **Required when tooling exists** |

If tooling is not ready, use `usage/GOVERNANCE_WAIVERS.md` — do not silently skip.

## Recipe index

| Stack | Mechanism | Prerequisites |
| --- | --- | --- |
| Python | Forbidden import `grep` or [import-linter](https://pypi.org/project/import-linter/) | Package layout (`domain/`, `infra/`) |
| TypeScript | [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) or ESLint `import/no-restricted-paths` | Layer folders under `src/` |
| Go | `grep` on import paths or ArchUnit-style tests in `_test.go` | Module path conventions |
| JVM | ArchUnit in test job | ArchUnit dependency, package naming |

---

## Python

**Goal:** Core/domain code must not import infrastructure/adapters.

**Minimal inline check** (no extra deps):

```bash
set -euo pipefail
# Adapt paths and forbidden prefixes
if grep -rE '^(from|import) (infra|adapters|\.infra)\.' src/myapp/domain/ 2>/dev/null; then
  echo "Boundary violation: domain imports infrastructure"
  exit 1
fi
```

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
if grep -r '"example.com/myapp/internal/infra"' ./pkg/domain/ 2>/dev/null; then
  echo "Boundary violation: domain imports infra"
  exit 1
fi
```

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
