#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
SLIDES_DIR="$REPO_ROOT/slides"
PID_FILE="$SLIDES_DIR/.slidev.pid"
LOG_FILE="$SLIDES_DIR/.slidev.log"
DEFAULT_PORT=3030

PORT="${PORT:-$DEFAULT_PORT}"

# Parse command line flags
COMMAND="${1:-status}"
shift || true

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--port)
      PORT="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

check_server_listening() {
  local port="$1"
  lsof -ti :"$port" 2>/dev/null || true
}

get_http_code() {
  local port="$1"
  local code
  code="$(curl --noproxy "*" -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${port}/" 2>/dev/null || true)"
  if [[ "$code" =~ ^[1-5][0-9]{2}$ ]]; then
    echo "$code"
  else
    echo "000"
  fi
}

cmd_status() {
  local pids
  pids="$(check_server_listening "$PORT")"
  if [[ -n "$pids" ]]; then
    local code
    code="$(get_http_code "$PORT")"
    if [[ "$code" != "000" && -n "$code" ]]; then
      echo "Slidev server is RUNNING on port $PORT (PID: $pids, HTTP: $code)"
    else
      echo "Slidev server is RUNNING on port $PORT (PID: $pids)"
    fi
    echo "  - Presentation: http://localhost:$PORT/"
    echo "  - Presenter View: http://localhost:$PORT/presenter"
    echo "  - Overview: http://localhost:$PORT/overview"
    return 0
  else
    echo "Slidev server is NOT running on port $PORT."
    return 1
  fi
}

cmd_start() {
  local pids
  pids="$(check_server_listening "$PORT")"
  if [[ -n "$pids" ]]; then
    echo "Slidev server is ALREADY running on port $PORT (PID: $pids)."
    cmd_status
    return 0
  fi

  if [[ ! -d "$SLIDES_DIR/node_modules" ]]; then
    echo "Installing missing dependencies in $SLIDES_DIR..."
    (cd "$SLIDES_DIR" && npm install)
  fi

  echo "Starting Slidev server in background on port $PORT..."
  (
    cd "$SLIDES_DIR"
    nohup npm run dev -- --port "$PORT" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
  )

  # Wait up to 15 seconds for server to respond
  local count=0
  local max_wait=30
  local success=0
  echo -n "Waiting for server to become ready on http://localhost:$PORT/..."
  while [[ $count -lt $max_wait ]]; do
    local code
    code="$(get_http_code "$PORT")"
    if [[ "$code" == "200" || "$code" == "304" ]]; then
      success=1
      break
    fi
    sleep 0.5
    count=$((count + 1))
    echo -n "."
  done
  echo ""

  if [[ $success -eq 1 ]]; then
    echo "Slidev server started successfully!"
    cmd_status
    return 0
  else
    echo "Error: Slidev server did not respond within 15 seconds."
    if [[ -f "$LOG_FILE" ]]; then
      echo "=== Recent server logs ($LOG_FILE) ==="
      tail -n 20 "$LOG_FILE"
    fi
    return 1
  fi
}

cmd_stop() {
  local pids
  pids="$(check_server_listening "$PORT")"

  if [[ -z "$pids" ]] && [[ -f "$PID_FILE" ]]; then
    pids="$(cat "$PID_FILE" 2>/dev/null || true)"
  fi

  if [[ -n "$pids" ]]; then
    echo "Stopping Slidev server (PID: $pids) on port $PORT..."
    # shellcheck disable=SC2086
    kill $pids 2>/dev/null || true
    sleep 1

    # Check if still running, send SIGKILL if needed
    local remaining
    remaining="$(check_server_listening "$PORT")"
    if [[ -n "$remaining" ]]; then
      echo "Force killing remaining process (PID: $remaining)..."
      # shellcheck disable=SC2086
      kill -9 $remaining 2>/dev/null || true
    fi

    rm -f "$PID_FILE"
    echo "Slidev server stopped."
    return 0
  else
    echo "No Slidev server running on port $PORT."
    rm -f "$PID_FILE"
    return 0
  fi
}

cmd_restart() {
  cmd_stop
  sleep 1
  cmd_start
}

case "$COMMAND" in
  status)
    cmd_status
    ;;
  start)
    cmd_start
    ;;
  stop)
    cmd_stop
    ;;
  restart)
    cmd_restart
    ;;
  *)
    echo "Usage: $0 {status|start|stop|restart} [-p|--port PORT]"
    exit 1
    ;;
esac
