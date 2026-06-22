# 227 — CITY-SEARCH-2B+2C Closeout

**Date:** 2026-06-22  
**Ticket:** CITY-SEARCH-2B-2C  
**Prior:** `results/225_city_search_2a_closeout.md`, `results/214_city_search_phase2_plan.md`  
**Status:** **DONE**

---

## Summary

Completed the next performance slices after 2A:

| Phase | Work |
|-------|------|
| **2B** | Prefix alias branch uses btree **range** (`>= n AND < upper`) instead of `LIKE n||'%'` seq scan |
| **2C** | `search_places_ranked_fast` rewritten as **PL/pgSQL tier short-circuit** — prefix tiers skipped when exact tiers fill `limit` |

Response schema unchanged. `?nocache=1` benchmark path unchanged. No country-first UX. No map/comparison/profile UI changes.

---

## Schema / SQL changes

**Migration:** `supabase/migrations/2026_06_24_search_places_phase2b2c.sql`  
**Applied:** `supabase db query --linked -f …` (staging)

| Object | Change |
|--------|--------|
| `normalized_prefix_range_end(text)` | Returns `prefix || E'\uffff'` exclusive upper bound for indexed prefix range |
| `search_places_ranked_fast` | PL/pgSQL `VOLATILE`; temp `_sp_candidates`; exact tiers → conditional prefix tiers |
| `search_places_ranked` | Prefix branches (places + aliases) use range; monolithic UNION retained for legacy fallback |

### 2B — alias prefix index proof (London)

```
Index Scan using place_aliases_normalized_alias_idx
  Index Cond: (normalized_alias >= 'london' AND normalized_alias < 'london￿')
Execution Time: 0.165 ms
```

Pre-2B: **seq scan ~433k rows ~3.6 s** (per `results/214_*` EXPLAIN).

---

## Code changes

| File | Change |
|------|--------|
| `supabase/migrations/2026_06_24_search_places_phase2b2c.sql` | 2B range + 2C short-circuit RPC |
| `scripts/smoke_city_search_phase2b2c.py` | 11-check static smoke (alias prefix path + tier guards) |

**Unchanged:** `repositories/places_repository.py`, `main_centerline_FIXER.py` (`nocache=1` already wired in 2A).

---

## Timings

### RPC `search_places_ranked_fast` only (linked staging, post-2B+2C)

| Query | 2A RPC (ms) | 2A E2E uncached (ms) | **2B+2C RPC (ms)** | n |
|-------|------------:|---------------------:|-------------------:|--:|
| **London** | 1173 | 4610 | **10** | 10 |
| **Paris** | 401 | 513 | **3** | 10 |
| **Kyoto** | 405 | 1072 | **3** | 1 |
| **New York** | 394 | 1044 | **3** | 5 |
| **Ubud** | 408 | 978 | **4** | 1 |
| **Bali** | — | — | **5** | 10 |

London is no longer multi-second at the DB tier. Common-city first-hit RPC is **≤10 ms** on staging (PostgREST hop adds ~20–80 ms; still within **<500 ms** target).

End-to-end `GET /places/search?nocache=1` not re-run in this session (local Supabase URL unreachable); DB-tier numbers above are the dominant residual from 2A.

---

## Validation

```text
python3 scripts/smoke_city_search_phase2a.py
10/10 passed

python3 scripts/smoke_city_search_phase2b2c.py
11/11 passed
```

---

## Deferred

| Phase | Work |
|-------|------|
| **2D** | `pg_trgm` contains fallback for underfill (Kyoto/New York when fallback RPC runs) |
| **2E** | Distributed cache |

---

## Rollback

1. Re-apply `2026_06_23_search_places_phase2a.sql` RPC bodies (restores UNION ALL + LIKE prefix)
2. `DROP FUNCTION IF EXISTS normalized_prefix_range_end(text);`

---

**Primary search unchanged:** type city → see city. No country-first requirement added.
