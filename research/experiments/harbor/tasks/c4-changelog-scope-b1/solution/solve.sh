#!/bin/bash
set -eu
root="${APP_ROOT:-/app}"
python3 - "$root" <<'PY'
import pathlib, sys
root = pathlib.Path(sys.argv[1])
path = root / 'CHANGELOG.md'
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text('# Changelog\n\n## Unreleased\n\n- Harbor scenario backlog (specs/006): maintainer C3/C4 controls.\n', encoding='utf-8')
path = root / 'loaded-overlay.md'
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text('No LOCAL_OVERLAY import or symlink row applies to this CHANGELOG-only edit.\n', encoding='utf-8')
PY
