# DIGNITIES-1A: Dignities + Diffs Visual Mockup Study

**Status:** Design study only — no implementation authorized  
**Date:** 2026-06-16  
**Amended:** 2026-06-16 — house-cell color-only dignity; no +/- indicators  
**Sources:**

- `results/119_dignities_diffs_display_doctrine_v1.md`
- `results/114_settings_doctrine_capture_v1.md`

**Goal:** Validate Dignities and Diffs display before DIGNITIES-1 implementation.

---

## Study Conventions

Mockups use ASCII wireframes. **Dignity is color on house-result cells only** — no `+`/`−` in real UI.

| Token | Meaning | Suggested CSS (study only) |
|-------|---------|----------------------------|
| `·` | Neutral house cell (no dignity) | default cell |
| `[S]` | Supportive dignity cell | `#eef7f3` fill / `#1a5c4a` dot or degree text |
| `[C]` | Challenging dignity cell | `#faf3e8` fill / `#7a4a12` dot or degree text |
| `[S′]` | Supportive, subtler shade (exaltation — optional v2) | lighter teal wash |
| `[C′]` | Challenging, subtler shade (fall — optional v2) | lighter amber wash |
| `░░` | Diff: identical across places (recede) | `#a8b0bb` text |
| `( )` | Mutual reception — neutral, not dignity color | `#8899aa` parentheses only |

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

**Rule:** Color applies to the **house-result cell** (● placement), not the planet name column.

### Variant 1 — Two-family color only (recommended)

```
┌─────────────────────────────────────────────────────────────────┐
│  Planet-in-House · Tokyo, Japan                                  │
├──────────┬────────┬────────┬────────┬────────┬────────┬─────────┤
│ Planet   │  H1    │  H2    │  H3    │  H4    │  H5    │  H6     │
├──────────┼────────┼────────┼────────┼────────┼────────┼─────────┤
│ Sun      │        │ [S]●   │        │        │        │         │  supportive cell
│ Moon     │   ●    │        │        │        │        │         │  neutral
│ Mercury  │        │        │ [C]●   │        │        │         │  challenging cell
│ Venus    │        │        │        │        │ [S]●   │         │
│ Mars     │        │        │        │        │        │ [C]●    │
│ Jupiter  │        │ [S]●   │        │        │        │         │
│ Saturn   │        │        │        │ [C]●   │        │         │
└──────────┴────────┴────────┴────────┴────────┴────────┴─────────┘
│  ☑ Dignities     Legend: teal wash = supportive  amber wash = challenging │
└─────────────────────────────────────────────────────────────────┘
```

**No +/- symbols.** User learns families from footer legend + optional tooltip on cell hover (rulership vs exaltation detail).

### Variant 2 — Subtle within-family cell shades (optional later)

Same as V1, but `[S]` vs `[S′]` differ only in wash depth (rulership vs exaltation); `[C]` vs `[C′]` for detriment vs fall. Still **no text indicators**.

### Variant comparison (study opinion)

| Criterion | V1 two-tone cells | V2 within-family shades |
|-----------|-------------------|-------------------------|
| Scan speed | Fast | Medium |
| Beginner | Clear | Needs legend once |
| Clutter | Lowest | Low if Δ shade ≤15% |
| Pro appearance | Clean | Acceptable for advanced |

---

## Mockup C## Mockup C — Comparison (Diffs OFF)

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
│ Jupiter  │ ░░[S]●░░    │ ░░[S]●░░    │ [C]●        │  dignity = cell color   │
│ Mercury  │ [C]●        │ ░░[C]●░░    │ ░░[C]●░░    │  diffs = muted text     │
│ Mars     │ ░░[C]●░░    │ [S]●        │ ░░[C]●░░    │                         │
└──────────┴─────────────┴─────────────┴─────────────┴─────────────────────────┘
│  ☑ Dignities                                                               │
└────────────────────────────────────────────────────────────────────────────┘
```

**Clutter assessment:** Acceptable when:

1. Dignity **colors house-result cells** only; planet labels stay neutral
2. Diffs grey **identical comparison values** in data cells; independent from dignity color
3. No `+`/`−` dignity glyphs — color carries supportive/challenging
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
│ Venus    │ ( [S]● )  │  [S]●   │  H4 ●   │
                    ↑
                    └── neutral parentheses around house cell only; color still = dignity
                        tooltip: "Mutual reception: Venus in Taurus, Mars in Libra"

**Clutter verdict:** Parentheses are **neutral** (grey), separate from teal/amber dignity fill.
Reject MR on planet label or dedicated MR column.

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

Two families on **house cells**, color-only, match doctrine. Ship Variant 1 first. No +/- UI.

### Question 2 — Does separate Ruler/Exalt/Fall/Detriment add value?

**Optional advanced layer later** (Settings → appearance), not v1 default.

Variant 2 adds value for **intermediate** users who already know dignity types; it does not justify four unrelated hues. If added later, use **shade/underline within family** only.

### Question 3 — Is Diffs readable without looking like a heatmap?

**Yes**, if identical cells use **muted text color only** (~#a8b0bb), not background fills, borders, or saturation ramps. Mockup D spec passes; reject cell background shading.

### Question 4 — Does Mutual Reception create noise?

**No**, if limited to **neutral parentheses** (or similar) beside the **house-result cell** with tooltip — and only when Settings gate is ON. Reject dedicated MR column.

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
/* Dignities — house-result cells, two families, color only */
.pih-cell.dignity-supportive { background: var(--dignity-support-bg, #eef7f3); }
.pih-cell.dignity-challenging { background: var(--dignity-challenge-bg, #faf3e8); }
/* planet label column: no dignity class */

/* Diffs — identical values in comparison cells */
.diff-same { color: var(--diff-muted, #a8b0bb); }

/* Mutual reception — future, neutral marker */
.pih-cell-mr-hint { color: var(--mr-neutral, #8899aa); }
```

---

## Amendment (house-cell styling)

Per DIGNITIES-1A feedback: dignity styling targets **PIH house-result cells**, not planet labels. Supportive/challenging is **color only** — no `+`/`−` in UI. Mutual reception, if enabled, uses a **minimal neutral marker** (e.g. parentheses); dignity state remains color-driven.

---

## Sign-off

This study satisfies DIGNITIES-1A deliverable requirements. **No production code.** Proceed to DIGNITIES-1 implementation per table in §Question 5.
