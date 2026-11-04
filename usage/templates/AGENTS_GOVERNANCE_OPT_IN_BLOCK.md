## Governance baseline

_Provenance: This block originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If copied, preserve this line._

- Kit root: `vendor/AI_governance/`.
- Bundles: **standard**, **research** (adjust if your ADR differs).
- Upstream commit: `<KIT_REVISION>` (full SHA).
- Overlay: `governance/LOCAL_OVERLAY.md` (precedence over kit where declared).
- Read `vendor/AI_governance/AGENTS.md` for kit projection; project tests and ADRs resolve from this repo root.

## Full opt-in stack

- Install / refresh: `./scripts/install-governance-opt-in.sh --stack-only` (see `docs/GOVERNANCE_OPERATOR.md` or `scripts/README-governance-opt-in.md`).
- Completeness: `bash governance/experimental/spec_gates/check-opt-in-stack.sh` (or from `KIT_SOURCE` before adapter copy).
- Acceptance: `export TASK_ACCEPTANCE_CMD="bash ci/adopter_task_acceptance_cmd.sh"` then `bash ci/run_task_acceptance_check.sh`.
- Gates: `bash .specify/gates/verify.sh --boundary git`.
- Natural-language AEP requests are sufficient when `.cursor/rules/autonomous-aep-execution.mdc` is present; do not require `/governed-work`.
- Commits with projected hooks: `git commit -F msgfile` (no `Co-Authored-By` trailer).

Playbook: `vendor/AI_governance/usage/FULL_OPT_IN_ADOPTION_PLAYBOOK.md`.
