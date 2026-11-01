#!/usr/bin/env bash
# Temporary candidate-job rejection. Removed by the repair commit.
# The git boundary keeps using the already projected policy.json, which does
# not call this script. CI runs sync-policy.sh first, so this command is what
# verify.sh executes on the pull request.
set -euo pipefail
echo "intentional candidate-job rejection: advisory verify.sh must fail this run" >&2
exit 1
