# 278 — S5 Glyph Library Implementation

**Date:** 2026-06-27  
**Authority:** [SETTINGS_V1_PRODUCT_SPEC.md](../docs/canon/SETTINGS_V1_PRODUCT_SPEC.md) §9  
**Scope:** Glyph variant selection for Mars, Uranus, Pluto, and Capricorn

## Summary

Production glyph library wiring: extensible asset registry, account-level `glyph_selections` settings, Appearance picker UI, and resolver consumers (tables + wheel). Uses AstroDotBasic production font variants where indexed; honest stub for Pluto traditional glyph pending asset audit.

## Asset status

| Entity | Variant | Status | Source |
|--------|---------|--------|--------|
| Mars | Standard arrow | **Production** | AstroDotBasic `E` |
| Mars | Inverted Venus | **Production** | AstroDotBasic `D` + 180° transform |
| Uranus | Herschel (curved H) | **Production** | AstroDotBasic `H` |
| Uranus | Simplified (linked circles) | **Production** | AstroDotBasic `n` |
| Pluto | PL monogram | **Production** | AstroDotBasic `J` |
| Pluto | Traditional glyph | **Stub** | `theme/glyphs/stubs/pluto_traditional.svg` (labeled) |
| Capricorn | US loop tail | **Production** | AstroDotBasic `j` |
| Capricorn | Euro V-loop | **Production** | AstroZLzx `J` (`theme/fonts/AstroZLzx.ttf`) |

No emoji. No Unicode glyph substitutes in settings or resolver.

## Files changed

| File | Change |
|------|--------|
| `settings/glyph_library_registry.json` | Asset registry (extensible entity/variant model) |
| `settings/astrology_settings_defaults.json` | `glyph_selections` defaults |
| `theme/glyphs.js` | Registry-aware `resolveGlyph`, SVG fragment helper |
| `theme/glyphs.css` | AstroZLzx `@font-face`, variant picker styles |
| `theme/fonts/AstroZLzx.ttf` | Euro Capricorn font (copied from vendor archive) |
| `theme/glyphs/stubs/pluto_traditional.svg` | Honest Pluto traditional stub |
| `services/account_settings_resolver.py` | `glyph_selections` in effective settings |
| `supabase_store_bridge.js` | `glyph_selections` merge |
| `app_shell.html` | Appearance glyph picker, save/restore/apply |
| `main_centerline_FIXER.py` | Registry, font, stub routes |
| `scripts/smoke_s5_glyph_settings.py` | S5 static smoke (29 checks) |
| `docs/BETA_MASTER_CHECKLIST.md` | S5 complete |

## Smoke

| Script | Result |
|--------|--------|
| `smoke_s5_glyph_settings.py` | **29/29 PASS** |
| `smoke_s4_appearance_settings.py` | **22/22 PASS** |
| `smoke_s3_dignities_settings.py` | **13/13 PASS** |
| `smoke_s2_astrology_settings.py` | **15/15 PASS** |
| `smoke_glyph_wiring_1.py` | **17/17 PASS** |

## Still SOON

- Glyph family selector (AstroDotBasic only, labeled in UI)
- Aspect notation format picker
- Full glyph catalog ingest from `Fonts and Glyphs/` archives

**Status:** S5 complete.
