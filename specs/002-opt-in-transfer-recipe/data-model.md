# Data Model: Opt-In Governed Work Transfer Recipe

This feature is procedural documentation and verification, not a runtime database. Entities below are logical artifacts and states.

## Transfer recipe

| Field           | Description                                            | Validation                                                                |
| --------------- | ------------------------------------------------------ | ------------------------------------------------------------------------- |
| Prerequisites   | Minimum kit baseline import, host-owned files list     | Must name `AGENTS.md`, `governance/LOCAL_OVERLAY.md`, kit root resolution |
| Copy steps      | Ordered shell or documented actions                    | Must refuse existing `vendor/superpowers/v7.0.1`; no symlink bypass       |
| Verification    | Pin integrity and host sentinel checks                 | `sha256sum -c SHA256SUMS` on pin; host files unchanged                    |
| Upgrade path    | Stage `.next`, verify, swap, retain `.prev`            | Documented in HOW_TO_IMPORT                                               |
| Rollback path   | Restore `.prev` to active pin                          | Must not modify overlay content                                           |
| Activation      | Discovery of governed-work entry and procedure routing | Cross-ref method selector and ADR-0015                                    |
| Conflict policy | Repeat install and operator-edited transferred files   | Idempotency or explicit stop; overlay precedence unchanged                |

## Pinned work profile (coherent unit)

| Component                  | Host path (after transfer)                               | Notes                                                                |
| -------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------- |
| Procedure pin              | `vendor/superpowers/v7.0.1/`                             | Regular files only; `PIN.md`, `SHA256SUMS`                           |
| Entry skill                | `.cursor/skills/governed-work/SKILL.md`                  | Regular file; references pin commit id                               |
| Optional preset            | `.specify/presets/ai-governance/`                        | Separate command. Not part of the verified pin-and-skill copy.       |
| Not transferred by default | Other `.cursor/skills/*` symlinks, `.specify/workflows/` | Kit repo uses symlinks; adopter uses pin paths via entry skill table |

## Adopter repository states

```text
[no_profile] --first opt-in copy--> [profile_installed]
[profile_installed] --repeat copy--> conflict (FileExistsError / documented stop)
[profile_installed] --upgrade--> [profile_upgraded] (optional .prev retained)
[profile_upgraded] --rollback--> [profile_installed] (pin bytes restored)
```

Host-owned artifacts (`AGENTS.md`, `LOCAL_OVERLAY.md`, host CI config) are unchanged across all transitions except operator-initiated merge.

## Pin record

| Field           | Source                                 |
| --------------- | -------------------------------------- |
| Version label   | Directory name e.g. `v7.0.1`           |
| Upstream commit | Stated in `PIN.md` and entry skill     |
| Integrity       | `SHA256SUMS` over vendored skill files |

## Host-owned artifacts (precedence)

Always retain operator authority: project agent entry, local overlay, host test commands, adoption decision record. Recipe may recommend merge pointers only.
