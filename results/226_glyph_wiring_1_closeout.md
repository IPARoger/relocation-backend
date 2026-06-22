# GLYPH-WIRING-1 Closeout

**Task:** Temporary production standardization — one glyph family (AstroDotBasic) everywhere, central `resolveGlyph()`, Unicode fallback. No picker, family selector, settings wiring, or alternate packs.

**Status:** Complete

## Source

- Font: `Fonts and Glyphs/Glyphs w Aspects/astrodotbasic/AstroDotBasic.ttf`
- Served copy: `theme/fonts/AstroDotBasic.ttf`
- Character map per AstroDotBasic specimen (not legacy Astro-ZLzx keys):
  - Planets: A–J (Sun–Pluto), U (Chiron), L/M (nodes)
  - Signs: a–l (Aries–Pisces)
  - Aspects: m–y (conjunction through contra-parallel)
  - Angles: P (ASC), Q (MC); DSC/IC fall back to text/Unicode

## Deliverables

| File | Role |
|------|------|
| `theme/glyphs.js` | `window.__rmGlyphs.resolveGlyph()`, `formatGlyphHtml()`, `formatGlyphSvgText()`, `svgFontFamilyAttr()` |
| `theme/glyphs.css` | `@font-face` + `.rm-glyph` styles |
| `theme/fonts/AstroDotBasic.ttf` | Production font asset |
| `main_centerline_FIXER.py` | Static routes for css/js/ttf |
| `app_shell.html` | All surface wiring via `rmGlyphs()` helpers |
| `scripts/smoke_glyph_wiring_1.py` | 17-check contract smoke |

## Surfaces wired

- **Wheel planets** — `formatGlyphSvgText("planet")` + AstroDotBasic `font-family` on SVG `<text>`
- **Wheel signs** — font glyphs at sign cusps (replaces stroke SVG `wheelZodiacSignSvg` at render site)
- **Wheel angles** — ASC/MC font glyphs; DSC/IC text fallback
- **PIH** — planet glyph prefix + sign glyph in longitude column
- **AIS** — angle glyph in label column; sign glyph in longitude display
- **A2A** — planet, aspect, and angle glyph columns (single + comparison matrix)
- **Comparison tables** — shared formatters (`formatTablePlanetNameHtml`, `aisFormatAngleDisplayHtml`, `formatA2aAspectLabelHtml`)
- **Relocated chart** — `renderRelocatedChartHtml` → wheel + PIH + AIS + A2A (all use shared helpers)
- **Profile page** — `renderProfileNatalChartHtml` → same stack as relocated chart

## Explicitly not wired

- `glyphAppearanceHtml()` settings stub — left unchanged (SETTINGS frozen)

## Smoke

```
python3 scripts/smoke_glyph_wiring_1.py
# OK: GLYPH-WIRING-1 (17 checks)
```

## Notes

- This is **temporary** production standardization only; no UX redesign.
- Unicode fallbacks apply when a glyph has no AstroDotBasic codepoint (e.g. DSC, IC, minor aspects not in font).
