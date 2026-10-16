#!/usr/bin/env bash
set -euo pipefail

# Setup script for Scenario 04: reverse-engineering-plan
# Prepares workspace with checkouts of libDaisy, DaisySP, and the two library skills

WORKSPACE_DIR="$(pwd)/workspace"
mkdir -p "$WORKSPACE_DIR" "$WORKSPACE_DIR/.agents/skills"

echo "=== Setting up Scenario 04 workspace ==="

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

# 3. Source the two library skills
SKILLS_SRC=""
if [ -d "../../../.agents/skills" ] && [ -d "../../../.agents/skills/libdaisy-guide" ]; then
  SKILLS_SRC="../../../.agents/skills"
elif [ -d "../../../../reverse-engineering-gamma/.agents/skills" ]; then
  SKILLS_SRC="../../../../reverse-engineering-gamma/.agents/skills"
elif [ -d "../../../../../reverse-engineering-gamma/.agents/skills" ]; then
  SKILLS_SRC="../../../../../reverse-engineering-gamma/.agents/skills"
fi

if [ -n "$SKILLS_SRC" ] && [ -d "$SKILLS_SRC/libdaisy-guide" ]; then
  echo "Copying library skills from local $SKILLS_SRC..."
  cp -r "$SKILLS_SRC/libdaisy-guide" "$WORKSPACE_DIR/.agents/skills/"
  cp -r "$SKILLS_SRC/daisysp-guide" "$WORKSPACE_DIR/.agents/skills/"
else
  echo "Local skills directory not found. Cloning reverse-engineering-gamma..."
  TMP_CLONE="$(mktemp -d)"
  git clone --depth 1 https://github.com/domesticmouse/reverse-engineering-gamma.git "$TMP_CLONE"
  cp -r "$TMP_CLONE/.agents/skills/libdaisy-guide" "$WORKSPACE_DIR/.agents/skills/"
  cp -r "$TMP_CLONE/.agents/skills/daisysp-guide" "$WORKSPACE_DIR/.agents/skills/"
  rm -rf "$TMP_CLONE"
fi

echo "Workspace ready with libDaisy, DaisySP, and 2 library skills at: $WORKSPACE_DIR"
