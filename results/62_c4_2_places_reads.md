# RESULT: 62_c4_2_places_reads

**Roadmap ID:** C4-2
**Author:** Cursor (manual copy-paste track)
**Date:** 2026-06-17 UTC

## M2 — geonames_id lookup (~line 2394)

**STOP — not replaced.** `GET /places/search` accepts only `?q=` (display_name ILIKE); backend has no `geonames_id` query param. The M2 block is a deterministic Supabase lookup by `geonames_id` with a fallback to the display_name search route already present. Replacing it would require a new `GET /places?geonames_id=` backend route (out of C4-2 scope).

The existing fallback in the same block (`GET /places/search?q=displayName`) is already a JWT route call — no Supabase in that path.

**Recommendation:** Add `geonames_id` param to `GET /places/search` or `GET /places` in a separate small task, then C4-2 M2 can be completed.

## M5 — handoff centering (~lines 6246–6264)

**Replaced.** Removed Supabase client dependency; replaced with `GET /place/{id}` (8004, already exists).

### Before (lines 6246–6264)
```js
async function centerOnHandoffPlaceId() {
    const pid = lastAppShellHandoff && lastAppShellHandoff.placeId;
    if (!pid) return;
    if (lastAppShellHandoff && lastAppShellHandoff.explorationId) return;
    const sbClient = window.SupabaseClient || (window.SupabaseReady ? await window.SupabaseReady : null) || window._supabaseClient;
    if (!sbClient) return;
    try {
        const { data: places } = await sbClient
            .from("places")
            .select("id, display_name, latitude, longitude")
            .eq("id", pid)
            .limit(1);
        const pl = Array.isArray(places) && places[0];
        if (!pl) return;
        await openSavedPlace(pl.display_name, pl.latitude, pl.longitude);
    } catch (err) {
        console.error("[saved-places-handoff]", err);
    }
}
```

### After
```js
async function centerOnHandoffPlaceId() {
    const pid = lastAppShellHandoff && lastAppShellHandoff.placeId;
    if (!pid) return;
    if (lastAppShellHandoff && lastAppShellHandoff.explorationId) return;
    try {
        const resp = await fetch(`${API_BASE}/place/${encodeURIComponent(pid)}`);
        if (!resp.ok) return;
        const pl = await resp.json();
        if (!pl || !pl.id) return;
        await openSavedPlace(pl.display_name, pl.latitude, pl.longitude);
    } catch (err) {
        console.error("[saved-places-handoff]", err);
    }
}
```

Field mapping: `GET /place/{id}` returns `{id, display_name, latitude, longitude, ...}` — identical to the Supabase select fields. No field rename needed.

## Route confirmation grep

```
2538:@app.get("/places/search")
2545:@app.get("/place/{place_id}")
```

Both routes confirmed in `main_centerline_FIXER.py`.

## Smoke result

```
{"overall_pass": true, ...}
exit=0
```

## Status

**PARTIALLY VERIFIED**

- M5 (handoff centering): **VERIFIED** — Supabase SELECT removed, `GET /place/{id}` used, smoke passes
- M2 (geonames_id lookup): **NOT REPLACED** — backend route has no `geonames_id` param; requires backend change first
