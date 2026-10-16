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

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Phased Plan: Bootstrap One Output Channel First</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>You can't probe 30 unknown pins blind without telemetry</li>
      <li>First find the OLED screen (<code>Phase 1 &amp; 2</code>) so the synth itself can display live GPIO and ADC readings</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Interactive Probing: Turn Knobs, Press Keys, Log Truth</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Flash diagnostic firmwares (<code>phase3_adc</code>, <code>phase4_keys_encoder</code>, <code>phase5_audio</code>)</li>
      <li>Record exact pin numbers, electrical polarities, and timing hazards</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Split Facts vs. Idioms: Modular Hardware Skills</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Package raw pinout truth + <code>gamma_pins.h</code> in <code>gamma-pinout</code></li>
      <li>Package C++ peripheral and USB driver architectures in <code>gamma-hardware-controls</code> and <code>gamma-usb-connectivity</code></li>
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
speed: 3.0
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

<ol class="space-y-2.5 text-xs text-gray-200 list-decimal pl-6 mt-4 leading-relaxed">
  <li>
    <strong class="text-white">Phase 0 &middot; Safety Net (Factory Backup &amp; DFU Restore)</strong>
    <ul class="list-disc pl-5 mt-0.5 space-y-0.5 text-gray-300">
      <li>Verify <code>gamma-v2.0.3.bin</code> restore and confirm <code>APP_TYPE = BOOT_SRAM</code> vector table entry</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Phase 1 &amp; 2 &middot; Visual Output (I2C Bus Scan &amp; OLED Bringup)</strong>
    <ul class="list-disc pl-5 mt-0.5 space-y-0.5 text-gray-300">
      <li>Scan <code>I2C1</code>, <code>I2C2</code>, <code>I2C4</code> across <code>0x08</code>–<code>0x77</code> to locate the 128&times;64 SSD1306 OLED screen</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Phase 3 &middot; Analog Controls (ADC1 Pots &amp; Thumbsticks)</strong>
    <ul class="list-disc pl-5 mt-0.5 space-y-0.5 text-gray-300">
      <li>Render live bar graphs for all 12 Daisy ADC pins on the OLED; turn each knob and stick axis one by one</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Phase 4 &middot; Digital Inputs (14 Keys &amp; Rotary Encoder)</strong>
    <ul class="list-disc pl-5 mt-0.5 space-y-0.5 text-gray-300">
      <li>Poll all remaining candidate GPIOs with internal pull-ups (<code>INPUT_PULLUP</code>) and display active-low pin indices on screen</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Phase 5 &middot; Audio &amp; Amp (PCM3060 Codec &amp; Speaker Enable)</strong>
    <ul class="list-disc pl-5 mt-0.5 space-y-0.5 text-gray-300">
      <li>Output a 440 Hz test tone via SAI1 and probe candidate output pins to unmute the internal speaker amplifier</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Phase 6 &middot; Synthesis (Distill into Skills &amp; Build Synths)</strong>
    <ul class="list-disc pl-5 mt-0.5 space-y-0.5 text-gray-300">
      <li>Freeze all discoveries into <code>gamma-pinout</code> and <code>gamma-hardware-controls</code>, then build full instruments</li>
    </ul>
  </li>
</ol>

<!--
Here is the 6-phase probing roadmap from `PLAN.md`. Notice how each phase builds on the last: Phase 0 secures recovery, Phase 1-2 unlocks the OLED screen, and Phases 3, 4, and 5 use the OLED screen to map every analog, digital, and audio pin.
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
With the OLED working, `phase3_adc` drew real-time bar graphs for all ADC channels on the screen. Turning each knob and moving each stick mapped all 4 pots (`D18`, `D17`, `D19`, `D20`) and all 4 joystick axes (`D22`, `D21`, `D24`, `D23`).
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
In Phase 4, we mapped all 14 tactile switches (`N1`–`N7` and `C1`–`C7`) plus the rotary encoder (`D15`, `D16`, `D28`). We also discovered that `oled.Update()` blocks for 9.5 ms over I2C—so encoder & key polling must run inside a 1 kHz `TIM5` timer interrupt!
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
In Phase 5, our 440 Hz test tone played on headphones, but the internal speaker was dead silent! Probing the remaining pins revealed that `seed::D32` (`PC3`) is an active-HIGH speaker amplifier enable pin. Driving `D32` HIGH brought the speaker to life.
-->

---
layout: default
---

<!-- S57 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Distilling Facts vs. Idioms: Three Modular Hardware Skills</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white"><code class="text-emerald-300">gamma-pinout</code> &middot; Declarative Hardware Truth</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Answers <strong>"What is connected where?"</strong> via a master 32-row pinout and polarity table</li>
      <li>Bundles a drop-in <code>resources/gamma_pins.h</code> C++ header with pure hardware constants</li>
    </ul>
  </li>
  <li>
    <strong class="text-white"><code class="text-emerald-300">gamma-hardware-controls</code> &middot; Front-Panel Driver Idioms</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Answers <strong>"How do I poll and render controls safely?"</strong> via a 1 kHz <code>TIM5</code> ISR Buxton Gray-code encoder state machine</li>
      <li>Provides lock-free key event queues, IIR deadband pot smoothing, and 5 deep subsystem guides in <code>references/*.md</code></li>
    </ul>
  </li>
  <li>
    <strong class="text-white"><code class="text-emerald-300">gamma-usb-connectivity</code> &middot; Non-Blocking USB CDC &amp; Reboot</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Answers <strong>"Why is <code>hw.StartLog()</code> silent?"</strong> (Gamma routes USB-C to <code>UsbHandle::FS_EXTERNAL</code> on <code>D29/D30</code>, not the Seed's internal port)</li>
      <li>Bundles <code>resources/gamma_usb.h</code> for deadlock-free telemetry and the hands-free <code>'b'</code> DFU soft-reboot command</li>
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
Zooming into `gamma-pinout/SKILL.md`: every single peripheral, Daisy Seed pin, STM32 port, ADC channel, and electrical polarity is documented in one authoritative table.
-->

---
layout: skill-breakdown
way: 3
skill: .agents/skills/gamma-pinout/resources/gamma_pins.h
title: Bundling resources/gamma_pins.h
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
Even better, `gamma-pinout` bundles `resources/gamma_pins.h` right inside the skill directory. The agent doesn't have to transcribe 30 pin numbers from markdown—it just copies `gamma_pins.h` into the project and `#include`s it.
-->

---
layout: skill-breakdown
way: 3
skill: .agents/skills/gamma-hardware-controls/SKILL.md
title: 1 kHz TIM5 ISR & Diagnostic Table
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
In `gamma-hardware-controls/SKILL.md`, we give the agent the 1 kHz `TIM5` hardware interrupt architecture so OLED updates never drop encoder clicks, plus a symptom-to-root-cause troubleshooting table.
-->

---
layout: skill-breakdown
way: 3
skill: .agents/skills/gamma-hardware-controls/references/
title: Progressive Disclosure via references
step: Zoom-In 4 of 4
---

<!-- S61 -->
<ol class="space-y-2.5 text-xs text-gray-200 list-decimal pl-6 leading-relaxed">
  <li>
    <strong class="text-emerald-300 font-mono">references/display.md</strong>
    <span class="text-gray-300"> &mdash; <code>I2C1</code> force-reset sequence, <code>I2C_1MHZ</code> config, and 30 Hz frame throttling</span>
  </li>
  <li>
    <strong class="text-emerald-300 font-mono">references/analog_inputs.md</strong>
    <span class="text-gray-300"> &mdash; 9-channel <code>AdcChannelConfig</code>, pot/joystick inversion, and soft-takeover / pickup logic</span>
  </li>
  <li>
    <strong class="text-emerald-300 font-mono">references/digital_keys.md</strong>
    <span class="text-gray-300"> &mdash; 14 active-low keys, 8ms shift-register debounce, and lock-free <code>KeyEvent</code> ring buffer</span>
  </li>
  <li>
    <strong class="text-emerald-300 font-mono">references/rotary_encoder.md</strong>
    <span class="text-gray-300"> &mdash; Buxton Gray-code state table eliminating mechanical contact bounce</span>
  </li>
  <li>
    <strong class="text-emerald-300 font-mono">references/main_loop_blueprint.md</strong>
    <span class="text-gray-300"> &mdash; Complete end-to-end C++ firmware skeleton combining all 4 subsystems</span>
  </li>
</ol>

<div class="mt-4 p-3 rounded-lg bg-gray-900/70 border border-gray-800 text-xs text-gray-300 text-center">
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
  <h2 class="text-2xl font-bold m-0">Takeaway: Hardware Discovery Skills</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Telemetry First</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>When reverse-engineering hardware with an agent, prioritize bringing up a visual or serial output channel in Phase 1</li>
      <li>Turns the device itself into a live logic analyzer for every subsequent phase</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Bundle Verified Code in <code>resources/</code></strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Don't just describe pin numbers in prose—ship a tested <code>gamma_pins.h</code> header in <code>resources/</code></li>
      <li>Eliminates pin transcription errors in future firmware builds</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Separate Declarative Truth from Driver Idioms</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Keeping <code>gamma-pinout</code> (facts) distinct from <code>gamma-hardware-controls</code> (ISR drivers) keeps both skills modular and easy to maintain</li>
    </ul>
  </li>
</ol>

<!--
That's Way 3: Hardware Discovery Skills. Turn ephemeral debugging sessions into permanent, verifiable hardware abstractions by bundling both declarative truth (`gamma_pins.h`) and real-time driver blueprints.
-->
