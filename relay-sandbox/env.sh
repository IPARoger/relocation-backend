#!/bin/bash
# Sandbox-only relay environment (sourced by start.sh / soak.sh).
# Avoids Anthropic planner API calls — uses Cursor Auto for executor.

export RELAY_SANDBOX_SKIP_PLANNER="${RELAY_SANDBOX_SKIP_PLANNER:-1}"
export CURSOR_MODEL="${CURSOR_MODEL:-auto}"
export RELAY_AUTO_MODEL="${RELAY_AUTO_MODEL:-1}"
export RELAY_PUSH=0
