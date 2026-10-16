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

