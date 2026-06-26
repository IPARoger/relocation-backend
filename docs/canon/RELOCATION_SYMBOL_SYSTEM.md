# Relocation Symbol System — GL-1 Curation Canon

**Status:** Archaeology complete · **Mode:** Curation reference only  
**Date:** 2026-06-27  
**Scope:** Permanent glyph collection in `Fonts and Glyphs/` — likely final gather.

> This document does **not** choose production defaults, wire Settings, or implement code. It is the museum catalog for future Relocation Symbol System decisions.

---

## 1. Curatorial philosophy

We are **not** selecting one font. Professional symbol systems combine sources when stroke weight, proportion, and visual voice align.

**Priority order:**
1. Visual harmony across chart, tables, and map overlays
2. Consistent stroke weight and geometry at small sizes (16–24 px)
3. Legibility in dense PIH/AIS grids
4. Historical authenticity (secondary)

**Future principle:** One coherent Symbol System for the application. If the strongest family lacks symbols, **commission matching originals** rather than mixing incompatible voices.

---

## 2. Collection inventory

| Metric | Count |
|--------|------:|
| Source archives extracted | 37 (+ 5 loose font folders) |
| Classified SVG instances | 633 |
| Unique shapes (deduplicated by geometry hash) | 529 |
| Font files inventoried | 30+ |
| Capricorn unique silhouettes | 18 |

**Duplicates removed:** ~103 repeated shapes across Flaticon re-releases and duplicate zips (`636915-astrology` / `636915-astrology (2)`, `3184943-zodiac` pairs, etc.).

**Attribution:** See [validation/glyph_catalog/SOURCE_ATTRIBUTION.md](../validation/glyph_catalog/SOURCE_ATTRIBUTION.md) and per-package license files inside each archive.

**Visual index:** [validation/glyph_catalog/contact_sheets/](../validation/glyph_catalog/contact_sheets/)

---

## 3. Object taxonomy

### Planets (10)
Sun · Moon · Mercury · Venus · Mars · Jupiter · Saturn · Uranus · Neptune · Pluto

### Zodiac (12)
Aries through Pisces — **Capricorn** has the richest variant field (18 unique silhouettes in catalog).

### Angles (4)
ASC · MC · DSC · IC — **collection gap:** only `7372162-esoteric-astrology` provides a named ASC SVG; MC/DSC/IC largely absent from icon packs.

### Aspects (13+ in product spec)
Conjunction · Opposition · Square · Trine · Sextile · Quincunx · Semi-square · Semi-sextile · Sesquiquadrate · Quintile · Biquintile · Novile · Septile (where present)

**Note:** Many packs spell conjunction `conjuction` (typo preserved in filenames).

### Other
Nodes · Chiron · Part of Fortune · Vertex · Lilith · Ceres/Pallas/Juno/Vesta · miscellaneous astronomical marks.

---

## 4. Style families (natural groupings)

| Family | Character | Representative sources | Chart suitability |
|--------|-----------|------------------------|-------------------|
| **Technical / Swiss** | Even stroke, letter-keyed fonts, engineered proportions | `astrodotbasic` (AstroDotBasic), `widget-font`, `astro-gadget-font`, `symbola-font` | **High** — designed for UI density |
| **Classical / Engraved** | Traditional astrological line weight, filled silhouettes | `5019557-astrology`, `636915-astrology`, `5693107-astrology-and-zodiac-sign`, `3114479-astrology` | **High** — planets/signs excellent |
| **Minimal / Linear** | Hairline outline, scientific diagram tone | `14822510-zodiac-linear-black`, `16028722-astrology-outline`, `15643732/636` Spaces Science outline vols | **Medium** — aspects often missing |
| **Modern / Flat Solid** | Rounded solid icons, app-style | `13093396-zodiac`, `16628856-astrology`, `14586254-astrology` | **Medium** — friendly but less precise |
| **Esoteric / Ornamental** | Decorative curls, mystic framing | `9009913-esoteric`, `7125112-esoteric-astrology`, `1885317-esoteric` | **Low** for charts — strong for marketing |
| **Scientific / Universal** | Broad Unicode coverage | `symbola-font` (Symbola), `14195899-astronomical` | **Mixed** — completeness over harmony |
| **Calligraphic / Brush** | Hand-painted strokes | `AstrologyBrush`, `BeyondTheGalaxy_Font`, `16567980-the-art-of-symbols` | **Reject for charts** — decorative |
| **Horoscope / Pictorial** | Metaphor names (warrior, archer, scales) | `11890082-astrological-solid`, `5796257-horoscope` | **Reject** — not standard glyphs |

---

## 5. Package-level classification

Labels: **Production Candidate** · **Strong Alternative** · **Historical** · **Decorative** · **Reject**

### Production Candidate
| Package | Strengths | Weaknesses |
|---------|-----------|------------|
| **5019557-astrology** | Full planets (10/10), all signs, 10 aspect types incl. quincunx & semi-aspects; consistent filled classical voice | No angles; stroke slightly heavy at 16px |
| **astrodotbasic** (AstroDotBasic) | Already in product; excellent Swiss proportions; multi-variant Mars/Uranus/Pluto/Capricorn via letter keys | Aspects/angles not in font; private letter mapping not Unicode |

### Strong Alternative
| Package | Notes |
|---------|-------|
| **636915-astrology** | Near-complete classical set; 4 core aspects + conjunction; same family as 5019557 but thinner aspect coverage |
| **5693107-astrology-and-zodiac-sign** | Full planets/signs; 4 aspects; good Pluto/Uranus alternates |
| **widget-font** (Widget family) | Five weights + outline; excellent technical voice; already feels “product UI” |
| **symbola-font** | Universal scientific glyphs; complete Unicode astrology block | Visual voice is generic/system — less distinctive |
| **astro-font** / Astro-ZLzx | Euro Capricorn loop variant; pairs with AstroDotBasic US loop | Partial set only |
| **3114479-astrology** | Strong planets; 9 signs | Missing Leo/Scorpio/Pisces in SVG set |
| **16628856-astrology**, **13093396-zodiac**, **8620169-zodiac** | Modern flat; good mobile legibility | Weaker aspect completeness |

### Historical
Outline-only packs, partial zodiac sets, duplicate Flaticon releases with no new shapes.

### Decorative / Reject
`AstrologyBrush*`, `BeyondTheGalaxy_Font`, `5796257-horoscope` (pictorial), packs where >50% of icons are elements/tarot/stars rather than glyphs.

---

## 6. Per-glyph catalog notes (high-variance objects)

### Capricorn (18 variants)
| Observation | Packages to review |
|-------------|-------------------|
| US loop-tail (♑ with fish tail loop) | `astrodotbasic` char `j`, `636915-astrology`, `5019557-astrology` |
| Euro V-loop (Z-shaped horn) | `astro-font` Astro-ZLzx char `J`, several Flaticon zodiac packs |
| Simplified goat-fish hybrid | `7125112-esoteric-astrology`, `9009913-esoteric` |
| Heavy / cartoon tail | `5796257-horoscope` — **Reject** |

### Uranus (13 variants)
| Style | Sources |
|-------|---------|
| Herschel H atop circle | `astrodotbasic` `H`, `636915-astrology`, `5019557-astrology` |
| Linked circles / antenna | `astrodotbasic` `n`, `16628856-astrology` |
| Astronomical ♅ | `symbola-font`, occasional Flaticon packs |

### Pluto (19 variants)
| Style | Sources |
|-------|---------|
| PL monogram | `astrodotbasic` `J` (in production) |
| Traditional orb + crescent | **Gap** — production uses honest stub; review `636915`, `7125112`, `5693107` SVGs |
| P monogram variants | Several modern flat packs |

### Mars (11 variants)
| Style | Sources |
|-------|---------|
| Standard arrow ♂ | `astrodotbasic` `E`, classical packs |
| Venus-inverted (rotated ♀) | `astrodotbasic` `D` + transform |
| Shield/circle variants | `7125112-esoteric-astrology`, modern flats |

### Quincunx (2 unique SVG shapes)
| Source | Notes |
|--------|-------|
| `5019557-astrology` | Clean 150° glyph — **narrowed field leader** |
| `7372162-esoteric-astrology` | Alternate geometry — verify stroke match before pairing with 5019557 family |

---

## 7. Gap analysis

| Gap | Severity | Notes |
|-----|----------|-------|
| **Angles (ASC/MC/DSC/IC)** | Critical | Almost no pack includes all four; Symbola/Widget may cover via Unicode — needs font audit |
| **Aspects in Technical fonts** | High | AstroDotBasic/Widget lack aspect glyphs — must pair with Classical SVG family or extend |
| **Pluto traditional** | Medium | Many SVG candidates; no single family-quality match to AstroDotBasic yet |
| **Novile / Septile** | Medium | Rare in icon packs; 5019557 missing novile |
| **Conjunction naming** | Low | Typo `conjuction` in filenames — map in registry, not rename sources |
| **Metaphorical zodiac** | Low | `11890082` uses archer/warrior — unsuitable without manual remap |

### Family completeness matrix

| Family | Planets | Signs | Aspects | Angles | Verdict |
|--------|---------|-------|---------|--------|---------|
| Classical 5019557 | ✓ | ✓ | 10/13 | ✗ | Best **aspect-complete** SVG family |
| Technical AstroDotBasic | ✓ (font) | partial | ✗ | ✗ | Best **planet** voice; needs paired aspect family |
| Widget | partial | partial | ✗ | ? | Strong UI voice — audit cmap |
| Symbola | ✓ Unicode | ✓ | partial | partial | Completeness backstop |
| Minimal outline vols | partial | ✓ | ✗ | ✗ | Charts only with commission work |

---

## 8. Completion feasibility

| Family | Missing | Feasible to commission matching originals? | Reasoning |
|--------|---------|---------------------------------------------|-----------|
| **5019557 Classical** | Angles, novile/septile | **YES** | Stroke language is consistent; angles are simple letterforms |
| **AstroDotBasic Technical** | Aspects, angles, full zodiac in one file | **MAYBE** | Would require same designer or careful tracing; letter-key system is intentional |
| **Widget** | Full astrology set | **MAYBE** | Outline voice clear; large commission |
| **Esoteric ornamental** | N/A | **NO** | Too decorative; commissioning would fight the voice |
| **Brush / calligraphic** | N/A | **NO** | Unsuitable for chart grids |

---

## 9. Recommendations (narrow the field — no winners declared)

### Top three **complete visual systems** (for future unified system study)

1. **Classical Engraved — `5019557-astrology` family**  
   Broadest aspect coverage; pairs naturally with AstroDotBasic planets if strokes are normalized.

2. **Technical Swiss — `astrodotbasic` + `widget-font` composite**  
   Strongest product UI voice already partially in production; requires aspect/angle companion.

3. **Scientific Universal — `symbola-font` backstop**  
   Not the most beautiful, but complete Unicode astrology block for gap-filling during transition.

*Runner-up for pure zodiac/planet coherence:* `636915-astrology` / `5693107-astrology-and-zodiac-sign` (same voice, fewer aspects).

### Top five **individual glyphs** to shortlist (per object)

**Uranus**
1. AstroDotBasic Herschel `H`
2. AstroDotBasic simplified `n`
3. `636915-astrology` SVG
4. `5019557-astrology` SVG
5. `16628856-astrology` flat variant

**Pluto**
1. AstroDotBasic PL monogram `J`
2. `636915-astrology` SVG traditional
3. `5693107-astrology-and-zodiac-sign` SVG
4. `7125112-esoteric-astrology` SVG
5. `3114479-astrology` SVG

**Capricorn**
1. AstroDotBasic US loop `j`
2. Astro-ZLzx Euro `J`
3. `5019557-astrology` SVG
4. `636915-astrology` SVG
5. `13093396-zodiac` flat SVG

**Mars**
1. AstroDotBasic standard `E`
2. AstroDotBasic inverted Venus `D`
3. `5019557-astrology` SVG
4. `636915-astrology` SVG
5. `7125112-esoteric-astrology` SVG

**Quincunx**
1. `5019557-astrology` SVG
2. `7372162-esoteric-astrology` SVG
3. *(field thins — commission recommended if Classical family chosen)*
4. Symbola Unicode (audit)
5. Widget font audit (if aspect glyphs exist)

---

## 10. Classification legend (per-glyph labels)

| Label | Meaning |
|-------|---------|
| **Production Candidate** | Beautiful, legible, consistent — permanent product material |
| **Strong Alternative** | Legitimate user preference; may pair as variant |
| **Historical** | Interesting reference; not default |
| **Decorative** | Artwork, brushes, logos — not chart glyphs |
| **Reject** | Cartoonish, inconsistent weight, metaphorical, or illegible small |

Full thumbnails: `validation/glyph_catalog/thumbnails/`  
Per-shape metadata: `validation/glyph_catalog/catalog.json`

---

## 11. What we deliberately did not do (GL-1)

- No Settings / `glyph_selections` changes
- No production defaults chosen
- No new `@font-face` wiring
- No Unicode substitution policy changes

---

---

## GL-2 — Production Symbol Workshop (2026-06-27)

**Mode:** Read / evaluate / curate — no production wiring, no code changes.  
**Workshop:** [validation/glyph_catalog/gl2_workshop/](../validation/glyph_catalog/gl2_workshop/)  
**Doctrine cross-ref:** [PERIPHERAL_LEGIBILITY_DOCTRINE.md](PERIPHERAL_LEGIBILITY_DOCTRINE.md)

GL-2 reduces the GL-1 catalog into **five candidate Symbol Themes** — visual voices, not different products. Glyphs were normalized (24×24 viewBox, 2px padding, optical baseline) for comparison without technical distortion.

### Five candidate themes

| Theme | Voice | Primary source | Gaps | Shortlist |
|-------|-------|----------------|------|-----------|
| **Classical** | Filled engraved tradition | `5019557-astrology` + `636915-astrology` | 5 (angles, nodes, etc.) | **Yes** |
| **Refined** | Classical bodies + lighter outline aspects | `5019557` planets/signs + outline aspects | 6 | **Yes** |
| **Technical** | Swiss letter-keyed UI density | `AstroDotBasic` | 18 (aspects, angles, minors) | **Yes** |
| **Heritage** | 636915 + Symbola backstop | Mixed | 11 | No — voice fracture |
| **Contemporary** | Modern flat solid icons | `16628856-astrology` | 13 | No — too trendy |

### Normalization standard

All workshop glyphs compared at:

- **Optical size:** 16 / 20 / 24 / 32 px logical
- **Retina:** 2× devicePixelRatio review
- **ViewBox:** 24×24 with 2px padding
- **Baseline / stroke:** preserved from source; spacing normalized in wrapper

### Context surfaces tested

Natal chart wheel · relocated chart · comparison PIH table · map popup · settings glyph picker · notes inline · help copy · buttons · chips · legends.

See [context_comparison.html](../validation/glyph_catalog/gl2_workshop/mockups/context_comparison.html).

### Evaluation scores (1–10, workshop judgment)

| Criterion | Classical | Refined | Technical | Heritage | Contemporary |
|-----------|:---------:|:-------:|:---------:|:--------:|:------------:|
| Readability | 8 | 8 | 9 | 7 | 7 |
| Peripheral legibility | 7 | 8 | 9 | 7 | 6 |
| Timelessness | 9 | 9 | 8 | 8 | 5 |
| Scientific credibility | 8 | 9 | 8 | 7 | 6 |
| Premium feel | 8 | 9 | 8 | 6 | 6 |
| Restraint | 7 | 9 | 9 | 7 | 6 |
| Harmony with product | 7 | 8 | 10 | 6 | 5 |
| Disappears when not examined | 7 | 9 | 9 | 7 | 6 |
| No "look at me" | 8 | 9 | 9 | 7 | 6 |
| **Average** | **7.7** | **8.7** | **8.8** | **6.9** | **5.9** |

Full matrix: [score_matrix.html](../validation/glyph_catalog/gl2_workshop/comparison_sheets/score_matrix.html).

### Explicit rejections

| Theme | Reject reason |
|-------|---------------|
| **Heritage** | Symbola backstop creates mixed voice; fails single-system coherence |
| **Contemporary** | Too trendy, too expressive, weaker at 16px — conflicts with peripheral legibility doctrine |
| *(GL-1 rejects carry forward)* | Brush, horoscope pictorial, esoteric ornamental — decorative/magical/comic |

### Gap analysis & completion feasibility

| Theme | Missing symbols | Commission feasible? |
|-------|-----------------|---------------------|
| **Classical** | ASC/MC/DSC/IC, Chiron, nodes, Part of Fortune | **YES** — stroke language consistent; angles are simple letterforms |
| **Refined** | Same + outline harmonization for semi-aspects/novile | **YES** — editorial voice clear; needs disciplined designer brief |
| **Technical** | Full aspect set, angles, minors, nodes | **MAYBE** — letter-key system intentional; extending requires same designer |
| **Heritage** | 11 gaps even with Symbola | **NO** as unified theme — backstop prevents coherence |
| **Contemporary** | 13 gaps + voice mismatch with stone/paper materials | **NO** — would age poorly |

### Shortlist (2–3 production-ready themes — no winner declared)

1. **Technical** — highest product harmony; already partially shipped; needs aspect/angle companion family.
2. **Refined** — highest premium/restraint/peripheral legibility; best long-session instrument feel.
3. **Classical** — strongest native aspect completeness; slightly heavier at dense table sizes.

**Not shortlisted:** Heritage (mixed voice), Contemporary (too trendy).

### Workshop deliverables

| Asset | Path |
|-------|------|
| Workshop index | `validation/glyph_catalog/gl2_workshop/index.html` |
| Per-theme sheets | `gl2_workshop/comparison_sheets/{classical,refined,technical,heritage,contemporary}.html` |
| Context mockups | `gl2_workshop/mockups/context_comparison.html` |
| 16px shortlist | `gl2_workshop/mockups/shortlist_16px.html` |
| Normalized glyphs | `gl2_workshop/normalized/` |
| Machine data | `gl2_workshop/themes.json`, `gl2_workshop/scores/theme_scores.json` |

### Suggested next step (not GL-2)

**GL-3** — Side-by-side stroke audit of shortlist at production CSS sizes; commission brief for Technical aspect companion or Refined angle set.

*GL-2 complete. No implementation. No wiring.*

---

## GL-3 — Final Selection (2026-06-27)

**Mode:** Design curation + asset preparation — **no production wiring**.  
**Workshop:** [validation/glyph_catalog/gl3_final_selection/](../validation/glyph_catalog/gl3_final_selection/)  
**Doctrine:** [PERIPHERAL_LEGIBILITY_DOCTRINE.md](PERIPHERAL_LEGIBILITY_DOCTRINE.md)  
**Implementation deferred to GL-4.**

### V1 Symbol System

| Role | Theme ID | Folder | Production | Needs original |
|------|----------|--------|:----------:|:--------------:|
| **Default** | `refined` | `default_theme/` | 38 | 11 |
| Alternate 1 | `classical` | `alternate_theme_1/` | 39 | 10 |
| Alternate 2 | `technical` | `alternate_theme_2/` | 22 | 27 |
| Alternate 3 | `engraved` | `alternate_theme_3/` | 33 | 16 |
| Alternate 4 | `linear` | `alternate_theme_4/` | 37 | 12 |

All five themes are **related voices** within the Relocation instrument — classical/technical family, not separate products.

### Default: Refined

Selected for V1 default because it best matches peripheral legibility doctrine: traditional with an artistic bent, restrained, premium, disappears when not examined. Classical engraved planets and signs from `5019557-astrology` with outline aspect treatment.

### Alternates (user taste, same identity)

1. **Classical** — filled engraved; strongest native aspect coverage  
2. **Technical** — AstroDotBasic Swiss density; continuity with partial production  
3. **Engraved Light** — `636915-astrology` lighter classical sibling  
4. **Linear** — `16028722-astrology-outline` hairline; thinnest peripheral weight  

### Rejected from V1 set

Heritage (Symbola fracture), Contemporary (trendy/expressive), brush/calligraphic/esoteric ornamental families — per GL-1/GL-2.

### Asset standards (all themes)

| Property | Value |
|----------|-------|
| viewBox | `0 0 24 24` |
| Padding | 2px |
| Optical center | 12, 12 |
| Scale review | 16 / 20 / 24 / 32 px + 2× Retina |
| Naming | `{category}/{slug}.svg` |
| Path | `gl3_final_selection/{theme_folder}/{category}/{slug}.svg` |
| Missing glyphs | `data-status="needs_matching_original"` — dashed TBD cell, **not** Unicode substitute |

Vendor font binaries stay in `Fonts and Glyphs/` / `extracted/` — GL-3 ships SVG derivatives and references only.

### Missing symbol plan

Angles (ASC/MC/DSC/IC) require **matching originals** across all themes — acceptable commission work.  
See [missing_originals_brief.md](../validation/glyph_catalog/gl3_final_selection/missing_originals_brief.md).

No weak substitutes were used to fake completeness.

### Implementation notes (GL-4 scope)

- Wire `implementation_manifest.json` into glyph registry  
- Replace `needs_matching_original` SVGs as commissions complete  
- Settings theme picker: default + four alternates  
- Do **not** mix theme families within a single render surface  

### Validation

`scripts/smoke_gl3_symbol_selection.py` — 106 static checks (folders, manifest, categories, missing markers, no emoji/unicode substitutes, no font binaries in gl3).

*GL-3 complete. Production wiring explicitly deferred to GL-4.*

