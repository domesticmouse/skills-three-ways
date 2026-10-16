#!/usr/bin/env bash
set -euo pipefail

# Scenario 01: What Are Agent Skills?
# Recommended terminal size: 116 columns x 30 rows in Ghostty

CAST_NAME="what-are-agent-skills.cast"
TARGET_DIR="../../../slides/public/casts"
mkdir -p "$TARGET_DIR"

echo "=== Recording Scenario 01: What Are Agent Skills? ==="
echo "Prompt to use in AGY:"
cat PROMPT.md
echo ""
echo "Press Enter to start recording (or Ctrl+C to abort)..."
read -r

asciinema rec -i 2.0 --overwrite "$CAST_NAME"

cp "$CAST_NAME" "$TARGET_DIR/$CAST_NAME"
echo "Saved to $CAST_NAME and copied to $TARGET_DIR/$CAST_NAME"
