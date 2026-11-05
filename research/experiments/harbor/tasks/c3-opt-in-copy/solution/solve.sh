#!/bin/bash
set -eu
root="${APP_ROOT:-/app}"
mkdir -p "$root/opt-in/copy"
cp -aL "$root/opt-in/pin/." "$root/opt-in/copy/"
cat > "$root/copy-report.md" <<'EOF'
Applied opt-in copy using cp -aL per LOCAL_OVERLAY symlink exception.
Materialized files under opt-in/copy/ without changing ci/import_bundle.py.
EOF
