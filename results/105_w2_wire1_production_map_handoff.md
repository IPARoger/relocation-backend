# W2-WIRE-1 — Production map handoff

**Status:** Complete  
**Scope:** `app_shell.html`, `scripts/smoke_app_shell_map_handoff.py`  
**Commit message (if requested):** `W2-WIRE-1: route shell map entries to production map`

## Goal

End the in-shell `#/map` dead-end. All map navigation should open `map_CURRENT.html` with `chartRecordId` (and related context) via `buildMapHandoffUrl`.

## Changes

### `app_shell.html`

1. **`buildMapHandoffFromPatch(patch)`** — test/smoke helper to build handoff URLs without redirecting.
2. **`openMap()`** — falls back `chartRecordId` to `viewModel.selectedChartRecordId` / `defaultChartRecordId`; preserves `explorationId` from nav context; accepts `source` / `notice`.
3. **`navigate()`** — intercepts `route === "map"` → merges context → `openMap()` (no `#/map` hash render).
4. **`render()`** — direct `#/map` bookmarks redirect via `openMap()` before painting placeholder.
5. **`compare-back-map`** — `returnTo.route === "map"` uses `openMap()` instead of in-shell navigate.
6. **`screenMap()`** — quarantined fallback (“Opening map…”) if redirect race; removed misleading “Save exploration (auto-save stub)”.
7. **Copy** — “Back to shell map” → “Back to map”; nav label → “Screen 2 — Map (production)”.

### `scripts/smoke_app_shell_map_handoff.py`

- Default `BASE_URL` → `8004`.
- URL-building journeys use `buildMapHandoffFromPatch` (stay on shell).
- New check: `navigate_map_redirects_production`.

## Entry points (all → production map)

| Entry | Mechanism |
|-------|-----------|
| Primary nav “2 Map” | `openMap()` (unchanged) |
| `data-nav="map"` (Screen 4/5 back) | `navigate("map")` intercept |
| `data-action` open-map-* / resume-exploration | `openMap()` (unchanged) |
| Guided onboarding launch | `openMap()` (unchanged) |
| Compare → back to map (no returnTo) | `openMap()` (unchanged) |
| Compare → back to map (returnTo map) | `openMap()` (fixed) |
| Direct `#/map` URL | `render()` redirect |
| Popup `data-nav="map"` | `navigate()` intercept |

## Validation

```bash
set -a && source .env.staging && set +a
venv/bin/python scripts/smoke_app_shell_map_handoff.py   # PASS (15 checks)
venv/bin/python scripts/smoke_map_current.py             # PASS
```

## Not in scope

Backend, renderer, comparison logic, settings, notes, export/share, place alias search.
