#!/bin/bash
# Install macOS LaunchAgent so relay survives sleep/wake and terminal close.
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PLIST_SRC="$REPO/relay/com.relocation.relay.plist.template"
PLIST_DST="$HOME/Library/LaunchAgents/com.relocation.relay.plist"
sed "s|REPO_PLACEHOLDER|$REPO|g" "$PLIST_SRC" > "$PLIST_DST"
launchctl bootout "gui/$(id -u)/com.relocation.relay" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_DST"
launchctl enable "gui/$(id -u)/com.relocation.relay"
launchctl kickstart -k "gui/$(id -u)/com.relocation.relay"
echo "Installed LaunchAgent: $PLIST_DST"
echo "Logs: $REPO/relay/handoffs/launchd.log"
