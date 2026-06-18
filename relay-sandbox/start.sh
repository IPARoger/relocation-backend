#!/bin/bash
cd "$(dirname "$0")/.."
# shellcheck source=env.sh
. "$(dirname "$0")/env.sh"
export RELAY_SANDBOX_TARGET="${RELAY_SANDBOX_TARGET:-10}"
export RELAY_SANDBOX_MIN_ELAPSED_SEC="${RELAY_SANDBOX_MIN_ELAPSED_SEC:-3600}"
export RELAY_SANDBOX_MOCK="${RELAY_SANDBOX_MOCK:-0}"
export RELAY_SANDBOX_FRESH="${RELAY_SANDBOX_FRESH:-1}"
export RELAY_SANDBOX_PROGRESS_SEC="${RELAY_SANDBOX_PROGRESS_SEC:-600}"
python3 relay-sandbox/launch_detached.py supervisor
echo "monitor: tail -f relay-sandbox/handoffs/session.log"
