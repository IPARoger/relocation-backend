# W2-WIRE-2 — User QA Recovery Closeout

**Date:** 2026-06-19  
**Roadmap:** `results/104_web2_wiring_priority_plan.md`  
**Mode:** Implement in subslices (A–E)

---

## Subslice A verdict — Compare overlay basic functionality

**Status:** PASS

### Changes (`app_shell.html`, `scripts/smoke_comparison_sets.py`)

1. Top nav **5 Compare** now `navigate("compare")` first, then `openComparisonOverlayFromChrome()` (overlay appears over Compare screen).
2. `#comparisonOverlayModal` click delegation wired (Cancel, Compare, favorite picks, chip remove) — fixes Cancel not closing when buttons were outside `#main`.
3. Overlay **Favorites** list (`#comparisonOverlayFavorites`) with empty state copy per spec.
4. Family B search mount unchanged (`rm-cmp-overlay-loc-search`, placeholder `Search locations or favorites`, `includeTeaching: true`).
5. Modal CSS: higher z-index for search dropdown inside overlay.

### Validation

```
smoke_comparison_sets.py — PASS
  fe_overlay_on_compare_screen
  fe_overlay_family_b_placeholder
  fe_overlay_cancel_closes
  fe_overlay_compare_enabled
  fe_overlay_max_five
```

---

## Subslice B verdict — Map version truth audit (read-only)

**Status:** COMPLETE — **do not switch handoff target**

| Item | Finding |
|------|---------|
| **Current handoff target** | `map_CURRENT.html` (via `openMap()` / `buildMapHandoffUrl`) |
| **Candidate modern files** | `map_SANDBOX_genie_v6.html`, `map_SANDBOX_genie_v7.html` |
| **Genie / ghost / explore UI** | Present in sandbox HTML/CSS mockups only (`body.explore`, `.ghoststrip`, collapsed bottle UX) |
| **map_CURRENT.html has** | `#citySearch` Family B search, `#savedPlaces` dropdown, saved-investigation save/replay, `findBtn`, Genie render handoff adapter (dev panel), relocated-chart popup — **not** sandbox ghost-strip chrome |
| **Sandbox status** | Aesthetic/prototype layer — not wired to Supabase store bridge, favorites, comparison handoff |
| **Recommendation** | **Do not repoint handoff now.** Migrate sandbox chrome components into `map_CURRENT.html` incrementally when ready. |

### Feature matrix (summary)

| Feature | map_CURRENT.html | map_SANDBOX_genie_v7.html |
|---------|------------------|---------------------------|
| Production auth/store | Yes | No |
| Family B location search | Yes | Clickable mock only |
| Saved places dropdown | Yes | Mock |
| Saved investigation | Yes (backend) | No |
| Ghost / explore controls | No | Yes (CSS mockup) |
| Genie variable builder | Handoff adapter only | Visual mock |
| Relocated chart popup | Yes | Unknown/partial |

---

## Subslice C verdict — Favorite save/load loop

**Status:** PASS

### Changes (`map_CURRENT.html`)

1. `getActiveFavoriteProfileId()` — returns **visible** saved profile only (Supabase-tagged or UUID option); removed silent URL/session handoff fallback that could desync UI vs save target.
2. After favorite save, persists `rm_active_profile_id` in sessionStorage.
3. `loadSavedPlacesForActiveProfile()` — clearer errors for 401 / 404 vs generic failure.
4. Existing post-save `loadSavedPlacesForActiveProfile()` refresh retained.

### Validation

```
smoke_favorites.py — PASS (fe_map_save_new, fe_map_dropdown_refresh, fe_map_save_active)
```

---

## Subslice D verdict — Relocated chart entry from map popup

**Status:** PASS

### Changes (`map_CURRENT.html`)

1. Replaced disabled **Full chart coming soon** with **View relocated chart** button.
2. `openChartFromMapButton()` resolves place via `resolvePlaceFromMapSelection`, navigates to `app_shell.html#/chart?chartRecordId=…&placeId=…`.
3. Requires saved profile or handoff chart record; shows inline status if missing.

### Validation

- Wired to existing Screen 4 hydrate path (`hydrateRelocatedChart` uses `/relocated-chart` + engine birth).
- `smoke_map_current.py` PASS (popup open/close with dialog auto-accept for custom naming).

---

## Subslice E verdict — Custom location naming

**Status:** PASS

### Changes (`map_CURRENT.html`)

1. Right-click map: `promptCustomLocationName()` before popup (default `Custom location near {lat}, {lon}`).
2. Favorite on unnamed `map_custom` origin prompts for name before resolve/save.
3. Popup title uses user-provided name.

### Validation

- `smoke_map_current.py` — dialog auto-accept added for headless right-click path.

---

## Smoke summary (all required)

| Script | Result |
|--------|--------|
| `smoke_comparison_sets.py` | PASS |
| `smoke_favorites.py` | PASS |
| `smoke_map_current.py` | PASS |
| `smoke_app_shell_map_handoff.py` | PASS |

---

## Files touched

- `app_shell.html`
- `map_CURRENT.html`
- `scripts/smoke_comparison_sets.py`
- `scripts/smoke_map_current.py`
- `relay/ROADMAP_QUEUE.md`
- `results/106_w2_wire2_user_qa_recovery.md`
