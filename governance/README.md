# Governance

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Purpose

This directory contains local governance overlays and repository-specific policy extensions.

## Contents

- **[LOCAL_OVERLAY.md](LOCAL_OVERLAY.md)** — Active overlay for **this upstream repository** only. Listed in `kit-manifest.yml` `exclude` so bundle import does not copy it into an adopter snapshot.
- **[LOCAL_OVERLAY_TEMPLATE.md](LOCAL_OVERLAY_TEMPLATE.md)** — Template for adopters. Copy to `governance/LOCAL_OVERLAY.md` at the **project root** and customize.

## Testing

For information on running tests in repositories that adopt this governance kit, see:

**[DEVELOPMENT.md](../DEVELOPMENT.md)** — Testing Quickstart with setup instructions and canonical test commands.

## Related Documents

- [constitution/AI_RULES.md](../constitution/AI_RULES.md) — Core AI governance rules
- [constitution/AI_ENFORCEMENT_DAILY.md](../constitution/AI_ENFORCEMENT_DAILY.md) — Daily AI enforcement checklist
- [ci/TEST_GATES.md](../ci/TEST_GATES.md) — Test CI gates and principles
- [usage/LOCAL_OVERLAY_AND_PRECEDENCE.md](../usage/LOCAL_OVERLAY_AND_PRECEDENCE.md) — How local overlays work
