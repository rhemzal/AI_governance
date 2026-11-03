# Feature Specification: Benchmark trial records

**Feature Branch**: `001-benchmark-trial-records`

**Created**: 2026-11-03

**Status**: Draft

**Input**: User description: "Keep the historical absence of B5–B8 trials recorded, allow a later trial file, and check that file instead of forbidding the directory."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Record a later trial without breaking the suite (Priority: P1)

An agent adds evidence under `research/benchmark_trials/` after the 2026-11-02 baseline. The suite still passes when the directory is absent, when it contains only `README.md`, and when a trial file has the required fields. A malformed file fails the suite.

**Why this priority**: The previous test made the absence permanent, so the recorded gap could not be closed.

**Independent Test**: Run `python3 -m unittest ci.gate_tests.test_open_claim_limits.OpenClaimLimits.test_historical_absence_allows_later_trial_files`.

**Acceptance Scenarios**:

1. **Given** the scenario section, **When** the checker reads it, **Then** it contains exactly one copy of "As of 2026-11-02, scenarios B5 through B8 had no recorded trial."
2. **Given** no `research/benchmark_trials` directory, **When** the checker runs, **Then** that absence is success.
3. **Given** a directory whose only Markdown file is `README.md`, **When** the checker runs, **Then** that directory is success.
4. **Given** a trial file with `scenario: B5`, `revision: abcdef0`, and `outcome: pass`, **When** the checker runs, **Then** it reports no errors.
5. **Given** a missing revision, a revision containing whitespace, an empty outcome, an outcome outside the allowed words, a scenario of `B50`, or a duplicate field, **When** the checker runs, **Then** it reports an error.
6. **Given** `outcome: cancelled` or `outcome: blocked`, **When** the checker runs, **Then** each is accepted. `outcome: pass` and `outcome: fail` are accepted too.

### Edge Cases

- A well-formed file is not a matched comparison and does not prove the outcome.
- The scenario section does not gain a "Trial result" line. Trials live in the directory, not in the scenario specification.
- The claim card `benchmark-scenarios-unrun` must not require the directory to be absent.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The 2026-11-02 absence sentence remains in `tooling/BENCHMARK_SCENARIOS.md`.
- **FR-002**: `ci/benchmark_trials.py` accepts a missing directory and a README-only directory.
- **FR-003**: A trial file's `scenario` is exactly `B5`, `B6`, `B7`, or `B8`.
- **FR-004**: `revision` is one non-empty token with no whitespace.
- **FR-005**: `outcome` is exactly one of `pass`, `fail`, `cancelled`, or `blocked`.
- **FR-006**: The claim card states this rule and its anchor is the new test.

### Key Entities

- **Absence baseline**: the dated sentence. It is not a trial file.
- **Trial record**: a Markdown file other than `README.md` in `research/benchmark_trials/`.

## Success Criteria *(mandatory)*

- **SC-001**: Creating `research/benchmark_trials` no longer fails the suite by itself.
- **SC-002**: The known-bad records in the acceptance scenarios fail the checker.
- **SC-003**: `outcome: cancelled` is accepted.
- **SC-004**: The historical sentence still appears once.

## Mandate continuation

Do not copy rules from `constitution/`. Apply `constitution/AI_RULES.md` and `constitution/AI_ENFORCEMENT.md` §§1.2–1.4.

**Authorized outcome:** Replace the permanent absence check with a historical sentence and a checker for later trial files. Pin the selected work procedures and record one completed Spec Kit cycle. No merge, push, or publish.

**Acceptance observation:** The original test fails with `AssertionError: True is not false` on `research/benchmark_trials` existing. After the change, a good record is accepted and a bad record is rejected.

**Automatic continuation:** The operator authorized this outcome. Specify, plan, tasks, and implement continue without asking between tasks.

**Human decision required:** None inside this outcome. Merge and push remain unauthorized.

**AEP:** The plan file carries one schema-version-1 Autonomous Execution Plan.

## Assumptions

- Trial files are Markdown field lists, not JSON.
- This cycle does not run scenarios B5 through B8. It only makes a later run recordable.
