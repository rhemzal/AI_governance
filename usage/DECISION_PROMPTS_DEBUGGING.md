# Decision Prompts — Debugging

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Copy-paste prompts for AI assistants to propose debugging strategies with explicit trade-offs, scope, assumptions, risks, verification steps, and PR-ready evidence.

This document is **advisory**. Normative rules remain in `constitution/` and `ci/`.

## How to use

1. Paste the relevant prompt below at the start of a troubleshooting task.
2. Add `constitution/AI_ENFORCEMENT_DAILY.md` for LOW-risk work or `constitution/AI_ENFORCEMENT.md` for HIGH-risk work.
3. Point the assistant at `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md` for pattern IDs and schemas.
4. Require the **Evidence output** section in every response.

---

## Prompt 1 — Strategy selection (pros/cons first)

Use when you know the symptom but not the best debugging approach.

```
Load usage/DEBUGGING_EFFECTIVENESS_CATALOG.md and usage/DEBUGGING_ACCELERATION_PLAYBOOK.md.

Task: Propose debugging strategy options for the issue below.

Issue:
<PASTE SYMPTOM, ERROR, OR TEST FAILURE>

Requirements:
1. Risk preflight: LOW or HIGH (justify). If HIGH or unclear, STOP before implementation.
2. Recommend the top 2–3 patterns from the catalog with:
   - Pattern ID and name
   - Problem fit (why it applies here)
   - Pros and cons
   - Do NOT use when (for this case)
   - Implementation cost (setup/maintenance)
3. State your recommended option and why.
4. Scope: smallest useful verification first (constitution/AI_ENFORCEMENT_DAILY.md).
5. Assumptions: list what you are inferring about the system.
6. Risks: false positives, blind spots, high-risk triggers (boundaries, contracts, security).
7. Verification steps: ordered, non-interactive commands where possible (AI_RULES §6.2).
8. Evidence output (mandatory):

### Evidence output
```text
DEBUGGING STRATEGY SELECTION
- Symptom:
- Risk: LOW|HIGH
- Options considered (2-3):
  1) <ID> — pros: ... | cons: ...
  2) <ID> — pros: ... | cons: ...
  3) <ID> — pros: ... | cons: ...
- Recommendation:
- Scope (smallest useful):
- Assumptions:
- Risks:
- Verification steps:
- STOP/confirm needed: yes/no
```
```

---

## Prompt 2 — Long-running playback issue

Use for video, audio, streaming, buffer, seek, or playlist defects.

```
Load usage/DEBUGGING_EFFECTIVENESS_CATALOG.md (DBG-media-01, DBG-media-02, DBG-io-01, DBG-contract-01)
and usage/DEBUGGING_ACCELERATION_PLAYBOOK.md (Long-running video / playback section).

Task: Debug this long-running or playback-related issue.

Issue:
<PASTE SYMPTOM — e.g. stall after N minutes, seek failure, buffer underrun>

Requirements:
1. Split decoder/GPU-dependent layers from transport/pipeline layers.
2. Propose speed-up simulation or synthetic traffic where applicable (DBG-media-02).
3. Propose deterministic fixtures (short clips, manifest snapshots) — repo-local, redacted.
4. Scope: identify the lowest layer that can reproduce the failure.
5. Assumptions: clock, codec, network, CDN, device dependencies.
6. Risks: acceleration false confidence; over-mocking; asset/license issues.
7. Verification steps: per-layer commands; one real-time check if timing-critical.
8. If HIGH risk (contract/API/error model): STOP and flag ADR need.
9. Evidence output (mandatory):

### Evidence output
```text
PLAYBACK DEBUG PLAN
- Failing layer: transport | decoder/GPU | UI | unknown
- Layer isolation plan:
- Acceleration/simulation:
- Fixtures:
- Scope (smallest useful):
- Assumptions:
- Risks:
- Verification steps:
- Pattern IDs used:
- ADR required: yes/no
```
```

---

## Prompt 3 — MCP diagnostic setup

Use when debugging through Model Context Protocol tools or proposing new diagnostic MCP surfaces.

```
Load usage/DEBUGGING_EFFECTIVENESS_CATALOG.md (DBG-mcp-01)
and usage/DEBUGGING_ACCELERATION_PLAYBOOK.md (MCP diagnostics section).

Task: Design or use MCP diagnostics for this integration issue.

Issue:
<PASTE SYMPTOM — e.g. tool timeout, wrong resource shape, agent cannot see state>

Requirements:
1. Treat MCP as integration-boundary adapter — not unconstrained shell access.
2. Default to read-only diagnostic tools; separate mutating tools explicitly.
3. Mutating actions: HIGH risk → STOP and request confirmation before implementation.
4. Security/data exposure: no secrets, PII, or full production dumps; redaction plan.
5. Scope: minimal tool surface to answer the diagnostic question.
6. Assumptions: existing MCP server capabilities and auth model.
7. Risks: data leak, accidental mutation, wrong boundary abstraction.
8. Verification steps: sample tool invocations (redacted output).
9. Evidence output (mandatory):

### Evidence output
```text
MCP DIAGNOSTIC PLAN
- Integration boundary:
- Read-only tools proposed/used:
- Mutating tools (if any) + guardrails:
- Scope:
- Assumptions:
- Risks (incl. data exposure):
- Verification steps:
- Redaction approach:
- HIGH risk / STOP: yes/no
```
```

---

## Prompt 4 — Flaky test triage

Use for intermittent CI or local test failures.

```
Load usage/DEBUGGING_EFFECTIVENESS_CATALOG.md (DBG-flake-01, DBG-reduce-01)
and usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md.
Normative policy: ci/TEST_GATES.md (quarantine over delete).

Task: Triage this flaky or intermittent test failure.

Failure:
<PASTE TEST NAME, LOG SNIPPET, FLAKE RATE IF KNOWN>

Requirements:
1. Classify: flake | deterministic | environment — with evidence.
2. Do NOT delete or weaken tests without justification.
3. Recommend fix vs quarantine per ci/TEST_GATES.md maturity level.
4. Apply minimal reproducible reduction (DBG-reduce-01) if repro is heavy.
5. Scope: single test or minimal suite slice.
6. Assumptions: CI image, parallelism, timing, shared state.
7. Risks: misclassification; permanent quarantine; masking product bugs.
8. Verification steps: multiple runs, isolation experiment, quarantine marker.
9. Evidence output (mandatory):

### Evidence output
```text
FLAKE TRIAGE REPORT
- Test scope:
- Classification: flake | deterministic | environment
- Evidence (runs, timestamps, correlation):
- Repro rate estimate:
- Reduction attempt:
- Recommended action: fix | quarantine | env stabilize
- Quarantine policy link:
- Assumptions:
- Risks:
- Verification steps:
- Product code change warranted: yes/no (justify)
```
```

---

## Prompt 5 — Minimal reproducible case

Use when reproduction steps are too large or noisy.

```
Load usage/DEBUGGING_EFFECTIVENESS_CATALOG.md (DBG-reduce-01)
and usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md.

Task: Reduce this failure to a minimal reproducible scenario.

Failure:
<PASTE FULL REPRO STEPS, LOGS, OR TEST>

Requirements:
1. Iteratively remove irrelevant services, steps, and data.
2. Preserve the failure signal — document each removed factor.
3. Output a minimal command, test, or script.
4. Propose a permanent regression test at minimal scope if appropriate.
5. Scope: smallest case that still fails (or clearly explains pass).
6. Assumptions: what environment state is still required.
7. Risks: oversimplification; hidden global state; wasted time if signal already minimal.
8. Verification steps: run minimal case before and after each reduction step.
9. Evidence output (mandatory):

### Evidence output
```text
MINIMAL REPRO CASE
- Original repro summary:
- Minimal repro (command/steps):
- Removed factors:
- Remaining dependencies:
- Scope:
- Assumptions:
- Risks:
- Verification steps:
- Regression test added: yes/no
- Working diagnosis (not RCA unless verified):
```
```

---

## Related Documents

- `usage/DEBUGGING_EFFECTIVENESS_CATALOG.md`
- `usage/DEBUGGING_ACCELERATION_PLAYBOOK.md`
- `usage/DEBUGGING_PATTERN_TEMPLATE.md`
- `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`
- `usage/HOW_TO_USE_WITH_COPILOT.md`
- `constitution/AI_ENFORCEMENT_DAILY.md`
- `constitution/AI_ENFORCEMENT.md`
- `ci/TEST_GATES.md`
