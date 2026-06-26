# 275 — S2 Astrology Settings Wiring

**Date:** 2026-06-27  
**Authority:** [SETTINGS_V1_PRODUCT_SPEC.md](../docs/canon/SETTINGS_V1_PRODUCT_SPEC.md)

## Summary

Astrology Settings UI in `app_shell.html` aligned to Settings V1: unified aspect rows (checkbox + orb), Advanced gates for minor aspects and custom orbs, simplified late-house planet alert (2° default), honest asteroids SOON control, applying/separating as appearance note only. Save handler unchanged — all controls remain wired to existing `user_settings` patch keys.

## Changes

| Area | Before | After |
|------|--------|-------|
| Major aspects | Separate visibility + orb grids | Single list: ☑ + orb per aspect |
| Minor aspects | Always visible | `Minor Aspects (Advanced)` `<details>` |
| Custom orbs | Separate orb settings section | `Custom Orbs (Advanced)` — aspect-to-angle orbs |
| Late house | House proximity + direction-aware stub | **Late-house planet alert** only (2°) |
| Asteroids | Absent | Disabled control + SOON badge |
| Presets | — | No Strict/Normal/Loose (none added) |

## Smoke

```
python3 scripts/smoke_s2_astrology_settings.py  → PASS 15/15
python3 scripts/smoke_bi0_archaeology.py        → PASS 34/34
```

## Still SOON / inert

- Aspects to asteroids (engine not in Beta)
- Dignities ontology editor (unchanged Advanced stub)
- Exact aspect threshold (read-only info)

**Status:** S2 complete.
