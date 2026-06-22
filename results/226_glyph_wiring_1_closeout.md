# 226 — GLYPH-WIRING-1 Closeout

**Date:** 2026-06-22  
**Ticket:** GLYPH-WIRING-1  
**Status:** **DONE**

---

## Summary

One temporary production glyph family (**AstroDotBasic**) is now wired across the application shell via a central `resolveGlyph()` resolver with Unicode fallbacks. No glyph picker, family selector, or settings stub was added.

| Surface | Status | Mechanism |
|---------|--------|-----------|
| Wheel planets | **Live** | `formatGlyphSvgText("planet", …)` + AstroDotBasic SVG font |
| Wheel signs | **Live** | Font glyphs at sign centers (replaced stroke paths) |
| Wheel angles | **Live** | ASC/MC/IC font glyphs; DSC text fallback |
| PIH tables | **Live** | Planet name prefix + sign glyph in longitude column |
| AIS tables | **Live** | Angle label glyph + sign glyph in position cells |
| A2A tables | **Live** | Planet/aspect/angle glyphs in single + matrix views |
| Comparison columns | **Live** | Shared formatters (`formatCanonicalAngleDisplayHtml`, etc.) |
| Relocated chart (Screen 4) | **Live** | Reuses `renderRelocatedChartHtml` stack |
| Profile natal facts | **Live** | Reuses `renderProfileNatalChartHtml` stack |

---

## New assets

| Path | Role |
|------|------|
| `theme/fonts/AstroDotBasic.ttf` | Served production font (copied from vendor archive) |
| `theme/glyphs.css` | `@font-face` + `.rm-glyph-*` classes |
| `theme/glyphs.js` | `resolveGlyph`, `formatGlyphHtml`, `formatGlyphSvgText` → `window.__rmGlyphs` |

## Server routes (`main_centerline_FIXER.py`)

- `/theme/glyphs.js`
- `/theme/glyphs.css`
- `/theme/fonts/AstroDotBasic.ttf`

## Astro key map (AstroDotBasic)

- Planets: Q=Sun … Z=Pluto, t=Chiron
- Signs: A=Aries … L=Pisces
- Aspects: `!` conjunct, `"` opposition, `#` square, `$` trine, `'` sextile, etc.
- Angles: a=ASC, b=MC, c=IC (DSC → Unicode text fallback)
- Nodes: `<` north, `>` south (resolver ready; not yet surfaced in tables)

---

## Smoke test

```bash
python3 scripts/smoke_glyph_wiring_1.py
```

---

## Out of scope (per ticket)

- `glyphAppearanceHtml()` settings stub — **not wired**
- Alternate glyph packs / user picker — deferred
- Map Genie overlay glyphs — separate surface (not in this slice)


## Post-closeout correction

Commit `4f6a0af` briefly applied legacy Astro-ZLzx keys (Q=Sun). Reverted to the **AstroDotBasic specimen** map (A=Sun, a–l signs, m–y aspects, P/Q angles) per the font character chart.
