# RESULT: 15_IN_SHELL_MAP_ROUTE_CLEANUP_AUDIT

Task: `15_IN_SHELL_MAP_ROUTE_CLEANUP_AUDIT`
Mode: read-only audit; documentation output only
Result: **VERIFIED**

## Files inspected

- `app_shell.html`
- `audits/05_frontend_placeholder_honesty_audit.md`
- `results/14_screen4_action_honesty_fix.md`

## Answers

1. **Reachability:** not via primary nav (that uses `openMap()` -> production map). Reachable via Screen 4 `Back to shell map` buttons (`data-nav="map"`, lines 1365/1397) and a direct `route=map` hash. `mountGenieDrawer()` is tied to `route === "map"`.
2. **screenMap() shows:** `Screen 2 — Map Discovery` heading + `Primary instrument` purpose; an honest `production-map` module that says the real map opens in the main tool with an `Open production map` handoff button; a Genie drawer placeholder; a `map-actions` panel (`Full chart`, `Compare places`, `Export / share status`, disabled `Save exploration (auto-save stub)`, `Back to Chart Record page`); debug + must-not notes. A computed `conditions` draft variable exists but is not rendered.
3. **Implies it is the real map?** Only in framing: `Screen 2 — Map Discovery` / `Primary instrument` oversells it. No fake map is rendered; the handoff button is honest.
4. **"Back to shell map" honest enough?** Yes — it names the shell route explicitly. `Back to map launcher` would be marginally clearer but is optional.
5. **Keep / rename / remove?** Reframe now as a context/launcher page; consider removal later (removal needs redirecting the Screen 4 back buttons and direct hash, which is bigger than a copy fix).
6. **Smallest safe fix:** copy-only reframe of the heading/purpose so it does not claim to be the primary map; optional `Back to map launcher` relabel; optional removal of the unused `conditions` draft variable.

## Scope verification

- No production files modified.
- No backend, schema, database, renderer, or map logic changed.
- Full detail in `audits/15_in_shell_map_route_cleanup_audit.md`.

VERIFIED
