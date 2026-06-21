# RETRO-MOTION-1 — Speed, Retrograde, and Station Truth Closeout

**Date:** 2026-06-21  
**Commit:** (pending) — `RETRO-MOTION-1: add speed retrograde and station truth`  
**Depends on:** P2P-ASPECTS-1 (`5cc9dd7`), SETTINGS-SOURCE-1 (`4f5ecbc`)

---

## Summary

`canonical_chart.planets` now includes server-sourced **motion truth** from existing `swe.calc_ut` longitude speed (`pos[0][3]`). No wheel glyphs, applying/separating, or display settings were added.

---

## Files changed

| File | Change |
|------|--------|
| `main_centerline_FIXER.py` | `STATION_THRESHOLD_DEG_PER_DAY`, `_planet_motion_from_speed()`; speed capture in `/relocated-chart`; motion fields on canonical planets |
| `scripts/smoke_settings_account.py` | Five `be_motion_*` backend checks |
| `scripts/smoke_comparison_sets.py` | `static_motion_*` (3) — no client motion wiring |

---

## Exact fields added (per planet)

```json
{
  "longitude_deg": 227.6174,
  "sign": "scorpio",
  "house": 7,
  "near_cusp": false,
  "speed_deg_per_day": -0.013616,
  "retrograde": true,
  "station": true,
  "motion_state": "station_retrograde"
}
```

| Field | Type | Definition |
|-------|------|------------|
| `speed_deg_per_day` | number | Signed ecliptic longitude speed from Swiss Ephemeris (`deg/day`) |
| `retrograde` | boolean | `speed_deg_per_day < 0` |
| `station` | boolean | `abs(speed_deg_per_day) <= STATION_THRESHOLD_DEG_PER_DAY` |
| `motion_state` | string | `direct` \| `retrograde` \| `station_direct` \| `station_retrograde` |

**`motion_state` rules (current speed only, no forecasting):**

| Condition | `motion_state` |
|-----------|----------------|
| `abs(speed) <= threshold` and `speed >= 0` | `station_direct` |
| `abs(speed) <= threshold` and `speed < 0` | `station_retrograde` |
| `speed < -threshold` | `retrograde` |
| `speed > threshold` | `direct` |

---

## Station threshold

**`STATION_THRESHOLD_DEG_PER_DAY = 0.05`**

Bodies with absolute longitude speed ≤ **0.05°/day** are classified as **station** at the birth instant. Threshold is a backend constant (not a user setting in this slice). Future display settings may expose it.

---

## Settings

None. Motion is astronomical fact at compute time — not gated behind visibility or display toggles.

---

## Validation results

| Check | Result |
|-------|--------|
| TestClient: all 11 planets have motion fields | **PASS** |
| `retrograde` matches `speed_deg_per_day < 0` | **PASS** |
| `motion_state` enum populated | **PASS** |
| Pluto on NYC 1990-03-15 fixture: `station` + `station_retrograde` | **PASS** (`|speed| ≈ 0.014°/day`) |
| `_planet_motion_from_speed` at ±0.01°/day | **PASS** (`station_direct` / `station_retrograde`) |
| `static_motion_*` (3) — no client wiring | **PASS** |
| Legacy `planet_houses` + existing canonical fields | **Unchanged** |

---

## Known limitations

1. **Station threshold is fixed** at 0.05°/day — not yet user-configurable.
2. **Speed at speed == 0** classifies as `station_direct` (non-negative branch).
3. **No applying/separating/exact** on aspects — deferred to A2A-MOTION-1.
4. **No wheel retrograde/station glyphs** — display slice not started.
5. **Nodes** not included — out of scope.
6. **Relocation invariance:** speeds are birth-instant facts (identical across relocated charts for same Chart Record).

---

## Rollback scope

Revert RETRO-MOTION-1 commit. `canonical_chart.planets` loses the four motion fields; `planet_houses` legacy may still carry `speed_deg_per_day` in internal dict until a broader revert — consumers of legacy mirror are unchanged.

---

*RETRO-MOTION-1 complete. Next: A2A-MOTION-1 (applying/separating/exact on aspect rows).*
