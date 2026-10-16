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
Now for Act 7—the payoff! We have all seven skills in `.agents/skills/`. What happens when we give an agent the exact same prompt to build a 7-voice Drum Synth for the Gamma mini synth WITHOUT skills versus WITH skills?
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
To make this a fair scientific comparison, both runs receive the exact same one-sentence prompt and have local checkouts of `libDaisy/` and `DaisySP/`. The only difference is `.agents/skills/`.
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
title: "Recording 05: Building the 7-Voice Drum Synth WITHOUT Skills"
cast: /casts/drum-synth-without-skills.cast
autoPlay: false
speed: 3.0
idleTimeLimit: 1.0
fit: both
---

<!-- S74 -->
<!--
Click to play: watch the unskilled agent grep through `libDaisy` and `DaisySP`, guess sequential pins `D0` through `D6` for the keys and `A0` through `A3` for the knobs, omit `APP_TYPE = BOOT_SRAM`, and never enable the speaker amp.
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
Look at the post-mortem of Attempt 1: five fatal hardware bugs in code that compiled cleanly! Wrong `Makefile` target (SOS blink), muted speaker amp (`D32`), guessed key pins (`D0` is battery fault!), encoder pins wired as ADC knobs, and wrong OLED I2C address (`0x3C` vs `0x3D`).
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
title: "Recording 06: Building the 7-Voice Drum Synth WITH All 7 Skills"
cast: /casts/drum-synth-with-skills.cast
autoPlay: false
speed: 4.0
idleTimeLimit: 1.0
fit: both
---

<!-- S77 -->
<!--
Click to play: AGY reads our skills, copies `gamma_pins.h` and `gamma_usb.h` into the project, wires all 7 drum voices to `N1`–`N7` and presets to `C1`–`C7`, sets `APP_TYPE = BOOT_SRAM`, and builds a verified binary at `0x24000000`.
-->

---
layout: default
---

<!-- S78 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">How All 7 Skills Composed Together</h2>
</div>

<ol class="space-y-2.5 text-xs text-gray-200 list-decimal pl-6 mt-4 leading-relaxed">
  <li>
    <strong class="text-cyan-300 font-mono">libdaisy-guide</strong>
    <span class="text-gray-300"> &mdash; Configured 48 kHz SAI1 <code>AudioCallback</code>, <code>AdcChannelConfig</code>, and <code>OledDisplay</code> transport</span>
  </li>
  <li>
    <strong class="text-cyan-300 font-mono">daisysp-guide</strong>
    <span class="text-gray-300"> &mdash; Selected and initialized the 7 drum voices (<code>AnalogBassDrum</code> &le; 90 Hz, <code>AnalogSnareDrum</code>, <code>HiHat</code>, <code>Svf</code>)</span>
  </li>
  <li>
    <strong class="text-emerald-300 font-mono">gamma-pinout</strong>
    <span class="text-gray-300"> &mdash; Supplied drop-in <code>gamma_pins.h</code> (<code>D1</code>–<code>D7</code> keys, <code>D18/17/19/20</code> pots, <code>D32</code> speaker amp)</span>
  </li>
  <li>
    <strong class="text-emerald-300 font-mono">gamma-hardware-controls</strong>
    <span class="text-gray-300"> &mdash; Supplied 1 kHz <code>TIM5</code> key/encoder ISR, <code>1.0f - raw</code> pot inversion, and <code>I2C1</code> <code>0x3D</code> OLED reset</span>
  </li>
  <li>
    <strong class="text-purple-300 font-mono">gamma-usb-connectivity</strong>
    <span class="text-gray-300"> &mdash; Supplied <code>gamma_usb.h</code> on <code>FS_EXTERNAL</code> with non-blocking logging and <code>'b'</code> DFU reboot hook</span>
  </li>
  <li>
    <strong class="text-amber-300 font-mono">gamma-firmware-flash &amp; gamma-firmware-restore</strong>
    <span class="text-gray-300"> &mdash; Enforced <code>APP_TYPE = BOOT_SRAM</code> (<code>0x24000000</code>) and automated USB DFU flashing</span>
  </li>
</ol>

<div class="mt-4 p-3 rounded-lg bg-gray-900 border border-gray-800 text-center text-xs text-gray-300">
  No single mega-skill did this—<strong>focused, modular skills composed seamlessly</strong> at task time.
</div>

<!--
Notice how the skills composed: `libdaisy-guide` and `daisysp-guide` handled the DSP engine, `gamma-pinout` supplied `gamma_pins.h`, `gamma-hardware-controls` supplied the 1 kHz `TIM5` ISR and pot inversion, and `gamma-usb-connectivity` added non-blocking telemetry and soft-rebooting.
-->

---
layout: center
class: text-center
---

<!-- S79 -->
<div class="space-y-6">
  <h1 class="text-5xl font-extrabold text-white">
    Live Demo on the Gamma Mini Synth
  </h1>

  <ol class="space-y-3 text-sm text-gray-200 list-decimal pl-6 max-w-xl mx-auto text-left leading-relaxed">
    <li>
      <strong class="text-white">Factory Synth Baseline</strong> &mdash; Play the physical Gamma running stock <code>gamma-v2.0.3.bin</code> firmware
    </li>
    <li>
      <strong class="text-white">Flash Custom <code>drum_synth</code></strong> &mdash; Run <code>flash_firmware.py</code> via <code>gamma-firmware-flash</code> over USB-C
    </li>
    <li>
      <strong class="text-white">Play the 7 Drum Voices Live</strong> &mdash; Trigger Kick, Snare, Hats, Clap, and Tom on the keys &amp; sweep the filter knobs
    </li>
  </ol>
</div>

<!--
Now let's put the slides aside for a moment and do this live on the physical Gamma Mini Synth right here on stage! First I'll play the factory synth, then we'll run `flash_firmware.py` to flash the `drum_synth` binary we just built, and play the 7 drum voices live.
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

<ol class="space-y-3 text-xs text-gray-200 list-decimal pl-6 mt-3 leading-relaxed">
  <li>
    <strong class="text-white">Way 1 &middot; Library Review Skills</strong>
    <span class="text-gray-300"> &mdash; Audit C++ source repos once and package architecture &amp; memory rules into <code>SKILL.md</code> + <code>references/</code></span>
  </li>
  <li>
    <strong class="text-white">Way 2 &middot; DFU Operational Skills</strong>
    <span class="text-gray-300"> &mdash; Wrap fragile hardware timing races and binary validation into deterministic <code>scripts/*.py</code></span>
  </li>
  <li>
    <strong class="text-white">Way 3 &middot; Hardware Discovery Skills</strong>
    <span class="text-gray-300"> &mdash; Run phased diagnostic probes and ship verified <code>resources/gamma_pins.h</code> &amp; 1 kHz ISR blueprints</span>
  </li>
  <li>
    <strong class="text-white">The Mashup Skill</strong>
    <span class="text-gray-300"> &mdash; Combine pinout truth (<code>SKILL.md</code>), firmware headers (<code>resources/</code>), and host CLI (<code>scripts/</code>) in one package</span>
  </li>
</ol>

<div class="grid grid-cols-2 gap-4 mt-5 text-xs">
  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="text-gray-400 uppercase font-mono text-[10px]">Presentation Deck &amp; Recording Scenarios</div>
    <div class="text-sm font-bold text-cyan-300 font-mono mt-0.5">github.com/domesticmouse/skills-three-ways</div>
  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="text-gray-400 uppercase font-mono text-[10px]">Gamma Firmware, Phased Probes &amp; 7 Skills</div>
    <div class="text-sm font-bold text-emerald-300 font-mono mt-0.5">github.com/domesticmouse/reverse-engineering-gamma</div>
  </div>
</div>

<!--
Thank you all so much! Whether you're teaching an agent a new library (Way 1), automating a tricky deployment workflow (Way 2), or reverse-engineering undocumented hardware (Way 3), Agent Skills turn one-off debugging sessions into permanent superpowers. Both repos are live on GitHub!
-->

