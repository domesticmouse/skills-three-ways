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
layout: default
---

<!-- S1-01b -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">About Me: Brett Morgan</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">16 Years in Developer Relations at Google</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>From Sydney &mdash; though I lived right here in Brisbane for a couple of years during the awkward years.</li>
      <li>Supported <strong>Blogger</strong>, <strong>Google+</strong>, <strong>Google Maps</strong>, <strong>Flutter</strong>, and now <strong>Google Antigravity</strong></li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Down the Synthesizer &amp; Electronics Rabbit Hole</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Picked up electronics as a hobby a couple of years ago after watching videos on Eurorack synthesizers</li>
      <li>It quickly snowballed from building modules into reverse-engineering hardware</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">How Agents Re-Shape User Interfaces</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Exploring how LLMs and Antigravity re-shape the definition of &mdash; and requirement for &mdash; user interfaces</li>
    </ul>
  </li>
</ol>

<!--
Before we jump in, a quick bit about me. I'm Brett Morgan, and I've been a Developer Relations Engineer at Google for 16 years. I'm from Sydney, though I actually lived right here in Brisbane for a couple of years during the awkward years! Over my time at Google I've supported Blogger, Google+, Google Maps, Flutter, and now Antigravity.

Why am I talking about hardware synthesizers today? A couple of years ago I picked up electronics as a hobby after falling down a YouTube rabbit hole on Eurorack synthesizers, and it has snowballed from there.

Coming from Flutter to Antigravity, I'm deeply interested in how LLMs and agents re-shape the definition of—and even the requirement for—user interfaces.
-->

---
layout: default
---

<!-- S1-01c -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Quote of the Day</h2>
</div>


<div class="h-80 flex flex-col items-center justify-center text-center px-8">
  <blockquote class="text-3xl font-semibold text-white tracking-tight leading-snug max-w-3xl">
    &ldquo;Don&rsquo;t ask &lsquo;How do we add AI to this?&rsquo;<br/>
    Ask &lsquo;What is the agent-first version of this?&rsquo;&rdquo;
  </blockquote>
  <p class="mt-6 text-sm text-gray-400">
    &mdash; From PostHog's newsletter <a href="https://posthog.com/newsletter/building-ai-products" target="_blank" class="text-cyan-300 underline">38 things we've learned about building AI products</a>
  </p>
</div>

<!--
There's a great line from the folks at PostHog that captures how I think about this shift: "Don't ask 'how do we add AI to this?' Ask 'what is the agent-first version of this?'"

Today, we're going to ask what the agent-first version of hardware bring-up, reverse engineering, and documentation looks like.
-->

---
layout: default
---

<!-- S1-01d -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Today&rsquo;s Itinerary</h2>
</div>

<ol class="space-y-3.5 text-sm text-gray-200 list-decimal pl-6 mt-4 leading-relaxed">
  <li>
    <strong class="text-white">What Are Agent Skills?</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Monolithic system prompts &rarr; 3-tier progressive disclosure</li>
      <li>Using Google Antigravity's inbuilt skills for fun and profit</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Two Synths &amp; Zero Schematics</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>How a late-night impulse purchases lead to developer talks</li>
      <li>Figuring out firmware without documentation</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Teaching the Agent Step by Step</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Building cheatsheets from libraries</li>
      <li>Making processes repeatable with code</li>
      <li>Planning out experiments to working hardware</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Without Skills vs. With Skills</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Same prompt, how different are the results?</li>
    </ul>
  </li>
</ol>

<!--
Here's our itinerary for today.

First, we'll do a quick primer on Agent Skills—why stuffing every manual into a monolithic system prompt fails, how 3-tier progressive disclosure keeps context clean, and how we use meta-skills so the agent actually writes the skills for us.

Second, I'll introduce the hardware mystery at the center of this talk: how a late-night ordering accident gave me a spare Gamma Mini Synth to open up, revealing an Electro-Smith Daisy Seed 2 DFM inside, but with closed-source firmware and zero wiring schematics.

Third is the core of the talk—Skills Three Ways:
- Way 1 is Library Review Skills, where we distill 50,000 lines of C++ audio library source code into architectural runbooks.
- Way 2 is DFU Operational Skills, where we turn fragile USB bootloader button-press races into deterministic flash and factory-restore scripts.
- Way 3 is Hardware Discovery Skills, where we run a 6-phase diagnostic firmware campaign to map every button, knob, joystick, and OLED pin on the board.

Finally, we'll put all seven skills to the test in a head-to-head experiment: giving two clean workspaces the exact same prompt to build a 7-voice drum synthesizer—one without skills, and one with skills—and seeing what happens.
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
speed: 2.0
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
.agents/skills/code-reviewer/
├── SKILL.md          # Required: YAML frontmatter + core runbook
├── scripts/          # Optional: Helper scripts & CLI utilities
│   └── run_linter.py
├── references/       # Optional: In-depth documentation & API specs
│   └── style_guide.md
└── resources/        # Optional: Drop-in templates & sample assets
    └── report_template.md
```

  </div>

  <div class="col-span-6 space-y-3 text-xs">
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-cyan-300">SKILL.md (Required)</div>
      <p class="text-gray-400 mt-1">Single entry point kept concise (&lt;500 lines). Contains activation metadata and primary procedural workflow.</p>
    </div>
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-amber-300">scripts/ (Executable Utilities)</div>
      <p class="text-gray-400 mt-1">Deterministic tools so the agent runs tested commands instead of ad hoc on-the-fly solutions.</p>
    </div>
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-emerald-300">references/ &amp; resources/ (Deep Context)</div>
      <p class="text-gray-400 mt-1">In-depth API specs, reference manuals, and template assets loaded on-demand only when a sub-step requires them.</p>
    </div>
  </div>
</div>

<!--
As Antigravity showed in the recording, a skill isn't just a loose markdown file—it is a self-contained directory package. SKILL.md acts as the primary runbook, while optional directories hold executable scripts, in-depth documentation, and reusable templates.
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
name: code-reviewer
description: >-
  Reviews code changes for bugs, security vulnerabilities, and style violations.
  Use when reviewing pull requests or checking code quality.
---
```

</div>

<div class="grid grid-cols-2 gap-4 mt-5 text-xs">
  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="font-mono font-bold text-white mb-1"><code>name</code> (Identifier Constraint)</div>
    <p class="text-gray-400 leading-relaxed">
      A unique, lowercase, hyphenated identifier that <strong>must match the parent directory name</strong>.
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="font-mono font-bold text-cyan-300 mb-1"><code>description</code> (The Routing Trigger)</div>
    <p class="text-gray-400 leading-relaxed">
      The <strong>primary activation trigger</strong> loaded at startup. The agent matches user prompts against this text to decide whether to load the full skill.
    </p>
  </div>
</div>

<!--
The YAML frontmatter provides the skill's identity and activation trigger. Because only name and description are loaded into context at session startup, the description must clearly specify domain keywords and explicit "Use when..." conditions.
-->

---
layout: default
---

<!-- S1-08 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Inside SKILL.md Part 2: The Important Stuff</h2>
</div>

<div class="grid grid-cols-2 gap-5 mt-6">
  <div class="p-5 rounded-xl bg-gray-900 border border-gray-800 space-y-3">
    <div class="text-xs font-mono text-cyan-300 uppercase">1. Runbook Procedures</div>
    <p class="text-xs text-gray-300 leading-relaxed">
      Step-by-step operational workflows, domain rules, and verification criteria the agent follows from start to finish:
    </p>

```markdown
## Review Workflow
1. Run the static analysis script on changed files.
2. Check changes against the project style guide.
3. Summarize findings using the report template.
```

  </div>

  <div class="p-5 rounded-xl bg-gray-900 border border-gray-800 space-y-3">
    <div class="text-xs font-mono text-emerald-300 uppercase">2. Pointers to Scripts &amp; References</div>
    <p class="text-xs text-gray-300 leading-relaxed">
      Relative links to executable utilities and deep reference documentation housed inside the skill directory:
    </p>

```markdown
## Bundled Resources
* Linter script:
  [`scripts/run_linter.py`](scripts/run_linter.py)
* Style guide:
  [`references/style_guide.md`](references/style_guide.md)
```

  </div>
</div>

<!--
Once triggered, the markdown body of SKILL.md acts as the agent's operational runbook. It contains the key step-by-step procedures for the task alongside direct relative pointers to additional resources housed within the skill—like helper scripts in `scripts/` and deep documentation in `references/`.
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
      <li>At session start, only <code>name</code> and <code>description</code> from each skill's YAML frontmatter are injected</li>
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
      <li>The agent selectively reads <code>references/*.md</code>, uses templates in <code>resources/</code>, or executes <code>scripts/*.py</code></li>
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
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Authoring Skills with Agent Skills</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Phase 1 &middot; Exploration &amp; Problem Solving (Do the Work First)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Solve an unfamiliar task, research an API, or reverse-engineer hardware interactively in the workspace</li>
      <li>Iterate until commands, scripts, and edge-case fixes are thoroughly tested and proven</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Phase 2 &middot; Synthesis with Meta-Skills (<code>/agy-customizations</code>)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Prompt the agent: <code>"/agy-customize Please convert this into an agent skill"</code></li>
      <li>The agent structures <code>SKILL.md</code>, formats YAML frontmatter, and isolates deep context into <code>scripts/</code> or <code>references/</code></li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Phase 3 &middot; Verification from Cold Storage (Test in a Clean Session)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Start a brand-new conversation with an empty context window to simulate a real user prompt</li>
      <li>Verify that semantic routing activates Tier 1 and the agent executes Tier 2 and 3 without human intervention</li>
    </ul>
  </li>
</ol>

<div class="mt-6 p-3.5 rounded-lg bg-gray-900/40 border border-gray-800/80 text-center text-sm text-gray-300">
  You don't need to write the skill <strong>by hand</strong>!
</div>

<!--
Best of all, you don't have to hand-author every line of SKILL.md. We use two built-in meta-skills—`agent-skills` for standard directory anatomy and YAML frontmatter, and `agy-customizations` for Antigravity-specific rules and discovery roots. The workflow is simple: first, solve the problem interactively in the terminal; second, tell the agent to package the working session into a skill; third, verify it in a brand-new conversation to prove it works from cold storage. Now let's meet the mystery hardware we're going to tackle!
-->
