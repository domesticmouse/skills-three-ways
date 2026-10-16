---
layout: center
class: text-center
---

<!-- S21 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Way 1: Library Review Skills
  </h1>
  <p class="text-xl font-mono text-cyan-300">
    libdaisy-guide
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
  <h2 class="text-2xl font-bold m-0">The Pattern: Source Tree &rarr; Architecture Report &rarr; Skill</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Clone Source: Check Out the Raw C++ Repo</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Clone <code>electro-smith/libDaisy</code> directly into the workspace</li>
      <li>Lets the agent inspect actual <code>.h</code> and <code>.cpp</code> files rather than relying on stale training weights</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Deep Audit: Synthesize Architecture</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Have AGY survey directory prefixes, linker scripts, memory sections, real-time ISR rules, and module catalogs</li>
      <li>Compile findings into a structured architectural reference</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Package Skill: Distill into <code>.agents/skills/</code></strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Convert the report into a fast Tier-2 <code>SKILL.md</code> cheatsheet plus Tier-3 <code>references/</code> catalogs</li>
      <li>Future tasks never need to grep 200 headers again</li>
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
title: "libdaisy-guide: Frontmatter & Activation Triggers"
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
title: "libdaisy-guide: Codebase Prefix Taxonomy"
step: Zoom-In 2 of 3
---

<!-- S27 -->
<div class="space-y-3 text-xs">
  <p class="text-gray-300">
    Instead of grepping blindly through hundreds of files, the skill maps <code>libDaisy/src/</code> into 6 domain prefixes:
  </p>
  <table>
    <thead>
      <tr>
        <th>Prefix</th>
        <th>Subsystem Domain</th>
        <th>Key Classes Documented in <code>SKILL.md</code></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>sys/</code></td>
        <td>System Infrastructure</td>
        <td><code>System</code>, <code>DmaHandler</code>, <code>FatFSInterface</code> (Clocks, MPU, D-cache)</td>
      </tr>
      <tr>
        <td><code>per/</code></td>
        <td>On-Chip Peripherals</td>
        <td><code>AdcHandle</code>, <code>GPIO</code>, <code>I2CHandle</code>, <code>SaiHandle</code>, <code>TimerHandle</code></td>
      </tr>
      <tr>
        <td><code>dev/</code></td>
        <td>External IC Drivers</td>
        <td><code>Pcm3060</code>, <code>SSD130x</code>, <code>SdramHandle</code>, <code>IS25LP064A</code></td>
      </tr>
      <tr>
        <td><code>hid/</code></td>
        <td>Human Interface</td>
        <td><code>AudioHandle</code>, <code>Switch</code>, <code>Encoder</code>, <code>UsbHandle</code>, <code>OledDisplay</code></td>
      </tr>
      <tr>
        <td><code>ui/</code> &amp; <code>util/</code></td>
        <td>Menus &amp; RT Utilities</td>
        <td><code>FIFO</code>, <code>FixedCapStr</code>, <code>PersistentStorage</code>, <code>CpuLoadMeter</code></td>
      </tr>
    </tbody>
  </table>
</div>

<!--
Second, look at how `libdaisy-guide` organizes the codebase into six clean prefixes: `sys/`, `per/`, `dev/`, `hid/`, `ui/`, and `util/`, naming the exact C++ classes in each domain.
-->

---
layout: skill-breakdown
way: 1
skill: .agents/skills/libdaisy-guide/SKILL.md
title: "libdaisy-guide: STM32H750 Memory Map & DMA Rules"
step: Zoom-In 3 of 3
---

<!-- S28 -->
<div class="space-y-3 text-xs">
  <table>
    <thead>
      <tr>
        <th>Memory Region</th>
        <th>Base Address</th>
        <th>Size</th>
        <th>Macro / Attribute</th>
        <th>Critical Engineering Rule</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>DTCM RAM</strong></td>
        <td><code>0x20000000</code></td>
        <td>128 KB</td>
        <td><code>DTCM_MEM_SECTION</code></td>
        <td>Zero-wait 480 MHz DSP state. <strong>No DMA access!</strong></td>
      </tr>
      <tr>
        <td><strong>AXI SRAM</strong></td>
        <td><code>0x24000000</code></td>
        <td>512 KB</td>
        <td>Standard (<code>.bss</code>/<code>.data</code>)</td>
        <td>Primary app RAM for <code>APP_TYPE = BOOT_SRAM</code>. Cached.</td>
      </tr>
      <tr>
        <td><strong>SRAM1 (D2)</strong></td>
        <td><code>0x30000000</code></td>
        <td>128 KB</td>
        <td><code>DMA_BUFFER_MEM_SECTION</code></td>
        <td><strong>Non-cached.</strong> Mandatory for ADC, SAI, I2C, SPI DMA buffers.</td>
      </tr>
      <tr>
        <td><strong>External SDRAM</strong></td>
        <td><code>0xC0000000</code></td>
        <td>64 MB</td>
        <td><code>DSY_SDRAM_BSS</code></td>
        <td>Large audio delay lines. No dynamic C++ constructors before <code>hw.Init()</code>.</td>
      </tr>
    </tbody>
  </table>
</div>

<!--
Third, `libdaisy-guide` gives the agent the exact STM32H750 memory map table—making it impossible to confuse cached AXI SRAM (`0x24000000`), non-cached `DMA_BUFFER_MEM_SECTION` (`0x30000000`), and `DSY_SDRAM_BSS` (`0xC0000000`).
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
