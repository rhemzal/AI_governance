# ADR 0019: VS Code Copilot Stop Adapter

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it, preserve this line._

## Status

Accepted — 2026-11-07.

## Context

Tier C's native Stop integration was Cursor-specific, so adopters requiring governed
work through VS Code and GitHub Copilot had no corresponding host adapter. VS Code
supports `agentStop` hooks in Preview. Its hook contract differs from Cursor's, and
configuration or contract tests cannot establish that the VS Code host dispatched it.

## Decision

1. Add a dedicated VS Code Copilot `agentStop` adapter and hook configuration. It runs
   the projected acceptance verifier and uses Copilot's block response contract.
2. Extend the Tier C installer to copy the adapter and merge the Copilot instruction
   route without replacing existing host files; reject a symlinked instruction target.
3. Extend the completeness checker to distinguish adapter configuration from native
   dispatch evidence. The optional recorder stores only minimal invocation metadata.
4. Document a fresh-session manual dispatch check for each host. Keep VS Code hooks
   experimental while the host feature is Preview; do not treat tests or file presence
   as native-dispatch evidence.

## Consequences

Tier C can be installed for Cursor and VS Code + Copilot without sharing a hook
implementation across hosts. Adopters must verify the adapter they use in its native
IDE and record the host version and observed result. Native VS Code dispatch remains
unverified in this repository because no VS Code runtime is available in the
implementation environment.

## References

- [Tier C adoption scope and host matrix](../usage/ADOPTION_SCOPE_AND_HOSTS.md)
- [Full opt-in adoption playbook](../usage/FULL_OPT_IN_ADOPTION_PLAYBOOK.md)
- [Opt-in stack guide](../governance/experimental/spec_gates/OPT_IN_STACK.md)
- [Experimental spec-gates adapter README](../governance/experimental/spec_gates/README.md)
- [VS Code hooks documentation](https://code.visualstudio.com/docs/copilot/customization/hooks)
