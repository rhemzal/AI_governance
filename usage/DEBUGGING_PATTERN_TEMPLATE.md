# Debugging Pattern Template

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Reusable schema for documenting debugging and quality-improvement patterns in the [Debugging Effectiveness Catalog](DEBUGGING_EFFECTIVENESS_CATALOG.md).

This document is **advisory**. Normative test and enforcement rules remain in `constitution/` and `ci/`.

## How to use

1. Copy the template below into a new section of the catalog (or a project-local overlay under `usage/`).
2. Fill every mandatory subsection.
3. Link to existing governance docs — do not restate normative rules.
4. Add the pattern to the catalog selection flow if it is generally reusable.

---

## Template (copy below this line)

```markdown
### Pattern: <short name>

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-<domain>-<nn>` (e.g. `DBG-media-01`) |
| **Maturity** | `experimental` \| `proven` \| `standard` |
| **Owner** | optional — team or role |

#### Problem fit
<One paragraph: symptom classes, system shape, and failure domain this pattern addresses.>

#### Use when
- <bullet>
- <bullet>

#### Do NOT use when
- <bullet>
- <bullet>

#### Pros
- <bullet>

#### Cons
- <bullet>

#### Failure modes
- <How this pattern can mislead, waste time, or hide real defects.>

#### Expected gain
- **Speed:** <e.g. 10× faster iteration on transport layer vs full real-time playback>
- **Quality:** <e.g. catches contract drift before E2E; reduces false-positive fixes>

#### Implementation cost
- **Setup:** low \| medium \| high — <brief note>
- **Maintenance:** low \| medium \| high — <brief note>

#### PR evidence expectations
- <What reviewers should see: commands, artifacts, before/after signals>
- <Link to `usage/AI_RUN_EVIDENCE.md` or project evidence block if applicable>

#### Governance Alignment
Map to existing kit documents (cite paths; do not duplicate normative text):

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Rules / enforcement | `constitution/AI_RULES.md`, `constitution/AI_ENFORCEMENT_DAILY.md` | e.g. AVR loop, smallest scope first |
| High-risk gates | `constitution/AI_ENFORCEMENT.md` | e.g. boundary/contract changes need ADR |
| CI / test gates | `ci/TEST_GATES.md`, `ci/INTERFACE_GATES.md` | e.g. quarantine policy, determinism |
| Architecture | `architecture/README.md`, `architecture/TERMINOLOGY_GLOSSARY.md` | e.g. integration boundary, MCP |

#### AI Prompt Snippet
```
When applying pattern <Pattern ID>:
- State scope, assumptions, and risks.
- Propose verification steps before code changes.
- Output evidence in the PR-ready block below.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — <Pattern ID>
- Pattern:
- Problem symptom:
- Scope (smallest useful):
- Assumptions:
- Commands/checks run:
- Signals captured:
- Working diagnosis (not RCA unless verified):
- Fix applied (if any):
- Rerun result:
- Residual risk:
```
```

---

## Related Documents

- `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md`
- `usage/DEBUGGING_ACCELERATION_PLAYBOOK.md`
- `usage/DECISION_PROMPTS_DEBUGGING.md`
- `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`
- `usage/AI_RUN_EVIDENCE.md`
- `ci/TEST_GATES.md`
- `constitution/AI_RULES.md`
