# asciicast File Format Specification

Reference specification for `.cast` recording files used across the asciinema ecosystem.

## Version Comparison

| Feature | asciicast v1 | asciicast v2 | asciicast v3 |
| :--- | :--- | :--- | :--- |
| **Data Format** | Monolithic JSON Object | Newline-Delimited JSON (NDJSON) | Newline-Delimited JSON (NDJSON) |
| **Streaming Support** | No (buffer in memory) | Yes (append line-by-line) | Yes (append line-by-line) |
| **Crash Resilience** | None (corrupt on interrupt) | Full (valid up to last written line) | Full (valid up to last written line) |
| **Timestamps** | Inter-frame delays | **Absolute elapsed seconds** ($t - t_0$) | **Relative delta seconds** ($\Delta t$ from previous event) |
| **Exit Code** | No | No | Yes (`"x"` event) |
| **Comment Lines** | No | No | Yes (`# comment line`) |

---

## asciicast v2 Specification

An `asciicast v2` file consists of:
1. **Line 1**: A single JSON object representing the recording header.
2. **Lines 2+**: A stream of 3-element JSON arrays representing events: `[time, type, data]`.

### Header Object (Line 1)

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

#### Fields:
- `version` (*integer, required*): Must be `2`.
- `width` (*integer, required*): Terminal columns.
- `height` (*integer, required*): Terminal rows.
- `timestamp` (*integer, optional*): Unix epoch timestamp when recording started.
- `duration` (*float, optional*): Total recording length in seconds.
- `idle_time_limit` (*float, optional*): Maximum idle duration in seconds to preserve during playback.
- `command` (*string, optional*): Command executed inside the session.
- `title` (*string, optional*): Descriptive recording title.
- `env` (*object, optional*): Environment variables captured at startup (typically `TERM` and `SHELL`).
- `theme` (*object, optional*): Color scheme overrides with `fg`, `bg`, and 8- or 16-color colon-delimited `palette`.

### Event Line Schema: `[time, type, data]`

- **`time`** (*float*): Absolute elapsed seconds from recording start ($t_0$).
- **`type`** (*string*):
  - `"o"`: **Output (stdout)**. Terminal escape sequences and UTF-8 characters printed to screen.
  - `"i"`: **Input (stdin)**. Keystrokes received from keyboard (disabled by default).
  - `"m"`: **Marker**. Bookmark/chapter delimiter; `data` contains optional label.
  - `"r"`: **Resize**. Window dimension change (`"{cols}x{rows}"`).
- **`data`** (*string*): UTF-8 payload.

#### Example Stream:
```json
{"version": 2, "width": 80, "height": 24, "timestamp": 1697400000}
[0.102450, "o", "\u001b[1;32muser@host\u001b[0m:\u001b[1;34m~\u001b[0m$ "]
[0.650120, "o", "echo 'Hello World'\r\n"]
[0.650800, "o", "Hello World\r\n"]
[1.200000, "m", "Chapter 2: Resizing"]
[1.500000, "r", "100x30"]
```

---

## asciicast v3 Specification (CLI 3.x / Rust)

Introduced with asciinema CLI 3.0:

### 1. Relative Delta Timestamps
Instead of absolute timestamps from $t_0$, `time` is the seconds elapsed since the **immediately preceding event**. Lines can be cut, spliced, or reordered without recalculating timestamps for the rest of the file.

### 2. Nested Terminal Metadata
Terminal configuration is grouped under `"term"`:
```json
{
  "version": 3,
  "term": {
    "cols": 80,
    "rows": 24,
    "type": "xterm-256color"
  },
  "timestamp": 1697400000
}
```

### 3. Exit Code Event (`"x"`)
Records child process termination status:
```json
[0.051200, "x", 0]
```

*Note on final frame holding*: In v3 recordings, preceding the `"x"` event with a 2–3s delay (e.g. `[3.0, "x", 0]`) holds the completed terminal screen so viewers can read final output before video players or animated GIFs loop.

### 4. Inline Comments
Lines starting with `#` are treated as comments and ignored by parsers:
```text
# Step 1: Initialize repository
[0.100000, "o", "git init\r\n"]
```
