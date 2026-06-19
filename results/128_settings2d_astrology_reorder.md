# SETTINGS-2D: Astrology Settings Reorder

**Date:** 2026-06-20  
**Scope:** `app_shell.html`  
**Doctrine:** `results/114_settings_doctrine_capture_v1.md`, `results/119_dignities_diffs_display_doctrine_v1.md`, `results/120_dignities_diffs_mockup_study.md`

## Summary

Astrology settings reordered to match doctrine. No backend changes; existing save paths preserved.

## Section order (canonical)

| # | Section | Notes |
|---|---------|-------|
| 1 | **Bodies** | Core planets locked on; Chiron default on; Nodes default off; More points collapsed |
| 2 | **Aspects** | Major first; minor individually selectable; master minor toggle retained |
| 3 | **Orbs** | Chart display orbs + aspect-to-angle / search orbs |
| 4 | **Subsequent House Rule** | Toggle + orb beneath |
| 5 | **Out-of-Sign Aspects** | Standalone toggle |
| 6 | **House System** | Placidus (unchanged) |
| 7 | **Zodiac** | Tropical read-only (unchanged) |
| 8 | **Dignities** | Display-only copy — PIH footer toggle; no preset editor |

## Removed from Astrology page

- Chart Appearance stub
- Interpretive hints block
- Effective configuration panel (quarantined in 2C)
- Dignity preset dropdown (replaced with PIH display note)

## Persistence (unchanged keys)

- `visible_minor_aspects`, `out_of_sign_aspects`, aspect visibility/orbs, `house_proximity_orb_degrees`, `subsequent_house_policy`, `aspect_to_angle_orbs`
- `visible_bodies` now includes `north_node` / `south_node` when saved from Additional bodies

## Validation (2026-06-20, port 8004)

```
PASS: smoke_settings_navigation (16 checks)
PASS: smoke_settings_account (22 checks)
```

## Out of scope

- Dignity ontology / preset editing (SETTINGS-3F)
- Chart vs A2A display column split on aspect rows (SETTINGS-3D)
- House system / zodiac editing
