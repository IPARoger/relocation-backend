# Phase 2.2 — Saved-View Replay + Shareable Map Deep Links

Date: 2026-05-22

## Scope

Phase 2.2 adds one product seam: a saved library view can reopen
`map_CURRENT.html` with the saved chart selected and the Leaflet camera
restored. It does not run the renderer, alter astrology math, change the
production substrate, or expand into auth/payments.

This phase builds on Phase 2.1's library handoff:

```text
/map_CURRENT.html?skipOnboarding=1#libraryActive=<chart_id>&view=<view_id>
```

The hash is intentionally client-side. It avoids backend route changes,
keeps the link inspectable, and preserves the existing product boundary:
library state supplies metadata, while the map remains responsible for
displaying its own Leaflet viewport.

## Deep-Link Contract

The first map deep-link contract is:

```text
/map_CURRENT.html?skipOnboarding=1#libraryActive=<chart_id>&view=<view_id>
```

Meaning:

* `libraryActive=<chart_id>` identifies the saved library chart.
* `view=<view_id>` identifies a saved viewport row belonging to that
  chart.
* `skipOnboarding=1` keeps shared links from showing the starter overlay.
* The map fetches `/library/state`, validates that both ids exist, and
  only replays the view if the view belongs to the chart.

The existing chart-library share contract remains intact:

```text
/library.html?chart=<chart_id>
```

That URL still shares the library chart/dashboard context. The new map
URL shares a concrete camera position for professional/client handoff.

## What Replays Now

`map_CURRENT.html` now reads:

* `#libraryActive=<chart_id>` (preferred over session storage)
* `sessionStorage.rm_library_active` (fallback)
* `#view=<view_id>`

After `loadChartProfiles()`:

1. Built-in chart profiles are populated exactly as before.
2. If a library handoff id exists, only the matching library chart is
   appended to the existing `#chartProfile` selector.
3. The selector value is set to the library chart id without dispatching
   a `change` event.
4. If a `view` id is present and belongs to that chart, the saved
   viewport is applied with `window.__rmMap.setView(..., { animate:
   false })`.

Viewport replay prefers saved `center_lat` / `center_lon` plus `zoom`.
If center fields are missing, it falls back to the midpoint of saved
bounds. Invalid or mismatched ids fail closed and are reported through
`window.__rmLibraryHandoff()` without changing renderer state.

## Library Share Links

`library.html` now exposes each saved view in the chart list and provides
a "Copy map link" action for each view. The helper exposed for smoke and
future UI work is:

```text
window.__rmLibrary.mapViewUrl(view)
```

It returns:

```text
<origin>/map_CURRENT.html?skipOnboarding=1#libraryActive=<chart_id>&view=<view_id>
```

The older `window.__rmLibrary.shareUrl(chartId)` still returns:

```text
<origin>/library.html?chart=<chart_id>
```

## What Remains Stubbed

* Saved-view `conditions` remain `[]`. Phase 2.2 deliberately did not
  capture or replay planet/house/sign/aspect controls, because that is a
  second instability source. This is now recorded in
  `docs/DEFERRED_EXCELLENCE_REGISTRY.md` as **4.5a Saved-view condition
  replay**.
* No saved view auto-runs "Find regions." Replayed links restore chart
  selection and camera only; the user must invoke the existing renderer
  action.
* No auth, ACL, client permissions, expiration, or payment gating.
* The map-deep-link contract assumes local `/library/state` for now.
  Account-backed ids can replace local ids later without changing the
  hash shape.

## Renderer Doctrine Preserved

Renderer behavior is unchanged:

* `ACTIVE_RENDERER_SUBSTRATE` remains `legacy_search_regions`.
* Canonical renderer remains debug-only.
* No astrology calculations changed.
* No `findRegions()` call is introduced by handoff or view replay.
* No `change` event is dispatched after setting `#chartProfile`.
* View replay only calls Leaflet camera APIs (`setView`) and does not
  touch polygon layers, aspect layers, aura layers, substrate adapters,
  cache policy, or truth endpoints.

The deep-link smoke verifies `rendererSubstrate:
"legacy_search_regions"`, `polygonLayers: 0`, and `renderStatus:
"Ready."` after opening a saved-view URL.

## Smoke Results

All relevant smokes passed from a cold library state:

| Smoke | Result |
| --- | --- |
| `scripts/smoke_library_handoff.py` | `all_pass: True` |
| `scripts/smoke_library_scaffold.py` | `all_pass: True` |
| `scripts/smoke_phase2_cache.py` | `all_pass: True` |
| `scripts/smoke_map_current.py` | `overall_pass: True` |
| `scripts/smoke_substrate_adapter.py` | `all_pass: True` |

The handoff smoke now covers Phase 2.2:

1. Create a library chart.
2. Save a view from `map_CURRENT.html`.
3. Open
   `/map_CURRENT.html?skipOnboarding=1#libraryActive=<id>&view=<view_id>`.
4. Verify the chart selector picks the library chart.
5. Verify map center/zoom matches the saved viewport.
6. Verify `polygonLayers === 0` and render status remains `Ready.`
7. Verify `library.html` exposes both the existing chart share URL and
   the new saved-view map URL.

## Professional Sharing Impact

This is the first useful client-share artifact: a practitioner can save a
view and copy a URL that restores the same chart identity and map camera.
It is not yet a full professional deliverable because conditions, notes,
annotations, account identity, and permissions are still incomplete.

Even in this minimal form, it establishes the future contract:

* chart id selects whose chart is being discussed;
* view id selects where the discussion is anchored;
* later phases can add condition replay, notes, ACLs, and exports without
  changing the base URL shape.

## Recommended Next Phase

**Phase 2.3 — saved-view condition capture/replay ONLY.**

Capture the active planet/house/sign/angle/aspect controls into the
existing saved-view `conditions` field and replay those controls from a
deep link, still without auto-running `Find regions`. This removes the
main trust gap in Phase 2.2 share links: they restore the place but not
yet the interpretive context.
