# RESEARCH_ENGINEERING_PLAYBOOKS.md

_Provenance: This research note was added to the AI_governance kit (https://github.com/rhemzal/AI_governance)._


## Status

**Research and adaptation reference — non-normative.**

Normative rules remain in `constitution/`. Do not treat this document as mandatory process.

## Purpose

This document summarizes external engineering playbooks and related public practices that should inform the `AI_governance` project.

The goal is not to copy existing playbooks, but to extract durable engineering principles and adapt them for AI-assisted development.

## Research Scope

Reviewed sources:

- Google Engineering Practices
- Microsoft ISE Engineering Fundamentals Playbook
- GitHub Copilot custom instructions documentation
- GitLab AI-Assisted Development Playbook
- GitLab Duo-First Development
- GitLab AI Model Validation
- Thoughtworks Technology Radar
- DORA software delivery metrics
- OpenSSF Scorecard
- AWS Well-Architected Operational Excellence
- AGENTS.md / coding-agent context file research

## 1. Google Engineering Practices

### Relevant findings

Google publishes generalized engineering practices intended to apply across languages and projects. The public repository states that these documents represent collective engineering experience and are made available because other organizations may benefit from them.

Relevant source:
- https://github.com/google/eng-practices
- https://google.github.io/eng-practices/review/reviewer/standard.html

Google’s code review standard is especially relevant: the purpose of review is to improve overall code health over time, not to achieve perfection. Reviewers should balance progress against quality, and approve changes that clearly improve maintainability, readability, and understandability.

### Adaptation for AI governance

Adopt:

- Code health over local cleverness
- Continuous improvement over perfection
- Review should focus on maintainability and understandability
- Small nits should not block progress

Adapt:

- In solo + AI-agent mode, “reviewer” can be an AI audit plus automated verification, not necessarily another human.
- Human code review should become mandatory only at higher governance levels.

Avoid:

- Treating Google-scale review process as mandatory for early solo projects.

## 2. Microsoft ISE Engineering Fundamentals Playbook

### Relevant findings

Microsoft’s playbook frames a playbook as a way to improve efficiency, reduce mistakes, avoid common pitfalls, and learn from shared experience. It also advises keeping the code quality bar high, preferring quality and precision, making the simple thing work now, avoiding scope creep, and shipping incremental customer value.

Relevant source:
- https://microsoft.github.io/code-with-engineering-playbook/

### Adaptation for AI governance

Adopt:

- A playbook exists to reduce repeated mistakes
- Fix the playbook when it is broken
- Prefer simple working increments
- Avoid expanding scope inside a task
- Ship incremental value

Adapt:

- In AI-assisted development, “playbook” should include instructions for agents, not only humans.
- Scope control should be enforced through AI prompts and verification reports.

Avoid:

- Turning the playbook into a large-team process manual.

## 3. GitHub Copilot Custom Instructions

### Relevant findings

GitHub supports custom instructions for Copilot. Repository custom instruction files give Copilot additional context on how to understand the project and how to build, test, and validate changes.

Relevant source:
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions

### Adaptation for AI governance

Adopt:

- Repository-local instructions are a supported mechanism for guiding AI behavior.
- Project rules should live in the repository.
- Instructions should include build/test/validation commands.

Adapt:

- Copilot instructions should be generated from governance documents, not be the only source of truth.
- Tool-specific files should be downstream projections of the governance kit.

Avoid:

- Assuming Copilot instructions are enforcement.
- Assuming Copilot will automatically obey all rules without tests, gates, or review.

## 4. GitLab AI-Assisted Development Playbook

### Relevant findings

GitLab’s AI-Assisted Development Playbook is the closest public artifact to this project’s direction. It provides a shared framework for working with AI coding agents, including readiness assessment, infrastructure, autonomy levels, the harness pattern, testing patterns, and efficiency techniques.

Relevant source:
- https://handbook.gitlab.com/handbook/engineering/workflow/ai-assisted-development/

Its core principles are highly relevant:

- failing test before every feature
- fix the environment, not the prompt
- constraints are multipliers
- encode constraints in CI rather than natural language where justified
- repo is the single source of truth
- instruct agents to challenge plans, not only execute them

It also defines autonomy levels from baseline autocomplete to harness-based autonomous agents and warns that skipping to higher autonomy without infrastructure amplifies technical debt.

### Adaptation for AI governance

Adopt strongly:

- Repo as source of truth
- Failing test defines “done”
- Constraints should move from prompt to environment/CI where justified
- Agents must challenge plans
- AI autonomy must depend on maturity

Adapt:

- GitLab’s model is designed for GitLab’s organization and tooling; convert it into a tool-agnostic governance model.
- Do not require GitLab-style MR workflows for solo projects.
- Keep adaptive governance levels separate from AI autonomy levels.

Avoid:

- Blindly applying “CI for everything” in early solo projects.
- Treating CI as always superior to local verification.

## 5. GitLab Duo-First Development

### Relevant findings

GitLab’s Duo-First Development standards define expected practices for using GitLab Duo in issue creation, merge request generation, review assistance, test case generation, and documentation generation.

Relevant source:
- https://handbook.gitlab.com/handbook/engineering/workflow/duo-first-development/

### Adaptation for AI governance

Adopt:

- AI should assist with issues/specs, code review, tests, and documentation.
- AI-generated review should happen before expensive human review where appropriate.
- Test scaffolding should be part of Definition of Done for new behavior.

Adapt:

- Replace tool-specific “Duo” language with generic AI-agent language.
- Apply only as a suggested workflow, not a mandatory governance rule for all projects.

Avoid:

- Tool lock-in.
- Large-team assumptions as default.

## 6. GitLab AI Model Validation

### Relevant findings

GitLab documents model validation as a process combining practical efficiency with performance, quality, legal, compliance, resource, and integration assessment. It also monitors the model market, benchmarks notable models, and accepts feature-team requests with use-case-specific evaluation criteria.

Relevant source:
- https://handbook.gitlab.com/handbook/engineering/ai/ai-framework/model-validation/model_evaluation/

### Adaptation for AI governance

Adopt:

- Model/tool selection should be treated as an experiment.
- Evaluation must include quality, performance, cost, integration complexity, and operational risk.
- Model switching must be justified by use case and evidence.

Adapt:

- For solo projects, use lightweight benchmark scenarios rather than formal enterprise validation.

Avoid:

- Defaulting to the newest model without benchmark evidence.

## 7. Thoughtworks Technology Radar

### Relevant findings

Thoughtworks Technology Radar is a twice-yearly, opinionated snapshot of tools, techniques, platforms, languages, and frameworks. It classifies items into adoption bands such as Adopt, Trial, Assess, and Caution.

Relevant source:
- https://www.thoughtworks.com/radar

### Adaptation for AI governance

Adopt:

- Technology choices should be classified by maturity, not hype.
- “Assess” and “Trial” are valid states.
- Governance should support experimentation without premature adoption.

Adapt:

- Create an internal lightweight radar for AI tools, architectural approaches, and governance practices.

Avoid:

- Treating emerging AI tools as default project infrastructure.

## 8. DORA Software Delivery Metrics

### Relevant findings

The DORA metrics program identifies software delivery performance metrics focused on delivering safely, quickly, and efficiently. The metrics distinguish throughput and instability, and can be used across different technologies and systems.

Relevant source:
- https://dora.dev/guides/dora-metrics/

### Adaptation for AI governance

Adopt:

- Measure delivery outcomes, not only activity.
- Track both speed and instability.
- For AI-assisted projects, include rework caused by AI-generated code.

Adapt:

- Use lightweight metrics for solo projects:
  - time to verify
  - number of failed agent iterations
  - number of human corrections
  - regression frequency
  - verification cost

Avoid:

- Applying enterprise DORA metrics dashboards to early projects.

## 9. OpenSSF Scorecard

### Relevant findings

OpenSSF Scorecard assesses open-source projects for security risks using automated checks. It was created to help maintainers improve security health and help consumers evaluate dependency risk.

Relevant source:
- https://scorecard.dev/

### Adaptation for AI governance

Adopt:

- Automated security checks are useful for public or dependency-like projects.
- Repository health can be partially measured automatically.

Adapt:

- Make Scorecard-like checks recommended from higher governance levels.
- For solo/private prototypes, keep security checks lightweight.

Avoid:

- Making full open-source security governance mandatory for early internal prototypes.

## 10. AWS Well-Architected Operational Excellence

### Relevant findings

AWS Well-Architected Operational Excellence provides best practices for design, delivery, maintenance, and ongoing improvement of workloads. It focuses on understanding benefits and risks of decisions, measuring operations and architectures against best practices, and identifying improvement areas.

Relevant source:
- https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html

### Adaptation for AI governance

Adopt:

- Architecture and operations should be evaluated against explicit questions.
- Improvement should be continuous and measurable.
- Operational readiness matters when deployment risk exists.

Adapt:

- Use only for production or serious operational projects.
- Do not impose operational excellence rituals on throwaway PoCs.

Avoid:

- Cloud-production assumptions as default.

## 11. AGENTS.md and Agent Context Files

### Relevant findings

AGENTS.md is presented as a simple open format for guiding coding agents and as a predictable place to provide project context and instructions.

Relevant source:
- https://agents.md/

Recent research warns that repository-level context files are not automatically beneficial. Context files can increase task difficulty and cost if they contain unnecessary requirements, conflicts, or context bloat.

Relevant research examples:
- https://arxiv.org/abs/2602.11988
- https://arxiv.org/abs/2606.15828

### Adaptation for AI governance

Adopt:

- Use agent instruction files.
- Keep them short, explicit, and actionable.
- Store stable project rules in the repository.

Adapt:

- Generate tool-specific instruction files from governance sources.
- Separate:
  - constitution
  - enforcement
  - architecture decisions
  - tool-specific projections

Avoid:

- Context bloat
- Duplicated rules
- Conflicting instructions
- Long theory dumps in files loaded on every AI task

## Overall Gap Analysis

Existing public sources provide strong pieces:

- Google: code health and review standards
- Microsoft: engineering playbook mindset
- GitHub: Copilot custom instructions
- GitLab: AI-assisted development playbook and autonomy levels
- Thoughtworks: technology maturity classification
- DORA metrics: delivery outcome metrics
- OpenSSF: automated security health checks
- AWS: operational excellence evaluation
- AGENTS.md ecosystem: agent context files and emerging risks

However, none of them fully combine:

- tool-agnostic AI governance
- adaptive enforcement levels
- solo developer + multi-agent workflow
- architecture decision framework
- RAG/theoretical grounding
- CI/CD proportionality
- interface automation-first rules
- AI tool optimization protocols
- explicit anti-overengineering controls

## Conclusion

The `AI_governance` project should not reinvent engineering fundamentals.

It should integrate proven engineering playbook principles into a smaller, adaptive, AI-first governance system.

The closest prior art is GitLab’s AI-Assisted Development Playbook, but this project should remain more general, tool-agnostic, solo-friendly, and architecture-oriented.
