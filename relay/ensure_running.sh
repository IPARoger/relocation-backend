#!/bin/bash
# Cron/login safety net: restart relay watchdog if it died.
REPO="/Users/davegoodman/Desktop/relocation-backend"
cd "$REPO" || exit 0
WPID="$REPO/relay/handoffs/watchdog.pid"
if [ -f "$WPID" ] && kill -0 "$(cat "$WPID" 2>/dev/null)" 2>/dev/null; then
  exit 0
fi
echo "ensure_running: restarting watchdog $(date -u)" >> "$REPO/relay/handoffs/ensure.log"
exec "$REPO/relay/start_24_7.sh" >> "$REPO/relay/handoffs/ensure.log" 2>&1
