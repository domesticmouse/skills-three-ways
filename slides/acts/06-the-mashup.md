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

