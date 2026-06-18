# S-UX-1C — Settings Subpage Router

**Date:** 2026-06-18  
**Roadmap ID:** S-UX-1C  
**Checkpoint:** c5b9b31 → this slice

# Files Changed

| File | Change |
|------|--------|
| `app_shell.html` | Settings landing cards, hash sub-routes (`#/settings/{sub}`), subpage shells, save handler works per subpage |
| `scripts/smoke_settings_account.py` | Landing/about/charts/account subpage navigation; minor/orb tests on correct subpages |

# Routing Model

- **Landing:** `#/settings` — seven category cards with Open buttons
- **Subpages:** `#/settings/account`, `#/settings/charts`, `#/settings/map-location`, `#/settings/appearance-regional`, `#/settings/sharing-data`, `#/settings/technical`, `#/settings/about`
- `navContext.settingsSubpage` parsed from hash path segment 2; `buildLocationHash` emits subpath
- `data-settings-sub` opens subpage; `data-action="settings-back"` returns to landing
- Top-level `data-nav="settings"` always resets to landing

# Settings Landing

Seven cards:

1. Account & Profiles  
2. Charts  
3. Map & Location  
4. Appearance & Regional  
5. Sharing & Data  
6. Technical & Personalization  
7. About & Data Sources  

# Subpages

| Subpage | Editable | Contents |
|---------|----------|----------|
| Account & Profiles | Yes (Save) | My Account placeholder, default profile selector, Manage Profiles |
| Charts | Yes (Save) | Full S-UX-1 charts stack (bodies, aspects, orbs, dignities shell, house/zodiac, advanced + effective config) |
| Map & Location | No | Map stubs + Location / Road Trip / GPS placeholders |
| Appearance & Regional | No | Appearance + Language stubs + glyph/date/time placeholders |
| Sharing & Data | No | Sharing + My Data stubs |
| Technical & Personalization | No | Technical + Personalization stubs |
| About & Data Sources | No | Swiss Ephemeris, GeoNames, IANA, Leaflet/OSM (`#sec-about`) |

Removed “Dashboard” wording from default profile copy.

# Persistence Preservation

- All `rm-settings-*` element IDs unchanged on Account and Charts subpages
- `save-settings` collects only fields present on the current subpage (no longer requires `#rm-settings-default-cr`)
- Keys preserved: `default_chart_record_id`, aspect/body/orb/house/A2A fields

# Validation

```bash
set -a && source .env.staging && set +a
venv/bin/python scripts/smoke_settings_account.py
```

**Result:** PASS (22/22)

| Check | Result |
|-------|--------|
| `fe_settings_landing` | PASS |
| `fe_settings_ia_about` | PASS |
| `fe_settings_charts_sub` | PASS |
| `fe_saved_msg` / default CR / minor / major orb | PASS |
| Backend ownership suite | PASS |

Grep: no backend, renderer, map, or search file changes.

# Deferred Items

- Nested settings sidebar (replaced by landing router)
- Functional Map / Appearance / Sharing subpages
- Per-account settings subpage deep-link in Help/docs

# Verdict

**PASS** — Settings is a compact landing plus focused subpages; persistence and smoke coverage preserved.
