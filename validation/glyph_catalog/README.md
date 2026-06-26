# GL-1 — Relocation Glyph Catalog

Archaeology and curation workspace for the permanent glyph collection. **Not wired to production.**

## Contents

| Path | Purpose |
|------|---------|
| `extracted/` | Unpacked archives from `Fonts and Glyphs/` (37 zip sources + loose font folders) |
| `thumbnails/` | Deduplicated SVG thumbnails grouped by category/object |
| `contact_sheets/` | HTML contact sheets — open in browser |
| `catalog.json` | Machine-readable inventory (531 unique classified shapes from 634 instances) |
| `SOURCE_ATTRIBUTION.md` | Per-package attribution index |

## Contact sheets

Open in a browser:

- [Packages overview](contact_sheets/packages_overview.html)
- [Planets](contact_sheets/planets.html)
- [Signs](contact_sheets/signs.html)
- [Aspects](contact_sheets/aspects.html)
- [Angles](contact_sheets/angles.html)
- [Other](contact_sheets/others.html)

## GL-3 Final Selection

[gl3_final_selection/](gl3_final_selection/) — V1 default (Refined) + 4 alternates. GL-4 implements.

## GL-2 Workshop

[gl2_workshop/](gl2_workshop/) — five candidate Symbol Themes, normalized comparison, context mockups.

## Canon

Authoritative curation narrative: [docs/canon/RELOCATION_SYMBOL_SYSTEM.md](../../docs/canon/RELOCATION_SYMBOL_SYSTEM.md)

## Regenerate

```bash
python3 scripts/build_glyph_catalog.py   # if added later
```

Catalog was built during GL-1 via inline archaeology scripts (2026-06-27).
