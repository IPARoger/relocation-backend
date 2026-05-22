# Phase 2.1 — Library-to-Map Handoff + Onboarding (Wire-Through Only)

## Scope

Wire the Phase 2.0 chart-library scaffold into `map_CURRENT.html` at the
lowest-risk product seam. This phase deliberately introduces **one** new
instability source: the chart-profile selector can be populated and
pre-selected from a library handoff. Everything else — renderer
substrate, astrology math, lat-cap policy, raster/adaptive aura paths,
Phase-2 cache doctrine — is untouched.

The work is reversible. Disabling the feature flag (`RM_PHASE2_LIBRARY=0`,
already off by default in production) makes `/library/state` return 404,
the handoff logic falls through to its no-op branch, and the renderer
behaves exactly as it did before Phase 2.0.

## What was wired

### Map handoff in `map_CURRENT.html`

* New helper `readActiveLibraryChartIdFromUrlOrSession()` reads
  `#libraryActive=<id>` first, then `sessionStorage.rm_library_active`.
  Source provenance (`"hash"` vs `"sessionStorage"`) is preserved for
  diagnostics.
* `fetchLibraryStateSafe()` GETs `/library/state` and silently no-ops on
  any non-200 response. Renderer behavior is unchanged when the library
  flag is off.
* `loadChartProfiles()` was extended in two strictly additive ways:
  * It still fetches `/chart-profiles` and populates the built-in
    options exactly as before.
  * If — and only if — there is an active handoff id, it fetches the
    library state and appends **only that one** library chart as an
    additional `<option>` with `data-library-source="1"` and a
    `[library] <Name>` label. No other library charts are merged into
    the dropdown. This preserves the existing renderer smoke's exact
    expected profile list for the no-handoff path.
* `applyLibraryActiveSelection()` finds the matching `<option>` and sets
  `select.value = handoff.id` after profiles load. **No `change` event
  is dispatched** — selection is inert until the user (or an existing
  control flow) chooses to act. This guarantees no auto-render or auto
  re-fetch.
* The session storage value is rewritten only on a successful match, so
  bad hash payloads can't poison the active selection.

### Library launch from `library.html`

`library.html` already wrote `sessionStorage.rm_library_active` and
opened `/map_CURRENT.html?skipOnboarding=1#libraryActive=<id>` from
the per-chart "Open in Map" action. The Phase 2.0 placeholder copy was
updated to reflect that the map now actually consumes the handoff.

### Save current view to library

`map_CURRENT.html` exposes a small "Save current view to library" button
in the panel (rendered only when an active library chart is selected).
It calls `window.__rmSaveCurrentViewToLibrary()`, which POSTs the
Leaflet bounds, center, and zoom plus the active chart id to
`/library/views`. No renderer state, no overlay, no map redraw — purely
a metadata POST. Failures surface in a small status line; successful
saves echo the new view id.

### Onboarding bridge

When `/library/state` responds 200, the existing panel exposes:

* "Open Chart Library" link (always shown while library is reachable).
* "Save current view to library" button (shown only when the active
  selection came from a library chart).

The link is small, sits below `Find regions` so it cannot push the
primary action out of the viewport, and is hidden entirely when the
flag is off.

## Diagnostic surface

`window.__rmLibraryHandoff()` returns:

```
{
  libraryAvailable: bool,
  libraryChartCount: number,
  activeLibraryChartId: string | null,
  activeLibraryChartSource: string | null,
  selectionAppliedFrom: "hash" | "sessionStorage" | null,
  selectionAppliedId: string | null
}
```

The same object is now embedded inside `window.__rmSmokeState()` under
the `libraryHandoff` key so the existing smoke surface can observe the
state without scraping the DOM.

## Files changed

* `map_CURRENT.html` — new library handoff CSS block, library-handoff
  panel fragment placed below `Find regions`, `loadChartProfiles()`
  extended, new helpers (`fetchLibraryStateSafe`,
  `readActiveLibraryChartIdFromUrlOrSession`,
  `applyLibraryActiveSelection`, `renderLibraryHandoffUI`,
  `saveCurrentViewToLibrary`), `__rmSmokeState` augmented with
  `libraryHandoff`.
* `library.html` — doctrine note refreshed; "Open in Map" toast copy
  updated to reflect Phase 2.1 wiring.
* `scripts/smoke_library_handoff.py` — **new** smoke covering the full
  handoff round-trip (library state → create chart → hash handoff →
  sessionStorage handoff → save view → library state observes the saved
  view → baseline path with no handoff is unchanged).
* `validation/narratives/phase2_1_library_map_handoff.md` — this file.

## Renderer doctrine preserved

* `ACTIVE_RENDERER_SUBSTRATE` stays `legacy_search_regions`; the
  smoke result confirms `rendererSubstrate: "legacy_search_regions"`
  in both the hash and sessionStorage handoff paths.
* `loadChartProfiles()` retains the **exact** label list expected by
  `scripts/smoke_map_current.py` when no handoff is present, because
  library charts are only injected on demand.
* No `change` event is dispatched after `select.value = id`, so no
  existing listener fires and no overlay re-renders. The user (or test)
  must click `Find regions` for the substrate to react, exactly as
  before.
* Astrology math, lat-cap defaults, canonical visible debug, Phase-2
  cache budgets, and the raster/adaptive aura debug paths are
  unmodified.
* The new endpoints all live under `/library/*`, are gated by
  `_ensure_library_enabled()`, and have no side effects on
  `/chart-profiles`, `/find-regions`, `/screen-pixel-truth`, or any
  other production surface.

## Smoke results

All four relevant smokes are green from a cold start with
`library/library.json` removed before each run.

| Smoke | Result |
| --- | --- |
| `scripts/smoke_library_handoff.py` (new, 7 checks) | **all_pass: True** |
| `scripts/smoke_map_current.py` | **overall_pass: True** |
| `scripts/smoke_library_scaffold.py` | **all_pass: True** |
| `scripts/smoke_phase2_cache.py` | **all_pass: True** |
| `scripts/smoke_substrate_adapter.py` | **all_pass: True** |

The new handoff smoke specifically asserts:

1. `/library/state` reachable with library flag on.
2. Library chart created with a deterministic `lib_chart_*` id.
3. Hash handoff (`#libraryActive=<id>`) selects the library chart in
   the existing `#chartProfile` dropdown, sets
   `selectionAppliedFrom: "hash"`, exposes the new "Save current view"
   button, and emits no console errors.
4. SessionStorage handoff (no hash) achieves the same outcome with
   `selectionAppliedFrom: "sessionStorage"`.
5. "Save current view to library" POSTs a viewport payload that the
   backend persists with a fresh `lib_view_*` id and the correct
   `chart_id`.
6. The persisted `/library/state.views[]` array contains the saved view
   and the active chart pointer survives.
7. The baseline path (no hash, no storage) still surfaces only the
   built-in chart profiles and the substrate stays legacy.

## What remains stubbed

* The map does **not** auto-trigger `findRegions()` after applying the
  handoff. The user must press the existing button. This is intentional
  — it keeps the renderer surface inert and matches the brief.
* `Save current view to library` records bounds/center/zoom only; the
  conditions list (planet/house/sign/angle/aspect inputs) is sent as
  `[]`. Wiring the active condition set into the saved view is a
  Phase 2.2 candidate.
* "Open Chart Library" link is the entire onboarding affordance. A
  proper onboarding flow (empty-state coaching, sample charts, etc.)
  is deferred per the Deferred Excellence Registry.
* Library charts are not yet visible inside the map's chart-profile
  dropdown unless they are the active handoff target. A future phase
  can merge all library charts after the renderer smoke's exact-list
  assertion is loosened — that smoke change is intentionally deferred.
* Shareable URLs still point at `/library.html?chart=<id>`. Direct deep
  links into `/map_CURRENT.html?...#libraryActive=<id>` for sharing are
  a Phase 2.2 candidate.
* No auth, no client accounts, no payment, no multi-device sync. The
  library file remains local JSON.

## How this prepares for account / client sharing

* The hash + sessionStorage handoff contract is now exercised end to
  end. Replacing the local id with a remote account-scoped id only
  changes the source of `chart.id`; the wire-through code stays the
  same.
* `saved view` rows now carry `{chart_id, viewport, conditions, notes}`
  per Phase 2.0's schema. A client-share export can serialize them
  directly.
* The `__rmLibraryHandoff` diagnostic surface gives later phases an
  observable seam to add analytics, share-link telemetry, and
  account-based gating without re-instrumenting the chart selector.

## Recommended next Phase 2.x step

**Phase 2.2 — Saved view replay + shareable map deep links.**
Wire `/library/views` rows so that opening `library.html`, picking a
chart, and choosing a saved view restores the map's center/zoom and
optionally re-applies the saved condition set. Then move the share URL
contract from `/library.html?chart=<id>` to
`/map_CURRENT.html?skipOnboarding=1#libraryActive=<id>&view=<view_id>`,
which gives professional clients a one-click "show me the map you saw"
artifact without requiring accounts yet.

The follow-up to that is **Phase 2.3 — minimal account stub** (local
"who am I" identity that can later swap in for a real auth backend),
which unblocks per-user library separation and the client-export work
mentioned in the Deferred Excellence Registry.
