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
    libdaisy-guide &middot; daisysp-guide
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    Turning 50,000+ lines of embedded C++ headers into high-signal runbooks
  </p>
</div>

<!--
Act 3 brings us to Way 1: Library Review Skills. Before touching the Gamma hardware, we needed the agent to master both `libDaisy` (the hardware abstraction layer) and `DaisySP` (the DSP synthesis library). We used the exact same workflow to generate `libdaisy-guide` and `daisysp-guide`—let's walk through how `libdaisy-guide` was built.
-->

---
layout: default
---

<!-- S22 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Source Tree &rarr; Architecture Report &rarr; Skill</h2>
</div>

<ol class="space-y-7 text-sm text-gray-200 list-decimal pl-6 mt-8 leading-relaxed">
  <li v-click>
    <strong class="text-white">Clone the Source Repos</strong>
    <ul class="list-disc pl-5 mt-2 space-y-2 text-gray-300">
      <li>Check out <code>electro-smith/libDaisy</code> and <code>electro-smith/DaisySP</code> locally</li>
      <li>Inspect live source code instead of relying on stale training weights</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Run an Architectural Audit</strong>
    <ul class="list-disc pl-5 mt-2 space-y-2 text-gray-300">
      <li>Survey linker scripts, memory sections, ISR rules, and module catalogs</li>
      <li>Synthesize findings into a structured architectural report</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Package into <code>.agents/skills/</code></strong>
    <ul class="list-disc pl-5 mt-2 space-y-2 text-gray-300">
      <li>Distill the report into a concise <code>SKILL.md</code> plus <code>references/</code> catalogs</li>
      <li>Future sessions start with an accurate map of the codebase</li>
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

<ol class="space-y-7 text-sm text-gray-200 list-decimal pl-6 mt-8 leading-relaxed">
  <li v-click>
    <strong class="text-white">Hallucinated HAL APIs</strong>
    <ul class="list-disc pl-5 mt-2 space-y-2 text-gray-300">
      <li>Mixes up Arduino <code>analogRead()</code>, raw STM32 HAL, and <code>libDaisy</code> v4 vs v7</li>
      <li>Triggers immediate compile errors and wasted retry loops</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">STM32H7 DMA &amp; RAM Traps</strong>
    <ul class="list-disc pl-5 mt-2 space-y-2 text-gray-300">
      <li>Cortex-M7 D-Cache does not snoop DMA transfers</li>
      <li>Cached DMA buffers or stack-allocated <code>ReverbSc</code> (395 KB) crash the MCU</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Audio ISR Deadline Violations</strong>
    <ul class="list-disc pl-5 mt-2 space-y-2 text-gray-300">
      <li><code>AudioCallback</code> has a strict <strong>1.0 ms</strong> deadline (48 samples @ 48 kHz)</li>
      <li>Calling <code>oled.Update()</code> (9 ms over I2C) inside the ISR destroys audio</li>
    </ul>
  </li>
</ol>

<!--
Why is this especially critical for embedded C++? Because general LLM weights hallucinate API signatures, forget Cortex-M7 DMA cache attributes, and put 395 KB reverbs on the stack.
-->

---
layout: cast-full
title: "Creating libdaisy-guide from libDaisy"
cast: /casts/libdaisy-skill-creation.cast
autoPlay: false
speed: 20.0
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

  <div class="space-y-4 text-sm pt-3">
    <div v-click class="px-4 py-5 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-cyan-300 font-semibold">Hardware Anchors:</span> Names <code>ARM Cortex-M7 @ 480 MHz</code> and <code>STM32H750</code> so any MCU-level question triggers the skill.
    </div>
    <div v-click class="px-4 py-5 rounded-lg bg-gray-900/80 border border-gray-800">
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
---

<!-- S27 -->
<div class="space-y-4 text-xs">
  <p class="text-sm text-gray-300 m-0">
    <code>libDaisy</code> targets the <strong>STM32H750IBK6</strong> MCU and standard Daisy peripherals:
  </p>
  <table class="w-full text-left border-collapse">
    <thead>
      <tr class="border-b border-gray-700 text-gray-200">
        <th class="py-2.5 pr-3">Component</th>
        <th class="py-2.5 px-3">Hardware Spec</th>
        <th class="py-2.5 pl-3">libDaisy Support</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-800/80 text-gray-300">
      <tr>
        <td class="py-2.5 pr-3 font-semibold text-white">MCU Core</td>
        <td class="py-2.5 px-3">ARM Cortex-M7 @ 480 MHz (FPU &amp; DSP)</td>
        <td class="py-2.5 pl-3">CMSIS-DSP, LL / HAL drivers</td>
      </tr>
      <tr>
        <td class="py-2.5 pr-3 font-semibold text-white">Internal Flash</td>
        <td class="py-2.5 px-3">128 KB Flash (<code>0x08000000</code>)</td>
        <td class="py-2.5 pl-3">Bootloader (<code>BOOT_NONE</code>)</td>
      </tr>
      <tr>
        <td class="py-2.5 pr-3 font-semibold text-white">Internal RAM</td>
        <td class="py-2.5 px-3">1 MB (AXI 512K, DTCM 128K, SRAM1–4)</td>
        <td class="py-2.5 pl-3">DSP (<code>DTCM</code>), DMA (<code>SRAM1</code>)</td>
      </tr>
      <tr>
        <td class="py-2.5 pr-3 font-semibold text-white">External SDRAM</td>
        <td class="py-2.5 px-3">64 MB SDRAM via FMC</td>
        <td class="py-2.5 pl-3">Audio buffers (<code>DSY_SDRAM_BSS</code>)</td>
      </tr>
      <tr>
        <td class="py-2.5 pr-3 font-semibold text-white">External Flash</td>
        <td class="py-2.5 px-3">8 MB QSPI NOR Flash</td>
        <td class="py-2.5 pl-3">Apps (<code>BOOT_SRAM</code>) &amp; presets</td>
      </tr>
      <tr>
        <td class="py-2.5 pr-3 font-semibold text-white">Audio Codec</td>
        <td class="py-2.5 px-3">24-bit stereo up to 96 kHz</td>
        <td class="py-2.5 pl-3">Double-buffered DMA via SAI1</td>
      </tr>
      <tr>
        <td class="py-2.5 pr-3 font-semibold text-white">USB</td>
        <td class="py-2.5 px-3">USB 2.0 Full / High-Speed</td>
        <td class="py-2.5 pl-3">CDC Serial, MIDI, Audio, Host</td>
      </tr>
    </tbody>
  </table>
</div>

<!--
Second, look at how `libdaisy-guide` anchors the hardware specification: naming the STM32H750 MCU core, memory sections, external SDRAM/Flash, audio codec, and USB peripherals directly in the skill runbook.
-->

---
layout: skill-breakdown
way: 1
skill: .agents/skills/libdaisy-guide/SKILL.md
title: Codebase Organization
---

<!-- S28 -->
<div class="space-y-4 text-xs">
  <p class="text-sm text-gray-300 m-0">
    <code>libDaisy</code> organizes <a href="https://github.com/domesticmouse/reverse-engineering-gamma/blob/main/libDaisy/src/" target="_blank" class="text-cyan-300 underline"><code>libDaisy/src/</code></a> by standardized module prefixes:
  </p>
  <table class="w-full text-left border-collapse">
    <thead>
      <tr class="border-b border-gray-700 text-gray-200">
        <th class="py-3 pr-3">Prefix</th>
        <th class="py-3 px-3">Subsystem</th>
        <th class="py-3 pl-3">Key Classes &amp; Role</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-800/80 text-gray-300">
      <tr>
        <td class="py-3 pr-3 font-semibold text-white"><code>sys/</code></td>
        <td class="py-3 px-3 font-semibold text-white">System</td>
        <td class="py-3 pl-3">Clocks, MPU, cache, DMA (<code>System</code>, <code>DmaHandler</code>)</td>
      </tr>
      <tr>
        <td class="py-3 pr-3 font-semibold text-white"><code>per/</code></td>
        <td class="py-3 px-3 font-semibold text-white">Peripherals</td>
        <td class="py-3 pl-3">On-chip STM32 drivers (<code>AdcHandle</code>, <code>GPIO</code>, <code>I2CHandle</code>, <code>TimerHandle</code>)</td>
      </tr>
      <tr>
        <td class="py-3 pr-3 font-semibold text-white"><code>dev/</code></td>
        <td class="py-3 px-3 font-semibold text-white">Devices</td>
        <td class="py-3 pl-3">Off-chip ICs: codecs (<code>Pcm3060</code>), OLEDs (<code>SSD130x</code>), memory</td>
      </tr>
      <tr>
        <td class="py-3 pr-3 font-semibold text-white"><code>hid/</code></td>
        <td class="py-3 px-3 font-semibold text-white">Human Interface</td>
        <td class="py-3 pl-3">Audio &amp; controls (<code>AudioHandle</code>, <code>Switch</code>, <code>Encoder</code>, <code>UsbHandle</code>)</td>
      </tr>
      <tr>
        <td class="py-3 pr-3 font-semibold text-white"><code>ui/</code></td>
        <td class="py-3 px-3 font-semibold text-white">User Interface</td>
        <td class="py-3 pl-3">Menus &amp; event queues (<code>UI</code>, <code>UiEventQueue</code>, <code>AbstractMenu</code>)</td>
      </tr>
      <tr>
        <td class="py-3 pr-3 font-semibold text-white"><code>util/</code></td>
        <td class="py-3 px-3 font-semibold text-white">Utilities</td>
        <td class="py-3 pl-3">Lock-free <code>FIFO</code>, <code>FixedCapStr</code>, <code>WavPlayer</code>, <code>CpuLoadMeter</code></td>
      </tr>
    </tbody>
  </table>
</div>

<!--
Third, `libdaisy-guide` maps out libDaisy's subsystem prefixes—`sys/`, `per/`, `dev/`, `hid/`, `ui/`, and `util/`. Instead of blindly grepping across 50,000 lines of headers, the agent knows immediately which directory hosts on-chip peripheral handles versus off-board IC drivers like display controllers and audio codecs.
-->

---
layout: default
---

<!-- S29 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Problem #1 Solved: Unfamiliar APIs &amp; Tribal Knowledge</h2>
</div>

<ol class="space-y-10 text-sm text-gray-200 list-decimal pl-6 mt-10 leading-relaxed">
  <li v-click>
    <strong class="text-white">The Problem: Hallucinated APIs &amp; Grep Loops</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Agents mix up versions and burn turns grepping 50,000+ lines of headers</li>
      <li>Constraints like DMA cache rules and 1 ms ISR deadlines aren't obvious</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">The Fix: Distill Once, Reuse Forever</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>One codebase audit produces a ~200-line <code>SKILL.md</code> + <code>references/</code></li>
      <li>Verified class names, memory macros, and DSP rules replace guesswork</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Portable Across Projects &amp; Teammates</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li><code>libdaisy-guide</code> and <code>daisysp-guide</code> work on any Daisy project</li>
      <li>Every new session and teammate inherits instant mastery on turn one</li>
    </ul>
  </li>
</ol>

<!--
That's Way 1: Library Review Skills—and notice how it directly solves Problem #1 from the start of our talk. Instead of watching the agent hallucinate APIs or burn turns grepping through 50,000 lines of C++ headers every session, we audited `libDaisy` and `DaisySP` once and distilled them into ~200-line runbooks. Now that tribal library knowledge travels with the repository, and every future session—or teammate—gets idiomatically correct Daisy C++ on the very first try.
-->
