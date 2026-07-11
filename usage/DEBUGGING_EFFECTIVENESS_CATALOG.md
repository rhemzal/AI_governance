# Debugging Effectiveness Catalog

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Systematize **advisory** debugging and quality-improvement strategies for AI-assisted development.

Help AI assistants proactively propose suitable debugging paths with explicit trade-offs (pros/cons), fit criteria, verification steps, and PR evidence expectations.

## Non-goals

- This catalog does **not** replace normative rules in `constitution/` or CI gate definitions in `ci/`.
- This catalog does **not** mandate specific tools, frameworks, or test runners.
- This catalog does **not** authorize weakening tests, deleting failures, or bypassing high-risk enforcement.
- This catalog does **not** claim root cause analysis (RCA) without evidence — prefer **working diagnosis** during Autonomous Verification & Repair (AVR) loops.
- Scientific-style patterns (`DBG-science-*`) are advisory debugging workflows; they do **not** replace normative test policy in `ci/TEST_GATES.md`.

## How to use the catalog (selection flow)

```mermaid
flowchart TD
  A[Symptom observed] --> B{Risk preflight}
  B -->|LOW| C{Cause clear?}
  B -->|HIGH / boundary / contract| D[STOP: use AI_ENFORCEMENT.md + ADR if needed]
  D --> C
  C -->|no| T[Prompt 7 triage max 3 IDs]
  C -->|yes| E[One domain pattern from decision table]
  T --> E2{Scientific path?}
  E2 -->|yes| E3[Prompt 6: DBG-science-01 falsification]
  E2 -->|no| F[Pick smallest-scope verification first]
  E3 --> E4[Prediction-before-change DBG-science-02]
  E4 --> F
  E --> F
  F --> G[Run AVR loop with evidence]
  G --> H{Sufficient signal?}
  H -->|yes| I[Minimal fix + rerun]
  H -->|no| T
  I --> I2{Prediction matched?}
  I2 -->|no| T
  I2 -->|yes| Done[Done with evidence]
```

**Practical steps:**

1. Classify risk (daily vs high-risk mode per `constitution/AI_ENFORCEMENT_DAILY.md` / `constitution/AI_ENFORCEMENT.md`).
2. Describe the symptom domain (test failure, flake, performance, integration boundary, long-running media, MCP tool, etc.).
3. If cause is unclear or the first fix failed: run **Scientific method triage** (below) or `usage/DECISION_PROMPTS_DEBUGGING.md` **Prompt 7** — max **3** pattern IDs; do not scan the full catalog.
4. If cause is proven or trivial: pick **one** domain pattern from the triage decision table.
5. When scientific path applies: formulate competing hypotheses (`DBG-science-01`), falsify before fixing, then **prediction-before-change** (`DBG-science-02`).
6. Use copy-paste prompts from `usage/DECISION_PROMPTS_DEBUGGING.md` when working with an AI assistant.
7. Execute the smallest useful scope; capture **PR evidence** per pattern.
8. On verification failure, apply the AVR loop (`constitution/AI_ENFORCEMENT_DAILY.md`) before escalating.

For operational playbooks and checklists, see `usage/DEBUGGING_ACCELERATION_PLAYBOOK.md`.

New patterns: use `usage/DEBUGGING_PATTERN_TEMPLATE.md`.

When cause is unclear, run **Scientific method triage** (below) or `usage/DECISION_PROMPTS_DEBUGGING.md` Prompt 7 before listing patterns.

---

## Scientific method triage

Use this section to **pick methods, not fixes** — before applying the full catalog or scientific checklists.

Copy-paste triage: `usage/DECISION_PROMPTS_DEBUGGING.md` **Prompt 7**.

### Pattern budget (anti-overload)

| Tier | Patterns | Limit per issue |
|------|----------|-----------------|
| **Core** | `DBG-science-01` + `DBG-science-02` | Always when scientific path is active |
| **Supporting** | One of `DBG-science-03` … `DBG-science-07` | Max **1** per AVR iteration |
| **Domain** | e.g. `DBG-flake-01`, `DBG-media-*`, `DBG-contract-01` | Max **1** alongside supporting |
| **Total** | All tiers combined | Max **3** pattern IDs (including core) |

### Decision table (symptom → supporting method)

| Signal | Primary supporting | Often skip instead |
|--------|-------------------|-------------------|
| Unclear cause, multiple hypotheses | `DBG-science-04` or `DBG-science-05` | Listing all catalog patterns |
| Multiple factors (config, cache, flag) | `DBG-science-03` | Shotgun config changes |
| Regression / “used to work” | `DBG-science-06` + `DBG-reduce-01` bisect | Random revert commits |
| Suspect harness / CI / MCP / runner | `DBG-science-07` | Long product-code chase |
| Intermittent failure | `DBG-flake-01` (+ `DBG-science-06` replication) | Immediate product rewrite |
| Logs/traces available, few experiments left | `DBG-science-04` | `DBG-observe-01` without hypothesis |

### Science path depth

| Path | When | Steps |
|------|------|-------|
| **skip** | Clear stack trace, typo, proven cause | Domain pattern or direct fix only |
| **lite** | Unclear cause, simple context | `DBG-science-01` → `DBG-science-02` → fix (no supporting) |
| **full** | Unclear cause, multi-factor, regression, or first fix failed | Triage → core + **1** supporting → fix |

### Anti-overload rules (for AI assistants)

- Run triage **before** enumerating the full catalog.
- Never list all 17+ patterns — output max **3** IDs with justification.
- One AVR iteration = **one** supporting scientific pattern.
- If core (`01`+`02`) is sufficient, do **not** add supporting.
- State **methods NOT chosen** in one line each (prevents catalog dumps).

---

## Patterns

### Pattern 1: Layered diagnostic test pyramid (long-running media / streaming)

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-media-01` |
| **Maturity** | `proven` |

#### Problem fit
Failures in video/audio playback, live streaming, or chunked media pipelines where full end-to-end runs are slow, GPU-dependent, or non-deterministic across environments.

#### Use when
- Symptoms appear only after minutes of real-time playback or under specific buffer states.
- Decoder, transport, and UI layers are separable.
- You need faster feedback than a full user-session replay.

#### Do NOT use when
- The defect is clearly in a single pure function with no I/O (use unit tests instead).
- Layers cannot be isolated without changing production architecture (escalate to ADR-first).
- You have no stable contracts between layers.

#### Pros
- Orders-of-magnitude faster iteration on transport/parsing vs full playback.
- Localizes failures to a layer before expensive E2E runs.
- Aligns with boundary-respecting tests (`constitution/AI_RULES.md` §4).

#### Cons
- Requires upfront fixture and contract investment.
- May miss cross-layer timing bugs if upper layers are over-mocked.
- GPU/codec paths may still need a thin integration slice.

#### Failure modes
- Over-mocking hides real backpressure or clock skew.
- “Green” unit layers while E2E still fails — indicates missing contract probes.
- Chasing decoder bugs when transport reordering is the actual fault.

#### Expected gain
- **Speed:** 5–50× faster diagnosis on non-GPU layers.
- **Quality:** clearer ownership per layer; fewer shotgun fixes.

#### Implementation cost
- **Setup:** medium — layer contracts + fixture clips/streams.
- **Maintenance:** medium — update fixtures when wire format changes.

#### PR evidence expectations
- Pyramid diagram or bullet list of which layer failed.
- Commands for each layer (unit → contract → thin integration → optional E2E).
- Minimal artifact: failing assertion, buffer state dump, or segment index.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Rules / enforcement | `constitution/AI_RULES.md`, `constitution/AI_ENFORCEMENT_DAILY.md` | Tests respect boundaries; AVR on smallest layer |
| CI / test gates | `ci/TEST_GATES.md` | Deterministic headless layers run in CI; heavy E2E optional |
| Architecture | `architecture/README.md` | Split core vs integration boundary |

#### AI Prompt Snippet
```
Apply DBG-media-01: propose a 3–4 layer diagnostic pyramid for this streaming/playback issue.
Split decoder/GPU from transport/pipeline. List pros/cons per layer test. Smallest scope first.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-media-01
- Pattern: Layered diagnostic test pyramid
- Failing layer:
- Layer commands run:
- Signals captured:
- Working diagnosis:
- Rerun result:
```

---

### Pattern 2: Synthetic speed-up simulation (faster-than-real-time input)

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-media-02` |
| **Maturity** | `proven` |

#### Problem fit
Time-dependent bugs (buffer underrun, seek race, playlist advance) that require long wall-clock waits in production but can be driven with accelerated or synthetic timelines in tests.

#### Use when
- Logic depends on timestamps, segment boundaries, or paced delivery — not wall-clock UX polish alone.
- A test harness can inject frames/chunks faster than real time.
- You need to reach failure conditions in seconds instead of minutes.

#### Do NOT use when
- Bug is strictly real-time scheduling or OS/GPU vsync dependent.
- Acceleration changes ordering guarantees the production path relies on.
- No injectable clock or transport abstraction exists (consider ADR for testability).

#### Pros
- Dramatically shortens debug cycles for pacing and buffer logic.
- Enables property-style checks over many virtual timelines.
- Pairs well with DBG-media-01 (transport layer).

#### Cons
- Risk of false confidence if accelerated path diverges from production pacing.
- Requires explicit virtual clock or throttle bypass in test mode.
- May need separate “real-time smoke” for final validation.

#### Failure modes
- Tests pass at 100× speed but fail at 1× (missing real-time constraint).
- Hidden coupling to `sleep()` instead of clock injection.
- Flaky tests when acceleration races internal thread pools.

#### Expected gain
- **Speed:** 10–100× for buffer/seek/playlist defects.
- **Quality:** broader scenario coverage in CI time budget.

#### Implementation cost
- **Setup:** medium — virtual clock or fast-forward API.
- **Maintenance:** low–medium — keep acceleration flag out of production defaults.

#### PR evidence expectations
- Document acceleration factor and clock injection mechanism.
- Show failing scenario time vs equivalent real-time duration.
- One real-time or near-real-time confirmation run when risk is high.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Rules / enforcement | `constitution/AI_RULES.md` §6.2 | Non-interactive commands; timeouts on long runs |
| Test execution | `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` | Avoid manual sleeps; prefer framework waits |
| CI / test gates | `ci/TEST_GATES.md` | Accelerated tests must remain deterministic |

#### AI Prompt Snippet
```
Apply DBG-media-02: design a faster-than-real-time simulation for this time-dependent bug.
State assumptions about clock/pacing. List risks of acceleration vs production.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-media-02
- Acceleration factor:
- Virtual clock / injection point:
- Scenario duration (simulated vs real-time equivalent):
- Working diagnosis:
- Real-time confirmation (if run):
```

---

### Pattern 3: Record/replay harness

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-io-01` |
| **Maturity** | `proven` |

#### Problem fit
Intermittent or environment-specific failures at integration boundaries (HTTP, WebSocket, gRPC, file I/O) where live reproduction is costly or non-deterministic.

#### Use when
- A failing run can be captured once and replayed deterministically.
- External services are unstable or rate-limited.
- You need shareable evidence across developers and CI.

#### Do NOT use when
- Recorded traffic contains secrets or PII (redact first or use synthetic fixtures).
- Protocol is stateful in ways the recorder does not capture (partial sessions).
- Replay diverges due to time/nonce/auth — needs contract stubs instead.

#### Pros
- Stable reproduction across machines.
- Fast CI feedback without live dependencies.
- Excellent PR evidence (attach trace file).

#### Cons
- Fixture drift when API evolves.
- Large artifacts if not trimmed.
- Can hide “works only with this exact traffic” bugs.

#### Failure modes
- Stale cassettes mask regressions.
- Recording production data into the repo (security/compliance violation).
- Replay passes while live system fails (missing dynamic auth or clock).

#### Expected gain
- **Speed:** eliminates wait on external instability.
- **Quality:** reproducible bug reports and regression tests.

#### Implementation cost
- **Setup:** medium — recorder + storage convention (repo-local `.artifacts/` or fixtures).
- **Maintenance:** medium — refresh cassettes on contract change.

#### PR evidence expectations
- Path to replay fixture (redacted).
- Command that replays and fails before fix / passes after.
- Note on fixture scope (single request vs full session).

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Rules | `constitution/AI_RULES.md` §4 | Integration boundary tests |
| Security | `usage/SECURITY_MINIMUM_ADOPTION.md` | No secrets in fixtures |
| Copilot usage | `usage/HOW_TO_USE_WITH_COPILOT.md` | Repo-local artifact paths |

#### AI Prompt Snippet
```
Apply DBG-io-01: propose record/replay for this boundary failure. Require redaction plan and replay command.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-io-01
- Fixture path (redacted):
- Record command:
- Replay command:
- First failure signal on replay:
```

---

### Pattern 4: Deterministic fault injection (timeouts / reorder / partial failure)

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-resilience-01` |
| **Maturity** | `proven` |

#### Problem fit
Resilience bugs: hung requests, duplicate delivery, partial writes, retry storms, and ordering violations that rarely occur in happy-path tests.

#### Use when
- System has retries, circuit breakers, or idempotency requirements.
- You can inject faults at a boundary without mutating production code paths permanently.
- You need to verify error model behavior (`constitution/AI_ENFORCEMENT.md` when error model changes).

#### Do NOT use when
- Fault injection requires changing security behavior without review (high-risk).
- Production environment would be used for injection (use test harness only).
- Faults are not observable — no metrics/logs/assertions to verify response.

#### Pros
- Makes rare failures routine and testable.
- Validates error handling and recovery paths.
- Supports table-driven scenarios (timeout 0ms, 1ms, hang, 50% drop).

#### Cons
- Harness complexity.
- Risk of testing implementation details instead of contracts.
- Over-injection can lead to unrealistic failure combinations.

#### Failure modes
- Tests pass with injection but production failure mode differs.
- Injection point too low — misses real network behavior.
- Masking product bugs by loosening timeouts without justification.

#### Expected gain
- **Speed:** faster than waiting for natural failures.
- **Quality:** higher confidence in retry/idempotency contracts.

#### Implementation cost
- **Setup:** medium–high — fault shim at boundary.
- **Maintenance:** medium — update with protocol changes.

#### PR evidence expectations
- Matrix of injected faults vs expected outcomes.
- Logs/metrics showing detection and recovery.
- Explicit note if error model or public contract changed (ADR trigger).

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| High-risk | `constitution/AI_ENFORCEMENT.md` | Error model / contract changes |
| CI | `ci/TEST_GATES.md`, `ci/INTERFACE_GATES.md` | Contract tests for failure semantics |
| Terminology | `architecture/TERMINOLOGY_GLOSSARY.md` | RCA vs working diagnosis |

#### AI Prompt Snippet
```
Apply DBG-resilience-01: list deterministic faults to inject (timeout, reorder, partial failure).
Map each to expected behavior. Flag high-risk error-model changes.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-resilience-01
- Fault matrix:
- Injection point:
- Observed vs expected:
- Error model / ADR required: yes/no
```

---

### Pattern 5: MCP diagnostic adapter pattern (boundary-safe introspection)

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-mcp-01` |
| **Maturity** | `experimental` |

#### Problem fit
Debugging through Model Context Protocol (MCP) integrations where direct production introspection is unsafe, opaque, or crosses trust boundaries.

#### Use when
- MCP exposes an integration boundary (tools, resources, external systems).
- Read-only diagnostics can narrow failure domain without mutating state.
- Agents need structured introspection instead of ad-hoc shell access.

#### Do NOT use when
- MCP tool would expose secrets, PII, or unredacted production data.
- Mutating actions are required without explicit operator confirmation.
- Native repo-local commands suffice (prefer `DEVELOPMENT.md` / make targets first).

#### Pros
- Keeps diagnostics at declared integration boundary.
- Enables AI assistants to gather evidence within guardrails.
- Separates read-only diagnostic tools from write operations.

#### Cons
- MCP surface must be designed and maintained.
- Wrongly scoped tools increase attack surface.
- Extra indirection vs direct test harness.

#### Failure modes
- Diagnostic tool accidentally performs mutating side effects.
- Over-broad resource URIs leak data.
- Agents rely on MCP when unit tests would be faster.

#### Expected gain
- **Speed:** faster evidence gathering for integration issues.
- **Quality:** repeatable, boundary-aligned introspection.

#### Implementation cost
- **Setup:** medium — read-only MCP tools + auth scoping.
- **Maintenance:** medium — version with API changes.

#### PR evidence expectations
- List of diagnostic MCP tools (read-only default).
- Sample tool invocation output (redacted).
- Mutating-action guardrail statement.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Terminology | `architecture/TERMINOLOGY_GLOSSARY.md` | MCP definition |
| Security | `usage/SECURITY_MINIMUM_ADOPTION.md` | Data exposure cautions |
| Architecture | `architecture/README.md` | Adapter at integration boundary |
| High-risk | `constitution/AI_ENFORCEMENT.md` | Interface / security behavior changes |

#### AI Prompt Snippet
```
Apply DBG-mcp-01: propose read-only MCP diagnostic tools for this integration.
Separate mutating actions. List data exposure risks and verification steps.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-mcp-01
- Diagnostic tools (read-only):
- Sample output (redacted):
- Mutating tools (if any) + guardrails:
- Verification:
```

---

### Pattern 6: Contract-first boundary probes

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-contract-01` |
| **Maturity** | `standard` |

#### Problem fit
Failures at integration boundaries where teams debate whether the bug is “ours” or “theirs” — HTTP schemas, event payloads, CLI output, adapter interfaces.

#### Use when
- A machine-readable contract exists or should exist (OpenAPI, JSON Schema, protobuf).
- You can fail fast on schema/status semantics before deep E2E.
- Boundary change is suspected (check high-risk triggers).

#### Do NOT use when
- No stable contract — define ADR + contract first.
- Probe duplicates an existing comprehensive test without narrowing scope.
- Contract checks are swapped for behavioral tests entirely.

#### Pros
- Fast, deterministic signal at the boundary.
- Clear PR evidence (schema diff, validation error).
- Prevents architecture drift (`ci/ARCHITECTURE_GATES.md`).

#### Cons
- Schema maintenance overhead.
- May pass contract but fail user-visible behavior.
- False precision if schemas are too loose.

#### Failure modes
- Chasing adapter code when contract was wrong.
- Weakening schema to greenwash tests.
- Missing versioning strategy for evolving contracts.

#### Expected gain
- **Speed:** minutes to isolate boundary mismatch.
- **Quality:** enforces explicit integration contracts.

#### Implementation cost
- **Setup:** low–medium — schema + probe test.
- **Maintenance:** medium — version with API evolution.

#### PR evidence expectations
- Failing validation message or contract diff.
- Probe command and smallest payload that fails.
- ADR link if contract semantics changed.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Rules | `constitution/AI_RULES.md` §4 | Integration boundary tests |
| CI | `ci/INTERFACE_GATES.md`, `ci/ARCHITECTURE_GATES.md` | Contract gates |
| High-risk | `constitution/AI_ENFORCEMENT.md` | Public contract changes |

#### AI Prompt Snippet
```
Apply DBG-contract-01: define the smallest contract probe for this boundary failure.
Include schema/status checks before E2E.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-contract-01
- Contract artifact:
- Probe command:
- Validation failure:
- Boundary owner (us/them/integration):
```

---

### Pattern 7: Golden / snapshot checks (stable machine-readable behavior)

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-snapshot-01` |
| **Maturity** | `proven` |

#### Problem fit
Regressions in stable, machine-readable outputs: CLI JSON, serialized configs, API response shapes, DOM accessibility trees, rendered markdown AST.

#### Use when
- Output format is intentionally stable and versioned.
- Human review of diffs is easier than hand-written assertions for large structures.
- Behavior is deterministic in CI.

#### Do NOT use when
- Output includes timestamps, random IDs, or environment-specific paths without normalization.
- Snapshot replaces semantic assertions for critical business rules.
- AI proposes vague snapshots to hide failures (`usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`).

#### Pros
- High signal for unintended output drift.
- Fast to add once harness exists.
- Excellent PR diff evidence.

#### Cons
- Snapshot churn on cosmetic changes.
- Review fatigue if snapshots are huge.
- Can encode bugs if updated blindly.

#### Failure modes
- Bulk snapshot update without understanding diffs.
- Non-deterministic snapshots → false flakes.
- Testing implementation details instead of user-visible contracts.

#### Expected gain
- **Speed:** quick regression detection on next change.
- **Quality:** prevents silent format breakage.

#### Implementation cost
- **Setup:** low–medium — normalizer + snapshot path.
- **Maintenance:** medium — disciplined update workflow.

#### PR evidence expectations
- Snapshot diff with intentional change called out.
- Normalization rules documented.
- Link to contract/version policy if output is public.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Test diagnostics | `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` | Do not weaken assertions |
| CI | `ci/INTERFACE_GATES.md` | DOM/a11y snapshot mentions |
| Interface | `interface/INTERFACE_RULES_PROPOSAL.md` | Stable automation-first output |

#### AI Prompt Snippet
```
Apply DBG-snapshot-01: propose golden/snapshot checks with normalization rules.
Warn if output is non-deterministic. Prefer semantic asserts for business rules.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-snapshot-01
- Snapshot path:
- Normalization applied:
- Diff summary:
- Intentional vs accidental drift:
```

---

### Pattern 8: Flakiness triage and quarantine loop

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-flake-01` |
| **Maturity** | `standard` |

#### Problem fit
Non-reproducible test failures, order-dependent tests, timing-sensitive UI tests, and CI noise that blocks progress.

#### Use when
- Failure is intermittent or environment-correlated.
- Same commit passes on rerun without code changes.
- Flakiness budget policy applies (`ci/TEST_GATES.md`).

#### Do NOT use when
- Failure is deterministic (use AVR on product/test code).
- Quarantine would hide a real regression without tracking.
- Default response is delete or weaken the test.

#### Pros
- Restores CI trust while root cause is investigated.
- Forces explicit flake tracking and ownership.
- Aligns with progressive CI maturity levels.

#### Cons
- Quarantined tests reduce coverage until fixed.
- Teams may leave tests quarantined indefinitely.
- Triage overhead.

#### Failure modes
- Misclassifying deterministic bug as flake.
- Permanent quarantine without ticket/policy.
- Retry loops that mask systemic timing bugs.

#### Expected gain
- **Speed:** unblocks merge path while investigating.
- **Quality:** long-term suite determinism when loop is closed.

#### Implementation cost
- **Setup:** low — quarantine tag + tracking convention.
- **Maintenance:** ongoing triage cadence.

#### PR evidence expectations
- Flake classification rationale (evidence from multiple runs).
- Quarantine marker or issue link.
- Plan: fix, stabilize environment, or remove quarantine.
- **Replication follow-up:** when classification is uncertain, run clean-env or second-machine reproduction (`DBG-science-06` control runs) before broad code changes.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| CI | `ci/TEST_GATES.md` | Quarantine over delete; flake windows |
| Test diagnostics | `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` | Flaky vs deterministic |
| Daily enforcement | `constitution/AI_ENFORCEMENT_DAILY.md` | Do not hide failures |

#### AI Prompt Snippet
```
Apply DBG-flake-01: triage this intermittent failure. Evidence from multiple runs.
Recommend fix vs quarantine per ci/TEST_GATES.md. Do not delete or weaken without justification.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-flake-01
- Classification: flake | deterministic | environment
- Repro rate:
- Runs observed:
- Quarantine action:
- Fix plan:
```

---

### Pattern 9: Minimal reproducible scenario reduction

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-reduce-01` |
| **Maturity** | `standard` |

#### Problem fit
Complex failures with large reproduction steps (multi-service, long scripts, full app navigation) where cause is unknown.

#### Use when
- A failure exists but scope is too large for efficient AVR loops.
- You need a shareable minimal case for reviewers or AI assistants.
- Bisection or delta debugging is next step.

#### Do NOT use when
- Smallest scope is already known (run it immediately).
- Reduction removes the conditions that trigger the bug.
- Spending reduction time exceeds fixing obvious signal.

#### Pros
- Faster diagnosis and review.
- Smaller tests added as regression guards.
- Better AI assistant prompts (less noise).

#### Cons
- Time upfront before fixing.
- Risk of oversimplification missing interaction bugs.
- May require multiple reduction iterations.

#### Failure modes
- “Minimal” case still depends on hidden global state.
- Reduced case passes while full scenario fails (incomplete reduction).
- Endless reduction without hypothesis (use `DBG-science-01` first).

#### Expected gain
- **Speed:** shorter AVR cycles after reduction.
- **Quality:** durable regression test from minimal case.

#### Implementation cost
- **Setup:** low — systematic halving/bisection discipline.
- **Maintenance:** low — minimal case becomes permanent test.

#### PR evidence expectations
- Before/after reproduction steps.
- Minimal command or test case added.
- List of removed irrelevant factors.

**Regression bisect (extension):** when failure is a regression, use `git bisect` (or equivalent) on commits between last-good and first-bad. Pair with `DBG-science-06` control runs (known-good vs failing commit). Document bisect command and introducing commit in PR evidence.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Daily enforcement | `constitution/AI_ENFORCEMENT_DAILY.md` | Smallest useful scope |
| Test diagnostics | `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` | Evidence before repair |
| AEP | `usage/AEP_VALIDATION.md` | Multi-file fixes after reduction |

#### AI Prompt Snippet
```
Apply DBG-reduce-01: reduce this failure to the smallest reproducible scenario.
Document each removed factor. Output minimal command/test.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-reduce-01
- Original repro:
- Minimal repro:
- Removed factors:
- Minimal test added: yes/no
```

---

### Pattern 10: Observability-first debugging pack (logs / metrics / traces)

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-observe-01` |
| **Maturity** | `proven` |

#### Problem fit
Production-like or integrated failures where symptom is clear but internal path is opaque — latency spikes, silent drops, partial errors, distributed traces.

#### Use when
- Structured logs, metrics, or traces exist or can be added at low risk.
- Failure is not easily reachable via unit test alone.
- You need correlation IDs across components.

#### Do NOT use when
- Logging would expose secrets without redaction.
- High-cardinality metrics would be added without review in production.
- Observability becomes substitute for deterministic tests.

#### Pros
- Reveals actual runtime path vs assumed path.
- Supports post-incident evidence.
- Narrows which layer/pattern to apply next.

#### Cons
- Noise without filtering discipline.
- Setup cost for tracing across services.
- Risk of PII/secrets in logs.

#### Failure modes
- Log archaeology without hypothesis (slow; pair with `DBG-science-01`).
- Missing correlation → inconclusive traces.
- Over-instrumentation in hot paths.

#### Expected gain
- **Speed:** faster localization when signals are good.
- **Quality:** evidence-backed working diagnosis.

#### Implementation cost
- **Setup:** low–high depending on existing stack.
- **Maintenance:** medium — dashboards/alerts optional.

#### PR evidence expectations
- Log/trace slice with correlation ID.
- Metric or span that pinpoints failure segment.
- Redaction confirmation for sensitive fields.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Test diagnostics | `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` | Prefer live detection; minimal evidence |
| Security | `usage/SECURITY_MINIMUM_ADOPTION.md` | No secrets in logs |
| Rules | `constitution/AI_RULES.md` §6.2 | Non-interactive collection where possible |

#### AI Prompt Snippet
```
Apply DBG-observe-01: list logs/metrics/traces to enable for this failure.
Propose correlation strategy. Redact secrets. Smallest signal before full log dump.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-observe-01
- Signals enabled:
- Correlation ID:
- Key log/trace slice (redacted):
- Working diagnosis:
```

---

### Pattern 11: Competing hypotheses + falsification loop

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-science-01` |
| **Maturity** | `standard` |

#### Problem fit
Unclear root cause with multiple plausible explanations; risk of implementing the first guess and discovering during implementation that it solves nothing.

#### Use when
- Symptom is reproducible but cause is unknown.
- AI or human shows tendency to jump straight to code changes.
- Several competing explanations exist (layer, config, timing, contract).

#### Do NOT use when
- Cause is already proven (e.g., clear stack trace to a single line).
- Trivial syntax/typo with obvious fix.
- HIGH-risk change without STOP gate and operator confirmation.

#### Pros
- Cheaper than blind fix-and-retry loops.
- Reduces confirmation bias (`architecture/TERMINOLOGY_GLOSSARY.md`).
- Produces evidence-backed working diagnosis before repair.

#### Cons
- Requires discipline; can slow obvious fixes.
- Poorly formed hypotheses waste cycles.
- Falsification tests can accidentally become fixes.

#### Failure modes
- Hypotheses too vague to falsify.
- Tests designed to confirm rather than disprove.
- Too many hypotheses at once; analysis paralysis.
- Treating surviving hypothesis as verified RCA without evidence.

#### Expected gain
- **Speed:** faster overall when first-guess fixes would fail.
- **Quality:** fewer false-green fixes and regression churn.

#### Implementation cost
- **Setup:** low — structured thinking + cheapest probe per hypothesis.
- **Maintenance:** low — reusable habit in AVR loops.

#### PR evidence expectations
- List of 2–3 competing working hypotheses.
- Falsification test per hypothesis and outcome (falsified / survived).
- Explicit note if fix was deferred pending falsification.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Rules / enforcement | `constitution/AI_ENFORCEMENT_DAILY.md` | AVR loop; smallest scope |
| Terminology | `architecture/TERMINOLOGY_GLOSSARY.md` | working hypothesis, falsification test, RCA vs working diagnosis |
| Test execution | `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` | Evidence before repair |

#### AI Prompt Snippet
```
Apply DBG-science-01: list 2-3 competing working hypotheses.
For each, propose the cheapest falsification test (not a product fix).
Do not implement a fix until a hypothesis survives at least one falsification round.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-science-01
- Competing hypotheses:
- Falsification tests and outcomes:
- Surviving hypothesis (if any):
- Fix deferred: yes/no
- Working diagnosis (not RCA unless verified):
```

---

### Pattern 12: Prediction-before-change (pre-registered outcome)

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-science-02` |
| **Maturity** | `standard` |

#### Problem fit
A working hypothesis has survived falsification; a code change is imminent; risk of false green (tests pass for the wrong reason).

#### Use when
- About to edit production or test code to address a diagnosed issue.
- Expected observable signal can be stated in advance.
- Surviving hypothesis from `DBG-science-01` needs verification via change.

#### Do NOT use when
- Change is documentation-only.
- Change is an explicit throwaway spike on a discard branch.
- Cause is unproven and falsification has not been attempted.

#### Pros
- Catches wrong fixes early; enables rollback.
- Makes AI/human reasoning auditable in PRs.
- Pairs naturally with AVR rerun steps.

#### Cons
- Extra step before edit; can feel bureaucratic for trivial fixes.
- Predictions may be vague if signals are poorly chosen.
- Requires honesty when prediction fails (revert, don't rationalize).

#### Failure modes
- Vague prediction (“should work”) that cannot fail.
- Ignoring prediction mismatch because tests turned green.
- Post-hoc rewriting of what was predicted.

#### Expected gain
- **Speed:** avoids long rework after wrong fixes.
- **Quality:** higher confidence that fix addresses the actual cause.

#### Implementation cost
- **Setup:** low — one sentence before each edit.
- **Maintenance:** low.

#### PR evidence expectations
- Pre-registered prediction: “If H, after X we will see Y.”
- Actual outcome vs prediction.
- Revert noted if prediction failed.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Test execution | `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` | Evidence before repair |
| Terminology | `architecture/TERMINOLOGY_GLOSSARY.md` | prediction-before-change |
| Daily enforcement | `constitution/AI_ENFORCEMENT_DAILY.md` | Minimal compliant repair |

#### AI Prompt Snippet
```
Apply DBG-science-02: before any code edit, state prediction-before-change.
If actual outcome ≠ prediction, revert and reject the hypothesis.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-science-02
- Hypothesis:
- Prediction (before change):
- Change made:
- Actual outcome:
- Prediction matched: yes/no
- Action if no: revert / new hypothesis
```

---

### Pattern 13: Controlled ablation (one-variable isolation)

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-science-03` |
| **Maturity** | `proven` |

#### Problem fit
Multi-factor environments where failure depends on an unknown subset of variables (config, cache, adapter, parallelism, feature flags).

#### Use when
- One factor at a time can be disabled, mocked, or reverted in a test harness.
- Goal is to falsify “factor A is necessary for the failure.”
- Competing hypotheses map to different factors.
- A numeric threshold may exist (timeout, buffer size) — use **continuous parameter sweep** on one variable before multi-factor ablation.

#### Do NOT use when
- Ablation would change production behavior without a harness.
- Isolation requires architecture change without ADR.
- Factors cannot be separated (tightly coupled monolith with no seams).

#### Pros
- Systematic causal narrowing.
- Complements `DBG-science-01` with concrete experiments.
- Often faster than full rewrites.

#### Cons
- Interaction effects may require multi-factor follow-up.
- Ablation setup can be non-trivial.
- May miss emergent bugs visible only when all factors are active.

#### Failure modes
- Ablation order biases conclusion (fix one symptom, hide another).
- Disabling factor changes timing and masks race.
- Confusing ablation (causal factor) with layer split (`DBG-media-01`, architectural layers).

#### Expected gain
- **Speed:** faster than shotgun fixes across all factors.
- **Quality:** identifies necessary vs incidental factors.

#### Implementation cost
- **Setup:** low–medium — toggles, stubs, or config matrix.
- **Maintenance:** low — document which ablations are safe in CI.

#### PR evidence expectations
- Ablation matrix: factor × on/off × outcome.
- Which factors are necessary for reproduction.
- Harness note (not production mutation).

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Rules | `constitution/AI_RULES.md` §4 | Boundary-respecting isolation |
| High-risk | `constitution/AI_ENFORCEMENT.md` | ADR if ablation needs new seams |
| Catalog | `DBG-media-01` | Layers vs causal factors — different axes |

#### AI Prompt Snippet
```
Apply DBG-science-03: propose one-variable ablations to falsify which factors are necessary for the failure.
Use harness/toggles only; do not mutate production without gates.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-science-03
- Factors tested:
- Ablation matrix (factor / on-off / outcome):
- Necessary factors for failure:
- Harness vs production:
```

---

### Pattern 14: Differential diagnosis matrix

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-science-04` |
| **Maturity** | `standard` |

#### Problem fit
Multiple competing hypotheses and existing observations (logs, traces, test output) — need structured elimination without implementing fixes.

#### Use when
- 2–3 hypotheses are plausible and some signals are already available.
- Few experiments remain; matrix helps prioritize the highest-information test next.
- Complements `DBG-science-01` (falsification) with parallel symptom–hypothesis mapping.

#### Do NOT use when
- No observations yet — gather minimal evidence first (`DBG-observe-01` with hypothesis).
- Single obvious hypothesis — use lite science path (`01`+`02` only).
- Matrix becomes a catalog dump — violates pattern budget.

#### Pros
- Reduces shotgun debugging; focuses next experiment.
- Works well with existing telemetry before new code changes.
- Clear PR artifact (matrix with eliminated rows).

#### Cons
- Upfront structuring time.
- Wrong expected signals in matrix mislead elimination.
- Can duplicate work if hypotheses are poorly stated.

#### Failure modes
- Matrix too large (more than 3 hypotheses).
- Treating elimination as verified RCA.
- Filling matrix post-hoc after fix (confirmation bias).

#### Expected gain
- **Speed:** faster choice of next falsification test.
- **Quality:** auditable elimination trail.

#### Implementation cost
- **Setup:** low — table on paper or in PR comment.
- **Maintenance:** none.

#### PR evidence expectations
- Matrix: hypothesis × expected signal × observed? (yes/no/unknown).
- Rows eliminated and why.
- Next recommended falsification test.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Terminology | `architecture/TERMINOLOGY_GLOSSARY.md` | differential diagnosis (debugging) |
| Scientific core | `DBG-science-01` | Matrix feeds falsification loop |
| Anti-overload | This section | Max 3 hypotheses in matrix |

#### AI Prompt Snippet
```
Apply DBG-science-04: build a differential diagnosis matrix (max 3 hypotheses).
Mark eliminated rows from observations. Propose ONE next falsification test.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-science-04
- Matrix (H × expected signal × observed):
- Eliminated hypotheses:
- Surviving hypotheses:
- Next falsification test:
```

---

### Pattern 15: Discriminative experiment

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-science-05` |
| **Maturity** | `standard` |

#### Problem fit
Several hypotheses remain plausible; sequential one-by-one falsification would take many AVR iterations.

#### Use when
- One experiment can produce **different outcomes** under H1 vs H2 vs H3.
- Test cost is still cheaper than implementing multiple fixes.
- Strong-inference style: maximize information per run.

#### Do NOT use when
- Hypotheses predict identical outcomes for any feasible test.
- Experiment is really a product fix in disguise.
- HIGH-risk change without STOP gates.

#### Pros
- Fewer AVR rounds than sequential falsification.
- Forces precise, competing predictions.
- Good pairing with `DBG-science-04` matrix.

#### Cons
- Harder to design than single-hypothesis tests.
- Wrong discriminator eliminates all hypotheses incorrectly.
- May need follow-up if outcomes are ambiguous.

#### Failure modes
- Discriminator correlates with all hypotheses (inconclusive).
- Outcome interpreted to favor first guess (confirmation bias).
- Over-engineered experiment vs simplest probe.

#### Expected gain
- **Speed:** 1 test instead of N sequential tests when design is good.
- **Quality:** sharper hypothesis separation.

#### Implementation cost
- **Setup:** low–medium — design table H1/H2/H3 → predicted outcomes.
- **Maintenance:** low.

#### PR evidence expectations
- Discriminator description and predicted outcome per hypothesis.
- Actual outcome and which hypotheses eliminated.
- Follow-up test if inconclusive.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Terminology | `architecture/TERMINOLOGY_GLOSSARY.md` | discriminative experiment |
| Scientific core | `DBG-science-01` | One round of strong inference |
| Pattern budget | Scientific method triage | Counts as supporting tier |

#### AI Prompt Snippet
```
Apply DBG-science-05: design ONE discriminative experiment for H1/H2/H3.
State predicted outcome per hypothesis before running. Do not implement fixes yet.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-science-05
- Hypotheses:
- Discriminator experiment:
- Predicted outcomes (H1/H2/H3):
- Actual outcome:
- Eliminated:
```

---

### Pattern 16: Control runs (positive/negative)

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-science-06` |
| **Maturity** | `proven` |

#### Problem fit
Uncertainty whether the system is broadly broken vs a specific regression; need baseline comparison.

#### Use when
- Known-good case exists (last release, main branch, golden fixture).
- “Used to work” regression suspected.
- Replication needed: same repro on clean env / second CI job / fresh checkout.

#### Do NOT use when
- No valid positive control (never worked in this config).
- Controls differ in more than one uncontrolled variable.
- Production comparison without harness and approval.

#### Pros
- Separates environmental failure from code regression.
- Cheap falsification: “not a product bug” if control also fails.
- Supports flake vs real bug (`DBG-flake-01` follow-up).

#### Cons
- Finding a true positive control can be hard.
- Control drift (stale baseline) misleads.
- Extra CI time for replication runs.

#### Failure modes
- Apples-to-oranges comparison (different config/data).
- Control passes for wrong reason (weaker assertion).
- Skipping replication when flake is suspected.

#### Expected gain
- **Speed:** fast narrow to diff/regression vs environment.
- **Quality:** strong evidence for bisect and PR narrative.

#### Implementation cost
- **Setup:** low — identify good/bad pair.
- **Maintenance:** low — refresh baselines when contracts change.

#### PR evidence expectations
- Positive control command + outcome.
- Negative (failing) command + outcome.
- Replication run(s) if intermittent.
- Diff or commit range if regression.

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| Reduce / bisect | `DBG-reduce-01` | Regression bisect extension |
| Flake | `DBG-flake-01` | Replication before product changes |
| Terminology | `architecture/TERMINOLOGY_GLOSSARY.md` | control run |

#### AI Prompt Snippet
```
Apply DBG-science-06: run positive and negative control. If intermittent, replicate on clean env.
Compare outcomes before product fixes.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-science-06
- Positive control:
- Negative control:
- Replication runs:
- Conclusion (regression | environment | inconclusive):
```

---

### Pattern 17: Instrument sanity check

| Field | Value |
|-------|-------|
| **Pattern ID** | `DBG-science-07` |
| **Maturity** | `standard` |

#### Problem fit
Diagnostics disagree with reality; suspect test runner, MCP tool, mock, log pipeline, or CI image — not product code.

#### Use when
- Harness passes trivial smoke but fails on real scenario (or inverse).
- MCP diagnostic or test tool recently changed.
- Long product investigation with no signal — verify tooling first.

#### Do NOT use when
- Instrument is known good and recently verified.
- Sanity check would take longer than obvious product signal.
- Mutating production to test instrumentation.

#### Pros
- Avoids expensive wrong-layer fixes.
- Fast smoke: known-good micro-case through same tool path.
- Pairs with `DBG-mcp-01` (read-only diagnostics after sanity).

#### Cons
- Easy to over-use and delay real diagnosis.
- Trivial smoke may not exercise broken path.
- Extra setup for isolated harness verification.

#### Failure modes
- Sanity test too shallow (always passes).
- Blaming CI forever while product bug persists.
- Instrument “fixed” by weakening assertions.

#### Expected gain
- **Speed:** saves hours when harness is the fault.
- **Quality:** correct layer ownership.

#### Implementation cost
- **Setup:** low — one minimal command through instrument.
- **Maintenance:** low.

#### PR evidence expectations
- Instrument under test (runner, MCP, mock, CI job).
- Sanity command + expected vs actual.
- Product investigation resumed only after sanity passes (or instrument fix merged).

#### Governance Alignment

| Kit area | Relevant doc(s) | Alignment note |
|----------|-----------------|----------------|
| MCP | `DBG-mcp-01` | Sanity before broad MCP conclusions |
| Test execution | `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md` | Repo-local verification path |
| Pattern budget | Supporting tier | One per iteration |

#### AI Prompt Snippet
```
Apply DBG-science-07: verify the diagnostic instrument with a trivial known-good case.
If sanity fails, fix harness before product code.
```

#### Evidence Block (for PR)
```text
DEBUGGING PATTERN EVIDENCE — DBG-science-07
- Instrument:
- Sanity command:
- Expected vs actual:
- Proceed to product diagnosis: yes/no
```

---

## Pattern index (quick reference)

| ID | Pattern | Primary gain |
|----|---------|--------------|
| `DBG-media-01` | Layered diagnostic test pyramid | Layer isolation for streaming/media |
| `DBG-media-02` | Synthetic speed-up simulation | Fast time-dependent iteration |
| `DBG-io-01` | Record/replay harness | Deterministic boundary reproduction |
| `DBG-resilience-01` | Deterministic fault injection | Resilience / error-path coverage |
| `DBG-mcp-01` | MCP diagnostic adapter | Boundary-safe agent introspection |
| `DBG-contract-01` | Contract-first boundary probes | Fast schema/contract failures |
| `DBG-snapshot-01` | Golden/snapshot checks | Stable output regression guard |
| `DBG-flake-01` | Flakiness triage & quarantine | CI trust during flake investigation |
| `DBG-reduce-01` | Minimal reproducible reduction | Smaller AVR scope |
| `DBG-observe-01` | Observability-first pack | Runtime path evidence |
| `DBG-science-01` | Competing hypotheses + falsification loop | Disprove before implement |
| `DBG-science-02` | Prediction-before-change | Catch false-green fixes |
| `DBG-science-03` | Controlled ablation | Isolate necessary factors |
| `DBG-science-04` | Differential diagnosis matrix | Structured hypothesis elimination |
| `DBG-science-05` | Discriminative experiment | One test, multiple hypotheses |
| `DBG-science-06` | Control runs | Baseline + replication |
| `DBG-science-07` | Instrument sanity check | Verify harness before product chase |

---

## Related Documents

- `usage/DEBUGGING_PATTERN_TEMPLATE.md`
- `usage/DEBUGGING_ACCELERATION_PLAYBOOK.md`
- `usage/DECISION_PROMPTS_DEBUGGING.md`
- `usage/AI_TEST_EXECUTION_AND_DIAGNOSTICS.md`
- `usage/AI_RUN_EVIDENCE.md`
- `usage/AEP_VALIDATION.md`
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT_DAILY.md`
- `constitution/AI_ENFORCEMENT.md`
- `ci/TEST_GATES.md`
- `ci/INTERFACE_GATES.md`
- `architecture/TERMINOLOGY_GLOSSARY.md`
- `README.md`
