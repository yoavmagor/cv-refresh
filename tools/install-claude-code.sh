#!/usr/bin/env bash
# Install cv-refresh as a personal Claude Code skill.
#   ./tools/install-claude-code.sh          symlink (updates follow `git pull`)
#   ./tools/install-claude-code.sh --copy   copy instead
# Your settings/history will live in <skill>/user-data/ (git-ignored),
# or in $CV_REFRESH_HOME if you set it.
set -euo pipefail
SRC="$(cd "$(dirname "$0")/.." && pwd)/skills/cv-refresh"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/cv-refresh"
mkdir -p "$(dirname "$DEST")"
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  echo "Already exists: $DEST (remove it first to reinstall)"
  exit 1
fi
if [ "${1:-}" = "--copy" ]; then
  cp -R "$SRC" "$DEST"
  echo "Copied to $DEST"
else
  ln -s "$SRC" "$DEST"
  echo "Linked $DEST -> $SRC"
fi
python3 "$SRC/scripts/doctor.py" || true
