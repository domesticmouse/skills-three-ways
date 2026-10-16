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

