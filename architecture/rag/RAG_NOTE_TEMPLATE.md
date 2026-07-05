# RAG Note Template (Extracted)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Standard structure for new advisory notes in `architecture/rag/`.

This is **not** a new concept — it extracts the note body requirements from the kit extension checklist in `architecture/SOLUTION_CLASS_TAXONOMY.md` (“How to Extend This Taxonomy”).

Use it to keep RAG notes consistent and to avoid micro-note sprawl.

## Rules (from `architecture/rag/README.md`)

- Advisory only — see `adr/ADR_0003_RAG_Is_Advisory_Not_Normative.md`.
- Each note MUST include failure modes (“when this fails”).
- Prefer actionable heuristics over academic depth.
- Prefer **extending an existing note** over creating a new file.

## When to use this template

- **Acknowledged or higher** coverage in `architecture/SOLUTION_CLASS_TAXONOMY.md` → write or upgrade a RAG note using the template below.
- **Mentioned only** → do not add a standalone note; extend taxonomy notes or an existing related note instead.

After the note exists, complete the rest of the taxonomy checklist: matrix column, framework links, enforcement (if Full), taxonomy row, RAG README index, and ADR if the change is a significant kit governance decision.

---

## Note file template

Copy into `architecture/rag/<CLASSNAME>.md` and replace placeholders.

```markdown
# <Title> — Advisory Note (Entry Point)

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Coverage Level
**<Acknowledged | Advisory | Full>** — <one sentence: what the kit covers vs. what is out of scope>

## Core Idea
<2–4 sentences: defining characteristic of this pattern/class>

## Why Teams Choose It
- <benefit 1>
- <benefit 2>

## When to Choose It
- <condition 1>
- <condition 2>

## When NOT to Choose It
- <anti-pattern or wrong context 1>
- <anti-pattern or wrong context 2>

## Common Failure Modes
- **<failure name>**: <what goes wrong and why>
- **<failure name>**: <what goes wrong and why>

## Heuristics
- <actionable rule 1>
- <actionable rule 2>

## How This Kit's Boundary Model Applies
<Map core / boundary contracts / integration boundaries to this pattern. Reference `constitution/AI_RULES.md` §1 where relevant.>

## Entry Points in This Kit
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` — <relevant section(s)>
- `architecture/SOLUTION_CLASS_TAXONOMY.md` — coverage map
- <other kit docs as applicable>

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/SOLUTION_CLASS_TAXONOMY.md`
- <related RAG notes, ADRs, CI gates>
```

---

## Compact variant (extend existing note only)

Use when the topic fits an existing note and does not warrant a new file. Add a subsection under the closest note:

```markdown
### <Subtopic> (extension)

**When it applies:** <1–2 sentences>

**Failure modes:**
- <failure 1>

**Heuristics:**
- <heuristic 1>
```

---

## Related Documents

- `architecture/SOLUTION_CLASS_TAXONOMY.md` — full extension checklist (matrix, framework, enforcement, taxonomy row)
- `architecture/rag/README.md` — RAG index and usage rules
- `adr/ADR_0003_RAG_Is_Advisory_Not_Normative.md`
- `architecture/rag/PLUGIN_EXTENSION_ARCHITECTURE.md` — example (Acknowledged entry-point note)
- `architecture/rag/SERVERLESS_FAAS.md` — example (Advisory entry-point note)
- `architecture/rag/OBSERVABILITY_AS_ARCHITECTURE.md` — example (Advisory cross-cutting note)
- `architecture/rag/FEATURE_FLAGS_PROGRESSIVE_DELIVERY.md` — example (Advisory cross-cutting note)
