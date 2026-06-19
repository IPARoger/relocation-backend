# DIGNITIES-1: PIH Dignities Display

**Date:** 2026-06-19  
**Scope:** `dignity_ontology.js`, `app_shell.html`, `main_centerline_FIXER.py`, `scripts/smoke_dignities_pih.py`  
**Doctrine:** `results/119_dignities_diffs_display_doctrine_v1.md`, `results/120_dignities_diffs_mockup_study.md`

## Summary

PIH (Planet-in-House) tables now support an optional **Dignities** footer toggle (default OFF). When enabled, house-result cells receive supportive/challenging background washes derived from a single Layer-2 ontology module. No glyphs, +/- indicators, mutual reception, or interpretive hints. Diffs remain out of scope.

## Implementation

### `dignity_ontology.js`

- Classical seven planets only (Sun–Saturn)
- `lookupFamily(planet, sign)` → `supportive` | `challenging` | `null`
- `parseSignFromLongitudeFormatted()` parses `14° Leo 23'` format from relocated-chart API

### `app_shell.html`

- PIH footer toggle labeled **Dignities** on Screen 4 planet-houses table and Screen 5 comparison columns
- CSS: `.pih-house-cell.dignity-supportive` (`#eef7f3`), `.dignity-challenging` (`#faf3e8`)
- `dignities_enabled` persisted in comparison workspace state (`settings_snapshot_json`)
- Screen 4 dignities are session-local (default OFF, not persisted)

### Static routes

- `/dignity_ontology.js`
- `/human_place_label.js` (missing route added alongside)

## Validation (2026-06-19, port 8041 temp / regression 8004)

```
PASS: smoke_dignities_pih (9 checks)
PASS: smoke_comparison_sets
PASS: smoke_settings_navigation
PASS: smoke_saved_investigations
```

## Out of scope (DIGNITIES-1)

- Diffs display
- Settings dignity presets (ontology is hard-coded v1 table; settings wiring is SETTINGS-2+)
- Map / favorites / search surfaces
- Mutual reception, glyphs, interpretive hints
