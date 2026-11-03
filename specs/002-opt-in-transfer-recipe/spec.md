# Feature Specification: Opt-In Governed Work Transfer Recipe

**Feature Branch**: `002-opt-in-transfer-recipe`

**Created**: 2026-11-03

**Status**: Draft

**Input**: User description: "Deliver a pinned opt-in transfer recipe for the existing governed work procedures, preserving adopter instructions and local policy."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Adopter enables governed work without losing local guidance (Priority: P1)

A team that already imported governance documentation wants the pinned governed-work procedures (debugging, plan execution, verification, review routing) available in their agent host. They follow an explicit opt-in recipe that adds only the work-procedure profile and its pin. Their existing project instructions, host configuration, and local policy overlay remain authoritative and unchanged except where they deliberately merge kit guidance.

**Why this priority**: Without safe transfer, the pilot capability stays confined to the kit repository and adopters cannot reuse the procedures without risking overwrite of host-owned files.

**Independent Test**: From a disposable adopter fixture with distinctive host instructions and a local overlay, apply the recipe once and confirm those distinctive files are preserved byte-for-byte or merge as documented, while the governed-work entry point and pin become discoverable.

**Acceptance Scenarios**:

1. **Given** a clean adopter with custom agent instructions and a filled local overlay, **When** the adopter completes the opt-in transfer recipe, **Then** custom instructions and overlay content remain intact and the governed-work entry point is present and discoverable from documented paths.
2. **Given** a completed opt-in transfer, **When** an operator asks the agent to debug a failing check using governed work, **Then** the agent can reach the entry point and follow the pinned procedure routing without copying undocumented symlinks that bypass import safety rules.

---

### User Story 2 - Maintainer documents a repeatable, pinned recipe (Priority: P1)

A kit maintainer publishes a single transfer recipe that names what is transferred (pinned third-party procedures, entry skill, optional preset and workflow references), what stays host-owned, and how pin integrity is verified. The recipe aligns with existing import bundle guidance and does not require adopters to change constitutional rules or mandatory gates.

**Why this priority**: The recipe is the deliverable; undocumented copying of active host links fails import safety and bundle coverage today.

**Independent Test**: A reader with no repository checkout can follow the recipe outline, identify required vs optional artifacts, and know which existing adoption documents govern conflicts and precedence.

**Acceptance Scenarios**:

1. **Given** the published recipe, **When** a maintainer reviews it against adoption import guidance, **Then** every transferred artifact is either covered by an documented opt-in path or explicitly excluded from default bundles with rationale.
2. **Given** the published recipe, **When** a maintainer checks pin claims, **Then** the recipe states how to verify pin version and integrity without modifying vendored upstream sources.

---

### User Story 3 - Adopter repeats install, upgrade, or rolls back safely (Priority: P2)

An adopter who already applied the recipe runs it again after a kit update, or rolls back to a previous pin. The recipe explains how to detect ownership conflicts, preserve local policy, and restore a prior pin without orphaning host configuration.

**Why this priority**: Real adoption includes updates; a one-shot copy instruction does not meet operational needs.

**Independent Test**: Apply the recipe twice on the same fixture (second pass after a deliberate local edit to a transferred file), then perform a documented upgrade and rollback sequence while checking pin and local overlay survival.

**Acceptance Scenarios**:

1. **Given** an adopter that already completed opt-in transfer, **When** the recipe is applied again, **Then** the operator receives clear conflict or idempotency behavior and local overlay precedence is unchanged.
2. **Given** a pin upgrade path documented in the recipe, **When** the adopter upgrades and then rolls back per recipe, **Then** the selected pin and local policy files match the documented end states and verification steps pass.

---

### Edge Cases

- Adopter uses a copy import while active host files use links that the standard importer rejects; recipe must not instruct bypassing symlink safety.
- Kit root path differs from project root after import; recipe must require that governance and vendored pin paths still resolve.
- Adopter has not imported `standard` or `full` bundles; recipe states minimum kit content needed for governed work.
- Adopter merges kit agent guidance with existing instructions; recipe references overlay precedence rather than silent overwrite.
- Repeat transfer after operator edited a transferred skill file; recipe documents detect-and-resolve without deleting local policy.
- Host environment unsupported for governed workflow; recipe records limitation without claiming universal host support.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The deliverable MUST include an opt-in transfer recipe that is explicit about what is added, what is never overwritten, and what requires operator merge decisions.
- **FR-002**: The recipe MUST preserve adopter host instructions and local policy overlay precedence as defined in existing kit adoption documentation.
- **FR-003**: The recipe MUST transfer the pinned governed-work profile (entry routing and vendored procedure pin) as a coherent unit with integrity verification steps.
- **FR-004**: The recipe MUST use existing kit import and bundle mechanisms as the primary path; any optional bundle or manifest change MUST be the smallest change that makes the opt-in path reproducible and MUST NOT weaken symlink rejection or other importer safety contracts.
- **FR-005**: The recipe MUST document activation: how an operator or agent discovers and invokes governed work after transfer, including proportionality rules already stated for documentation-only changes versus behavior changes.
- **FR-006**: The recipe MUST include repeatable-install behavior: idempotency or explicit conflict detection when transfer runs more than once.
- **FR-007**: The recipe MUST include upgrade and rollback guidance for the pinned procedure version that preserves local policy and recorded pin identity.
- **FR-008**: Verification for the recipe MUST be executable in a disposable adopter fixture before any named downstream production repository trial; downstream trial remains optional and separately authorized.
- **FR-009**: The recipe MUST NOT present governed-work procedures as new mandatory constitutional requirements or replace existing enforcement authority.
- **FR-010**: Documentation MUST cross-reference existing import guides and bundle selection so adopters do not maintain two conflicting sources of truth for baseline vs overlay.

### Key Entities *(include if feature involves data)*

- **Transfer recipe**: Human- and agent-readable procedure listing prerequisites, steps, verification, upgrade, rollback, and conflict handling.
- **Pinned work profile**: The governed-work entry point, linked procedure skills, vendored upstream pin, and optional preset/workflow references that activate Spec Kit governed flows.
- **Adopter repository**: Target project containing governance baseline, host agent configuration, and optional local overlay.
- **Host-owned artifacts**: Agent instruction entry points, host-specific configuration, and local overlay content that retain precedence over kit defaults.
- **Pin record**: Version identity and integrity evidence for the vendored procedure source used by the profile.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In a disposable adopter fixture, **100%** of deliberately distinctive host instruction and local overlay content survives a first-time opt-in transfer when following the recipe (no undocumented overwrites).
- **SC-002**: In the same fixture, an operator can complete a small useful change (documented smoke task) using governed-work discovery within **one session** without manual repair of broken relative paths to governance or vendored pin content.
- **SC-003**: Repeat application of the recipe on the same fixture produces **documented** conflict or idempotency outcomes in **100%** of trial runs (no silent corruption of host-owned files).
- **SC-004**: Upgrade-then-rollback trial on the fixture restores pin identity and local overlay to documented end states in **100%** of trial runs.
- **SC-005**: At least **two** independent readers (maintainer and adopter role) can answer "what stays mine vs what the kit adds" from the recipe alone with matching answers on a structured checklist of **ten** items.

## Assumptions

- Governed-work procedures are already pinned and exercised in the kit repository; this feature documents transfer and activation, not re-piloting upstream procedure content.
- The policy snapshot still uses `ci/import_bundle.py`. The procedure pin does not: that helper rejects symlinks, and the active skill links are symlinks. The opt-in path copies regular files and leaves the symlink check unchanged.
- Default import bundles may omit active profile paths; the recipe may propose optional bundle or manifest adjustments only after a local-only recipe proves a reproducible gap.
- Cursor-class agent hosts are the first supported activation target; other hosts are out of scope unless explicitly tested and documented later.
- Disposable adopter fixtures are sufficient evidence for recipe correctness; trials on named downstream repositories require separate operator authorization.
- Constitutional enforcement and required CI gates remain unchanged; opt-in transfer is additive and advisory unless the adopter explicitly adopts further kit policy.
- Merge semantics for agent instruction entry points follow existing kit import guidance (append/merge, not replace) unless the adopter chooses a documented override.
