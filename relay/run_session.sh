#!/bin/bash
# 24/7 relay session — set RELAY_SESSION_HOURS=0 for unlimited.
cd "$(dirname "$0")/.."
set +e

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

HOURS="${RELAY_SESSION_HOURS:-0}"
if [ "$HOURS" = "0" ]; then
  END=4102444800
  LABEL="24/7 (no end)"
else
  END=$(( $(date +%s) + HOURS * 3600 ))
  LABEL="${HOURS}h"
fi

echo "=== relay session start $(date -u) pid=$$ ($LABEL, cycle_timeout=${RELAY_CYCLE_TIMEOUT:-2700}s) ===" >> relay/handoffs/session.log

while [ $(date +%s) -lt $END ]; do
  python3 -u relay/run_cycle.py
  code=$?
  if [ $code -eq 124 ]; then
    sleep 30
  elif [ $code -ne 0 ]; then
    sleep 60
  else
    sleep 10
  fi
done
echo "=== relay session end $(date -u) ===" >> relay/handoffs/session.log
