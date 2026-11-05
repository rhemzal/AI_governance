# Automated scenarios closure (007)

Plan: `tasks.md`  
AEP: `aep.md`  
Scope: close PR #58 handoff gaps after H5 qualification; **not** adopter CI requirements.

## Objective

Synchronize research/changelog/benchmark docs with eight-task Harbor qualification, add
maintainer `workflow_dispatch` for oracle/nop, ship optional `ci/select_overlay_rows.py`,
and publish scaffolds for Experiment B (H7) and native Stop (H8) without claiming automation.

## Backlog

| ID | Item | Status in 007 |
| --- | --- | --- |
| D1 | Post-qualification DOC DELTA (EXTERNAL, CHANGELOG, BENCHMARK) | Implement |
| D2 | Image digest + agent install limits in harbor docs | Document |
| D3 | H6 `governance-scenarios` workflow (oracle/nop; optional cursor input) | Implement |
| D4 | H9 `ci/select_overlay_rows.py` + tests | Implement |
| D5 | H7 fresh-context review harness README | Scaffold |
| D6 | H8 native Stop observation README | Scaffold |

H7/H8 remain **out of Harbor**; scaffolds record manual trial steps only.

## Evidence

`progress.md`
