# AUDIT: 02_SETTINGS_CONSUMPTION_AUDIT

**Type:** Read-only settings consumption audit
**Author:** Cursor (relay trial — results/ lane)
**Date:** 2026-06-15
**Status:** Read-only — no code/backend/schema/data changes

---

## Objective

For every user-facing setting: where stored, loaded, consumed, and whether it
actually affects behavior.

---

## Files read

- `supabase_store_bridge.js` (load path)
- `app_shell.html` (display, save handler, consumption)
- `main_centerline_FIXER.py` (engine consumption)
- `map_CURRENT.html` (map/Genie payload consumption)

Evidence marked (E) or inference (I).

---

## Settings surface

Settings are stored in `user_settings.settings_json` as a JSON blob, keyed
per account (`profile_id IS NULL` for account-level settings). The bridge
selects the account-level row and deserializes it into `storeUserSettings`.

---

## Setting-by-setting inventory

---

### 1. Default Chart Record

| Field | Value |
|---|---|
| Key | `default_chart_record_id` |
| Stored in | `user_settings.settings_json` via `saveAccountSettingsPatch` (E) |
| Loaded by | `supabase_store_bridge.js` → `storeUserSettings.default_chart_record_id` (E) |
| Consumed by | `app_shell.html` `adaptStoreToView` — used to determine which chart record is the default when the app loads; `screenSettings` pre-selects it in the dropdown (E) |
| Affects behavior? | **Yes — fully wired.** Dashboard and "Open Map (default)" use this to pick the starting chart record. `normalizeNavContext` falls back to it when `chartRecordId` is absent. (E) |
| Status | **Complete** |

---

### 2. House System

| Field | Value |
|---|---|
| Key | `house_system` |
| Stored in | `user_settings.settings_json` via `saveAccountSettingsPatch` (E) |
| Loaded by | `supabase_store_bridge.js` → `storeUserSettings.house_system` (default: `"placidus"`) (E) |
| Displayed by | `app_shell.html` `screenSettings` — reads `raw.user_settings.house_system` and pre-selects the dropdown (E) |
| Consumed by calculation? | **No — inert.** `main_centerline_FIXER.py` hardcodes `b'P'` (Placidus) in every `swe.houses` call: in `get_chart_angles()` (line 570) and in `relocated_chart()` (line 1791). `SearchRequest` has no `house_system` field. `/relocated-chart` accepts no house parameter. The saved value is never passed to the engine. (E) |
| Status | **Saved and displayed; NEVER consumed by calculation engine. Inert.** |
| Gap severity | High — UI implies the setting changes calculations; it does not. |

---

### 3. Zodiac Mode

| Field | Value |
|---|---|
| Key | `zodiac_mode` |
| Stored in | `user_settings.settings_json` (E) |
| Loaded by | `supabase_store_bridge.js` → `storeUserSettings.zodiac_mode` (default: `"tropical"`) (E) |
| Displayed by | Not exposed in `screenSettings` UI — no select for zodiac mode exists in the Settings screen (E) |
| Consumed by calculation? | **No — inert.** No reference to `zodiac_mode` found in `main_centerline_FIXER.py`, `map_CURRENT.html`, or `app_shell.html` beyond loading. (E) |
| Status | **Stored in bridge shape; never displayed; never consumed. Fully inert.** |
| Gap severity | Low — not user-visible (no UI control) so no user confusion. Value exists for future use. |

---

### 4. Orb Defaults

| Field | Value |
|---|---|
| Key | `orb_defaults` |
| Stored in | `user_settings.settings_json` (E) |
| Loaded by | `supabase_store_bridge.js` → `storeUserSettings.orb_defaults` with defaults: `{conjunction:8, square:6, opposition:8, trine:8, sextile:4}` (E) |
| Displayed by | No UI control in `screenSettings` (E) |
| Consumed by calculation? | **Partially.** `map_CURRENT.html` uses per-call `orb_deg` values returned by the backend `/aspect-orb-at-point` endpoint (E), but that endpoint takes lat/lon/birth params and computes the orb — it does not accept a user orb override. The `orb_defaults` from `user_settings` are not passed to `/search-regions` (`SearchRequest` has no orb field) or to `/relocated-chart`. (E) |
| Status | **Stored in bridge shape; no UI control; not consumed by engine routes. Inert for now.** |
| Gap severity | Medium — when aspect-based search is extended, orb defaults will be needed; path is clear but not wired. |

---

### 5. Visible Minor Aspects

| Field | Value |
|---|---|
| Key | `visible_minor_aspects` |
| Stored in | `user_settings.settings_json` (E) |
| Loaded by | `supabase_store_bridge.js` → `storeUserSettings.visible_minor_aspects` (default: `false`) (E) |
| Displayed by | No UI control in `screenSettings` (E) |
| Consumed by calculation? | **No — inert.** No reference found in engine routes, map, or shell beyond loading. (E) |
| Status | **Stored; no UI; not consumed. Inert.** |
| Gap severity | Low — no user-facing control, so no honesty gap visible to the user. |

---

### 6. Helper Layers

| Field | Value |
|---|---|
| Key | `helper_layers` |
| Stored in | `user_settings.settings_json` (E) |
| Loaded by | `supabase_store_bridge.js` → `storeUserSettings.helper_layers` (default: `{}`) (E) |
| Displayed by | No UI control in `screenSettings` (E) |
| Consumed by calculation? | **No — inert.** No reference in engine routes, map, or shell beyond loading. (E) |
| Status | **Stored; no UI; not consumed. Inert.** |
| Gap severity | Low — invisible to user. |

---

### 7. Ontology Pack ID

| Field | Value |
|---|---|
| Key | `ontology_pack_id` |
| Stored in | `user_settings.settings_json` (E) |
| Loaded by | `supabase_store_bridge.js` → `storeUserSettings.ontology_pack_id` (default: `null`) (E) |
| Displayed by | No UI control in `screenSettings` (E) |
| Consumed by calculation? | **No — inert.** No reference in engine routes or frontend beyond loading. (E) |
| Status | **Stored; no UI; not consumed. Inert.** |
| Gap severity | Low — invisible to user; reserved for future ontology/AI interpretation layer (frozen per governance). |

---

### 8. Settings Version

| Field | Value |
|---|---|
| Key | `settings_version` |
| Stored in | `user_settings.settings_json` (E) |
| Loaded by | `supabase_store_bridge.js` → `storeUserSettings.settings_version` (default: `1`) (E) |
| Consumed | Not used for any version-gating logic currently visible in frontend or backend (I) |
| Status | **Stored; no active consumer. Placeholder for future migration gating.** |
| Gap severity | None — infrastructure field, not user-visible. |

---

## Summary table

| Setting | UI Control | Stored | Loaded | Consumed | Status |
|---|---|---|---|---|---|
| default_chart_record_id | Yes (Settings dropdown) | Yes | Yes | Yes (dashboard default, nav context) | **Complete** |
| house_system | Yes (Settings dropdown) | Yes | Yes | **No — engine hardcodes Placidus** | **Inert (honesty gap)** |
| zodiac_mode | No | Yes | Yes | No | **Inert** |
| orb_defaults | No | Yes | Yes | No (not passed to engine) | **Inert** |
| visible_minor_aspects | No | Yes | Yes | No | **Inert** |
| helper_layers | No | Yes | Yes | No | **Inert** |
| ontology_pack_id | No | Yes | Yes | No | **Inert (frozen layer)** |
| settings_version | No | Yes | Yes | No active use | **Placeholder** |

---

## Critical finding

Only **one** of the eight settings fields in the current schema actually affects
runtime behavior: `default_chart_record_id`.

`house_system` is the only other user-visible setting. It is saved to Supabase,
displayed in the Settings dropdown, and implies that changing it will alter
calculations. **It will not.** Both `get_chart_angles()` and `relocated_chart()`
hardcode `swe.houses(jd, lat, lon, b'P')` (Placidus). `SearchRequest` has no
`house_system` field. `/relocated-chart` accepts no house parameter.

This is the largest honesty gap in the settings system.

---

## Comparison set `settings_snapshot_json`

`comparison_sets` has a `settings_snapshot_json` field. In `map_CURRENT.html`
this is always set to `{}` on comparison-set insert (`settings_snapshot_json: {}`).
It is not populated with active settings at comparison-build time. (E)

---

## Explicitly NOT done (rejected scope)

- No code changes.
- No backend / schema / data changes.
- No implementation of fixes.
- No self-selected follow-up tasks.

---

## Result

VERIFIED (read-only; no files changed)
