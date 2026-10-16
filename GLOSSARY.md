# Skills Three Ways

Presentation and technical project exploring Agent Skills authoring, generation, and reverse-engineering embedded firmware for the Gamma mini synth.

## Language

**Skills Three Ways**:
The presentation title and taxonomy by Brett Morgan that categorizes the Agent Skills authored while reverse-engineering the Gamma mini synth into three distinct origins (plus a capstone mashup):
1. **Library Review Skills** (`libdaisy-guide`, `daisysp-guide`)
2. **DFU Operational Skills** (`gamma-firmware-flash`, `gamma-firmware-restore`)
3. **Hardware Discovery Skills** (`gamma-pinout`, `gamma-hardware-controls`)
Plus the **Mashup Skill** (`gamma-usb-connectivity`) combining pinout facts, C++ firmware drivers, and host-side Python scripting.

**Library Review Skills**:
Way 1 of the three ways: skills (`libdaisy-guide`, `daisysp-guide`) created by having AGY inspect C++ library source trees, generate a comprehensive reference report on how to use the library, and convert that report into an Agent Skill.

**DFU Operational Skills**:
Way 2 of the three ways: skills (`gamma-firmware-flash`, `gamma-firmware-restore`) created by having AGY figure out how to connect to the Gamma mini synth over USB-C using `dfu-util` (solving the `BOOT_SRAM` `0x24000000` vector table requirement and ~2.5s bootloader grace window) and wrapping the solution into a Python script plus a runbook skill.

**Hardware Discovery Skills**:
Way 3 of the three ways: skills (`gamma-pinout`, `gamma-hardware-controls`) distilled from a phased series of diagnostic firmwares (`PLAN.md` Phases 1–4) that mapped the physical pins, polarities, and C++ driver idioms for the 14 keys, 4 pots, 2 thumbsticks, rotary encoder, and SSD1306 OLED screen.

**Mashup Skill**:
The synthesis skill (`gamma-usb-connectivity`) that combines all three patterns in a single package: hardware pinout knowledge (`UsbHandle::FS_EXTERNAL` on `D29`/`D30`), deadlock-immune C++ firmware driver code (`gamma_usb.h`), and a host-side Python communication script (`gamma_usb.py`).

**Gamma mini synth**:
The hardware synthesizer device by this.is.NOISE inc. based on the Daisy Seed 2 DFM microcontroller, used as the exploration and reverse-engineering case study.
_Avoid_: Gamma synth, synthesizer toy

**Daisy Seed 2 DFM**:
The embedded microcontroller hardware module at the core of the Gamma mini synth.
_Avoid_: Daisy board, Seed MCU

**LibDaisy**:
The official hardware abstraction C++ library for the Daisy embedded audio platform.
_Avoid_: libdaisy library, Daisy HAL

**DaisySP**:
The official digital signal processing (DSP) library for audio synthesis on Daisy hardware.
_Avoid_: daisysp library, Daisy DSP

**Slidev**:
The Markdown-based presentation framework powered by Vue 3 and Vite used to build the slide deck and static bundle for GitHub Pages.
_Avoid_: Slide deck generator, presentation tool
