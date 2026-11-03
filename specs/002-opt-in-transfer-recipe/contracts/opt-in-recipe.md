# Contract: Opt-In Governed Work Transfer (Adopter-Facing)

**Version**: 1.0 (feature 002)  
**Normative procedure**: `usage/HOW_TO_IMPORT.md` § Opt-in work procedures  
**Verification implementation**: `ci/gate_tests/test_work_procedures.py` (`_copy_procedures` and related tests)

## Preconditions

- Adopter has imported governance baseline per `usage/ADOPTION_BUNDLES.md` (minimum: documents needed for enforcement references in entry skill).
- `KIT` environment variable points at a reviewed kit checkout at the intended revision.
- Path `vendor/superpowers/v7.0.1` MUST NOT exist in the adopter root.

## Operation: `transfer_first_install`

**Inputs**: kit root, adopter project root  
**Effects**:

1. Copy `vendor/superpowers/v7.0.1` as regular files.
2. Copy `.cursor/skills/governed-work/SKILL.md` as a regular file (not symlink).
3. Do not copy `.specify/presets/ai-governance/`. That preset is a separate command in `usage/HOW_TO_IMPORT.md` and is not part of this verified copy.
4. MUST NOT modify `AGENTS.md` or `governance/LOCAL_OVERLAY.md`.

**Postconditions**:

- `(cd vendor/superpowers/v7.0.1 && sha256sum -c SHA256SUMS)` exits 0.
- Entry skill is not a symlink.
- Distinctive host sentinel strings in fixture tests remain byte-identical.

## Operation: `transfer_repeat`

**Precondition**: `vendor/superpowers/v7.0.1` exists  
**Behavior**: MUST fail without overwriting (documented stop / `FileExistsError` in tests).

## Operation: `pin_upgrade`

**Inputs**: staged tree at `vendor/superpowers/v7.0.1.next` with valid sums  
**Effects**: Rename active to `.prev`, promote `.next` to active  
**Invariant**: `governance/LOCAL_OVERLAY.md` content unchanged.

## Operation: `pin_rollback`

**Precondition**: `vendor/superpowers/v7.0.1.prev` exists  
**Effects**: Replace active pin with previous tree  
**Postcondition**: Active pin matches pre-upgrade bytes; overlay unchanged; sums check passes.

## Non-goals (this contract)

- Does not authorize symlink import via `ci/import_bundle.py`.
- Does not imply native `specify workflow run` success.
- Does not replace constitutional enforcement or mandatory CI gates (FR-009).
