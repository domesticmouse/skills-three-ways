---
theme: default
background: '#121317'
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## Skills Three Ways
  Teaching Agents New Tricks via Agent Skills
  Presentation by Brett Morgan (Google Cloud DevRel)
drawings:
  persist: false
transition: slide-left
title: Skills Three Ways
mdc: true
---

<!-- S01 -->
<div class="h-full flex flex-col items-center justify-center">
  <div class="flex items-center gap-2 mb-4">
    <span class="px-3 py-1 text-xs font-semibold uppercase tracking-widest rounded-full badge-way1">Library Review</span>
    <span class="px-3 py-1 text-xs font-semibold uppercase tracking-widest rounded-full badge-way2">DFU Operational</span>
    <span class="px-3 py-1 text-xs font-semibold uppercase tracking-widest rounded-full badge-way3">Hardware Discovery</span>
    <span class="px-3 py-1 text-xs font-semibold uppercase tracking-widest rounded-full badge-mashup">+ The Mashup</span>
  </div>

  <h1 class="text-5xl font-extrabold tracking-tight text-white mb-3">
    Skills Three Ways
  </h1>
  <p class="text-2xl text-gray-300 font-light max-w-2xl">
    Teaching Coding Agents New Tricks on Uncharted Hardware
  </p>

  <div class="mt-10 text-gray-400 text-base">
    <span class="font-semibold text-gray-200">Brett Morgan</span> &middot; Developer Relations Engineer, Google Cloud
  </div>

  <div class="mt-10 text-xs text-gray-500">
    Press <kbd>Space</kbd> or <kbd>&rarr;</kbd> to advance
  </div>
</div>

<!--
Welcome everyone! Today we're going to explore how to teach AI coding agents new tricks using Agent Skills—specifically by reverse-engineering an undocumented hardware synthesizer from scratch.
-->

---
layout: hardware-callout
section: Act 1 · The Hook
title: Meet the Gamma Mini Synth
subtitle: this.is.NOISE inc.
image: /images/gamma-promo.png
imageCaption: Gamma Mini Synth — Pocket-sized polyphonic chord & lead synthesizer
imageTag: Hardware Target
---

<!-- S02 -->
<div class="space-y-4">
  <h3 class="text-lg font-bold text-emerald-300">A Pocket-Sized Dual Engine Synth</h3>
  <p class="text-sm text-gray-300 leading-relaxed">
    Built by <strong>this.is.NOISE inc.</strong>, the Gamma Mini Synth packs a complete dual-voice performance instrument into a battery-powered handheld enclosure.
  </p>
  <ul class="text-sm text-gray-300 space-y-2 list-disc pl-5">
    <li><strong>Dual Engines</strong>: Independent Chord &amp; Lead Note synthesizers</li>
    <li><strong>Tactile Surface</strong>: 14 mechanical switch keys + 2 dual-axis thumbsticks</li>
    <li><strong>Hands-On Control</strong>: 4 top analog pots + clickable rotary encoder</li>
    <li><strong>Visual &amp; Audio</strong>: 1.3" OLED display + built-in speaker &amp; 3.5mm stereo out</li>
  </ul>
</div>

<!--
Meet the star of today's story: the Gamma Mini Synth by this.is.NOISE inc. It's a compact, battery-powered hardware synthesizer with thumbsticks, tactile keys, four knobs, an OLED screen, and an internal speaker.
-->

---
layout: default
---

<!-- S03 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">What the Factory Synth Does Out of the Box</h2>
</div>

<div class="grid grid-cols-3 gap-4 mt-6">
  <div class="p-4 rounded-xl bg-gray-900/70 border border-gray-800">
    <div class="text-cyan-400 font-mono text-xs uppercase mb-1">Left &amp; Right Keypads</div>
    <div class="text-lg font-bold text-white mb-2">7 Note + 7 Chord Keys</div>
    <p class="text-xs text-gray-400 leading-relaxed">
      Left keypad plays melodic scale degrees (<code>N1</code>–<code>N7</code>). Right keypad triggers rich diatonic seventh &amp; extended chords (<code>C1</code>–<code>C7</code>).
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900/70 border border-gray-800">
    <div class="text-amber-400 font-mono text-xs uppercase mb-1">Expressive Modulation</div>
    <div class="text-lg font-bold text-white mb-2">2 Analog Thumbsticks</div>
    <p class="text-xs text-gray-400 leading-relaxed">
      Spring-loaded 2-axis joysticks bend pitch, sweep LFO depth, and morph wave-shaping in real time under your thumbs.
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900/70 border border-gray-800">
    <div class="text-emerald-400 font-mono text-xs uppercase mb-1">Top Panel &amp; Menu</div>
    <div class="text-lg font-bold text-white mb-2">4 Knobs + OLED + Encoder</div>
    <p class="text-xs text-gray-400 leading-relaxed">
      Dedicated Chord/Note Volume &amp; Filter cutoff knobs across the top, plus a 128&times;64 OLED navigated by a clickable rotary dial.
    </p>
  </div>
</div>

<div class="mt-6 p-3.5 rounded-lg bg-gray-900/40 border border-gray-800/80 text-center text-sm text-gray-300">
  It's super fun out of the box—so why would anyone risk bricking it?
</div>

<!--
Out of the box, it plays chords on the right, lead notes on the left, modulates with two analog thumbsticks, and shapes tone with four top knobs. So why risk tearing it open?
-->

---
layout: default
---

<!-- S04 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Late-Night Accident</h2>
</div>

<div class="grid grid-cols-12 gap-6 items-center mt-8">
  <div class="col-span-7 space-y-4">
    <div class="p-5 rounded-xl bg-gray-900/80 border border-gray-800 space-y-3">
      <div class="text-xs font-mono text-amber-400 uppercase">Chronology of a Hardware Impulse Buy</div>
      <ol class="text-sm text-gray-300 space-y-3 list-decimal pl-5">
        <li>Backed / ordered a <strong>Gamma Mini Synth</strong> and waited patiently while the batch was being manufactured.</li>
        <li>Months later, late at night, saw an email about the Gamma, completely forgot I already had one in the queue...</li>
        <li><strong>Ordered a second one.</strong></li>
      </ol>
    </div>
  </div>

  <div class="col-span-5 p-6 rounded-xl bg-amber-950/20 border border-amber-500/30 text-center">
    <div class="text-4xl font-black text-amber-300 mb-2">2&times;</div>
    <div class="text-base font-semibold text-white mb-2">Gamma Mini Synths Arrived</div>
    <p class="text-xs text-gray-400">
      What starts as a late-night ordering mistake quickly turns into an engineering opportunity.
    </p>
  </div>
</div>

<!--
Here's my confession: while waiting for my first Gamma to be manufactured, I forgot I had already ordered one and accidentally ordered a second unit late at night. Suddenly I had two identical synths on my desk.
-->

---
layout: default
---

<!-- S05 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">One for Music, One for Science</h2>
</div>

<div class="grid grid-cols-2 gap-6 mt-8">
  <div class="p-6 rounded-xl bg-gray-900/60 border border-gray-800 flex flex-col justify-between">
    <div>
      <span class="text-xs font-mono px-2 py-0.5 rounded bg-gray-800 text-gray-300">Unit #1 · Factory Stock</span>
      <h3 class="text-xl font-bold text-white mt-3 mb-2">One for Making Music</h3>
      <p class="text-sm text-gray-400 leading-relaxed">
        Kept completely untouched running official <code>gamma-v2.0.3.bin</code> firmware. Serves as the ground-truth behavioral reference for how every knob, stick, and key should feel.
      </p>
    </div>
    <div class="mt-6 pt-3 border-t border-gray-800 text-xs text-gray-500 font-mono">
      Risk of permanent loss: 0%
    </div>
  </div>

  <div class="p-6 rounded-xl bg-emerald-950/15 border border-emerald-500/40 flex flex-col justify-between">
    <div>
      <span class="text-xs font-mono px-2 py-0.5 rounded badge-way3">Unit #2 · The Lab Rat</span>
      <h3 class="text-xl font-bold text-emerald-300 mt-3 mb-2">One for Reverse Engineering</h3>
      <p class="text-sm text-gray-300 leading-relaxed">
        Having a spare unit completely transforms your risk tolerance. We can open the chassis, probe unknown buses, and flash experimental firmware without fear.
      </p>
    </div>
    <div class="mt-6 pt-3 border-t border-emerald-800/40 text-xs text-emerald-400 font-mono">
      "Let's see what powers this thing inside..."
    </div>
  </div>
</div>

<!--
Having a spare unit completely changes your psychology. One unit stays pristine for making music; the second unit goes on the operating table for science.
-->

---
layout: hardware-callout
section: Act 1 · The Hook
title: Asking the Creator How to Get Inside
subtitle: Disassembly Guidance
image: /images/gamma-screws.jpg
imageCaption: Annotated rear enclosure photo showing which 4 corner screws to remove
imageTag: Chassis Access
---

<!-- S06 -->
<div class="space-y-4">
  <h3 class="text-lg font-bold text-amber-300">Which Screws Open the Case?</h3>
  <p class="text-sm text-gray-300 leading-relaxed">
    The rear plate has multiple fasteners holding both internal standoffs and the outer shell. Before randomly unscrewing hardware, I reached out to the creator at <strong>this.is.NOISE</strong>.
  </p>
  <div class="p-3.5 rounded-lg bg-gray-900/80 border border-gray-800 text-xs text-gray-300 space-y-2">
    <div class="font-semibold text-white">Creator's Annotated Reply:</div>
    <p class="text-gray-400">
      Undo only the <strong>4 outer corner screws</strong> circled on the backplate—leave the inner assembly screws untouched so the key switches and thumbsticks stay aligned.
    </p>
  </div>
</div>

<!--
Before taking a screwdriver to every bolt on the backplate, I asked the creator how to safely open the enclosure. They kindly sent back an annotated photo showing which four corner screws release the shell.
-->

---
layout: default
---

<!-- S07 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Inside the Chassis: Electro-Smith Daisy Seed 2 DFM</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-6 items-center">
  <div class="col-span-6 space-y-3">
    <p class="text-sm text-gray-300 leading-relaxed">
      Lifting the back cover revealed a welcome surprise soldered onto the Gamma mainboard: an <strong>Electro-Smith Daisy Seed 2 DFM</strong> module!
    </p>
    <div class="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/30 space-y-2">
      <div class="text-xs font-mono text-cyan-300 uppercase">Hardware Specs on the Carrier</div>
      <ul class="text-xs text-gray-200 space-y-1.5 list-disc pl-4">
        <li><strong>MCU</strong>: STM32H750IBK6 (ARM Cortex-M7 @ 480 MHz)</li>
        <li><strong>RAM</strong>: 1 MB Internal + 64 MB External SDRAM</li>
        <li><strong>Flash</strong>: 8 MB External QSPI NOR Flash (<code>0x90000000</code>)</li>
        <li><strong>Audio Codec</strong>: TI PCM3060 24-bit / 48 kHz Stereo via SAI1</li>
      </ul>
    </div>
  </div>

  <div class="col-span-6">
    <div class="p-5 rounded-xl bg-gray-900 border border-gray-800 font-mono text-xs space-y-2">
      <div class="text-gray-400">// Physical buttons accessible inside:</div>
      <div class="p-2.5 rounded bg-gray-950 border border-gray-800 text-emerald-300">
        [BOOT] Button  &middot;  [RESET] Button
      </div>
      <div class="text-gray-400 pt-2">// Open-Source C++ Ecosystem Available:</div>
      <div class="p-2.5 rounded bg-gray-950 border border-gray-800 text-cyan-300">
        electro-smith/libDaisy  (Hardware BSP)<br/>
        electro-smith/DaisySP   (DSP Synthesis Library)
      </div>
    </div>
  </div>
</div>

<!--
Opening the shell revealed a huge win: the brain of the Gamma is an Electro-Smith Daisy Seed 2 DFM running an STM32H750 Cortex-M7 at 480 MHz with a TI PCM3060 stereo codec—supported by the open-source C++ libDaisy and DaisySP libraries.
-->

---
layout: default
---

<!-- S08 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Catch: Zero Schematics, Closed-Source Rust</h2>
</div>

<div class="grid grid-cols-3 gap-4 mt-6">
  <div class="p-5 rounded-xl bg-red-950/20 border border-red-500/30">
    <div class="text-xs font-mono text-red-400 uppercase mb-1">Obstacle 1</div>
    <h3 class="text-base font-bold text-white mb-2">No Public Schematic</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      Over 30 Daisy Seed GPIO pins (<code>D0</code>–<code>D32</code>), 3 I2C buses, and multiple ADC channels—with zero documentation on what pin connects to which button, pot, stick, or amp.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-red-950/20 border border-red-500/30">
    <div class="text-xs font-mono text-red-400 uppercase mb-1">Obstacle 2</div>
    <h3 class="text-base font-bold text-white mb-2">Closed Factory Firmware</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      The stock firmware (<code>gamma-v2.0.3.bin</code>) is distributed only as a raw compiled binary written in embedded Rust—no C++ project template or board header exists.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-red-950/20 border border-red-500/30">
    <div class="text-xs font-mono text-red-400 uppercase mb-1">Obstacle 3</div>
    <h3 class="text-base font-bold text-white mb-2">Silent Failure Modes</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      Wrong linker target? Red SOS LED blink. Wrong USB port? Complete silence on <code>hw.StartLog()</code>. Uninitialized speaker mute pin? Dead audio output.
    </p>
  </div>
</div>

<div class="mt-6 p-3.5 rounded-lg bg-gray-900/70 border border-gray-800 text-center text-sm text-gray-300">
  If you ask a coding agent out-of-the-box to "build a synth for the Gamma", it has <strong>zero chance</strong> of guessing the hardware wiring.
</div>

<!--
Here's the catch: knowing it's a Daisy Seed doesn't tell you how the carrier PCB is wired. There's no schematic, no pinout table, and the stock binary is closed-source Rust. An out-of-the-box coding agent has zero chance of guessing the pins.
-->

---
layout: default
---

<!-- S09 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Mission: Collaborating with Antigravity (AGY)</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-6 items-center">
  <div class="col-span-7 space-y-4">
    <p class="text-sm text-gray-200 leading-relaxed">
      Could we use <strong>Google Antigravity (AGY)</strong> not just to write C++ code, but to systematically <strong>reverse-engineer the physical hardware</strong> and capture every discovery as reusable <strong>Agent Skills</strong>?
    </p>
    <div class="space-y-2.5 text-xs text-gray-300">
      <div class="p-3 rounded-lg bg-gray-900 border border-gray-800 flex items-center gap-3">
        <span class="text-cyan-400 font-bold font-mono">Step 1</span>
        <span>Teach the agent the C++ libraries (<code>libDaisy</code> &amp; <code>DaisySP</code>) before touching hardware.</span>
      </div>
      <div class="p-3 rounded-lg bg-gray-900 border border-gray-800 flex items-center gap-3">
        <span class="text-amber-400 font-bold font-mono">Step 2</span>
        <span>Establish a rock-solid USB DFU flash &amp; factory restore safety net.</span>
      </div>
      <div class="p-3 rounded-lg bg-gray-900 border border-gray-800 flex items-center gap-3">
        <span class="text-emerald-400 font-bold font-mono">Step 3</span>
        <span>Run phased diagnostic firmwares to map every pin, polarity, and peripheral.</span>
      </div>
    </div>
  </div>

  <div class="col-span-5 p-5 rounded-xl bg-gray-900/90 border border-gray-700/80 text-left space-y-3">
    <div class="text-xs font-mono text-purple-300 uppercase">The End Goal</div>
    <div class="text-lg font-bold text-white">One-Shot Custom Firmware</div>
    <p class="text-xs text-gray-400 leading-relaxed">
      Once all 7 skills are authored, any developer or agent can prompt: <em>"Build a 7-voice drum synth for the Gamma"</em>—and get working, hardware-verified firmware on the first build.
    </p>
  </div>
</div>

<!--
So the mission became: can we partner with Google Antigravity (AGY) to reverse-engineer the hardware step by step, and package everything we learn into modular Agent Skills so future firmware builds work on the first try?
-->

---
layout: default
---

<!-- S10 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Thesis: Skills Three Ways (+ The Mashup)</h2>
</div>

<div class="grid grid-cols-2 gap-4 mt-4">
  <div class="p-4 rounded-xl border border-cyan-500/40 bg-cyan-950/15">
    <div class="flex items-center justify-between mb-1.5">
      <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full badge-way1">Way 1 · Library Review Skills</span>
      <span class="text-xs font-mono text-cyan-300">2 Skills</span>
    </div>
    <div class="font-mono text-sm font-bold text-white mb-1">libdaisy-guide &middot; daisysp-guide</div>
    <p class="text-xs text-gray-300">
      Point AGY at a third-party C++ source tree &rarr; generate an architectural usage report &rarr; distill into a progressive-disclosure runbook.
    </p>
  </div>

  <div class="p-4 rounded-xl border border-amber-500/40 bg-amber-950/15">
    <div class="flex items-center justify-between mb-1.5">
      <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full badge-way2">Way 2 · DFU Operational Skills</span>
      <span class="text-xs font-mono text-amber-300">2 Skills</span>
    </div>
    <div class="font-mono text-sm font-bold text-white mb-1">gamma-firmware-flash &middot; gamma-firmware-restore</div>
    <p class="text-xs text-gray-300">
      Solve fragile USB DFU timing &amp; linker traps interactively &rarr; codify into deterministic Python scripts wrapped by a skill.
    </p>
  </div>

  <div class="p-4 rounded-xl border border-emerald-500/40 bg-emerald-950/15">
    <div class="flex items-center justify-between mb-1.5">
      <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full badge-way3">Way 3 · Hardware Discovery Skills</span>
      <span class="text-xs font-mono text-emerald-300">2 Skills</span>
    </div>
    <div class="font-mono text-sm font-bold text-white mb-1">gamma-pinout &middot; gamma-hardware-controls</div>
    <p class="text-xs text-gray-300">
      Execute a 6-phase hardware probing plan (<code>PLAN.md</code>) &rarr; capture verified pin tables (<code>gamma_pins.h</code>) and 1 kHz ISR driver idioms.
    </p>
  </div>

  <div class="p-4 rounded-xl border border-purple-500/40 bg-purple-950/15">
    <div class="flex items-center justify-between mb-1.5">
      <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full badge-mashup">The Mashup Skill</span>
      <span class="text-xs font-mono text-purple-300">1 Skill</span>
    </div>
    <div class="font-mono text-sm font-bold text-white mb-1">gamma-usb-connectivity</div>
    <p class="text-xs text-gray-300">
      Combines all three ways in one package: hardware pinout truth (<code>FS_EXTERNAL</code>), deadlock-free C++ header (<code>gamma_usb.h</code>), and host Python CLI (<code>gamma_usb.py</code>).
    </p>
  </div>
</div>

<!--
Across this project, seven skills emerged naturally in three distinct patterns—what I call "Skills Three Ways": Library Review Skills, DFU Operational Skills, and Hardware Discovery Skills, plus a seventh Mashup skill that combines all three.
-->

---
layout: center
class: text-center
---

<!-- S11 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Primer: What Are Agent Skills?
  </h1>
  <p class="text-lg text-gray-400 max-w-xl mx-auto">
    Why on-demand procedural runbooks beat stuffing everything into your system prompt
  </p>
</div>

<!--
Before we dive into the three ways, let's do a quick primer on what Agent Skills actually are and why they exist.
-->

---
layout: default
---

<!-- S12 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Context Window Trap</h2>
</div>

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="p-5 rounded-xl bg-red-950/15 border border-red-500/30 space-y-3">
    <div class="text-xs font-mono text-red-400 uppercase">Anti-Pattern: Monolithic AGENTS.md</div>
    <h3 class="text-lg font-bold text-white">Stuffing Every Manual into Always-On Rules</h3>
    <ul class="text-xs text-gray-300 space-y-2 list-disc pl-4">
      <li>50,000+ lines of <code>libDaisy</code> and <code>DaisySP</code> headers</li>
      <li>32-row pinout tables, ADC channel maps, and I2C addresses</li>
      <li>DFU bootloader recovery procedures and Python scripts</li>
      <li><strong>Result</strong>: Permanent token bloat on every turn, competing instructions, and degraded reasoning focus.</li>
    </ul>
  </div>

  <div class="p-5 rounded-xl bg-emerald-950/15 border border-emerald-500/30 space-y-3">
    <div class="text-xs font-mono text-emerald-400 uppercase">The Solution: Progressive Disclosure</div>
    <h3 class="text-lg font-bold text-white">Modular, Self-Contained Skill Packages</h3>
    <ul class="text-xs text-gray-300 space-y-2 list-disc pl-4">
      <li>Keep <code>AGENTS.md</code> tiny—only universal project conventions</li>
      <li>Package domain-specific workflows into <code>.agents/skills/&lt;name&gt;/</code></li>
      <li>Agent sees only a ~100-token <code>name</code> + <code>description</code> pointer at startup</li>
      <li>Full runbook, headers, and scripts load <strong>only when triggered</strong></li>
    </ul>
  </div>
</div>

<!--
Why not just paste all our hardware docs and library guides into AGENTS.md? Because always-on rules consume context on every single turn and dilute attention. Skills give us progressive disclosure.
-->

---
layout: default
---

<!-- S13 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Asking Antigravity: "What Are Agent Skills?"</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-6 items-center">
  <div class="col-span-7 space-y-4">
    <div class="p-4 rounded-xl bg-gray-900 border border-gray-700">
      <div class="text-xs font-mono text-cyan-400 uppercase mb-1">Exact AGY CLI Prompt</div>
      <p class="font-mono text-base text-white m-0">
        "What are agent skills?"
      </p>
    </div>

    <div class="space-y-2 text-sm text-gray-300">
      <div class="font-semibold text-white">What to Watch For in the Recording:</div>
      <ul class="text-xs text-gray-300 space-y-2 list-disc pl-5">
        <li>AGY recognizes the question matches its built-in <code>agy-customizations</code> and <code>agent-skills</code> knowledge.</li>
        <li>Explains how skills live in <code>.agents/skills/&lt;skill-name&gt;/SKILL.md</code>.</li>
        <li>Highlights on-demand activation via YAML frontmatter descriptions.</li>
      </ul>
    </div>
  </div>

  <div class="col-span-5 p-5 rounded-xl bg-gray-900/60 border border-gray-800 text-xs text-gray-400 space-y-2">
    <div class="font-mono text-emerald-400 uppercase">Interactive Player Note</div>
    <p>
      On the next slide, the terminal recording is rendered by <code>asciinema-player</code> v3 (WebAssembly)—click the terminal to start playback at 2&times; speed.
    </p>
  </div>
</div>

<!--
Let's ask Antigravity directly in the terminal: "What are agent skills?" On the next slide, I'll click the terminal player to play back the session.
-->

---
layout: cast-full
act: Act 2 · Primer
title: "Recording 01: What Are Agent Skills?"
cast: /casts/what-are-agent-skills.cast
autoPlay: false
speed: 2.0
idleTimeLimit: 1.0
fit: both
---

<!-- S14 -->
<!--
Here's AGY answering in Ghostty. Notice how it immediately checks its customization skill and breaks down the directory structure, frontmatter triggers, and progressive disclosure model.
-->

---
layout: default
---

<!-- S15 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Rules vs. Agent Skills vs. MCP Tools</h2>
</div>

<div class="mt-4">
  <table>
    <thead>
      <tr>
        <th>Dimension</th>
        <th>Rules (<code>AGENTS.md</code>)</th>
        <th>Agent Skills (<code>SKILL.md</code>)</th>
        <th>MCP Tools / Servers</th>
      </tr>
    </thead>
    <tbody class="text-xs">
      <tr>
        <td><strong>Cognitive Role</strong></td>
        <td>Always-on project constitution &amp; guardrails</td>
        <td>On-demand <strong>procedural runbook</strong> &amp; domain kit</td>
        <td>Live external <strong>muscle &amp; sensors</strong> (JSON-RPC)</td>
      </tr>
      <tr>
        <td><strong>Context Cost</strong></td>
        <td>Paid on <strong>every turn</strong> (100% upfront)</td>
        <td><strong>~100 tokens</strong> at startup; body loaded on match</td>
        <td>Tool JSON schemas in tool definition space</td>
      </tr>
      <tr>
        <td><strong>Bundled Assets</strong></td>
        <td>Plain markdown text only</td>
        <td><code>SKILL.md</code> + <code>scripts/</code> + <code>references/</code> + <code>resources/</code></td>
        <td>Remote API endpoints / local stdio binaries</td>
      </tr>
      <tr>
        <td><strong>Open Standard</strong></td>
        <td>Repo convention (<code>AGENTS.md</code> / <code>CLAUDE.md</code>)</td>
        <td><a href="https://agentskills.io">agentskills.io</a> portable directory spec</td>
        <td>Model Context Protocol (<code>modelcontextprotocol.io</code>)</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="mt-5 p-3 rounded-lg bg-cyan-950/20 border border-cyan-500/30 text-xs text-cyan-200 text-center">
  <strong>Analogy</strong>: MCP is the keycard that unlocks the lab; an <strong>Agent Skill</strong> is the engineering SOP manual that tells the agent which instruments to run and in what order.
</div>

<!--
How do Rules, Skills, and MCP fit together? Rules are always-on guardrails, MCP provides live external tool connections, and Agent Skills are portable on-demand engineering runbooks governed by the agentskills.io standard.
-->

---
layout: default
---

<!-- S16 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Directory Anatomy of an Agent Skill</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-5 items-center">
  <div class="col-span-6">

```text
.agents/skills/<skill-name>/
├── SKILL.md          # Required: YAML frontmatter + core runbook
├── scripts/          # Optional: Deterministic CLI helpers (.py, .sh)
│   └── flash_firmware.py
├── references/       # Optional: Deep Tier-3 docs read on demand
│   ├── display.md
│   └── rotary_encoder.md
└── resources/        # Optional: Drop-in templates & C++ headers
    └── gamma_pins.h
```

  </div>

  <div class="col-span-6 space-y-3 text-xs">
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-cyan-300">SKILL.md (Mandatory)</div>
      <p class="text-gray-400 mt-1">Entry point kept concise (&lt;500 lines). Contains activation metadata and primary procedural workflow.</p>
    </div>
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-amber-300">scripts/ (Deterministic Execution)</div>
      <p class="text-gray-400 mt-1">Executable Python/Bash utilities so the agent runs tested code instead of improvising fragile shell pipelines.</p>
    </div>
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-emerald-300">references/ &amp; resources/ (Deep Artifacts)</div>
      <p class="text-gray-400 mt-1">Subsystem deep-dives and verified <code>.h</code> headers loaded only when the specific task requires them.</p>
    </div>
  </div>
</div>

<!--
A skill isn't just a markdown file—it's a directory package. Alongside SKILL.md, it can bundle executable scripts in scripts/, deep subsystem docs in references/, and ready-to-include C++ headers in resources/.
-->

---
layout: default
---

<!-- S17 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Inside SKILL.md Part 1: YAML Frontmatter</h2>
</div>

<div class="mt-4">

```yaml
---
name: gamma-firmware-flash
description: >-
  Build, validate, and flash custom or diagnostic firmware to the this.is.NOISE
  Gamma Mini Synth (Electro-Smith Daisy Seed 2 DFM) via USB DFU using the
  automated Daisy Bootloader polling workflow.
---
```

</div>

<div class="grid grid-cols-2 gap-4 mt-5 text-xs">
  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="font-mono font-bold text-white mb-1"><code>name</code> (Identifier Constraint)</div>
    <p class="text-gray-400 leading-relaxed">
      1–64 chars, lowercase alphanumeric + hyphens (<code>^[a-z0-9]+(-[a-z0-9]+)*$</code>), and <strong>must match the parent folder name</strong>.
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="font-mono font-bold text-cyan-300 mb-1"><code>description</code> (The Routing Trigger)</div>
    <p class="text-gray-400 leading-relaxed">
      This is the <strong>only text</strong> the model sees before activation. Pack it with domain nouns (<code>Daisy Seed 2 DFM</code>, <code>USB DFU</code>) and explicit "Use when..." trigger conditions.
    </p>
  </div>
</div>

<!--
Inside SKILL.md, the YAML frontmatter is critical. Because the agent only sees <code>name</code> and <code>description</code> in its initial system prompt, your <code>description</code> is the semantic router that determines whether the skill gets read.
-->

---
layout: default
---

<!-- S18 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Inside SKILL.md Part 2: Runbooks &amp; Negative Constraints</h2>
</div>

<div class="grid grid-cols-2 gap-5 mt-4">
  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-2">
    <div class="text-xs font-mono text-amber-300 uppercase">1. Sharp Negative Constraints ("Do NOT")</div>
    <p class="text-xs text-gray-300">
      Tell the agent explicitly which plausible-looking defaults will fail on your target:
    </p>

```markdown
> [!CAUTION]
> Do **NOT** use `BOOT_QSPI` or `BOOT_NONE`;
> the Daisy Bootloader rejects `BOOT_QSPI`
> builds and emits an SOS error blink!
```

  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-2">
    <div class="text-xs font-mono text-emerald-300 uppercase">2. Relative Pointers to Tier-3 Files</div>
    <p class="text-xs text-gray-300">
      Link directly to bundled scripts, headers, and reference docs using relative paths:
    </p>

```markdown
## Pin Definitions & Header Location
* Canonical Header:
  [`resources/gamma_pins.h`](resources/gamma_pins.h)
* Display Guide:
  [`references/display.md`](references/display.md)
```

  </div>
</div>

<!--
The body of SKILL.md does two jobs: it establishes sharp negative constraints—stopping the agent from using plausible defaults that fail—and provides relative file links into scripts/, references/, and resources/.
-->

---
layout: default
---

<!-- S19 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The 3-Tier Progressive Disclosure Model</h2>
</div>

<div class="grid grid-cols-3 gap-4 mt-6">
  <div class="p-5 rounded-xl bg-gray-900/90 border border-cyan-500/30 relative">
    <div class="text-xs font-mono text-cyan-400 uppercase mb-1">Tier 1 · Discovery</div>
    <div class="text-xl font-bold text-white mb-2">~100 Tokens</div>
    <p class="text-xs text-gray-300 leading-relaxed">
      At session start, only <code>name</code> and <code>description</code> from each skill's YAML frontmatter are injected into the system prompt.
    </p>
    <div class="mt-4 text-[11px] font-mono text-cyan-300">Loaded: Always</div>
  </div>

  <div class="p-5 rounded-xl bg-gray-900/90 border border-amber-500/30 relative">
    <div class="text-xs font-mono text-amber-400 uppercase mb-1">Tier 2 · Activation</div>
    <div class="text-xl font-bold text-white mb-2">&lt; 5,000 Tokens</div>
    <p class="text-xs text-gray-300 leading-relaxed">
      When the user's task matches a skill's description, the agent calls <code>view_file</code> on <code>SKILL.md</code> to load the core runbook into working memory.
    </p>
    <div class="mt-4 text-[11px] font-mono text-amber-300">Loaded: When relevant</div>
  </div>

  <div class="p-5 rounded-xl bg-gray-900/90 border border-emerald-500/30 relative">
    <div class="text-xs font-mono text-emerald-400 uppercase mb-1">Tier 3 · Execution</div>
    <div class="text-xl font-bold text-white mb-2">On-Demand Files</div>
    <p class="text-xs text-gray-300 leading-relaxed">
      The agent selectively reads <code>references/*.md</code>, copies <code>resources/*.h</code>, or executes <code>scripts/*.py</code> only for the specific sub-steps required.
    </p>
    <div class="mt-4 text-[11px] font-mono text-emerald-300">Loaded: Per sub-task</div>
  </div>
</div>

<!--
This 3-tier progressive disclosure model is why we can have 40+ skills installed in a workspace without blowing up the context window: 100 tokens at Tier 1, SKILL.md at Tier 2, and deep reference files or scripts at Tier 3.
-->

---
layout: default
---

<!-- S20 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Authoring Skills with Agent Skills</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-6 items-center">
  <div class="col-span-7 space-y-4">
    <p class="text-sm text-gray-300 leading-relaxed">
      You don't have to write <code>SKILL.md</code> files by hand! Antigravity includes built-in meta-skills (<code>agy-customizations</code> and <code>agent-skills</code>) that know the <code>agentskills.io</code> specification inside and out.
    </p>
    <div class="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-2 text-xs">
      <div class="font-mono text-cyan-300 uppercase">The Meta-Workflow We Used Across All 7 Skills:</div>
      <ol class="list-decimal pl-5 space-y-1.5 text-gray-300">
        <li>Solve or research a problem with AGY in the workspace.</li>
        <li>Ask AGY: <em>"Convert these findings and scripts into a self-contained Agent Skill in <code>.agents/skills/&lt;name&gt;/</code>."</em></li>
        <li>Validate frontmatter, negative constraints, and relative links.</li>
      </ol>
    </div>
  </div>

  <div class="col-span-5 p-5 rounded-xl bg-cyan-950/15 border border-cyan-500/30 text-center space-y-2">
    <div class="text-xs font-mono text-cyan-300 uppercase">Next Up</div>
    <div class="text-xl font-bold text-white">Way 1: Library Review Skills</div>
    <p class="text-xs text-gray-400">
      Let's see how we used this exact workflow to turn <code>libDaisy</code> and <code>DaisySP</code> into our first two skills.
    </p>
  </div>
</div>

<!--
Best of all, you don't have to hand-author every line of SKILL.md. Using the <code>agent-skills</code> and <code>agy-customizations</code> skills, you can have the agent itself package its research and scripts into a compliant skill directory. Let's see that in Way 1!
-->

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
    libdaisy-guide &middot; daisysp-guide
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    Turning 50,000+ lines of embedded C++ headers into high-signal architectural runbooks
  </p>
</div>

<!--
Act 3 brings us to Way 1: Library Review Skills. Before touching the Gamma hardware, we needed the agent to master <code>libDaisy</code> and <code>DaisySP</code>.
-->

---
layout: default
---

<!-- S22 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Pattern: Source Tree &rarr; Architecture Report &rarr; Skill</h2>
</div>

<div class="grid grid-cols-3 gap-4 mt-8">
  <div class="p-5 rounded-xl bg-gray-900 border border-cyan-500/30">
    <div class="text-xs font-mono text-cyan-400 mb-1">Step 1 · Clone Source</div>
    <h3 class="text-base font-bold text-white mb-2">Check Out the Raw C++ Repo</h3>
    <p class="text-xs text-gray-400 leading-relaxed">
      Clone <code>electro-smith/libDaisy</code> and <code>electro-smith/DaisySP</code> directly into the workspace so the agent can read actual <code>.h</code> and <code>.cpp</code> files rather than relying on stale training weights.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-gray-900 border border-cyan-500/30">
    <div class="text-xs font-mono text-cyan-400 mb-1">Step 2 · Deep Audit</div>
    <h3 class="text-base font-bold text-white mb-2">Synthesize Architecture</h3>
    <p class="text-xs text-gray-400 leading-relaxed">
      Have AGY survey directory prefixes, linker scripts, memory sections, real-time ISR rules, and module catalogs into a structured architectural report.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-gray-900 border border-cyan-500/30">
    <div class="text-xs font-mono text-cyan-400 mb-1">Step 3 · Package Skill</div>
    <h3 class="text-base font-bold text-white mb-2">Distill into <code>.agents/skills/</code></h3>
    <p class="text-xs text-gray-400 leading-relaxed">
      Convert the report into a fast Tier-2 <code>SKILL.md</code> cheatsheet plus Tier-3 <code>references/</code> catalogs so future tasks never need to grep 200 headers again.
    </p>
  </div>
</div>

<!--
The Way 1 pattern is simple and repeatable for any library: check out the source repository locally, have the agent perform a systematic architectural audit, and package that audit into a progressive-disclosure skill.
-->

---
layout: default
---

<!-- S23 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Why Embedded C++ Libraries Need Skills</h2>
</div>

<div class="grid grid-cols-3 gap-4 mt-6">
  <div class="p-4 rounded-xl bg-gray-900/80 border border-gray-800 space-y-2">
    <div class="text-xs font-mono text-red-400 uppercase">Failure Mode 1</div>
    <div class="text-base font-bold text-white">Hallucinated HAL APIs</div>
    <p class="text-xs text-gray-400 leading-relaxed">
      Without a skill, LLMs mix up Arduino <code>analogRead()</code>, raw STM32 HAL calls, and older <code>libDaisy</code> v4 vs v7 <code>AdcChannelConfig</code> structs—causing immediate compile errors.
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900/80 border border-gray-800 space-y-2">
    <div class="text-xs font-mono text-red-400 uppercase">Failure Mode 2</div>
    <div class="text-base font-bold text-white">STM32H7 DMA &amp; RAM Traps</div>
    <p class="text-xs text-gray-400 leading-relaxed">
      The Cortex-M7 D-Cache does not snoop DMA! Putting a DMA buffer in cached AXI SRAM or putting a 395 KB <code>ReverbSc</code> on the stack silently crashes the MCU.
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900/80 border border-gray-800 space-y-2">
    <div class="text-xs font-mono text-red-400 uppercase">Failure Mode 3</div>
    <div class="text-base font-bold text-white">ISR Deadline Violations</div>
    <p class="text-xs text-gray-400 leading-relaxed">
      At 48 kHz with a 48-sample block, <code>AudioCallback</code> has exactly <strong>1.0 millisecond</strong>. Calling <code>oled.Update()</code> (9 ms over I2C) inside the audio ISR destroys audio output.
    </p>
  </div>
</div>

<!--
Why is this especially critical for embedded C++? Because general LLM weights hallucinate API signatures, forget Cortex-M7 DMA cache attributes, and put 395 KB reverbs on the stack.
-->

---
layout: default
---

<!-- S24 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Creating the <code>libdaisy-guide</code> Skill from Source</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-5 items-center">
  <div class="col-span-8 space-y-4">
    <div class="p-4 rounded-xl bg-gray-900 border border-cyan-500/40">
      <div class="text-xs font-mono text-cyan-400 uppercase mb-1">Exact AGY Prompt (Scenario 02)</div>
      <p class="font-mono text-xs text-white leading-relaxed m-0">
        "Inspect the libDaisy/ repository in this workspace. Produce a comprehensive architectural report on how to build firmware with libDaisy, detailing the hardware peripheral taxonomy, STM32H7 memory map, and initialization patterns, and format it as an Agent Skill named libdaisy-guide."
      </p>
    </div>

    <div class="text-xs text-gray-300 space-y-1.5">
      <div class="font-semibold text-white">What to Watch For:</div>
      <ul class="list-disc pl-5 space-y-1 text-gray-400">
        <li>AGY traverses <code>libDaisy/src/</code> (<code>sys/</code>, <code>per/</code>, <code>dev/</code>, <code>hid/</code>, <code>ui/</code>, <code>util/</code>) and linker scripts.</li>
        <li>Extracts the STM32H750 memory regions (<code>DTCM</code>, <code>AXI SRAM</code>, <code>SRAM1</code> DMA, <code>SDRAM</code>, <code>QSPI</code>).</li>
        <li>Writes <code>.agents/skills/libdaisy-guide/SKILL.md</code>.</li>
      </ul>
    </div>
  </div>

  <div class="col-span-4 p-4 rounded-xl bg-cyan-950/15 border border-cyan-500/30 text-xs text-gray-300">
    <div class="font-mono text-cyan-300 uppercase mb-1">Target Repo</div>
    <div class="font-bold text-white mb-2"><code>electro-smith/libDaisy</code></div>
    <p class="text-gray-400">
      C++ Hardware Abstraction &amp; Board Support Package for STM32H750 Daisy boards.
    </p>
  </div>
</div>

<!--
In Recording 2, we point AGY at a shallow checkout of <code>libDaisy/</code> and ask it to inspect the source tree and produce the <code>libdaisy-guide</code> skill. Let's watch how it explores the codebase.
-->

---
layout: cast-full
act: Act 3 · Way 1 (Library Review)
badgeClass: badge-way1
title: "Recording 02: Creating libdaisy-guide from libDaisy/"
cast: /casts/libdaisy-skill-creation.cast
autoPlay: false
speed: 4.0
idleTimeLimit: 1.0
fit: both
---

<!-- S25 -->
<!--
Click to play: watch AGY scan <code>libDaisy/src/</code>, inspect the peripheral headers and STM32H750 linker sections, and synthesize the complete <code>libdaisy-guide</code> skill.
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
Let's zoom into the resulting <code>libdaisy-guide</code> skill. First, look at its YAML frontmatter: it packs every peripheral acronym and STM32H7 memory section into the description so any firmware task activates it automatically.
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
Second, look at how <code>libdaisy-guide</code> organizes the codebase into six clean prefixes: <code>sys/</code>, <code>per/</code>, <code>dev/</code>, <code>hid/</code>, <code>ui/</code>, and <code>util/</code>, naming the exact C++ classes in each domain.
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
Third, <code>libdaisy-guide</code> gives the agent the exact STM32H750 memory map table—making it impossible to confuse cached AXI SRAM (<code>0x24000000</code>), non-cached <code>DMA_BUFFER_MEM_SECTION</code> (<code>0x30000000</code>), and <code>DSY_SDRAM_BSS</code> (<code>0xC0000000</code>).
-->

---
layout: default
---

<!-- S29 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Creating the <code>daisysp-guide</code> Skill from Source</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-5 items-center">
  <div class="col-span-8 space-y-4">
    <div class="p-4 rounded-xl bg-gray-900 border border-cyan-500/40">
      <div class="text-xs font-mono text-cyan-400 uppercase mb-1">Exact AGY Prompt (Scenario 03)</div>
      <p class="font-mono text-xs text-white leading-relaxed m-0">
        "Inspect the DaisySP/ repository in this workspace. Review the DSP synthesis modules, extract the 5 real-time audio constraints, and convert the findings into an Agent Skill named daisysp-guide with a fast module catalog."
      </p>
    </div>

    <div class="text-xs text-gray-300 space-y-1.5">
      <div class="font-semibold text-white">What to Watch For:</div>
      <ul class="list-disc pl-5 space-y-1 text-gray-400">
        <li>AGY inspects <code>DaisySP/Source/</code> (MIT core) and <code>DaisySP/DaisySP-LGPL/</code> (LGPL submodule).</li>
        <li>Catalogs Drum, Filter, Oscillator, Physical Modeling, and Effects classes.</li>
        <li>Splits the output into <code>SKILL.md</code> (Tier 2) + <code>references/module_catalog.md</code> &amp; <code>references/audio_recipes.md</code> (Tier 3).</li>
      </ul>
    </div>
  </div>

  <div class="col-span-4 p-4 rounded-xl bg-cyan-950/15 border border-cyan-500/30 text-xs text-gray-300">
    <div class="font-mono text-cyan-300 uppercase mb-1">Target Repo</div>
    <div class="font-bold text-white mb-2"><code>electro-smith/DaisySP</code></div>
    <p class="text-gray-400">
      C++ Digital Signal Processing library for synthesizers, drums, filters, and effects.
    </p>
  </div>
</div>

<!--
Next, in Recording 3, we run the same Way 1 playbook on <code>DaisySP/</code>—asking AGY to extract the real-time audio constraints and build a fast module catalog skill.
-->

---
layout: cast-full
act: Act 3 · Way 1 (Library Review)
badgeClass: badge-way1
title: "Recording 03: Creating daisysp-guide from DaisySP/"
cast: /casts/daisysp-skill-creation.cast
autoPlay: false
speed: 4.0
idleTimeLimit: 1.0
fit: both
---

<!-- S30 -->
<!--
Click to play: AGY scans every DSP category in <code>DaisySP/Source/</code> and <code>DaisySP-LGPL/</code>, checks memory footprints like <code>ReverbSc</code>, and builds <code>daisysp-guide</code> along with its Tier-3 reference catalog.
-->

---
layout: skill-breakdown
way: 1
skill: .agents/skills/daisysp-guide/SKILL.md
title: "daisysp-guide: Frontmatter & MIT vs. LGPL Boundary"
step: Zoom-In 1 of 3
---

<!-- S31 -->
<div class="space-y-3">

```yaml
---
name: daisysp-guide
description: >-
  Comprehensive guide and architectural reference for developing audio and synthesis
  applications with DaisySP. Use this skill whenever writing audio callbacks,
  implementing DSP synthesis, filters, or effects, selecting DaisySP modules, or
  diagnosing memory allocation and real-time performance issues on Daisy hardware.
---
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-1">
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-emerald-300 mb-1">MIT Core (<code>#include "daisysp.h"</code>)</div>
      <p class="text-gray-400">Default build. Includes <code>Oscillator</code>, <code>Svf</code>, <code>AnalogBassDrum</code>, <code>AnalogSnareDrum</code>, <code>HiHat</code>, <code>StringVoice</code>, <code>ModalVoice</code>, <code>Chorus</code>, <code>Overdrive</code>.</p>
    </div>
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-amber-300 mb-1">LGPL (<code>#include "daisysp-lgpl.h"</code>)</div>
      <p class="text-gray-400">Requires <code>USE_DAISYSP_LGPL = 1</code> in <code>Makefile</code>. Needed for <code>ReverbSc</code>, <code>Compressor</code>, <code>MoogLadder</code>, <code>BlOsc</code>, <code>Pluck</code>.</p>
    </div>
  </div>
</div>

<!--
Zooming into <code>daisysp-guide</code>: right after the frontmatter, it highlights a crucial build boundary—which modules live in MIT <code>daisysp.h</code> vs which require <code>USE_DAISYSP_LGPL = 1</code> and <code>daisysp-lgpl.h</code>.
-->

---
layout: skill-breakdown
way: 1
skill: .agents/skills/daisysp-guide/SKILL.md
title: "daisysp-guide: The 5 Real-Time Audio Tenets"
step: Zoom-In 2 of 3
---

<!-- S32 -->
<div class="space-y-2.5 text-xs">
  <table>
    <thead>
      <tr>
        <th>Tenet</th>
        <th>Rule</th>
        <th>Engineering Contract</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. Static Memory</strong></td>
        <td>No runtime allocation</td>
        <td>Never call <code>malloc</code>, <code>new</code>, or <code>std::vector</code> in audio callbacks. Place large buffers in <code>DSY_SDRAM_BSS</code>.</td>
      </tr>
      <tr>
        <td><strong>2. Evaluation</strong></td>
        <td>Single-sample <code>Process()</code></td>
        <td>Evaluate sample-by-sample for feedback stability; use <code>ProcessBlock</code> only where SIMD-accelerated.</td>
      </tr>
      <tr>
        <td><strong>3. Signal Ranges</strong></td>
        <td>Normalized floats</td>
        <td>Audio signals in $[-1.0\text{f}, +1.0\text{f}]$ ($0\text{ dBFS}$); control voltages in $[0.0\text{f}, 1.0\text{f}]$.</td>
      </tr>
      <tr>
        <td><strong>4. Rate Separation</strong></td>
        <td>Decouple control vs audio</td>
        <td>Update envelopes/UI parameter mappings once per block rather than per-sample where possible.</td>
      </tr>
      <tr>
        <td><strong>5. Lifecycle</strong></td>
        <td><code>Init(sr)</code> &rarr; <code>Process()</code></td>
        <td>Always call <code>.Init(sample_rate)</code> before starting audio to initialize filter coefficients.</td>
      </tr>
    </tbody>
  </table>
</div>

<!--
Next, <code>daisysp-guide</code> enforces the 5 Real-Time Audio Tenets: zero heap allocation in the audio callback, single-sample <code>Process()</code>, normalized floats, rate separation, and mandatory <code>.Init(sample_rate)</code> before audio starts.
-->

---
layout: skill-breakdown
way: 1
skill: .agents/skills/daisysp-guide/references/
title: "daisysp-guide: Fast Index + Tier-3 Reference Catalog"
step: Zoom-In 3 of 3
---

<!-- S33 -->
<div class="grid grid-cols-12 gap-4 items-center text-xs">
  <div class="col-span-6 space-y-2">
    <div class="font-mono text-cyan-300 uppercase">Tier 2 (<code>SKILL.md</code> Fast Index)</div>

```markdown
| Domain | Modules |
| :--- | :--- |
| **Drum Synthesis** | `AnalogBassDrum`, `AnalogSnareDrum`, `HiHat`, `SyntheticBassDrum`, `SyntheticSnareDrum` |
| **Filters** | `Svf`, `LadderFilter`, `OnePole` |
| **Physical** | `StringVoice`, `ModalVoice`, `Drip` |
```

  </div>

  <div class="col-span-6 space-y-2">
    <div class="font-mono text-emerald-300 uppercase">Tier 3 (<code>references/module_catalog.md</code>)</div>

```markdown
### `AnalogBassDrum` (`Drums/analogbassdrum.h`)
- `Init(float sample_rate)`
- `Trig()` / `Process(bool trigger = false)`
- `SetFreq(float f0)` (Note: keep <= 90 Hz!)
- `SetTone(float tone)`, `SetDecay(float decay)`
- `SetAttackFmAmount(float)`, `SetSelfFmAmount(float)`
```

  </div>
</div>

<!--
And look at the Tier-2 vs Tier-3 split in <code>daisysp-guide</code>: <code>SKILL.md</code> has a compact 13-row table so the agent picks the right DSP module in seconds, and then reads <code>references/module_catalog.md</code> for exact method signatures.
-->

---
layout: default
---

<!-- S34 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Way 1 Takeaway: Library Review Skills</h2>
</div>

<div class="grid grid-cols-3 gap-5 mt-8">
  <div class="p-5 rounded-xl bg-cyan-950/15 border border-cyan-500/30 text-center">
    <div class="text-3xl font-black text-cyan-300 mb-1">50,000+</div>
    <div class="text-xs font-mono uppercase text-gray-400 mb-2">Lines of C++ Headers</div>
    <p class="text-xs text-gray-300">
      Raw source across <code>libDaisy/</code> and <code>DaisySP/</code> that would overwhelm context if searched ad-hoc every session.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-cyan-950/15 border border-cyan-500/30 text-center">
    <div class="text-3xl font-black text-cyan-300 mb-1">~200</div>
    <div class="text-xs font-mono uppercase text-gray-400 mb-2">Lines per SKILL.md</div>
    <p class="text-xs text-gray-300">
      Distilled architectural cheatsheets with zero-hallucination class names, memory macros, and real-time rules.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-cyan-950/15 border border-cyan-500/30 text-center">
    <div class="text-3xl font-black text-cyan-300 mb-1">100%</div>
    <div class="text-xs font-mono uppercase text-gray-400 mb-2">Reusable Across Projects</div>
    <p class="text-xs text-gray-300">
      <code>libdaisy-guide</code> and <code>daisysp-guide</code> work for <strong>any</strong> Electro-Smith Daisy project—not just the Gamma!
    </p>
  </div>
</div>

<!--
That's Way 1: Library Review Skills. By distilling 50,000+ lines of C++ headers into two ~200-line runbooks, the agent writes idiomatically correct Daisy C++ on the first try—and those two skills are reusable on any Daisy hardware project.
-->

---
layout: center
class: text-center
---

<!-- S35 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Way 2: DFU Operational Skills
  </h1>
  <p class="text-xl font-mono text-amber-300">
    gamma-firmware-flash &middot; gamma-firmware-restore
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    Turning fragile USB bootloader timing races into deterministic Python scripts &amp; safety nets
  </p>
</div>

<!--
Now we had the library skills, so it was time to plug a USB-C cable into Unit #2. That brings us to Act 4 and Way 2: DFU Operational Skills.
-->

---
layout: default
---

<!-- S36 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Pattern: Interactive Troubleshooting &rarr; Script &rarr; Skill</h2>
</div>

<div class="grid grid-cols-3 gap-4 mt-8">
  <div class="p-5 rounded-xl bg-gray-900 border border-amber-500/30">
    <div class="text-xs font-mono text-amber-400 mb-1">Step 1 · Hit the Wall</div>
    <h3 class="text-base font-bold text-white mb-2">Debug the Hardware Protocol</h3>
    <p class="text-xs text-gray-400 leading-relaxed">
      Work interactively with AGY to figure out USB VID/PIDs, bootloader button combos, memory offsets, and exit codes.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-gray-900 border border-amber-500/30">
    <div class="text-xs font-mono text-amber-400 mb-1">Step 2 · Automate in Code</div>
    <h3 class="text-base font-bold text-white mb-2">Write a Deterministic Script</h3>
    <p class="text-xs text-gray-400 leading-relaxed">
      Don't leave timing loops or binary header checks as prose instructions! Put the exact polling &amp; validation logic into a Python script.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-gray-900 border border-amber-500/30">
    <div class="text-xs font-mono text-amber-400 mb-1">Step 3 · Wrap in a Skill</div>
    <h3 class="text-base font-bold text-white mb-2">Bundle <code>scripts/*.py</code> + <code>SKILL.md</code></h3>
    <p class="text-xs text-gray-400 leading-relaxed">
      Package the script inside <code>.agents/skills/&lt;name&gt;/scripts/</code> and write <code>SKILL.md</code> to tell the agent when and how to invoke it.
    </p>
  </div>
</div>

<!--
Way 2 follows a different pattern: when you hit operational friction like flashing hardware or racing a bootloader window, you debug it interactively once, codify the mechanics into a Python script, and wrap that script in an Agent Skill.
-->

---
layout: default
---

<!-- S37 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">First Contact over USB-C (<code>dfu-util -l</code>)</h2>
</div>

<div class="space-y-4 mt-5">
  <p class="text-sm text-gray-300">
    Plugging the Gamma into macOS and tapping <code>RESET</code> revealed the Electro-Smith <strong>Daisy Bootloader</strong> over USB DFU:
  </p>

```text
$ dfu-util -l
Found DFU: [0483:df11] ver=0200, devnum=12, cfg=1, intf=0, path="1-1", alt=0,
  name="@External Flash /0x90000000/2048*4Kg", serial="3067366D3433"
  Product: "Daisy Bootloader" (Electrosmith)
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono text-amber-300 font-bold mb-1">Bootloader in Internal Flash (<code>0x08000000</code>)</div>
      <p class="text-gray-400">The STM32H750's 128 KB internal flash holds the permanent Electro-Smith second-stage bootloader.</p>
    </div>
    <div class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono text-amber-300 font-bold mb-1">App in QSPI Flash (<code>0x90040000</code>)</div>
      <p class="text-gray-400">User firmware binaries live in external 8 MB QSPI flash starting at offset <code>0x90040000</code>.</p>
    </div>
  </div>
</div>

<!--
When we plugged the Gamma in over USB-C and ran <code>dfu-util -l</code>, we immediately hit four classic embedded traps. First contact showed the Electro-Smith Daisy Bootloader (<code>0483:df11</code>) exposing external QSPI flash at <code>0x90040000</code>.
-->

---
layout: default
---

<!-- S38 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Trap #1: The Two Different Bootloaders</h2>
</div>

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="p-5 rounded-xl bg-red-950/20 border border-red-500/30 space-y-2">
    <div class="text-xs font-mono text-red-400 uppercase">What Standard Docs Say</div>
    <h3 class="text-lg font-bold text-white">Hold BOOT + Tap RESET</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      Holding the physical <code>BOOT</code> button while tapping <code>RESET</code> drops the STM32H750 into the <strong>STM32 System ROM Bootloader</strong> (<code>@Internal Flash /0x08000000</code>).
    </p>
    <div class="p-2.5 rounded bg-red-950/50 border border-red-800/50 text-xs text-red-200 font-mono">
      Danger: Flashing <code>0x08000000</code> overwrites the Daisy Bootloader itself—and cannot write to QSPI <code>0x90040000</code>!
    </div>
  </div>

  <div class="p-5 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
    <div class="text-xs font-mono text-emerald-400 uppercase">What the Gamma Actually Needs</div>
    <h3 class="text-lg font-bold text-white">Tap RESET Only (or Tap BOOT After)</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      To reach the <strong>Daisy Bootloader</strong> (<code>@External Flash /0x90000000</code>), you simply tap <code>RESET</code> (or power-cycle) without holding <code>BOOT</code> during reset.
    </p>
    <div class="p-2.5 rounded bg-emerald-950/50 border border-emerald-800/50 text-xs text-emerald-200 font-mono">
      Result: Enumerates "Daisy Bootloader" ready for <code>0x90040000</code> QSPI uploads.
    </div>
  </div>
</div>

<!--
Trap #1: If you follow standard Daisy Seed instructions and hold BOOT while tapping RESET, you enter the raw STM32 ROM bootloader—which can't write to QSPI at <code>0x90040000</code> and risks overwriting the Daisy Bootloader! You have to tap RESET alone.
-->

---
layout: default
---

<!-- S39 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Trap #2: The 2.5-Second DFU Grace Period Race</h2>
</div>

<div class="space-y-5 mt-6">
  <div class="p-5 rounded-xl bg-gray-900 border border-gray-800">
    <div class="text-xs font-mono text-amber-300 uppercase mb-2">Boot Timeline After Tapping RESET</div>
    <div class="grid grid-cols-12 gap-2 text-center text-xs font-mono">
      <div class="col-span-4 p-3 rounded bg-amber-950/40 border border-amber-500/40 text-amber-200">
        0.0s &ndash; 2.5s<br/>
        <strong>DFU Window Open (<code>0483:df11</code>)</strong><br/>
        <span class="text-[10px] text-amber-400">USER LED pulsing</span>
      </div>
      <div class="col-span-8 p-3 rounded bg-gray-800/70 border border-gray-700 text-gray-300">
        2.5s+<br/>
        <strong>DFU Closes &rarr; Copies QSPI to SRAM &rarr; Boots App</strong><br/>
        <span class="text-[10px] text-gray-400"><code>dfu-util: No DFU capable USB device available</code></span>
      </div>
    </div>
  </div>

  <div class="grid grid-cols-2 gap-4 text-xs">
    <div class="p-4 rounded-xl bg-red-950/15 border border-red-500/30">
      <div class="font-bold text-red-300 mb-1">When the Agent Runs <code>dfu-util</code> Manually</div>
      <p class="text-gray-400">By the time you tap <code>RESET</code> and tell the agent "okay go", the 2.5-second window has already expired.</p>
    </div>
    <div class="p-4 rounded-xl bg-emerald-950/15 border border-emerald-500/30">
      <div class="font-bold text-emerald-300 mb-1">When Wrapped in a 100ms Polling Script</div>
      <p class="text-gray-400">The script loops <code>dfu-util -l</code> every 100ms (or sends <code>'b'</code> over USB CDC) and flashes the instant <code>0483:df11</code> appears.</p>
    </div>
  </div>
</div>

<!--
Trap #2: When you tap RESET, the Daisy Bootloader only listens for DFU connections for 2.5 seconds! Trying to coordinate a human button press with an LLM tool call fails 90% of the time unless you wrap it in a 100ms polling script.
-->

---
layout: default
---

<!-- S40 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Trap #3: Why Does My Firmware Blink SOS?</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-5 items-center">
  <div class="col-span-6 space-y-3 text-xs">
    <p class="text-sm text-gray-300 leading-relaxed">
      Our first test build flashed to <code>0x90040000</code>—so naturally we assumed <code>APP_TYPE = BOOT_QSPI</code>. Instead of booting, the Daisy Seed LED blinked a <strong>red SOS pattern</strong> (<code>... --- ...</code>)!
    </p>
    <div class="p-3.5 rounded-xl bg-amber-950/20 border border-amber-500/30">
      <div class="font-mono font-bold text-amber-300 mb-1">How AGY Solved It:</div>
      <p class="text-gray-300">
        AGY unpacked the first 8 bytes (ARM Cortex-M7 vector table) of the official <code>gamma-v2.0.3.bin</code> factory binary:
      </p>
    </div>
  </div>

  <div class="col-span-6">

```python
# Inspecting official gamma-v2.0.3.bin vector table:
with open("gamma-v2.0.3.bin", "rb") as f:
    sp, reset_handler = struct.unpack("<II", f.read(8))

# Initial SP:    0x20020000 (End of 128KB DTCM RAM)
# Reset Handler: 0x240047ED (Inside AXI SRAM 0x24000000!)
```

    <div class="mt-3 p-3 rounded-lg bg-emerald-950/30 border border-emerald-500/40 text-xs text-emerald-200 font-mono">
      Aha! Even though it's stored in QSPI at <code>0x90040000</code>, the bootloader copies the binary into AXI SRAM (<code>0x24000000</code>) before jumping. Makefile MUST set <code>APP_TYPE = BOOT_SRAM</code>!
    </div>
  </div>
</div>

<!--
Trap #3 was a real head-scratcher: since we flash to QSPI at <code>0x90040000</code>, we compiled with <code>APP_TYPE = BOOT_QSPI</code>—and got an SOS error blink! AGY inspected the ARM vector table of the factory binary and saw the Reset Handler at <code>0x240047ED</code>: AXI SRAM (<code>BOOT_SRAM</code>)!
-->

---
layout: default
---

<!-- S41 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Trap #4: The Ghost on the OLED Screen</h2>
</div>

<div class="grid grid-cols-2 gap-6 mt-6 items-center">
  <div class="p-5 rounded-xl bg-gray-900 border border-gray-800 space-y-3">
    <div class="text-xs font-mono text-amber-400 uppercase">The Illusion</div>
    <h3 class="text-lg font-bold text-white">"Wait—Did Our Flash Fail?"</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      After flashing minimal LED-blink firmware, the Gamma's 1.3" OLED still proudly displayed the factory <code>this.is.NOISE inc</code> UI—making it look like the factory firmware was still running!
    </p>
  </div>

  <div class="p-5 rounded-xl bg-amber-950/15 border border-amber-500/30 space-y-3">
    <div class="text-xs font-mono text-amber-300 uppercase">The Hardware Reality</div>
    <h3 class="text-lg font-bold text-white">SSD1306 GDDRAM Retention</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      The SSD1306 OLED controller has its own internal Graphic Display Data RAM (GDDRAM). As long as 3.3V power stays on across a soft reset, the screen retains its last image until new firmware explicitly initializes I2C1 (<code>0x3D</code>) and clears the buffer.
    </p>
  </div>
</div>

<!--
Trap #4 fooled us more than once: the SSD1306 OLED has its own internal display RAM. Across a soft reset, it keeps displaying the old screen even if your new firmware is running—or if the MCU is completely halted!
-->

---
layout: default
---

<!-- S42 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Safety First: Building <code>gamma-firmware-restore</code> Before Probing</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-6 items-center">
  <div class="col-span-7 space-y-3">
    <p class="text-sm text-gray-300 leading-relaxed">
      Before writing a single hardware-probing binary, we built our <strong>parachute</strong>: a one-command skill that restores the official <code>gamma-v2.0.3.bin</code> factory firmware even if the MCU is completely hung.
    </p>
    <ul class="text-xs text-gray-300 space-y-2 list-disc pl-5">
      <li>Caches <code>backups/gamma-v2.0.3.bin</code> locally (with automatic fallback download from <code>gammaupdatetool.netlify.app</code>).</li>
      <li>Polls <code>dfu-util -l</code> at 100ms intervals so a single tap of <code>RESET</code> restores factory state in 4 seconds.</li>
      <li>Verifies post-restore USB enumeration (<code>kUSBProductString = "Gamma"</code>, <code>0483:5740</code>).</li>
    </ul>
  </div>

  <div class="col-span-5 p-5 rounded-xl bg-amber-950/20 border border-amber-500/40 text-center space-y-2">
    <div class="text-xs font-mono text-amber-300 uppercase">Rule of Hardware Reverse Engineering</div>
    <div class="text-lg font-bold text-white">Never Probe Without an Automated Unbrick Script</div>
    <p class="text-xs text-gray-400">
      We triggered this restore skill dozens of times while debugging I2C locks and USB interrupts.
    </p>
  </div>
</div>

<!--
Before probing a single unknown pin, we built our parachute: <code>gamma-firmware-restore</code>. Whenever an experimental firmware hung the MCU, one command + one tap of RESET brought the synth back to factory condition in four seconds.
-->

---
layout: skill-breakdown
way: 2
skill: .agents/skills/gamma-firmware-restore/
title: "gamma-firmware-restore: Unbrick Runbook & Script"
step: Zoom-In 1 of 3
---

<!-- S43 -->
<div class="grid grid-cols-12 gap-4 items-center text-xs">
  <div class="col-span-6 space-y-2">
    <div class="font-mono text-amber-300 uppercase">SKILL.md Frontmatter &amp; Command</div>

```yaml
---
name: gamma-firmware-restore
description: >-
  Restore official factory firmware or unbrick the
  this.is.NOISE Gamma Mini Synth (Electro-Smith Daisy
  Seed 2 DFM) via USB DFU when the device is
  unresponsive, hanging on the splash screen, or
  failing to connect to the official web updater.
---
```

```bash
python3 .agents/skills/gamma-firmware-restore/\
  scripts/restore_firmware.py
```

  </div>

  <div class="col-span-6 space-y-2">
    <div class="font-mono text-emerald-300 uppercase">Inside <code>scripts/restore_firmware.py</code></div>

```python
OFFICIAL_BIN_URL = (
  "https://gammaupdatetool.netlify.app/"
  "data/gamma-v2.0.3.bin"
)
QSPI_START_ADDRESS = "0x90040000"

# Poll every 100ms during the 2.5s grace window
while time.time() - start_time < timeout:
    res = subprocess.run(
        ["dfu-util", "-l"], capture_output=True, text=True
    )
    if "0483:df11" in res.stdout:
        subprocess.run([
            "dfu-util", "-a", "0",
            "-s", f"{QSPI_START_ADDRESS}:leave",
            "-D", bin_path
        ])
```

  </div>
</div>

<!--
Here's <code>gamma-firmware-restore</code> side by side: <code>SKILL.md</code> tells the agent when to use it and how to verify recovery, while <code>scripts/restore_firmware.py</code> handles downloading/caching <code>gamma-v2.0.3.bin</code> and polling <code>dfu-util</code> at 100ms.
-->

---
layout: skill-breakdown
way: 2
skill: .agents/skills/gamma-firmware-flash/SKILL.md
title: "gamma-firmware-flash: Negative Constraints & Exit Code 74"
step: Zoom-In 2 of 3
---

<!-- S44 -->
<div class="grid grid-cols-2 gap-4 text-xs">
  <div class="space-y-2">
    <div class="font-mono text-amber-300 uppercase">Constraint 1: Linker Target</div>

````markdown
### 1. Build Target: `APP_TYPE = BOOT_SRAM`
The bootloader expects user binaries compiled for
**AXI SRAM** (`0x24000000`).

```makefile
APP_TYPE = BOOT_SRAM
```
*(Do NOT use `BOOT_QSPI` or `BOOT_NONE`; the Daisy
Bootloader will reject `BOOT_QSPI` builds and emit
an SOS error blink on the LED).*
````

  </div>

  <div class="space-y-2">
    <div class="font-mono text-amber-300 uppercase">Constraint 2: Normal Exit Code 74</div>

```markdown
> [!NOTE]
> `dfu-util: Error during download get_status`
> / exit code 74 upon `:leave` is normal because
> the MCU reboots immediately upon receiving the
> leave command.
```

    <div class="p-3 rounded bg-gray-900 border border-gray-800 text-gray-300">
      Without this note in <code>SKILL.md</code>, coding agents think exit code <code>74</code> means the flash failed and enter an endless retry loop!
    </div>
  </div>
</div>

<!--
Now look at <code>gamma-firmware-flash/SKILL.md</code>. Beyond requiring <code>APP_TYPE = BOOT_SRAM</code>, notice Constraint 2: <code>dfu-util</code> always exits with code 74 on <code>:leave</code> because the STM32 reboots before acknowledging the final USB status packet. Documenting that stops the agent from thinking the flash failed!
-->

---
layout: skill-breakdown
way: 2
skill: .agents/skills/gamma-firmware-flash/scripts/flash_firmware.py
title: "gamma-firmware-flash: Binary Validation & Hands-Free Reboot"
step: Zoom-In 3 of 3
---

<!-- S45 -->
<div class="space-y-2 text-xs">

```python
def validate_binary(bin_path):
    with open(bin_path, "rb") as f:
        sp, reset_handler = struct.unpack("<II", f.read(8))
    if 0x24000000 <= reset_handler < 0x24080000:
        print("[+] Target architecture verified: BOOT_SRAM (AXI SRAM entry point)")
    else:
        print("[!] WARNING: Reset Handler is NOT in AXI SRAM (0x24000000)!")

# Hands-free soft reboot: if USB CDC is active, send 'b' to jump straight to DFU!
for dev in glob.glob("/dev/cu.usbmodem*"):
    fd = os.open(dev, os.O_RDWR | os.O_NOCTTY)
    tty.setraw(fd)
    os.write(fd, b"b\r\n")
```

  <div class="p-2.5 rounded bg-amber-950/20 border border-amber-500/30 text-amber-200">
    <strong>Result</strong>: <code>flash_firmware.py</code> checks the ARM vector table <em>before</em> flashing and automatically triggers a software reboot into DFU mode over USB serial—no button press required!
  </div>
</div>

<!--
And inside <code>scripts/flash_firmware.py</code>, we added two superpowers: first, it unpacks the binary's ARM vector table to verify the Reset Handler is in <code>0x24000000</code> AXI SRAM before flashing; second, if USB serial is active, it sends <code>'b'</code> to reboot the synth into DFU mode hands-free!
-->

---
layout: default
---

<!-- S46 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Way 2 Takeaway: DFU Operational Skills</h2>
</div>

<div class="grid grid-cols-3 gap-5 mt-8">
  <div class="p-5 rounded-xl bg-amber-950/15 border border-amber-500/30">
    <div class="text-xs font-mono text-amber-400 uppercase mb-1">Principle 1</div>
    <h3 class="text-base font-bold text-white mb-2">Scripts Over Prose for Timing</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      Never ask an LLM to race a 2.5-second hardware window via sequential shell tool calls. Put the polling loop inside <code>scripts/</code>.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-amber-950/15 border border-amber-500/30">
    <div class="text-xs font-mono text-amber-400 uppercase mb-1">Principle 2</div>
    <h3 class="text-base font-bold text-white mb-2">Pre-Flight Validation</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      Checking 8 bytes of the <code>.bin</code> header in <code>flash_firmware.py</code> catches wrong <code>Makefile</code> linker targets before touching hardware.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-amber-950/15 border border-amber-500/30">
    <div class="text-xs font-mono text-amber-400 uppercase mb-1">Principle 3</div>
    <h3 class="text-base font-bold text-white mb-2">Document Benign Errors</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      Explicitly noting that <code>dfu-util</code> exit code <code>74</code> on <code>:leave</code> is expected prevents wasted agent debugging loops.
    </p>
  </div>
</div>

<!--
That's Way 2: DFU Operational Skills. Don't make the agent re-solve fragile hardware timing races in prose—wrap operational mechanics and pre-flight binary checks into deterministic Python scripts inside the skill.
-->

---
layout: center
class: text-center
---

<!-- S47 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Way 3: Hardware Discovery Skills
  </h1>
  <p class="text-xl font-mono text-emerald-300">
    gamma-pinout &middot; gamma-hardware-controls
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    Executing a 6-phase diagnostic firmware plan to map every pin, bus, polarity, and ISR timer
  </p>
</div>

<!--
Now we had the C++ library skills (Way 1) and the DFU flash/restore skills (Way 2). It was time for Act 5 and Way 3: probing the physical hardware to create our Hardware Discovery Skills.
-->

---
layout: default
---

<!-- S48 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Pattern: Diagnostic Firmwares (<code>PLAN.md</code>) &rarr; Truth + Idioms</h2>
</div>

<div class="grid grid-cols-3 gap-4 mt-8">
  <div class="p-5 rounded-xl bg-gray-900 border border-emerald-500/30">
    <div class="text-xs font-mono text-emerald-400 mb-1">Step 1 · Phased Plan</div>
    <h3 class="text-base font-bold text-white mb-2">Bootstrap One Output Channel First</h3>
    <p class="text-xs text-gray-400 leading-relaxed">
      You can't probe 30 unknown pins blind. First find the OLED screen (<code>Phase 1 &amp; 2</code>) so the synth itself can display live GPIO &amp; ADC readings!
    </p>
  </div>

  <div class="p-5 rounded-xl bg-gray-900 border border-emerald-500/30">
    <div class="text-xs font-mono text-emerald-400 mb-1">Step 2 · Interactive Probing</div>
    <h3 class="text-base font-bold text-white mb-2">Turn Knobs, Press Keys, Log Truth</h3>
    <p class="text-xs text-gray-400 leading-relaxed">
      Flash diagnostic firmwares (<code>phase3_adc</code>, <code>phase4_keys_encoder</code>, <code>phase5_audio</code>) and record exact pin numbers, polarities, and timing hazards.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-gray-900 border border-emerald-500/30">
    <div class="text-xs font-mono text-emerald-400 mb-1">Step 3 · Split Facts vs. Idioms</div>
    <h3 class="text-base font-bold text-white mb-2">Two Complementary Skills</h3>
    <p class="text-xs text-gray-400 leading-relaxed">
      Package raw pinout truth + <code>gamma_pins.h</code> in <code>gamma-pinout</code>, and C++ peripheral driver architectures in <code>gamma-hardware-controls</code>.
    </p>
  </div>
</div>

<!--
How do you reverse-engineer a board with no schematic? You design a phased sequence of diagnostic firmwares where Phase 1 finds the display, and every subsequent phase uses that display to turn physical actions into verified pin tables.
-->

---
layout: default
---

<!-- S49 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Designing the 6-Phase Reverse-Engineering Plan (<code>PLAN.md</code>)</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-5 items-center">
  <div class="col-span-8 space-y-4">
    <div class="p-4 rounded-xl bg-gray-900 border border-emerald-500/40">
      <div class="text-xs font-mono text-emerald-400 uppercase mb-1">Exact AGY Prompt (Scenario 04)</div>
      <p class="font-mono text-xs text-white leading-relaxed m-0">
        "We have a Gamma mini synth built on the Daisy Seed 2 DFM (STM32H750IBK6), but no schematics or pinout table. Using our libdaisy-guide and daisysp-guide skills, design a phased, safe reverse-engineering plan (PLAN.md) starting with firmware backup and progressing through I2C scanning, ADC pot/joystick mapping, digital key scanning, and audio amp discovery."
      </p>
    </div>

    <div class="text-xs text-gray-300 space-y-1.5">
      <div class="font-semibold text-white">What to Watch For:</div>
      <ul class="list-disc pl-5 space-y-1 text-gray-400">
        <li>AGY activates <code>libdaisy-guide</code> and <code>daisysp-guide</code> to check valid Daisy Seed I2C, ADC, and GPIO pins.</li>
        <li>Designs a safe, dependency-ordered 6-phase probing roadmap (<code>PLAN.md</code>).</li>
      </ul>
    </div>
  </div>

  <div class="col-span-4 p-4 rounded-xl bg-emerald-950/15 border border-emerald-500/30 text-xs text-gray-300">
    <div class="font-mono text-emerald-300 uppercase mb-1">Key Insight</div>
    <div class="font-bold text-white mb-2">Bootstrapping Telemetry</div>
    <p class="text-gray-400">
      Once Phase 1 discovers the OLED screen on I2C, the OLED becomes our logic analyzer for Phases 2–5!
    </p>
  </div>
</div>

<!--
In Recording 4, we ask AGY—armed with <code>libdaisy-guide</code> and <code>daisysp-guide</code>—to design a safe, phased hardware reverse-engineering plan (<code>PLAN.md</code>). Let's watch the replay.
-->

---
layout: cast-full
act: Act 5 · Way 3 (Hardware Discovery)
badgeClass: badge-way3
title: "Recording 04: Designing the 6-Phase Hardware Probing Plan (PLAN.md)"
cast: /casts/reverse-engineering-plan.cast
autoPlay: false
speed: 3.0
idleTimeLimit: 1.0
fit: both
---

<!-- S50 -->
<!--
Click to play: AGY reads <code>libdaisy-guide</code> to identify all candidate I2C, ADC, and GPIO pins on the Daisy Seed 2 DFM and structures the 6-phase <code>PLAN.md</code> diagnostic roadmap.
-->

---
layout: default
---

<!-- S51 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The 6-Phase Hardware Probing Roadmap (<code>PLAN.md</code>)</h2>
</div>

<div class="grid grid-cols-3 gap-3.5 mt-5 text-xs">
  <div class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
    <div class="font-mono text-amber-300 font-bold">Phase 0 · Safety Net</div>
    <div class="text-white font-semibold mt-1">Factory Backup &amp; DFU Restore</div>
    <p class="text-gray-400 mt-1">Verify <code>gamma-v2.0.3.bin</code> restore and confirm <code>APP_TYPE = BOOT_SRAM</code> vector table entry.</p>
  </div>

  <div class="p-3.5 rounded-xl bg-gray-900 border border-emerald-500/30">
    <div class="font-mono text-emerald-300 font-bold">Phase 1 &amp; 2 · Visual Output</div>
    <div class="text-white font-semibold mt-1">I2C Bus Scan &amp; OLED Bringup</div>
    <p class="text-gray-400 mt-1">Scan <code>I2C1</code>, <code>I2C2</code>, <code>I2C4</code> across <code>0x08</code>–<code>0x77</code> to locate the 128&times;64 SSD1306 OLED screen.</p>
  </div>

  <div class="p-3.5 rounded-xl bg-gray-900 border border-emerald-500/30">
    <div class="font-mono text-emerald-300 font-bold">Phase 3 · Analog Controls</div>
    <div class="text-white font-semibold mt-1">ADC1 Pots &amp; Thumbsticks</div>
    <p class="text-gray-400 mt-1">Render live bar graphs for all 12 Daisy ADC pins on the OLED; turn each knob and stick axis one by one.</p>
  </div>

  <div class="p-3.5 rounded-xl bg-gray-900 border border-emerald-500/30">
    <div class="font-mono text-emerald-300 font-bold">Phase 4 · Digital Inputs</div>
    <div class="text-white font-semibold mt-1">14 Keys &amp; Rotary Encoder</div>
    <p class="text-gray-400 mt-1">Poll all remaining candidate GPIOs with internal pull-ups (<code>INPUT_PULLUP</code>) and display active-low pin indices on screen.</p>
  </div>

  <div class="p-3.5 rounded-xl bg-gray-900 border border-emerald-500/30">
    <div class="font-mono text-emerald-300 font-bold">Phase 5 · Audio &amp; Amp</div>
    <div class="text-white font-semibold mt-1">PCM3060 Codec &amp; Speaker Enable</div>
    <p class="text-gray-400 mt-1">Output a 440 Hz test tone via SAI1 and probe candidate output pins to unmute the internal speaker amplifier.</p>
  </div>

  <div class="p-3.5 rounded-xl bg-gray-900 border border-cyan-500/30">
    <div class="font-mono text-cyan-300 font-bold">Phase 6 · Synthesis</div>
    <div class="text-white font-semibold mt-1">Distill into Skills &amp; Build Synths</div>
    <p class="text-gray-400 mt-1">Freeze all discoveries into <code>gamma-pinout</code> and <code>gamma-hardware-controls</code>, then build full instruments.</p>
  </div>
</div>

<!--
Here is the 6-phase probing roadmap from <code>PLAN.md</code>. Notice how each phase builds on the last: Phase 0 secures recovery, Phase 1-2 unlocks the OLED screen, and Phases 3, 4, and 5 use the OLED screen to map every analog, digital, and audio pin.
-->

---
layout: default
---

<!-- S52 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Phase 1 &amp; 2 (<code>phase1_i2c_scan</code>): Finding the OLED Screen</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-5 items-center">
  <div class="col-span-6 space-y-3 text-xs">
    <p class="text-sm text-gray-300 leading-relaxed">
      How does <code>phase1_i2c_scan</code> report which I2C bus and address answered if we don't have a screen or working USB serial yet?
    </p>
    <div class="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-2">
      <div class="font-mono font-bold text-emerald-300">Clever Bootstrap Trick:</div>
      <p class="text-gray-300">
        Have the firmware scan every <code>(Bus, Address)</code> pair, and as soon as a device ACKs, <strong>immediately initialize an SSD1306 driver on that bus/address</strong> and draw the result onto the screen itself!
      </p>
    </div>
  </div>

  <div class="col-span-6">

```cpp
// Verified OLED Discovery on Gamma Mini Synth:
I2CHandle::Config i2c_config;
i2c_config.periph         = I2CHandle::Config::Peripheral::I2C_1;
i2c_config.speed          = I2CHandle::Config::Speed::I2C_1MHZ;
i2c_config.pin_config.scl = seed::D11; // PB8 (I2C1_SCL)
i2c_config.pin_config.sda = seed::D12; // PB9 (I2C1_SDA)

// 7-bit I2C Address: 0x3D (128x64 SSD1306)
oled_config.driver_config.transport_config.i2c_address = 0x3D;
```

    <div class="mt-3 p-2.5 rounded bg-amber-950/20 border border-amber-500/30 text-xs text-amber-200 font-mono">
      Bonus Discovery: Must call <code>__HAL_RCC_I2C1_FORCE_RESET()</code> on boot to clear stalled I2C1 state after soft-resetting!
    </div>
  </div>
</div>

<!--
In Phase 1, how do you read I2C scan results without a screen or serial port? We had the scanner try initializing an SSD1306 driver on every I2C address that ACKed—and the OLED lit up immediately on <code>I2C1</code> (<code>D11</code>/<code>D12</code>) at address <code>0x3D</code>!
-->

---
layout: default
---

<!-- S53 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Phase 3 (<code>phase3_adc</code>): Mapping Knobs &amp; Thumbsticks</h2>
</div>

<div class="grid grid-cols-2 gap-5 mt-5 text-xs">
  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-2">
    <div class="font-mono text-emerald-300 uppercase">4 Top Rotary Potentiometers (Left &rarr; Right)</div>
    <table>
      <thead>
        <tr><th>Control</th><th>Daisy Pin</th><th>STM32 / ADC1</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>Knob 1 (Chord Vol)</strong></td><td><code>seed::D18</code></td><td><code>PA7</code> / <code>ADC1_INP7</code></td></tr>
        <tr><td><strong>Knob 2 (Chord Filter)</strong></td><td><code>seed::D17</code></td><td><code>PB1</code> / <code>ADC1_INP5</code></td></tr>
        <tr><td><strong>Knob 3 (Notes Vol)</strong></td><td><code>seed::D19</code></td><td><code>PA6</code> / <code>ADC1_INP3</code></td></tr>
        <tr><td><strong>Knob 4 (Notes Filter)</strong></td><td><code>seed::D20</code></td><td><code>PC1</code> / <code>ADC1_INP11</code></td></tr>
      </tbody>
    </table>
    <p class="text-gray-400 pt-1">Notice <code>D18</code> comes physically before <code>D17</code> on the top panel!</p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-2">
    <div class="font-mono text-cyan-300 uppercase">2 Dual-Axis Thumbsticks (4 Analog Axes)</div>
    <table>
      <thead>
        <tr><th>Stick Axis</th><th>Daisy Pin</th><th>STM32 / ADC1</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>Left Stick X (LX)</strong></td><td><code>seed::D22</code></td><td><code>PA5</code> / <code>ADC1_INP19</code></td></tr>
        <tr><td><strong>Left Stick Y (LY)</strong></td><td><code>seed::D21</code></td><td><code>PC4</code> / <code>ADC1_INP4</code></td></tr>
        <tr><td><strong>Right Stick X (RX)</strong></td><td><code>seed::D24</code></td><td><code>PA1</code> / <code>ADC1_INP17</code></td></tr>
        <tr><td><strong>Right Stick Y (RY)</strong></td><td><code>seed::D23</code></td><td><code>PA4</code> / <code>ADC1_INP18</code></td></tr>
      </tbody>
    </table>
    <p class="text-gray-400 pt-1">Plus Auxiliary Battery Sense on <code>seed::D31</code> (<code>PC2</code> / <code>ADC1_INP12</code>).</p>
  </div>
</div>

<!--
With the OLED working, <code>phase3_adc</code> drew real-time bar graphs for all ADC channels on the screen. Turning each knob and moving each stick mapped all 4 pots (<code>D18</code>, <code>D17</code>, <code>D19</code>, <code>D20</code>) and all 4 joystick axes (<code>D22</code>, <code>D21</code>, <code>D24</code>, <code>D23</code>).
-->

---
layout: default
---

<!-- S54 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Polarity Surprise: Inverted Pots &amp; Asymmetric Sticks!</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-5 items-center">
  <div class="col-span-6 space-y-3 text-xs">
    <div class="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 space-y-2">
      <div class="font-mono font-bold text-amber-300 uppercase">Surprise 1: All 4 Knobs Are Wired Inverted</div>
      <p class="text-gray-300 leading-relaxed">
        Turning any top knob <strong>clockwise</strong> swept the ADC voltage from <code>3.3V &rarr; 0.0V</code> (<code>1.0f</code> down to <code>0.0f</code>). Without <code>1.0f - raw</code>, turning volume up turns the sound down!
      </p>
    </div>

    <div class="p-4 rounded-xl bg-purple-950/20 border border-purple-500/30 space-y-2">
      <div class="font-mono font-bold text-purple-300 uppercase">Surprise 2: 3 of 4 Stick Axes Are Inverted</div>
      <p class="text-gray-300 leading-relaxed">
        <strong>Left Stick X (<code>D22</code>)</strong> reads <code>0.0f</code> (Left) &rarr; <code>1.0f</code> (Right), while <strong>Right Stick X (<code>D24</code>)</strong> is rotated on the PCB and reads <code>1.0f</code> (Left) &rarr; <code>0.0f</code> (Right)!
      </p>
    </div>
  </div>

  <div class="col-span-6">

```cpp
// Verified in gamma_pins.h:
namespace knobs {
    constexpr bool invert[4] = {true, true, true, true};
}

namespace joysticks {
    constexpr bool invert[4] = {
        false, // Left X  (D22): Direct
        true,  // Left Y  (D21): Inverted (1.0f - raw)
        true,  // Right X (D24): Inverted (1.0f - raw)
        true   // Right Y (D23): Inverted (1.0f - raw)
    };
}
```

  </div>
</div>

<!--
And here was the biggest surprise of Phase 3: all four pots are wired with 3.3V on the counter-clockwise lug, so turning a knob clockwise decreases the raw ADC reading! Even wilder, 3 of the 4 joystick axes are inverted while Left X is normal.
-->

---
layout: default
---

<!-- S55 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Phase 4 (<code>phase4_keys_encoder</code>): 14 Keys &amp; Quadrature Encoder</h2>
</div>

<div class="grid grid-cols-12 gap-5 mt-5 text-xs">
  <div class="col-span-7 space-y-3">
    <div class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono text-emerald-300 font-bold mb-1">Left Keypad: 7 Note Keys (<code>N1</code>–<code>N7</code>)</div>
      <p class="text-gray-300 font-mono">
        <code>D1</code> (<code>PC11</code>), <code>D2</code> (<code>PC10</code>), <code>D3</code> (<code>PC9</code>), <code>D4</code> (<code>PC8</code>), <code>D5</code> (<code>PD2</code>), <code>D6</code> (<code>PC12</code>), <code>D7</code> (<code>PG10</code>)
      </p>
    </div>
    <div class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono text-cyan-300 font-bold mb-1">Right Keypad: 7 Chord Keys (<code>C1</code>–<code>C7</code>)</div>
      <p class="text-gray-300 font-mono">
        <code>D8</code> (<code>PG11</code>), <code>D9</code> (<code>PB4</code>), <code>D10</code> (<code>PB5</code>), <code>D13</code> (<code>PB6</code>), <code>D14</code> (<code>PB7</code>), <code>D26</code> (<code>PD11</code>), <code>D27</code> (<code>PG9</code>)
      </p>
    </div>
    <div class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono text-amber-300 font-bold mb-1">Rotary Encoder + Push Switch</div>
      <p class="text-gray-300 font-mono">
        Phase A: <code>D15</code> (<code>PC0</code>) &middot; Phase B: <code>D16</code> (<code>PA3</code>) &middot; Click: <code>D28</code> (<code>PA2</code>)
      </p>
    </div>
  </div>

  <div class="col-span-5 p-4 rounded-xl bg-red-950/20 border border-red-500/30 space-y-2">
    <div class="font-mono text-red-400 uppercase">The Display Blocking Hazard</div>
    <div class="text-sm font-bold text-white">Why Main-Loop Encoder Polling Drops Clicks</div>
    <p class="text-gray-300 leading-relaxed">
      <code>oled.Update()</code> blocks the main thread for <strong>~9.5 ms</strong> over I2C1. Quadrature encoder transitions last 1–3 ms!
    </p>
    <p class="text-emerald-300 font-semibold pt-1">
      Solution: Sample the encoder and 14 keys inside a <strong>1 kHz <code>TIM5</code> hardware interrupt</strong>!
    </p>
  </div>
</div>

<!--
In Phase 4, we mapped all 14 tactile switches (<code>N1</code>–<code>N7</code> and <code>C1</code>–<code>C7</code>) plus the rotary encoder (<code>D15</code>, <code>D16</code>, <code>D28</code>). We also discovered that <code>oled.Update()</code> blocks for 9.5 ms over I2C—so encoder & key polling must run inside a 1 kHz <code>TIM5</code> timer interrupt!
-->

---
layout: default
---

<!-- S56 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Phase 5 (<code>phase5_audio</code>): The Hidden Speaker Amplifier Pin</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-6 items-center">
  <div class="col-span-6 space-y-3 text-xs">
    <p class="text-sm text-gray-300 leading-relaxed">
      When we started <code>AudioCallback</code> at 48 kHz, audio played through the 3.5mm headphone jack—but the Gamma's <strong>built-in speaker was completely silent</strong>!
    </p>
    <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
      <div class="font-mono font-bold text-emerald-300">Discovery on <code>seed::D32</code> (<code>PC3</code>):</div>
      <p class="text-gray-300">
        The internal Class-D speaker amplifier has an active-HIGH enable/unmute line wired to <code>seed::D32</code> (<code>PC3</code>)—a pin on the Daisy Seed 2 DFM bottom pads!
      </p>
    </div>
  </div>

  <div class="col-span-6">

```cpp
// Pop-Free Speaker Amp Initialization Sequence:
GPIO spk_en;

// 1. Pull LOW immediately on boot to prevent startup pop
spk_en.Init(gamma_pins::speaker_amp::pin_enable, // seed::D32 (PC3)
            GPIO::Mode::OUTPUT,
            GPIO::Pull::NOPULL);
spk_en.Write(false);

// 2. Start SAI1 PCM3060 48kHz audio engine
hw.StartAudio(AudioCallback);

// 3. Drive HIGH after audio callback is running
spk_en.Write(true);
```

  </div>
</div>

<!--
In Phase 5, our 440 Hz test tone played on headphones, but the internal speaker was dead silent! Probing the remaining pins revealed that <code>seed::D32</code> (<code>PC3</code>) is an active-HIGH speaker amplifier enable pin. Driving <code>D32</code> HIGH brought the speaker to life.
-->

---
layout: default
---

<!-- S57 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Distilling Facts vs. Idioms: Why Two Hardware Skills?</h2>
</div>

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="p-5 rounded-xl bg-emerald-950/15 border border-emerald-500/40 space-y-3">
    <div class="flex items-center justify-between">
      <span class="font-mono text-sm font-bold text-emerald-300">gamma-pinout</span>
      <span class="text-xs px-2 py-0.5 rounded bg-gray-800 text-gray-300">Declarative Hardware Truth</span>
    </div>
    <p class="text-xs text-gray-300 leading-relaxed">
      Answers <strong>"What is connected where?"</strong>
    </p>
    <ul class="text-xs text-gray-400 space-y-1.5 list-disc pl-4">
      <li>Master 32-row pinout &amp; polarity table</li>
      <li>Drop-in <code>resources/gamma_pins.h</code> C++ header</li>
      <li>Zero driver state machines—pure hardware constants</li>
    </ul>
  </div>

  <div class="p-5 rounded-xl bg-emerald-950/15 border border-emerald-500/40 space-y-3">
    <div class="flex items-center justify-between">
      <span class="font-mono text-sm font-bold text-emerald-300">gamma-hardware-controls</span>
      <span class="text-xs px-2 py-0.5 rounded bg-gray-800 text-gray-300">Procedural Driver Idioms</span>
    </div>
    <p class="text-xs text-gray-300 leading-relaxed">
      Answers <strong>"How do I poll and render controls safely?"</strong>
    </p>
    <ul class="text-xs text-gray-400 space-y-1.5 list-disc pl-4">
      <li>1 kHz <code>TIM5</code> ISR Buxton Gray-code encoder state machine</li>
      <li>Lock-free key event queue &amp; IIR deadband pot smoothing</li>
      <li>5 deep subsystem guides in <code>references/*.md</code></li>
    </ul>
  </div>
</div>

<!--
Once Phases 1 through 5 were complete, we made a key architectural decision: we split our hardware knowledge into two skills—<code>gamma-pinout</code> for declarative pin truth and <code>gamma_pins.h</code>, and <code>gamma-hardware-controls</code> for non-blocking C++ driver idioms.
-->

---
layout: skill-breakdown
way: 3
skill: .agents/skills/gamma-pinout/SKILL.md
title: "gamma-pinout: Master Pinout & Polarity Table"
step: Zoom-In 1 of 4
---

<!-- S58 -->
<div class="space-y-2 text-xs">
  <table>
    <thead>
      <tr>
        <th>Peripheral</th>
        <th>Label</th>
        <th>Daisy Pin</th>
        <th>STM32 Pin</th>
        <th>Function / Channel</th>
        <th>Polarity / Logic</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>OLED Display</strong></td>
        <td>SCL / SDA</td>
        <td><code>D11</code> / <code>D12</code></td>
        <td><code>PB8</code> / <code>PB9</code></td>
        <td><code>I2C1</code> @ <code>0x3D</code></td>
        <td>1 MHz Fast Mode Plus</td>
      </tr>
      <tr>
        <td><strong>Top Pots</strong></td>
        <td>Knobs 1–4</td>
        <td><code>D18, D17, D19, D20</code></td>
        <td><code>PA7, PB1, PA6, PC1</code></td>
        <td><code>ADC1</code> (Ch 7, 5, 3, 11)</td>
        <td><strong>Inverted</strong>: <code>1.0f - raw</code></td>
      </tr>
      <tr>
        <td><strong>Left Stick</strong></td>
        <td>LX / LY</td>
        <td><code>D22</code> / <code>D21</code></td>
        <td><code>PA5</code> / <code>PC4</code></td>
        <td><code>ADC1</code> (Ch 19, 4)</td>
        <td>LX: Normal, LY: <strong>Inverted</strong></td>
      </tr>
      <tr>
        <td><strong>Right Stick</strong></td>
        <td>RX / RY</td>
        <td><code>D24</code> / <code>D23</code></td>
        <td><code>PA1</code> / <code>PA4</code></td>
        <td><code>ADC1</code> (Ch 17, 18)</td>
        <td>RX: <strong>Inverted</strong>, RY: <strong>Inverted</strong></td>
      </tr>
      <tr>
        <td><strong>Keypads</strong></td>
        <td>N1–N7, C1–C7</td>
        <td><code>D1–D10, D13–14, D26–27</code></td>
        <td>Multiple GPIOs</td>
        <td>GPIO In (<code>PULLUP</code>)</td>
        <td>Active LOW (<code>0</code> = Pressed)</td>
      </tr>
      <tr>
        <td><strong>Speaker Amp</strong></td>
        <td>Amp Enable</td>
        <td><code>seed::D32</code></td>
        <td><code>PC3</code></td>
        <td>GPIO Out Push-Pull</td>
        <td>Active HIGH (<code>1</code> = On)</td>
      </tr>
    </tbody>
  </table>
</div>

<!--
Zooming into <code>gamma-pinout/SKILL.md</code>: every single peripheral, Daisy Seed pin, STM32 port, ADC channel, and electrical polarity is documented in one authoritative table.
-->

---
layout: skill-breakdown
way: 3
skill: .agents/skills/gamma-pinout/resources/gamma_pins.h
title: "gamma-pinout: Bundling resources/gamma_pins.h"
step: Zoom-In 2 of 4
---

<!-- S59 -->
<div class="space-y-2 text-xs">

```cpp
#pragma once
#include "daisy_seed.h"

namespace gamma_pins {
namespace knobs {
    enum Index { CHORD_VOL = 0, CHORD_FILTER, NOTES_VOL, NOTES_FILTER, COUNT };
    constexpr daisy::Pin pins[COUNT] = {
        daisy::seed::D18, daisy::seed::D17, daisy::seed::D19, daisy::seed::D20
    };
    constexpr bool invert[COUNT] = {true, true, true, true};
}
namespace note_keys {
    constexpr daisy::Pin pins[7] = {
        daisy::seed::D1, daisy::seed::D2, daisy::seed::D3,
        daisy::seed::D4, daisy::seed::D5, daisy::seed::D6, daisy::seed::D7
    };
}
namespace speaker_amp {
    constexpr daisy::Pin pin_enable = daisy::seed::D32; // PC3 (Active HIGH)
}
} // namespace gamma_pins
```

  <div class="p-2.5 rounded bg-emerald-950/20 border border-emerald-500/30 text-emerald-200">
    Instead of re-typing 30 GPIO pin numbers from markdown, the agent simply copies <code>resources/gamma_pins.h</code> into the firmware directory and <code>#include</code>s it!
  </div>
</div>

<!--
Even better, <code>gamma-pinout</code> bundles <code>resources/gamma_pins.h</code> right inside the skill directory. The agent doesn't have to transcribe 30 pin numbers from markdown—it just copies <code>gamma_pins.h</code> into the project and <code>#include</code>s it.
-->

---
layout: skill-breakdown
way: 3
skill: .agents/skills/gamma-hardware-controls/SKILL.md
title: "gamma-hardware-controls: 1 kHz TIM5 ISR & Diagnostic Table"
step: Zoom-In 3 of 4
---

<!-- S60 -->
<div class="grid grid-cols-12 gap-4 items-center text-xs">
  <div class="col-span-6 space-y-2">
    <div class="font-mono text-emerald-300 uppercase">1 kHz Hardware Timer (<code>TIM5</code>)</div>

```cpp
// Sample encoder & 14 keys at 1000 Hz
// Immune to 9.5ms I2C OLED frame updates!
TimerHandle::Config tim_cfg;
tim_cfg.periph     = TimerHandle::Config::Peripheral::TIM_5;
tim_cfg.dir        = TimerHandle::Config::CounterDir::UP;
tim_cfg.period     = 240000 - 1; // 240MHz / 240k = 1kHz
tim_cfg.enable_irq = true;
```

  </div>

  <div class="col-span-6 space-y-2">
    <div class="font-mono text-amber-300 uppercase">Symptom &rarr; Cause Lookup in SKILL.md</div>
    <table>
      <thead>
        <tr><th>Symptom</th><th>Root Cause</th></tr>
      </thead>
      <tbody>
        <tr><td>OLED blank on soft reboot</td><td>Missing <code>I2C1_FORCE_RESET</code></td></tr>
        <tr><td>Encoder misses clicks</td><td>Polled in main loop vs <code>TIM5</code></td></tr>
        <tr><td>Controls freeze during play</td><td>Runaway DSP (<code>AnalogBassDrum</code> &gt; 90 Hz) starving <code>TIM5</code> ISR</td></tr>
      </tbody>
    </table>
  </div>
</div>

<!--
In <code>gamma-hardware-controls/SKILL.md</code>, we give the agent the 1 kHz <code>TIM5</code> hardware interrupt architecture so OLED updates never drop encoder clicks, plus a symptom-to-root-cause troubleshooting table.
-->

---
layout: skill-breakdown
way: 3
skill: .agents/skills/gamma-hardware-controls/references/
title: "gamma-hardware-controls: Progressive Disclosure via references/"
step: Zoom-In 4 of 4
---

<!-- S61 -->
<div class="grid grid-cols-5 gap-2.5 text-xs mt-2">
  <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
    <div class="font-mono font-bold text-emerald-300 mb-1">display.md</div>
    <p class="text-gray-400 text-[11px]">
      <code>I2C1</code> force-reset sequence, <code>I2C_1MHZ</code> config, 30 Hz frame throttling.
    </p>
  </div>

  <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
    <div class="font-mono font-bold text-emerald-300 mb-1">analog_inputs.md</div>
    <p class="text-gray-400 text-[11px]">
      9-channel <code>AdcChannelConfig</code>, pot inversion, soft-takeover / pickup logic.
    </p>
  </div>

  <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
    <div class="font-mono font-bold text-emerald-300 mb-1">digital_keys.md</div>
    <p class="text-gray-400 text-[11px]">
      14 active-low keys, 8ms shift-register debounce, lock-free <code>KeyEvent</code> ring buffer.
    </p>
  </div>

  <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
    <div class="font-mono font-bold text-emerald-300 mb-1">rotary_encoder.md</div>
    <p class="text-gray-400 text-[11px]">
      Buxton Gray-code state table eliminating mechanical contact bounce.
    </p>
  </div>

  <div class="p-3 rounded-lg bg-gray-900 border border-emerald-500/40">
    <div class="font-mono font-bold text-white mb-1">main_loop_blueprint.md</div>
    <p class="text-gray-300 text-[11px]">
      Complete end-to-end C++ firmware skeleton combining all 4 subsystems!
    </p>
  </div>
</div>

<div class="mt-4 p-3 rounded-lg bg-gray-900/70 border border-gray-800 text-xs text-gray-300 text-center">
  <code>SKILL.md</code> stays a crisp 91-line index; the agent reads only the specific <code>references/*.md</code> file it needs.
</div>

<!--
Look at how <code>gamma-hardware-controls</code> uses Tier-3 <code>references/</code>: <code>SKILL.md</code> is only 91 lines long, pointing to five deep reference files—<code>display.md</code>, <code>analog_inputs.md</code>, <code>digital_keys.md</code>, <code>rotary_encoder.md</code>, and <code>main_loop_blueprint.md</code>.
-->

---
layout: default
---

<!-- S62 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Way 3 Takeaway: Hardware Discovery Skills</h2>
</div>

<div class="grid grid-cols-3 gap-5 mt-8">
  <div class="p-5 rounded-xl bg-emerald-950/15 border border-emerald-500/30">
    <div class="text-xs font-mono text-emerald-400 uppercase mb-1">Takeaway 1</div>
    <h3 class="text-base font-bold text-white mb-2">Telemetry First</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      When reverse-engineering hardware with an agent, prioritize bringing up a visual or serial output channel in Phase 1 so the device can report its own state.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-emerald-950/15 border border-emerald-500/30">
    <div class="text-xs font-mono text-emerald-400 uppercase mb-1">Takeaway 2</div>
    <h3 class="text-base font-bold text-white mb-2">Bundle Verified Code (<code>resources/</code>)</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      Don't just describe pin numbers in prose—ship a tested <code>gamma_pins.h</code> header in <code>resources/</code> so future builds have zero transcription errors.
    </p>
  </div>

  <div class="p-5 rounded-xl bg-emerald-950/15 border border-emerald-500/30">
    <div class="text-xs font-mono text-emerald-400 uppercase mb-1">Takeaway 3</div>
    <h3 class="text-base font-bold text-white mb-2">Separate Truth from Drivers</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      Keeping <code>gamma-pinout</code> (facts) distinct from <code>gamma-hardware-controls</code> (ISR drivers) keeps both skills modular and easy to maintain.
    </p>
  </div>
</div>

<!--
That's Way 3: Hardware Discovery Skills. Turn ephemeral debugging sessions into permanent, verifiable hardware abstractions by bundling both declarative truth (<code>gamma_pins.h</code>) and real-time driver blueprints.
-->

---
layout: center
class: text-center
---

<!-- S63 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    The Mashup Skill
  </h1>
  <p class="text-xl font-mono text-purple-300">
    gamma-usb-connectivity
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    Combining Pinout Truth + Deadlock-Immune C++ Firmware Driver + Host Python Utility in a single skill
  </p>
</div>

<!--
Now we arrive at Act 6: our seventh skill, <code>gamma-usb-connectivity</code>. We call this "The Mashup Skill" because solving USB serial on the Gamma required combining all three ways into a single package.
-->

---
layout: default
---

<!-- S64 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Mystery: Why Did <code>hw.StartLog()</code> Produce Zero Output?</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-6 items-center">
  <div class="col-span-6 space-y-3 text-xs">
    <p class="text-sm text-gray-300 leading-relaxed">
      Every standard <code>libDaisy</code> tutorial starts USB serial logging with two lines of code:
    </p>

```cpp
hw.StartLog();
hw.PrintLine("Hello from Daisy!");
```

    <p class="text-sm text-gray-300 leading-relaxed">
      Yet when we flashed this to the Gamma, <strong>no <code>/dev/cu.usbmodem*</code> port ever appeared on macOS</strong>! Even worse, passing <code>hw.StartLog(true)</code> (wait for terminal) froze the synth at boot forever.
    </p>
  </div>

  <div class="col-span-6 p-5 rounded-xl bg-purple-950/20 border border-purple-500/30 space-y-2 text-xs">
    <div class="font-mono text-purple-300 uppercase">Why Did Standard Daisy Logging Fail?</div>
    <p class="text-gray-300 leading-relaxed">
      The STM32H750 actually has <strong>two separate USB OTG controllers</strong>:
    </p>
    <ul class="list-disc pl-5 space-y-1.5 text-gray-300">
      <li><code>USB_OTG_FS</code> (<code>PA11</code>/<code>PA12</code>): The micro-USB port on a standard Daisy Seed (<code>UsbHandle::FS_INTERNAL</code> / <code>LOGGER_INTERNAL</code>).</li>
      <li><code>USB_OTG_HS</code> in FS mode (<code>PB14</code>/<code>PB15</code>, pins <code>D29</code>/<code>D30</code>): The external USB pins (<code>UsbHandle::FS_EXTERNAL</code>).</li>
    </ul>
  </div>
</div>

<!--
Here was the mystery: every <code>libDaisy</code> example uses <code>hw.StartLog()</code>, which defaults to <code>LOGGER_INTERNAL</code> on pins <code>PA11</code>/<code>PA12</code>. On the Gamma, <code>hw.StartLog()</code> produced zero USB enumeration! Why?
-->

---
layout: default
---

<!-- S65 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">On-OLED Register Debugging: Discovering <code>UsbHandle::FS_EXTERNAL</code></h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-5 items-center">
  <div class="col-span-6 space-y-3 text-xs">
    <p class="text-sm text-gray-300 leading-relaxed">
      Using the OLED display we unlocked in Phase 2, we rendered live STM32 USB OTG peripheral register states directly on the synth screen while plugging and unplugging the USB-C cable.
    </p>
    <div class="p-3.5 rounded-xl bg-gray-900 border border-gray-800 space-y-1.5">
      <div class="font-mono text-emerald-300 font-bold">Hardware Discovery:</div>
      <p class="text-gray-300">
        The Gamma's chassis USB-C port is wired to <strong><code>seed::D29</code> (<code>PB14</code>) and <code>seed::D30</code> (<code>PB15</code>)</strong>—which connects to the STM32's second USB peripheral (<code>UsbHandle::FS_EXTERNAL</code>)!
      </p>
    </div>
  </div>

  <div class="col-span-6">

```cpp
// Wrong (Daisy Seed onboard port - unconnected):
hw.StartLog(); // Uses LOGGER_INTERNAL (PA11/PA12)

// Correct Hardware Port on Gamma Mini Synth:
hw.usb_handle.Init(UsbHandle::FS_EXTERNAL); // D29/D30
```

    <div class="mt-3 p-3 rounded-lg bg-purple-950/25 border border-purple-500/40 text-xs text-purple-200 font-mono">
      Enumerates on host as:<br/>
      VID:PID <code>0483:5740</code> &middot; <code>"Daisy Seed External"</code><br/>
      macOS: <code>/dev/cu.usbmodem*</code>
    </div>
  </div>
</div>

<!--
By displaying the STM32 USB registers on the OLED screen, we proved that the Gamma's USB-C port is wired to <code>D29</code> and <code>D30</code>—<code>UsbHandle::FS_EXTERNAL</code>. The moment we initialized <code>FS_EXTERNAL</code>, <code>/dev/cu.usbmodem*</code> appeared on macOS!
-->

---
layout: default
---

<!-- S66 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Two Real-Time USB Deadlocks That Hung the Synth</h2>
</div>

<div class="grid grid-cols-2 gap-5 mt-6 text-xs">
  <div class="p-5 rounded-xl bg-red-950/20 border border-red-500/30 space-y-2.5">
    <div class="font-mono text-red-400 uppercase">Hazard 1: Disconnect Spinloop</div>
    <h3 class="text-base font-bold text-white"><code>Logger&lt;LOGGER_EXTERNAL&gt;::TransmitSync()</code></h3>
    <p class="text-gray-300 leading-relaxed">
      When a serial terminal connects and then closes, the host stops reading the USB IN endpoint. <code>libDaisy</code>'s built-in <code>Logger</code> calls <code>TransmitSync()</code>, which spins in an <strong>infinite <code>while(1)</code> loop</strong> waiting for TX-complete—freezing the main loop forever!
    </p>
  </div>

  <div class="p-5 rounded-xl bg-red-950/20 border border-red-500/30 space-y-2.5">
    <div class="font-mono text-red-400 uppercase">Hazard 2: USB ISR Self-Deadlock</div>
    <h3 class="text-base font-bold text-white">Printing Inside <code>UsbRxCallback</code></h3>
    <p class="text-gray-300 leading-relaxed">
      <code>UsbRxCallback</code> fires inside the <strong>USB OTG interrupt handler</strong>. Calling any blocking transmit function inside <code>UsbRxCallback</code> causes an immediate hardware deadlock because the TX-complete interrupt cannot preempt the active RX ISR!
    </p>
  </div>
</div>

<!--
Getting USB to enumerate was only half the battle. In real-time synthesis, standard <code>libDaisy</code> USB logging has two fatal deadlocks: <code>TransmitSync()</code> freezes forever the moment you close your terminal window, and printing inside <code>UsbRxCallback</code> deadlocks the USB ISR.
-->

---
layout: default
---

<!-- S67 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Why <code>gamma-usb-connectivity</code> Is a Three-Way Mashup</h2>
</div>

<div class="grid grid-cols-3 gap-4 mt-6 text-xs">
  <div class="p-4 rounded-xl bg-gray-900 border border-emerald-500/40 space-y-2">
    <span class="px-2 py-0.5 rounded-full badge-way3 text-[10px] uppercase font-semibold">From Way 3 · Hardware Truth</span>
    <div class="font-mono font-bold text-white text-sm pt-1">SKILL.md Pinout &amp; VID/PID</div>
    <p class="text-gray-400 leading-relaxed">
      Documents <code>UsbHandle::FS_EXTERNAL</code> on <code>D29</code>/<code>D30</code> (<code>PB14</code>/<code>PB15</code>), VID/PID <code>0483:5740</code>, and why <code>hw.StartLog()</code> must never be used.
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-cyan-500/40 space-y-2">
    <span class="px-2 py-0.5 rounded-full badge-way1 text-[10px] uppercase font-semibold">From Way 1 · C++ Architecture</span>
    <div class="font-mono font-bold text-white text-sm pt-1">resources/gamma_usb.h</div>
    <p class="text-gray-400 leading-relaxed">
      Drop-in C++ driver (<code>gamma_usb::UsbComm</code>) with a 4-buffer non-blocking TX pool, 500 &mu;s timeout, 200 ms backoff, and lock-free RX ring buffer.
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-amber-500/40 space-y-2">
    <span class="px-2 py-0.5 rounded-full badge-way2 text-[10px] uppercase font-semibold">From Way 2 · Operational CLI</span>
    <div class="font-mono font-bold text-white text-sm pt-1">scripts/gamma_usb.py</div>
    <p class="text-gray-400 leading-relaxed">
      Zero-dependency Python <code>termios</code> host utility for live serial monitoring, command dispatch, and sending <code>'b'</code> to reboot into DFU mode.
    </p>
  </div>
</div>

<!--
To solve this cleanly for the agent, <code>gamma-usb-connectivity</code> mashes up all three ways in one skill directory: Way 3 hardware truth in <code>SKILL.md</code>, a Way 1 deadlock-free C++ header in <code>resources/gamma_usb.h</code>, and a Way 2 host Python CLI in <code>scripts/gamma_usb.py</code>.
-->

---
layout: skill-breakdown
way: mashup
skill: .agents/skills/gamma-usb-connectivity/SKILL.md
title: "Mashup Breakdown 1: USB Hardware & Deadlock Rules"
step: Zoom-In 1 of 3
---

<!-- S68 -->
<div class="space-y-3 text-xs">

```yaml
---
name: gamma-usb-connectivity
description: >-
  Comprehensive guide and implementation reference for USB connectivity on the this.is.NOISE
  Gamma Mini Synth (Electro-Smith Daisy Seed 2 DFM): USB CDC Virtual COM Port configuration,
  deadlock-immune non-blocking logging, bidirectional host-synth command dispatch, Python host
  communication scripts, and firmware integration examples.
---
```

  <div class="grid grid-cols-2 gap-4 pt-1">
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-purple-300 mb-1">Namespace Trap Documented:</div>
      <p class="text-gray-300">
        <code>using namespace gamma_usb;</code> — <strong>never</strong> name a C++ namespace <code>gamma</code> because newlib's <code>&lt;math.h&gt;</code> defines <code>double gamma(double)</code>!
      </p>
    </div>
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-purple-300 mb-1">Built-In DFU Reboot Hook:</div>
      <p class="text-gray-300">
        Receiving ASCII <code>'b'</code> or <code>'B'</code> in <code>UsbComm::Process()</code> mutes <code>PC3</code>, clears the OLED, and calls <code>System::ResetToBootloader()</code>.
      </p>
    </div>
  </div>
</div>

<!--
Look at <code>gamma-usb-connectivity/SKILL.md</code>: it documents even subtle C++ traps like never naming your namespace <code>gamma</code> (which collides with <code>&lt;math.h&gt;</code>'s <code>gamma()</code> function in newlib) and building in the <code>'b'</code> soft-reboot command.
-->

---
layout: skill-breakdown
way: mashup
skill: .agents/skills/gamma-usb-connectivity/resources/gamma_usb.h
title: "Mashup Breakdown 2: Non-Blocking C++ Driver (gamma_usb.h)"
step: Zoom-In 2 of 3
---

<!-- S69 -->
<div class="space-y-2 text-xs">

```cpp
// 1. ISR-Safe RX Callback: Only pushes bytes into lock-free ring buffer!
static void RxCallbackInternal(uint8_t* buf, uint32_t* len) {
    for(uint32_t i = 0; i < *len; i++) {
        size_t next = (s_rx_head + 1) % kRxQueueSize;
        if(next != s_rx_tail) { s_rx_queue[s_rx_head] = (char)buf[i]; s_rx_head = next; }
    }
}

// 2. Timeout-Guarded TX with 4-Buffer Pool & 200ms Disconnect Backoff:
uint32_t start_us = System::GetUs();
while(s_hw->usb_handle.TransmitExternal((uint8_t*)buf, len) == UsbHandle::Result::ERR) {
    if((System::GetUs() - start_us) >= 500) { // Max 500 us wait
        s_last_timeout_ms = now_ms;           // Fast-fail for next 200 ms!
        break;
    }
}
```

  <div class="p-2.5 rounded bg-purple-950/20 border border-purple-500/30 text-purple-200">
    Whether a terminal is connected, disconnected, or closed mid-session, <code>UsbComm::PrintLine()</code> never stalls the synth loop!
  </div>
</div>

<!--
Inside <code>resources/gamma_usb.h</code>, <code>RxCallbackInternal</code> only pushes bytes into a lock-free ring buffer, and <code>TransmitExternal</code> caps waiting at 500 microseconds with a 200 millisecond fast-fail backoff when no terminal is listening.
-->

---
layout: skill-breakdown
way: mashup
skill: .agents/skills/gamma-usb-connectivity/scripts/gamma_usb.py
title: "Mashup Breakdown 3: Zero-Dependency Host Script (gamma_usb.py)"
step: Zoom-In 3 of 3
---

<!-- S70 -->
<div class="grid grid-cols-12 gap-4 items-center text-xs">
  <div class="col-span-7">

```bash
# Auto-detects /dev/cu.usbmodem* and runs automated ping/help check:
python3 .agents/skills/gamma-usb-connectivity/scripts/gamma_usb.py --test

# Send a command ('m' = toggle mode, 'w' = cycle waveform) & read reply:
python3 .agents/skills/gamma-usb-connectivity/scripts/gamma_usb.py --send h

# Trigger software reboot straight into Daisy DFU Bootloader:
python3 .agents/skills/gamma-usb-connectivity/scripts/gamma_usb.py --bootloader
```

  </div>

  <div class="col-span-5 space-y-2">
    <div class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-purple-300 mb-1">Zero Pip Dependencies</div>
      <p class="text-gray-300 leading-relaxed">
        Uses Python's built-in POSIX <code>termios</code>, <code>tty</code>, and <code>select</code> modules out of the box—so the agent can verify live firmware telemetry in any environment without <code>pip install pyserial</code>.
      </p>
    </div>
  </div>
</div>

<!--
And on the host side, <code>scripts/gamma_usb.py</code> uses standard-library POSIX <code>termios</code>—zero pip dependencies—so the agent can run <code>--test</code>, send interactive commands with <code>--send</code>, or reboot into DFU mode with <code>--bootloader</code>.
-->

---
layout: center
class: text-center
---

<!-- S71 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Putting All 7 Skills to the Test
  </h1>
  <p class="text-xl text-gray-300">
    Building a 7-Voice Drum Synth: <strong>Without Skills</strong> vs. <strong>With Skills</strong>
  </p>
</div>

<!--
Now for Act 7—the payoff! We have all seven skills in <code>.agents/skills/</code>. What happens when we give an agent the exact same prompt to build a 7-voice Drum Synth for the Gamma mini synth WITHOUT skills versus WITH skills?
-->

---
layout: default
---

<!-- S72 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Identical Prompt, Two Workspaces</h2>
</div>

<div class="p-4 rounded-xl bg-gray-900 border border-gray-700 mt-4">
  <div class="text-xs font-mono text-cyan-400 uppercase mb-1">Identical Prompt Given to Both Agents (Scenarios 05 &amp; 06)</div>
  <p class="font-mono text-sm text-white leading-relaxed m-0">
    "Write and build a complete C++ firmware for a 7-voice drum synth on the this.is.NOISE Gamma mini synth using libDaisy and DaisySP, mapping the drum voices to the front keys and filter controls to the knobs."
  </p>
</div>

<div class="grid grid-cols-2 gap-5 mt-5 text-xs">
  <div class="p-4 rounded-xl bg-red-950/15 border border-red-500/30">
    <div class="font-mono font-bold text-red-400 uppercase mb-1">Workspace A (Scenario 05)</div>
    <div class="text-base font-bold text-white mb-1">Without Skills</div>
    <p class="text-gray-400">
      Contains checkouts of <code>libDaisy/</code> and <code>DaisySP/</code>, plus <code>arm-none-eabi-gcc</code>—and <strong>zero skills</strong> in <code>.agents/skills/</code>.
    </p>
  </div>

  <div class="p-4 rounded-xl bg-emerald-950/15 border border-emerald-500/30">
    <div class="font-mono font-bold text-emerald-400 uppercase mb-1">Workspace B (Scenario 06)</div>
    <div class="text-base font-bold text-white mb-1">With All 7 Skills</div>
    <p class="text-gray-400">
      Identical <code>libDaisy/</code> and <code>DaisySP/</code> checkouts, plus <strong>all 7 skills</strong> installed in <code>.agents/skills/</code>.
    </p>
  </div>
</div>

<!--
To make this a fair scientific comparison, both runs receive the exact same one-sentence prompt and have local checkouts of <code>libDaisy/</code> and <code>DaisySP/</code>. The only difference is <code>.agents/skills/</code>.
-->

---
layout: default
---

<!-- S73 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Attempt 1: Building the Drum Synth WITHOUT Skills</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-6 items-center">
  <div class="col-span-7 space-y-3 text-xs">
    <div class="text-sm font-bold text-white">What Happens When the Agent Has Only Raw Library Source?</div>
    <ul class="list-disc pl-5 space-y-2 text-gray-300 leading-relaxed">
      <li>It searches <code>libDaisy/</code> and <code>DaisySP/</code> to find <code>AnalogBassDrum</code>, <code>AnalogSnareDrum</code>, <code>HiHat</code>, and <code>Svf</code>.</li>
      <li>It writes plausible-looking C++ that <strong>compiles cleanly</strong> (<code>0 errors</code>)!</li>
      <li><strong>Wait—if it compiles with zero errors, does it work on the Gamma?</strong></li>
      <li>Watch closely what pins, <code>Makefile</code> settings, and audio initialization it chooses...</li>
    </ul>
  </div>

  <div class="col-span-5 p-5 rounded-xl bg-red-950/20 border border-red-500/30 text-xs text-gray-300 space-y-2">
    <div class="font-mono text-red-400 uppercase">The "Compiles != Works" Trap</div>
    <p>
      In embedded systems, code that compiles cleanly with guessed GPIO pins and default linker flags will brick or stay completely silent on real hardware.
    </p>
  </div>
</div>

<!--
Let's watch Attempt 1 first: building the drum synth WITHOUT skills. Spoiler alert: the agent writes C++ that compiles with zero errors—and fails on the physical hardware in five separate ways.
-->

---
layout: cast-full
act: Act 7 · Without Skills
badgeClass: bg-red-950 text-red-300 border border-red-500/40
title: "Recording 05: Building the 7-Voice Drum Synth WITHOUT Skills"
cast: /casts/drum-synth-without-skills.cast
autoPlay: false
speed: 3.0
idleTimeLimit: 1.0
fit: both
---

<!-- S74 -->
<!--
Click to play: watch the unskilled agent grep through <code>libDaisy</code> and <code>DaisySP</code>, guess sequential pins <code>D0</code> through <code>D6</code> for the keys and <code>A0</code> through <code>A3</code> for the knobs, omit <code>APP_TYPE = BOOT_SRAM</code>, and never enable the speaker amp.
-->

---
layout: default
---

<!-- S75 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Anatomy of the Failure (Without Skills)</h2>
</div>

<div class="mt-4">
  <table>
    <thead>
      <tr>
        <th>Subsystem</th>
        <th>What the Unskilled Agent Wrote</th>
        <th>What Happens on Physical Hardware</th>
      </tr>
    </thead>
    <tbody class="text-xs">
      <tr>
        <td><strong>1. Linker Target</strong></td>
        <td>Default <code>Makefile</code> (<code>BOOT_NONE</code> at <code>0x08000000</code>)</td>
        <td><span class="text-red-400 font-semibold">Bootloader rejects binary</span> &rarr; Red SOS LED blink!</td>
      </tr>
      <tr>
        <td><strong>2. Speaker Amp</strong></td>
        <td>Never configures <code>seed::D32</code> (<code>PC3</code>)</td>
        <td><span class="text-red-400 font-semibold">Internal speaker stays muted</span> &rarr; Dead silence!</td>
      </tr>
      <tr>
        <td><strong>3. Key Pins</strong></td>
        <td>Guessed <code>D0</code>–<code>D6</code> (<code>D0</code> is Battery Fault!)</td>
        <td><span class="text-red-400 font-semibold">Wrong GPIO mapping</span> &rarr; Keys don't trigger voices!</td>
      </tr>
      <tr>
        <td><strong>4. Potentiometers</strong></td>
        <td>Guessed <code>D15</code>–<code>D18</code> (<code>D15</code>/<code>D16</code> are Encoder!), raw <code>0..1</code></td>
        <td><span class="text-red-400 font-semibold">Wrong ADC pins &amp; backwards</span> (CW turns cutoff down)!</td>
      </tr>
      <tr>
        <td><strong>5. OLED &amp; USB</strong></td>
        <td>Guessed <code>0x3C</code> on <code>I2C1</code>; called <code>hw.StartLog()</code></td>
        <td><span class="text-red-400 font-semibold">Dead screen</span> (actual is <code>0x3D</code>) &amp; <span class="text-red-400 font-semibold">no USB serial</span>!</td>
      </tr>
    </tbody>
  </table>
</div>

<!--
Look at the post-mortem of Attempt 1: five fatal hardware bugs in code that compiled cleanly! Wrong <code>Makefile</code> target (SOS blink), muted speaker amp (<code>D32</code>), guessed key pins (<code>D0</code> is battery fault!), encoder pins wired as ADC knobs, and wrong OLED I2C address (<code>0x3C</code> vs <code>0x3D</code>).
-->

---
layout: default
---

<!-- S76 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Attempt 2: Building the Drum Synth WITH All 7 Skills</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-6 items-center">
  <div class="col-span-7 space-y-3 text-xs">
    <div class="text-sm font-bold text-white">Now Watch the Exact Same Prompt with Our 7 Skills Installed:</div>
    <ul class="list-disc pl-5 space-y-2 text-gray-300 leading-relaxed">
      <li>AGY immediately activates <code>gamma-pinout</code>, <code>gamma-hardware-controls</code>, <code>gamma-usb-connectivity</code>, <code>libdaisy-guide</code>, <code>daisysp-guide</code>, and <code>gamma-firmware-flash</code>.</li>
      <li>Copies <code>gamma_pins.h</code> and <code>gamma_usb.h</code> directly from <code>.agents/skills/*/resources/</code>.</li>
      <li>Configures <code>APP_TYPE = BOOT_SRAM</code>, unmutes <code>seed::D32</code>, sets up the 1 kHz <code>TIM5</code> ISR, inverts the 4 knobs, and compiles a verified <code>.bin</code>!</li>
    </ul>
  </div>

  <div class="col-span-5 p-5 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-xs text-gray-300 space-y-2">
    <div class="font-mono text-emerald-400 uppercase">Zero Guessing</div>
    <p>
      Every pin, polarity, timer interrupt, and linker flag is pulled from verified skill artifacts.
    </p>
  </div>
</div>

<!--
Now let's watch Attempt 2: the exact same prompt, but in a workspace with our 7 skills installed. Watch how the agent composes the skills together.
-->

---
layout: cast-full
act: Act 7 · With All 7 Skills
badgeClass: badge-way3
title: "Recording 06: Building the 7-Voice Drum Synth WITH All 7 Skills"
cast: /casts/drum-synth-with-skills.cast
autoPlay: false
speed: 4.0
idleTimeLimit: 1.0
fit: both
---

<!-- S77 -->
<!--
Click to play: AGY reads our skills, copies <code>gamma_pins.h</code> and <code>gamma_usb.h</code> into the project, wires all 7 drum voices to <code>N1</code>–<code>N7</code> and presets to <code>C1</code>–<code>C7</code>, sets <code>APP_TYPE = BOOT_SRAM</code>, and builds a verified binary at <code>0x24000000</code>.
-->

---
layout: default
---

<!-- S78 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">How All 7 Skills Composed Together</h2>
</div>

<div class="grid grid-cols-3 gap-3 mt-4 text-xs">
  <div class="p-3 rounded-xl border border-cyan-500/30 bg-cyan-950/10">
    <div class="font-mono font-bold text-cyan-300">1. libdaisy-guide</div>
    <p class="text-gray-400 mt-1">48 kHz SAI1 <code>AudioCallback</code>, <code>AdcChannelConfig</code>, <code>OledDisplay</code> setup.</p>
  </div>
  <div class="p-3 rounded-xl border border-cyan-500/30 bg-cyan-950/10">
    <div class="font-mono font-bold text-cyan-300">2. daisysp-guide</div>
    <p class="text-gray-400 mt-1">7 drum voices (<code>AnalogBassDrum</code> &le; 90 Hz, <code>AnalogSnareDrum</code>, <code>HiHat</code>, <code>Svf</code>).</p>
  </div>
  <div class="p-3 rounded-xl border border-emerald-500/30 bg-emerald-950/10">
    <div class="font-mono font-bold text-emerald-300">3. gamma-pinout</div>
    <p class="text-gray-400 mt-1">Provided <code>gamma_pins.h</code> (<code>D1</code>–<code>D7</code> keys, <code>D18/17/19/20</code> pots, <code>D32</code> speaker amp).</p>
  </div>
  <div class="p-3 rounded-xl border border-emerald-500/30 bg-emerald-950/10">
    <div class="font-mono font-bold text-emerald-300">4. gamma-hardware-controls</div>
    <p class="text-gray-400 mt-1">1 kHz <code>TIM5</code> key/encoder ISR, <code>1.0f - raw</code> pot inversion, <code>I2C1</code> <code>0x3D</code> OLED reset.</p>
  </div>
  <div class="p-3 rounded-xl border border-purple-500/30 bg-purple-950/10">
    <div class="font-mono font-bold text-purple-300">5. gamma-usb-connectivity</div>
    <p class="text-gray-400 mt-1">Provided <code>gamma_usb.h</code> on <code>FS_EXTERNAL</code> with <code>'b'</code> DFU bootloader command.</p>
  </div>
  <div class="p-3 rounded-xl border border-amber-500/30 bg-amber-950/10">
    <div class="font-mono font-bold text-amber-300">6 &amp; 7. flash &amp; restore</div>
    <p class="text-gray-400 mt-1">Verified <code>APP_TYPE = BOOT_SRAM</code> (<code>0x24000000</code>) and ready for live USB DFU flashing!</p>
  </div>
</div>

<div class="mt-4 p-3 rounded-lg bg-gray-900 border border-gray-800 text-center text-xs text-gray-300">
  No single mega-skill did this—<strong>6 small, focused skills composed seamlessly</strong> at task time.
</div>

<!--
Notice how the skills composed: <code>libdaisy-guide</code> and <code>daisysp-guide</code> handled the DSP engine, <code>gamma-pinout</code> supplied <code>gamma_pins.h</code>, <code>gamma-hardware-controls</code> supplied the 1 kHz <code>TIM5</code> ISR and pot inversion, and <code>gamma-usb-connectivity</code> added non-blocking telemetry and soft-rebooting.
-->

---
layout: center
class: text-center
---

<!-- S79 -->
<div class="space-y-5">
  <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-500/50 text-xs font-mono uppercase tracking-widest">
    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></span>
    Live Hardware Stage Demo
  </div>

  <h1 class="text-5xl font-extrabold text-white">
    Live Demo on the Gamma Mini Synth
  </h1>

  <div class="grid grid-cols-3 gap-4 max-w-3xl mx-auto text-left text-xs pt-4">
    <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono text-amber-300 font-bold mb-1">1. Factory Synth</div>
      <p class="text-gray-400">Play the physical Gamma running stock factory firmware.</p>
    </div>
    <div class="p-4 rounded-xl bg-gray-900 border border-emerald-500/40">
      <div class="font-mono text-emerald-300 font-bold mb-1">2. Flash <code>drum_synth</code></div>
      <p class="text-gray-400">Run <code>flash_firmware.py</code> via <code>gamma-firmware-flash</code> over USB-C.</p>
    </div>
    <div class="p-4 rounded-xl bg-gray-900 border border-cyan-500/40">
      <div class="font-mono text-cyan-300 font-bold mb-1">3. Play the 7 Drum Voices</div>
      <p class="text-gray-400">Trigger Kick, Snare, Hats, Clap, Tom &amp; sweep the DJ filter live!</p>
    </div>
  </div>
</div>

<!--
Now let's put the slides aside for a moment and do this live on the physical Gamma Mini Synth right here on stage! First I'll play the factory synth, then we'll run <code>flash_firmware.py</code> to flash the <code>drum_synth</code> binary we just built, and play the 7 drum voices live.
-->

---
layout: default
---

<!-- S80 -->
<div class="flex items-center justify-between mb-4">
  <div class="flex items-center gap-3">
    <h2 class="text-2xl font-bold m-0">Skills Three Ways: Key Takeaways &amp; Links</h2>
  </div>
  <span class="text-xs font-mono text-gray-400">Brett Morgan &middot; Google Cloud DevRel</span>
</div>

<div class="grid grid-cols-4 gap-3 mt-4 text-xs">
  <div class="p-3.5 rounded-xl border border-cyan-500/40 bg-cyan-950/15">
    <div class="font-mono font-bold text-cyan-300 uppercase mb-1">Way 1 · Library Review</div>
    <p class="text-gray-300">Audit C++ source repos once &rarr; package architecture &amp; memory rules into <code>SKILL.md</code> + <code>references/</code>.</p>
  </div>
  <div class="p-3.5 rounded-xl border border-amber-500/40 bg-amber-950/15">
    <div class="font-mono font-bold text-amber-300 uppercase mb-1">Way 2 · Operational</div>
    <p class="text-gray-300">Wrap fragile hardware timing &amp; binary validation into deterministic <code>scripts/*.py</code>.</p>
  </div>
  <div class="p-3.5 rounded-xl border border-emerald-500/40 bg-emerald-950/15">
    <div class="font-mono font-bold text-emerald-300 uppercase mb-1">Way 3 · Discovery</div>
    <p class="text-gray-300">Run phased diagnostic probes &rarr; ship verified <code>resources/gamma_pins.h</code> &amp; ISR blueprints.</p>
  </div>
  <div class="p-3.5 rounded-xl border border-purple-500/40 bg-purple-950/15">
    <div class="font-mono font-bold text-purple-300 uppercase mb-1">The Mashup</div>
    <p class="text-gray-300">Combine pinout truth (<code>SKILL.md</code>), firmware headers (<code>resources/</code>), and host CLI (<code>scripts/</code>).</p>
  </div>
</div>

<div class="grid grid-cols-2 gap-4 mt-5 text-xs">
  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800 flex items-center justify-between">
    <div>
      <div class="text-gray-400 uppercase font-mono text-[10px]">Presentation Deck &amp; Recording Scenarios</div>
      <div class="text-sm font-bold text-white font-mono mt-0.5">github.com/domesticmouse/skills-three-ways</div>
    </div>
    <span class="px-2 py-1 rounded bg-gray-800 text-cyan-300 font-mono">Slidev + Casts</span>
  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800 flex items-center justify-between">
    <div>
      <div class="text-gray-400 uppercase font-mono text-[10px]">Gamma Firmware, Phased Probes &amp; 7 Skills</div>
      <div class="text-sm font-bold text-white font-mono mt-0.5">github.com/domesticmouse/reverse-engineering-gamma</div>
    </div>
    <span class="px-2 py-1 rounded bg-gray-800 text-emerald-300 font-mono">C++ &amp; Skills</span>
  </div>
</div>

<!--
Thank you all so much! Whether you're teaching an agent a new library (Way 1), automating a tricky deployment workflow (Way 2), or reverse-engineering undocumented hardware (Way 3), Agent Skills turn one-off debugging sessions into permanent superpowers. Both repos are live on GitHub!
-->
