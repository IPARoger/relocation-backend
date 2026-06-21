# A2A-MOTION-1 Closeout

**Date:** 2026-06-21  
**Scope:** Instantaneous applying / separating / exact / unknown on canonical aspect rows. No forecasting, perfection logic, or transit prediction.

---

## Summary

`canonical_chart.aspects_to_angles[]` and `canonical_chart.aspects_planet_to_planet[]` now include Layer-1 motion fields derived from existing planet speeds (`RETRO-MOTION-1`) and a short forward sample for relocated angle speeds (A2A only). When motion cannot be determined truthfully — especially at station — rows emit `motion: "unknown"`.

---

## Files changed

| File | Change |
|------|--------|
| `main_centerline_FIXER.py` | Motion helpers; A2A + P2P row fields; angle speed sample; `jd` passed into `build_canonical_chart_v1` |
| `settings/astrology_settings_defaults.json` | `exact_aspect_threshold_deg: 0.5` |
| `services/account_settings_resolver.py` | Resolve `exact_aspect_threshold_deg` in effective settings |
| `scripts/smoke_a2a_motion.py` | Static, unit, and TestClient validation (14 checks) |

**Not in scope:** A/S table coloring, wheel glyphs, `show_applying_separating_color` setting, perfection / ephemeris search.

---

## Schema additions (per aspect row)

Added to **both** `aspects_to_angles[]` and `aspects_planet_to_planet[]`:

| Field | Type | Meaning |
|-------|------|---------|
| `exact` | boolean | `separation_deg <= exact_aspect_threshold_deg` |
| `applying` | boolean | Instantaneous separation decreasing |
| `separating` | boolean | Instantaneous separation increasing |
| `motion` | string | `applying` \| `separating` \| `exact` \| `unknown` |

**Invariants:**

- `motion === "exact"` ⇒ `exact === true`, `applying === false`, `separating === false`
- `motion === "applying"` ⇒ `applying === true`, `separating === false`, `exact === false`
- `motion === "separating"` ⇒ `separating === true`, `applying === false`, `exact === false`
- `motion === "unknown"` ⇒ `applying === false`, `separating === false` (exact may still be true if within threshold)

Existing fields (`separation_deg`, `orb_limit_deg`, `in_orb`, `out_of_sign`, planet/angle keys) unchanged.

---

## Formulas used

### Separation from exact (unchanged)

```
signed_sep = normalize_deg(planet_lon - target_lon)   # (-180, 180]
separation_deg = abs(abs(signed_sep) - aspect_target_deg)
```

Major aspects use `_ASPECT_TARGET_DEG`; P2P uses `_P2P_ASPECT_TARGET_DEG`.

### Exact

```
exact = separation_deg <= exact_aspect_threshold_deg
```

Default threshold **0.5°** from `settings/astrology_settings_defaults.json` (`exact_aspect_threshold_deg`).

### Applying / separating (instantaneous v1)

Forward sample over **`ASPECT_MOTION_SAMPLE_DAYS = 1.0`** day:

```
lon_a_future = (lon_a + speed_a * dt) mod 360
lon_b_future = (lon_b + speed_b * dt) mod 360
separation_future = separation_from_exact(lon_a_future, lon_b_future, aspect)
```

| Condition | `motion` |
|-----------|----------|
| `exact` | `exact` |
| `separation_future < separation_now - ε` | `applying` |
| `separation_future > separation_now + ε` | `separating` |
| otherwise | `unknown` |

`ε = 1e-9` degrees (`_ASPECT_MOTION_DERIVATIVE_EPSILON_DEG`).

### Speed inputs

| Context | Body A speed | Body B speed |
|---------|--------------|--------------|
| **A2A** | Planet `speed_deg_per_day` from Swiss Ephemeris | Relocated angle speed from `swe.houses(jd)` vs `swe.houses(jd + 1 day)` at `(lat, lon)` |
| **P2P** | `speed_deg_per_day` planet A | `speed_deg_per_day` planet B |

P2P motion is **location-invariant** (birth instant). A2A motion is **location-dependent** (angles rotate with relocation).

---

## Station handling

Uses existing planet classification (`STATION_THRESHOLD_DEG_PER_DAY = 0.05`):

| Case | Policy |
|------|--------|
| **P2P:** either planet `station === true` | `motion: "unknown"` — do not guess applying/separating |
| **P2P:** missing `speed_deg_per_day` | `motion: "unknown"` |
| **A2A:** planet `station === true` | `motion: "unknown"` |
| **A2A:** angle | No station flag; angle speed from house rotation sample |
| **Derivative ≈ 0** (not exact) | `motion: "unknown"` — covers stagnation near exact without claiming direction |
| **Exact within threshold** | `motion: "exact"` even if a body is station |

**Documented limitation:** Instantaneous applying does **not** imply the aspect will perfect; no perfection / transit forecast is computed.

**Fixture:** NYC 1990-03-15 — Pluto `station_retrograde` ⇒ all Pluto P2P rows `motion: "unknown"`.

---

## Validation

`venv/bin/python scripts/smoke_a2a_motion.py` — **14/14 PASS**

| Check | Result |
|-------|--------|
| Static wiring (helpers, defaults) | PASS |
| Unit: applying / separating / exact / station→unknown | PASS |
| `/relocated-chart` A2A rows have motion fields | PASS (8 rows) |
| `/relocated-chart` P2P rows have motion fields | PASS (19 rows) |
| `motion` enum + boolean consistency | PASS |
| Pluto station → unknown on P2P | PASS |

---

## Future limitations

1. **No UI coloring** — blue/red/green A/S display and `show_applying_separating_color` setting deferred.
2. **No perfection field** — `perfecting: true/false/unknown` requires bounded ephemeris search (out of scope).
3. **No transit prediction** — speeds at birth instant only.
4. **Station on one P2P body** blocks motion for that row — conservative per doctrine.
5. **1-day sample** — sufficient for v1 derivative; sub-day sampling not exposed as setting.
6. **Angle speeds** — numeric sample, not analytic house-rotation formula.
7. **Display surfaces** — A2A/P2P tables do not yet render `motion` column (data available on canonical rows).

---

## Rollback scope

Revert A2A-MOTION-1 commit. Aspect rows lose the four motion fields; planet motion fields (`RETRO-MOTION-1`) and all other canonical structure unchanged. Remove `exact_aspect_threshold_deg` from defaults if fully reverting settings slice.

---

## Commit

```
A2A-MOTION-1: add applying separating exact on canonical aspects
```
