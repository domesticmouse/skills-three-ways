#!/usr/bin/env bash
set -euo pipefail

# Scenario 03: daisysp-skill-creation
# Recommended terminal size: 116 columns x 30 rows in Ghostty

CAST_NAME="daisysp-skill-creation.cast"
TARGET_DIR="../../../slides/public/casts"
mkdir -p "$TARGET_DIR"

./setup.sh

echo ""
echo "=== Recording Scenario 03: daisysp-skill-creation ==="
echo "Target workspace: $(pwd)/workspace"
echo "Prompt to use in AGY:"
cat PROMPT.md
echo ""
echo "Press Enter to start recording in workspace/ (or Ctrl+C to abort)..."
read -r

cd workspace
asciinema rec -i 2.0 --overwrite "../$CAST_NAME"
cd ..

cp "$CAST_NAME" "$TARGET_DIR/$CAST_NAME"
echo "Saved to $CAST_NAME and copied to $TARGET_DIR/$CAST_NAME"
