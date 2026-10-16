# Terminal recording inventory and scenario scripts

Type: grilling
Status: resolved
Blocked by: 03

## Question

What is the exact checklist of terminal recordings required across the presentation, mapping each to its corresponding slide, and what specific AGY CLI prompts and mock/repro scripts are needed to record the missing recordings (LibDaisy research, DaisySP research, firmware planning, and drum synth without vs with skills)?

## Answer

### 1. Terminal Recordings Inventory & Slide Beat Mapping

The presentation incorporates 6 asciinema terminal recordings, each paired across a 2-slide beat (Intro Card on Slide N $\to$ Full-viewport click-to-play replay on Slide N+1):

| # | Cast File Name | Slide Beat | Act & Context | Prompt Summary | Target Workspace |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | `what-are-agent-skills.cast` | S04–S05 | Act 1: Primer | "What are agent skills?" | Empty / reference workspace |
| **02** | `libdaisy-skill-creation.cast` | S24–S25 | Act 3: Way 1 | Inspect `libDaisy/` source tree, report architecture, create `libdaisy-guide` | Shallow checkout of `libDaisy` |
| **03** | `daisysp-skill-creation.cast` | S29–S30 | Act 3: Way 1 | Inspect `DaisySP/` source tree, report real-time audio rules, create `daisysp-guide` | Shallow checkout of `DaisySP` |
| **04** | `reverse-engineering-plan.cast` | S49–S50 | Act 5: Way 3 | Collaborate on 6-phase diagnostic probing plan (`PLAN.md`) | `libDaisy` + `DaisySP` + 2 library skills |
| **05** | `drum-synth-without-skills.cast` | S73–S74 | Act 7: Payoff (A/B) | Build 7-voice drum synth for Gamma mini synth (No skills installed) | `libDaisy` + `DaisySP` (zero skills) |
| **06** | `drum-synth-with-skills.cast` | S76–S77 | Act 7: Payoff (A/B) | Build 7-voice drum synth for Gamma mini synth (All 7 skills installed) | `libDaisy` + `DaisySP` + all 7 skills |

### 2. Prompt Specifications

- **Scenario 01**: `"What are agent skills?"`
- **Scenario 02**: `"Inspect the libDaisy/ repository in this workspace. Produce a comprehensive architectural report on how to build firmware with libDaisy, detailing the hardware peripheral taxonomy, STM32H7 memory map, and initialization patterns, and format it as an Agent Skill named libdaisy-guide."`
- **Scenario 03**: `"Inspect the DaisySP/ repository in this workspace. Review the DSP synthesis modules, extract the 5 real-time audio constraints, and convert the findings into an Agent Skill named daisysp-guide with a fast module catalog."`
- **Scenario 04**: `"We have a Gamma mini synth built on the Daisy Seed 2 DFM (STM32H750IBK6), but no schematics or pinout table. Using our libdaisy-guide and daisysp-guide skills, design a phased, safe reverse-engineering plan (PLAN.md) starting with firmware backup and progressing through I2C scanning, ADC pot/joystick mapping, digital key scanning, and audio amp discovery."`
- **Scenarios 05 & 06 (A/B Experiment)**: Exact identical prompt for an unadulterated comparison:
  `"Write and build a complete C++ firmware for a 7-voice drum synth on the this.is.NOISE Gamma mini synth using libDaisy and DaisySP, mapping the drum voices to the front keys and filter controls to the knobs."`
  *(Note: Hardware USB flashing is omitted from the AGY prompt so it can be performed live on stage on Slide 79).*

### 3. Scenario Runner Architecture (`terminal-recordings/scenarios/`)

Each scenario is packaged into a self-contained directory containing:
- `PROMPT.md`: Exact prompt text ready to copy-paste into `agy`.
- `setup.sh`: Automated workspace preparation (shallow git cloning of `libDaisy`/`DaisySP`, copying skills from `../reverse-engineering-gamma/.agents/skills/` or git fallback).
- `record.sh`: Interactive runner that executes `setup.sh`, prompts the presenter, and records via `asciinema rec -i 2.0 --overwrite <cast-name>` in Ghostty (116 cols x 30 rows), auto-deploying the result into `slides/public/casts/`.

### 4. Handling Varied Session Runtimes

- Standard short recordings (`01`, `05`) run in ~30–60s real-time (~15–30s at 2x playback).
- In-depth library exploration (`02`, `03`) and full multi-skill synthesis (`06`) run naturally longer (up to ~10 minutes).
- Playback pacing is managed in Slidev via `:speed` multipliers (e.g. `:speed="5.0"` or `:speed="8.0"` for long sessions) and asciinema idle time limits (`:idleTimeLimit="1.0"`), with optional chapter markers (`Ctrl+x`) during recording.

