# Integrate asciinema-player with Slidev

Type: research
Status: resolved
Blocked by: none

## Question

How should `asciinema-player` v3 (with its CSS and WASM bundle) be cleanly packaged as a Vue 3 component for Slidev in `slides/`, ensuring it runs client-side without Vite SSR/build failures, handles responsive container resizing, and supports local `.cast` files?

## Answer

Package `asciinema-player` v3 as a custom Vue 3 Single File Component (`slides/components/AsciinemaPlayer.vue`) using dynamic client-side `import('asciinema-player')` inside `onMounted()` with explicit `player.dispose()` teardown in `onUnmounted()`. Configure `slides/vite.config.ts` with `ssr.noExternal: ['asciinema-player']` and `optimizeDeps.include: ['asciinema-player']` to prevent Node.js SSR pre-rendering failures. Resolve local `.cast` files from `slides/public/casts/` prefixed with `import.meta.env.BASE_URL` to ensure GitHub Pages subpaths don't 404, and attach a `ResizeObserver` on the wrapper element to maintain terminal geometry during Slidev slide transforms.

Comprehensive findings, Vite configs, and copy-pasteable component source on branch `research/asciinema-slidev-integration`: [`docs/research/asciinema-slidev-integration.md`](https://github.com/domesticmouse/skills-three-ways/blob/research/asciinema-slidev-integration/docs/research/asciinema-slidev-integration.md) (local: `git show research/asciinema-slidev-integration:docs/research/asciinema-slidev-integration.md`).
