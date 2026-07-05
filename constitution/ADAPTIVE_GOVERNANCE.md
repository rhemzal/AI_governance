# ADAPTIVE_GOVERNANCE — Proportional Governance for AI-Assisted Development

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

This document is **normative**. It defines the adaptive governance model for AI-assisted software projects, with an emphasis on proportionality, solo and multi-agent development, and fast iteration without unnecessary overhead.

---

## 1. Purpose

This document defines a proportional governance framework that explicitly supports the common case of:
- one human developer working with one or more AI coding agents
- fast iteration, rapid experimentation, and short feedback loops
- lightweight but effective verification

It provides governance levels that scale with project maturity, risk, and deployment criticality — rather than applying a fixed enterprise model to every project.

---

## 2. Why Fixed Enterprise Governance Is Harmful for Solo / AI-Agent Development

Enterprise CI/CD and governance workflows are designed for:
- large teams with multiple contributors
- long-lived codebases with complex ownership
- regulated deployments with audit requirements
- slow, deliberate release cycles with stakeholder sign-off

Applying that model to a solo or early-stage AI-assisted project causes:

- **Friction without benefit.** PR workflows, coverage thresholds, mandatory ADRs, and complex CI pipelines add cost without reducing risk when there is one developer and no shared codebase.
- **AI over-engineering.** AI coding agents trained on enterprise patterns will propose enterprise-grade solutions by default. Without explicit governance constraints, they add unnecessary infrastructure.
- **Maintenance debt before value.** Heavy process introduced early becomes a burden that slows down the iteration needed to find product-market fit or validate an idea.
- **False confidence.** A green CI pipeline does not mean the project is healthy. Checking boxes without purpose is not governance.

The correct response is governance proportional to actual risk and context.

---

## 3. Proportional Governance Principle

> **Governance and CI/CD enforcement must be proportional to project maturity, risk, number of contributors or agents, deployment criticality, reversibility of changes, and cost of verification.**

Factors that increase the appropriate governance level:
- more contributors (human or AI)
- external users or customers
- production deployments
- irreversible operations (data deletion, financial transactions, published APIs)
- regulated domains (security, privacy, safety)

Factors that decrease the appropriate governance level:
- exploratory or throwaway code
- no external users
- reversible changes
- single developer with full context

---

## 4. Governance Levels

### Level 0 — Exploration / Scratch / Throwaway PoC

**Use when:**
- Code is experimental, exploratory, or a throwaway proof of concept.
- No production users.
- Changes are cheap and reversible.

**Recommended:**
- Local verification only.
- Simple `make test`, `make verify`, or `./verify.sh`.
- No cloud CI required.

**Avoid:**
- PR policies or branch protection rules.
- Coverage thresholds.
- Release workflows.
- Heavy documentation requirements.
- ADRs for small decisions.

---

### Level 1 — Solo Prototype

**Use when:**
- One developer.
- Code has value but is not yet critical.
- AI agents may assist with implementation.
- Project may or may not continue.

**Recommended:**
- Local verification command (e.g., `make verify` or `./verify.sh`).
- Lint/format if cheap and tool is already in place.
- Unit tests for core logic.
- Smoke test for CLI or API if applicable.

**Avoid:**
- Complex CI pipeline.
- Mandatory ADRs for small, reversible changes.
- PR review requirements (no other reviewers exist).
- Formal release process.

---

### Level 2 — Serious Solo / Multi-Agent Project

**Use when:**
- One human developer.
- Multiple AI agents may modify code.
- Regressions matter and would be costly to debug.
- Project should remain maintainable over time.

**Recommended:**
- Lightweight CI on push or PR (e.g., GitHub Actions free tier).
- Install/build check.
- Lint and typecheck.
- Unit tests covering core logic.
- Smoke tests for CLI or API.
- Minimal architectural boundary checks where practical.

**Avoid by default:**
- Heavy PR bureaucracy (mandatory reviewers, required reviews, complex checklists).
- Enterprise release process.
- Complex deployment gates.
- Excessive documentation gates.
- Coverage thresholds that block iteration.

> **Level 2 is the default target for serious AI-assisted solo projects.**

---

### Level 3 — Shared / Released Project

**Use when:**
- Multiple humans contribute.
- External users exist.
- Releases are published and versioned.

**Recommended:**
- PR checklist.
- Code review rules (at least one reviewer for non-trivial changes).
- Architecture boundary checks in CI.
- Integration tests.
- Documentation consistency checks.
- Dependency and security checks.
- Release notes.

---

### Level 4 — Production / Safety / Regulated

**Use when:**
- Failures can cause outages, data loss, security incidents, customer harm, or compliance violations.
- Deployment is to production systems with SLAs or regulatory requirements.

**Recommended:**
- Deployment pipeline with staged rollout.
- Rollback strategy.
- Migration checks (schema, data, configuration).
- Performance regression tests.
- Observability and alerting checks.
- Security gates (SAST, dependency scanning, secrets scanning).
- Audit trail.

> **Level 4 is not the default. It must be justified by concrete, documented risk.**

Applying Level 4 governance to a Level 0–2 project is an overengineering error.

---

## 5. AI Responsibilities

When an AI coding agent operates in this repository or any repository using this governance kit, it MUST:

1. **Identify the project's governance level** before recommending or adding any CI/CD, documentation process, or enforcement mechanism.
2. **Apply the GOVERNANCE FIT CHECK** (see Section 7) before proposing gates, pipelines, ADRs, or process requirements.
3. **Default to the lowest sufficient level.** If the project stage is ambiguous, the AI MUST ask rather than assume a high level.
4. **Flag overengineering.** If asked to add enterprise-grade CI/CD to a Level 0–2 project without justification, the AI MUST flag this as a governance mismatch.
5. **Prefer local verification** over cloud CI when local verification provides equivalent risk reduction.
6. **Prefer reversible, incremental additions** over comprehensive upfront infrastructure.

---

## 6. Anti-Overengineering Rules

> **Do not add a CI/CD gate, ADR requirement, documentation process, or enforcement mechanism unless it mitigates a concrete risk and has acceptable maintenance cost.**

### External engineering playbooks

External engineering playbooks must be adapted, not copied.

A principle may be adopted when it improves code health, verification, maintainability, or architectural clarity.

A process may be adopted only when the project maturity and risk justify its maintenance cost.

See `research/RESEARCH_ENGINEERING_PLAYBOOKS.md` and `research/PLAYBOOK_ADAPTATION_GUIDE.md` for research and adaptation guidance (non-normative).

Additional rules:

- Do not add required reviewers, branch protection, or PR policies to solo projects.
- Do not require coverage thresholds at Level 0–1.
- Do not require ADRs for implementation decisions that can be reversed in minutes.
- Do not add release automation before there are releases.
- Do not add deployment pipelines before there are deployments.
- Do not add monitoring and observability before the system is running in production.
- Do not require changelog entries or release notes at Level 0–1.
- Do not require structured commit messages (e.g., Conventional Commits) unless a tool that depends on them is already in use.
- Do not propose more than two new process requirements in a single change.

Violation of these rules by an AI agent is itself a governance error and must be reported in the COMPLIANCE REPORT.

---

## 7. Mandatory GOVERNANCE FIT CHECK

Every AI response that proposes, recommends, or adds CI/CD, enforcement mechanisms, documentation processes, ADRs, or workflow requirements MUST include this output block:

```
GOVERNANCE FIT CHECK
- Project stage: exploration / solo prototype / serious solo / shared / production
- Recommended enforcement level: 0 / 1 / 2 / 3 / 4
- CI/CD needed now: yes / no / partial
- Reason:
- What to defer:
```

If this block is missing from a response that proposes governance or process changes, the response is considered non-compliant.

---

## Related Documents
- `constitution/AI_RULES.md`
- `constitution/AI_ENFORCEMENT.md`
- `research/RESEARCH_ENGINEERING_PLAYBOOKS.md`
- `research/PLAYBOOK_ADAPTATION_GUIDE.md`
- `ci/ARCHITECTURE_GATES.md`
- `ci/TEST_GATES.md`
- `ci/INTERFACE_GATES.md`
- `ci/DOC_GATES.md`
