#!/bin/bash
# Restarts session if dead OR hung (heartbeat stuck on cycle_start too long).
cd "$(dirname "$0")/.."

load_env() {
  for f in .env.local .env; do
    [ -f "$f" ] || continue
    while IFS= read -r line || [ -n "$line" ]; do
      line="${line%%#*}"
      line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
      [ -z "$line" ] && continue
      case "$line" in *=*) export "$line" ;; esac
    done < "$f"
  done
}
load_env

set +e
INTERVAL="${RELAY_WATCHDOG_INTERVAL:-120}"
# Default 90 min: just over RELAY_CYCLE_TIMEOUT (3600) would be too long; use 90 min or env
STALE="${RELAY_STALE_SEC:-5400}"
HUNG="${RELAY_HUNG_SEC:-2700}"
PIDFILE=relay/handoffs/session.pid
LOG=relay/handoffs/session.log

start_session() {
  nohup ./relay/run_session.sh >> "$LOG" 2>&1 &
  echo $! > "$PIDFILE"
  echo "watchdog: started session pid $(cat "$PIDFILE") $(date -u)" >> "$LOG"
}

kill_session() {
  echo "watchdog: killing session pid $(cat "$PIDFILE" 2>/dev/null) $(date -u)" >> "$LOG"
  pkill -f "relay/run_cycle.py" 2>/dev/null
  pkill -f "relay_robot.py" 2>/dev/null
  pkill -P "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null
  kill "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null
  sleep 5
}

while true; do
  if [ ! -f "$PIDFILE" ] || ! kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    start_session
  elif [ -f relay/handoffs/heartbeat ]; then
    ts=$(head -1 relay/handoffs/heartbeat 2>/dev/null)
    note=$(tail -1 relay/handoffs/heartbeat 2>/dev/null)
    now=$(date +%s)
    age=$(( now - ${ts%.*} ))
    if [ -n "$ts" ] && [ "$age" -gt "$STALE" ]; then
      echo "watchdog: stale heartbeat age=${age}s (limit ${STALE}s) $(date -u)" >> "$LOG"
      kill_session
      start_session
    elif [ "$note" = "cycle_start" ] && [ "$age" -gt "$HUNG" ]; then
      echo "watchdog: hung cycle (cycle_start age=${age}s, limit ${HUNG}s) $(date -u)" >> "$LOG"
      kill_session
      start_session
    fi
  fi
  sleep "$INTERVAL"
done
