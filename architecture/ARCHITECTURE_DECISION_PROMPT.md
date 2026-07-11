# Architecture Decision Prompt (Copy-Paste)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Short, runnable prompt for everyday AI-assisted architecture work.

`architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` defines the questions; this document gives a **fixed output format** so agents answer them before picking a style or writing code.

## When to use

- Starting a new feature, service, or module where architectural style is not yet explicit
- Before choosing hexagonal vs layered vs event-driven vs pipeline vs hybrid
- When you need a fast precheck before an ADR (`adr/ADR_TEMPLATE.md`)

Do **not** skip the framework ? use it as the reasoning source while filling the output block below.

Run **step A (precheck)** before **step B (RAG/style expansion)**. See `architecture/README.md` (RAG triage).

---

## Copy-paste prompt

```
This task is architecture precheck only unless I say otherwise.

STEP A ? Precheck (always; do not load style matrix or architecture/rag/ yet)

Load and follow:
- architecture/ARCHITECTURE_DECISION_FRAMEWORK.md
- architecture/SOLUTION_CLASS_TAXONOMY.md (relevant row(s) for primary axis only)

Rules:
- Do not pick an architecture style before answering the framework questions.
- Do NOT load architecture/ARCHITECTURE_STYLE_MATRIX.md or architecture/rag/ notes in this step.
- If ADR is required (see framework Rule of Use), say so explicitly and stop before implementation changes.

Context:
- <DESCRIBE THE SYSTEM, CONSTRAINTS, AND WHAT YOU ARE DECIDING>

Output exactly this block (fill every line; use "unknown" + risk note if not inferable):

ARCHITECTURE DECISION PRECHECK
- Primary axis:
- Top 3 quality attributes:
- Stability location:
- Failure zones:
- Points of no return:
- Candidate baseline style:
- Two alternatives rejected:
- Hybrid needed: yes/no
- ADR required: yes/no

STEP B ? RAG / style expansion (after step A only)

Load:
- architecture/ARCHITECTURE_STYLE_MATRIX.md (columns for candidate baseline + max 1 alternative only)
- architecture/rag/ (max 2 note paths from taxonomy links)
- architecture/SOLUTION_CLASS_TAXONOMY.md ?C (max 1 cross-cutting concern, if applicable)
- architecture/DATA_MODELING_GUIDE.md (if persistence/modeling is central)

Corpus budget: max 2 RAG notes + 1 cross-cutting; do not dump the RAG index or full matrix.

Output:

ARCHITECTURE RAG TRIAGE
- Candidate baseline style:
- RAG notes loaded (max 2):
- Cross-cutting (max 1):
- Matrix columns consulted:
- NOT chosen (one line each):
- ADR required: yes/no

Then add:
- Unknowns / risks (bullets)
- Next step (ADR, spike, or proceed) with one sentence why

If persistence or data modeling is central, also output (from architecture/DATA_MODELING_GUIDE.md ?5):

DATA MODEL DECISION RECORD
- Domain model:
- Persistence model:
- Read model:
- System of record:
- Invariants:
- Schema evolution strategy:
- Migration / rollback:
- Testing strategy:
```

---

## Field guide (maps to framework sections)

| Output field | Framework section |
|---|---|
| Primary axis | ?1 Identify the System's Primary Axis |
| Top 3 quality attributes | ?2 Define Quality Attribute Priorities |
| Stability location | ?3 Locate Stability |
| Failure zones | ?4 Boundaries and Failure Zones |
| Points of no return | ?5 Points of No Return |
| Candidate baseline style | ?6 Choose a Baseline Style |
| Two alternatives rejected | ?6 (stress-test alternatives) |
| Hybrid needed | ?6a Hybrid Architectures |
| ADR required | Rule of Use + ?7 Required Output |
| ARCHITECTURE RAG TRIAGE | `architecture/README.md` (RAG triage) |
| DATA MODEL DECISION RECORD (when persistence central) | `architecture/DATA_MODELING_GUIDE.md` ?5 |

If persistence or data modeling is central, include the `DATA MODEL DECISION RECORD` block in the prompt output (see copy-paste prompt above) before finalizing the ADR.

---

## Related Documents

- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/ARCHITECTURE_STYLE_MATRIX.md`
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- `architecture/README.md`
- `adr/ADR_TEMPLATE.md`
- `usage/QUICKGUIDE.md` (Recipe F)
