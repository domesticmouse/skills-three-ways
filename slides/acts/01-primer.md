---
class: text-center
---

<!-- S1-01 -->
<div class="h-full flex flex-col items-center justify-center">

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
layout: center
class: text-center
---

<!-- S1-02 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Primer: What Are Agent Skills?
  </h1>
  <p class="text-lg text-gray-400 max-w-xl mx-auto">
    Why on-demand procedural runbooks beat stuffing everything into your system prompt
  </p>
</div>

<!--
Before we dive into our hardware story, let's do a quick primer on what Agent Skills actually are and why they exist.
-->

---
layout: default
---

<!-- S1-03 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Context Window Trap</h2>
</div>

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="p-5 rounded-xl bg-red-950/15 border border-red-500/30 space-y-3">
    <div class="text-xs font-mono text-red-400 uppercase">Anti-Pattern: Monolithic AGENTS.md</div>
    <h3 class="text-lg font-bold text-white">Stuffing Every Manual into Always-On Rules</h3>
    <ul class="text-xs text-gray-300 space-y-2 list-disc pl-4">
      <li>Dozens of MCP servers with hundreds of functions</li>
      <li>Massive monolithic <code>AGENTS.md</code> files</li>
      <li>Pasted PDF manuals and sprawling documentation</li>
      <li>Increased token consumption and competing instructions</li>
      <li><strong>Result:</strong> Degraded reasoning and lost focus.</li>
    </ul>
  </div>

  <div class="p-5 rounded-xl bg-emerald-950/15 border border-emerald-500/30 space-y-3">
    <div class="text-xs font-mono text-emerald-400 uppercase">The Solution: Progressive Disclosure</div>
    <h3 class="text-lg font-bold text-white">Modular, Self-Contained Skill Packages</h3>
    <ul class="text-xs text-gray-300 space-y-2 list-disc pl-4">
      <li>Keep <code>AGENTS.md</code> tiny—only universal project conventions</li>
      <li>Package domain-specific workflows into Agent Skills</li>
      <li>Agent sees only an invitation to invoke a capability</li>
      <li>Cheatsheets, runbooks, and scripts load <strong>when required</strong></li>
    </ul>
  </div>
</div>

<!--
Why not just load dozens of MCP servers, paste in PDF manuals, or stuff everything into AGENTS.md? Because always-on rules consume context on every single turn and dilute attention. Skills give us progressive disclosure.
-->

---
layout: default
---

<!-- S1-04 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">What Are Agent Skills?</h2>
</div>

<div class="h-80 flex flex-col items-center justify-center text-center">
  <p class="text-4xl font-semibold text-white tracking-tight">
    "I know, let's ask Antigravity!"
  </p>
</div>

<!--
Let's ask Antigravity directly in the terminal: "What are agent skills?" 
-->

---
layout: cast-full
title: "Asking Antigravity: What Are Agent Skills?"
cast: /casts/what-are-agent-skills.cast
autoPlay: true
speed: 1.75
idleTimeLimit: 1.0
fit: both
---

<!-- S1-05 -->
<!--
Here's AGY answering in Ghostty. Notice how it immediately checks its customization skill and breaks down the directory structure, frontmatter triggers, and progressive disclosure model.
-->


---
layout: default
---

<!-- S1-06 -->
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

<!-- S1-07 -->
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
Inside SKILL.md, the YAML frontmatter is critical. Because the agent only sees `name` and `description` in its initial system prompt, your `description` is the semantic router that determines whether the skill gets read.
-->

---
layout: default
---

<!-- S1-08 -->
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

<!-- S1-09 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">The 3-Tier Progressive Disclosure Model</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Tier 1 &middot; Discovery (~100 Tokens, Always Loaded)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>At session start, only <code>name</code> and <code>description</code> from each skill's YAML frontmatter are injected into the system prompt</li>
      <li>Acts as a lightweight semantic index without consuming working memory</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Tier 2 &middot; Activation (&lt; 5,000 Tokens, Loaded When Relevant)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>When the user's task matches a skill's description, the agent reads <code>SKILL.md</code> into working memory</li>
      <li>Provides the primary procedural workflow, negative constraints, and relative links</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Tier 3 &middot; Execution (On-Demand Files, Loaded Per Sub-Task)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>The agent selectively reads <code>references/*.md</code>, copies <code>resources/*.h</code>, or executes <code>scripts/*.py</code> only for required sub-steps</li>
      <li>Executable code runs in the terminal rather than bloating the prompt context</li>
    </ul>
  </li>
</ol>

<!--
This 3-tier progressive disclosure model is why we can have 40+ skills installed in a workspace without blowing up the context window: 100 tokens at Tier 1, SKILL.md at Tier 2, and deep reference files or scripts at Tier 3.
-->

---
layout: default
---

<!-- S1-10 -->
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

  <div class="col-span-5 p-5 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-center space-y-2">
    <div class="text-xs font-mono text-emerald-400 uppercase">Next Up</div>
    <div class="text-xl font-bold text-white">The Hardware Target</div>
    <p class="text-xs text-gray-400">
      Now let's apply this in practice: enter the <strong>Gamma Mini Synth</strong>, an uncharted hardware instrument on our desk.
    </p>
  </div>
</div>

<!--
Best of all, you don't have to hand-author every line of SKILL.md. Using the `agent-skills` and `agy-customizations` skills, you can have the agent itself package its research and scripts into a compliant skill directory. Now let's meet the mystery hardware we're going to tackle!
-->
