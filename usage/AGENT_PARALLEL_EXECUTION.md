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

## Related documents

- [AI Engineering Methods](AI_ENGINEERING_METHODS.md)
- `constitution/AI_ENFORCEMENT.md`
- `usage/AI_RUN_EVIDENCE.md`
