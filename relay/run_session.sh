#!/bin/bash
cd "$(dirname "$0")/.."
set -a
[ -f .env.local ] && source .env.local
[ -f .env ] && source .env
set +a
export ANTHROPIC_MODEL="${ANTHROPIC_MODEL:-claude-sonnet-4-6}"
END=$(( $(date +%s) + 7200 ))
echo "=== relay session start $(date -u) ===" >> relay/handoffs/session.log
while [ $(date +%s) -lt $END ]; do
  python3 -u scripts/relay_robot.py --once 2>&1 | tee -a relay/handoffs/session.log
  code=${PIPESTATUS[0]}
  echo "=== cycle exit $code at $(date -u) ===" >> relay/handoffs/session.log
  [ $code -ne 0 ] && sleep 30
  sleep 5
done
echo "=== relay session end $(date -u) ===" >> relay/handoffs/session.log
