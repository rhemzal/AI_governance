# AI Tool Optimization (Advisory)

## Purpose
Provide a structured way to optimize AI-assisted workflows without turning tooling into governance.

## Non-Goals
- This does not change the rules in `constitution/`.
- This does not mandate a specific model/vendor.

## Protocol Overview
1. Define target tasks (use `tooling/BENCHMARK_SCENARIOS.md`).
2. Define evaluation criteria:
   - correctness (tests passing)
   - rule compliance (constitution + enforcement)
   - time-to-merge
   - diff size (avoid churn)
3. Run controlled trials:
   - same prompt
   - same codebase state
   - same success criteria
4. Record results and decide.

## Output Template
- Tooling configuration:
- Scenario:
- Success criteria:
- Result summary:
- Failures observed:
- Recommendation:

## Related Documents
- `adr/ADR_0004_Tooling_Is_Experimental.md`
- `tooling/BENCHMARK_SCENARIOS.md`
- `constitution/AI_RULES.md` and `constitution/AI_ENFORCEMENT.md`

## Optional: External Priors for Planning (As of 2025-12-28)
This section is **optional** and exists to support planning conversations.

Rules:
- These are not governance requirements.
- Do not treat them as facts; treat them as *assumptions to validate*.
- Prefer calibrating on your own repo using the benchmarks in this folder.

### What You May Assume (Qualitative)
- AI often reduces “typing time”, but may increase iteration/review time if boundaries and tests are weak.
- The biggest time sink in AI-heavy development is often **rework loops** (`T_fixups`), not initial code generation.
- Strong tests and deterministic design reduce total cost more than “better prompts” alone.

### How to Use Priors Safely
1. Start with a conservative estimate range (wide uncertainty band).
2. Run 3–10 benchmark scenarios on the real repo.
3. Replace priors with measured medians and variability.

### Planning Template (Priors → Measurements)
- Prior assumptions (qualitative):
- Prior uncertainty band: wide / medium / narrow
- Measurements collected (links to runs):
- Updated planning band:

