# Audit Report — AI_governance kit

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance)._

Date: 2025-12-28
Scope: Full re-run of `usage/AUDIT_PLAYBOOK.md` (Steps 1–5) + strict doc hygiene check.
Result summary:
- Scavenger test: PASS (all items findable quickly)
- Consistency scan: PASS (no conflicting “owners”; canonical pointers present)
- Enforceability review: PASS with one standing constraint (CI gates are principles; enforcement depends on downstream CI implementation)
- Theory validation: PASS (scenario → tactics → architecture → enforcement is explicitly supported)
- Red-team drift scenarios: documented below
- Doc hygiene check: PASS

---

## Findings

- **ID**: A-01
- **Severity**: Low
- **Category**: findability
- **Evidence**: `README.md` includes “Find What You Need (Fast Navigation)” with direct links (e.g., “High-risk change (boundaries/contracts)”).
- **Impact**: If missing, teams waste time and drift to ad-hoc rules.
- **Fix proposal**: None.
- **Verification**: Grep-based scavenger re-run found all items in < 60 seconds.

- **ID**: A-02
- **Severity**: Low
- **Category**: findability
- **Evidence**: `usage/HOW_TO_USE_WITH_COPILOT.md` has “High-Risk Changes” and points to `constitution/AI_ENFORCEMENT.md`.
- **Impact**: Without a clear “high-risk mode”, boundary/contract changes slip without the hard gates.
- **Fix proposal**: None.
- **Verification**: Scavenger item “high-risk boundary/contract change” is findable from README and usage docs.

- **ID**: A-03
- **Severity**: Low
- **Category**: theory
- **Evidence**: `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` requires 2–5 measurable quality attribute scenarios and points to `architecture/rag/QUALITY_ATTRIBUTES.md`.
- **Impact**: Without measurable scenarios, architecture selection devolves into adjectives and cargo-culting.
- **Fix proposal**: None.
- **Verification**: Framework explicitly requires scenario writing and provides a canonical template location.

- **ID**: A-04
- **Severity**: Low
- **Category**: contradiction
- **Evidence**: `architecture/ARCHITECTURE_STYLE_MATRIX.md` states hybridization guidance is a summary and points to the canonical rules in `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`.
- **Impact**: Dual “ownership” of hybridization rules would create drift.
- **Fix proposal**: None.
- **Verification**: Only one canonical location for hybrid rules; matrix is explicitly subordinate.

- **ID**: A-05
- **Severity**: Low
- **Category**: theory
- **Evidence**: `adr/ADR_TEMPLATE.md` includes “Trade-Offs” and “Sensitivity Points & Risks”.
- **Impact**: Without sensitivity points, reviews miss the small changes that break quality attributes.
- **Fix proposal**: None.
- **Verification**: Template enforces the ATAM-lite traceability fields.

- **ID**: A-06
- **Severity**: Medium
- **Category**: enforceability
- **Evidence**: `ci/ARCHITECTURE_GATES.md`, `ci/TEST_GATES.md`, `ci/DOC_GATES.md`, `ci/INTERFACE_GATES.md` are explicitly “principles”.
- **Impact**: In a downstream repo without CI wiring, rules can be “paper compliant” but not policed.
- **Fix proposal**: Downstream action: implement at least one lightweight CI check per gate family (even scripts initially) and make them required checks.
- **Verification**: N/A in this kit alone (requires an actual CI system in the consuming repo).

- **ID**: A-07
- **Severity**: Low
- **Category**: enforceability
- **Evidence**: `constitution/AI_RULES.md` defines “Non-Interactive Execution & Time Limits” and `constitution/AI_ENFORCEMENT.md` has a hard gate for non-interactive commands/timeouts.
- **Impact**: Without this, automation workflows can hang indefinitely or rely on human prompts.
- **Fix proposal**: None.
- **Verification**: Both normative and enforcement docs include the rule and expected behavior.

- **ID**: A-08
- **Severity**: Low
- **Category**: interface
- **Evidence**: `interface/INTERFACE_CI_GATES.md` and `ci/INTERFACE_GATES.md` include “GUI Visual Verification (If Applicable)”, including text-critical OCR guidance.
- **Impact**: GUI correctness can regress without deterministic verification.
- **Fix proposal**: None.
- **Verification**: Gate is present and phrased conditionally (“If Applicable”).

- **ID**: A-09
- **Severity**: Low
- **Category**: duplication
- **Evidence**: Scenario template exists in `architecture/rag/QUALITY_ATTRIBUTES.md`; the framework points to it rather than duplicating full templates.
- **Impact**: Multiple templates drift and create conflicting “right answers”.
- **Fix proposal**: None.
- **Verification**: Consistency scan did not find competing full templates.

- **ID**: A-10
- **Severity**: Low
- **Category**: enforceability
- **Evidence**: A doc hygiene check can enforce basic markdown hygiene (tabs, missing backtick file refs, README hub references).
- **Impact**: Doc drift accumulates silently.
- **Fix proposal**: Downstream action: run it in CI or as a required local pre-commit.
- **Verification**: A doc hygiene check passes.

---

## Red-Team Drift Scenarios (Step 5)

1) Integration bypass of boundary contracts under time pressure
- How it slips through: a new integration directly imports domain internals “just for now”.
- Smallest fix: enforce A1 boundary integrity with a dependency/import allowlist (CI) + require ADR for boundary changes.

2) “Tests exist” but are non-deterministic
- How it slips through: time/random/network dependencies make tests flaky; teams rerun until green.
- Smallest fix: enforce T1 determinism; add a flakiness budget policy (T4) and quarantine rules.

3) Docs drift via parallel “owners”
- How it slips through: teams add a new doc that partially overlaps rules, but keep both.
- Smallest fix: enforce D1 single source of truth and D5 anti-fragmentation; require “Doc Delta” block in PRs.
