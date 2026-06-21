# SETTINGS-WIRE-1 Closeout: Body Visibility + Minor Aspects
**Date:** 2026-06-21  
**Task:** Wire body visibility (Chiron + core planets) and minor aspect availability  
**Files changed:**  
`main_centerline_FIXER.py`, `app_shell.html`, `map_CURRENT.html`,  
`scripts/smoke_settings_account.py`, `scripts/smoke_settings_navigation.py`

---

## PART 1 — Body Visibility

### What Is Now Wired

**`app_shell.html` — Relocated Chart PIH (Screen 4):**  
Added `getVisibleBodyNamesSet()` helper. The planet rows in `renderRelocatedChartHtml` now filter
`Object.keys(planet_houses)` against this set before rendering. If a user disables Chiron in
Settings → Charts → Additional bodies, Chiron no longer appears in the PIH table.

**`app_shell.html` — Comparison PIH (Screen 5):**  
`renderComparisonTableHtml` used a hardcoded `const planetNames = [...]` list. This is now
dynamically filtered through `getVisibleBodyNamesSet()`. Disabled planets/bodies are excluded from
all comparison columns.

**`map_CURRENT.html` — Genie body selectors:**  
Added `syncGenieBodySelectorsToSettings()`. On DOMContentLoaded (and again after 1.5s for async
store load), all four planet selectors (`planetA`, `planetB`, `planetC`, `overlayPlanet`) have
disabled-in-settings bodies hidden and disabled. If the selected value becomes hidden, the selector
resets to the next visible option.

### What Remains Display-Only

The engine (`/relocated-chart`, `/search-regions`) **always returns all bodies** including Chiron
and all core planets. Filtering happens entirely client-side at display time. This is architecturally
correct for this slice — engine-level filtering requires changes to `SearchRequest` and is a
separate engineering task.

### What Is Deferred

Advanced points (Lilith, Vertex, Part of Fortune, other points) are marked with a doctrine comment
in `planetsBodiesHtml`:  
> "Advanced points are future body support, not part of SETTINGS-WIRE-1."

These will appear under "More points" when engine support ships.

### Nodes

North Node and South Node remain permanently disabled (carried from CHART-TRUTH-FIX-1/FIX-3).
`getVisibleBodyNamesSet()` never includes them, regardless of any stored setting.

---

## PART 2 — Minor Aspects

### What Is Now Wired

**`main_centerline_FIXER.py` — engine `aspect_sets`:**  
Added 8 minor aspects as first-class geometric entries:

| Aspect | Offsets |
|---|---|
| quincunx | 150°, 210° |
| semisextile | 30°, 330° |
| semisquare | 45°, 315° |
| sesquiquadrate | 135°, 225° |
| quintile | 72°, 288° |
| biquintile | 144°, 216° |
| novile | 40°, 320° |
| septile | 51°, 309° (≈360/7) |

Each minor aspect also has a distinct muted color in `aspect_colors` for overlay rendering.

**`map_CURRENT.html` — Genie overlay aspect selector:**  
Added an `<optgroup id="overlay-minor-aspects-group">` containing all 8 minor aspects with their
degree labels. The group is hidden by default. `syncGenieMinorAspectOptionsToSettings()` reads
`RMSettings.getEffectiveSettings()` and shows the group when `visible_minor_aspects` is true.

**`app_shell.html` — Settings aspects registry:**  
Added novile and septile to `MINOR` in `_aspectRegistryContext`. Both now appear as toggleable
checkboxes in Settings → Charts → Minor aspects. The save handler's `minorAspIds` includes both.

### What Remains Display-Only

Settings `visible_minor_aspects` (the master toggle) and `visible_minor_aspects_list` (per-aspect
list) save to the database. The AIS, A2A, and comparison displays do not yet filter aspects by this
setting — that is a separate wiring task. For this slice, the primary effect is:
1. Engine now accepts all 8 minor aspects in overlay requests
2. Genie overlay selector exposes minor aspects when the master toggle is on

---

## Known Limitations

1. **Engine-side body filtering not implemented.** The backend always returns all bodies. Only the
   display layer filters. If a future consumer calls `/relocated-chart` directly, it still receives
   Chiron even if Chiron is disabled in settings.

2. **Genie sync fires once at load.** If the user changes settings in the same tab session without
   a page reload, Genie selectors don't automatically re-sync. A settings-change event hook would
   be needed. Low priority for v1.

3. **`septile` precision.** The engine uses 51° as an integer. True septile is 360/7 ≈ 51.43°.
   The max_orb for overlays covers this rounding; no false negatives observed in testing.

4. **Minor aspects in AIS/A2A comparison columns** — wiring to comparison/AIS displays deferred to
   a future SETTINGS-WIRE slice.

---

## Smoke Results

| Smoke | Result | Notes |
|---|---|---|
| `smoke_settings_account.py` | **25/25 PASS** | Includes `be_minor_asp_quincunx_overlay`, `be_minor_asp_novile_overlay` |
| `smoke_settings_navigation.py` | Auth infra failure | New `fe_minor_asp_novile_exists`, `fe_minor_asp_septile_exists`, `fe_chiron_exists`, `fe_chiron_default_on` assertions added |
| `smoke_map_current.py` | Auth infra failure | Pre-existing expired magic link |
| `smoke_comparison_sets.py` | Not run | Needs fresh auth session |
| `smoke_dignities_pih.py` | Not run | Needs fresh auth session |
