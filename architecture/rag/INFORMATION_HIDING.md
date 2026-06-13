# Information Hiding (Parnas) — Advisory Note

## Core Idea
Design modules so that **volatile decisions are hidden** behind stable interfaces.
A “secret” is any design choice likely to change.

## Practical Heuristics
- Put volatility at the edges: protocols, persistence, vendors, UIs.
- Keep the core stable: domain rules, invariants, policies.
- If a change forces edits across many modules, information hiding is failing.

## What This Suggests Architecturally
- Clear boundaries and boundary contracts (ports/interfaces) help isolate change.
- Dependency direction should point toward stable policy.

## Extraction Discipline
When deciding whether and how to extract a responsibility into a separate module:
- Extract by **volatility and responsibility**, not by file-size or line-count thresholds.
  A small file that changes for many reasons is a better extraction candidate than a large file that changes for one reason.
- Prefer one extraction per change slice:
  - **Feature seam**: a boundary drawn around a unit of behavioral delivery (one use-case, one capability). Use this when the extraction enables independent testability or delivery.
  - **Build seam**: a boundary drawn around a unit of build or dependency isolation (one build target, one package). Use this when the extraction reduces rebuild blast radius or unnecessary dependency coupling.
  - Mixing both seam types in one change increases review complexity; prefer separating them.
- Before extracting, verify that the new boundary is stable (unlikely to change in the next 2–3 cycles). Premature extraction of an unstable boundary creates churn faster than it reduces it.

## When This Fails / Failure Modes
- The team cannot identify what is volatile (wrong stability assumptions).
- Premature abstraction: hiding "secrets" that are not actually volatile.
- Performance constraints force leaky abstractions (e.g., query patterns crossing boundaries).
- Extraction is driven by tool suggestions or file-size linters rather than by responsibility analysis.
- A "build seam" is treated as a "feature seam": the boundary is placed to satisfy CI speed without a corresponding behavioral or responsibility boundary.

## Related Documents
- `constitution/AI_RULES.md` §3.1 (Incremental Structural Hygiene)
- `architecture/rag/MEASURED_PERFORMANCE.md`
- `ci/ARCHITECTURE_GATES.md` Gate A5
