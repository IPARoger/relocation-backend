# W2-SETTINGS-1: Settings navigation framework

**Date:** 2026-06-16  
**Scope:** `app_shell.html`, `scripts/smoke_settings_navigation.py`  
**Backend:** None

## Summary

Settings now uses a **canonical seven-section subpage architecture** with shared sidebar navigation, hash routes, placeholder panels for future controls, and preserved save flows for Account and Astrology. No new settings persistence or API work.

## Subpages

| Section | Route | Save bar | Content |
|---------|-------|----------|---------|
| Account | `#/settings/account` | Yes | Default profile + profile list (existing) |
| Astrology | `#/settings/astrology` | Yes | Chart bodies, aspects, orbs, dignities (existing) |
| Display | `#/settings/display` | No | Appearance, regional, map/location stubs (`#sec-display`) |
| Notifications | `#/settings/notifications` | No | Alert stubs (`#sec-notifications`) |
| Exports | `#/settings/exports` | No | Share/export stubs (`#sec-exports`) |
| Data | `#/settings/data` | No | Saved work + technical stubs (`#sec-data-saved`) |
| About | `#/settings/about` | No | Ephemeris / GeoNames / IANA / OSM attribution |

**Landing:** `#/settings` — sidebar + `.settings-landing-grid` card grid (unchanged for existing smokes).

## Legacy URL aliases

Bookmarks and older smokes keep working; aliases normalize to canonical IDs in `navContext` and renderers:

| Legacy | Canonical |
|--------|-----------|
| `charts` | `astrology` |
| `map-location` | `display` |
| `appearance-regional` | `display` |
| `sharing-data` | `exports` |
| `technical` | `data` |

## Framework pieces (`app_shell.html`)

- `SETTINGS_SECTIONS` — canonical section metadata (id, label, title, desc).
- `normalizeSettingsSubpage()` — alias → canonical id.
- `settingsNavHtml(activeId)` — sidebar buttons with `data-settings-sub` and `.active`.
- `settingsPageLayout()` — shared shell: `data-settings-framework`, nav, title, body, optional save bar.
- `settingsSubpageShell()` — thin wrapper; `showSave` only when `{ showSave: true }`.
- `SETTINGS_SUBPAGE_RENDERERS` — one renderer per canonical section; legacy keys delegate.
- Placeholder rows use `settingsStubRow()` + `data-settings-future` on section panels where future controls will mount.

**Preserved behavior**

- Account: `#rm-settings-default-cr`, profile management, save → `PUT /settings`.
- Astrology: `#rm-settings-minor-aspects`, major/minor orbs, aspect toggles — same DOM ids and save path.
- About attribution block and landing grid selectors used by `smoke_settings_account.py`.

## Smoke

**New:** `scripts/smoke_settings_navigation.py`

- Landing: 7 nav items + `.settings-landing-grid`
- Each canonical subpage: hash, active nav item, section marker
- Legacy `charts` → `astrology` in `navContext`
- Sidebar click navigation (account → notifications)
- No spurious console errors

**Regression:** `scripts/smoke_settings_account.py` — all checks pass (save, default profile, orbs, landing, `charts` sub alias).

## Validation (2026-06-16, port 8004)

```
PASS: smoke_settings_navigation (11 checks)
PASS: smoke_settings_account (22 checks)
```

## Out of scope (intentional)

- Notification delivery, export presets, display themes, data export — stubs only
- Backend settings schema changes
- New persisted keys beyond existing Account/Astrology save
