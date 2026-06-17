#!/bin/bash
# Restart sandbox supervisor if dead; log to session.log
cd "$(dirname "$0")/.."
PIDFILE=relay-sandbox/handoffs/supervisor.pid
LOG=relay-sandbox/handoffs/session.log
INTERVAL="${RELAY_SANDBOX_MONITOR_SEC:-600}"
while true; do
  if [ ! -f "$PIDFILE" ] || ! kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    echo "monitor: supervisor dead, restarting $(date -u)" >> "$LOG"
    ./relay-sandbox/start.sh
  fi
  sleep "$INTERVAL"
done
