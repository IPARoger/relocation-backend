#!/usr/bin/env python3
"""
SET-4 smoke: Profile page settings propagation.

Checks (static, no server required):
  1. rehydrateSettingsConsumers includes chart-record branch calling hydrateProfileNatalFacts.
  2. rehydrateSettingsConsumers clears _profileCanonicalCache before re-hydrating.
  3. chart-record branch comes before chart branch (correct order).
  4. fetchCanonicalRelocatedChart reads resolveHouseProximityOrbDeg (live settings orb).
  5. resolveHouseProximityOrbDeg reads _settingsEff().
  6. hydrateProfileNatalFacts calls fetchCanonicalRelocatedChart (orb pass-through active).
"""

from pathlib import Path
import sys

shell = Path("app_shell.html").read_text()

checks = []

# 1 + 2 + 3: rehydrateSettingsConsumers body
rehydrate_start = shell.find("function rehydrateSettingsConsumers()")
rehydrate_end   = shell.find("\n}", rehydrate_start) + 2
rehydrate_body  = shell[rehydrate_start:rehydrate_end]

checks.append((
    "set4_chart_record_in_rehydrate",
    'navContext.route === "chart-record"' in rehydrate_body
    and "hydrateProfileNatalFacts()" in rehydrate_body,
    "rehydrateSettingsConsumers includes chart-record branch calling hydrateProfileNatalFacts",
))
checks.append((
    "set4_profile_cache_cleared",
    "_profileCanonicalCache = null" in rehydrate_body,
    "rehydrateSettingsConsumers clears _profileCanonicalCache before re-hydration",
))
cr_pos = rehydrate_body.find('"chart-record"')
c_pos  = rehydrate_body.find('"chart"')
checks.append((
    "set4_chart_record_before_chart",
    -1 < cr_pos < c_pos,
    "chart-record branch comes before chart branch in rehydrateSettingsConsumers",
))

# 4: fetchCanonicalRelocatedChart uses orb from settings
fetch_start = shell.find("async function fetchCanonicalRelocatedChart(")
fetch_end   = shell.find("\n}", fetch_start) + 2
fetch_body  = shell[fetch_start:fetch_end]
checks.append((
    "set4_orb_from_settings_in_fetch",
    "resolveHouseProximityOrbDeg()" in fetch_body and "house_proximity_orb" in fetch_body,
    "fetchCanonicalRelocatedChart reads resolveHouseProximityOrbDeg (picks up effective settings orb)",
))

# 5: resolveHouseProximityOrbDeg reads _settingsEff
resolve_start = shell.find("function resolveHouseProximityOrbDeg(")
resolve_end   = shell.find("\n}", resolve_start) + 2
resolve_body  = shell[resolve_start:resolve_end]
checks.append((
    "set4_resolve_orb_reads_settings",
    "_settingsEff()" in resolve_body,
    "resolveHouseProximityOrbDeg reads _settingsEff() — orb is live from account settings",
))

# 6: hydrateProfileNatalFacts calls fetchCanonicalRelocatedChart
hydrate_start = shell.find("async function hydrateProfileNatalFacts(")
hydrate_end   = shell.find("\nasync function ", hydrate_start + 1)
hydrate_body  = shell[hydrate_start:hydrate_end]
checks.append((
    "set4_profile_uses_fetch_canonical",
    "fetchCanonicalRelocatedChart(" in hydrate_body,
    "hydrateProfileNatalFacts calls fetchCanonicalRelocatedChart (orb pass-through active)",
))

passed = failed = 0
for name, result, label in checks:
    print(f"{'PASS' if result else 'FAIL'} {name}: {label}")
    if result: passed += 1
    else: failed += 1
print(f"\n{passed}/{len(checks)} passed")
import sys; sys.exit(0 if failed == 0 else 1)
