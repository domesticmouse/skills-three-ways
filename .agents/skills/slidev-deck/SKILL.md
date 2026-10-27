---
name: slidev-deck
description: Scaffold, author, style, preview, and deploy dark-theme Slidev presentation decks with modular act files, custom Vue layouts, and embedded asciinema terminal recordings. Use when creating a new Slidev deck, authoring or refactoring slides and presenter notes, embedding .cast recordings or visual callouts, running or managing the local Slidev dev server, or configuring GitHub Pages deployment.
compatibility: Requires Node.js (v18+) and npm; integrates with Slidev (@slidev/cli) and asciinema-player v3
---

# Slidev Deck

Procedural runbook, reusable Vue components/layouts, and server tooling for building high-signal technical slide decks with [Slidev](https://sli.dev/) (`slides/`), embedded `asciinema-player` terminal recordings, dark-mode typography, and static GitHub Pages deployment.

Works alongside `/asciinema` (recording, sanitizing, and trimming `.cast` files) and `/crop-image` (trimming transparent margins and solid borders on slide images).

## Workflows

Choose the matching workflow based on your objective:

1. [Scaffold a New Slidev Deck](#1-scaffold-a-new-slidev-deck)
2. [Structure Modular Acts](#2-structure-modular-acts)
3. [Author Slides, Layouts & Presenter Notes](#3-author-slides-layouts--presenter-notes)
4. [Embed Terminal Recordings & Visual Assets](#4-embed-terminal-recordings--visual-assets)
5. [Run & Manage the Local Dev Server](#5-run--manage-the-local-dev-server)
6. [Verify Build & Deploy to GitHub Pages](#6-verify-build--deploy-to-github-pages)

---

### 1. Scaffold a New Slidev Deck

Initialize a new `slides/` workspace from the bundled templates in [`resources/`](resources/):

1. Create the directory hierarchy and copy the starter configuration, theme stylesheet, component, and custom layouts:
   ```bash
   mkdir -p slides/{acts,components,layouts,public/casts,public/images}
   cp .agents/skills/slidev-deck/resources/package.json slides/package.json
   cp .agents/skills/slidev-deck/resources/vite.config.ts slides/vite.config.ts
   cp .agents/skills/slidev-deck/resources/style.css slides/style.css
   cp .agents/skills/slidev-deck/resources/slides.md slides/slides.md
   cp .agents/skills/slidev-deck/resources/components/AsciinemaPlayer.vue slides/components/AsciinemaPlayer.vue
   cp .agents/skills/slidev-deck/resources/layouts/*.vue slides/layouts/
   ```
2. Update the `--base /<repo-name>/` flag in `slides/package.json` (`"build": "slidev build --base /<repo-name>/"`) to match the repository name for GitHub Pages subpath hosting (or omit `--base` if deploying to a custom root domain).
3. Add `slides/node_modules/`, `slides/dist/`, `slides/.slidev.pid`, and `slides/.slidev.log` to `.gitignore`.
4. Install dependencies:
   ```bash
   npm --prefix slides install
   ```
5. *Completion Criterion*: `slides/node_modules/` is populated and `npm --prefix slides run build` exits with code 0.

---

### 2. Structure Modular Acts

Split multi-part presentations into Act-level markdown files under `slides/acts/` while keeping `slides/slides.md` as the master manifest:

1. Configure `slides/slides.md` with global presentation headmatter (`colorSchema: dark`, `background: '#121317'`, `highlighter: shiki`, `mdc: true`) and set `hide: true` on the headmatter block so Slidev does not insert a blank initial slide or leak headmatter fields into the first act:
   ```yaml
   ---
   theme: default
   background: '#121317'
   colorSchema: dark
   highlighter: shiki
   lineNumbers: false
   info: |
     ## Presentation Title
     Subtitle and Presenter Info
   drawings:
     persist: false
   transition: slide-left
   title: Presentation Title
   mdc: true
   hide: true
   ---

   ---
   src: ./acts/01-primer.md
   ---

   ---
   src: ./acts/02-core-story.md
   ---
   ```
2. Name act files sequentially (`01-primer.md`, `02-the-hook.md`, etc.) inside `slides/acts/`.
3. Tag every slide with a unique comment identifier immediately after its frontmatter block (e.g., `<!-- S01 -->`, `<!-- S12 -->`) to anchor edits and reviews.
4. *Completion Criterion*: `slides/slides.md` contains `hide: true` in its headmatter block and every `src: ./acts/...` entry resolves to a valid markdown file in `slides/acts/`.

---

### 3. Author Slides, Layouts & Presenter Notes

Follow the slide design conventions below. For copy-pasteable HTML/Markdown templates of every slide archetype, read [`references/SLIDE-PATTERNS.md`](references/SLIDE-PATTERNS.md).

#### Core Formatting Conventions:
1. **Clean Slide Headings**: Render slide titles using a clean flex header container without badges, pills, or Act chips:
   ```html
   <div class="flex items-center gap-3 mb-6">
     <h2 class="text-2xl font-bold m-0">Slide Title</h2>
   </div>
   ```
2. **Numbered Concept Lists**: Present multi-point explanations and comparisons as structured numbered lists (`<ol>`) with bold white titles and nested `<ul>` takeaways rather than cramped multi-card grids or dense multi-column tables:
   ```html
   <ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
     <li>
       <strong class="text-white">Topic / Feature Title</strong>
       <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
         <li>Primary high-signal takeaway or mechanism</li>
         <li>Secondary context or contrast</li>
       </ul>
     </li>
   </ol>
   ```
   When comparing 3–4 broad paradigms (e.g., MCP vs. Rules vs. Skills), give each concept its own focused numbered-list slide followed by a synthesis slide rather than squeezing all columns into one tiny table.
3. **Flush Code Fences Inside HTML**: Place markdown fenced code blocks (` ``` `) flush at column 0 with blank lines above and below whenever they sit inside HTML `<div>` wrappers. Indenting a fenced code block by 4+ spaces inside HTML causes Markdown to render raw tags instead of highlighted code.
4. **Conversational Presenter Notes**: Conclude every slide with an HTML comment (`<!-- ... -->`) containing natural spoken narrative that explains the transition and talking points behind each bullet. Write pure spoken prose without bracketed stage directions (`[Click]`, `[Next slide]`).

#### Choosing a Slide Layout:
- **`layout: center` (`class: text-center`)**: Title slide, Act divider slides, and big-quote callouts.
- **`layout: default`**: Concept lists, 2-column anti-pattern vs. solution cards (`bg-red-950/15` vs. `bg-emerald-950/15`), and code/architecture tables.
- **`layout: cast-full`**: Full-viewport (85–90% height) interactive `asciinema-player` slide (`title`, `cast: /casts/file.cast`, `autoPlay: false`, `speed: 2.0`, `idleTimeLimit: 1.0`, `fit: both`).
- **`layout: skill-breakdown`**: Framed zoom-in card with top-right monospace metadata (`way: 1|2|3|mashup`, `skill: path/to/file`, `title`, `step: Zoom-In 1 of 3`).
- **`layout: hardware-callout`**: 12-column split pairing a framed image and optional caption overlay on the left (`title`, `subtitle`, `image: /images/file.png`, `imageCaption`) with explanatory HTML content in the default slot on the right.

*Completion Criterion*: Every authored slide includes a clean `<h2>` header (or uses a dedicated layout header), unindented code fences with blank line separators, and a conversational `<!-- ... -->` speaker note block.

---

### 4. Embed Terminal Recordings & Visual Assets

Consult [`references/ASCIINEMA-INTEGRATION.md`](references/ASCIINEMA-INTEGRATION.md) for component props, Vite SSR rules, and base-path normalization details.

1. **Prepare & Embed `.cast` Recordings**:
   - Use `/asciinema` to sanitize secrets (`sanitize-cast.py`) and strip trailing shell exit prompts (`trim-cast.py --in-place`) before copying `.cast` files into `slides/public/casts/`.
   - Reference recordings with root-relative paths in slide frontmatter:
     ```yaml
     ---
     layout: cast-full
     title: "Recording Title"
     cast: /casts/demo.cast
     autoPlay: false
     speed: 2.0
     idleTimeLimit: 1.0
     fit: both
     ---
     ```
   - When `speed` is set to a value other than `1`, `AsciinemaPlayer.vue` automatically renders a subtle `Playback speed: Nx` badge below the terminal.
2. **Prepare & Embed Images**:
   - Use `/crop-image` (`crop.py --inspect` / `--autocrop`) to remove excess transparent margins or solid borders before placing images in `slides/public/images/`.
   - Reference images via `image: /images/<filename>` in `hardware-callout` slides.
3. **Preserve `BASE_URL` Resolution in Custom Vue Files**:
   - In any custom Vue layout or component that loads local assets from `slides/public/`, normalize paths with `import.meta.env.BASE_URL` so assets resolve on both local dev (`/`) and GitHub Pages subpaths (`/<repo-name>/`).
4. *Completion Criterion*: All `/casts/*` and `/images/*` paths referenced in `slides/acts/*.md` exist in `slides/public/{casts,images}/`.

---

### 5. Run & Manage the Local Dev Server

Manage the background Slidev development server using the bundled [`scripts/slides-server.sh`](scripts/slides-server.sh) utility:

```bash
# Start server on default port 3030 (auto-installs node_modules if missing)
.agents/skills/slidev-deck/scripts/slides-server.sh start

# Check server PID, HTTP status, and navigation URLs
.agents/skills/slidev-deck/scripts/slides-server.sh status

# Restart or stop the server
.agents/skills/slidev-deck/scripts/slides-server.sh restart
.agents/skills/slidev-deck/scripts/slides-server.sh stop

# Use a custom port if 3030 is in use
.agents/skills/slidev-deck/scripts/slides-server.sh start -p 3040
```

#### Live Slidev Endpoints:
- **Presentation Deck**: `http://localhost:3030/`
- **Presenter Console** (speaker notes, timer, next slide): `http://localhost:3030/presenter`
- **Slide Overview Grid**: `http://localhost:3030/overview`

*Completion Criterion*: Running `.agents/skills/slidev-deck/scripts/slides-server.sh status` reports `RUNNING` with `HTTP: 200` (or `304`).

---

### 6. Verify Build & Deploy to GitHub Pages

1. Run the static production build to verify that all Vue components, layouts, Shiki code blocks, and Markdown slides compile cleanly:
   ```bash
   npm --prefix slides run build
   ```
2. To configure automated GitHub Pages deployment, copy the workflow template into `.github/workflows/deploy-slides.yml`:
   ```bash
   mkdir -p .github/workflows
   cp .agents/skills/slidev-deck/resources/deploy-slides.yml .github/workflows/deploy-slides.yml
   ```
3. Ensure repository GitHub Pages settings are configured with **Build and deployment > Source: GitHub Actions**.
4. *Completion Criterion*: `npm --prefix slides run build` exits with returncode 0 and generates `slides/dist/index.html`.
