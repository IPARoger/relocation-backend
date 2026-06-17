#!/bin/bash
cd "$(dirname "$0")/.."
PIDFILE=relay-sandbox/handoffs/supervisor.pid
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "sandbox supervisor already running pid=$(cat "$PIDFILE")"
  exit 0
fi
nohup python3 -u relay-sandbox/supervisor.py >> relay-sandbox/handoffs/supervisor.nohup.log 2>&1 &
echo $! > "$PIDFILE"
echo "started sandbox supervisor pid=$(cat "$PIDFILE")"
echo "monitor: tail -f relay-sandbox/handoffs/session.log"
