#!/bin/bash
cd "$(dirname "$0")/.."
launchctl bootout "gui/$(id -u)/com.relocation.relay" 2>/dev/null || true
for f in supervisor.pid watchdog.pid session.pid caffeinate.pid; do
  [ -f "relay/handoffs/$f" ] && kill "$(cat relay/handoffs/$f)" 2>/dev/null
  rm -f "relay/handoffs/$f"
done
pkill -f "relay/watchdog.sh" 2>/dev/null
pkill -f "relay/run_session.sh" 2>/dev/null
pkill -f "relay/run_cycle.py" 2>/dev/null
pkill -f "relay_robot.py" 2>/dev/null
pkill -f "relay_executor.py" 2>/dev/null
pkill -f "caffeinate.*relay" 2>/dev/null
echo "relay stopped"
