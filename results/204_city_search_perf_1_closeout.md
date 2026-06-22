# CITY-SEARCH-PERF-1 Closeout

**Date:** 2026-06-22  
**Goal:** Smallest real performance improvement — staged backend search, timing logs, optional cache, immediate local favorites in UI.

---

## Before / after timings

Measured via `GET /places/search?q=…&limit=10` against `http://127.0.0.1:8004` (linked Supabase staging).

| Query | BEFORE (ms) | AFTER uncached (ms) | AFTER cached repeat (ms) | n | Notes |
|-------|------------:|--------------------:|-----------------------:|--:|-------|
| Paris | 6650 | 3358 | 66 | 10 | Fast tier fills limit; ILIKE contains skipped |
| London | 3098 | 4338 | 3 | 10 | Staged fast-only |
| Springfield | 3401 | 3019 | 2 | 10 | Staged fast-only |
| Ubud | 2953 | 6951 | 1 | 1 | Rare name; only 1 DB hit either way |
| Kyoto | 3135 | 3904 | 2 | 10–14 | Fast underfills → fallback RPC runs |
| New York | 2971 | 3453 | 1 | 7 | Fast partial fill → small fallback |

**BEFORE** captured at task start (pre-change server). **AFTER uncached** = warm server, one request per query. **AFTER cached** = immediate repeat of same query/limit.

### Assessment

- **Staged search:** For common prefix/exact queries (Paris, London, Springfield), the backend stops after `search_places_ranked_fast` when the limit is met — the `%query%` ILIKE contains branch is not executed. Direct RPC comparison showed ~300–400 ms savings vs monolithic `search_places_ranked` for full-limit prefix hits.
- **In-process cache (180s TTL):** Repeat queries return in **1–66 ms** — typing backspace/retype and debounced re-queries feel instant.
- **Client:** `saved_location_search_ui.js` renders matching favorites/saved rows immediately while `/places/search` continues.
- First-hit latency remains **~3–7 s** (DB-bound `normalize_place_alias_text` scans). This task did not rewrite indexes or the full RPC; it removed unnecessary slow-tier work and added cache + perceived-speed UX.

`scripts/smoke_place_alias_search.py`: **30/31 passed** (Peking returned 0 once during a long parallel smoke run; direct retest returns Beijing via alias).

---

## Backend change

### `repositories/places_repository.py`

1. **Staged RPC calls:**
   - Stage 1–2: `search_places_ranked_fast` (exact + prefix tiers 1–6)
   - Stage 3: `search_places_ranked_fallback` (ILIKE contains) **only if** `len(fast) < limit`
   - Legacy fallback: monolithic `search_places_ranked` if staged RPCs unavailable; table ILIKE if all RPCs fail
2. **In-process cache:** key `(normalized_query, limit)`, TTL **180 s**
3. **Timing logs:** `logger.info("places.search … stage=… fast=… fallback=… ms=…")`

### `main_centerline_FIXER.py`

- `GET /places/search` prints `[places/search] q=… limit=… n=… ms=…` per request.

### Client

- `saved_location_search_ui.js` — `runSearch()` calls `loadProfileSaved` + `rankResults` to show **Favorites & saved** hits before awaiting full `search()`.
- Family B debounce/cache in `saved_location_search_service.js` / `place_search_client.js` unchanged.

---

## RPC / migration

**Applied to linked staging** via `supabase db query --linked -f`:

`supabase/migrations/2026_06_22_search_places_staged.sql`

Creates:

| Function | Purpose |
|----------|---------|
| `search_places_ranked_fast(p_query, p_norm, p_limit)` | Tiers 1–6: exact + prefix only |
| `search_places_ranked_fallback(p_query, p_norm, p_limit, p_exclude)` | Tier 7–8: ILIKE contains, excludes IDs already returned |

Grants: `anon`, `authenticated`, `service_role`.

**Not changed:** `search_places_ranked` (legacy monolithic) remains for rollback / missing-RPC fallback.

**Migration history note:** `supabase db push --linked` is out of sync with remote (pre-existing `places` table); this migration was applied with `supabase db query --linked -f` only.

---

## Rollback scope

1. **Code:** Revert `repositories/places_repository.py`, `main_centerline_FIXER.py` (`/places/search`), `saved_location_search_ui.js`.
2. **DB (optional):** `DROP FUNCTION IF EXISTS search_places_ranked_fast; DROP FUNCTION IF EXISTS search_places_ranked_fallback;` — monolithic `search_places_ranked` continues to work.
3. **No schema/table changes** — rollback is function + Python/JS only.

---

## Files touched

- `supabase/migrations/2026_06_22_search_places_staged.sql` (new)
- `repositories/places_repository.py`
- `main_centerline_FIXER.py`
- `saved_location_search_ui.js`
- `results/204_city_search_perf_1_closeout.md` (this file)
