# Phase 2.3 — Saved Investigation Replay

## Purpose

Phase 2.3 turns the existing saved-view scaffold into a saved-investigation scaffold.

Phase 2.2 could reopen a library chart at a saved viewport, but the interpretive inquiry itself was still missing. Phase 2.3 captures and replays the semantic map inquiry under the existing saved-view endpoint without changing renderer behavior, astrology math, account/auth scope, or visual/aesthetic systems.

## Saved Investigation Definition

A saved investigation is:

- chart identity,
- semantic inquiry conditions,
- viewport/display context.

It is not a frozen renderer execution, a graphic artifact, or a saved relocated chart for one destination city.

## Persisted State

Saved investigations are stored inside the existing saved-view `conditions` field as a versioned object:

- `schema_version`
- `kind: "saved_investigation"`
- `chart_id`
- normalized planet-in-house conditions by UI slot
- optional angle-in-sign condition
- current aspect-to-angle overlay intent
- viewport center, zoom, and bounds through the existing saved-view viewport fields
- existing saved-view label and notes fields

This preserves user intent and where the user was looking.

## Explicitly Not Persisted

Phase 2.3 intentionally does not persist:

- renderer substrate,
- debug flags,
- resolution settings,
- full renderer request payload,
- Leaflet layers,
- polygons, lines, raster cells, or canvas output,
- aura, virga, or raindrop output,
- cache state,
- smoke/debug diagnostics,
- implementation-specific execution state.

Renderer execution remains environment-controlled.

## Replay Behavior

Opening `/map_CURRENT.html?skipOnboarding=1#libraryActive=<chart_id>&view=<view_id>` now:

1. restores the library chart selection when the chart is available,
2. restores the saved semantic inquiry controls,
3. restores the saved viewport center/zoom,
4. leaves the map renderer inert.

Replay does not click or invoke `Find regions`, does not call `/search-regions`, and does not draw overlay layers. The user must explicitly press `Find regions` to execute the inquiry.

## Renderer Behavior

Production renderer defaults are unchanged.

The active production substrate remains `legacy_search_regions`. Canonical/debug/adaptive/aura paths remain controlled by their existing environment, URL, and debug gates. Phase 2.3 does not alter astrology math, renderer theory, cache doctrine, or visual/aesthetic doctrine.

## Validation

Targeted validation was run sequentially:

```bash
./venv/bin/python scripts/smoke_library_scaffold.py
```

Result: `all_pass: true`

```bash
./venv/bin/python scripts/smoke_library_handoff.py
```

Result: `all_pass: true`

The smokes verify:

- saved-investigation semantic conditions round-trip,
- viewport round-trips,
- replay restores controls and viewport,
- replay does not auto-render,
- `rendererSubstrate` remains `legacy_search_regions`,
- renderer/debug metadata is not persisted in the saved condition object.

Note: the library smokes must run sequentially. They share and reset `library/library.json`, so parallel execution can create false failures through local scaffold persistence contention.

## Risk Classification

- **Trust risk resolved:** shared map links now preserve interpretive inquiry semantics, not only camera position.
- **Deferred excellence:** durable account-backed storage, migration tooling, ACL/share permissions, and formal saved-investigation product UI remain future platform work.
- **Rejected scope:** persisting graphic artifacts, renderer substrate, debug flags, aura/virga/raindrop output, or full renderer request payload as durable product truth.
- **No-op:** renderer behavior, astrology math, accounts/auth, payments, and aesthetics remain unchanged.

## Rollback Scope

Rollback is limited to:

- `map_CURRENT.html`
- `scripts/smoke_library_scaffold.py`
- `scripts/smoke_library_handoff.py`
- this narrative
- optionally the saved-object taxonomy note in `docs/relocation_app_product_roadmap.md`

No renderer math, backend astrology logic, account/auth system, or visual/aesthetic system is involved.

## Governance Closeout

- **Deferred Excellence:** no new registry item is required. The existing saved-view condition replay trust gap has been implemented; permanent storage and sharing governance remain known future-platform concerns.
- **Rendering Doctrine:** no update required because renderer behavior and default substrate did not change.
- **Validation Narrative:** this file records the Phase 2.3 behavior, validation, risks, and rollback scope.
- **Next recommendation:** commit Phase 2.3 as a focused saved-investigation replay checkpoint, then decide whether to proceed to product UI polish, account/auth direction, or persistence architecture planning.
