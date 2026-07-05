# PLAYBOOK_ADAPTATION_GUIDE.md

## Status

**Research and adaptation reference — non-normative.**

Normative rules remain in `constitution/`. Use this guide when evaluating whether to adopt, adapt, defer, or reject external practices.

## Purpose

This document defines how principles from established engineering playbooks should be adapted into `AI_governance`.

The goal is to avoid both extremes:

- reinventing known engineering fundamentals
- importing enterprise-heavy process into solo AI-assisted development

## Core Adaptation Rule

Adopt principles, not organizational bureaucracy.

A principle is reusable when it improves:

- code health
- maintainability
- verification
- decision quality
- architectural clarity
- AI-agent reliability

A process should only be adopted when the project maturity and risk justify its cost.

## 1. Adopt Directly

### 1.1 Repo Is the Source of Truth

Adopt from GitHub Copilot docs and GitLab AI-Assisted Development Playbook.

Rules, verification commands, architecture decisions, and agent instructions should live in the repository.

Reason:

- AI agents can read repository-local instructions.
- Human and AI workflows stay aligned.
- Rules are versioned with the code.

Recommended files:

- `AI_RULES.md`
- `AI_ENFORCEMENT.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `architecture/`
- `adr/`
- `ci/`

### 1.2 Code Health Over Perfection

Adopt from Google Engineering Practices.

A change should improve the overall health of the codebase. Do not block useful progress because the change is not perfect.

AI adaptation:

- AI review should identify real maintainability risks.
- Minor style nits should not block progress unless they indicate systemic drift.

### 1.3 Simple Working Increment First

Adopt from Microsoft Engineering Fundamentals Playbook.

Prefer a small working step over a broad unfinished design.

AI adaptation:

- Agents should avoid scope expansion.
- If scope grows, the agent must stop and report it.

### 1.4 Constraints Belong in Environment / Tests / CI Where Practical

Adopt from GitLab AI-Assisted Development Playbook.

Prompts are useful, but durable constraints should move into tests, linters, static analysis, scripts, or CI when justified.

AI adaptation:

- First use prompts for exploration.
- Promote repeated failures into enforceable checks.
- Do not add heavy CI gates unless adaptive governance justifies them.

### 1.5 AI Must Challenge the Plan

Adopt from GitLab AI-Assisted Development Playbook.

AI agents should not only execute instructions. They must identify flawed assumptions, missing tests, architectural violations, and overengineering.

Required output:

```text
CHALLENGE CHECK
- Risky assumption:
- Missing verification:
- Possible simpler alternative:
- Should proceed: yes / no
```

## 2. Adopt With Adaptation

### 2.1 Code Review

Source inspiration:

- Google Engineering Practices
- Microsoft Engineering Playbook
- GitLab Duo-First Development

Adaptation:

- Level 0–1: local self-review + AI audit is enough.
- Level 2: AI adversarial review before merge/commit.
- Level 3: human review or PR checklist.
- Level 4: mandatory review and audit trail.

Do not require human PR review by default for solo projects.

### 2.2 CI/CD

Source inspiration:

- GitLab AI-Assisted Development Playbook
- DORA
- OpenSSF
- AWS Well-Architected

Adaptation:

- CI/CD must be proportional to maturity and risk.
- Local verification is acceptable in early stages.
- Cloud CI becomes useful when regressions, releases, or agent concurrency matter.

Default for serious solo + multi-agent development:

- one fast verification command
- lightweight GitHub Action
- unit tests
- smoke tests
- basic architecture checks if cheap

Avoid:

- enterprise release gates as default
- mandatory coverage thresholds without risk reasoning
- slow pipelines that discourage iteration

### 2.3 Metrics

Source inspiration:

- DORA
- GitLab model validation

Adaptation for AI-assisted development:

Track lightweight operational signals:

- number of failed AI iterations
- time to verify a change
- number of manual corrections
- regression frequency
- cost/latency of model/tool usage
- percentage of tasks completed without human rescue

Avoid:

- dashboard-heavy enterprise measurement for small projects

### 2.4 Tool and Model Selection

Source inspiration:

- GitLab AI Model Validation
- GitHub Copilot model/tool documentation
- Thoughtworks Technology Radar

Adaptation:

- Treat model/tool choice as an experiment.
- Benchmark against project-specific tasks.
- Use “Adopt / Trial / Assess / Caution” style classification.

Required evaluation dimensions:

- correctness
- architecture compliance
- test generation quality
- latency
- cost
- context handling
- ability to follow repository rules
- maintenance risk

### 2.5 Agent Instruction Files

Source inspiration:

- GitHub Copilot custom instructions
- AGENTS.md ecosystem
- research on context-file effectiveness and smells

Adaptation:

- Keep loaded agent instructions short.
- Put stable, task-critical rules in `AGENTS.md` or Copilot instructions.
- Put deeper theory and decision guides outside always-loaded context.
- Avoid duplicating rules across many files.

Required rule:

```text
Agent instruction files must be minimal, non-conflicting, and actionable.
```

## 3. Defer Until Needed

### 3.1 Heavy PR Policies

Defer unless:

- multiple humans contribute
- external users depend on releases
- regressions are costly
- compliance/audit trail is required

### 3.2 Full Security Governance

Defer full security gates unless:

- project is public
- project is deployed
- project is reused as a dependency
- sensitive data is handled

Lightweight local checks are acceptable earlier.

### 3.3 Production Operational Excellence

Defer AWS-style operational excellence unless:

- the project runs in production
- outages matter
- deployment rollback is required
- observability is necessary

### 3.4 Formal Architecture Review Boards

Do not adopt as default.

Use lightweight ADRs and AI-assisted architecture decision checks first.

## 4. Reject as Default

Reject these as default practices for early or solo projects:

- mandatory PR workflow for every change
- mandatory cloud CI for throwaway PoCs
- ADR for every small reversible decision
- coverage thresholds without risk analysis
- large always-loaded AI instruction files
- tool-specific governance as the root source of truth
- “best practice” claims without project context

## 5. Proposed Mapping Into AI_governance

### Constitution

Add or maintain:

- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
- `constitution/ADAPTIVE_GOVERNANCE.md`

### Architecture

Add:

- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/ARCHITECTURE_STYLE_MATRIX.md`
- `adr/ADR_Architecture_Is_Contextual.md`

### Interface

Maintain:

- `interface/INTERFACE_RULES_PROPOSAL.md`
- `interface/INTERFACE_CI_GATES.md`
- `adr/ADR_Interface_Automation_First.md`

### Tooling

Add:

- `tooling/AI_TOOL_OPTIMIZATION.md`
- `tooling/COPILOT_OPTIMIZATION_PROTOCOL.md`
- `tooling/BENCHMARK_SCENARIOS.md`
- `adr/ADR_Tooling_Is_Experimental.md`

### Research / RAG

Add:

- `research/RESEARCH_ENGINEERING_PLAYBOOKS.md`
- `research/PLAYBOOK_ADAPTATION_GUIDE.md`
- `rag/README.md`
- `adr/ADR_RAG_Is_Advisory_Not_Normative.md`

### Agent Instructions

Generate concise projections:

- `AGENTS.md`
- `.github/copilot-instructions.md`

These files should reference deeper documents rather than duplicate them.

## 6. Mandatory Adaptive Governance Check

Before adding a process, gate, ADR requirement, or CI workflow, AI must answer:

```text
GOVERNANCE FIT CHECK
- Project stage:
- Recommended governance level:
- Risk mitigated:
- Required now: yes / no / partial
- Local verification sufficient: yes / no
- Maintenance cost:
- Simplest useful enforcement:
- What to defer:
```

## Final Recommendation

Use external playbooks as a reference library, not as a process template.

The default governance posture should be:

- lightweight
- adaptive
- solo-friendly
- AI-agent aware
- verification-oriented
- resistant to overengineering
