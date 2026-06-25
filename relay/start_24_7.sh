#!/bin/bash
# Start watchdog + keep Mac awake while relay runs (close laptop lid may still sleep).
cd "$(dirname "$0")/.."
WATCHDOG_PIDFILE=relay/handoffs/watchdog.pid
if [ -f "$WATCHDOG_PIDFILE" ] && kill -0 "$(cat "$WATCHDOG_PIDFILE" 2>/dev/null)" 2>/dev/null; then
  echo "watchdog already running"
else
  nohup ./relay/watchdog.sh >> relay/handoffs/session.log 2>&1 &
  echo $! > relay/handoffs/watchdog.pid
  echo "watchdog pid $(cat relay/handoffs/watchdog.pid)"
fi
# Opt-in only: export RELAY_CAFFEINATE=1 to block system sleep during relay.
if [ "${RELAY_CAFFEINATE:-0}" = "1" ] && ! pgrep -f "caffeinate.*relay" >/dev/null; then
  nohup caffeinate -dims -w "$(cat relay/handoffs/watchdog.pid)" >> relay/handoffs/session.log 2>&1 &
  echo $! > relay/handoffs/caffeinate.pid
  echo "caffeinate pid $(cat relay/handoffs/caffeinate.pid) (RELAY_CAFFEINATE=1 — blocks sleep)"
else
  echo "caffeinate off (Mac can sleep; relay may pause until wake)"
fi
echo "Monitor: tail -f relay/handoffs/session.log"
