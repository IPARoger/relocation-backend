#!/bin/bash
# Extended soak: 10 consecutive OK cycles + 1h minimum, real executor (no mock).
set -euo pipefail
cd "$(dirname "$0")/.."
export RELAY_SANDBOX_TARGET=10
export RELAY_SANDBOX_MIN_ELAPSED_SEC=3600
export RELAY_SANDBOX_MOCK=0
export RELAY_SANDBOX_FRESH=1
export RELAY_SANDBOX_PROGRESS_SEC=600
export RELAY_SANDBOX_MONITOR_SEC=600
LOG=relay-sandbox/handoffs/session.log
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) soak.sh: starting extended soak (target=10, min=60min, mock=0)" >> "$LOG"
# Reset status for fresh 10/10
python3 - <<'PY'
import json, time
from datetime import datetime, timezone
from pathlib import Path
p = Path("relay-sandbox/handoffs/status.json")
p.write_text(json.dumps({
    "ok_streak": 0, "target": 10, "min_elapsed_min": 60,
    "elapsed_min": 0, "last_code": None, "last_error": None,
    "mock": "0", "note": "soak_reset", "updated": datetime.now(timezone.utc).isoformat(),
}, indent=2) + "\n")
PY
./relay-sandbox/start.sh
# Start monitor in background if not running
MONPID=relay-sandbox/handoffs/monitor.pid
if [ ! -f "$MONPID" ] || ! kill -0 "$(cat "$MONPID" 2>/dev/null)" 2>/dev/null; then
  nohup ./relay-sandbox/monitor.sh >> relay-sandbox/handoffs/monitor.log 2>&1 &
  echo $! > "$MONPID"
  echo "started monitor pid=$(cat "$MONPID")"
else
  echo "monitor already running pid=$(cat "$MONPID")"
fi
echo "Soak running. Watch: tail -f relay-sandbox/handoffs/session.log"
echo "Resume if stopped: RELAY_SANDBOX_FRESH=0 ./relay-sandbox/soak.sh"
