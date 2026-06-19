# SETTINGS-2E: Appearance Cleanup

**Date:** 2026-06-20  
**Scope:** `app_shell.html`  
**Doctrine:** `results/114_settings_doctrine_capture_v1.md`, `results/125_settings2a_terminology_alignment.md`, `results/128_settings2d_astrology_reorder.md`

## Summary

Visual presentation stubs consolidated under **Appearance**. **Astrology** retains calculation and interpretation settings only.

## Boundary

| Area | Owns |
|------|------|
| **Appearance** | Chart appearance, glyph appearance, aspect-band appearance, themes, map presentation, regional formats |
| **Astrology** | Bodies, aspects, orbs, subsequent house rule, out-of-sign aspects, house system, zodiac, dignities (ontology/display note) |

## Moved into Appearance

| Section | Stubs |
|---------|-------|
| **Chart appearance** | Wheel style, chart surface |
| **Glyph appearance** | Glyph family, glyph variants (Mars, Capricorn, Uranus, Pluto, aspect notation) |
| **Aspect-band appearance** | Aspect band style, aspect band topology (relocated from Map) |
| **Themes** | Color themes (future) |

## Removed from Astrology

- Orphaned `chartAppearanceStubHtml`, `dignitiesShellHtml`, `interpretiveHintsShellHtml` (dead code from prior slices)
- Visual framing in subpage subtitle ("chart display" → calculation-focused copy)

## Astrology unchanged (calculation)

Bodies, aspects, orbs (chart display + aspect-to-angle), subsequent house rule, out-of-sign aspects, house system, zodiac, dignities PIH footer note.

> **Note:** "Chart display" under Orbs refers to planet-to-planet orb **calculation**, not wheel styling.

## Persistence

No changes.

## Validation (2026-06-20, port 8004)

```
PASS: smoke_settings_navigation (16 checks)
PASS: smoke_settings_account (22 checks)
```

## Out of scope

- Wiring real theme/glyph/band controls (SETTINGS-3H–J)
- Dignity preset editor (SETTINGS-3F)
- Interpretive hints toggle (SETTINGS-3G)
