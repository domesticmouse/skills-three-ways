# Asciinema & Asset Integration Reference

Architecture and troubleshooting reference for embedding `asciinema-player` v3 and static assets inside Slidev (`slides/`) for both local development and GitHub Pages subpath builds.

---

## 1. Why `AsciinemaPlayer.vue` Uses Dynamic Client Imports

Slidev pre-renders slides in Node.js during `slidev build`. Importing `asciinema-player` at module top-level fails during SSR because the player accesses browser DOM globals (`window`, `document`).

[`resources/components/AsciinemaPlayer.vue`](../resources/components/AsciinemaPlayer.vue) solves this with four mechanisms:

1. **Dynamic Import in `onMounted`**:
   ```ts
   const AsciinemaPlayer = await import('asciinema-player')
   playerInstance = AsciinemaPlayer.create(resolvedSrc, containerRef.value, playerOptions)
   ```
2. **Vite SSR Configuration (`slides/vite.config.ts`)**:
   ```ts
   export default defineConfig({
     optimizeDeps: {
       include: ['asciinema-player'],
     },
     ssr: {
       noExternal: ['asciinema-player'],
     },
   })
   ```
3. **`ResizeObserver` Reflow**:
   Slidev scales slides using CSS transforms. Attaching a `ResizeObserver` on the container element and calling `playerInstance.render()` ensures terminal geometry stays crisp across view transitions and presenter-console previews.
4. **Automatic Playback Speed Pill**:
   Whenever `:speed` is set to a value other than `1` (e.g., `2.0`, `10.0`, `20.0`), the component displays a pill badge (`Playback speed: 10x`) beneath the terminal so the audience knows when a long build or codebase scan has been accelerated.

---

## 2. Base URL Resolution for GitHub Pages (`resolveUrl`)

When building for GitHub Pages with `slidev build --base /<repo-name>/`, root-relative URLs like `/casts/demo.cast` or `/images/photo.png` passed as Vue props will 404 at `https://<user>.github.io/casts/demo.cast` unless prefixed with Vite's `import.meta.env.BASE_URL`.

Both `AsciinemaPlayer.vue` and `layouts/hardware-callout.vue` normalize local paths via `resolveUrl`:

```ts
function resolveUrl(rawSrc: string | undefined): string {
  if (!rawSrc) return ''
  if (
    rawSrc.startsWith('http://') ||
    rawSrc.startsWith('https://') ||
    rawSrc.startsWith('data:') ||
    rawSrc.startsWith('blob:')
  ) {
    return rawSrc
  }
  const base = import.meta.env.BASE_URL || '/'
  const normalizedBase = base.endsWith('/') ? base : `${base}/`
  const cleanPath = rawSrc.replace(/^\.?\//, '')
  return `${normalizedBase}${cleanPath}`
}
```

Always include `resolveUrl()` in any new custom Vue layout or component that renders local files from `slides/public/`.

---

## 3. High-Contrast Terminal Theme Overrides (`slides/style.css`)

Default terminal palettes often render dim gray comments (`--term-color-8`) or dark blue prompts (`--term-color-4`) with low contrast on projectors. [`resources/style.css`](../resources/style.css) overrides `.ap-player` and `.asciinema-player-theme-dracula` with high-contrast Tokyo Night / Dracula colors:

- `--term-color-4: #7aa2f7` (Vibrant blue for prompt text)
- `--term-color-8: #9aa5ce` (Readable bright slate for secondary labels and timestamps)
- `--term-color-background: #1a1b26` (Distinct terminal surface against the `#121317` slide background)

---

## 4. Recommended Playback Settings by Recording Type

| Recording Type | Recommended `speed` | `idleTimeLimit` | `fit` | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Short Q&A or single command (~15–30s) | `1.5` – `2.0` | `1.0` | `both` | Easy to read live while keeping talk pacing tight |
| Multi-step build or test run (~1–2m) | `3.0` – `5.0` | `1.0` | `both` | Shows full progress without stalling the presentation |
| Deep codebase audit or multi-file generation (3–10m) | `10.0` – `20.0` | `1.0` | `both` | Compresses a 5-minute agent run into a 15–25s visual beat |

Before copying a `.cast` file into `slides/public/casts/`, run the `/asciinema` skill's trim utility so the player stops cleanly on the final output frame instead of showing `exit` or shell termination prompts:

```bash
python3 .agents/skills/asciinema/scripts/trim-cast.py slides/public/casts/demo.cast --in-place
```
