#!/usr/bin/env bash
set -euo pipefail

# Setup script for Scenario 05: drum-synth-without-skills
# Prepares workspace with checkouts of libDaisy and DaisySP, but explicitly NO agent skills

WORKSPACE_DIR="$(pwd)/workspace"
mkdir -p "$WORKSPACE_DIR"

echo "=== Setting up Scenario 05 workspace (WITHOUT skills) ==="

# 1. Clone libDaisy
if [ ! -d "$WORKSPACE_DIR/libDaisy" ]; then
  echo "Cloning shallow libDaisy into $WORKSPACE_DIR/libDaisy..."
  git clone --depth 1 https://github.com/electro-smith/libDaisy.git "$WORKSPACE_DIR/libDaisy"
fi

# 2. Clone DaisySP
if [ ! -d "$WORKSPACE_DIR/DaisySP" ]; then
  echo "Cloning shallow DaisySP into $WORKSPACE_DIR/DaisySP..."
  git clone --depth 1 https://github.com/electro-smith/DaisySP.git "$WORKSPACE_DIR/DaisySP"
fi

# 3. Ensure no local skills are present
rm -rf "$WORKSPACE_DIR/.agents" "$WORKSPACE_DIR/.gemini"

echo "Workspace ready with libDaisy and DaisySP (NO skills) at: $WORKSPACE_DIR"
