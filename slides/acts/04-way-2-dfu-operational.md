---
layout: center
class: text-center
---

<!-- S35 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    DFU Operational Skills
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
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Interactive Troubleshooting &rarr; Script &rarr; Skill</h2>
</div>

<ol class="space-y-10 text-sm text-gray-200 list-decimal pl-6 mt-10 leading-relaxed">
  <li v-click>
    <strong class="text-white">Debug the Protocol Interactively</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Uncover USB VID/PIDs, bootloader combos, offsets, and exit codes</li>
      <li>Isolate where standard assumptions fail on real hardware</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Automate in a Deterministic Script</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Move timing loops and binary checks out of prose instructions</li>
      <li>Put polling and validation into a standalone Python utility</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Wrap in a Skill (<code>scripts/*.py</code> + <code>SKILL.md</code>)</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Package the utility inside <code>.agents/skills/&lt;name&gt;/scripts/</code></li>
      <li>Document when to run it and what exit codes to expect</li>
    </ul>
  </li>
</ol>

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
    <div v-click class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono text-amber-300 font-bold mb-1">Bootloader in Internal Flash (<code>0x08000000</code>)</div>
      <p class="text-gray-400">The STM32H750's 128 KB internal flash holds the permanent Electro-Smith second-stage bootloader.</p>
    </div>
    <div v-click class="p-3.5 rounded-xl bg-gray-900 border border-gray-800">
      <div class="font-mono text-amber-300 font-bold mb-1">App in QSPI Flash (<code>0x90040000</code>)</div>
      <p class="text-gray-400">User firmware binaries live in external 8 MB QSPI flash starting at offset <code>0x90040000</code>.</p>
    </div>
  </div>
</div>

<!--
When we plugged the Gamma in over USB-C and ran `dfu-util -l`, first contact showed the Electro-Smith Daisy Bootloader (`0483:df11`) exposing external QSPI flash at `0x90040000`—and we immediately ran into two bootloader traps and two build/flash constraints.
-->

---
layout: default
---

<!-- S38 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Trap #1: The Two Different Bootloaders</h2>
</div>

<div class="grid grid-cols-2 gap-6 mt-6">
  <div v-click class="p-5 rounded-xl bg-red-950/20 border border-red-500/30 space-y-2">
    <div class="text-xs font-mono text-red-400 uppercase">What Standard Docs Say</div>
    <h3 class="text-lg font-bold text-white">Hold BOOT + Tap RESET</h3>
    <p class="text-xs text-gray-300 leading-relaxed">
      Holding the physical <code>BOOT</code> button while tapping <code>RESET</code> drops the STM32H750 into the <strong>STM32 System ROM Bootloader</strong> (<code>@Internal Flash /0x08000000</code>).
    </p>
    <div class="p-2.5 rounded bg-red-950/50 border border-red-800/50 text-xs text-red-200 font-mono">
      Danger: Flashing <code>0x08000000</code> overwrites the Daisy Bootloader itself—and cannot write to QSPI <code>0x90040000</code>!
    </div>
  </div>

  <div v-click class="p-5 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
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
Trap #1: If you follow standard Daisy Seed instructions and hold BOOT while tapping RESET, you enter the raw STM32 ROM bootloader—which can't write to QSPI at `0x90040000` and risks overwriting the Daisy Bootloader! You have to tap RESET alone.
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

  <div class="space-y-4 text-sm">
    <div v-click class="px-5 py-4 rounded-xl bg-red-950/15 border border-red-500/30">
      <div class="font-bold text-red-300 mb-1.5">When the Agent Runs <code>dfu-util</code> Manually</div>
      <p class="text-gray-300 m-0">By the time you tap <code>RESET</code> and tell the agent "okay go", the 2.5-second window has already expired.</p>
    </div>
    <div v-click class="px-5 py-4 rounded-xl bg-emerald-950/15 border border-emerald-500/30">
      <div class="font-bold text-emerald-300 mb-1.5">When Wrapped in a 100ms Polling Script</div>
      <p class="text-gray-300 m-0">The script loops <code>dfu-util -l</code> every 100ms (or sends <code>'b'</code> over USB CDC) and flashes the instant <code>0483:df11</code> appears.</p>
    </div>
  </div>
</div>

<!--
Trap #2: When you tap RESET, the Daisy Bootloader only listens for DFU connections for 2.5 seconds! Trying to coordinate a human button press with an LLM tool call fails 90% of the time unless you wrap it in a 100ms polling script.
-->

---
layout: default
---

<!-- S42 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Safety First: <code>gamma-firmware-restore</code></h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-10 items-center">
  <div class="col-span-7 space-y-6">
    <p class="text-sm text-gray-200 leading-relaxed m-0">
      First we built our <strong>parachute</strong>: one command to restore factory <code>gamma-v2.0.3.bin</code> even from a hung MCU.
    </p>
    <ul class="text-sm text-gray-300 space-y-4 list-disc pl-5 leading-relaxed">
      <li>Caches <code>gamma-v2.0.3.bin</code> locally with fallback download</li>
      <li>Polls <code>dfu-util -l</code> every 100ms &mdash; one <code>RESET</code> tap restores in 4s</li>
      <li>Verifies USB re-enumeration (<code>"Gamma"</code>, <code>0483:5740</code>)</li>
    </ul>
  </div>

  <div v-click class="col-span-5 p-5 rounded-xl bg-amber-950/20 border border-amber-500/40 text-center space-y-2">
    <div class="text-xs font-mono text-amber-300 uppercase">Rule of Hardware Reverse Engineering</div>
    <div class="text-lg font-bold text-white">Never Probe Without an Automated Unbrick Script</div>
    <p class="text-xs text-gray-400">
      We triggered this restore skill dozens of times while debugging I2C locks and USB interrupts.
    </p>
  </div>
</div>

<!--
Before probing a single unknown pin, we built our parachute: `gamma-firmware-restore`. Whenever an experimental firmware hung the MCU, one command + one tap of RESET brought the synth back to factory condition in four seconds.
-->

---
layout: skill-breakdown
way: 2
skill: .agents/skills/gamma-firmware-restore/SKILL.md
title: "More Than a Script Wrapper: The Restore Runbook"
step: Zoom-In 1 of 4
---

<!-- S43a -->
<ol class="space-y-8 text-sm text-gray-200 list-decimal pl-6 mt-4 leading-relaxed">
  <li v-click>
    <strong class="text-white">Hardware &amp; Failure Mental Model</strong>
    <ul class="list-disc pl-5 mt-2.5 space-y-2 text-gray-300">
      <li>Bootloader map (<code>0x08000000</code> &rarr; <code>0x90040000</code>), 2.5s DFU window, and SOS blink</li>
      <li><strong>OLED GDDRAM retention:</strong> splash stays frozen on screen even when MCU is dead</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Three Tiered Recovery Procedures</strong>
    <ul class="list-disc pl-5 mt-2.5 space-y-2 text-gray-300">
      <li>Method 1: Automated <code>scripts/restore_firmware.py</code> + cached/hosted <code>gamma-v2.0.3.bin</code></li>
      <li>Fallbacks: Manual <code>dfu-util</code> CLI (with exit code <code>74</code> note) &amp; Web Updater &ldquo;Can't Enter Boot&rdquo;</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Post-Restore Verification</strong>
    <ul class="list-disc pl-5 mt-2.5 space-y-2 text-gray-300">
      <li>Runs <code>ioreg -p IOUSB</code> to verify <code>"Gamma"</code> (<code>0x0483</code> / <code>0x5740</code>) re-enumerates</li>
      <li>Confirms the live synthesizer UI returns on the OLED display</li>
    </ul>
  </li>
</ol>

<!--
First, look at `gamma-firmware-restore/SKILL.md`. It isn't just a thin wrapper around a Python script—it gives the agent the full operational mental model: the bootloader memory map, why the OLED stays frozen on the splash screen when the MCU halts due to GDDRAM retention, three tiered recovery paths including manual `dfu-util` and web updater fallbacks, and explicit `ioreg` verification checks to prove the synth actually came back to life.
-->

---
layout: skill-breakdown
way: 2
skill: .agents/skills/gamma-firmware-restore/scripts/restore_firmware.py
title: Deterministic 100ms DFU Polling Loop
step: Zoom-In 2 of 4
---

<!-- S43b -->
<div class="space-y-4 text-xs">

```python
OFFICIAL_BIN_URL = "https://gammaupdatetool.netlify.app/data/gamma-v2.0.3.bin"
QSPI_START_ADDRESS = "0x90040000"

# Poll every 100ms during the 2.5s grace window
while time.time() - start_time < timeout:
    res = subprocess.run(["dfu-util", "-l"], capture_output=True, text=True)
    if "0483:df11" in res.stdout:
        subprocess.run([
            "dfu-util", "-a", "0", "-s", f"{QSPI_START_ADDRESS}:leave", "-D", bin_path
        ])
```

  <div class="p-3.5 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-200 text-sm">
    <strong>Why a script:</strong> Downloading/caching <code>gamma-v2.0.3.bin</code> and polling at 100ms happens deterministically in Python—never in prose.
  </div>
</div>

<!--
Second, look inside `scripts/restore_firmware.py`. All the delicate timing and caching mechanics—downloading `gamma-v2.0.3.bin`, polling `dfu-util -l` every 100ms for `0483:df11`, and flashing to `0x90040000`—live inside deterministic Python code.
-->

---
layout: skill-breakdown
way: 2
skill: .agents/skills/gamma-firmware-flash/SKILL.md
title: "Guardrails: Negative Constraints & Benign Errors"
step: Zoom-In 3 of 4
---

<!-- S44 -->
<ol class="space-y-6 text-sm text-gray-200 list-decimal pl-6 mt-2 leading-relaxed">
  <li v-click>
    <strong class="text-white">Negative Constraint: <code>APP_TYPE = BOOT_SRAM</code> Only</strong>
    <ul class="list-disc pl-5 mt-2 space-y-1.5 text-gray-300">
      <li>Explicitly bans <code>BOOT_QSPI</code> and <code>BOOT_NONE</code> despite flashing into QSPI</li>
      <li>Prevents bootloader rejections and red SOS blink crashes up front</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Benign Failure Mode: <code>dfu-util</code> Exit Code <code>74</code></strong>
    <ul class="list-disc pl-5 mt-2 space-y-1.5 text-gray-300">
      <li>MCU reboots immediately on <code>:leave</code> before sending final USB status</li>
      <li>Stops agents from mistaking a successful flash for an error and looping</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Deadlock Trap: Ban <code>daisy::Logger&lt;LOGGER_EXTERNAL&gt;</code></strong>
    <ul class="list-disc pl-5 mt-2 space-y-1.5 text-gray-300">
      <li>Closing a serial monitor hangs <code>TransmitSync()</code> with notes stuck forever</li>
      <li>Routes the agent straight to our timeout-guarded non-blocking logger</li>
    </ul>
  </li>
</ol>

<!--
Now look at `gamma-firmware-flash/SKILL.md`. The biggest win in operational skills is documenting negative constraints and benign failure modes. First, explicitly telling the agent NOT to use `BOOT_QSPI` prevents SOS blink crashes even though we're flashing to QSPI. Second, noting that `dfu-util` exit code 74 on `:leave` is normal stops the agent from thinking the flash failed and entering an endless retry loop. And third, banning `daisy::Logger` prevents a nasty USB deadlock that hangs the synth with notes stuck playing forever.
-->

---
layout: skill-breakdown
way: 2
skill: .agents/skills/gamma-firmware-flash/scripts/flash_firmware.py
title: Binary Validation & Hands-Free Reboot
step: Zoom-In 4 of 4
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
And inside `scripts/flash_firmware.py`, we added two superpowers: first, it unpacks the binary's ARM vector table to verify the Reset Handler is in `0x24000000` AXI SRAM before flashing; second, if USB serial is active, it sends `'b'` to reboot the synth into DFU mode hands-free!
-->

---
layout: default
---

<!-- S46 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Problem #2 Solved: Non-Deterministic Prose Prompts</h2>
</div>

<ol class="space-y-10 text-sm text-gray-200 list-decimal pl-6 mt-10 leading-relaxed">
  <li v-click>
    <strong class="text-white">The Problem: Prose Fails on Fragile Operations</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Racing a 2.5s DFU window via sequential shell calls fails almost every time</li>
      <li>Benign quirks like <code>dfu-util</code> exit code <code>74</code> trigger endless retry loops</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">The Fix: Scripts &amp; Negative Constraints</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li><code>flash_firmware.py</code> and <code>restore_firmware.py</code> run 100ms polling &amp; vector checks</li>
      <li><code>SKILL.md</code> documents <code>BOOT_SRAM</code> and benign exit codes to stop guesswork</li>
    </ul>
  </li>
  <li v-click>
    <strong class="text-white">Repeatability Across Any Workflow</strong>
    <ul class="list-disc pl-5 mt-3 space-y-2.5 text-gray-300">
      <li>Hardware flashing, DB migrations, or releases become one-command execution</li>
      <li>Verified code handles the delicate steps instead of LLM improvisation</li>
    </ul>
  </li>
</ol>

<!--
That's Way 2: DFU Operational Skills—and this directly solves Problem #2 from the start of the talk: prose prompts are non-deterministic. When a workflow depends on tight timing windows, binary pre-flight checks, or quirky CLI exit codes, you don't want an LLM improvising shell commands from prose instructions. By wrapping tested Python scripts and explicit negative constraints inside the skill, we turn flaky operational chores into deterministic, one-command execution.
-->
