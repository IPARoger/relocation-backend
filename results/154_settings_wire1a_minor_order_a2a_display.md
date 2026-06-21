# SETTINGS-WIRE-1A Closeout: Minor Aspect Order + A2A Display Settings
**Date:** 2026-06-21  
**Task:** Two follow-up corrections after SETTINGS-WIRE-1  
**Files changed:**  
`app_shell.html`, `map_CURRENT.html`, `main_centerline_FIXER.py`,  
`supabase_store_bridge.js`, `services/account_settings_resolver.py`,  
`scripts/smoke_settings_account.py`, `scripts/smoke_settings_navigation.py`

---

## FIX 1 — Minor Aspect Display Order

### Problem
SETTINGS-WIRE-1 added novile before septile in all three locations. The correct
harmonic family order is:
1. Quincunx (6th-harmonic adjacent)
2. Semi-sextile
3. Semi-square
4. Sesquiquadrate
5. Quintile (5th harmonic)
6. Biquintile
7. **Septile (7th harmonic)**
8. **Novile (9th harmonic)**

5-family → 7-family → 9-family.

### Changes
- **`app_shell.html`**: `_aspectRegistryContext` MINOR array and `minorAspIds` in save handler — septile now precedes novile.
- **`map_CURRENT.html`**: Genie `overlayAspect` optgroup — Septile (51°) now listed before Novile (40°).
- **`main_centerline_FIXER.py`**: `aspect_sets` — `septile` entry now precedes `novile` entry.

---

## FIX 2 — Aspect-to-Angle Display Settings

### What Was Added

New settings section: **Settings → Astrology → Aspect-to-Angle Display**

Four toggle checkboxes with honest defaults:

| Angle | Default | Rationale |
|---|---|---|
| ASC (Ascendant) | **ON** | Primary relocation marker |
| MC (Midheaven) | **ON** | Primary relocation marker |
| DSC (Descendant) | OFF | Less commonly used in relocation |
| IC (Imum Coeli) | OFF | Less commonly used in relocation |

### New setting key: `display_aspects_to_angles`

```json
{ "asc": true, "mc": true, "dsc": false, "ic": false }
```

### Wiring

**`app_shell.html`:**
- New `a2aDisplayAnglesHtml()` function renders the four checkboxes with current values from effective settings.
- `settingsChartsBodyHtml()` includes a new "Aspect-to-Angle Display" section after Aspects.
- Save handler collects all four checkbox states and writes `display_aspects_to_angles` to `settingsPatch`.

**`supabase_store_bridge.js`:**
- Added `display_aspects_to_angles` to `RM_SETTINGS_DEFAULTS` with defaults `{asc:true, mc:true, dsc:false, ic:false}`.
- Added to `getEffectiveSettings()` return — stored value overrides default, no silent fallback.

**`services/account_settings_resolver.py`:**
- Added `display_aspects_to_angles` to `RM_SETTINGS_DEFAULTS` (Python side).
- Added to `get_effective_settings()` return with stored→ontology→default priority.

### Display Consumer Note

A code comment in `a2aDisplayAnglesHtml` makes the current state explicit:
> "NOTE: The A2A chart table consumer reads these at render time; chart wheel renderer is not yet live — these settings are wired for persistence now, display consumer integration follows."

The controls are not labeled "coming soon" because they are real, persisted preferences — they already work as data. Their effect on rendered tables and chart wheels is the pending integration.

---

## Smoke Results

| Smoke | Result | Notes |
|---|---|---|
| `smoke_settings_account.py` | **26/26 PASS** | Includes `be_a2d_persists` (display_aspects_to_angles round-trips through PATCH) |
| `smoke_settings_navigation.py` | Auth infra failure | New `fe_septile_before_novile`, `fe_a2d_controls_exist`, `fe_a2d_defaults` assertions added |
| `smoke_map_current.py` | Not affected | No map-side changes |
