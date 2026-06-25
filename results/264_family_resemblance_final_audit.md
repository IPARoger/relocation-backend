# 264 — Family Resemblance Final Audit (H10)

**Date:** 2026-06-26  
**Authority:** `docs/canon/MATERIAL_SYSTEM_CANON.md` (D1), `docs/design/family_resemblance_exploration_2_9a.md`, `UI_STANDARDIZATION_CANON_v1_2026-06-12.md`  
**Method:** Targeted review of production surfaces in `app_shell.html` and canonical modules — not full-repository archaeology.

---

## Executive summary

**Profile, Relocated, and Comparison V5** form the reference instrument family: shared stone ground (`--rm-paper` gradients), G3 table cards (`tband_foundation.css`), serif authority plates, Avenir body, Notes canonical composer, and recessed shell chrome.

**Settings, Help, Notes Library, and Map** were the primary outliers. H10 applies a shared `rm-instrument-surface` layer to administrative and reading routes and wires the dormant `CityIntelligenceCanonical` module for renderer parity on Comparison CI.

**Map** remains the largest unresolved gap — separate prototype lineage (`map_CURRENT.html` / Genie v6) per `263_material_system_delta.md` P0.

---

## Scoring key

| Score | Meaning |
|-------|---------|
| **Aligned** | Matches Material Canon and beta reference |
| **Partial** | Same family intent; localized gaps |
| **Outlier** | Different visual language or chrome |

Dimensions: Typography · Materials · Controls · Motion · Spacing · Chrome · Hierarchy · Reading comfort · Interaction rhythm

---

## 1. Map

| Dimension | Score | Finding |
|-----------|-------|---------|
| Typography | Partial | Genie v6 explores profile-grammar plate; production map not harmonized |
| Materials | Outlier | Geography-owned ground; not stone/paper instrument stack |
| Controls | Partial | Native selects + sidebar prototype; D2 dropdown family not site-wide |
| Motion | Partial | Genie choreography specified (v6); production differs |
| Spacing | Outlier | Sidebar density unlike chart pages |
| Chrome | Outlier | Full topbar vs dissolved explore chrome on beta |
| Hierarchy | Aligned | Map-first doctrine correct; material treatment diverges |
| Reading comfort | Partial | Popup typography adequate; not unified with plate system |
| Interaction rhythm | Partial | Teaching-paced Genie intent not fully propagated |

**Verdict:** Purpose-correct; **material family not aligned**. Deferred to dedicated map harmonization pass (not H10 scope).

---

## 2. Profile

| Dimension | Score | Finding |
|-----------|-------|---------|
| Typography | Aligned | Avenir 15.5px body; Iowan name plate |
| Materials | Aligned | Stone ground, paper `tcard`, G3 glow |
| Controls | Aligned | D2-style profile selector; left caret collapse |
| Motion | Partial | Table collapse per doctrine; not all motions wired |
| Spacing | Aligned | Fibonacci t-band grid 8·8·13·5 |
| Chrome | Aligned | Banner hidden; compact nav |
| Hierarchy | Aligned | Wheel focal; tables structural |
| Reading comfort | Aligned | Fixed row rhythm; lines-only |
| Interaction rhythm | Aligned | Contemplative pacing |

**Verdict:** **Reference surface** for the instrument family.

---

## 3. Relocated

| Dimension | Score | Finding |
|-----------|-------|---------|
| Typography | Aligned | Matches Profile stack |
| Materials | Aligned | Same stone ground and tcard |
| Controls | Aligned | City selector D2 family |
| Motion | Partial | Same as Profile |
| Spacing | Aligned | Zone C location emphasis without breaking grid |
| Chrome | Aligned | Beta chrome recession |
| Hierarchy | Aligned | Guest card register; intel block subordinate |
| Reading comfort | Aligned | Intel rows compact reference tone |
| Interaction rhythm | Aligned | |

**Verdict:** **Aligned** with Profile. Inline CI block styling present; canonical renderer depends on script wiring.

---

## 4. Comparison (V5)

| Dimension | Score | Finding |
|-----------|-------|---------|
| Typography | Aligned | Matches chart pages; AIS/PiH/A2A formats locked |
| Materials | Aligned | Stone ground, G3, column hatch |
| Controls | Aligned | City bar, angle pills, notes rail |
| Motion | Partial | Carousel slide; table collapse |
| Spacing | Aligned | V5 beta column breathing room |
| Chrome | Aligned | `rm-beta-compare` + `rm-compare-v5-canonical` |
| Hierarchy | Aligned | City bar → tables → CI → notes species order |
| Reading comfort | Aligned | Hatch separation; no winner coloring |
| Interaction rhythm | Aligned | |

**Verdict:** **Aligned**. CI inline previously fell back to placeholder snippets when `CityIntelligenceCanonical` unloaded — fixed in H10.

---

## 5. Notes

| Dimension | Score | Finding |
|-----------|-------|---------|
| Typography | Aligned | `notes_canonical.css` — 14.5px / 1.55 |
| Materials | Aligned | Paper field, quiet toolbar |
| Controls | Aligned | Shared toolbar all surfaces |
| Motion | Partial | Pop-out morph doctrine; polish deferred |
| Spacing | Aligned | Species separation in t-band |
| Chrome | Aligned | Toolbar below editor |
| Hierarchy | Aligned | Notes subordinate to tables |
| Reading comfort | Aligned | Premium publishing intent |
| Interaction rhythm | Aligned | |

**Verdict:** **Aligned** (H7 canonicalization complete).

---

## 6. Settings

| Dimension | Score | Finding |
|-----------|-------|---------|
| Typography | Partial | Sans metadata good; lacked serif section authority on landing |
| Materials | Partial | H6 paper panels started; stone ground and `--rm-*` tokens missing |
| Controls | Partial | Warm stubs; nav active state used generic `#eff6ff` blue |
| Motion | N/A | Minimal |
| Spacing | Aligned | H6 subsection rhythm |
| Chrome | Outlier | Shell banner + default header visible |
| Hierarchy | Aligned | 7-section IA clear |
| Reading comfort | Partial | Administrative read OK; felt like separate app |
| Interaction rhythm | Partial | |

**Verdict:** **Partial** → H10 applies `rm-instrument-surface` + warm nav/panel tokens.

---

## 7. City Intelligence

| Dimension | Score | Finding |
|-----------|-------|---------|
| Typography | Partial | `city_intelligence_canonical.css` uses generic `--ink`/`--muted` fallbacks |
| Materials | Partial | Full page layout approved; `--rm-*` mapping incomplete |
| Controls | Partial | Accordion progressive disclosure on full page |
| Motion | Aligned | 200ms ease accordion — human-scale |
| Spacing | Aligned | Canon length budgets respected in module |
| Chrome | N/A | Content-forward |
| Hierarchy | Aligned | CI subordinate to astrology tables |
| Reading comfort | Aligned | Neutral reference prose |
| Interaction rhythm | Aligned | |

**Verdict:** **Partial** — module exists; script/CSS unwired from shell before H10. Full page route still pending (H8). Renderer wiring is harmonization, not new feature.

---

## 8. Help

| Dimension | Score | Finding |
|-----------|-------|---------|
| Typography | Outlier | Generic `h2`/`panel` — no Iowan/Avenir split |
| Materials | Outlier | Default `--panel` on cold app shell |
| Controls | Partial | Basic buttons; no TOC/search (H9 deferred) |
| Motion | N/A | |
| Spacing | Partial | Unbounded width |
| Chrome | Outlier | Full debug chrome visible |
| Hierarchy | Partial | Logical sections; not field-guide layout |
| Reading comfort | Partial | Readable but "software help" tone |
| Interaction rhythm | Outlier | Felt like utility screen |

**Verdict:** **Outlier** → H10 applies `rm-handbook-root` reading surface (full H9 handbook deferred).

---

## Shared DNA checklist (Tier 1 spine)

| Trait | Profile | Relocated | Compare | Notes | Settings | Help | Map | CI |
|-------|---------|-----------|---------|-------|----------|------|-----|-----|
| Stone ground | ✓ | ✓ | ✓ | ✓ | H10 | H10 | ✗ | partial |
| `--rm-*` ink tokens | ✓ | ✓ | ✓ | ✓ | H10 | H10 | ✗ | partial |
| Chrome recession | ✓ | ✓ | ✓ | ✓ | H10 | H10 | ✗ | — |
| Serif/sans hierarchy | ✓ | ✓ | ✓ | ✓ | partial | H10 | partial | partial |
| Paper cards | ✓ | ✓ | ✓ | ✓ | H10 | H10 | ✗ | ✓ |
| G3 table glow | ✓ | ✓ | ✓ | — | — | — | — | — |
| Canonical module | — | — | V5 route | NotesCanonical | — | — | — | H10 wire |

---

## H10 fixes applied (high-confidence only)

1. **`theme/family_resemblance.css`** — shared `body.rm-instrument-surface` stone ground, chrome recession, warm controls.
2. **Route wiring** — instrument class on chart-record, chart, compare, settings, help, notes-library, profiles.
3. **Settings/Notes Library** — warm active/hover states replace generic blue tints.
4. **Help** — `rm-handbook-root` wrapper + paper panels (reading comfort, not full handbook).
5. **CI canonical** — link `city_intelligence_canonical.js` + `.css` so Comparison uses shared renderer (no placeholder snippets).

## Explicitly deferred (not H10)

- Map harmonization pass
- Full Help handbook (H9): TOC, search, progressive disclosure, illustrations
- Full CI page route + relocated inline hydration (H8)
- D2 material/color tokens
- Button/link formalization (#7–#8 UI canon)
- Removing duplicated stone-ground CSS from per-route `body.rm-beta-*` blocks (cosmetic DRY; low risk left for D2)

---

## Revision log

| Date | Note |
|------|------|
| 2026-06-26 | H10 final family resemblance audit + targeted harmonization |
