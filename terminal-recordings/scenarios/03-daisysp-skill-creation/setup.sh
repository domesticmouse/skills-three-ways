#!/usr/bin/env bash
set -euo pipefail

# Setup script for Scenario 03: daisysp-skill-creation
# Prepares workspace with a shallow checkout of DaisySP

WORKSPACE_DIR="$(pwd)/workspace"
mkdir -p "$WORKSPACE_DIR"

echo "=== Setting up Scenario 03 workspace ==="
if [ ! -d "$WORKSPACE_DIR/DaisySP" ]; then
  echo "Cloning shallow DaisySP into $WORKSPACE_DIR/DaisySP..."
  git clone --depth 1 https://github.com/electro-smith/DaisySP.git "$WORKSPACE_DIR/DaisySP"
else
  echo "DaisySP already present in $WORKSPACE_DIR/DaisySP."
fi

echo "Workspace ready at: $WORKSPACE_DIR"
