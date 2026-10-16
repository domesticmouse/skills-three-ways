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

