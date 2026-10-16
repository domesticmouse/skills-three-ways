#!/usr/bin/env bash
set -euo pipefail

# Setup script for Scenario 02: libdaisy-skill-creation
# Prepares workspace with a shallow checkout of libDaisy

WORKSPACE_DIR="$(pwd)/workspace"
mkdir -p "$WORKSPACE_DIR"

echo "=== Setting up Scenario 02 workspace ==="
if [ ! -d "$WORKSPACE_DIR/libDaisy" ]; then
  echo "Cloning shallow libDaisy into $WORKSPACE_DIR/libDaisy..."
  git clone --depth 1 https://github.com/electro-smith/libDaisy.git "$WORKSPACE_DIR/libDaisy"
else
  echo "libDaisy already present in $WORKSPACE_DIR/libDaisy."
fi

echo "Workspace ready at: $WORKSPACE_DIR"
