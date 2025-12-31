# Professional Standards & References (Research, Advisory)

## Purpose
This page exists to support **theoretical and professional validation** of architecture and governance decisions.

Rules:
- This page is **advisory** (non-normative). Normative rules remain in `constitution/`.
- Do not cargo-cult standards. Use them as **checklists and vocabulary** to make decisions reviewable.
- Prefer linking to a standard rather than re-stating its content.

## How to Use This (Practical)
When you write an ADR or justify an architecture/hybrid:
1. Express the decision using **measurable quality attribute scenarios** (see `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`).
2. Validate trade-offs using **ATAM-lite** (also in the framework).
3. Use references below to ensure your terminology and artifacts match professional expectations.

When a project starts “from architecture”, do not forget **externalities** (regulatory, security, privacy, operability constraints). Capture them explicitly in the ADR **Context** so they are reviewable.

## Externalities Checklist (What People Forget Early)
Use this as a prompt list, not as a requirement set. Pick what applies.

- **Cybersecurity & trust boundaries**: threat model assumptions, authentication/authorization, secrets handling, auditability, incident response expectations.
- **Cyber resilience & availability**: RTO/RPO (recovery time objective / recovery point objective) expectations, dependency failure behavior, rate limits, DDoS posture, graceful degradation.
- **Privacy & data protection**: data minimization, retention, lawful basis, data subject rights, cross-border transfers, logging sensitivity.
- **Supply chain & provenance**: third-party dependencies, SBOM (software bill of materials) expectations, signed builds, vulnerability management.
- **Safety / harm constraints** (if applicable): what “unsafe behavior” means for the domain, fail-safe defaults.
- **Accessibility** (if user-facing): a11y (accessibility) requirements, evidence of conformance.
- **Data residency / sovereignty**: where data may live, who may access it, cloud region constraints.
- **Operational constraints**: observability, runbooks, on-call model, deployment windows, change management.

Recommended workflow:
- Put the applicable items into the ADR “Context” and “Sensitivity Points & Risks”.
- Translate the top risks into measurable scenarios (quality attributes), then into tactics and enforceable checks.

## Architecture Description & Evaluation
- **ISO/IEC/IEEE 42010** — Architecture description: stakeholders, concerns, viewpoints, and rationale. Use it to check whether your architecture is *described* in a reviewable way.
- **ATAM (Architecture Tradeoff Analysis Method)** — Evaluation approach: validate an architecture against quality attribute scenarios and trade-offs. This repo uses an “ATAM-lite” variant.
- **C4 Model** — Diagramming conventions (Context/Container/Component/Code). Use it to make diagrams consistent and reviewable.

## Quality Models (What ‘Quality’ Means)
- **ISO/IEC 25010** — Standard quality attribute taxonomy. Use it to avoid fuzzy terms (“good quality”) and to anchor your top priorities.

## Requirements & Lifecycle Process (How ‘Professional Development’ Is Framed)
- **ISO/IEC/IEEE 12207** — Software lifecycle processes. Use it as a vocabulary for roles/activities (requirements, design, implementation, verification, maintenance).
- **ISO/IEC/IEEE 29148** — Requirements engineering. Use it to keep requirements testable and to separate functional vs. non-functional constraints.

## Testing & Verification
- **ISO/IEC/IEEE 29119** — Software testing standards (process, documentation, techniques). Use it as a checklist for whether your test strategy is coherent.

## Security (Vocabulary & Checklists)
- **ISO/IEC 27001** — Information security management system (ISMS). Use it to reason about governance, evidence, and control coverage.
- **ISO/IEC 27005** — Information security risk management (risk framing, assessment, treatment).
- **NIST SP 800-53** — Security and privacy controls catalog (broad, control-centric). Use it for “what controls do we need?” thinking.
- **NIST Cybersecurity Framework (CSF)** — High-level security outcomes (Identify/Protect/Detect/Respond/Recover).
- **OWASP ASVS** — Application security verification standard. Use it as an app-level verification checklist.
- **NIST SP 800-218 (SSDF)** — Secure software development framework (practices for building and maintaining software securely).
- **STRIDE** — Threat modeling categories. Use it for lightweight threat discovery.

## Privacy (If You Process Personal Data)
- **GDPR (EU)** — Legal framework for personal data processing (consult legal/compliance for applicability).
- **ISO/IEC 27701** — Privacy information management extension to ISO 27001.
- **NIST Privacy Framework** — Outcome-oriented privacy risk management.

## Cyber Resilience / Regulatory (If Applicable)
These are context-dependent and sector/jurisdiction specific; treat them as “check if relevant”.
- **NIS2 (EU)** — Network and Information Systems Directive (NIS2): security and incident reporting obligations for certain entities.
- **DORA (EU)** — Digital operational resilience for financial sector.
- **Cyber Resilience Act (EU)** — Product cybersecurity requirements (especially relevant for shipped software products).

## Supply Chain & Provenance
- **SLSA** — Supply-chain Levels for Software Artifacts: supply-chain security levels for build provenance.
- **SBOM formats**: SPDX (Software Package Data Exchange), CycloneDX (SBOM standard) (useful for inventory and vulnerability management).

## Business Continuity (If Availability Matters)
- **ISO 22301** — Business continuity management.

## Accessibility (If You Ship a UI)
- **WCAG** — Web Content Accessibility Guidelines.
- **EN 301 549** — Accessibility requirements for ICT products and services (commonly referenced in public sector contexts).

## Identity & Access Control (Where RBAC Fits)
- **RBAC / ABAC** — Authorization models (see `architecture/TERMINOLOGY_GLOSSARY.md`).
- **NIST SP 800-63** — Digital identity guidelines (identity proofing, authentication). Useful when authn/authz is a core concern.

## Documentation & Configuration Management
- **ADRs** — Decision logging pattern (this repo’s template is the local “standard”).
- If your org uses formal document control: map ADRs and architecture docs into that process rather than duplicating content.

## Notes
- References above are intentionally high-level; exact editions/versions and applicability are organization-dependent.
- If you want to enforce artifacts that align to these references, do it via ADR templates and CI gates rather than by adding more docs.
