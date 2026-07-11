# Proactive Trigger Map

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

When a change touches a path prefix, run the mapped checks **before merge** — constraints in checks, not prompts.

Use this map so agents do not guess which governance mode applies.

## Trigger table

| Path prefix | Risk mode | Required checks / actions |
| --- | --- | --- |
| `constitution/**` | **High-risk** | Load `constitution/AI_ENFORCEMENT.md`; ADR consideration; full `## COMPLIANCE REPORT`; terminology check (`architecture/TERMINOLOGY_GLOSSARY.md`). |
| `ci/**` | **High-risk** | Adaptive Governance Check (`constitution/ADAPTIVE_GOVERNANCE.md`); CI adoption consistency (`usage/CI_MINIMUM_ADOPTION.md`); verify gate docs align with enforcement level. |
| `architecture/**` | **Medium** (often ADR-adjacent) | Start at `architecture/README.md`; terminology check; decision consistency (`architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`, `architecture/ARCHITECTURE_DECISION_PROMPT.md` for prechecks); new RAG notes via `architecture/rag/RAG_NOTE_TEMPLATE.md` + taxonomy checklist; confirm `architecture/rag/` edits stay advisory/non-normative. |
| `interface/**` | **High-risk** | Automation-first check (`adr/ADR_0001_Automation_First_Interfaces.md`); interface gates (`ci/INTERFACE_GATES.md`, `interface/INTERFACE_CI_GATES.md`). |
| `research/**` | **Low** (advisory) | Advisory/non-normative check — must not override `constitution/` or `ci/`; ambiguous acronym check per `architecture/TERMINOLOGY_GLOSSARY.md`. |
| `usage/**` | **Medium** | Import/adoption consistency; broken link check; DOC DELTA when behavior guidance changes. |
| `governance/**` | **High-risk** (local policy) | Overlay precedence check (`usage/LOCAL_OVERLAY_AND_PRECEDENCE.md`); no silent conflict with imported kit rules. |
| `adr/**` | **Medium → High** | New ADR uses `adr/ADR_TEMPLATE.md`; accepted ADRs are durable decisions — link from affected rules/gates. |
| `.github/**` | **Medium** | Projection brevity check; no duplicated governance playbooks; point to `constitution/` and `usage/` instead. |
| `kit-manifest.yml` | **Medium** | Manifest paths exist (doc hygiene review); update `usage/ADOPTION_BUNDLES.md` if bundle purpose changes; **Import bundle change** changelog entry. |
| Root projections (`AGENTS.md`, `README.md`) | **Medium** | Brevity + link integrity; README must keep top links to core entry points. |

## Event triggers

| Event | Risk mode | Required checks / actions |
| --- | --- | --- |
| GUI / interface test failure | Medium → High | Use `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`; capture first failure signal; avoid full rerun until diagnosis. |
| Ambiguous cause / first fix failed | Medium | Use `usage/DECISION_PROMPTS_DEBUGGING.md` Prompt 6 (`DBG-science-01`); falsify hypotheses before next fix. |

## Multi-prefix changes

If a PR spans multiple prefixes, apply the **highest** risk mode from the table and union all mapped checks.

Example: `constitution/AI_RULES.md` + `ci/TEST_GATES.md` → high-risk + adaptive governance + CI consistency.

## Automation hooks

| Check | Command / doc |
| --- | --- |
| Doc hygiene (links, provenance, manifest, terminology) | Kit repo: `.github/workflows/doc-hygiene.yml`; manual: `DEVELOPMENT.md` checklist |
| Doc gates (principles) | `ci/DOC_GATES.md` |
| AEP for multi-file agent work | `usage/AEP_VALIDATION.md`; optional CI: `usage/CI_STARTER_WORKFLOWS.md` §5 |
| Boundary integrity (downstream) | `usage/CI_STARTER_WORKFLOWS.md` §3; `ci/ARCHITECTURE_GATES.md` |
| ADR on architecture paths (downstream) | `usage/CI_STARTER_WORKFLOWS.md` §4 |
| AVR on verification failure | `constitution/AI_ENFORCEMENT_DAILY.md` |

## Related Documents

- `constitution/AI_ENFORCEMENT.md`
- `constitution/ADAPTIVE_GOVERNANCE.md`
- `ci/DOC_GATES.md`
- `usage/CI_MINIMUM_ADOPTION.md`
- `AGENTS.md`
