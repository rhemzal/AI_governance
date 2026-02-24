# External Project Evaluations (Research, Advisory)

_Provenance: This research note was added to the AI_governance kit (https://github.com/rhemzal/AI_governance)._

## Purpose

This document records structured evaluations of external projects considered for adoption, inspiration, or rejection by this governance kit. It exists to:

- Prevent re-evaluation of the same project without new context
- Preserve adoption/rejection rationale so decisions are reviewable
- Retain institutional knowledge about what was considered and why

This document is **advisory**. Normative rules live in `constitution/`.

## How to Use

- **Before evaluating an external project**: check whether it already has an entry here. If it does, read the existing entry and its re-evaluation trigger before starting a new assessment.
- **After evaluation**: append a new entry using the template below. Do not remove or overwrite existing entries.
- **If a previous evaluation is revisited** (new version, changed context, updated requirements): add a **Re-evaluation** sub-entry under the original entry — do not overwrite the original.

---

## Evaluation Entry Template

```
### [Project Name] — [Date YYYY-MM-DD]

**Source**: URL or reference

**Evaluated by**: who initiated/conducted the evaluation

**Category**: governance | architecture | tooling | workflow | testing | other

**What it provides**: 1–3 sentence summary of what the project does.

**Verdict**: ADOPTED (partial) | ADOPTED (full) | INSPIRATION ONLY | REJECTED | DEFERRED

**Overlap with this kit**: what areas overlap and which project covers them better.

**Gaps it fills (if any)**: what the project provides that this kit currently lacks.

**What we adopted / were inspired by** (if applicable): concrete items taken or inspired, with target location in the kit.

**Why rejected / deferred** (if applicable): concrete reasons.

**Re-evaluation trigger**: under what conditions this entry should be revisited.
```

---

## Entries

### contains-studio/agents — 2026-02-24

**Source**: https://github.com/contains-studio/agents

**Evaluated by**: @rhemzal (via Copilot Space assessment)

**Category**: tooling / workflow

**What it provides**: A catalog of ~30 specialized AI agent system prompts for Claude Code, organized by "department" (engineering, design, marketing, product, testing, operations). Each agent is a `.md` file with YAML frontmatter (name, description, color, tools) and a detailed system prompt. Includes proactive trigger patterns and multi-agent coordination.

**Verdict**: INSPIRATION ONLY

**Overlap with this kit**:

- Testing agents (`test-writer-fixer`, `api-tester`, `performance-benchmarker`, `test-results-analyzer`) cover similar ground to `ci/TEST_GATES.md` — but as capabilities/expertise, not as enforceable constraints. AI_governance is deeper on enforcement; contains-studio is more tool-specific.
- `backend-architect` lists architecture patterns (hexagonal, DDD, CQRS, etc.) as buzzwords without trade-off analysis or decision framework. AI_governance covers this substantially better via `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md` + style matrix + RAG notes with failure modes.
- `legal-compliance-checker` provides actionable GDPR/COPPA/HIPAA checklists. AI_governance references standards (`research/PROFESSIONAL_STANDARDS_AND_REFERENCES.md`) but does not provide ready-to-use compliance checklists.

**Gaps it fills (if any)**:

- **Technology-specific "recipes"**: Concrete performance budgets (LCP <2.5s, JS <200KB), framework-specific test commands (k6, JMeter, Pact), and benchmark report templates. AI_governance is intentionally tool-agnostic but could benefit from an optional "recipes" appendix pattern for concrete projects.
- **Proactive trigger pattern**: The idea that certain checks/agents should fire automatically after specific events (e.g., "after code change → run test check", "after boundary change → trigger ADR review"). This could complement governance workflow.
- **Compliance checklists as actionable artifacts**: GDPR/COPPA checklist format is more immediately usable than reference links to standards.

**What we adopted / were inspired by**:

- (Pending) Consider adding a "proactive trigger" recommendation to `usage/` or local overlay guidance — mapping governance checks to triggering events.
- (Pending) Consider whether `research/` should include optional compliance checklist templates for common regulations.

**Why not adopted further**:

- Different layer: contains-studio defines what AI *can do* (capabilities); AI_governance defines what AI *must do* (constraints). They are complementary layers, not substitutes.
- No governance enforcement: contains-studio has zero enforcement mechanisms, no CI gates, no ADR discipline, no boundary integrity rules, no compliance reporting.
- Marketing/design/growth agents are entirely out of scope for an engineering governance kit.
- Architecture guidance is superficial (pattern name-dropping without trade-off analysis or failure modes).

**Re-evaluation trigger**: If contains-studio adds governance/enforcement mechanisms, or if we decide to ship agent definitions as part of the kit.

---

## Related Documents

- `research/PROFESSIONAL_STANDARDS_AND_REFERENCES.md`
- `constitution/AI_RULES.md`
- `adr/ADR_0004_Tooling_Is_Experimental.md`
