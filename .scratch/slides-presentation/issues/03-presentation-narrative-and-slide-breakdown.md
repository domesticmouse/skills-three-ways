# Presentation narrative arc and slide-by-slide structure

Type: grilling
Status: resolved
Blocked by: 02

## Question

How should the narrative beats be structured into concrete Slidev slides, including slide titles, key takeaways, visual layouts (text vs code vs embedded terminal recordings), speaker notes, and pacing transitions from Agent Skills fundamentals to reverse-engineering the Gamma mini synth?

## Answer

### 1. Talk Format & Pacing
- **Duration**: 35–40 minutes (~30 seconds per slide).
- **Target Slide Count**: 80 slides across 7 Acts.
- **Core Taxonomy ("Skills Three Ways" + Mashup)**:
  1. **Way 1 — Library Review Skills (`libdaisy-guide`, `daisysp-guide`)**: Created by having AGY inspect the `libDaisy` and `DaisySP` C++ source trees, generate an architectural usage report, and convert that report into an Agent Skill.
  2. **Way 2 — DFU Operational Skills (`gamma-firmware-flash`, `gamma-firmware-restore`)**: Created by having AGY figure out how to connect to the Gamma mini synth over USB-C via `dfu-util` (solving the `APP_TYPE = BOOT_SRAM` `0x24000000` vector table requirement, ~2.5s bootloader grace period, and OLED GDDRAM retention), turning the workflow into a Python script (`flash_firmware.py`, `restore_firmware.py`) and a wrapper skill.
  3. **Way 3 — Hardware Discovery Skills (`gamma-pinout`, `gamma-hardware-controls`)**: Created from a phased series of diagnostic firmwares (`PLAN.md` Phases 1–5) that mapped how the 14 keys, 4 knobs, 2 thumbsticks, rotary encoder, speaker amp enable pin, and SSD1306 OLED screen are wired (`gamma-pinout` + `resources/gamma_pins.h`) and captured the C++ driver idioms (`gamma-hardware-controls` + `references/`).
  4. **The Mashup Skill (`gamma-usb-connectivity`)**: Combines all three aspects in one skill: hardware pinout truth (`UsbHandle::FS_EXTERNAL` on `D29`/`D30`), deadlock-immune non-blocking C++ firmware driver (`resources/gamma_usb.h`), and a zero-dependency host Python script (`scripts/gamma_usb.py`).

### 2. Visual Layout Conventions
- **2-Slide Beat for All 6 Terminal Recordings**:
  - **Slide N (Recording Intro Card)**: Large-type context, the exact AGY prompt, and what the audience should watch for.
  - **Slide N+1 (`cast-full` Layout — 85–90% Viewport, Click-to-Play)**: Top compact 10% header bar (Act breadcrumb + title + `Click terminal to play` badge) and 85–90% main area with `<AsciinemaPlayer :autoPlay="false" :speed="2.0" :idleTimeLimit="1.0" fit="both" />`. The presenter advances onto the slide, introduces it, clicks to play, talks over it, and advances when finished.
- **Multi-Slide Zoom-In Rhythm for Skill Breakdowns**:
  - Rather than cramming a skill onto one slide, each skill bucket is unpacked across 3–4 slides (30s each): (1) Directory Tree & Anatomy (`SKILL.md`, `scripts/`, `references/`, `resources/`), (2) YAML Frontmatter & Trigger Design, (3) Core Runbook / Negative Constraints, and (4) Bundled Executable Script or C++ Header.
- **Hardware Photo Assets**:
  - `slides/public/images/gamma-promo.png`: Official advertising asset from the Gamma website.
  - `slides/public/images/gamma-screws.jpg`: Photo sent by the synth creator indicating which screws to undo to open the enclosure and access the internals (used on the spare unit ordered during a late-night impulse buy).
- **Live Hardware Demonstration (Act 7 Climax, Slide 79)**:
  - Show the physical Gamma mini synth running the default factory firmware, have AGY build/flash the `drum_synth` firmware, and demonstrate the 7-voice drum synth live on the physical unit.

### 3. Complete 80-Slide Breakdown

#### Act 1: Primer — What Are Agent Skills? (Slides 1–11)
- **S01**: Title — *Skills Three Ways: Teaching Agents New Tricks* (Brett Morgan, Developer Relations Engineer, Google Cloud)
- **S02**: Section Divider — *Primer: What Are Agent Skills?*
- **S03**: The Context Window Trap — Why stuffing every manual, pinout, and script into `AGENTS.md` fails
- **S04**: Recording 1 Intro — *Asking AGY: "What are Agent Skills?"*
- **S05**: Recording 1 Replay (`cast-full`, click-to-play) — `what-are-agent-skills.cast`
- **S06**: Agent Skills as On-Demand Runbooks — Open specification (`agentskills.io`) vs. always-on Rules and raw MCP Tools
- **S07**: Directory Anatomy of a Skill — `SKILL.md`, `scripts/`, `references/`, `resources/`
- **S08**: Inside `SKILL.md` Part 1 — YAML Frontmatter (`name` + semantic trigger `description`)
- **S09**: Inside `SKILL.md` Part 2 — Procedural workflows, negative constraints, and relative links
- **S10**: The 3-Tier Progressive Disclosure Model — Discovery (~100 tokens) $\to$ Activation (`SKILL.md`) $\to$ Execution (`references/` & `scripts/`)
- **S11**: Generating Skills with `/agy-customizations` & `agent-skills` — Turning research and workflows into self-contained packages

#### Act 2: The Hook & The Two Gamma Mini Synths (Slides 12–20)
- **S12**: Meet the **Gamma mini synth** by *this.is.NOISE inc.* (`gamma-promo.png` + hardware overview)
- **S13**: What the Factory Synth Does Out of the Box — 7 chord keys, 7 note keys, 2 analog thumbsticks, 4 pots, rotary encoder, 1.3" OLED
- **S14**: The Late-Night Accident — Ordering a second Gamma mini synth while the first was still being manufactured
- **S15**: One for Music, One for Science — Why having a spare unit changes your risk tolerance for hardware hacking
- **S16**: Asking the Creator How to Get Inside — The annotated photo showing which screws to undo (`gamma-screws.jpg`)
- **S17**: Inside the Chassis — Discovering the **Electro-Smith Daisy Seed 2 DFM** (ARM Cortex-M7 @ 480 MHz, STM32H750IBK6, PCM3060 stereo codec)
- **S18**: The Catch — No public schematic, no pinout table, and factory firmware written in closed-source embedded Rust
- **S19**: The Mission — Can an AI coding agent (AGY) reverse-engineer the hardware and build custom C++ DSP synth firmware?
- **S20**: The Thesis: *Skills Three Ways* — Library Review Skills, DFU Operational Skills, Hardware Discovery Skills (+ The Mashup Skill)

#### Act 3: Way 1 — Library Review Skills (`libdaisy-guide` & `daisysp-guide`) (Slides 21–34)
- **S21**: Section Divider — *Way 1: Library Review Skills (`libdaisy-guide` & `daisysp-guide`)*
- **S22**: The Pattern: C++ Source Tree $\to$ Architecture Usage Report $\to$ Agent Skill
- **S23**: Why Embedded C++ Libraries Need Skills — Hallucinated HAL methods, STM32H7 DMA cache traps, and real-time audio violations
- **S24**: Recording 2 Intro — *Having AGY review `libDaisy/` and convert the report into `libdaisy-guide`*
- **S25**: Recording 2 Replay (`cast-full`, click-to-play) — `libdaisy-skill-creation.cast`
- **S26**: `libdaisy-guide` Breakdown 1 — YAML Frontmatter & activation triggers
- **S27**: `libdaisy-guide` Breakdown 2 — Codebase prefix taxonomy (`sys/`, `per/`, `dev/`, `hid/`, `ui/`, `util/`)
- **S28**: `libdaisy-guide` Breakdown 3 — STM32H750 memory map (`AXI SRAM`, `DTCM`, `SRAM1` DMA buffers, `DSY_SDRAM_BSS`)
- **S29**: Recording 3 Intro — *Having AGY review `DaisySP/` and convert the report into `daisysp-guide`*
- **S30**: Recording 3 Replay (`cast-full`, click-to-play) — `daisysp-skill-creation.cast`
- **S31**: `daisysp-guide` Breakdown 1 — YAML Frontmatter & MIT (`daisysp.h`) vs. LGPL (`daisysp-lgpl.h`) licensing boundary
- **S32**: `daisysp-guide` Breakdown 2 — The 5 Real-Time Audio Tenets (no `malloc`, single-sample `Process()`, rate separation, `Init(sr)`)
- **S33**: `daisysp-guide` Breakdown 3 — Fast Module Selection Index + `references/module_catalog.md` (Tier 3 deep context)
- **S34**: Way 1 Takeaway — Distilling 50,000+ lines of C++ headers into ~200 lines of high-signal agent runbooks

#### Act 4: Way 2 — DFU Operational Skills (`gamma-firmware-flash` & `gamma-firmware-restore`) (Slides 35–46)
- **S35**: Section Divider — *Way 2: DFU Operational Skills (`gamma-firmware-flash` & `gamma-firmware-restore`)*
- **S36**: The Pattern: Interactive USB-C Troubleshooting $\to$ Python Script $\to$ Wrapper Skill
- **S37**: First Contact over USB-C — Running `dfu-util -l` and discovering `"Daisy Bootloader" (0483:df11)` at `0x90040000`
- **S38**: Trap #1: The Bootloader Mode Confusion — Why `Hold BOOT + Tap RESET` enters dead STM32 ROM instead of the Daisy Bootloader
- **S39**: Trap #2: The 2.5-Second Grace Period — Racing `dfu-util` manually while the USER LED pulses
- **S40**: Trap #3: Why Does My Firmware SOS Blink? — Inspecting the factory binary vector table (`0x240047ED`) to discover `APP_TYPE = BOOT_SRAM`
- **S41**: Trap #4: The Ghost on the OLED — SSD1306 GDDRAM retention keeping `this.is.NOISE inc` on screen even when the MCU is halted
- **S42**: Safety First: `gamma-firmware-restore` — Caching `gamma-v2.0.3.bin` and building an unbrick runbook before probing hardware
- **S43**: `gamma-firmware-restore` Breakdown — `SKILL.md` recovery procedures + `scripts/restore_firmware.py`
- **S44**: `gamma-firmware-flash` Breakdown 1 — `SKILL.md` negative constraints (`APP_TYPE = BOOT_SRAM`, never `BOOT_QSPI` or `BOOT_NONE`)
- **S45**: `gamma-firmware-flash` Breakdown 2 — Inside `scripts/flash_firmware.py` (vector table `0x24000000` check + USB CDC `'b'` soft-reboot + `dfu-util` polling + exit code `74` handling)
- **S46**: Way 2 Takeaway — Don't make the agent re-solve fragile timing races; wrap operational mechanics in deterministic scripts

#### Act 5: Way 3 — Hardware Discovery Skills (`gamma-pinout` & `gamma-hardware-controls`) (Slides 47–62)
- **S47**: Section Divider — *Way 3: Hardware Discovery Skills (`gamma-pinout` & `gamma-hardware-controls`)*
- **S48**: The Pattern: Phased Diagnostic Firmwares (`PLAN.md`) $\to$ Pinout Truth + C++ Driver Idioms
- **S49**: Recording 4 Intro — *Collaborating with AGY to design the 6-Phase Reverse-Engineering Plan (`PLAN.md`)*
- **S50**: Recording 4 Replay (`cast-full`, click-to-play) — `reverse-engineering-plan.cast`
- **S51**: The 6-Phase Probing Roadmap — From Phase 0 (Baseline Backup) to Phase 5 (Audio & Speaker Amp)
- **S52**: Phase 1 & 2 Probing (`phase1_i2c_scan`) — Scanning I2C buses to find the 1.3" SSD1306 OLED on `I2C1` (`D11`/`D12`) at `0x3D`
- **S53**: Phase 3 Probing (`phase3_adc`) — Mapping the 4 top knobs (`D18`, `D17`, `D19`, `D20`) and 2 dual-axis thumbsticks (`D22`/`D21`, `D24`/`D23`)
- **S54**: The Polarity Surprise — Discovering that all 4 pots and 3 of 4 joystick axes are wired inverted (`1.0f - raw`)!
- **S55**: Phase 4 Probing (`phase4_keys_encoder`) — Mapping 14 active-low tactile keys (`N1`–`N7`, `C1`–`C7`) and the quadrature encoder (`D15`/`D16`/`D28`)
- **S56**: Phase 5 Probing (`phase5_audio`) — Finding the internal stereo speaker amplifier enable/mute pin on `seed::D32` (`PC3`, active HIGH)
- **S57**: Distilling Facts vs. Idioms — Why we split hardware truth into two skills: `gamma-pinout` and `gamma-hardware-controls`
- **S58**: `gamma-pinout` Breakdown 1 — `SKILL.md` Master Pinout Table (every pin, STM32 port, ADC channel, and polarity)
- **S59**: `gamma-pinout` Breakdown 2 — Bundling `resources/gamma_pins.h` so the agent includes verified constants instead of typing magic numbers
- **S60**: `gamma-hardware-controls` Breakdown 1 — `SKILL.md` front-panel driver architecture & 1 kHz `TIM` ISR Buxton Gray-code encoder decoding
- **S61**: `gamma-hardware-controls` Breakdown 2 — Progressive disclosure via `references/` (`display.md`, `analog_inputs.md`, `digital_keys.md`, `rotary_encoder.md`)
- **S62**: Way 3 Takeaway — Turn ephemeral debugging sessions into permanent, verifiable hardware abstractions

#### Act 6: The Mashup Skill (`gamma-usb-connectivity`) (Slides 63–70)
- **S63**: Section Divider — *The Mashup Skill (`gamma-usb-connectivity`)*
- **S64**: The Mystery: Why Did `hw.StartLog()` Produce Zero Output?
- **S65**: On-OLED Register Debugging — Discovering the USB-C port is wired to `USB_OTG_HS` in FS mode (`UsbHandle::FS_EXTERNAL` on `D29`/`D30`), not `FS_INTERNAL`
- **S66**: Two Real-Time USB Deadlocks — Hazard 1: `Logger<LOGGER_EXTERNAL>::TransmitSync()` infinite spinloop when terminal disconnects; Hazard 2: `UsbRxCallback` ISR deadlock
- **S67**: Why `gamma-usb-connectivity` is a Mashup — Combining Pinout Info + C++ Firmware Driver + Host Python Script in one skill
- **S68**: Mashup Breakdown 1 (`SKILL.md`) — USB VID/PID (`0483:5740`), `FS_EXTERNAL` rules, and deadlock documentation
- **S69**: Mashup Breakdown 2 (`resources/gamma_usb.h`) — 4-buffer pool, 500 µs max wait, 200 ms fast-fail backoff, lock-free RX ring buffer
- **S70**: Mashup Breakdown 3 (`scripts/gamma_usb.py`) — Zero-dependency host script for serial telemetry, interactive commands, and `'b'` DFU reboot

#### Act 7: The Payoff — Drum Synth Without vs. With Skills + Live Demo (Slides 71–80)
- **S71**: Section Divider — *Putting All 7 Skills to the Test: Building a Drum Synth*
- **S72**: The Experiment — Identical prompt to build a 7-voice Drum Synth for the Gamma mini synth: **Without Skills** vs. **With Skills**
- **S73**: Recording 5 Intro — *Attempt 1: Building a Drum Synth WITHOUT Skills*
- **S74**: Recording 5 Replay (`cast-full`, click-to-play) — `drum-synth-without-skills.cast`
- **S75**: Anatomy of the Failure (Without Skills) — Wrong `Makefile` target (SOS blink), wrong USB port (`FS_INTERNAL`), guessed GPIO pins, inverted knobs
- **S76**: Recording 6 Intro — *Attempt 2: Building & Flashing the Drum Synth WITH All 7 Skills*
- **S77**: Recording 6 Replay (`cast-full`, click-to-play) — `drum-synth-with-skills.cast`
- **S78**: How the 7 Skills Composed — `libdaisy-guide` + `daisysp-guide` + `gamma-pinout` + `gamma-hardware-controls` + `gamma-usb-connectivity` + `gamma-firmware-flash`
- **S79**: **LIVE DEMO**: Physical Gamma mini synth running default firmware $\to$ AGY installs `drum_synth` $\to$ live play of the 7 drum voices, soft-takeover knobs, and DJ filter thumbstick
- **S80**: Closing & Links — Recap of *Skills Three Ways*, links to `domesticmouse/reverse-engineering-gamma` & `domesticmouse/skills-three-ways`
