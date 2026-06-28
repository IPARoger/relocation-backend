#!/usr/bin/env bash
# Verify which Settings V3 implementation your local app_shell.html contains.
# Uses grep (no ripgrep required). Run from repo root on your Mac.
set -euo pipefail

FILE="${1:-app_shell.html}"
if [[ ! -f "$FILE" ]]; then
  echo "ERROR: $FILE not found" >&2
  exit 1
fi

echo "=== Settings V3 local verification ==="
echo "File: $FILE"
echo "MD5: $(md5 -q "$FILE" 2>/dev/null || md5sum "$FILE" | awk '{print $1}')"
echo "Size: $(wc -c < "$FILE") bytes"
echo

check() {
  local label="$1"
  local pattern="$2"
  local count
  count=$(grep -cE "$pattern" "$FILE" 2>/dev/null || true)
  if [[ "$count" -gt 0 ]]; then
    echo "  [YES] $label ($count)"
    grep -nE "$pattern" "$FILE" | head -3
  else
    echo "  [NO]  $label"
  fi
  echo
}

check "Rich sidebar (My Profiles)" 'My Profiles'
check "Settings V3 renderer" 'screenSettingsV3'
check "Table orbs grid (PR23 fix)" 'rm-sv3-oa-table'
check "Broken orbs grid (pre-23774db)" 'rm-sv3-oa-grid|display: contents'
check "Advanced Bodies section" 'Advanced Bodies'
check "Above-fold North Node" 'north_node.*North Node|North Node'
check "Above-fold South Node" 'south_node.*South Node|South Node'
check "External settings_v3 module" 'settings_v3/'

echo "=== Reference MD5 fingerprints ==="
echo "  origin/main (no settings-v3):     7501c89845c6d925d4cfc464ec7b1dfd"
echo "  PR #23 / 23774db (minimal sv3):   aa5d2e207aaa0e533c12d86e28c7f38d"
echo "  Your Mac (2026-06-25):            543021be2d111aebf4ac6bd942a1fd46"
echo
echo "If My Profiles=YES and rm-sv3-oa-table=NO → port PR23 fixes into YOUR file (see SETTINGS_V3_PORT_GUIDE.md)"
echo "If rm-sv3-oa-grid=YES → replace orbs CSS grid with rm-sv3-oa-table (broken in Chrome)"
