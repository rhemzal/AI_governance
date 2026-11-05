#!/bin/bash
set -eu
root="${APP_ROOT:-/app}"
python3 - "$root" <<'PY'
import pathlib, sys
root = pathlib.Path(sys.argv[1])
path = root / 'usage/ADOPTION_SCOPE_AND_HOSTS.md'
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text('# Adoption scope, authorization, and hosts\n\n_Provenance: fixture slice for the Harbor C2 control._\n\nThis page routes operators before they pick an install mode.\n\nA Harbor trial fixture is a disposable copy. It is not adoption of this kit.\n', encoding='utf-8')
PY
