#!/bin/bash
cd "$(dirname "$0")/.."
PIDFILE=relay-sandbox/handoffs/supervisor.pid
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "sandbox supervisor already running pid=$(cat "$PIDFILE")"
  exit 0
fi
# Pass soak env through nohup (defaults: target=10, mock=0, min=3600s)
export RELAY_SANDBOX_TARGET="${RELAY_SANDBOX_TARGET:-10}"
export RELAY_SANDBOX_MIN_ELAPSED_SEC="${RELAY_SANDBOX_MIN_ELAPSED_SEC:-3600}"
export RELAY_SANDBOX_MOCK="${RELAY_SANDBOX_MOCK:-0}"
export RELAY_SANDBOX_FRESH="${RELAY_SANDBOX_FRESH:-1}"
export RELAY_SANDBOX_PROGRESS_SEC="${RELAY_SANDBOX_PROGRESS_SEC:-600}"
nohup env \
  RELAY_SANDBOX_TARGET="$RELAY_SANDBOX_TARGET" \
  RELAY_SANDBOX_MIN_ELAPSED_SEC="$RELAY_SANDBOX_MIN_ELAPSED_SEC" \
  RELAY_SANDBOX_MOCK="$RELAY_SANDBOX_MOCK" \
  RELAY_SANDBOX_FRESH="$RELAY_SANDBOX_FRESH" \
  RELAY_SANDBOX_PROGRESS_SEC="$RELAY_SANDBOX_PROGRESS_SEC" \
  python3 -u relay-sandbox/supervisor.py >> relay-sandbox/handoffs/supervisor.nohup.log 2>&1 &
echo $! > "$PIDFILE"
echo "started sandbox supervisor pid=$(cat "$PIDFILE")"
echo "monitor: tail -f relay-sandbox/handoffs/session.log"
