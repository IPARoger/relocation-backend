# Phase-2 Cache Protocol — Implementation Notes

> **Status:** Product-substrate prototype (sandbox).
> **Doctrine:** `docs/relocation_map_architecture.md` § "Phase 2 cache priority protocol".
> **Sandbox:** `/map_SANDBOX_phase2_cache.html`

## What was built

A client-side **single-active-job scheduler** with:

- `AbortController` per fetch (hard cancel on user interrupt)
- `Map` cache with canonical JSON keys (chart + bounds + zoom + conditions)
- Priority queue A→H registered after first successful user paint
- `PHASE2.cachePaused` gate so `_maybeStartNext()` cannot run after map interaction
- Budget counter (`233_118` samples) with `deferred` status when exceeded
- H-priority transits registered as `deferred_inactive` (date-mode-gated)

## Protocol mapping

| Doctrine rule | Code location |
|---------------|---------------|
| First paint = user only | `requestUser()` → `SCHEDULER.serveUser(userJob)` before background |
| Interrupt on zoom/pan | `onUserAction` on `movestart` / `zoomstart` |
| No half-cached entries | Cache `.set()` only after full `fetch` resolves; abort drops result |
| Priority A→H | `registerBackgroundJobs()` enqueue order |
| H conditional on date | `deferred_inactive` row; `setDateModeActive(true)` to enable (future UI) |
| Budget | `PHASE2_BUDGET = 233_118` in sandbox |
| No mouse prediction | Not implemented (by design) |

## Smoke test

```bash
./venv/bin/python scripts/smoke_phase2_cache.py
```

Output: `validation/reports/phase2_cache_smoke.json`

Latest run: **all_pass: true** (7 tests).

## Known limitations (gaps)

1. **Not in `map_CURRENT.html`** — prototype sandbox only.
2. **D jobs split** — planet-in-house warm-up is one job per planet per house-half (6 conditions max per call). Full doctrine D is ~20 sequential jobs; cancellation can interrupt mid-D.
3. **E job placeholder signs** — angle-in-sign cache uses placeholder signs; production must cache actual relocated signs per cell.
4. **Synthetic zoom/pan grids** — A/B/C priorities use `map.project` / `unproject` at synthetic zoom without moving the map (correct for cache-only warm-up).
5. **No server persistence** — cache dies on page reload.
6. **Interior zoom reuse** — not implemented; every zoom still re-classifies in this sandbox.

## Next product steps

1. Extract scheduler into `static/phase2_cache_scheduler.js` (or equivalent) shared by product map.
2. Wire `map_CURRENT.html` map events to `onUserAction`.
3. Connect date-mode UI to `setDateModeActive`.
4. Add server-side optional cache keyed by `(profile_id, bounds_hash, zoom, condition_set_hash)` when session persistence is required.
