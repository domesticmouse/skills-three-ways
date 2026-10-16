---
name: asciinema
description: Record, replay, convert, and embed terminal sessions. Use when recording terminal demos, converting .cast files to animated GIF or SVG, embedding asciinema-player in web apps, sanitizing terminal recordings, inspecting cast durations, or trimming trailing exit sequences.
---

# Asciinema

Tools and procedures to record, replay, export, sanitize, and embed terminal sessions using the asciinema ecosystem.

## Workflows

Identify the user's objective and choose the matching workflow:

1. [Record a Terminal Session](#1-record-a-terminal-session)
2. [Replay or Inspect a Recording](#2-replay-or-inspect-a-recording)
3. [Convert and Export (GIF / SVG / Text)](#3-convert-and-export)
4. [Sanitize and Redact Sensitive Data](#4-sanitize-and-redact-sensitive-data)
5. [Trim Exit Sequences and Inspect Timing](#5-trim-exit-sequences-and-inspect-timing)
6. [Embed in Web Applications](#6-embed-in-web-applications)
7. [Self-Host an asciinema Server](#7-self-host-an-asciinema-server)

---

### 1. Record a Terminal Session

Launch an intercepted PTY session using `asciinema rec`:

```bash
# Basic interactive recording
asciinema rec session.cast

# Record with idle-time cap (recommended: 2.0s) and non-interactive overwrite
asciinema rec -i 2.0 --overwrite session.cast

# Record a specific command and exit immediately upon completion
asciinema rec -c "pnpm test" -i 2.0 test-run.cast

# Headless recording in CI/automation with fixed dimensions
asciinema rec --headless --window-size 100x30 -c "./build.sh" build.cast
```

#### Core Flags & Rules:
- **`-i, --idle-time-limit <sec>`**: Limits pauses between terminal events. Always specify this for tutorials and documentation (recommended: `1.5` to `2.0`).
- **`-c, --command <cmd>`**: Executes a command directly and terminates recording when done.
- **`--overwrite`**: Overwrites the target file without an interactive confirmation prompt.
- **`--window-size <cols>x<rows>`**: Sets explicit terminal dimensions (e.g. `80x24`, `120x30`).
- **Security Guardrail**: Do **not** use `-I` or `--stdin` unless explicitly required. Capturing keyboard input logs raw keystrokes and can expose passwords, tokens, and credentials in plaintext.

#### Interactive Hotkeys During Recording:
- **`Ctrl+\`**: Pause and resume recording (acts like a microphone mute).
- **`Ctrl+x`**: Insert chapter marker (`"m"` event) at current timestamp.
- **`Ctrl+d`** or `exit`: Terminate session and save recording.

---

### 2. Replay or Inspect a Recording

#### Terminal Replay
```bash
# Replay local cast
asciinema play session.cast

# Accelerated playback (2x speed) with 1s max pause
asciinema play -s 2.0 -i 1.0 session.cast

# Pause automatically on markers (slide mode)
asciinema play -m session.cast

# Loop continuously
asciinema play -l session.cast
```

**Playback Controls**: `Space` (pause/resume), `.` (step frame), `]` (next marker), `Ctrl+c` (quit).

#### Fast Inspection & Text Extraction
```bash
# Dump raw terminal stdout without timing pauses (pipeable)
asciinema cat session.cast | grep "ERROR"

# Convert cast to plain text (CLI 3.x)
asciinema convert session.cast output.txt -f txt

# Convert format between v3 and v2 (CLI 3.x)
asciinema convert session.v3.cast session.v2.cast -f asciicast-v2
```

For schema details on v1, v2, and v3 files, see [FORMAT.md](FORMAT.md).

---

### 3. Convert and Export

#### A. Compile to Animated GIF (`agg`)
Use `agg` (asciinema GIF generator) for high-quality, lightweight GIFs:

```bash
# Compact, web-ready documentation GIF
agg --theme monokai --fps-cap 15 --speed 1.5 --idle-time-limit 2 session.cast demo.gif
```

**Optimization options**:
- `--theme <name>`: `dracula` (default), `monokai`, `solarized-dark`, `solarized-light`, `gruvbox-dark`, `nord`, `github-dark`, `github-light`.
- `--fps-cap <num>`: Cap FPS to `15` or `12` to drastically reduce file size.
- `--font-size <px>`: Default `14`.
- `--last-frame-duration <sec>`: Pause on final frame before loop (default `3.0`).

#### B. Vector / SVG Export
- **Self-contained animated SVG**:
  ```bash
  cat session.cast | svg-term --out demo.svg --window --width 80 --height 24
  ```
- **asciinema.org SVG Badge** (Safe for GitHub READMEs):
  ```markdown
  [![asciicast](https://asciinema.org/a/<id>.svg)](https://asciinema.org/a/<id>)
  ```

---

### 4. Sanitize and Redact Sensitive Data

Before publishing or sharing `.cast` files, strip secrets and credential keystrokes:

1. **Verify stdin is stripped**: Default recordings do not capture keystrokes, but if `-I`/`--stdin` was used, `"i"` events must be deleted.
2. **Scrub Environment Metadata**: Verify `env` in header line 1 contains only safe values (`TERM`, `SHELL`).
3. **Redact Output Patterns**: Replace API keys, tokens, or internal URLs in `"o"` events.

Use the bundled utility script [scripts/sanitize-cast.py](scripts/sanitize-cast.py):

```bash
# Strip stdin events and clean environment metadata
python3 .agents/skills/asciinema/scripts/sanitize-cast.py session.cast sanitized.cast

# Strip stdin and redact custom sensitive patterns
python3 .agents/skills/asciinema/scripts/sanitize-cast.py session.cast sanitized.cast \
  --redact "ghp_123456=REDACTED" "internal.corp=example.com"
```

Quick regex redaction with `sed`:
```bash
sed -E 's/(ghp_[a-zA-Z0-9]{36}|AKIA[0-9A-Z]{16})/REDACTED/g' session.cast > sanitized.cast
```

---

### 5. Trim Exit Sequences and Inspect Timing

Interactive recordings frequently capture trailing `Ctrl+D` keystrokes, warning prompts (e.g. `press ctrl+d again to exit`), resume text, or dropping back into the shell prompt before session termination.

Use the bundled utility script [scripts/trim-cast.py](scripts/trim-cast.py):

#### A. Inspect Durations and Detect Exit Sequences
Inspect recording duration (both raw elapsed time and `idle_time_limit` playback time) and auto-detect trailing exit prompts without modifying the file:

```bash
# Print timing analysis and trailing pattern detection
python3 .agents/skills/asciinema/scripts/trim-cast.py session.cast --info
```

#### B. Strip Exit Sequences and Hold Final Frame
Cut off the trailing exit sequence and append a clean exit event (`"x"`) holding on the final frame (default: 3.0s pause before exit) so that video exports and looping web players don't immediately restart:

```bash
# Trim in place with default 3.0s final frame hold
python3 .agents/skills/asciinema/scripts/trim-cast.py session.cast --in-place

# Trim and write to a new file with custom 2.0s hold
python3 .agents/skills/asciinema/scripts/trim-cast.py session.cast trimmed.cast --hold 2.0

# Trim at an explicit pattern or regex
python3 .agents/skills/asciinema/scripts/trim-cast.py session.cast --in-place --cut-at "press ctrl+d"
```

- **Checkable Completion Criterion**: Run `python3 .agents/skills/asciinema/scripts/trim-cast.py <file> --info`. Confirm that no trailing exit sequence is detected and duration matches the expected trimmed time.

---

### 6. Embed in Web Applications

Integrate interactive virtual terminal playback using `asciinema-player` v3 (WASM/Rust driven).

Consult [EMBEDDING.md](EMBEDDING.md) for complete copy-pasteable code examples:
- **Vanilla HTML / JS**: `AsciinemaPlayer.create(src, container, options)`
- **React / Next.js / Docusaurus**: SSR-safe dynamic import inside `useEffect`
- **Vue 3 / VitePress**: Client-only dynamic mount with Vite SSR exclusion
- **Hugo**: Reusable shortcode
- **asciinema.org Embeds**: Direct `<script>` widget or responsive `<iframe>`

---

### 7. Self-Host an asciinema Server

For private session repositories, air-gapped networks, or corporate compliance:
- Run `asciinema-server` via Docker Compose (Phoenix + PostgreSQL).
- Configure CLI clients with `export ASCIINEMA_SERVER_URL="https://asciinema.corp.internal"`.
- Run `asciinema auth` to link local CLI installations to private accounts.

Full Docker Compose configuration, environment variables, and bootstrap steps are documented in [SELF-HOSTING.md](SELF-HOSTING.md).
