#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# setup-daisy-experiment.sh
# 
# Standalone setup script for initializing an out-of-tree experiment workspace:
#   1. Creates a directory called 'daisy-experiment'
#   2. Initializes a new git repository inside daisy-experiment
#   3. Adds both libDaisy and DaisySP as git submodules
#   4. Seeds .agents/skills/agent-skills scaffolding
#   5. Writes PROMPTS.md OUTSIDE the daisy-experiment directory
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DEST_DIR=""
SHALLOW_CLONE=true
COPY_AGENT_SKILLS=true

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS] [BASE_DIR]

Creates a 'daisy-experiment' git repository with libDaisy and DaisySP submodules,
and places PROMPTS.md outside the repository.

Arguments:
  BASE_DIR                    Parent directory where daisy-experiment/ and PROMPTS.md
                              will be created (default: current working directory ".")

Options:
  -d, --dir <path>            Explicit parent directory path
      --full                  Perform full submodule clones instead of shallow (--depth 1)
      --no-agent-skills       Skip seeding .agents/skills/agent-skills
  -h, --help                  Show this help message

Submodules added:
  - libDaisy: https://github.com/electro-smith/libDaisy.git
  - DaisySP:  https://github.com/electro-smith/DaisySP.git

Layout created:
  <BASE_DIR>/
  ├── PROMPTS.md              (experiment prompts kept outside repository)
  └── daisy-experiment/       (git repository)
      ├── .gitmodules
      ├── libDaisy/           (submodule)
      ├── DaisySP/            (submodule)
      ├── .agents/skills/     (agent skills scaffolding)
      └── README.md
EOF
  exit 0
}

# Parse options
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      ;;
    -d|--dir)
      DEST_DIR="$2"
      shift 2
      ;;
    --full)
      SHALLOW_CLONE=false
      shift
      ;;
    --no-agent-skills)
      COPY_AGENT_SKILLS=false
      shift
      ;;
    -*)
      echo "Error: Unknown option '$1'" >&2
      usage
      ;;
    *)
      if [[ -z "$DEST_DIR" ]]; then
        DEST_DIR="$1"
        shift
      else
        echo "Error: Unexpected argument '$1'" >&2
        usage
      fi
      ;;
  esac
done

DEST_DIR="${DEST_DIR:-.}"
mkdir -p "$DEST_DIR"
DEST_DIR="$(cd "$DEST_DIR" && pwd)"

# Resolve experiment dir and prompts location
if [[ "$(basename "$DEST_DIR")" == "daisy-experiment" ]]; then
  EXPERIMENT_DIR="$DEST_DIR"
  OUTSIDE_DIR="$(dirname "$DEST_DIR")"
else
  EXPERIMENT_DIR="$DEST_DIR/daisy-experiment"
  OUTSIDE_DIR="$DEST_DIR"
fi

echo "=========================================================="
echo " Setting up Daisy Skills Experiment"
echo " Experiment repo: $EXPERIMENT_DIR"
echo " Prompts path:    $OUTSIDE_DIR/PROMPTS.md"
echo " Shallow clones:  $SHALLOW_CLONE"
echo "=========================================================="

# 1. Initialize git repository in daisy-experiment
mkdir -p "$EXPERIMENT_DIR"
cd "$EXPERIMENT_DIR"

if [[ ! -d ".git" ]]; then
  echo "Initializing git repository in $EXPERIMENT_DIR..."
  git init -b main 2>/dev/null || { git init && git checkout -B main; }
  echo "✔ Git repository initialized."
else
  echo "✔ Existing git repository found in $EXPERIMENT_DIR."
fi

# 2. Add libDaisy submodule
LIBDAISY_URL="https://github.com/electro-smith/libDaisy.git"
if [[ -d "libDaisy/.git" || -f "libDaisy/.git" ]]; then
  echo "✔ libDaisy submodule already exists."
else
  echo "Adding libDaisy submodule ($LIBDAISY_URL)..."
  SUBMODULE_ARGS=()
  if [[ "$SHALLOW_CLONE" == true ]]; then
    SUBMODULE_ARGS+=(--depth 1)
  fi
  git submodule add "${SUBMODULE_ARGS[@]}" "$LIBDAISY_URL" libDaisy
  echo "✔ libDaisy submodule added."
fi

# 3. Add DaisySP submodule
DAISYSP_URL="https://github.com/electro-smith/DaisySP.git"
if [[ -d "DaisySP/.git" || -f "DaisySP/.git" ]]; then
  echo "✔ DaisySP submodule already exists."
else
  echo "Adding DaisySP submodule ($DAISYSP_URL)..."
  SUBMODULE_ARGS=()
  if [[ "$SHALLOW_CLONE" == true ]]; then
    SUBMODULE_ARGS+=(--depth 1)
  fi
  git submodule add "${SUBMODULE_ARGS[@]}" "$DAISYSP_URL" DaisySP
  echo "✔ DaisySP submodule added."
fi

# 4. Scaffold .agents/skills for the experiment
SKILLS_DIR="$EXPERIMENT_DIR/.agents/skills"
mkdir -p "$SKILLS_DIR"

if [[ "$COPY_AGENT_SKILLS" == true ]]; then
  FOUND_AGENT_SKILLS=""
  SEARCH_PATHS=(
    "$SCRIPT_DIR/../.agents/skills/agent-skills"
    "$SCRIPT_DIR/.agents/skills/agent-skills"
    "/Users/brett/Documents/GitHub/skills-three-ways/.agents/skills/agent-skills"
    "/Users/brett/Documents/GitHub/reverse-engineering-gamma/.agents/skills/agent-skills"
  )

  for p in "${SEARCH_PATHS[@]}"; do
    if [[ -d "$p" && -f "$p/SKILL.md" ]]; then
      FOUND_AGENT_SKILLS="$p"
      break
    fi
  done

  if [[ -n "$FOUND_AGENT_SKILLS" ]]; then
    echo "Seeding agent-skills meta-skill from $FOUND_AGENT_SKILLS..."
    rm -rf "$SKILLS_DIR/agent-skills"
    cp -r "$FOUND_AGENT_SKILLS" "$SKILLS_DIR/agent-skills"
    echo "✔ agent-skills seeded."
  else
    echo "Local agent-skills not found. Fetching from skills-three-ways repo..."
    TMP_CLONE="$(mktemp -d)"
    if git clone --depth 1 https://github.com/domesticmouse/skills-three-ways.git "$TMP_CLONE" 2>/dev/null; then
      if [[ -d "$TMP_CLONE/.agents/skills/agent-skills" ]]; then
        cp -r "$TMP_CLONE/.agents/skills/agent-skills" "$SKILLS_DIR/"
        echo "✔ agent-skills fetched and seeded."
      fi
    else
      echo "Note: Could not fetch agent-skills automatically; proceeding with empty skills directory."
    fi
    rm -rf "$TMP_CLONE"
  fi
fi

# 5. Create repository README inside daisy-experiment
cat << 'EOF' > "$EXPERIMENT_DIR/README.md"
# Daisy Skills Creation Experiment

This repository contains submodules of the official Electro-Smith Daisy C++ audio libraries:
- `libDaisy/`: Hardware abstraction layer and board support package.
- `DaisySP/`: DSP synthesis and audio processing library.

## Goal
Author high-signal Agent Skills for each library using Antigravity:
1. `libdaisy-guide`: System architecture, peripheral taxonomy (`sys/`, `per/`, `dev/`, `hid/`, `ui/`, `util/`), audio callback double-buffered DMA, and STM32H7 memory map (DTCM, SRAM1 DMA, SDRAM).
2. `daisysp-guide`: DSP modules, zero-allocation real-time audio callback constraints, audio block processing, and licensing (MIT core vs LGPL submodules).

## Output Skills Directory
Place authored skills in:
- `.agents/skills/<skill-name>/SKILL.md`

*(Note: Experiment prompts are maintained outside this repository in `../PROMPTS.md`)*
EOF

# Initial git commit if repo has unstaged/uncommitted files
if git status --porcelain | grep -q .; then
  echo "Creating initial commit in daisy-experiment..."
  git add .
  # Check if git user is set; if not set temporary author for initial commit
  if ! git config user.name >/dev/null 2>&1; then
    git -c user.name="Daisy Experimenter" -c user.email="experimenter@local" commit -m "Initial commit with libDaisy and DaisySP submodules" >/dev/null
  else
    git commit -m "Initial commit with libDaisy and DaisySP submodules" >/dev/null
  fi
  echo "✔ Initial commit created."
fi

# 6. Write PROMPTS.md OUTSIDE the daisy-experiment directory
PROMPTS_FILE="$OUTSIDE_DIR/PROMPTS.md"
cat << 'EOF' > "$PROMPTS_FILE"
# Experiment Prompts for Daisy Skill Creation

Use these prompts with Antigravity / AGY inside the `daisy-experiment/` workspace.

---

### Experiment 1: Authoring `libdaisy-guide`
```text
Inspect the libDaisy/ repository in this workspace. Produce a comprehensive architectural guide on how to build firmware with libDaisy, detailing the hardware peripheral taxonomy, STM32H7 memory map (DTCM, SRAM1 DMA, SDRAM), audio callback mechanisms, and initialization patterns. Package this as an Agent Skill named `libdaisy-guide` in `.agents/skills/libdaisy-guide/SKILL.md`.
```

---

### Experiment 2: Authoring `daisysp-guide`
```text
Inspect the DaisySP/ repository in this workspace. Produce a comprehensive DSP developer runbook and catalog for audio synthesis, filter algorithms, effects, and zero-allocation constraints in real-time callbacks. Document module selection, parameter ranges, and the licensing distinction between MIT core and LGPL submodules. Package this as an Agent Skill named `daisysp-guide` in `.agents/skills/daisysp-guide/SKILL.md`.
```

---

### Experiment Workflow Tip
1. Open the repository in your agent / editor:
   ```bash
   cd daisy-experiment
   ```
2. Run your agent with the prompt for `libdaisy-guide`.
3. Validate the generated skill using the seeded validator:
   ```bash
   python3 .agents/skills/agent-skills/scripts/validate-skill.py .agents/skills/libdaisy-guide
   ```
4. Repeat for `daisysp-guide`.
EOF
echo "✔ Prompts written to $PROMPTS_FILE (outside daisy-experiment)."

echo ""
echo "=========================================================="
echo " Setup complete!"
echo " Workspace git repo: $EXPERIMENT_DIR"
echo " Prompts file:       $PROMPTS_FILE"
echo ""
echo " Submodules:"
echo "   - $EXPERIMENT_DIR/libDaisy"
echo "   - $EXPERIMENT_DIR/DaisySP"
echo ""
echo " To start your experiment:"
echo "   cd \"$EXPERIMENT_DIR\""
echo "=========================================================="
