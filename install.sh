#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="github-ai-arsenal"
SOURCE_DIR=""
TMP_DIR=""

if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "$(dirname "${BASH_SOURCE[0]}")/SKILL.md" ]; then
  SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
  REPO="${GH_ARSENAL_REPO:-fazah-arsenal/github-ai-arsenal}"
  BRANCH="${GH_ARSENAL_BRANCH:-main}"
  TMP_DIR="$(mktemp -d)"
  echo "Downloading $SKILL_NAME from https://github.com/$REPO ($BRANCH)..."
  curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" | tar -xz -C "$TMP_DIR"
  SOURCE_DIR="$(find "$TMP_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
fi

TARGETS=(
  "$HOME/.agents/skills/$SKILL_NAME"
  "$HOME/.gemini/config/skills/$SKILL_NAME"
)
for extra in ".claude/skills" ".codex/skills" ".cursor/skills"; do
  if [ -d "$HOME/$extra" ]; then
    TARGETS+=("$HOME/$extra/$SKILL_NAME")
  fi
done

for dest in "${TARGETS[@]}"; do
  echo "Installing $SKILL_NAME -> $dest"
  rm -rf "$dest"
  mkdir -p "$dest"
  cp "$SOURCE_DIR/SKILL.md" "$dest/"
  cp "$SOURCE_DIR/README.md" "$dest/"
  cp -R "$SOURCE_DIR/scripts" "$dest/scripts"
  cp -R "$SOURCE_DIR/references" "$dest/references"
  [ -d "$SOURCE_DIR/examples" ] && cp -R "$SOURCE_DIR/examples" "$dest/examples"
  chmod +x "$dest/scripts/gh_arsenal.py"
done

[ -n "$TMP_DIR" ] && rm -rf "$TMP_DIR"

# Install short global CLI command: `fazah`
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/fazah" <<'EOF'
#!/usr/bin/env bash
exec python3 "$HOME/.agents/skills/github-ai-arsenal/scripts/gh_arsenal.py" "$@"
EOF
chmod +x "$HOME/.local/bin/fazah"

echo "Installed $SKILL_NAME (20,078+ GitHub tools, Native MCP Server & short 'fazah' CLI) successfully!"
echo "Try now: fazah doc | fazah r 'telegram bot' | fazah m -q 'postgres'"
