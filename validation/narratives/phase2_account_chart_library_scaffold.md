# Phase 2.0 — Account + Chart-Library Scaffold

Date: 2026-05-22. Product scaffolding only. Renderer doctrine preserved.

## Scope

Phase 1.19 declared the renderer MVP-ready on `legacy_search_regions`. Phase 2.0 begins Web 2 product scaffolding so that account, library, favorites, share, and (future) client features can land without re-opening the rendering substrate.

This is scaffold-only:

- Renderer behavior unchanged. `map_CURRENT.html` is not modified.
- Astrology math unchanged.
- Canonical renderer remains debug-only.
- No aura, raindrop, or virga work.
- Existing smoke suites continue to gate regressions.

## Product Scaffold Now Available

| Surface | What exists |
|---------|-------------|
| Dashboard page | `library.html` (served at `/library.html`). Lists saved charts, save/edit form, view-save stub, settings placeholder, share URL copy. |
| Persisted model | Reuses the existing chart-profile shape (`id`, `name`, `date`, `time`, `timezone`, `place`, `lat`, `lon`, `notes`) plus a `favorite` flag and a derived `share_url`. |
| Library state | `GET /library/state` returns `{schema_version, charts, views, favorites, active_chart_id, settings}`. |
| Chart CRUD | `POST /library/charts` (upsert), `DELETE /library/charts/{id}`. |
| Favorites | `POST /library/charts/{id}/favorite` with `{favorite: bool}`; favorites list mirrored in state. |
| Active selection | `POST /library/active` with `{chart_id}` validates that the chart exists. |
| View metadata stub | `POST /library/views` saves viewport + condition slot list + label per chart. |
| Settings stub | `PUT /library/settings` patches `default_substrate`, `lat_cap_label_enabled`, `phase2_cache_enabled`, `experimental_mode_enabled`. |
| Share URL | Each chart record returns `share_url = "/library.html?chart=<id>"`; library page deep-links into the saved record. |
| Test hooks | `window.__rmLibrary.{state, reload, saveChart, favoriteChart, deleteChart, setActive, saveView, saveSettings, shareUrl}`. |

### Feature-Flag Isolation

The entire scaffold lives behind `RM_PHASE2_LIBRARY` (default `1`). When set to `0`, all `/library/*` routes — including the page — return 404. This guarantees the scaffold is opt-out and never co-located with renderer behavior.

## Persistence Choice

Local file persistence at `library/library.json` with `schema_version: 1`. Each write is a single atomic `json.dump` against the same file. The file is git-ignored (`library/library.json`, `library/library.*.json`) so user data never enters version control.

This satisfies the brief’s preference for "simple local JSON / lightweight backend file storage". It avoids:

- introducing an auth provider,
- introducing a database,
- introducing payments,
- coupling to client-sharing infrastructure.

The shape is forward-compatible: an account-backed sync layer can be added later by reading and writing the same JSON keys per user.

## UI Entry Point

`/library.html` is the dashboard. Open in a browser with the backend running:

```
http://127.0.0.1:8000/library.html
```

Deep-link to a saved chart:

```
http://127.0.0.1:8000/library.html?chart=<chart_id>
```

The page is intentionally plain: no map, no canvas, no aura, no animation. It is a sober list/form/settings panel so future React/Next migration can lift the contract without aesthetic debt.

## Share URL Contract

| Field | Value |
|-------|-------|
| Path | `/library.html` |
| Query | `?chart=<chart_id>` |
| Record-attached | Every chart returns `share_url = "/library.html?chart=<chart_id>"` |
| Map entry | `/map_CURRENT.html?skipOnboarding=1#libraryActive=<chart_id>` (handoff only — auto-select inside the map is intentionally Phase 2.1). |
| Persistence | Library writes `sessionStorage.rm_library_active` so a future map handoff can read it without touching the renderer today. |

`library.html` reads `?chart=` on load and populates the edit form with the matching record. The map remains responsible for selecting the chart via its existing dropdown until Phase 2.1.

## What Remains Stubbed

| Item | Status |
|------|--------|
| Auto-select chart inside `map_CURRENT.html` | **Stub.** Library writes `sessionStorage.rm_library_active` and the URL hash; the renderer is not modified. Phase 2.1 will wire the handoff. |
| Save current map view from the map UI | **Stub.** Library exposes a view-save form; capturing live map state from `map_CURRENT.html` is deferred. |
| Authentication / accounts | **Stub.** No login; single-tenant local file. |
| Payments | **Stub.** No billing surface. |
| Client sharing (professional mode) | **Stub.** Share URL exists; client-side ACL is deferred. |
| Multi-device sync | **Stub.** Local JSON only. |
| Settings effects on renderer | **Stub.** Settings persist but do not alter rendering. |

## How This Preserves Renderer Doctrine

1. `map_CURRENT.html` is untouched: `git diff --stat map_CURRENT.html` shows no Phase 2.0 changes.
2. Production substrate stays `legacy_search_regions`. The settings stub records the user’s preference but does not switch substrates.
3. Lat-cap policy and on-screen label remain shipped behavior.
4. Phase-2 cache doctrine remains documented; the settings toggle does not wire it in.
5. Canonical substrate stays debug-only behind `?canonicalDryRun`/`?canonicalVisible` flags.
6. Astrology math endpoints (`/screen-pixel-truth`, `/aura-*`, `/search-regions`, `/relocated-chart`, …) are not touched.
7. Existing smokes continue to gate regressions.

## Validation

All four smoke gates pass after Phase 2.0:

| Smoke | Result |
|-------|--------|
| `scripts/smoke_library_scaffold.py` (new) | **12/12 pass** |
| `scripts/smoke_substrate_adapter.py` | **14/14 pass** |
| `scripts/smoke_phase2_cache.py` | **pass** |
| `scripts/smoke_map_current.py` | **pass** |

The library smoke validates: feature flag observable, library state shape, chart upsert + share URL contract, favorite toggle persistence, active selection round-trip, view save with chart linkage, settings PATCH semantics, `/chart-profiles` still served, `library.html` served with documented `window.__rmLibrary` hooks, dashboard JS loads without console errors, and delete cleans dependents (favorites, active, views).

## Files Changed

| File | Role |
|------|------|
| `main_centerline_FIXER.py` | Added `/library.html`, `/library/state`, `/library/charts*`, `/library/active`, `/library/views`, `/library/settings` + Pydantic models + file persistence helpers. Guarded by `RM_PHASE2_LIBRARY`. |
| `library.html` (new) | Dashboard scaffold page with chart list, save/edit form, view-save stub, settings stub, share URL copy, and `window.__rmLibrary` hooks. |
| `library/.gitkeep` (new) | Reserves persistence folder. |
| `.gitignore` | Adds `library/library.json` and `library/library.*.json`. |
| `scripts/smoke_library_scaffold.py` (new) | 12-test scaffold smoke. |
| `validation/narratives/phase2_account_chart_library_scaffold.md` (this file) | Phase 2.0 narrative. |

No renderer files were modified. No astrology engine files were modified.

## How This Prepares For Accounts / Payments / Client Sharing

- The `library/library.json` shape is the unit that a future account sync layer will adopt verbatim. Each user’s library JSON can be stored against a user record without changing the API surface.
- `share_url` is already attached to every chart record, ready to become an ACL-checked endpoint when client sharing lands.
- The `settings.experimental_mode_enabled` slot is the documented place for narrow-orb/high-lat advanced gating, satisfying the Phase 1.19 doctrine.
- The feature flag `RM_PHASE2_LIBRARY` lets a payment/account migration kill-switch the scaffold without touching the renderer.
- `window.__rmLibrary` exposes a small, stable contract that a React/Next port can target.

## Recommended Next Product Phase

**Phase 2.1 — map_CURRENT handoff + onboarding flow.**

Scope:

1. Add a tiny, isolated handler inside `map_CURRENT.html` that reads `sessionStorage.rm_library_active` (or the URL hash `#libraryActive=<id>`) and selects the matching chart in the existing dropdown. **No renderer changes.** This is purely a `<select>` value assignment that runs after the existing `loadChartProfiles()`.
2. Add a “Save current map view to library” action in the map sidebar that POSTs to `/library/views` using the existing chart dropdown selection and current Leaflet bounds. Still no astrology math change.
3. Provide a minimal onboarding redirect: if `sessionStorage.rm_library_active` is empty and `RM_PHASE2_LIBRARY=1`, link the user to `/library.html`.
4. Extend `smoke_library_scaffold.py` to validate the handoff after the dropdown selection.

This stays inside the anti-death-spiral doctrine: every Phase 2.1 task removes a named product-trust risk (orphaned active selection, missing live view capture, onboarding gap) without re-opening rendering.

## Decision

Phase 2.0 is complete and isolated. Phase 2.1 should be the smallest viable handoff wire-in; anything beyond that (auth, payments, sync, sharing) belongs to dedicated, narrowly scoped product phases.
