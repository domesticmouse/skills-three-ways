# Comprehensive Technical Investigation: asciinema Architecture, Recording, Playback, and Ecosystem

This report presents an exhaustive, primary-source investigation into the **asciinema** ecosystem (frequently referred to as "ascii cinema"), covering its terminal virtualization architecture, CLI tools, file format specifications (asciicast v1, v2, v3), web embedding, asset conversion, data sanitization, and enterprise self-hosting.

Every technical claim, schema definition, and configuration parameter cited below is sourced directly from official project repositories and documentation:
- **Official Documentation**: [docs.asciinema.org](https://docs.asciinema.org/)
- **Core CLI Repository**: [github.com/asciinema/asciinema](https://github.com/asciinema/asciinema)
- **Web Player Repository**: [github.com/asciinema/asciinema-player](https://github.com/asciinema/asciinema-player)
- **GIF Generator Repository**: [github.com/asciinema/agg](https://github.com/asciinema/agg)
- **Server Repository**: [github.com/asciinema/asciinema-server](https://github.com/asciinema/asciinema-server)
- **File Format Specifications**: [docs.asciinema.org/asciicast/](https://docs.asciinema.org/asciicast/)

---

## 1. Overview & Architecture

### 1.1 What asciinema Is
**asciinema** is an open-source suite of tools designed to record, replay, stream, and share terminal sessions. Rather than recording visual screen output as video codecs (such as H.264, VP9, or animated GIFs), asciinema captures the raw, text-based stream of byte events entering and leaving a Unix pseudo-terminal (PTY) along with precise millisecond timestamps.

### 1.2 PTY Capture vs. Video Screen Capture
Traditional video screen recorders (OBS, QuickTime, ffmpeg) capture graphical pixel buffers 30 to 60 times per second:
- **Video Disadvantages**: Heavy CPU/GPU rendering overhead, large binary payloads (tens to hundreds of megabytes), resolution scaling blurriness, loss of semantic text metadata, and impossibility of selecting or copying on-screen terminal text.
- **Asciinema Architecture (PTY Capture)**:
  1. **PTY Allocation**: asciinema allocates a Unix pseudo-terminal master/slave pair (via `openpty`/`forkpty` system calls).
  2. **Process Execution**: The user's target shell or commanded binary runs inside the slave PTY.
  3. **Event Interception**: The asciinema daemon attaches to the master PTY, monitoring raw byte streams (`stdout`, and optionally `stdin`), terminal window resize events (`SIGWINCH`), and high-resolution system clock intervals.
  4. **Data Stream Preservation**: Raw ANSI/VT100 escape sequences (SGR color codes, cursor position movements, screen clearing codes) and UTF-8 characters are written directly to a stream file with timestamps.
  5. **Dynamic Reconstruction**: Playback engines (both CLI and Web Player) implement virtual terminal emulators that parse ANSI sequences dynamically into terminal state grids. 
  6. **Benefits**: File sizes are infinitesimal (10 KB to 200 KB for minutes of activity), render razor-sharp text at any display DPI, and enable native text copy-pasting directly from the player.

### 1.3 Version History: Python CLI (v2) vs. Rust Rewrite (v3)
- **asciinema CLI v1.x & v2.x (Python)**:
  - Implemented in Python 3.
  - Relied on the host Python interpreter and platform packaging dependencies.
  - v2 established the line-delimited streaming standard (`asciicast v2`).
- **asciinema CLI v3.x (Rust Rewrite)**:
  - *Primary Source*: [asciinema 3.0 Announcement & Docs](https://docs.asciinema.org/) / [github.com/asciinema/asciinema](https://github.com/asciinema/asciinema).
  - Completely rewritten from scratch in **Rust**.
  - **Standalone Binaries**: Distributes zero-dependency, statically linked single binaries without requiring Python runtime environments.
  - **Core Integration**: Built on top of `avt` (asciinema virtual terminal library in Rust), enabling native headless terminal state emulation.
  - **Format Evolution**: Introduced the `asciicast v3` specification utilizing relative interval/delta timings, exit codes (`x`), and comment support (`#`).
  - **Native Live Streaming**: Introduced the `asciinema stream` command supporting both local peer-to-peer/LAN HTTP streaming and remote relay streaming through an asciinema server.
  - **Format Conversion Subsystem**: Built-in `asciinema convert` to transform between v1, v2, v3, raw streams, and plain text.

---

## 2. Installation & Requirements

### 2.1 Supported Operating Systems & Terminal Environments
- **Supported OS**:
  - **macOS**: macOS 11+ (Apple Silicon and Intel x86_64).
  - **Linux**: All standard distributions (glibc and musl-based): Debian, Ubuntu, Arch Linux, Fedora, Alpine, openSUSE, Gentoo, NixOS.
  - **BSD**: FreeBSD, OpenBSD, NetBSD.
  - **Windows**: Not natively supported due to Windows Console subsystem differences with POSIX pseudo-terminals; officially supported and recommended via **Windows Subsystem for Linux (WSL / WSL2)**.
- **Terminal Requirements**:
  - POSIX-compliant PTY interface (`/dev/pts`).
  - Terminal emulator supporting standard ANSI/VT100/xterm escape codes and 256-color or 24-bit truecolor (SGR).
  - UTF-8 character encoding configured in system locale (`$LANG`, `$LC_ALL`, or `$LC_CTYPE` containing `UTF-8`).

### 2.2 Package Managers & Installation Methods
*Source*: [docs.asciinema.org/getting-started/](https://docs.asciinema.org/getting-started/)

```bash
# macOS (Homebrew & MacPorts)
brew install asciinema
# or
sudo port install asciinema

# Debian / Ubuntu (22.04+)
sudo apt update && sudo apt install asciinema

# Arch Linux
sudo pacman -S asciinema

# Fedora
sudo dnf install asciinema

# Alpine Linux
apk add asciinema

# Nix / NixOS
nix-env -i asciinema
# or within nix shell: nix-shell -p asciinema

# FreeBSD
pkg install py39-asciinema # (or current pkg variant)

# Python Package Index (CLI 2.x releases via pipx / pip)
pipx install asciinema
# or
python3 -m pip install asciinema

# Standalone Pre-compiled Binaries (GitHub Releases)
# Direct executable download for Linux x86_64, aarch64, and macOS
curl -sL https://github.com/asciinema/asciinema/releases/latest/download/asciinema-x86_64-unknown-linux-musl.tar.gz | tar -xz
sudo mv asciinema /usr/local/bin/

# Containerized execution (Docker / Podman)
docker pull ghcr.io/asciinema/asciinema
docker run --rm -it -v "$PWD":/data ghcr.io/asciinema/asciinema rec /data/demo.cast
```

---

## 3. Recording Sessions (`asciinema rec`)

*Source*: [docs.asciinema.org/manual/cli/rec/](https://docs.asciinema.org/manual/cli/)

### 3.1 Command Syntax & CLI Flags
The `asciinema rec` (alias: `asciinema record`) command launches an intercepted subshell and streams session events:

```bash
asciinema rec [options] [filename.cast]
```

#### Key Command-Line Flags:
- **`-i, --idle-time-limit <sec>`**: Limits recorded terminal inactivity to at most `<sec>` seconds (floating-point). Long pauses between keystrokes or waiting for long compiles are truncated, ensuring recordings remain fast-paced. In v2/v3, this value is also embedded in the file header (`idle_time_limit`).
- **`-c, --command <cmd>`**: Executes `<cmd>` directly inside the PTY rather than launching an interactive `$SHELL`. Recording concludes immediately when the commanded process exits (e.g. `asciinema rec -c "htop" htop.cast`).
- **`-I, --capture-input`** *(CLI 3.x)* / **`--stdin`** *(CLI 2.x)*: Enables keyboard input recording. Standard asciinema recordings capture only output (`stdout`). Enabling stdin capture records every raw keystroke as `"i"` events.
- **`-a, --append`**: Appends new terminal events to an existing `.cast` recording file rather than creating a new one.
- **`--overwrite`** *(CLI 3.x)* / **`-y, --yes`** *(CLI 2.x)*: Overwrites the target recording file without interactive confirmation prompts.
- **`-t, --title <title>`**: Embeds an arbitrary descriptive string into the header metadata of the recording.
- **`-f, --output-format <format>`** *(CLI 3.x)*: Explicitly sets output format: `asciicast-v3` (default), `asciicast-v2`, `raw`, or `txt`.
- **`--window-size <cols>x<rows>`**: Overrides the initial PTY window dimensions (e.g. `--window-size 80x24`).
- **`--headless`** *(CLI 3.x)*: Operates without an interactive terminal attached to recorder output (used in CI/CD automation or headless background sessions).
- **`--return`**: Configures asciinema to exit with the return code of the executed child command rather than asciinema's own process status.
- **`-q, --quiet`**: Suppresses informational status output to stderr (e.g. *"~ Asciicast recording started."*).

### 3.2 Environment Variables & Key Bindings During Recording

#### Configuration Files:
- CLI 3.x: `$HOME/.config/asciinema/config.toml`
- CLI 2.x: `$HOME/.config/asciinema/config`

#### Interactive Key Bindings:
- **Pause / Resume Recording**: **`Ctrl+\`** toggles capturing on and off. When paused, terminal commands continue to run normally, but all generated stdout/stdin data is omitted from the recorded stream (analogous to muting a microphone).
  - Config key: `recording.pause_key = "C-\\"` (v3) or `rec.pause_key = "C-\\"` (v2).
- **Insert Marker**: Triggers an `"m"` marker event at the current timestamp, bookmarking the position for chapter navigation or automated breakpoints.
  - Config key: `recording.add_marker_key = "C-x"` (v3) or `rec.add_marker_key = "C-x"` (v2).
- **Prefix Key**: Configures a modal hotkey (similar to `tmux` / GNU `screen` `Ctrl+b`):
  - Config key: `recording.prefix_key = "C-a"`.
- **Exit Recording**: Type `exit` or press **`Ctrl+d`** to terminate the shell/PTY session.

#### Environment Variables:
- `ASCIINEMA_SERVER_URL`: Specifies the target server URL for uploads and remote streaming (defaults to `https://asciinema.org`).
- `SHELL`: Path to the shell spawned if `-c` is omitted.
- `NO_COLOR`: Suppresses ANSI styling in asciinema's own CLI banners.

### 3.3 Output Destination: Local Storage vs. asciinema.org Upload
1. **Local File**: Specifying a path saves the file locally:
   ```bash
   asciinema rec session.cast
   ```
2. **Interactive Prompt**: If the file path argument is omitted, asciinema saves the recording to a temporary file in `/tmp/` and prompts upon session exit:
   ```text
   ~ Asciicast recording finished.
   ~ Press <enter> to upload to asciinema.org, <ctrl+c> to save locally.
   ```
3. **Manual Upload**: Any existing local file can be published explicitly:
   ```bash
   asciinema upload session.cast
   ```
   *Privacy*: Default uploads generate unlisted "secret" URLs (e.g. `https://asciinema.org/a/bJMOlPe5F4mFLY0Rl6fiJSOp3`). They are not indexed in search engines or public profiles unless claimed and made public.
4. **Account Linking (`asciinema auth`)**:
   ```bash
   asciinema auth
   ```
   Generates a one-time activation link embedding the CLI's installation UUID (stored in `$HOME/.config/asciinema/install-id`). Visiting this URL binds all recordings uploaded from that machine to your registered user profile on asciinema.org or your self-hosted server.

---

## 4. Terminal Playback (`asciinema play`)

*Source*: [docs.asciinema.org/manual/cli/play/](https://docs.asciinema.org/manual/cli/)

### 4.1 Playback Command Options
To replay a recording directly within the terminal console:

```bash
# Replay local file
asciinema play demo.cast

# Stream and replay remote recording from asciinema.org or raw URL
asciinema play https://asciinema.org/a/335445
asciinema play https://example.com/recordings/demo.cast
```

#### CLI Flags:
- **`-s, --speed <multiplier>`**: Alters playback timing. Values `> 1.0` accelerate playback; values `< 1.0` slow it down (e.g. `asciinema play -s 2.0 demo.cast`).
- **`-i, --idle-time-limit <sec>`**: Enforces or overrides the maximum delay between events during playback.
- **`-l, --loop`**: Automatically restarts playback in an infinite loop upon reaching the end.
- **`-m, --pause-on-markers`**: Automatically pauses playback every time a marker (`"m"`) event is encountered, turning recordings into stepped presentation slides.

### 4.2 Interactive Playback Shortcuts
While replaying in the terminal, keyboard controls can manipulate playback in real-time:

| Shortcut | Action | Config Setting (CLI 3.x) | Config Setting (CLI 2.x) |
| :--- | :--- | :--- | :--- |
| **`Space`** | Pause / resume playback | `playback.pause_key = " "` | `play.pause_key = " "` |
| **`.` (dot)** | Step forward single frame | `playback.step_key = "."` | `play.step_key = "."` |
| **`]`** | Jump to next marker | `playback.next_marker_key = "]"` | `play.next_marker_key = "]"` |
| **`Ctrl+c`** | Immediately terminate playback | — | — |

---

## 5. File Format Specifications (`asciicast`)

*Sources*:
- [asciicast v1 specification](https://docs.asciinema.org/asciicast/v1/)
- [asciicast v2 specification](https://docs.asciinema.org/asciicast/v2/)
- [asciicast v3 specification](https://docs.asciinema.org/asciicast/v3/)

### 5.1 asciicast v1 vs. v2 vs. v3 Architecture

| Feature | asciicast v1 | asciicast v2 | asciicast v3 |
| :--- | :--- | :--- | :--- |
| **Data Format** | Monolithic JSON Object | Newline-Delimited JSON (NDJSON) | Newline-Delimited JSON (NDJSON) |
| **Streaming Support** | No (buffer in memory) | Yes (line-by-line append) | Yes (line-by-line append) |
| **Crash Resilience** | None (corrupt on interrupt) | Full (valid up to crash line) | Full (valid up to crash line) |
| **Timestamps** | Delays between frames | **Absolute time** (from $t_0$) | **Delta time** (from prior event) |
| **Comment Support** | No | No | Yes (`# comment line`) |
| **Exit Code Recording**| No | No | Yes (`"x"` event) |

### 5.2 asciicast v2 Deep Dive

An `asciicast v2` recording consists of:
1. **Header Object (Line 1)**: Single-line JSON object.
2. **Event Stream (Lines 2+)**: Continuous stream of 3-element JSON arrays: `[time, type, data]`.

#### Header Object Schema:
```json
{
  "version": 2,
  "width": 80,
  "height": 24,
  "timestamp": 1697400000,
  "duration": 42.15,
  "idle_time_limit": 2.0,
  "command": "/bin/zsh",
  "title": "Tutorial Demo",
  "env": {
    "TERM": "xterm-256color",
    "SHELL": "/bin/zsh"
  },
  "theme": {
    "fg": "#d0d0d0",
    "bg": "#151515",
    "palette": "#151515:#ac4142:#7e8e50:#e5b567:#6c99bb:#9f4e85:#7dd6cf:#d0d0d0:#505050:#ac4142:#7e8e50:#e5b567:#6c99bb:#9f4e85:#7dd6cf:#f5f5f5"
  }
}
```
- **`version`** (*integer, required*): Must be `2`.
- **`width`** (*integer, required*): Initial terminal columns.
- **`height`** (*integer, required*): Initial terminal rows.
- **`timestamp`** (*integer, optional*): Unix epoch timestamp of recording initiation.
- **`idle_time_limit`** (*float, optional*): Maximum idle duration in seconds to preserve during playback.
- **`env`** (*object, optional*): Whitelisted map of captured environment variables (typically `TERM` and `SHELL`).
- **`theme`** (*object, optional*): Defines `fg` (hex text color), `bg` (hex background color), and `palette` (colon-delimited 8 or 16 hex color strings).

#### Event Line Schema: `[time, type, data]`
Each event is a 3-element array:
1. **`time`** (*float*): Elapsed time in seconds (with microsecond precision) since the start of recording.
2. **`type`** (*string*):
   - **`"o"` (Output / stdout)**: Data printed to the terminal screen. Contains UTF-8 text and ANSI escape sequences.
   - **`"i"` (Input / stdin)**: Data read from the terminal keyboard (disabled by default).
   - **`"m"` (Marker)**: Breakpoint or chapter bookmark. `data` contains an optional chapter label.
   - **`"r"` (Resize)**: Window size change event triggered by `SIGWINCH`. `data` specifies `"{COLS}x{ROWS}"`.
3. **`data`** (*string*): The UTF-8 payload.

```json
{"version": 2, "width": 80, "height": 24, "timestamp": 1697400000}
[0.102450, "o", "\u001b[1;32muser@host\u001b[0m:\u001b[1;34m~\u001b[0m$ "]
[0.650120, "o", "echo 'Hello World'\r\n"]
[0.650800, "o", "Hello World\r\n"]
[1.200000, "m", "Chapter 2: Resizing"]
[1.500000, "r", "100x30"]
```

### 5.3 asciicast v3 Evolution
Introduced with CLI 3.0:
- **Relative Deltas**: Rather than absolute timestamps from $t_0$, `time` represents seconds since the **immediately preceding event**. If an author edits or deletes a line in the middle of a `.cast` file, they do not have to recalculate every subsequent timestamp.
- **Grouped Terminal Metadata**: The header nests terminal parameters under a `"term"` dictionary (`cols`, `rows`, `type`).
- **Exit Code Event (`"x"`)**: Records child process termination code: `[0.0, "x", 0]`.
- **Comments**: Lines prefixed with `#` are ignored by parsers.

---

## 6. Web Playback & Embedding

*Source*: [docs.asciinema.org/manual/player/](https://docs.asciinema.org/manual/player/) / [github.com/asciinema/asciinema-player](https://github.com/asciinema/asciinema-player)

### 6.1 `asciinema-player` Overview
The official web player is written in TypeScript and Rust (compiled to WebAssembly via `wasm-pack` and `avt`). It simulates a full virtual terminal state inside the browser DOM.

- **NPM Package**: `asciinema-player`
- **Bundled Files**: Distributed with `dist/bundle/asciinema-player.js` and `dist/bundle/asciinema-player.css`.
- **API Paradigm**: Starting with player v3, custom web components (`<asciinema-player>`) were superseded by a direct JavaScript initialization API: `AsciinemaPlayer.create(src, containerElement, options)`.

### 6.2 Player Configuration Options Reference

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`cols`** | `number` | `80` (or header) | Terminal column width |
| **`rows`** | `number` | `24` (or header) | Terminal row height |
| **`autoPlay`** / **`autoplay`** | `boolean` | `false` | Automatically starts playback on load |
| **`preload`** | `boolean` | `false` | Immediately downloads recording file before interaction |
| **`loop`** | `boolean \| number`| `false` | `true` loops infinitely; integer sets fixed iteration count |
| **`startAt`** | `number \| string`| `0` | Skips to offset in seconds or NPT notation (`"1:15"`) |
| **`speed`** | `number` | `1.0` | Playback speed multiplier (e.g. `2.0`) |
| **`idleTimeLimit`** | `number` | Header limit | Max seconds of pause between frames |
| **`theme`** | `string` | `"asciinema"` | Terminal color theme (see below) |
| **`poster`** | `string` | `undefined` | Preview frame: `"npt:0:15"` or `"data:text/plain,..."` |
| **`fit`** | `string \| boolean`| `"width"` | Scaling behavior: `"width"`, `"height"`, `"both"`, `"none"` |
| **`controls`** | `boolean \| "auto"`| `"auto"` | Control bar visibility (`true`, `false`, or `"auto"` on hover)|
| **`markers`** | `array` | `[]` | Timeline markers: `[5.0, 12.5]` or `[[5.0, "Start"], [20.0, "End"]]` |
| **`pauseOnMarkers`**| `boolean` | `false` | Auto-pause upon hitting markers |
| **`terminalFontSize`**| `string` | `"small"` | CSS font-size or preset: `"small"`, `"medium"`, `"big"` |
| **`terminalFontFamily`**| `string` | Monospace fallback | CSS font family list |
| **`terminalLineHeight`**| `number` | `1.3333` | Relative line height multiplier |

#### Built-in Themes:
`asciinema`, `dracula`, `monokai`, `nord`, `solarized-dark`, `solarized-light`, `gruvbox-dark`, `tango`, `github-dark`, `github-light`.

### 6.3 Framework Integration Patterns

#### A. Vanilla HTML
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

#### B. React & Docusaurus (Next.js / SSR-Safe)
Because `asciinema-player` interacts directly with DOM APIs and WebAssembly binaries, it will throw errors if executed on a Node.js SSR runtime. It must be dynamically imported in a `useEffect` hook or wrapped in Docusaurus's `<BrowserOnly>`.

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

export default function TerminalPlayer({ src, theme = 'dracula', speed = 1, autoPlay = false }: TerminalPlayerProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let playerInstance: any = null;
    let isMounted = true;

    // Dynamic import isolates browser execution from SSR
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

#### C. Vue 3 & VitePress
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

*VitePress Config Warning*: In `.vitepress/config.ts`, ensure dynamic libraries or WASM dependencies are exempt from SSR bundling:
```ts
export default defineConfig({
  vite: {
    ssr: {
      noExternal: ['asciinema-player']
    }
  }
});
```

#### D. Static Site Generators (Hugo Shortcode)
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
Usage in Markdown: `{{< asciinema id="demo1" src="/casts/install.cast" theme="nord" >}}`

### 6.4 asciinema.org Embed Options
When hosted on asciinema.org, three official embedding mechanisms are supported:
1. **Dynamic Script Injection**:
   ```html
   <script src="https://asciinema.org/a/335445.js" id="asciicast-335445" async></script>
   ```
   *Behavior*: Automatically creates an auto-resizing `<iframe>` pointing to the hosted player.
2. **Direct Responsive `<iframe>`**:
   ```html
   <iframe src="https://asciinema.org/a/335445/iframe" width="100%" height="400" frameborder="0"></iframe>
   ```
3. **Markdown Image Badge (Safe for GitHub READMEs)**:
   GitHub strictly sanitizes `<script>` and `<iframe>` tags in markdown. The platform generates an SVG screenshot link:
   ```markdown
   [![asciicast](https://asciinema.org/a/335445.svg)](https://asciinema.org/a/335445)
   ```

---

## 7. Converting & Exporting Recordings

*Source*: [docs.asciinema.org/manual/agg/](https://docs.asciinema.org/manual/agg/) / [github.com/asciinema/agg](https://github.com/asciinema/agg)

### 7.1 `agg` (asciinema GIF Generator)
`agg` is the official, high-performance command-line tool written in Rust to compile `.cast` files into animated GIFs.
- **Engine**: Employs `gifski` (the highest-quality lossy/lossless GIF encoder) alongside `avt` for ANSI terminal emulation.
- **Installation**:
  ```bash
  # Cargo
  cargo install agg
  # Homebrew
  brew install agg
  # Arch Linux
  pacman -S agg
  ```

#### CLI Syntax & Flags:
```bash
agg [options] input.cast output.gif
```
- **`--theme <name>`**: Specifies color scheme (`asciinema`, `dracula` [default], `monokai`, `solarized-dark`, `solarized-light`, `gruvbox-dark`, `nord`, `github-dark`, `github-light`).
- **`--speed <num>`**: Speed multiplier (e.g. `--speed 2.0`).
- **`--fps-cap <num>`**: Limits maximum frames per second (default: `30`). Lowering to `15` or `12` drastically reduces GIF file size.
- **`--font-size <px>`**: Pixel size of the terminal font (default: `14`).
- **`--font-family <family>`**: Font family fallback string (e.g. `"Fira Code, JetBrains Mono, monospace"`).
- **`--line-height <num>`**: Relative terminal line spacing (default: `1.4`).
- **`--last-frame-duration <sec>`**: How many seconds to pause on the final frame before looping (default: `3.0`).
- **`--idle-time-limit <sec>`**: Overrides max pause duration between frames.

```bash
# High-efficiency, compact documentation GIF
agg --theme monokai --fps-cap 15 --speed 1.5 --idle-time-limit 2 demo.cast demo.gif
```

### 7.2 SVG and Vector Export
- **Asciinema Server SVG Endpoint**: Asciinema server instances automatically compile server-side vector snapshots at `https://asciinema.org/a/<id>.svg`.
- **Third-Party Animated SVG Tools**:
  - `svg-term-cli`: Node.js utility (`npm install -g svg-term-cli`) that transforms asciicast recordings into self-contained animated SVGs via CSS keyframe animations.
    ```bash
    cat demo.cast | svg-term --out demo.svg --window --width 80 --height 24
    ```

### 7.3 Raw Stream & Plain Text Extraction (`asciinema convert` / `cat`)
- **`asciinema convert`** *(CLI 3.x)*:
  ```bash
  # Convert between formats
  asciinema convert input.cast output.v2.cast -f asciicast-v2
  asciinema convert input.cast output.txt -f txt
  ```
- **`asciinema cat`**: Dumps raw terminal stdout stream directly to terminal stdout without timing pauses. Useful for piping into utilities:
  ```bash
  asciinema cat demo.cast | grep "ERROR"
  asciinema cat demo.cast > raw_output.log
  ```

---

## 8. Privacy, Security & Sanitization

*Source*: [docs.asciinema.org/manual/cli/rec/](https://docs.asciinema.org/manual/cli/) / [asciicast v2 spec](https://docs.asciinema.org/asciicast/v2/)

### 8.1 Sensitive Data Risks
Because asciinema attaches directly to a PTY master device, it records **all raw bytes transmitted to stdout**:
- **Passwords entered in terminal**: When tools like `sudo`, `su`, or `ssh` prompt for passwords, they put the terminal into raw cooked mode and disable terminal echo (`termios.c_lflag &= ~ECHO`). Because keystrokes are not echoed back to `stdout`, **passwords are NOT captured in default recordings**.
- **THE STDIN CAVEAT**: If stdin recording is explicitly enabled via `-I` or `--stdin`, raw keystrokes are saved into `"i"` events. In this mode, **passwords, PINs, and secrets typed into the terminal ARE recorded in plaintext**.
- **Environment Variable Leaks**: If commands like `printenv`, `env`, or `export` are run, or if error traces print tokens/keys to stdout, those characters are stored permanently in `"o"` events.
- **Header Metadata**: Inspect the first-line JSON header: by default, asciinema captures `$TERM` and `$SHELL`. Verify that custom configurations did not inject custom environment variables (`--capture-env`).

### 8.2 Sanitizing & Post-Processing `.cast` Files
Because `asciicast v2` and `v3` files are plain newline-delimited JSON, redaction can be performed deterministically via standard text streams:

#### A. Regex Redaction with `sed`
```bash
# Redact GitHub personal access tokens
sed -E 's/ghp_[a-zA-Z0-9]{36}/ghp_REDACTED/g' recording.cast > sanitized.cast

# Redact AWS Access Keys
sed -E 's/AKIA[0-9A-Z]{16}/AKIA_REDACTED/g' sanitized.cast > final.cast
```

#### B. Programmatic Frame Trimming with Python
To trim unwanted preamble commands, delete sensitive sections, or remove stdin (`"i"`) events completely:

```python
#!/usr/bin/env python3
import json
import sys

def sanitize_cast(input_path, output_path, redact_pattern=None):
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        # Process header (Line 1)
        header = json.loads(infile.readline())
        # Clean sensitive env keys if present
        if "env" in header:
            header["env"] = {k: v for k, v in header["env"].items() if k in ["TERM", "SHELL"]}
        outfile.write(json.dumps(header) + '\n')
        
        # Process event lines (Lines 2+)
        for line in infile:
            if not line.strip() or line.startswith('#'):
                continue
            event = json.loads(line)
            time, event_type, data = event[0], event[1], event[2]
            
            # Strip all stdin input events to eliminate credential keylogging
            if event_type == "i":
                continue
                
            # Perform string replacements on terminal output
            if event_type == "o" and redact_pattern:
                for secret, placeholder in redact_pattern.items():
                    data = data.replace(secret, placeholder)
                    
            outfile.write(json.dumps([time, event_type, data]) + '\n')

if __name__ == "__main__":
    replacements = {"supersecrettoken123": "REDACTED_TOKEN"}
    sanitize_cast("raw.cast", "sanitized.cast", replacements)
```

---

## 9. Self-Hosting / `asciinema-server`

*Source*: [docs.asciinema.org/manual/server/](https://docs.asciinema.org/manual/server/) / [github.com/asciinema/asciinema-server](https://github.com/asciinema/asciinema-server)

Organizations requiring internal session storage, private access controls, or on-prem air-gapped infrastructure can deploy their own instance of **asciinema-server**.

### 9.1 Server Architecture & Requirements
- **Technology Stack**: Written in Elixir using the Phoenix web framework; frontend terminal playback driven by `asciinema-player`.
- **System Requirements**:
  - Container engine: Docker, Podman, or Kubernetes.
  - Memory: 512 MB minimum (1 GB recommended).
  - Database: PostgreSQL 14.0 or newer.
  - Storage: Local filesystem or AWS S3-compatible object storage (MinIO, S3, GCS).
  - Mail server: SMTP relay for passwordless magic login emails (optional for single-user instances).

### 9.2 Docker Compose Deployment (`docker-compose.yml`)
The official container image is published at `ghcr.io/asciinema/asciinema-server`.

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: asciinema
      POSTGRES_PASSWORD: asciinema_db_password
      POSTGRES_DB: asciinema_prod
    volumes:
      - pgdata:/var/lib/postgresql/data

  asciinema:
    image: ghcr.io/asciinema/asciinema-server:latest
    restart: always
    depends_on:
      - postgres
    ports:
      - "4000:4000"
    environment:
      # Mandatory: 64-character random string (generate with: openssl rand -hex 32)
      SECRET_KEY_BASE: "78cf196238b97587bcba29381640a92cd86b240182470984cfb7eef2009234ae"
      DATABASE_URL: "ecto://asciinema:asciinema_db_password@postgres:5432/asciinema_prod"
      SERVER_URL: "https://asciinema.corp.internal"
      SERVER_NAME: "Internal asciinema"
      
      # Security & Admin Access
      ADMIN_PANEL_ON_MAIN_ENDPOINT: "1"
      SIGN_UP_DISABLED: "false" # Set to "true" after creating initial admin account
      
      # SMTP Configuration for magic login links
      SMTP_HOST: "smtp.mailgun.org"
      SMTP_PORT: "587"
      SMTP_USERNAME: "postmaster@mail.corp.internal"
      SMTP_PASSWORD: "smtp_secret_password"
      SMTP_FROM_ADDRESS: "asciinema@corp.internal"
      
      # Optional: S3 Object Storage for .cast assets
      # FS_STORE: "s3"
      # S3_BUCKET: "internal-asciinema-casts"
      # S3_REGION: "us-east-1"
      # S3_AWS_ACCESS_KEY_ID: "..."
      # S3_AWS_SECRET_ACCESS_KEY: "..."
    volumes:
      - uploads:/opt/app/uploads

volumes:
  pgdata:
  uploads:
```

### 9.3 Server Administration & Setup Workflow
1. **Initialize Database**: The official container runs automated Ecto database migrations upon startup.
2. **First User Bootstrap**: The first account that signs up via the server automatically receives administrator privileges.
3. **Lock Down Signups**: Once authorized users have claimed accounts, set `SIGN_UP_DISABLED=true` in the environment to prevent unauthorized external access.
4. **Point asciinema CLI to Private Server**:
   Configure local development machines or servers to upload exclusively to the internal instance:

   ```bash
   # Method A: Environment variable
   export ASCIINEMA_SERVER_URL="https://asciinema.corp.internal"

   # Method B: Global configuration file (~/.config/asciinema/config.toml)
   [api]
   server_url = "https://asciinema.corp.internal"
   ```

5. **Authenticate CLI with Private Server**:
   ```bash
   asciinema auth
   ```
   The CLI outputs an authentication link pointing to `https://asciinema.corp.internal/connect/<uuid>`, binding the terminal client installation to the user's private enterprise account.

---

## 10. Summary & Synthesis

asciinema replaces lossy, oversized video recordings with deterministic Unix pseudo-terminal event streams. The transition from Python (v2) to Rust (v3) has eliminated runtime dependencies while introducing delta-timed streaming (`asciicast v3`), native live terminal broadcasts, and tight coupling with WebAssembly-driven web players (`asciinema-player`) and GIF compilers (`agg`). The newline-delimited JSON structure of `.cast` files ensures infinite scalability, instant copy-pasting of terminal commands, crash resilience, and easy compliance filtering for sensitive corporate environments.
