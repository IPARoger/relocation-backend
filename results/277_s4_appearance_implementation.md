# 277 — S4 Appearance Palettes Implementation

**Date:** 2026-06-27  
**Authority:** [SETTINGS_V1_PRODUCT_SPEC.md](../docs/canon/SETTINGS_V1_PRODUCT_SPEC.md) §8

## Summary

Production appearance controls: five curated palette families (overlay, aspect, dignity, chart, inner glow) wired to `user_settings`, CSS variables, chart wheel, PIH dignity washes, and Search Map pinwheel chips. Optimistic-primary / Spring doctrine is the default. No custom color pickers in Appearance.

## Changes

| File | Change |
|------|--------|
| `settings/appearance_settings_defaults.json` | New defaults for five palette keys |
| `settings/astrology_settings_defaults.json` | Merged appearance keys + optimistic dignity colors |
| `theme/appearance_palettes.js` | Curated palette catalog, CSS apply, pinwheel colors |
| `services/account_settings_resolver.py` | Resolver picks for appearance keys |
| `supabase_store_bridge.js` | Effective settings merge + store export |
| `main_centerline_FIXER.py` | `GET /settings/appearance_settings_defaults.json` |
| `app_shell.html` | Appearance palette UI, save/restore, wheel/aspect consumers |
| `map_CURRENT.html` | Pinwheel colors from `RMAppearancePalettes`; theme scripts |
| `scripts/smoke_s4_appearance_settings.py` | 22 static checks |

## Palettes (curated)

| Family | Default | Options |
|--------|---------|---------|
| Overlay | optimistic-primary | summer-expansion, winter-clarity |
| Aspect | optimistic-primary | spring-harmony |
| Dignity | optimistic-soft | spring-mist |
| Chart | optimistic-primary | warm-stone |
| Inner glow | micro-green | micro-blue, micro-warm |

Pinwheel / map variable chips use overlay palette order (Spring doctrine twelve) — not placeholder `VAR_COLORS` / Google rainbow.

## Smoke

| Script | Result |
|--------|--------|
| `smoke_s4_appearance_settings.py` | **22/22 PASS** |
| `smoke_s2_astrology_settings.py` | **15/15 PASS** |
| `smoke_s3_dignities_settings.py` | **13/13 PASS** |
| `smoke_dignities_house.py` | **15/15 PASS** |

## Screenshot

`validation/mockups/beta/screenshots/s4_appearance_settings/01_appearance_palettes.png`

## Integration notes

- Dignity **preset/rules** remain under Astrology → Dignities (S3).
- Appearance dignity palette sets curated `dignity_colors`; astrology color mode (paired/four) unchanged.
- Seasonal themes (`RelocationTheme`) remain device-local; overlay palette overrides `--th-ov-*` at runtime.
- Glyph / aspect-band / wheel-style rows stay SOON stubs.

**Status:** S4 complete.
