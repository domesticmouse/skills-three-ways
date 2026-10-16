---
theme: default
background: '#121317'
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## Skills Three Ways
  Presentation by Brett Morgan (Google Cloud DevRel)
drawings:
  persist: false
transition: slide-left
title: Skills Three Ways
mdc: true
---

# Skills Three Ways

Teaching Agents New Tricks via Agent Skills

<div class="pt-6 text-gray-400">
  Brett Morgan &middot; Developer Relations Engineer, Google Cloud
</div>

<div class="pt-12 text-sm text-gray-500">
  Press <kbd>Space</kbd> or <kbd>&rarr;</kbd> to navigate
</div>

---
layout: two-cols
---

# Proof of Concept

Interactive Terminal Replay in Slidev

- **Engine**: `asciinema-player` v3 (Rust + WebAssembly `vt-js`)
- **Integration**: Custom Vue 3 component (`AsciinemaPlayer.vue`)
- **Asset**: `what-are-agent-skills.cast` (202 KB)
- **Deployment**: Static build to GitHub Pages (`/skills-three-ways/`)

<br/>

The terminal on the right is an interactive recording, not a video: text can be selected, copied, and inspected.

::right::

<div class="h-100 flex items-center justify-center p-2">
  <AsciinemaPlayer
    src="/casts/what-are-agent-skills.cast"
    theme="dracula"
    :speed="1.2"
    :idleTimeLimit="1.5"
    :autoPlay="true"
    fit="width"
  />
</div>

---
layout: default
---

# Stack Validation

Architecture for the "Skills Three Ways" Presentation

| Dimension | Implementation | Validation |
| :--- | :--- | :--- |
| **Presentation Framework** | Slidev (Vue 3 + Vite) | Declarative Markdown + reactive Vue components |
| **Terminal Integration** | `AsciinemaPlayer.vue` | Dynamic client import (`onMounted`), zero SSR errors |
| **Asset Pipeline** | `slides/public/casts/` | Subpath auto-resolution via `BASE_URL` |
| **CI/CD** | GitHub Actions (`deploy-slides.yml`) | Automated build & deploy to GitHub Pages |

<div class="pt-8 text-center text-green-400 font-semibold">
  Ready for full slide narrative & recording scripts.
</div>
