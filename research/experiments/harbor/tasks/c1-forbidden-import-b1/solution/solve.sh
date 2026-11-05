#!/bin/bash
set -eu
root="${APP_ROOT:-/app}"
python3 - "$root" <<'PY'
import pathlib, sys
root = pathlib.Path(sys.argv[1])
path = root / 'decision.md'
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text('Refused: first import refuses an existing destination without --readopt.\nLOCAL_OVERLAY: first import refuses an existing destination.\n', encoding='utf-8')
PY
