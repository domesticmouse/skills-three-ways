# Skills Three Ways: Teaching Agents New Tricks via Agent Skills

A presentation and technical exploration by Brett Morgan categorizing how **Agent Skills** (following the [agentskills.io](https://agentskills.io) open specification) are authored, generated, and applied in practice—using the reverse-engineering of embedded firmware for the **this.is.NOISE Gamma mini synth** (powered by an Electro-Smith **Daisy Seed 2 DFM**) as a real-world case study.

📊 **[Live Slide Deck](https://domesticmouse.github.io/skills-three-ways/)**

## Related Resources

- **Companion Hardware & Firmware Repository:** [github.com/domesticmouse/reverse-engineering-gamma](https://github.com/domesticmouse/reverse-engineering-gamma/)
- **Blog Post:** [Reverse Engineering a this.is.NOISE Gamma Synth (Medium)](https://medium.com/@domesticmouse/reverse-engineering-a-this-is-noise-gamma-synth-f15a72d7dbfd)

---

## The "Three Ways" Taxonomy

When reverse-engineering the Gamma mini synth without schematics or source code, seven custom Agent Skills emerged across three distinct authoring patterns (plus a capstone mashup):

1. **Way 1: Library Review Skills**
   - [`libdaisy-guide`](.agents/skills/libdaisy-guide/SKILL.md) & [`daisysp-guide`](.agents/skills/daisysp-guide/SKILL.md)
   - Created by having an agent inspect C++ library source trees (`libDaisy` and `DaisySP`), synthesize architectural and real-time DSP reference reports, and package those findings into reusable skills.

2. **Way 2: DFU Operational Skills**
   - [`gamma-firmware-flash`](.agents/skills/gamma-firmware-flash/SKILL.md) & [`gamma-firmware-restore`](.agents/skills/gamma-firmware-restore/SKILL.md)
   - Created by solving USB-C `dfu-util` bootloader flashing requirements (`BOOT_SRAM` `0x24000000` vector table relocation and the ~2.5s Daisy bootloader grace window) and wrapping the workflow into deterministic Python scripts and operational runbooks.

3. **Way 3: Hardware Discovery Skills**
   - [`gamma-pinout`](.agents/skills/gamma-pinout/SKILL.md) & [`gamma-hardware-controls`](.agents/skills/gamma-hardware-controls/SKILL.md)
   - Distilled from a phased series of interactive diagnostic firmwares that mapped physical pins, ADC channels, polarities, and C++ driver idioms for the 14 tactile keys, 4 potentiometers, 2 dual-axis thumbsticks, rotary encoder, and SSD1306 OLED display.

4. **The Capstone Mashup Skill**
   - [`gamma-usb-connectivity`](.agents/skills/gamma-usb-connectivity/SKILL.md)
   - Combines all three patterns into a single skill package: discovered USB pinout facts (`UsbHandle::FS_EXTERNAL` on `D29`/`D30`), a deadlock-immune C++ firmware driver (`gamma_usb.h`), and a host-side Python communication utility (`gamma_usb.py`).

---

## Repository Structure

- [`slides/`](slides/) — [Slidev](https://sli.dev/) presentation deck, custom Vue components, layouts, and acts (`01-primer.md` through `06-experiment-and-conclusion.md`).
- [`.agents/skills/`](.agents/skills/) — Agent Skills packages used both in the Gamma mini synth case study and for authoring/maintaining this repository.
- [`terminal-recordings/`](terminal-recordings/) — Sanitized [asciinema](https://asciinema.org/) `.cast` recordings embedded in the presentation.
- [`GLOSSARY.md`](GLOSSARY.md) — Canonical project terminology and domain language.

---

## Running the Slide Deck Locally

The presentation is built with [Slidev](https://sli.dev/) (Vue 3 + Vite).

```bash
cd slides
npm install
npm run dev
```

To build the static bundle locally:

```bash
cd slides
npm run build
```

---

## License & Disclaimer

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for full terms and conditions.

**Disclaimer:** This is not an official Google product.