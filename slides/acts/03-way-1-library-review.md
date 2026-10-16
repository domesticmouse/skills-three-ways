---
layout: center
class: text-center
---

<!-- S21 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Library Review Skills
  </h1>
  <p class="text-xl font-mono text-cyan-300">
    libdaisy-guide daisysp-guide
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    Turning 50,000+ lines of embedded C++ headers into high-signal runbooks
  </p>
</div>

<!--
Act 3 brings us to Way 1: Library Review Skills. Before touching the Gamma hardware, we needed the agent to master `libDaisy`.
-->

---
layout: default
---

<!-- S22 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Source Tree &rarr; Architecture Report &rarr; Skill</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Clone Source: Check Out the Raw C++ Repo</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Clone <code>electro-smith/libDaisy</code> directly into the workspace</li>
      <li>Ask agent to inspect source code rather than relying on stale training weights</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Deep Audit: Synthesize Architecture</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Have Antigravity survey linker scripts, memory sections, real-time ISR rules, and module catalogs</li>
      <li>Compile findings into a structured architectural reference</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Package Skill: Distill into <code>.agents/skills/</code></strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Convert the report into a <code>SKILL.md</code> cheatsheet plus <code>references</code> catalogs</li>
      <li>Future tasks know where to start looking for things</li>
    </ul>
  </li>
</ol>

<!--
The Way 1 pattern is simple and repeatable for any library: check out the source repository locally, have the agent perform a systematic architectural audit, and package that audit into a progressive-disclosure skill.
-->

---
layout: default
---

<!-- S23 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Why Embedded C++ Libraries Need Skills</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Hallucinated HAL APIs</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Without a skill, LLMs mix up Arduino <code>analogRead()</code>, raw STM32 HAL calls, and older <code>libDaisy</code> v4 vs v7</li>
      <li>Causes immediate compile errors and wasted retry loops</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">STM32H7 DMA &amp; RAM Traps</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>The Cortex-M7 D-Cache does not snoop DMA transfers</li>
      <li>Putting a DMA buffer in cached AXI SRAM or a 395 KB <code>ReverbSc</code> on the stack silently crashes the MCU</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">ISR Deadline Violations</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>At 48 kHz with a 48-sample block, <code>AudioCallback</code> has a strict <strong>1.0 millisecond</strong> deadline</li>
      <li>Calling <code>oled.Update()</code> (9 ms over I2C) inside the audio ISR destroys audio output</li>
    </ul>
  </li>
</ol>

<!--
Why is this especially critical for embedded C++? Because general LLM weights hallucinate API signatures, forget Cortex-M7 DMA cache attributes, and put 395 KB reverbs on the stack.
-->

---
layout: cast-full
title: "Recording 02: Creating libdaisy-guide from libDaisy/"
cast: /casts/libdaisy-skill-creation.cast
autoPlay: false
speed: 4.0
idleTimeLimit: 1.0
fit: both
---

<!-- S25 -->
<!--
Click to play: watch AGY scan `libDaisy/src/`, inspect the peripheral headers and STM32H750 linker sections, and synthesize the complete `libdaisy-guide` skill.
-->

---
layout: skill-breakdown
way: 1
skill: .agents/skills/libdaisy-guide/SKILL.md
title: Frontmatter & Activation Triggers
step: Zoom-In 1 of 3
---

<!-- S26 -->
<div class="space-y-4">

```yaml
---
name: libdaisy-guide
description: >-
  Comprehensive guide and architectural reference for developing embedded audio firmware
  with libDaisy on the Electro-Smith Daisy platform (ARM Cortex-M7 @ 480 MHz, STM32H750).
  Use this skill whenever writing audio callbacks, implementing DSP synthesis, configuring
  on-chip peripherals (ADC, DAC, GPIO, I2C, SPI, UART, SAI, QSPI), debugging STM32H7 memory
  sections (DTCM, SRAM1 DMA, SDRAM), integrating with the Daisy Bootloader, or troubleshooting
  audio glitches, cache incoherency, and build failures.
---
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-cyan-300 font-semibold">Hardware Anchors:</span> Names <code>ARM Cortex-M7 @ 480 MHz</code> and <code>STM32H750</code> so any MCU-level question triggers the skill.
    </div>
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-cyan-300 font-semibold">Subsystem Triggers:</span> Lists <code>ADC, DAC, GPIO, I2C, SPI, UART, SAI, QSPI</code> and <code>DTCM, SRAM1 DMA, SDRAM</code>.
    </div>
  </div>
</div>

<!--
Let's zoom into the resulting `libdaisy-guide` skill. First, look at its YAML frontmatter: it packs every peripheral acronym and STM32H7 memory section into the description so any firmware task activates it automatically.
-->

---
layout: skill-breakdown
way: 1
skill: .agents/skills/libdaisy-guide/SKILL.md
title: "System & Hardware Architecture"
step: Zoom-In 2 of 3
---

<!-- S27 -->
<div class="space-y-3 text-xs">

`libDaisy` targets the **STM32H750IBK6** high-performance microcontroller and standard Daisy hardware peripherals:

| Component | Hardware Specification | libDaisy Support |
| :--- | :--- | :--- |
| **MCU Core** | ARM Cortex-M7 @ 480 MHz with FPU (double/single precision) & DSP extensions | CMSIS-DSP, CMSIS Core, LL / HAL drivers |
| **Internal Flash** | 128 KB User Flash (`0x08000000`) | Base bootloader location (`APP_TYPE = BOOT_NONE`) |
| **Internal RAM** | 1 MB total: AXI SRAM (512 KB), DTCM (128 KB), SRAM1–3 (288 KB), SRAM4 (64 KB) | Fast DSP state (`DTCM`), DMA buffers (`SRAM1`) |
| **External SDRAM** | 64 MB 32-bit SDRAM (AS4C32M16SB) via FMC bus @ ~100–120 MHz | Large audio buffers / delay lines (`DSY_SDRAM_BSS`) |
| **External Flash** | 8 MB QSPI NOR Flash (IS25LP064A) via Quad-SPI | Daisy Bootloader app storage (`APP_TYPE = BOOT_SRAM`) & presets |
| **Audio Codec** | 24-bit stereo up to 96 kHz (AK4556, WM8731, PCM3060, TAC5242) | Interrupt double-buffered DMA via SAI1 |
| **USB** | USB 2.0 Full-Speed (12 Mbps) or High-Speed with external ULPI | USB CDC (Serial), USB MIDI, USB Audio, USB Host |

</div>

<!--
Second, look at how `libdaisy-guide` anchors the hardware specification: naming the STM32H750 MCU core, memory sections, external SDRAM/Flash, audio codec, and USB peripherals directly in the skill runbook.
-->

---
layout: skill-breakdown
way: 1
skill: .agents/skills/libdaisy-guide/SKILL.md
title: Codebase Organization
step: Zoom-In 3 of 3
---

<!-- S28 -->
<div class="space-y-3 text-xs">

The `libDaisy` source tree ([`libDaisy/src/`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/)) uses standardized module prefixes:

| Prefix | Subsystem Domain | Description & Key Classes |
| :--- | :--- | :--- |
| **`sys/`** | **System Infrastructure** | Clocks, MPU, D-cache invalidation, DMA routing, FatFs.<br>• [`System`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/sys/system.h), [`DmaHandler`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/sys/dma.h), [`FatFSInterface`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/sys/fatfs.h) |
| **`per/`** | **Internal Peripherals** | High-performance C++ drivers for STM32 on-chip peripherals.<br>• [`AdcHandle`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/per/adc.h), [`DacHandle`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/per/dac.h), [`GPIO`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/per/gpio.h), [`I2CHandle`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/per/i2c.h), [`SpiHandle`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/per/spi.h), [`SaiHandle`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/per/sai.h), [`UartHandler`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/per/uart.h), [`QSPIHandle`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/per/qspi.h), [`TimerHandle`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/per/tim.h), [`Pwm`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/per/pwm.h), [`Random`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/per/rng.h) |
| **`dev/`** | **External Devices** | External ICs mounted on boards.<br>• Codecs: [`Ak4556`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/codec_ak4556.h), [`Wm8731`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/codec_wm8731.h), [`Pcm3060`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/codec_pcm3060.h)<br>• Displays: [`SSD130x`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/oled_ssd130x.h), [`SH1106`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/oled_sh1106.h), [`SSD1327`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/oled_ssd1327.h), [`SSD1351`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/oled_ssd1351.h)<br>• Memory & Expanders: [`SdramHandle`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/sdram.h), [`IS25LP064A`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/flash_IS25LP064A.h), [`MCP23x17`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/mcp23x17.h), [`TCA9534`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/tca9534.h), [`ShiftRegister595`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/sr_595.h), [`ShiftRegister4021`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/sr_4021.h)<br>• Sensors & LEDs: [`Mpr121`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/mpr121.h), [`APDS9960`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/apds9960.h), [`NeoPixel`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/neopixel.h), [`DotStar`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/dev/dotstar.h) |
| **`hid/`** | **Human Interface** | Real-time audio engine, smoothed inputs, debounce, encoders, MIDI, USB, and display drawing.<br>• [`AudioHandle`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/audio.h), [`AnalogControl`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/ctrl.h), [`Parameter`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/parameter.h), [`Switch`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/switch.h), [`Switch3`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/switch3.h), [`Encoder`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/encoder.h), [`GateIn`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/gatein.h), [`Led`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/led.h), [`RgbLed`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/rgb_led.h), [`MidiHandler`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/midi.h), [`UsbHandle`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/usb.h), [`UsbHostHandle`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/usb_host.h), [`Logger`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/logger.h), [`Display`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/disp/display.h), [`OledDisplay`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/hid/disp/oled_display.h) |
| **`ui/`** | **User Interface** | Screen menu hierarchies, event queues, and input monitoring.<br>• [`UI`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/ui/UI.h), [`UiEventQueue`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/ui/UiEventQueue.h), [`AbstractMenu`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/ui/AbstractMenu.h), [`FullScreenItemMenu`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/ui/FullScreenItemMenu.h), [`ButtonMonitor`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/ui/ButtonMonitor.h) |
| **`util/`** | **Utilities** | Lock-free FIFOs, string formatting without heap allocation, WAV streaming, preset saving, and load profiling.<br>• [`FIFO`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/util/FIFO.h), [`FixedCapStr`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/util/FixedCapStr.h), [`WavPlayer`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/util/WavPlayer.h), [`WavWriter`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/util/WavWriter.h), [`WaveTableLoader`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/util/WaveTableLoader.h), [`PersistentStorage`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/util/PersistentStorage.h), [`CpuLoadMeter`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/util/CpuLoadMeter.h), [`VoctCalibration`](https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/util/VoctCalibration.h) |

</div>

<!--
Third, `libdaisy-guide` maps out libDaisy's subsystem prefixes—`sys/`, `per/`, `dev/`, `hid/`, `ui/`, and `util/`. Instead of blindly grepping across 50,000 lines of headers, the agent knows immediately which directory hosts on-chip peripheral handles versus off-board IC drivers like display controllers and audio codecs.
-->

---
layout: default
---

<!-- S29 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Way 1 Takeaway: Library Review Skills</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">50,000+ Lines of C++ Headers Distilled</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Raw source across <code>libDaisy/</code> would overwhelm context if searched ad-hoc every session</li>
      <li>Pre-auditing once eliminates repetitive codebase grep loops</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">~200 Lines per <code>SKILL.md</code> Runbook</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Concise architectural cheatsheets with zero-hallucination class names, memory macros, and real-time rules</li>
      <li>Backed by on-demand Tier-3 catalogs in <code>references/</code></li>
    </ul>
  </li>
  <li>
    <strong class="text-white">100% Reusable Across Any Daisy Project</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li><code>libdaisy-guide</code> captures platform-level knowledge independent of the Gamma PCB</li>
      <li>Portable to any Electro-Smith Daisy Seed, Pod, Patch, or Petal project</li>
    </ul>
  </li>
</ol>

<!--
That's Way 1: Library Review Skills. By distilling 50,000+ lines of C++ headers into a ~200-line runbook, the agent writes idiomatically correct Daisy C++ on the first try—and that skill is reusable on any Daisy hardware project.
-->
