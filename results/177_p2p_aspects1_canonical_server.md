# P2P-ASPECTS-1 — Canonical Planet-to-Planet Aspects Closeout

**Date:** 2026-06-21  
**Commit:** (pending) — `P2P-ASPECTS-1: add canonical planet-to-planet aspects`  
**Depends on:** SETTINGS-SOURCE-1 (`4f5ecbc`)

---

## Summary

`canonical_chart` now includes server-computed **`aspects_planet_to_planet[]`** for future wheel spokes. No client rendering, tables, or comparison outputs were added.

---

## Files changed

| File | Change |
|------|--------|
| `main_centerline_FIXER.py` | P2P aspect targets/order; `_compute_aspects_planet_to_planet`; field on `build_canonical_chart_v1` |
| `services/account_settings_resolver.py` | `chart_display_orb_limit()` for major/minor chart-display orbs |
| `scripts/smoke_settings_account.py` | Six `be_p2p_*` backend checks |
| `scripts/smoke_comparison_sets.py` | `static_p2p_*` (3) — no client P2P math/tables/spokes |

---

## Exact schema

```json
"aspects_planet_to_planet": [
  {
    "body_a": "Chiron",
    "body_b": "Moon",
    "aspect": "trine",
    "separation_deg": 0.82,
    "orb_limit_deg": 8.0,
    "in_orb": true,
    "out_of_sign": false
  }
]
```

| Field | Type | Notes |
|-------|------|-------|
| `body_a` | string | Lexicographically smaller canonical body name |
| `body_b` | string | Lexicographically larger canonical body name |
| `aspect` | string | Major or enabled minor aspect id |
| `separation_deg` | number | Degrees from exact aspect |
| `orb_limit_deg` | number | From `major_aspect_orbs` or `minor_aspect_orbs` |
| `in_orb` | boolean | Always `true` when row emitted |
| `out_of_sign` | boolean | Sign-gate per `_ASPECT_SIGN_MODULO` (majors) |

**Pair policy:** Each unordered pair once; no self-aspects; bodies filtered by `_body_visible`.

**Aspect order:** Majors (`conjunction`, `opposition`, `square`, `trine`, `sextile`) then minors in UI order (`quincunx` … `novile`) when enabled.

---

## Settings honored (via `effective_settings` from SETTINGS-SOURCE-1)

| Setting | P2P use |
|---------|---------|
| `visible_planets` | Core body inclusion |
| `visible_bodies` | Chiron inclusion |
| `visible_major_aspects` | Major aspect types computed |
| `visible_minor_aspects` | Master switch for minors |
| `visible_minor_aspects_list` | Which minors computed |
| `major_aspect_orbs` | Major `orb_limit_deg` |
| `minor_aspect_orbs` | Minor `orb_limit_deg` |
| `out_of_sign_aspects` | Sign-gate inclusion |

**Not used for P2P:** `aspect_to_angle_orbs` (A2A-only).

---

## Validation results

| Check | Result |
|-------|--------|
| TestClient `/relocated-chart` has `aspects_planet_to_planet` | **PASS** (19 rows on NYC fixture) |
| Row schema + `body_a < body_b` | **PASS** |
| Major orb tight vs wide | **PASS** |
| Disable square in `visible_major_aspects` | **PASS** |
| Chiron off via non-empty `visible_bodies` without `chiron` | **PASS** |
| Minors only when `visible_minor_aspects` + list | **PASS** (with `out_of_sign_aspects: true` for quincunx on fixture) |
| `aspect_to_angle_orbs` does not change P2P `orb_limit_deg` | **PASS** |
| `static_p2p_*` (3) | **PASS** |
| `be_p2p_*` in `smoke_settings_account.py` | Added before Playwright (requires Supabase) |

---

## Known limitations

1. **Minor out-of-sign:** `_ASPECT_SIGN_MODULO` is defined for majors only. Minors are treated as out-of-sign unless `out_of_sign_aspects` is true (backend-ready; UI toggle still disabled).
2. **Location invariance:** P2P rows are recomputed per `/relocated-chart` call (longitudes are relocation-invariant; harmless duplication).
3. **No wheel spokes, tables, motion, or applying/separating** — by design this slice.
4. **`septile` / `novile` orbs:** Fall back to registry `minor_aspect_orbs` defaults when not in user settings.

---

## Rollback scope

Revert P2P-ASPECTS-1 commit. `canonical_chart` loses `aspects_planet_to_planet`; all other fields and consumers unchanged.

---

*P2P-ASPECTS-1 complete. Next: WHEEL-v2 spokes renderer.*
