#!/usr/bin/env bash
# Copy kit slim speckit-checklist skill into the current repo (fixes Cursor 5000-token SKILL.md warning).
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
KIT_SOURCE="${KIT_SOURCE:-}"
if [[ -z "$KIT_SOURCE" ]]; then
  echo "overlay-speckit-checklist-skill: set KIT_SOURCE to pinned AI_governance checkout" >&2
  exit 1
fi
skill=speckit-checklist
src="$KIT_SOURCE/.cursor/skills/$skill"
dst="$ROOT/.cursor/skills/$skill"
if [[ ! -f "$src/SKILL.md" ]] || [[ ! -f "$src/checklist-full-procedure.md" ]]; then
  echo "overlay-speckit-checklist-skill: missing kit files under $src" >&2
  exit 1
fi
mkdir -p "$dst"
if [[ "$(realpath "$src")" != "$(realpath "$dst")" ]]; then
  cp -L "$src/SKILL.md" "$src/checklist-full-procedure.md" "$dst/"
fi
manifest="$ROOT/.specify/integrations/cursor-agent.manifest.json"
if [[ -f "$manifest" ]]; then
  python3 - "$manifest" "$dst/SKILL.md" <<'PY'
import hashlib, json, sys
from pathlib import Path
manifest_path, skill_path = Path(sys.argv[1]), Path(sys.argv[2])
rel = ".cursor/skills/speckit-checklist/SKILL.md"
digest = hashlib.sha256(skill_path.read_bytes()).hexdigest()
data = json.loads(manifest_path.read_text(encoding="utf-8"))
data.setdefault("files", {})[rel] = digest
manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY
fi
echo "overlay-speckit-checklist-skill: installed slim $skill under $dst"
