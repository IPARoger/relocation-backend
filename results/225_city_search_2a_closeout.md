# 225 — CITY-SEARCH-2A Closeout

**Date:** 2026-06-22  
**Ticket:** CITY-SEARCH-2A  
**Plan:** `results/214_city_search_phase2_plan.md` Phase 2A only  
**Status:** **DONE** (2B alias prefix + 2C short-circuit deferred)

---

## Summary

Added **generated stored** normalized search columns on `places`, btree + `text_pattern_ops` indexes, and rewrote RPC branches **1, 2, 4, 5** in `search_places_ranked_fast` and `search_places_ranked` to compare indexed columns instead of per-row `normalize_place_alias_text()`.

No UX redesign. Country-first unchanged (fallback only). Primary search remains type city → see city.

---

## Schema changes

**Migration:** `supabase/migrations/2026_06_23_search_places_phase2a.sql`  
**Applied:** `supabase db query --linked -f …` (staging)

| Column | Definition |
|--------|------------|
| `normalized_canonical` | `GENERATED ALWAYS AS (normalize_place_alias_text(canonical_name)) STORED` |
| `normalized_display_primary` | `GENERATED ALWAYS AS (normalize_place_alias_text(split_part(display_name, ',', 1))) STORED` |

| Index | Purpose |
|-------|---------|
| `places_normalized_canonical_idx` | exact match |
| `places_normalized_canonical_prefix_idx` | `text_pattern_ops` prefix |
| `places_normalized_display_primary_idx` | exact match |
| `places_normalized_display_primary_prefix_idx` | prefix |

RPC branches **3** (exact alias) and **6** (prefix alias) unchanged — Phase **2B** target.

---

## Code changes

| File | Change |
|------|--------|
| `supabase/migrations/2026_06_23_search_places_phase2a.sql` | columns, indexes, RPC rewrite |
| `repositories/places_repository.py` | `search_places(..., use_cache=True)` for benchmark `nocache` |
| `main_centerline_FIXER.py` | `GET /places/search?nocache=1` bypasses 180s TTL |
| `scripts/benchmark_city_search.py` | first-hit benchmark helper |
| `scripts/smoke_city_search_phase2a.py` | static migration smoke (10 checks) |

---

## Before / after timings

**Method:** `search_places(q, 10, use_cache=False)` against linked Supabase staging (PostgREST + staged RPC), 2026-06-22 after migration apply.

**BEFORE** = CITY-SEARCH-PERF-1 / Phase-2 plan baselines (`results/204_*`, `results/214_*`) — uncached first-hit band **~3–9 s**.

| Query | BEFORE (ms) | AFTER 2A (ms) | Δ | n | Notes |
|-------|------------:|--------------:|---|--:|-------|
| **London** | 9030 / 4338 | **4610** | −49% vs 9030 | 10 | Places branches faster; **alias prefix seq scan (branch 6) still dominates** |
| **Paris** | 5720 / 3358 | **513** | **−85%** | 10 | Fast tier fills limit; near target |
| **Kyoto** | 3904 | **1072** | −73% | 10 | Fallback may still run when underfill |
| **New York** | 3453 / 2971 | **1044** | −70% | 7 | Partial fast fill |
| **Ubud** | 6951 / 2953 | **978** | −86% vs 6951 | 1 | Rare name; fallback path |

### RPC `search_places_ranked_fast` only (DB tier, post-2A)

| Query | RPC ms | n |
|-------|-------:|--:|
| London | 1173 | 10 |
| Paris | 401 | 10 |
| Kyoto | 405 | 1 |
| New York | 394 | 5 |
| Ubud | 408 | 1 |

Places-indexed branches no longer seq-scan 68k rows with per-row normalize. **London** residual latency is branch 6 (`place_aliases` prefix seq scan) + UNION overhead — matches plan prediction (**2B + 2C** needed for <500 ms London).

---

## Validation

```text
python3 scripts/smoke_city_search_phase2a.py
10/10 passed
```

---

## Deferred (not 2A)

| Phase | Work |
|-------|------|
| **2B** | Prefix alias range query for index use |
| **2C** | SQL tier short-circuit (stop when limit met) |
| **2D** | pg_trgm fallback for contains |

---

## Rollback

1. Restore prior RPC bodies from `2026_06_22_search_places_staged.sql`
2. `ALTER TABLE places DROP COLUMN IF EXISTS normalized_canonical, DROP COLUMN IF EXISTS normalized_display_primary;` (drops dependent indexes)

---

**Primary search unchanged:** type city → see city. No country-first requirement added.
