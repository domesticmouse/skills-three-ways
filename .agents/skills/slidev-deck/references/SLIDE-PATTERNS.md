# Slide Patterns & Layout Reference

Copy-pasteable slide archetypes, layout frontmatter contracts, and Markdown/HTML formatting rules for Slidev decks.

---

## 1. Title Slide (`class: text-center`)

```markdown
---
class: text-center
---

<!-- S01 -->
<div class="h-full flex flex-col items-center justify-center">

  <h1 class="text-5xl font-extrabold tracking-tight text-white mb-3">
    Presentation Title
  </h1>
  <p class="text-2xl text-gray-300 font-light max-w-2xl">
    High-signal subtitle describing the core technical story
  </p>

  <div class="mt-10 text-gray-400 text-base">
    <span class="font-semibold text-gray-200">Speaker Name</span> &middot; Role, Organization
  </div>

  <div class="mt-10 text-xs text-gray-500">
    Press <kbd>Space</kbd> or <kbd>&rarr;</kbd> to advance
  </div>
</div>

<!--
Welcome everyone! Today we are exploring...
-->
```

---

## 2. Act / Section Divider (`layout: center`)

Use clean centered typography without "Act N" badges or pills:

```markdown
---
layout: center
class: text-center
---

<!-- S21 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Section Title
  </h1>
  <p class="text-xl font-mono text-cyan-300">
    key-artifact-one &middot; key-artifact-two
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    One-sentence summary of what this section accomplishes
  </p>
</div>

<!--
This brings us to our next section...
-->
```

---

## 3. Numbered Concept List (`layout: default`)

Preferred over multi-card grids or dense tables for 3–4 point conceptual explanations:

```markdown
---
layout: default
---

<!-- S22 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Slide Heading</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">First Concept or Step</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Primary high-signal mechanism or takeaway</li>
      <li>Supporting detail or concrete constraint</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Second Concept or Step</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Primary high-signal mechanism or takeaway</li>
      <li>Supporting detail or concrete constraint</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Third Concept or Step</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Primary high-signal mechanism or takeaway</li>
      <li>Supporting detail or concrete constraint</li>
    </ul>
  </li>
</ol>

<!--
Walk through the three steps in conversational prose...
-->
```

---

## 4. Anti-Pattern vs. Solution Split (`layout: default`)

Use a 2-column red/emerald comparison grid for contrasting a naive approach against the recommended architecture:

```markdown
---
layout: default
---

<!-- S03 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Problem vs. The Solution</h2>
</div>

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="p-5 rounded-xl bg-red-950/15 border border-red-500/30 space-y-3">
    <div class="text-xs font-mono text-red-400 uppercase">Anti-Pattern: Naive Approach</div>
    <h3 class="text-lg font-bold text-white">Why the Default Fails</h3>
    <ul class="text-xs text-gray-300 space-y-2 list-disc pl-4">
      <li>First failure mode</li>
      <li>Second failure mode</li>
      <li><strong>Result:</strong> Concrete negative outcome.</li>
    </ul>
  </div>

  <div class="p-5 rounded-xl bg-emerald-950/15 border border-emerald-500/30 space-y-3">
    <div class="text-xs font-mono text-emerald-400 uppercase">The Solution: Target Architecture</div>
    <h3 class="text-lg font-bold text-white">How We Solve It</h3>
    <ul class="text-xs text-gray-300 space-y-2 list-disc pl-4">
      <li>First architectural improvement</li>
      <li>Second architectural improvement</li>
      <li><strong>Result:</strong> Concrete positive outcome.</li>
    </ul>
  </div>
</div>

<!--
Contrast the anti-pattern on the left with the solution on the right...
-->
```

---

## 5. Full-Viewport Terminal Recording (`layout: cast-full`)

Renders an interactive `asciinema-player` filling 85–90% of the slide height:

```markdown
---
layout: cast-full
title: "Descriptive Action Title"
cast: /casts/recording-name.cast
autoPlay: false
speed: 2.0
idleTimeLimit: 1.0
fit: both
---

<!-- S05 -->
<!--
Click to play: explain what the viewer is watching in the terminal session and why the playback speed was chosen.
-->
```

---

## 6. Code / Architecture Zoom-In (`layout: skill-breakdown`)

Used for multi-slide deep-dives (`Zoom-In 1 of 3`, `Zoom-In 2 of 3`, etc.) with color-coded card borders (`way: 1` cyan, `way: 2` amber, `way: 3` emerald, `way: mashup` purple):

````markdown
---
layout: skill-breakdown
way: 1
skill: .agents/skills/example-skill/SKILL.md
title: Frontmatter & Activation Triggers
step: Zoom-In 1 of 3
---

<!-- S26 -->
<div class="space-y-4">

```yaml
---
name: example-skill
description: >-
  Concise trigger description.
---
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-cyan-300 font-semibold">Key Highlight 1:</span> Explanation of the first detail.
    </div>
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-cyan-300 font-semibold">Key Highlight 2:</span> Explanation of the second detail.
    </div>
  </div>
</div>

<!--
Zoom in on the first section of the artifact...
-->
````

> **Important Markdown Rule**: Notice how the ```` ```yaml ```` block above is flush at column 0 with blank lines above and below. Never indent fenced code blocks by 4+ spaces inside HTML `<div>` tags.

---

## 7. Hardware / Visual Callout (`layout: hardware-callout`)

Pairs a framed image and caption overlay on the left (6 columns) with rich HTML callouts in the default slot on the right (6 columns):

```markdown
---
layout: hardware-callout
title: Visual Callout Title
subtitle: Component or Subsystem Name
image: /images/example-photo.png
imageCaption: Concise caption describing the visual asset
---

<!-- S12 -->
<div class="space-y-4">
  <h3 class="text-lg font-bold text-emerald-300">Right-Column Headline</h3>
  <p class="text-sm text-gray-300 leading-relaxed">
    Contextual paragraph explaining what the viewer sees in the photo or diagram on the left.
  </p>
  <ul class="text-sm text-gray-300 space-y-2 list-disc pl-5">
    <li><strong>Feature A</strong>: Specific detail</li>
    <li><strong>Feature B</strong>: Specific detail</li>
  </ul>
</div>

<!--
Introduce the visual asset on the left and walk through its key specs on the right...
-->
```

---

## 8. Standalone Quote Slide (`layout: default`)

```markdown
---
layout: default
---

<!-- S01c -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Quote of the Day</h2>
</div>

<div class="h-80 flex flex-col items-center justify-center text-center px-8">
  <blockquote class="text-3xl font-semibold text-white tracking-tight leading-snug max-w-3xl">
    &ldquo;First line of the quote.<br/>
    Second line of the quote.&rdquo;
  </blockquote>
  <p class="mt-6 text-sm text-gray-400">
    &mdash; Attribution &middot; <a href="https://example.com" target="_blank" class="text-cyan-300 underline">Source Title</a>
  </p>
</div>

<!--
Share the context behind the quote and how it frames the talk...
-->
```

---

## 9. Concluding Links & Resources Slide (`layout: default`)

```markdown
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
      <a href="https://github.com/org/repo" target="_blank" class="text-cyan-300 hover:underline">github.com/org/repo</a>
    </div>
    <p class="text-xs text-gray-400 mt-1.5 m-0">
      One-line summary of what is in the repository
    </p>
  </div>
</div>

<!--
Thank the audience and highlight the links on screen...
-->
```
