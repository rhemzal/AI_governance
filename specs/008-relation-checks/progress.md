# Relation checks — progress

Plan: `tasks.md`  
AEP: `aep.md`  
Spec: `spec.md`

## Task log

| Task | Status | Notes |
| --- | --- | --- |
| 1 ADR-0020 | not started | Write before the first `ci/` or `architecture/` edit of this feature |
| 2 Metamorphic relation | not started | |
| 3 Token cross-check | not started | |
| 4 Resume hash | not started | |
| 5 Skill-copy parity | not started | |
| 6 Procedure index and follow-up | not started | |
| 7 Ledger of execution | not started | This file records the plan only |

The AEP declaration was written on 2026-11-28. The four checks are not implemented.

Declaration check: `python3 ci/validate_aep.py < specs/008-relation-checks/aep.md` → exit 0, `PASS: READY declaration shape; authority, feasibility, and results still require review`.

Ruling: no commit for the plan files unless the operator asks. Upstream task lists that say "commit" are not authorization.
