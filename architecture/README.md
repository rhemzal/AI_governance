# Architecture Guidance

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

This directory helps choose architecture deliberately, not by default or hype.

## Start here

1. Use [ARCHITECTURE_DECISION_FRAMEWORK.md](ARCHITECTURE_DECISION_FRAMEWORK.md)
2. For daily AI work, run [ARCHITECTURE_DECISION_PROMPT.md](ARCHITECTURE_DECISION_PROMPT.md) before picking a style
3. Check coverage in [SOLUTION_CLASS_TAXONOMY.md](SOLUTION_CLASS_TAXONOMY.md)
4. Compare styles in [ARCHITECTURE_STYLE_MATRIX.md](ARCHITECTURE_STYLE_MATRIX.md)
5. Use [DATA_MODELING_GUIDE.md](DATA_MODELING_GUIDE.md) when persistence/modeling is central (incl. `DATA MODEL DECISION RECORD` in §5)
6. Use [rag/](rag/) only as advisory grounding; new notes via [rag/RAG_NOTE_TEMPLATE.md](rag/RAG_NOTE_TEMPLATE.md)

## Do not

- Pick a style before answering the framework questions
- Treat RAG notes as normative rules
- Add new architecture styles without updating taxonomy + matrix + framework links
- Add RAG notes without `rag/RAG_NOTE_TEMPLATE.md` and the taxonomy extension checklist
