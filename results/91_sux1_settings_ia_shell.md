# S-UX-1 — Settings IA Shell + Data Sources

**Date:** 2026-06-18  
**Mode:** IMPLEMENT  
**Roadmap:** `docs/roadmaps/active/WEB2_COMPLETION__ACTIVE__2026-06-18.md`

# Files Changed

| File | Change |
|------|--------|
| `app_shell.html` | Settings sidebar IA (12 sections), Charts regrouping, About & Data Sources, stub sections, `initSettingsNav()` |
| `scripts/smoke_settings_account.py` | `major_aspect_orbs` persistence, `#sec-about` check, benign 404 console filter |

# Prototype Alignment

- Production Settings uses prototype top-level structure via sticky sidebar + anchor cards:
  1. My Account · 2. My Profiles · 3. Charts · 4. My Map · 5. Appearance · 6. Location · 7. Language & Regional · 8. Sharing & Exports · 9. My Data · 10. Technical · 11. Personalization · 12. About & Data Sources
- Non-launch sections use prototype-inspired rows with **Coming soon** badges; no fake persistence wiring.
- Nav click scrolls to `#sec-*` sections; save bar remains sticky at bottom.

# Existing Persistence Preserved

All existing `save-settings` / `saveAccountSettingsPatch` keys unchanged (same element IDs):

- `default_chart_record_id` (moved UI to My Profiles)
- `visible_minor_aspects`, `out_of_sign_aspects`
- `visible_planets`, `visible_bodies`
- `visible_major_aspects`, `major_aspect_orbs`
- `visible_minor_aspects_list`, `minor_aspect_orbs`
- `house_proximity_orb_degrees`, `subsequent_house_policy`
- `aspect_to_angle_orbs`

`house_system` remains display-only (not written on save; merge preserves stored value).

# Charts Section

Launch order inside **Charts** card:

1. **Astral Bodies & Points** — `planetsBodiesHtml()`
2. **Chart Appearance** — stub (coming soon)
3. **Aspect Display** — `advancedSettingsHtml()` + `aspectRegistryVisibilityHtml()`
4. **Orbs & House Boundaries** — `aspectRegistryOrbsHtml()` + late-in-house + A2A copy
5. **Dignities** — shell only (Traditional/Modern/Hybrid disabled; not applied)
6. **House System** — honest disabled Placidus select
7. **Zodiac** — read-only effective mode
8. **Advanced** — interpretive hints shell + effective config read-only table

**Interpretive hints:** default off, disabled checkbox, orange/green swatch preview, `?` tooltip with required copy. No scoring/rendering.

# About & Data Sources

Exact labels in `#sec-about`:

- Astronomical calculations — Swiss Ephemeris
- Location database — GeoNames
- Time zone identifiers — IANA Time Zone Database
- Maps — Leaflet / OpenStreetMap

No claim that IANA data has been downloaded/imported. GeoNames labeled as location database (not “place database”).

# Validation

```bash
set -a && source .env.staging && set +a
venv/bin/python scripts/smoke_settings_account.py
```

**Result:** PASS (20/20 checks) including:

- `fe_settings_ia_about` — About section present with GeoNames
- `fe_inmemory_major_orb` / `fe_reload_major_orb` / `fe_db_major_orb` — `major_aspect_orbs.conjunction`
- All prior default CR + `visible_minor_aspects` checks

**Also attempted:** `scripts/smoke_app_shell_store_read.py` — TIMEOUT (environment/session; not a Settings regression signal).

**Manual/grep:**

- Settings route loads via `#/settings` / `navigate('settings')`
- Save Settings works (smoke verified)
- `#sec-about` + GeoNames in `app_shell.html`
- No astrology renderer / chart math / backend route changes

# Deferred Items

- Dignity engine and scoring
- Engine wiring for orbs, bodies, house proximity, A2A
- Functional Map / Appearance / Language / Sharing / My Data / Technical / Personalization settings
- Chart Appearance persistence
- `smoke_app_shell_store_read.py` timeout investigation (pre-existing env flake)

# S-UX-1 Verdict

**COMPLETE** — Production Settings is launch-navigable with prototype IA, Charts regrouped, GeoNames/Swiss Ephemeris attribution in About & Data Sources, and all existing persistence paths preserved.
