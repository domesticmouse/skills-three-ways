---
name: slides-dev-server
description: Start, stop, check, and manage the local Slidev development server for slides/. Use when running the slides dev server, previewing slides locally, verifying server health, or troubleshooting presentation ports and URLs.
compatibility: Requires Node.js (v18+) and npm; Slidev installed in slides/
---

# Slides Dev Server

Procedural runbook and tooling to start, verify, stop, and manage the local Slidev presentation development server for the deck located in `slides/`.

## Workflows

Identify the task objective and follow the appropriate workflow:

1. [Start the Slides Dev Server](#1-start-the-slides-dev-server)
2. [Verify Server Health and Endpoints](#2-verify-server-health-and-endpoints)
3. [Stop or Restart the Dev Server](#3-stop-or-restart-the-dev-server)
4. [Custom Port and Port Conflict Resolution](#4-custom-port-and-port-conflict-resolution)
5. [Agent Background Execution Guide](#5-agent-background-execution-guide)

---

### 1. Start the Slides Dev Server

#### Option A: Managed Script (Recommended)

Run the included management script from repo root:

```bash
.agents/skills/slides-dev-server/scripts/slides-server.sh start
```

This script:
1. Verifies if port `3030` is already in use.
2. Checks that `slides/node_modules/` exists (runs `npm install` inside `slides/` if missing).
3. Spawns Slidev in the background with output redirected to `slides/.slidev.log`.
4. Polls `http://localhost:3030/` until HTTP 200/304 is confirmed (up to 15s).

#### Option B: Direct Shell Command

To run interactively in a developer terminal:

```bash
npm --prefix slides run dev
```

Or navigating to the directory:

```bash
cd slides && npm run dev
```

To auto-open the browser upon launch, pass `-- --open`:

```bash
npm --prefix slides run dev -- --open
```

#### Checkable Completion Criterion:
- Running `curl -s -o /dev/null -w "%{http_code}" http://localhost:3030/` returns `200` or `304`.

---

### 2. Verify Server Health and Endpoints

Check if the server is active, identify its PID, and list navigation URLs:

```bash
.agents/skills/slides-dev-server/scripts/slides-server.sh status
```

Or perform manual health checks:

```bash
# Check if port 3030 is bound
lsof -i :3030

# Verify HTTP response code
curl -s -I http://localhost:3030/ | head -n 5
```

#### Slidev Endpoints:
- **Presentation Deck**: [http://localhost:3030/](http://localhost:3030/)
- **Presenter Console** (notes, timer, next slide): [http://localhost:3030/presenter](http://localhost:3030/presenter)
- **Slide Overview Grid**: [http://localhost:3030/overview](http://localhost:3030/overview)

#### Checkable Completion Criterion:
- The script or curl command confirms status code `200` and displays the presentation URL.

---

### 3. Stop or Restart the Dev Server

#### Stop the Server:

Using the management script:

```bash
.agents/skills/slides-dev-server/scripts/slides-server.sh stop
```

Or terminate the process bound to port 3030 manually:

```bash
# Find and terminate Slidev on port 3030
PID=$(lsof -ti :3030)
if [ -n "$PID" ]; then
  kill $PID
fi
```

#### Restart the Server:

```bash
.agents/skills/slides-dev-server/scripts/slides-server.sh restart
```

#### Checkable Completion Criterion:
- Running `lsof -ti :3030` produces empty output and `curl -s http://localhost:3030/` fails to connect.

---

### 4. Custom Port and Port Conflict Resolution

If port `3030` is occupied by another application or multiple slide decks are being previewed:

#### Using the Management Script:

```bash
# Start on custom port 3040
.agents/skills/slides-dev-server/scripts/slides-server.sh start -p 3040

# Check status on custom port 3040
.agents/skills/slides-dev-server/scripts/slides-server.sh status -p 3040

# Stop server on custom port 3040
.agents/skills/slides-dev-server/scripts/slides-server.sh stop -p 3040
```

#### Using Direct npm / slidev Flag:

```bash
npm --prefix slides run dev -- --port 3040
```

#### Checkable Completion Criterion:
- `curl -s -o /dev/null -w "%{http_code}" http://localhost:3040/` returns `200`.

---

### 5. Agent Background Execution Guide

When an Antigravity agent or autonomous assistant starts the Slidev server as a long-running background process:

1. **Use `run_command` with `IsDaemon: true`**:
   - `Cwd`: `/Users/brett/Documents/GitHub/skills-three-ways/slides`
   - `CommandLine`: `npm run dev` (or `npm run dev -- --port 3030`)
   - `IsDaemon`: `true`
   - `WaitMsBeforeAsync`: `2000`
2. **Verify immediate readiness**:
   - Execute a synchronous curl check: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3030/`.
   - If not yet ready, retry after 1–2 seconds.
3. **Present links to the user**:
   - Presentation: `http://localhost:3030/`
   - Presenter View: `http://localhost:3030/presenter`
   - Overview: `http://localhost:3030/overview`

#### Checkable Completion Criterion:
- Daemon background process is active and HTTP GET to `http://localhost:3030/` returns `200`.
