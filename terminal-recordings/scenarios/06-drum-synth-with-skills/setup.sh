#!/usr/bin/env bash
set -euo pipefail

# Setup script for Scenario 06: drum-synth-with-skills
# Prepares workspace with checkouts of libDaisy, DaisySP, and ALL 7 Gamma Agent Skills

WORKSPACE_DIR="$(pwd)/workspace"
mkdir -p "$WORKSPACE_DIR" "$WORKSPACE_DIR/.agents/skills"

echo "=== Setting up Scenario 06 workspace (WITH all 7 skills) ==="

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

# 3. Source all 7 skills
SKILLS=(
  "libdaisy-guide"
  "daisysp-guide"
  "gamma-firmware-flash"
  "gamma-firmware-restore"
  "gamma-pinout"
  "gamma-hardware-controls"
  "gamma-usb-connectivity"
)

SKILLS_SRC="${SKILLS_SRC:-}"
if [ -z "$SKILLS_SRC" ]; then
  if [ -d "../../../.agents/skills" ] && [ -d "../../../.agents/skills/libdaisy-guide" ]; then
    SKILLS_SRC="../../../.agents/skills"
  elif [ -d "/Users/brett/Documents/GitHub/skills-three-ways/.agents/skills" ] && [ -d "/Users/brett/Documents/GitHub/skills-three-ways/.agents/skills/libdaisy-guide" ]; then
    SKILLS_SRC="/Users/brett/Documents/GitHub/skills-three-ways/.agents/skills"
  elif [ -d "../../../../reverse-engineering-gamma/.agents/skills" ]; then
    SKILLS_SRC="../../../../reverse-engineering-gamma/.agents/skills"
  elif [ -d "../../../../../reverse-engineering-gamma/.agents/skills" ]; then
    SKILLS_SRC="../../../../../reverse-engineering-gamma/.agents/skills"
  fi
fi

if [ -n "$SKILLS_SRC" ] && [ -d "$SKILLS_SRC/libdaisy-guide" ]; then
  echo "Copying 7 skills from local $SKILLS_SRC..."
  for skill in "${SKILLS[@]}"; do
    if [ -d "$SKILLS_SRC/$skill" ]; then
      cp -r "$SKILLS_SRC/$skill" "$WORKSPACE_DIR/.agents/skills/"
    else
      echo "Warning: $skill not found in $SKILLS_SRC"
    fi
  done
else
  echo "Local skills directory not found. Cloning reverse-engineering-gamma..."
  TMP_CLONE="$(mktemp -d)"
  git clone --depth 1 https://github.com/domesticmouse/reverse-engineering-gamma.git "$TMP_CLONE"
  for skill in "${SKILLS[@]}"; do
    if [ -d "$TMP_CLONE/.agents/skills/$skill" ]; then
      cp -r "$TMP_CLONE/.agents/skills/$skill" "$WORKSPACE_DIR/.agents/skills/"
    fi
  done
  rm -rf "$TMP_CLONE"
fi

echo "Workspace ready with libDaisy, DaisySP, and all 7 skills at: $WORKSPACE_DIR"
