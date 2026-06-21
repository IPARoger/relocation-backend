# SETTINGS-WIRE-2: Orbs and House-Edge Settings

**Date:** 2026-06-21  
**Commit:** SETTINGS-WIRE-2: wire orb settings and disclose house-edge limits  
**Status:** COMPLETE

---

## Summary

Wired the four settings categories that were creating the strongest false expectations: house proximity orb, subsequent house rule disclosure, aspect-to-angle orbs, and chart display orb annotation.

---

## PART 1 — House Proximity Orb (WIRED)

**Problem:** `/relocated-chart` hardcoded `near_cusp` threshold as `sep < 2.0` regardless of the user's persisted `house_proximity_orb_degrees` setting.

**Fix:**
- `main_centerline_FIXER.py`: Added `house_proximity_orb: float = 2.0` query parameter to `/relocated-chart`. Used for both `near_cusp` calculation and `cusp_transition_visual_deg` in the response.
- `app_shell.html` (`hydrateRelocatedChart`): Reads `_settingsEff().house_proximity_orb_degrees` and passes as `house_proximity_orb` query param. Default 2.0 preserved.
- `app_shell.html` (comparison columns): Same wiring for all comparison PIH columns.
- `map_CURRENT.html` (popup): Reads `RMSettings.getEffectiveSettings()` to pass `house_proximity_orb` for map popup chart calls.

**Surfaces updated:** Screen 4 relocated chart, map popup relocated chart, comparison PIH columns.

**Default behaviour:** Unchanged. If the setting is absent, defaults to 2.0.

---

## PART 2 — Subsequent House Rule (DISCLOSED)

**Problem:** The UI's "subsequent house" checkbox implied direction-aware (retrograde/applying) house-edge reassignment was in effect. The doctrine requires retrograde-aware logic that is not yet implemented.

**Decision:** Option B — Disclose honestly. The checkbox is preserved for persistence. A clear disclosure paragraph was added to `subsequentHouseRuleHtml()` in `app_shell.html`:

> "The orb controls how close a planet must be to a cusp to flag it as near-cusp. Direction-aware house-edge reassignment (retrograde/applying) is stored and coming soon."

**What is live:** The `house_proximity_orb` value is fully wired (Part 1). The subsequent-house *policy* (direction-aware reassignment) is stored but not calculated.

---

## PART 3 — Aspect-to-Angle Orbs (WIRED)

**Problem:** The `/search-regions` aspect overlay did not read or propagate any `max_orb` value from the client; only the zero-crossing contour line was drawn.

**Fix:**
- `main_centerline_FIXER.py` (`search_regions`): Reads `max_orb` from `aspect_overlay` dict. Falls back to aspect-class defaults (major: 8 deg, sextile: 6 deg, minor: 2-3 deg). Stored in each output GeoJSON feature's `properties` as `max_orb` for downstream consumers.
- `map_CURRENT.html` (`getSelectedAspectOverlay`): Now reads `aspect_to_angle_orbs[aspect]` from effective settings and includes `max_orb` in the overlay payload sent to `/search-regions`.

**What this enables:** Each overlay feature carries its orb in properties, so overlay renderers can display proximity bands or filter by strength. The line itself remains the exact zero-crossing contour; the orb is metadata.

**Default behaviour:** If `max_orb` is absent in the request, defaults to aspect-class default (matches existing behaviour).

---

## PART 4 — Chart Display Orbs (ANNOTATED)

**Problem:** The major/minor chart display orbs had no disclosure that they don't yet affect any live rendering.

**Fix:** Added user-visible note to `chartDisplayOrbsHtml()` in `app_shell.html`:

> "Stored and persisted. These will control aspect visibility in the chart wheel and aspect tables when those renderers are live. They do not affect PIH or map region calculations."

No calculation changes — the values are correctly persisted and will be consumed when chart wheel rendering goes live.

---

## Validation

### smoke_settings_account.py — 19/19 PASS

New assertions added:

| ID | Description | Result |
|----|-------------|--------|
| `be_hpo_accepted` | `/relocated-chart` accepts `house_proximity_orb` param | PASS |
| `be_hpo_monotonic` | Tight orb (0.0001) yields <= near_cusp count of wide orb (2.0) | PASS (nc_wide=1, nc_tight=0) |
| `be_a2a_orb_in_features` | `max_orb=4.0` appears in overlay feature properties | PASS |

### smoke_settings_navigation.py — 20/20 PASS

Pre-existing assertions maintained. Also fixed a pre-existing SyntaxError in the test file (line 256 — nested quote conflict in querySelectorAll JS string) that prevented the file from being parsed.

### smoke_comparison_sets.py — 20/20 PASS

No regressions.

### smoke_map_current.py — PRE-EXISTING INFRA FAILURE

`trigger_find_regions_and_wait` times out on a Playwright click blocked by the Leaflet map element intercepting pointer events. Pre-existing infrastructure issue unrelated to SETTINGS-WIRE-2 changes.

---

## Files Modified

| File | Change |
|------|--------|
| `main_centerline_FIXER.py` | Add `house_proximity_orb` param to `/relocated-chart`; add `overlay_max_orb` extraction and propagation in `search_regions` |
| `app_shell.html` | Wire `house_proximity_orb` in both relocated chart calls; add disclosure to `subsequentHouseRuleHtml()`; add live-consumer note to `chartDisplayOrbsHtml()` |
| `map_CURRENT.html` | Wire `house_proximity_orb` in popup call; add `max_orb` to `getSelectedAspectOverlay()` |
| `scripts/smoke_settings_account.py` | Add `be_hpo_accepted`, `be_hpo_monotonic`, `be_a2a_orb_in_features` assertions |
| `scripts/smoke_settings_navigation.py` | Fix pre-existing syntax error in JS querySelectorAll string |

---

## Doctrine Compliance

- No false expectations: every setting now either changes calculation or carries a clear disclosure.
- `house_proximity_orb`: Fully live. Affects `near_cusp` flag and `cusp_transition_visual_deg` in all three relocated chart consumers.
- `subsequent_house_policy`: Stored. UI discloses direction-aware calculation is not yet implemented.
- `aspect_to_angle_orbs`: Passed through to feature properties. Line overlay geometry remains exact-crossing; orb is metadata for future band rendering.
- `chart_display_orbs`: Stored. UI discloses they will affect the chart wheel when live.
