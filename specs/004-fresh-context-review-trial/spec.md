# Fresh-context review trial (Experiment B)

Host: Tier B, `requesting-code-review` pattern without author verdict in packet.  
Review target: `ci/uncommitted_diff_identity.py` + `ci/gate_tests/test_workflow_acceptance.py` (PR #53 scope).  
Starting revision: `b4c6b1e` (includes Experiment A record).

## Acceptance criteria (screening)

1. **B1** reviewer (fresh packet: diff/spec/acceptance only) reports ≥1 **confirmed** gap missed by **B0** author-style pass.
2. Gap is **verifiable** (missing test, wrong edge case, or doc mismatch).
3. **False positives** on clean control: ≤1.
4. One repair + recheck cycle max in first round.

## B1 packet contents

- ADR-0016 amendment text (content-aware dirty identity)
- Files: `ci/uncommitted_diff_identity.py`, relevant tests
- Explicit exclusion: prior chat, “already merged”, COMPLIANCE blocks

## Evidence

`progress.md`
