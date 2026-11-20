---
layout: center
class: text-center
---

<!-- S47 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Hardware Discovery Skills
  </h1>
  <p class="text-xl font-mono text-emerald-300">
    gamma-pinout &middot; gamma-hardware-controls &middot; gamma-usb-connectivity
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    Executing a 6-phase diagnostic firmware plan to map every pin, bus, polarity, and ISR timer
  </p>
</div>

<!--
Now we had the C++ library skills (Way 1) and the DFU flash/restore skills (Way 2). It was time for Act 5 and Way 3: probing the physical hardware to create our three Hardware Discovery Skills.
-->

---
layout: default
---

<!-- S48 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Diagnostic Firmwares (<code>PLAN.md</code>) &rarr; Truth + Idioms</h2>
</div>

<ol class="space-y-10 text-sm text-gray-200 list-decimal pl-6 mt-10 leading-relaxed">
  <li v-click>
    <strong class="text-white">Bootstrap Telemetry First</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>You can't probe 30 unknown pins blind without an output channel</li>
      <li>Find the OLED screen first so the synth displays live GPIO &amp; ADC data</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Probe Interactively &amp; Log Truth</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Flash phased firmwares (<code>phase3_adc</code>, <code>phase4_keys_encoder</code>, <code>phase5_audio</code>)</li>
      <li>Record exact pins, inverted polarities, and timing hazards</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Split Facts vs. Driver Idioms</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Ship pinout truth + <code>gamma_pins.h</code> inside <code>gamma-pinout</code></li>
      <li>Isolate drivers in <code>gamma-hardware-controls</code> &amp; <code>gamma-usb-connectivity</code></li>
    </ul>
  </li>
</ol>

<!--
How do you reverse-engineer a board with no schematic? You design a phased sequence of diagnostic firmwares where Phase 1 finds the display, and every subsequent phase uses that display to turn physical actions into verified pin tables and driver skills.
-->

---
layout: cast-full
title: "Designing the 6-Phase Hardware Probing Plan (PLAN.md)"
cast: /casts/reverse-engineering-plan.cast
autoPlay: false
speed: 10.0
idleTimeLimit: 1.0
fit: both
---

<!-- S50 -->
<!--
Click to play: AGY reads `libdaisy-guide` to identify all candidate I2C, ADC, and GPIO pins on the Daisy Seed 2 DFM and structures the 6-phase `PLAN.md` diagnostic roadmap.
-->

---
layout: default
---

<!-- S51 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The 6-Phase Hardware Probing Roadmap (<code>PLAN.md</code>)</h2>
</div>

<ol class="space-y-7 text-base text-gray-200 list-decimal pl-6 mt-9 leading-relaxed">
  <li v-click>
    <strong class="text-white">Phase 0 &middot; Safety Net</strong> &mdash; Verify DFU restore &amp; <code>BOOT_SRAM</code>
  </li>
  <li v-click>
    <strong class="text-white">Phase 1 &amp; 2 &middot; OLED Display</strong> &mdash; Scan <code>I2C</code> buses to bring up SSD1306
  </li>
  <li v-click>
    <strong class="text-white">Phase 3 &middot; Analog Controls</strong> &mdash; Plot ADC bars to map pots &amp; sticks
  </li>
  <li v-click>
    <strong class="text-white">Phase 4 &middot; Digital Inputs</strong> &mdash; Poll <code>INPUT_PULLUP</code> for 14 keys &amp; encoder
  </li>
  <li v-click>
    <strong class="text-white">Phase 5 &middot; Audio &amp; Amp</strong> &mdash; Output 440 Hz &amp; find speaker amp pin
  </li>
  <li v-click>
    <strong class="text-white">Phase 6 &middot; Synthesis</strong> &mdash; Package into <code>gamma-pinout</code> &amp; driver skills
  </li>
</ol>

<!--
Here is the 6-phase probing roadmap from `PLAN.md`. Notice how each phase builds on the last: Phase 0 secures recovery, Phase 1-2 unlocks the OLED screen, and Phases 3, 4, and 5 use the OLED screen to map every analog, digital, and audio pin.
-->

---
layout: default
---

<!-- S52 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Phase 1 &amp; 2: Finding the OLED Screen</h2>
</div>

<ol class="space-y-10 text-sm text-gray-200 list-decimal pl-6 mt-10 leading-relaxed">
  <li v-click>
    <strong class="text-white">The Chicken-and-Egg Problem</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>No working USB serial and no working display yet</li>
      <li>How does <code>phase1_i2c_scan</code> report which bus and address answered?</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">The Bootstrap Trick</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Scan every <code>(Bus, Address)</code> pair across <code>I2C1</code>, <code>I2C2</code>, and <code>I2C4</code></li>
      <li>On ACK, immediately init SSD1306 there and draw the address onto the screen</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">The Discovery</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>OLED lit up on <code>I2C1</code> (<code>D11</code> SCL / <code>D12</code> SDA, 1 MHz) at address <code>0x3D</code></li>
      <li>Bonus trap: must call <code>__HAL_RCC_I2C1_FORCE_RESET()</code> on boot after soft-resets</li>
    </ul>
  </li>
</ol>

<!--
In Phase 1, how do you read I2C scan results without a screen or serial port? We had the scanner try initializing an SSD1306 driver on every I2C address that ACKed—and the OLED lit up immediately on `I2C1` (`D11`/`D12`) at address `0x3D`!
-->

---
layout: default
---

<!-- S53 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Phase 3 (<code>phase3_adc</code>): Mapping Knobs &amp; Thumbsticks</h2>
</div>

<div class="grid grid-cols-2 gap-5 mt-5 text-xs">
  <div v-click class="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-2">
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

  <div v-click class="p-4 rounded-xl bg-gray-900 border border-gray-800 space-y-2">
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
With the OLED working, `phase3_adc` drew real-time bar graphs for all ADC channels on the screen. Turning each knob and moving each stick mapped all 4 pots (`D18`, `D17`, `D19`, `D20`) and all 4 joystick axes (`D22`, `D21`, `D24`, `D23`).
-->

---
layout: default
---

<!-- S54 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Polarity Surprise: Inverted Pots &amp; Asymmetric Sticks!</h2>
</div>

<div class="grid grid-cols-2 gap-4 mt-3 text-xs">
  <div v-click class="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 space-y-1.5">
    <div class="font-mono font-bold text-amber-300 uppercase">Surprise 1: All 4 Knobs Inverted</div>
    <p class="text-gray-300 leading-relaxed m-0">
      Turning clockwise sweeps <code>3.3V &rarr; 0.0V</code> (<code>1.0f &rarr; 0.0f</code>). Without <code>1.0f - raw</code>, turning volume up turns sound down!
    </p>
  </div>
  <div v-click class="p-4 rounded-xl bg-purple-950/20 border border-purple-500/30 space-y-1.5">
    <div class="font-mono font-bold text-purple-300 uppercase">Surprise 2: 3 of 4 Stick Axes Inverted</div>
    <p class="text-gray-300 leading-relaxed m-0">
      <strong>Left X (<code>D22</code>)</strong> reads <code>0.0f &rarr; 1.0f</code>, while <strong>Right X (<code>D24</code>)</strong> is rotated on the PCB and reads <code>1.0f &rarr; 0.0f</code>!
    </p>
  </div>
</div>

<div v-click class="mt-4">

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
    <div v-click class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono text-emerald-300 font-bold mb-2">Left Keypad: 7 Note Keys (<code>N1</code>–<code>N7</code>)</div>
      <div class="grid grid-cols-4 gap-1.5 font-mono text-[11px]">
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-emerald-300 font-semibold">D1</span> <span class="text-gray-400">(PC11)</span></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-emerald-300 font-semibold">D2</span> <span class="text-gray-400">(PC10)</span></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-emerald-300 font-semibold">D3</span> <span class="text-gray-400">(PC9)</span></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-emerald-300 font-semibold">D4</span> <span class="text-gray-400">(PC8)</span></div>
        <div></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-emerald-300 font-semibold">D5</span> <span class="text-gray-400">(PD2)</span></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-emerald-300 font-semibold">D6</span> <span class="text-gray-400">(PC12)</span></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-emerald-300 font-semibold">D7</span> <span class="text-gray-400">(PG10)</span></div>
      </div>
    </div>
    <div v-click class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono text-cyan-300 font-bold mb-2">Right Keypad: 7 Chord Keys (<code>C1</code>–<code>C7</code>)</div>
      <div class="grid grid-cols-4 gap-1.5 font-mono text-[11px]">
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-cyan-300 font-semibold">D8</span> <span class="text-gray-400">(PG11)</span></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-cyan-300 font-semibold">D9</span> <span class="text-gray-400">(PB4)</span></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-cyan-300 font-semibold">D10</span> <span class="text-gray-400">(PB5)</span></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-cyan-300 font-semibold">D13</span> <span class="text-gray-400">(PB6)</span></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-cyan-300 font-semibold">D14</span> <span class="text-gray-400">(PB7)</span></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-cyan-300 font-semibold">D26</span> <span class="text-gray-400">(PD11)</span></div>
        <div class="px-1.5 py-1 rounded bg-gray-800/70 border border-gray-700/60 text-center whitespace-nowrap"><span class="text-cyan-300 font-semibold">D27</span> <span class="text-gray-400">(PG9)</span></div>
      </div>
    </div>
    <div v-click class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono text-amber-300 font-bold mb-1.5">Rotary Encoder + Push Switch</div>
      <div class="space-y-1 font-mono text-[11px]">
        <div><span class="inline-block w-16 text-gray-400">Phase A:</span> <span class="text-amber-300 font-semibold">D15</span> <span class="text-gray-400">(PC0)</span></div>
        <div><span class="inline-block w-16 text-gray-400">Phase B:</span> <span class="text-amber-300 font-semibold">D16</span> <span class="text-gray-400">(PA3)</span></div>
        <div><span class="inline-block w-16 text-gray-400">Click:</span> <span class="text-amber-300 font-semibold">D28</span> <span class="text-gray-400">(PA2)</span></div>
      </div>
    </div>
  </div>

  <div v-click class="col-span-5 p-6 rounded-xl bg-red-950/20 border border-red-500/30 space-y-5">
    <div class="font-mono text-red-400 uppercase">The Display Blocking Hazard</div>
    <div class="text-sm font-bold text-white">Why Main-Loop Encoder Polling Drops Clicks</div>
    <p class="text-gray-300 leading-relaxed m-0">
      <code>oled.Update()</code> blocks the main thread for <strong>~9.5 ms</strong> over I2C1. Quadrature encoder transitions last 1–3 ms!
    </p>
    <p class="text-emerald-300 font-semibold leading-relaxed pt-2 m-0">
      Solution: Sample the encoder and 14 keys inside a <strong>1 kHz <code>TIM5</code> hardware interrupt</strong>!
    </p>
  </div>
</div>

<!--
In Phase 4, we mapped all 14 tactile switches (`N1`–`N7` and `C1`–`C7`) plus the rotary encoder (`D15`, `D16`, `D28`). We also discovered that `oled.Update()` blocks for 9.5 ms over I2C—so encoder & key polling must run inside a 1 kHz `TIM5` timer interrupt!
-->

---
layout: default
---

<!-- S56 -->
<div class="flex items-center gap-3 mb-3">
  <h2 class="text-2xl font-bold m-0">Phase 5 (<code>phase5_audio</code>): The Hidden Speaker Amplifier Pin</h2>
</div>

<div class="grid grid-cols-12 gap-5 mt-3 items-center">
  <p class="col-span-6 text-sm text-gray-300 leading-relaxed m-0">
    When we started <code>AudioCallback</code> at 48 kHz, audio played through the 3.5mm headphone jack—but the Gamma's <strong>built-in speaker was completely silent</strong>!
  </p>
  <div v-click class="col-span-6 p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-1.5 text-xs">
    <div class="font-mono font-bold text-emerald-300">Discovery on <code>seed::D32</code> (<code>PC3</code>):</div>
    <p class="text-gray-300 leading-relaxed m-0">
      The internal Class-D speaker amplifier has an active-HIGH enable/unmute line wired to <code>seed::D32</code> (<code>PC3</code>)—a pin on the Daisy Seed 2 DFM bottom pads!
    </p>
  </div>
</div>

<div v-click class="mt-4">

```cpp
// Pop-Free Speaker Amp Initialization Sequence:
GPIO spk_en;

// 1. Pull LOW immediately on boot to prevent startup pop
spk_en.Init(gamma_pins::speaker_amp::pin_enable, GPIO::Mode::OUTPUT, GPIO::Pull::NOPULL);
spk_en.Write(false);

// 2. Start SAI1 PCM3060 48kHz audio engine
hw.StartAudio(AudioCallback);

// 3. Drive HIGH after audio callback is running
spk_en.Write(true);
```

</div>

<!--
In Phase 5, our 440 Hz test tone played on headphones, but the internal speaker was dead silent! Probing the remaining pins revealed that `seed::D32` (`PC3`) is an active-HIGH speaker amplifier enable pin. Driving `D32` HIGH brought the speaker to life.
-->

---
layout: default
---

<!-- S57 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Distilling Facts vs. Idioms: Three Modular Hardware Skills</h2>
</div>

<ol class="space-y-10 text-sm text-gray-200 list-decimal pl-6 mt-10 leading-relaxed">
  <li v-click>
    <strong class="text-white"><code class="text-emerald-300">gamma-pinout</code> &middot; Declarative Hardware Truth</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Answers <strong>"What is connected where?"</strong> in a master pinout &amp; polarity table</li>
      <li>Bundles drop-in <code>resources/gamma_pins.h</code> constants</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white"><code class="text-emerald-300">gamma-hardware-controls</code> &middot; Front-Panel Driver Idioms</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Answers <strong>"How do I poll controls safely?"</strong> via a 1 kHz <code>TIM5</code> ISR</li>
      <li>Adds lock-free key queues, pot smoothing, and 5 guides in <code>references/</code></li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white"><code class="text-emerald-300">gamma-usb-connectivity</code> &middot; Non-Blocking USB CDC &amp; Reboot</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Answers <strong>"Why is <code>hw.StartLog()</code> silent?"</strong> (USB-C routes to <code>FS_EXTERNAL</code>)</li>
      <li>Bundles <code>resources/gamma_usb.h</code> for safe logging &amp; <code>'b'</code> DFU reboot</li>
    </ul>
  </li>
</ol>

<!--
Once our hardware probing was complete, we split our findings into three focused skills: `gamma-pinout` for declarative pin truth (`gamma_pins.h`), `gamma-hardware-controls` for non-blocking front-panel drivers, and `gamma-usb-connectivity` (`gamma_usb.h`) after discovering the carrier board routes USB-C to `FS_EXTERNAL` pins rather than the Seed's onboard port. Let's zoom into `gamma-pinout` and `gamma-hardware-controls`.
-->

---
layout: skill-breakdown
way: 3
skill: .agents/skills/gamma-pinout/SKILL.md
title: Master Pinout & Polarity Table
---

<!-- S58 -->
<div class="space-y-4 text-xs">
  <p class="text-sm text-gray-300 m-0">
    <code>gamma-pinout</code> captures every verified peripheral, Daisy Seed pin, interface, and polarity in one authoritative table:
  </p>
  <table class="w-full text-left border-collapse">
    <thead>
      <tr class="border-b border-gray-700 text-gray-200">
        <th class="py-3 pr-3">Peripheral</th>
        <th class="py-3 px-3">Daisy Pins</th>
        <th class="py-3 px-3">Interface</th>
        <th class="py-3 pl-3">Polarity / Logic</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-800/80 text-gray-300">
      <tr>
        <td class="py-3 pr-3 font-semibold text-white whitespace-nowrap">OLED Display</td>
        <td class="py-3 px-3 font-mono text-emerald-300 whitespace-nowrap">D11, D12</td>
        <td class="py-3 px-3"><code>I2C1</code> @ <code>0x3D</code></td>
        <td class="py-3 pl-3">1 MHz Fast Mode Plus</td>
      </tr>
      <tr>
        <td class="py-3 pr-3 font-semibold text-white whitespace-nowrap">Top Pots (1–4)</td>
        <td class="py-3 px-3 font-mono text-emerald-300 whitespace-nowrap">D18, D17, D19, D20</td>
        <td class="py-3 px-3"><code>ADC1</code> (Ch 7, 5, 3, 11)</td>
        <td class="py-3 pl-3"><strong class="text-amber-300">Inverted</strong>: <code>1.0f - raw</code></td>
      </tr>
      <tr>
        <td class="py-3 pr-3 font-semibold text-white whitespace-nowrap">Left Stick (LX / LY)</td>
        <td class="py-3 px-3 font-mono text-emerald-300 whitespace-nowrap">D22, D21</td>
        <td class="py-3 px-3"><code>ADC1</code> (Ch 19, 4)</td>
        <td class="py-3 pl-3">LX normal &middot; LY <strong class="text-amber-300">inverted</strong></td>
      </tr>
      <tr>
        <td class="py-3 pr-3 font-semibold text-white whitespace-nowrap">Right Stick (RX / RY)</td>
        <td class="py-3 px-3 font-mono text-emerald-300 whitespace-nowrap">D24, D23</td>
        <td class="py-3 px-3"><code>ADC1</code> (Ch 17, 18)</td>
        <td class="py-3 pl-3">RX &amp; RY <strong class="text-amber-300">inverted</strong></td>
      </tr>
      <tr>
        <td class="py-3 pr-3 font-semibold text-white whitespace-nowrap">Keypads (N1–7, C1–7)</td>
        <td class="py-3 px-3 font-mono text-emerald-300 whitespace-nowrap">D1–10, D13–14, D26–27</td>
        <td class="py-3 px-3">GPIO In (<code>PULLUP</code>)</td>
        <td class="py-3 pl-3">Active LOW (<code>0</code> = pressed)</td>
      </tr>
      <tr>
        <td class="py-3 pr-3 font-semibold text-white whitespace-nowrap">Speaker Amp</td>
        <td class="py-3 px-3 font-mono text-emerald-300 whitespace-nowrap">D32 (PC3)</td>
        <td class="py-3 px-3">GPIO Out (Push-Pull)</td>
        <td class="py-3 pl-3">Active HIGH (<code>1</code> = on)</td>
      </tr>
    </tbody>
  </table>
</div>

<!--
Zooming into `gamma-pinout/SKILL.md`: every single peripheral, Daisy Seed pin, STM32 port, ADC channel, and electrical polarity is documented in one authoritative table.
-->

---
layout: skill-breakdown
way: 3
skill: .agents/skills/gamma-pinout/resources/gamma_pins.h
title: Bundling resources/gamma_pins.h
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
Even better, `gamma-pinout` bundles `resources/gamma_pins.h` right inside the skill directory. The agent doesn't have to transcribe 30 pin numbers from markdown—it just copies `gamma_pins.h` into the project and `#include`s it.
-->

---
layout: skill-breakdown
way: 3
skill: .agents/skills/gamma-hardware-controls/references/
title: Progressive Disclosure via references
---

<!-- S61 -->
<ol class="space-y-7 text-sm text-gray-200 list-decimal pl-6 mt-4 leading-relaxed">
  <li v-click>
    <strong class="text-emerald-300 font-mono">references/display.md</strong>
    <span class="text-gray-300"> &mdash; <code>I2C1</code> force-reset sequence, <code>I2C_1MHZ</code> config, and 30 Hz frame throttling</span>
  </li>
  <li v-click>
    <strong class="text-emerald-300 font-mono">references/analog_inputs.md</strong>
    <span class="text-gray-300"> &mdash; 9-channel <code>AdcChannelConfig</code>, pot/joystick inversion, and soft-takeover / pickup</span>
  </li>
  <li v-click>
    <strong class="text-emerald-300 font-mono">references/digital_keys.md</strong>
    <span class="text-gray-300"> &mdash; 14 active-low keys, 8ms shift-register debounce, and lock-free ring buffer</span>
  </li>
  <li v-click>
    <strong class="text-emerald-300 font-mono">references/rotary_encoder.md</strong>
    <span class="text-gray-300"> &mdash; Buxton Gray-code state table eliminating mechanical contact bounce</span>
  </li>
  <li v-click>
    <strong class="text-emerald-300 font-mono">references/main_loop_blueprint.md</strong>
    <span class="text-gray-300"> &mdash; Complete end-to-end C++ firmware skeleton combining everything</span>
  </li>
</ol>

<div v-click class="mt-9 p-4 rounded-lg bg-gray-900/70 border border-gray-800 text-sm text-gray-300 text-center">
  <code>SKILL.md</code> stays a crisp 91-line index; the agent reads only the specific <code>references/*.md</code> file it needs.
</div>

<!--
Look at how `gamma-hardware-controls` uses Tier-3 `references/`: `SKILL.md` is only 91 lines long, pointing to five deep reference files—`display.md`, `analog_inputs.md`, `digital_keys.md`, `rotary_encoder.md`, and `main_loop_blueprint.md`.
-->

---
layout: default
---

<!-- S62 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Takeaway: Solving Problem #3 (&ldquo;Groundhog Day&rdquo; Debugging)</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li v-click>
    <strong class="text-white">The Problem We Started With: Ephemeral Chat Breakthroughs</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Normally, spending hours probing unknown GPIO pins, inverted pot polarities, and I2C blocking hazards lives only inside that one chat transcript</li>
      <li>Close the terminal window and that hard-won system context vanishes &mdash; forcing the next session right back to square one</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">How Discovery Skills Solve It: Freeze Truth into Code &amp; Runbooks</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Shipping verified <code>resources/gamma_pins.h</code> and <code>resources/gamma_usb.h</code> headers inside the skills turns ephemeral discoveries into drop-in C++ code</li>
      <li>Separating declarative pin truth (<code>gamma-pinout</code>) from 1 kHz <code>TIM5</code> ISR driver blueprints (<code>gamma-hardware-controls</code>) keeps institutional memory modular</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Compounding Engineering Intelligence</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Every solved mystery or reverse-engineered subsystem becomes a permanent upgrade to the workspace &mdash; so the agent gets smarter after every hard problem you solve together</li>
    </ul>
  </li>
</ol>

<!--
And that's Way 3: Hardware Discovery Skills—which solves Problem #3 from the start of our talk: Groundhog Day debugging sessions. In a typical agent workflow, all those hours we spent discovering inverted potentiometers, the hidden `D32` speaker amp pin, and the 9.5 ms OLED I2C blocking hazard would have died the moment we closed the chat tab. By freezing our discoveries into drop-in C++ headers and modular driver skills, every hard problem you solve permanently upgrades your agent for the next task.
-->
