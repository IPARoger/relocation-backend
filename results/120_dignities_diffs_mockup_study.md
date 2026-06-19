# DIGNITIES-1A: Dignities + Diffs Visual Mockup Study

**Status:** Design study only — no implementation authorized  
**Date:** 2026-06-16  
**Sources:**

- `results/119_dignities_diffs_display_doctrine_v1.md`
- `results/114_settings_doctrine_capture_v1.md`

**Goal:** Validate Dignities and Diffs display before DIGNITIES-1 implementation.

---

## Study Conventions

Mockups use ASCII wireframes with **token labels** where color would apply in UI:

| Token | Meaning | Suggested CSS (study only) |
|-------|---------|----------------------------|
| `·` | Neutral (no dignity) | default text |
| `+` | Supportive family | `#1a5c4a` on `#eef7f3` (teal wash) |
| `++` | Supportive, stronger shade (rulership) | `#0f4a3a` on `#e3f2ec` |
| `+°` | Supportive, lighter shade (exaltation) | `#2d6b5a` on `#f0f8f5` |
| `−` | Challenging family | `#7a4a12` on `#faf3e8` (warm amber wash) |
| `−−` | Challenging, stronger (detriment) | `#6b3d0f` on `#f5ebe0` |
| `−°` | Challenging, lighter (fall) | `#8a5a20` on `#faf6ef` |
| `░░` | Diff: identical across places (recede) | `#c8cdd4` text / 38% opacity |
| `MR` | Mutual reception marker | parentheses or 6px dot + tooltip |

Sample data: **Anna Rivera** comparison — **Tokyo** vs **Singapore** vs **Portland** (3-place PIH slice).

---

## Mockup A — PIH Table (Baseline)

**State:** Dignities **OFF** · Diffs **OFF** · Single relocated chart (Tokyo)

```
┌─────────────────────────────────────────────────────────────────┐
│  Comparison · Anna Rivera                    [ AIS ] [ PIH ] …   │
├─────────────────────────────────────────────────────────────────┤
│  Planet-in-House · Tokyo, Japan                                  │
├──────────┬────────┬────────┬────────┬────────┬────────┬─────────┤
│ Planet   │  H1    │  H2    │  H3    │  H4    │  H5    │  H6     │
├──────────┼────────┼────────┼────────┼────────┼────────┼─────────┤
│ Sun      │        │   ●    │        │        │        │         │
│ Moon     │   ●    │        │        │        │        │         │
│ Mercury  │        │        │   ●    │        │        │         │
│ Venus    │        │        │        │        │   ●    │         │
│ Mars     │        │        │        │        │        │    ●    │
│ Jupiter  │        │   ●    │        │        │        │         │
│ Saturn   │        │        │        │   ●    │        │         │
└──────────┴────────┴────────┴────────┴────────┴────────┴─────────┘
│  ☐ Dignities                                    ← footer, OFF    │
└─────────────────────────────────────────────────────────────────┘
```

**Notes:** House membership only. No dignity glyphs, colors, or relationship labels. This is the **control** — current acceptable PIH density.

---

## Mockup B — PIH Table (Dignities ON)

Same Tokyo PIH. Footer: `☑ Dignities`

Planet rows show **sign placement** (abbreviated) with dignity family applied to the **planet label** or trailing marker — not a second table.

### Variant 1 — Positive / Negative only (two families)

```
┌─────────────────────────────────────────────────────────────────┐
│  Planet-in-House · Tokyo, Japan                                  │
├──────────┬────────┬────────┬────────┬────────┬────────┬─────────┤
│ Sun +    │        │  H2 ●  │        │        │        │         │  Leo · supportive
│ Moon ·   │  H1 ●  │        │        │        │        │         │
│ Mercury −│        │        │  H3 ●  │        │        │         │  Pisces · challenging
│ Venus +  │        │        │        │        │  H5 ●  │         │  Taurus · supportive
│ Mars −   │        │        │        │        │        │  H6 ●   │  Cancer · challenging
│ Jupiter +│        │  H2 ●  │        │        │        │         │  Cancer · supportive (exalt)
│ Saturn − │        │        │        │  H4 ●  │        │         │  Aries · challenging
└──────────┴────────┴────────┴────────┴────────┴────────┴─────────┘
│  ☑ Dignities                                                     │
└─────────────────────────────────────────────────────────────────┘

Legend (footer, collapsed by default):
  + supportive (rulership & exaltation)    − challenging (detriment & fall)
```

**Visual:** One teal wash for all `+`, one warm amber wash for all `−`. Sign name in muted meta on hover/tooltip only.

### Variant 2 — Subtle within-family distinction

```
│ Sun ++       │  Leo      rulership
│ Jupiter +°   │  Cancer   exaltation
│ Mercury −−   │  Pisces   detriment
│ Mars −°      │  Cancer   fall
```

Same two hue families; **rulership/detriment** slightly deeper saturation; **exaltation/fall** slightly lighter + optional thin underline vs dotted underline (not a third color).

```
│  ☑ Dignities     + ruler/exalt   − detriment/fall   (i tooltip)
```

### Variant comparison (study opinion)

| Criterion | V1 two-tone | V2 within-family |
|-----------|-------------|------------------|
| Scan speed | Faster | Slightly slower |
| Beginner | Clearer | Needs legend once |
| Clutter | Lower | Low if shade delta ≤15% |
| Pro appearance | Clean | Acceptable for advanced users |

---

## Mockup C — Comparison (Diffs OFF)

**State:** 3-place comparison · AIS table first · Diffs **OFF**

```
┌────────────────────────────────────────────────────────────────────────────┐
│  Angles-in-Signs · Anna Rivera                                               │
├─────────────┬──────────────────┬──────────────────┬──────────────────────┤
│ Angle       │ Tokyo            │ Singapore        │ Portland             │
├─────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ ASC         │ 14° Leo          │  2° Virgo        │  8° Scorpio          │
│ MC          │  3° Taurus       │ 18° Gemini       │ 22° Leo              │
│ DSC         │ 14° Aquarius     │  2° Pisces       │  8° Taurus           │
│ IC          │  3° Scorpio      │ 18° Sagittarius  │ 22° Aquarius         │
└─────────────┴──────────────────┴──────────────────┴──────────────────────┘
│  ☐ Diffs                                                                   │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Planet-in-House · (scroll)                                                 │
│  … full density, all cells equal weight …                                   │
│  ☐ Dignities                                                               │
└────────────────────────────────────────────────────────────────────────────┘
```

**Reference:** Every cell same visual weight. User scans all columns.

---

## Mockup D — Comparison (Diffs ON)

Same data. **Diffs ON** (global — applies to AIS, PIH, A2A, etc.)

```
┌────────────────────────────────────────────────────────────────────────────┐
│  Angles-in-Signs                                                            │
├─────────────┬──────────────────┬──────────────────┬──────────────────────┤
│ Angle       │ Tokyo            │ Singapore        │ Portland             │
├─────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ ASC         │ 14° Leo          │ ░░ 2° Virgo ░░   │ ░░ 8° Scorpio ░░     │  ← all differ
│ MC          │ ░░ 3° Taurus ░░  │ ░░ 18° Gemini ░░ │ ░░ 22° Leo ░░        │  ← all differ
│ DSC         │ 14° Aquarius     │ ░░ 2° Pisces ░░  │ ░░ 8° Taurus ░░      │
│ IC          │ ░░ 3° Scorpio ░░ │ ░░ 18° Sag ░░    │ ░░ 22° Aquarius ░░   │
└─────────────┴──────────────────┴──────────────────┴──────────────────────┘
│  ☑ Diffs                                                                   │
└────────────────────────────────────────────────────────────────────────────┘
```

**Example row where two places match** (PIH excerpt, Diffs ON):

```
│ Venus │ H5 ● │ H5 ● │ ░░ H5 ● ░░ │   ← Tokyo & Singapore identical → recede
│       │      │      │  (or only   │      Portland differs → stays full contrast
│       │      │      │   Portland  │
│       │      │      │   column    │
│       │      │      │   readable) │
```

**Greying spec (recommended):**

- Identical **value** across compared places → `color: #a8b0bb` (~55% of body contrast), **not** background heatmap
- Row label (planet/angle) stays full contrast
- No bolding of “winners”; no red/green

**Anti-pattern (rejected):**

```
│ Venus │ ███ H5 │ ░░ H5 ░░ │ ░░ H5 ░░ │  ← looks like heatmap / scoring
```

---

## Mockup E — Combined Usage

**State:** Diffs **ON** + PIH Dignities **ON** (3-place comparison)

```
┌────────────────────────────────────────────────────────────────────────────┐
│  AIS (Diffs ON — identical angle rows receded)                    ☑ Diffs  │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Planet-in-House                                                            │
├──────────┬─────────────┬─────────────┬─────────────┬─────────────────────────┤
│          │ Tokyo       │ Singapore   │ Portland    │                         │
├──────────┼─────────────┼─────────────┼─────────────┼─────────────────────────┤
│ Jupiter +│ ░░ H2 ● ░░  │ ░░ H2 ● ░░  │  H4 ●       │  dignity on label only  │
│ Mercury −│  H3 ●       │ ░░ H3 ● ░░  │ ░░ H3 ● ░░  │  diffs on cells         │
│ Mars −   │ ░░ H6 ● ░░  │  H8 ●       │ ░░ H6 ● ░░  │                         │
└──────────┴─────────────┴─────────────┴─────────────┴─────────────────────────┘
│  ☑ Dignities                                                               │
└────────────────────────────────────────────────────────────────────────────┘
```

**Clutter assessment:** Acceptable when:

1. Dignity affects **planet name column only** (one column), not every house cell
2. Diffs grey **data cells** only, not planet labels
3. Footer toggles remain separated (see below)

**Risk:** Combining both on dense 5-place PIH — recommend max 5 places unchanged; if cluttered, Diffs already reduces noise by hiding identical cells.

---

## Footer Placement Study

```
┌─ AIS section ─────────────────────────────────────────────┐
│  [ table … ]                                               │
│  ─────────────────────────────────────────────────────── │
│  ☐ Diffs                              ← ONLY global diff   │
└────────────────────────────────────────────────────────────┘

        ↓ scroll ↓

┌─ PIH section ────────────────────────────────────────────┐
│  [ table … ]                                               │
│  ─────────────────────────────────────────────────────── │
│  ☐ Dignities                          ← PIH-only         │
└────────────────────────────────────────────────────────────┘

┌─ A2A section ─────────────────────────────────────────────┐
│  [ table … ]                                               │
│  (no footer — Diffs already ON from AIS)                   │
└────────────────────────────────────────────────────────────┘
```

**Verification:** Toggles are **vertically separated** by section scroll; labels are short; no shared footer bar. Diffs never appears beside Dignities.

**Rejected layout:**

```
│  ☐ Diffs   ☐ Dignities   │  ← colocated — doctrine violation
```

---

## Mutual Reception Study (Settings-Gated, Not Implemented)

**Assume:** Settings → Show Mutual Reception = **ON** · PIH Dignities = **ON**

```
│ Venus + (MR↔Mars)  │  H5 ●  │  H5 ●  │  H4 ●  │
       ↑
       └── "(MR↔Mars)" in #8899aa, 0.85em, OR 6px interlocked dot with tooltip:
           "Mutual reception: Venus in Taurus, Mars in Libra"
```

**Alternative (cleanest):**

```
│ Venus +*  │  …   │   * = single subtle asterisk, tooltip only, no inline prose
```

**Clutter verdict:** Acceptable **at most one marker per planet row**; reject extra MR column or badge chips.

---

## Evaluation Matrix

| Mockup | Readability | Scan speed | Visual weight | Professional | Beginner-friendly | Clutter risk |
|--------|-------------|------------|---------------|--------------|-------------------|--------------|
| **A** Baseline | Excellent | Fast | Light | High | High | None |
| **B V1** 2-family | Very good | Fast | Light+ | High | High | Low |
| **B V2** 4-shade | Good | Medium | Medium | High | Medium | Low–medium |
| **C** Diffs OFF | Excellent | Medium | Heavy (full) | High | High | None |
| **D** Diffs ON | Very good | **Faster** for diffs | Light on diffs | High | Good | Low if grey subtle |
| **E** Combined | Good | Good | Medium | High | Medium | Medium (manageable) |
| **MR** marker | Good | Neutral | Minimal | High | Needs tooltip | Low if one glyph |

---

## Recommendations

### Question 1 — Is Positive/Negative only sufficient?

**Yes for DIGNITIES-1 default.**

Two families match doctrine, minimize beginner cognitive load, and keep PIH scannable. Ship Variant 1 first.

### Question 2 — Does separate Ruler/Exalt/Fall/Detriment add value?

**Optional advanced layer later** (Settings → appearance), not v1 default.

Variant 2 adds value for **intermediate** users who already know dignity types; it does not justify four unrelated hues. If added later, use **shade/underline within family** only.

### Question 3 — Is Diffs readable without looking like a heatmap?

**Yes**, if identical cells use **muted text color only** (~#a8b0bb), not background fills, borders, or saturation ramps. Mockup D spec passes; reject cell background shading.

### Question 4 — Does Mutual Reception create noise?

**No**, if limited to a **single subtle marker** (parentheses, asterisk, or dot) on the planet label with tooltip — and only when Settings gate is ON. Reject dedicated MR column.

### Question 5 — What should DIGNITIES-1 actually implement?

| Item | DIGNITIES-1 scope |
|------|-------------------|
| PIH footer toggle **Dignities** | Yes — default OFF |
| Two-family dignity styling (V1) | Yes |
| Data-driven dignity lookup | Yes — no hard-coded sprawl |
| PIH comparison + single-chart PIH | Yes |
| **Diffs** footer on AIS | Yes — default OFF, global state |
| Identical-cell grey (text-only) | Yes |
| Mutual reception UI | **No** — settings + UI deferred |
| Four-color dignity | **No** |
| Map / popup / search dignity | **No** |
| Interpretive Hints | **No** |
| Scoring / ranking / strength shading | **No** |

---

## Suggested Implementation Tokens (Reference for DIGNITIES-1)

```css
/* Dignities — two families */
.dignity-supportive { color: var(--dignity-support-fg, #1a5c4a); }
.dignity-challenging { color: var(--dignity-challenge-fg, #7a4a12); }

/* Diffs — identical cells */
.diff-same { color: var(--diff-muted, #a8b0bb); }

/* Mutual reception — future */
.dignity-mr-hint { opacity: 0.75; font-size: 0.85em; }
```

---

## Sign-off

This study satisfies DIGNITIES-1A deliverable requirements. **No production code.** Proceed to DIGNITIES-1 implementation per table in §Question 5.
