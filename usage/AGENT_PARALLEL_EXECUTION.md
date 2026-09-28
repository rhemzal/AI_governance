# Agent Parallel Execution

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

Use parallel agents when independent work can reduce wall time or context pressure without creating unsafe shared mutation.

This is advisory implementation guidance for concurrency requirements already defined in `constitution/AI_ENFORCEMENT.md`.

## When parallelism helps

Good candidates include independent repository research, separate backend/frontend investigation, implementation plus independent falsification review, independent fixture preparation, and unrelated modules with clear ownership.

Poor candidates include two writers changing the same files/contract, dependent work presented as parallel, scarce shared hardware without ownership, and tasks where integration cost exceeds saved time.

## Isolation pattern

```text
task owner / integrator
   ├─ worker A -> isolated workspace -> evidence A
   ├─ worker B -> isolated workspace -> evidence B
   └─ shared device/service -> explicit owner or lease
                     ↓
                integration
                     ↓
              re-verification
```

Git worktrees, clones, containers, or remote sandboxes are implementation options. Governance requires the property, not a specific tool.

## Delegation contract

A bounded delegate should receive:
- objective and stop condition;
- relevant source-of-truth pointers;
- allowed targets/effects;
- whether it may edit or is research-only;
- expected output/evidence;
- ownership of files/resources;
- return point to the integration owner.

A subagent cannot expand its own authority.

## Integration

The integration owner reconciles contradictory findings, resolves overlapping edits deliberately, verifies the integrated revision rather than trusting worker-local results, and records unresolved assumptions.

## Shared resources

Physical devices, test environments, services, databases, and ports may require leases or explicit ownership. Retrying a mutation requires determining whether the first attempt already succeeded.

## Benefit and stopping criteria

Use a single agent as the default when the work is coupled or small. Before delegating,
identify independent outputs, the integration test and the reason parallel work is likely
to help. Record coordination/review cost and discarded work; wall time alone can hide a
larger total burden. Stop redundant branches when they no longer add discriminating evidence.

A worktree isolates files, not ports, databases, credentials, devices or deployment targets.
Use explicit ownership or independent instances for those resources. A second model/context
can still share the same mistaken specification; require counterexamples and observations
rather than counting approving reviewers. No fixed multi-agent topology is required.

## Related Documents

- [AI Engineering Methods](AI_ENGINEERING_METHODS.md)
- `constitution/AI_ENFORCEMENT.md`
- `usage/AI_RUN_EVIDENCE.md`
