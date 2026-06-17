#!/bin/bash
# Start watchdog + keep Mac awake while relay runs (close laptop lid may still sleep).
cd "$(dirname "$0")/.."
if pgrep -f "relay/watchdog.sh" >/dev/null; then
  echo "watchdog already running"
else
  nohup ./relay/watchdog.sh >> relay/handoffs/session.log 2>&1 &
  echo $! > relay/handoffs/watchdog.pid
  echo "watchdog pid $(cat relay/handoffs/watchdog.pid)"
fi
if ! pgrep -f "caffeinate.*relay" >/dev/null; then
  nohup caffeinate -dims -w "$(cat relay/handoffs/watchdog.pid)" >> relay/handoffs/session.log 2>&1 &
  echo $! > relay/handoffs/caffeinate.pid
  echo "caffeinate pid $(cat relay/handoffs/caffeinate.pid) (prevents idle sleep)"
fi
echo "Monitor: tail -f relay/handoffs/session.log"
