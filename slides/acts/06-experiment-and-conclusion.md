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
Now for Act 6—the payoff! We have all seven skills in `.agents/skills/`. What happens when we give an agent the exact same prompt to build a 7-voice Drum Synth for the Gamma mini synth WITHOUT skills versus WITH skills?
-->

---
layout: default
---

<!-- S72 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Identical Prompt, Two Workspaces</h2>
</div>

<div class="p-4 rounded-xl bg-gray-900 border border-gray-700 mt-4">
  <div class="text-xs font-mono text-cyan-400 uppercase mb-1">Identical Prompt Given to Both Agents</div>
  <p class="font-mono text-sm text-white leading-relaxed m-0">
    "Write and build a complete C++ firmware for a 7-voice drum synth on the this.is.NOISE Gamma mini synth using libDaisy and DaisySP, mapping the drum voices to the front keys and filter controls to the knobs."
  </p>
</div>

<div class="grid grid-cols-2 gap-5 mt-5 text-xs">
  <div class="p-4 rounded-xl bg-red-950/15 border border-red-500/30">
    <div class="font-mono font-bold text-red-400 uppercase mb-1">Workspace A</div>
    <div class="text-base font-bold text-white mb-1">Without Skills</div>
    <p class="text-gray-400">
      Contains checkouts of <code>libDaisy/</code> and <code>DaisySP/</code>, plus <code>arm-none-eabi-gcc</code>—and <strong>zero skills</strong> in <code>.agents/skills/</code>.
    </p>
  </div>

  <div class="p-4 rounded-xl bg-emerald-950/15 border border-emerald-500/30">
    <div class="font-mono font-bold text-emerald-400 uppercase mb-1">Workspace B</div>
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
layout: cast-full
title: "Building the 7-Voice Drum Synth WITHOUT Skills"
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
layout: cast-full
title: "Building the 7-Voice Drum Synth WITH All 7 Skills"
cast: /casts/drum-synth-with-skills.cast
autoPlay: false
speed: 10.0
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
    <strong class="text-emerald-300 font-mono">gamma-usb-connectivity</strong>
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
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Wrapping Up
  </h1>
  <p class="text-xl text-cyan-300">
    Tools, Rules, and Skills in Harmony
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    Stepping back to see where Agent Skills fit alongside MCP and always-on rules
  </p>
</div>

<!--
With our drum synth built and the hardware experiment complete, let's step back and wrap up. How do Agent Skills fit into the broader agent ecosystem alongside tools like MCP and rules like AGENTS.md? Let's break down how they work together.
-->

---
layout: default
---

<!-- S79a -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Model Context Protocol</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Local &rarr; Remote</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Started as local desktop execution (stdio)</li>
      <li>Migrated to remote servers as teams moved to the cloud</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">MCP V2</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Simplified server-farm deployment</li>
      <li>Shifted from stateful sessions to stateless requests with routing headers</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Token Tax</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Context overhead scales at <span class="font-mono text-purple-300">Servers &times; Tools per Server</span></li>
      <li>Every schema must be declared upfront in tool definition</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">LLMs Can Now Code</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Server infrastructure got easier, but agent capability leaped forward</li>
      <li>Modern models can write scripts and execute CLI runbooks directly</li>
    </ul>
  </li>
</ol>

<!--
Now that we've seen all seven skills come together in the live demo, let's step back and summarize the architectural landscape.

MCP started as a clean way to connect local desktop clients to tools over stdio, then migrated to remote servers. Early on, that meant stateful connections and sticky sessions. MCP 2 addressed that head-on—going stateless and exposing methods in headers so server farms and API gateways can easily route calls.

However, that’s an infrastructure optimization. It doesn't solve the context window tax: you're still paying the schema cost for every tool across every server upfront. More importantly, it’s orthogonal to the biggest change in AI: LLMs can now write and execute code. If an agent can run a script or follow a runbook, we don't always need a heavyweight RPC server to get work done.
-->

---
layout: default
---

<!-- S79b -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Always-On Rules</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Constitution &amp; Guardrails</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Permanent project conventions and non-negotiable boundaries</li>
      <li>Sets core behavioral rules that the agent must never violate</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Paid on Every Turn</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Injected into prompt context on every single conversational turn</li>
      <li>Permanently consumes working memory regardless of task relevance</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Plain Markdown Only</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Static text instructions without bundled executable code</li>
      <li>Cannot package helper scripts, dependencies, or rich assets</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Repository Conventions</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>De facto root conventions (<code class="text-blue-300">AGENTS.md</code>, <code class="text-blue-300">CLAUDE.md</code>)</li>
      <li>Recognized across modern coding assistants for project-wide guidance</li>
    </ul>
  </li>
</ol>

<!--
Rules in files like AGENTS.md act as your project's constitution. They're essential for non-negotiable guardrails—things like code style, branch naming, or security constraints that the agent should never violate.

The catch is context cost: you pay for them on every single turn. Whether the agent is writing a complex feature or just fixing a typo, your entire rules file is sitting in the prompt. And because they're plain Markdown, they can't package runnable scripts, data files, or multi-step workflows. They set boundaries, but they don't teach deep procedures.
-->

---
layout: default
---

<!-- S79c -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Agent Skills</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Procedural Runbooks</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Specialized step-by-step procedures loaded on-demand</li>
      <li>Teaches the model how to solve specific domains without prompt bloat</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">3-Tier Progressive Disclosure</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Only metadata (~100 tokens) loaded into system context at startup</li>
      <li>Full <code>SKILL.md</code> runbook and <code>references/</code> pulled into context only on match</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Self-Contained Packages</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Directory bundling <code class="text-emerald-300">SKILL.md</code>, <code class="text-emerald-300">scripts/</code>, and <code class="text-emerald-300">references/</code></li>
      <li>Executable code runs directly in terminal instead of eating context tokens</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Open Standard</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Governed by the portable <span class="text-emerald-300 font-mono">agentskills.io</span> specification</li>
      <li>Shareable and cross-compatible across modern agent environments</li>
    </ul>
  </li>
</ol>

<!--
Agent Skills take a completely different approach: progressive disclosure and procedural runbooks. Instead of loading everything into memory upfront, the agent only sees a tiny 100-token summary during indexing.

When a task matches, the full SKILL.md is read into context. Crucially, a skill is a directory, not just a document. It bundles executable scripts, reference guides, and templates. Because modern LLMs can run code, a skill can execute complex workflows locally in a sandbox without needing an external RPC server or bloating the prompt with thousands of lines of documentation. And it's an open standard via agentskills.io.
-->

---
layout: default
---

<!-- S79d -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">The Laboratory Analogy</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">The Keycard: Model Context Protocol</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Unlocks the lab doors and powers up external instruments</li>
      <li>Gives the agent the raw capability and authorization to act</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">The Safety Placard: Always-On Rules</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Safety policies and guardrails posted permanently on the wall</li>
      <li>Non-negotiable boundaries the agent must never violate</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">The Procedure Manual: Agent Skills</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Standard operating procedures resting on the workbench</li>
      <li>Opened and followed step-by-step only when running a specific protocol</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Working in Harmony</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li><strong class="text-purple-300">Tools</strong> provide access &middot; <strong class="text-blue-300">Rules</strong> set boundaries &middot; <strong class="text-emerald-300">Skills</strong> teach the SOP</li>
      <li>Each mechanism solves a distinct challenge in agent architecture</li>
    </ul>
  </li>
</ol>

<!--
To pull these three concepts together, think of an agent entering a research laboratory.

MCP is the keycard: it unlocks the doors, turns on the power, and gives access to the lab instruments. AGENTS.md is the safety placard on the wall: the hard rules you read once and must never break, like wearing eye protection. And Agent Skills are the standard operating procedure manuals sitting on the bench: you don't memorize them all, you just open the centrifuge protocol when you need to spin down a sample.

Tools give access, Rules set boundaries, and Skills teach the actual procedure.
-->

---
layout: default
---

<!-- S80 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Links &amp; Resources</h2>
</div>

<div class="space-y-4 mt-6">
  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="flex items-center justify-between">
      <div class="text-xs font-mono text-cyan-400 uppercase tracking-wide">Presentation Deck</div>
      <span class="text-xs font-mono text-gray-500">github.com</span>
    </div>
    <div class="text-base font-bold font-mono mt-1">
      <a
        href="https://github.com/domesticmouse/skills-three-ways"
        target="_blank"
        class="text-cyan-300 hover:underline"
      >github.com/domesticmouse/skills-three-ways</a>
    </div>
    <p class="text-xs text-gray-400 mt-1.5 m-0">
      Slidev deck source, asciinema terminal recordings, and a fun use of Matt Pocock's <code>/wayfinder</code> skill
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="flex items-center justify-between">
      <div class="text-xs font-mono text-emerald-400 uppercase tracking-wide">Gamma Synth Repo</div>
      <span class="text-xs font-mono text-gray-500">github.com</span>
    </div>
    <div class="text-base font-bold font-mono mt-1">
      <a
        href="https://github.com/domesticmouse/reverse-engineering-gamma"
        target="_blank"
        class="text-emerald-300 hover:underline"
      >github.com/domesticmouse/reverse-engineering-gamma</a>
    </div>
    <p class="text-xs text-gray-400 mt-1.5 m-0">
      Multiple Gamma firmwares, hardware discovery plan, and all 7 custom skills
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="flex items-center justify-between">
      <div class="text-xs font-mono text-purple-400 uppercase tracking-wide">Technical Blog</div>
      <span class="text-xs font-mono text-gray-500">medium.com</span>
    </div>
    <div class="text-base font-bold font-mono mt-1">
      <a
        href="https://medium.com/@domesticmouse/"
        target="_blank"
        class="text-purple-300 hover:underline"
      >https://medium.com/@domesticmouse/</a>
    </div>
    <p class="text-xs text-gray-400 mt-1.5 m-0">
      Deep-dive writeups on reverse engineering the Gamma synth, AI coding agents, and random DevRel musings
    </p>
  </div>
</div>

<!--
Thank you all so much! All three resources are available online:
1. The presentation deck repository at github.com/domesticmouse/skills-three-ways includes the full Slidev source, all embedded asciinema recordings, and the skill definitions.
2. The Gamma synth companion repo at github.com/domesticmouse/reverse-engineering-gamma contains the C++ firmware, diagnostic probes, and all seven skills we built.
3. And you can follow my blog on Medium at medium.com/@domesticmouse for in-depth articles detailing the reverse-engineering journey and agent workflows.
-->
