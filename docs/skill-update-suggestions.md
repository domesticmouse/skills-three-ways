# Skill & Customization Update Suggestions

Post-conversation retrospective mapping the layout fixes, Slidev quirks, server lifecycle findings, and hardware truth corrections from polishing the deck into clean updates across Antigravity's customization layers (**on-demand Skills** for procedural runbooks/templates vs. **always-on Rules** for short non-negotiable guardrails, with zero duplication).

---

## 1. `.agents/skills/slidev-deck/`

Primary home for all Slidev authoring conventions, copy-pasteable archetypes, and dev-server mechanics.

### 1.1 Dev Server Lifecycle under Agent Harnesses (`SKILL.md` §5 & `scripts/slides-server.sh`)

- **Why `slides-server.sh` fails under agent shells**: [`scripts/slides-server.sh`](../.agents/skills/slidev-deck/scripts/slides-server.sh#L81-L85) spawns `nohup npm run dev ... &`, which dies as soon as an ephemeral non-daemon `run_command` finishes (process-group reaping). Running a sandboxed server also binds inside the sandbox network namespace so the host browser hits connection refused (`HTTP 000`).
- **Update §5**:
  - Keep `scripts/slides-server.sh` for interactive human terminals.
  - Document the agent-native workflow: launch `npm --prefix slides run dev -- --port 3030` directly as a persistent daemon (`IsDaemon: true`, unsandboxed when the host browser needs `localhost:3030`), and terminate it with `manage_task` rather than relying on `.slidev.pid`.

### 1.2 Slidev `v-click` Mechanics & Narrative Order (`SKILL.md` §3 & `references/SLIDE-PATTERNS.md`)

- **Progressive reveals by default**: Add `v-click` to `<li v-click>`, comparison cards, summary boxes, and trailing callouts across all templates in [`references/SLIDE-PATTERNS.md`](../.agents/skills/slidev-deck/references/SLIDE-PATTERNS.md).
- **Avoid nested auto-incremented `v-click` (Slidev v0.48.9 bug/trap)**:
  - Slidev's `v-click` directive calls `resolveClick()` inside Vue's `mounted()` hook (`+1` auto-increment). Because Vue mounts children before parents, a nested `<strong v-click>` or `<p v-click>` registers *first* and receives a lower click index than its parent `<div v-click>`—causing both to appear simultaneously when the parent finally unhides.
  - **Rule**: Whenever nesting a reveal inside another `v-click` container, assign explicit numeric indices (`v-click="1"`, `v-click="2"`, `v-click="3"`) to decouple click order from mount order.
- **Setup before reveal**: Place framing prose or setup cards *above* code snippets and reveal the punchline code *below* on `v-click`—never put the code reveal before the setup it explains.
- **Reactive diagram highlights**: Document binding `:class` expressions against Slidev's reactive `$clicks` (e.g., `$clicks === 1`, `$clicks === 2`) alongside explicit `v-click` blocks when highlighting parts of inline SVG/HTML diagrams step by step.

### 1.3 Canvas Height Budget, Whitespace, Code Width & Tables (`SKILL.md` §3 & `references/SLIDE-PATTERNS.md`)

- **Document usable canvas budgets upfront**:
  - `layout: default`: ~`868 × 472 px` usable area.
  - `layout: skill-breakdown`: ~`890 × 401 px` usable inner card area.
- **Replace cramped default list spacing**: Update the `space-y-4 mt-5` / `mt-1 space-y-1` defaults in [`references/SLIDE-PATTERNS.md`](../.agents/skills/slidev-deck/references/SLIDE-PATTERNS.md#L84-L106) with item-count sizing targets:
  - *3-item takeaway lists*: Keep concise single-line bullets and use airy spacing (`space-y-10 mt-10` on `<ol>`, `mt-3 space-y-2.5` on nested `<ul>`).
  - *5–6 item lists*: Scale vertically (`space-y-7` to `space-y-8`) with a spaced trailing summary box (`mt-9 p-4 text-sm`) so content fills the frame rather than hugging the top half.
- **Full-width code rule**: Never squeeze code blocks with lines > ~50 chars into `col-span-6` half-width columns where Shiki clips lines horizontally. Give code full width and pair it either with:
  - vertically stacked explanation boxes below (`space-y-4` / `space-y-3`, setting `m-0` on card `<p>` tags so bottom padding matches top padding), or
  - a 2-column setup row above (`grid-cols-2`) followed by full-width code below on `v-click`.
- **Add a Structured Reference Table archetype**:
  - Cap at 3–4 scannable columns (**Item**, **Pins / Key**, **Interface / Scope**, **Rule / Polarity**).
  - Use `w-full text-left border-collapse`, header underline (`border-b border-gray-700`), row dividers (`divide-y divide-gray-800/80`), `py-2.5`–`py-3` cell padding, bold white left anchors, plain colored `font-mono` pin columns (avoiding noisy per-pin `<code>` pill clutter), and accent highlights for traps/inversions.
- **Warn against invalid utility typos**: Explicitly note that `text-s` is not a valid UnoCSS/Tailwind class (unlike `text-xs` or `text-sm`) and silently falls back to `16px`.

### 1.4 Drop `step: Zoom-In X of Y` Visual Noise (`SKILL.md` §3, `SLIDE-PATTERNS.md` §6, `resources/layouts/skill-breakdown.vue`)

- Remove `step: Zoom-In 1 of 3` from:
  - [`SKILL.md`](../.agents/skills/slidev-deck/SKILL.md#L118) (`layout: skill-breakdown` summary line)
  - [`references/SLIDE-PATTERNS.md`](../.agents/skills/slidev-deck/references/SLIDE-PATTERNS.md#L181-L192) (prose description and frontmatter block)
- Keep [`resources/layouts/skill-breakdown.vue`](../.agents/skills/slidev-deck/resources/layouts/skill-breakdown.vue#L11-L15) optional `step` support if ever needed internally, or drop `step` from recommended frontmatter so only `skill` renders cleanly on the right.

### 1.5 CommonMark HTML-Block Trap & Stronger Build Verification (`SKILL.md` §3 & §6)

- **Expand the Markdown/HTML guardrail (§3 item 3)**:
  - Not only fenced code blocks—**never leave blank lines inside non-code HTML blocks (`<div>`, `<table>`, `<ol>`) when subsequent lines are indented by 4+ spaces**. CommonMark exits the HTML block at the blank line and parses indented HTML tags as a literal `<pre><code>` code block on the slide.
- **Upgrade §6 completion criteria**:
  - Note that `npm --prefix slides run build` returning exit code `0` does *not* catch CommonMark raw-HTML `<pre><code>` mistakes or misordered `v-click` indices.
  - After complex HTML/SVG edits or nested `v-click` slides, spot-check the compiled `slides/dist/assets/slidev/<N>-*.js` render function to verify native DOM nodes and exact click numbers (`[[r,1]]`, `[[r,2]]`, `[[r,3]]`).

---

## 2. `AGENTS.md` (Always-On Workspace Rules)

Per Antigravity's customization rules (`docs/rules.md` / `agy-customizations`), `AGENTS.md` is injected on every turn and should contain crisp invariants rather than full HTML templates that drift from skills:

- **Remove stale template duplication**: Delete the multi-line non-`v-click` `<ol class="space-y-4 ...">` snippet in [`AGENTS.md`](../AGENTS.md) so `AGENTS.md` and `slidev-deck` don't contradict each other.
- **Keep short always-on invariants + skill pointer**:
  - Keep: no title badges/pills, conversational speaker notes without bracketed stage directions, numbered lists preferred over dense cards, and **no `Zoom-In X of Y` step labels**.
  - Add: default `v-click` progressive reveals (setup before reveal; explicit indices when nested) and point to `.agents/skills/slidev-deck/SKILL.md` for layouts and canvas spacing patterns.

---

## 3. `.agents/skills/gamma-pinout/SKILL.md`

- **Fix Left Keypad ASCII diagram (`lines 151–154`)**: [`SKILL.md`](../.agents/skills/gamma-pinout/SKILL.md#L151-L154) currently left-aligns `N5–N7` directly under `N1–N3`. Per [`slides/public/images/GammaMiniSynth.png`](../slides/public/images/GammaMiniSynth.png), the physical PCB shifts the Left Keypad's 3 bottom keys **right** under columns 2–4 (leaving column 1 open above the left thumbstick, mirroring how the Right Keypad leaves column 4 open above the right thumbstick):

```text
  [ N1 ]   [ N2 ]   [ N3 ]   [ N4 ]     <-- Top Row
           [ N5 ]   [ N6 ]   [ N7 ]     <-- Bottom Row
```

---

## 4. Scope & Portability

- **Keep repo-specific skills in `.agents/skills/`**: `gamma-pinout` and the Daisy/Gamma hardware skills belong strictly in workspace VCS.
- **Evaluate promoting `slidev-deck`**: Keep `slidev-deck` in `.agents/skills/` if it remains tied to this talk's repository, or promote the updated skill to global scope (`~/.gemini/config/skills/slidev-deck/`) or a shareable plugin if you intend to build future Slidev decks across other repos.

---

## 5. Implementation Checklist

- [ ] Update [`.agents/skills/slidev-deck/SKILL.md`](../.agents/skills/slidev-deck/SKILL.md) (§3 formatting/budget/v-click/CommonMark rules, §5 agent daemon workflow, §6 compiled bundle check).
- [ ] Update [`.agents/skills/slidev-deck/references/SLIDE-PATTERNS.md`](../.agents/skills/slidev-deck/references/SLIDE-PATTERNS.md) (`v-click` defaults, airy spacing, full-width code + setup-before-reveal templates, 4-col reference table archetype, remove `Zoom-In X of Y`).
- [ ] Sync [`.agents/skills/slidev-deck/resources/layouts/skill-breakdown.vue`](../.agents/skills/slidev-deck/resources/layouts/skill-breakdown.vue) if simplifying frontmatter fields.
- [ ] Slim [`AGENTS.md`](../AGENTS.md) down to non-duplicated always-on slide invariants + pointer to `slidev-deck`.
- [ ] Correct the Left Keypad ASCII alignment diagram in [`.agents/skills/gamma-pinout/SKILL.md`](../.agents/skills/gamma-pinout/SKILL.md#L151-L154).
- [ ] Run `./.agents/skills/agent-skills/scripts/validate-skill.py` on modified skills and verify `npm --prefix slides run build` still exits `0`.
