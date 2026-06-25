#!/bin/bash
# One-shot: install cron safety net + start relay now.
set -e
REPO="/Users/davegoodman/Desktop/relocation-backend"
MARK="# relocation-relay-ensure"
CRON_LINE="*/2 * * * * $REPO/relay/ensure_running.sh"
( crontab -l 2>/dev/null | grep -v "$MARK" || true
  echo "$CRON_LINE $MARK"
) | crontab -
echo "Installed cron (every 2 min): $CRON_LINE"
"$REPO/relay/stop_24_7.sh" 2>/dev/null || true
"$REPO/relay/start_24_7.sh"
sleep 2
if [ -f "$REPO/relay/handoffs/watchdog.pid" ] && kill -0 "$(cat "$REPO/relay/handoffs/watchdog.pid")" 2>/dev/null; then
  echo "OK watchdog pid $(cat "$REPO/relay/handoffs/watchdog.pid")"
else
  echo "FAIL watchdog not running" >&2
  exit 1
fi
