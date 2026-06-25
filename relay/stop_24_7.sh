#!/bin/bash
# Stop relay watchdog, session, and caffeinate.
cd "$(dirname "$0")/.."
launchctl bootout "gui/$(id -u)/com.relocation.relay" 2>/dev/null || true
pkill -f "relay/run_cycle.py" 2>/dev/null
pkill -f "relay_robot.py" 2>/dev/null
pkill -f "relay/watchdog.sh" 2>/dev/null
if [ -f relay/handoffs/caffeinate.pid ]; then
  kill "$(cat relay/handoffs/caffeinate.pid)" 2>/dev/null
  rm -f relay/handoffs/caffeinate.pid
fi
pkill -f "caffeinate.*relay" 2>/dev/null
if [ -f relay/handoffs/watchdog.pid ]; then
  kill "$(cat relay/handoffs/watchdog.pid)" 2>/dev/null
  rm -f relay/handoffs/watchdog.pid relay/handoffs/session.pid
fi
echo "relay stopped — Mac can sleep normally"
