#!/bin/bash
# Start relay with self-healing supervisor (watchdog respawns if it dies).
cd "$(dirname "$0")/.."
SUP_PIDFILE=relay/handoffs/supervisor.pid
WATCHDOG_PIDFILE=relay/handoffs/watchdog.pid
mkdir -p relay/handoffs

if [ -f "$SUP_PIDFILE" ] && kill -0 "$(cat "$SUP_PIDFILE" 2>/dev/null)" 2>/dev/null; then
  echo "relay supervisor already running pid $(cat "$SUP_PIDFILE")"
  exit 0
fi

nohup bash -c '
  cd "'$(pwd)'"
  while true; do
    echo "supervisor: launching watchdog $(date -u)" >> relay/handoffs/session.log
    ./relay/watchdog.sh
    echo "supervisor: watchdog exited — respawn in 15s $(date -u)" >> relay/handoffs/session.log
    sleep 15
  done
' >> relay/handoffs/session.log 2>&1 &
echo $! > "$SUP_PIDFILE"
echo "supervisor pid $(cat "$SUP_PIDFILE")"

# Opt-in: RELAY_CAFFEINATE=1 blocks system sleep during relay.
if [ "${RELAY_CAFFEINATE:-0}" = "1" ] && ! pgrep -f "caffeinate.*relay" >/dev/null; then
  nohup caffeinate -dims -w "$(cat "$SUP_PIDFILE")" >> relay/handoffs/session.log 2>&1 &
  echo $! > relay/handoffs/caffeinate.pid
  echo "caffeinate on (blocks sleep)"
else
  echo "caffeinate off (Mac can sleep; cron/supervisor resumes after wake)"
fi
echo "Monitor: tail -f relay/handoffs/session.log"
