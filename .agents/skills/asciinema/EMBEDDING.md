# Web Playback & Embedding Guide

Integrate asciinema sessions into web applications, static documentation, and markdown files.

## Overview

The official web player (`asciinema-player` v3) is implemented in TypeScript and Rust (compiled to WebAssembly via `wasm-pack` and `avt`). It runs a headless terminal state emulator in the browser DOM, rendering sharp text with full ANSI support, palette theming, and copy-paste capabilities.

- **NPM Package**: `asciinema-player`
- **Assets**: `dist/bundle/asciinema-player.js` and `dist/bundle/asciinema-player.css`
- **Core API**: `AsciinemaPlayer.create(src, containerElement, options)`

---

## Player Options Reference

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `cols` | `number` | `80` (or header) | Terminal columns override |
| `rows` | `number` | `24` (or header) | Terminal rows override |
| `autoPlay` / `autoplay` | `boolean` | `false` | Automatically starts playback on load |
| `preload` | `boolean` | `false` | Preloads recording file before user interaction |
| `loop` | `boolean \| number` | `false` | `true` loops infinitely; integer sets fixed iteration count |
| `startAt` | `number \| string` | `0` | Skip to offset in seconds or NPT timestamp (`"1:15"`) |
| `speed` | `number` | `1.0` | Playback speed multiplier (e.g. `1.5`, `2.0`) |
| `idleTimeLimit` | `number` | Header limit | Max pause in seconds between frames |
| `theme` | `string` | `"asciinema"` | Terminal color theme (see below) |
| `poster` | `string` | `undefined` | Preview frame: `"npt:0:15"` or `"data:text/plain,..."` |
| `fit` | `string \| boolean` | `"width"` | Scaling mode: `"width"`, `"height"`, `"both"`, `"none"` |
| `controls` | `boolean \| "auto"` | `"auto"` | Control bar visibility (`true`, `false`, or `"auto"` on hover) |
| `markers` | `array` | `[]` | Chapter markers: `[5.0, 12.5]` or `[[5.0, "Start"], [20.0, "End"]]` |
| `pauseOnMarkers` | `boolean` | `false` | Auto-pause upon hitting markers |
| `terminalFontSize` | `string` | `"small"` | Preset (`"small"`, `"medium"`, `"big"`) or CSS size |
| `terminalFontFamily` | `string` | Monospace fallback | CSS font family string |
| `terminalLineHeight` | `number` | `1.3333` | Relative line height multiplier |

### Built-in Themes
`asciinema`, `dracula`, `monokai`, `nord`, `solarized-dark`, `solarized-light`, `gruvbox-dark`, `tango`, `github-dark`, `github-light`.

---

## Framework Integration Patterns

### 1. Vanilla HTML & JavaScript

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="asciinema-player.css" />
</head>
<body>
  <div id="player-container"></div>
  <script src="asciinema-player.js"></script>
  <script>
    AsciinemaPlayer.create('/recordings/demo.cast', document.getElementById('player-container'), {
      theme: 'dracula',
      speed: 1.5,
      idleTimeLimit: 2,
      poster: 'npt:0:02',
      fit: 'width'
    });
  </script>
</body>
</html>
```

---

### 2. React / Next.js / Docusaurus (SSR-Safe)

> [!IMPORTANT]
> `asciinema-player` interacts directly with DOM APIs and WebAssembly binaries. It will throw errors if executed in Node.js server environments. Load it dynamically inside `useEffect` or wrap it with client-only containers.

```tsx
// components/TerminalPlayer.tsx
import React, { useEffect, useRef } from 'react';
import 'asciinema-player/dist/bundle/asciinema-player.css';

interface TerminalPlayerProps {
  src: string;
  theme?: string;
  speed?: number;
  autoPlay?: boolean;
}

export default function TerminalPlayer({
  src,
  theme = 'dracula',
  speed = 1,
  autoPlay = false
}: TerminalPlayerProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let playerInstance: any = null;
    let isMounted = true;

    // Dynamic import prevents server-side execution
    import('asciinema-player').then((AsciinemaPlayer) => {
      if (isMounted && containerRef.current) {
        playerInstance = AsciinemaPlayer.create(src, containerRef.current, {
          theme,
          speed,
          autoPlay,
          fit: 'width'
        });
      }
    });

    return () => {
      isMounted = false;
      if (playerInstance && typeof playerInstance.dispose === 'function') {
        playerInstance.dispose();
      }
    };
  }, [src, theme, speed, autoPlay]);

  return <div ref={containerRef} />;
}
```

---

### 3. Vue 3 & VitePress

```vue
<!-- components/TerminalPlayer.vue -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import 'asciinema-player/dist/bundle/asciinema-player.css';

const props = defineProps<{
  src: string;
  theme?: string;
}>();

const containerRef = ref<HTMLDivElement | null>(null);
let player: any = null;

onMounted(async () => {
  const AsciinemaPlayer = await import('asciinema-player');
  if (containerRef.value) {
    player = AsciinemaPlayer.create(props.src, containerRef.value, {
      theme: props.theme || 'dracula',
      fit: 'width'
    });
  }
});

onUnmounted(() => {
  player?.dispose?.();
});
</script>

<template>
  <div ref="containerRef" />
</template>
```

**VitePress Config (`.vitepress/config.ts`)**: Exempt `asciinema-player` from SSR bundling:
```ts
export default defineConfig({
  vite: {
    ssr: {
      noExternal: ['asciinema-player']
    }
  }
});
```

---

### 4. Hugo Shortcode

Create `layouts/shortcodes/asciinema.html`:
```html
{{ $id := .Get "id" }}
<div id="player-{{ $id }}"></div>
<script>
  window.addEventListener('DOMContentLoaded', () => {
    AsciinemaPlayer.create('{{ .Get "src" }}', document.getElementById('player-{{ $id }}'), {
      theme: '{{ .Get "theme" | default "dracula" }}',
      speed: {{ .Get "speed" | default 1.0 }}
    });
  });
</script>
```

Usage in Markdown content:
```markdown
{{< asciinema id="install-demo" src="/casts/install.cast" theme="nord" >}}
```

---

## Hosted asciinema.org Embeds

When hosting recordings on asciinema.org or a private server:

### A. Dynamic Script Injection
```html
<script src="https://asciinema.org/a/335445.js" id="asciicast-335445" async></script>
```

### B. Responsive `<iframe>`
```html
<iframe src="https://asciinema.org/a/335445/iframe" width="100%" height="400" frameborder="0"></iframe>
```

### C. Markdown SVG Badge (Safe for GitHub READMEs)
GitHub sanitizes `<script>` and `<iframe>` tags in markdown. Use the platform-generated SVG badge:
```markdown
[![asciicast](https://asciinema.org/a/335445.svg)](https://asciinema.org/a/335445)
```
