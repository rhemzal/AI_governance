# Adopting This Kit in Existing Projects

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

Use the current import path. Do not copy `constitution/` into the project root and do not turn on CI gates as part of copying files.

- Snapshot and host-file rules: [How to import](HOW_TO_IMPORT.md)
- One-slice method rollout after import: [Engineering methods adoption](ENGINEERING_METHODS_ADOPTION.md)
- Local conventions from the code already in the project: [Discover local constraints](ENGINEERING_METHODS_ADOPTION.md#discover-local-constraints)
- Product tests start at CI Maturity CM1 when the project already has tests. A CM0 import does not invent them.

An earlier draft of this page told adopters to add `constitution/` and optional warning gates first. That conflicted with the snapshot importer and the adoption contract.
