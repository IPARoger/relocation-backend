# SETTINGS-2A: Settings Terminology Alignment

**Date:** 2026-06-20  
**Scope:** `app_shell.html`, `scripts/smoke_settings_navigation.py`  
**Doctrine:** `results/114_settings_doctrine_capture_v1.md`, `results/123_settings2_placeholder_audit_slices.md`

## Summary

Settings navigation terminology aligned to doctrine without changing persistence, save paths, or section URL ids.

| Before | After |
|--------|-------|
| Display | **Appearance** |
| Data | **My Data** |

Internal route ids remain `display` and `data` for bookmark compatibility. URL aliases added: `appearance` → `display`, `my-data` → `data`.

## Nav order (doctrine 114)

Account → My Data → Astrology → Appearance → Notifications → Exports → About

## Copy cleanup

- Account: removed profile-management framing; subtitle is sign-in / subscription / identity
- Default profile label: removed “Map & app” coupling
- My Data: removed Technical / Personalization / debug stubs from user panel; doctrine-aligned saved-work rows
- History actions: removed “(placeholder)” wording
- Settings purpose line: removed “placeholders” language
- Map location futures: “Experimental” → “Coming soon”

## Validation (2026-06-20, port 8004)

```
PASS: smoke_settings_navigation (16 checks)
PASS: smoke_settings_account (22 checks)
```

## Out of scope (SETTINGS-2A)

- Moving Manage Profiles from Account to My Data (SETTINGS-2B)
- Dev stub quarantine (SETTINGS-2C)
- Astrology subsection reorder (SETTINGS-2D)
- New persisted settings keys
