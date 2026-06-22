# INFORMATION-HIERARCHY-STUDY-1 — First-Principles Secondary Information

**Date:** 2026-06-22  
**Mode:** Research + visual study only (no production code)  
**Study file:** `validation/mockups/beta/information_hierarchy_study_1.html`  
**Context:** Prior diffs studies (214, 220, 222) converged on grey ink, opacity avoidance, or cell-local washes. This study **does not assume** any of those are correct. It begins from how professional dense-information systems achieve *"easy to ignore, instantly recoverable"* without a disabled register.

**Scenario cities:** Boston, MA · New York, NY · Omaha, NE — east-coast high-duplicate pair plus divergent control column.

---

## 1. The design problem (stated without solutions)

When Comparisons Diffs are ON, some cells contain **facts that repeat across cities** (e.g. Sun house 10 in both Boston and New York). The user's primary scan should surface **what differs** (Omaha's 11th house, different A2A orbs). The repeated facts must remain:

| Requirement | Meaning |
|-------------|---------|
| Visible when intentionally scanned | Full legibility on deliberate fixation |
| Ignorable during primary scanning | Low salience in peripheral / gist pass |
| Never hidden | No `display:none`, no off-layer plotting, no tooltip-only facts |
| Never disabled | No faded-to-unreadable, no strikethrough, no "inactive" chrome |
| Never treated as unimportant | Data is true and current — only its *attention rank* changes |

**Target phrase:** *easy to ignore, instantly recoverable* — not *de-emphasized because less true*.

Production today (`.rm-cmp-diff-duplicate`: `opacity: 0.48; color: #64748b`) violates the last three rows: it reads disabled, fights dignity tints, and collapses hue + luminance + weight together.

---

## 2. Reference systems — what they actually do

### 2.1 Bloomberg Terminal

- **Channel separation:** Meaning encoded in **color family** (amber = caution, green = positive, red = negative); static fields stay in a **narrow luminance band** but remain fully opaque.
- **Hierarchy tool:** **Field grouping** and column alignment, not row fade. Unchanged quote fields don't disappear — adjacent changed fields draw attention by **motion and hue jump**.
- **Lesson:** Highlight *delta*, demote *stable* via **contextual surround**, not amplitude collapse on the stable value itself.

### 2.2 GIS (ArcGIS, QGIS)

- **Layer order + symbology:** Secondary layers use **thinner stroke**, **dashed linestyle**, **lower saturation fill** — each channel independent.
- **Hatching:** Repeating micro-pattern denotes "same class / background" without removing geometry.
- **Lesson:** **Edge treatment + pattern** can mark "reference class" while fill and label stay readable.

### 2.3 CAD (AutoCAD, Revit)

- **Lineweight scale:** 0.13 mm vs 0.35 mm — same ink color, different **stroke weight** hierarchy.
- **Linetype:** Dashed = construction/reference; solid = design intent — **structure** not grey.
- **Lesson:** Weight and linestyle are primary hierarchy levers; color often unchanged.

### 2.4 Scientific atlases (Gray's, brain atlases)

- **Leader lines:** Thin, low-contrast connectors; **labels** remain full ink when read.
- **Cross-hatching:** Region equivalence shown by **texture**, not label deletion.
- **Lesson:** **Micro-pattern in ground**, not in glyph, preserves figure-ground.

### 2.5 Editorial infographics (NYT, FT)

- **Typographic scale:** Secondary annotations one step smaller in **optical size**, often wider tracking — still black/near-black.
- **Ink budget:** Primary headline heavy; data labels regular — **no 50% opacity body copy**.
- **Lesson:** **Size + weight + tracking** before hue fade.

### 2.6 Financial dashboards (TradingView, FactSet)

- **Unchanged metrics:** Prior close shown in **tabular nums, regular weight**; change column gets color.
- **Heat only where delta:** Cell background heatmap for variance; static cells **paper-white**.
- **Lesson:** **Reserve chroma for delta**; stable cells neutral but opaque.

### 2.7 Transit maps (Vignelli, TfL)

- **Route hierarchy:** Express = thick stroke; local stops = **smaller type**, same ink.
- **Duplicate station names:** Disambiguated by **position and weight**, not greying one city name away.
- **Lesson:** **Scale and weight** encode importance; color encodes line identity, not "off".

### 2.8 Air traffic control (STARS, ERAM)

- **Data blocks:** Routine traffic in **cool, compact** blocks; alerts **bright, larger, bordered**.
- **Never "disabled" aircraft:** All targets visible; **attention** via blink/border/size — not removal.
- **Lesson:** **Enclosure and border luminance** signal urgency; routine stays fully visible.

### 2.9 Professional charting (Solar Fire, Astro.com print)

- **Aspect lines:** Minor aspects thinner/dashed; major solid — **geometry weight**.
- **Degree text:** Often smaller than planet glyph; glyph stays full contrast.
- **Lesson:** **Split elements within a cell** — glyph/orb can stay primary while house digit demotes.

### 2.10 Cross-cutting principle

Professional systems **demote one visual channel at a time** while holding others at full fidelity. Collapsing all channels (opacity) is the amateur shortcut — it mimics disabled UI from form design, not instrument design.

---

## 3. Evaluation of ten hierarchy dimensions

Each dimension is scored for PIH (single-digit house, dignity tints) and A2A (aspect word + colored orb) applicability.

| # | Dimension | Mechanism | PIH fit | A2A fit | Risk if misused |
|---|-----------|-----------|---------|---------|-----------------|
| 1 | **Ink hierarchy** | Hue/value of glyph only | Good if **warm-shift** not cool-grey | Good on aspect word, not orb | Cool grey reads "disabled" on warm paper |
| 2 | **Saturation hierarchy** | Desaturate toward paper, keep luminance | Excellent on digits over dignity tint | Good on aspect label | Over-desat → grey metaphor |
| 3 | **Figure-ground** | Micro-wash behind glyph, glyph full ink | Excellent — tint + wash compose | Good | Row-wide wash → zebra/selection |
| 4 | **Local contrast** | Weight 400 vs 600; size −0.5–1px | Excellent for 1–2 digit houses | Excellent split: word demote, orb primary | Too light → illegible |
| 5 | **Edge treatments** | Inset hairline, corner ticks, bracket | Good grouping cue | Strong for dup pairs | Grid noise if on every cell |
| 6 | **Texture / micro-patterns** | Paper grain, 3% noise in cell | Good on neutral dignity cells | Moderate | Can muddy small type |
| 7 | **Peripheral vision cues** | Tracking, size, spacing | High — gist reads "lighter column" | High on aspect tokens | Letter-spacing alone too weak on PIH |
| 8 | **Color-temperature shift** | Ink toward `--paper` hue, not neutral grey | Better palette integration than grey | Use on words only | Wrong direction (cool) pops |
| 9 | **Density-based** | Tighter column when mostly dup | Poor — misleading | Poor | Implies less data |
| 10 | **Cell-local** | All techniques scoped to `<td class="dup-cell">` | **Required** | **Required** | Row/column scope → selection metaphor |

### 3.1 Ink hierarchy — not assumed correct

Ink shift works when it is **analogous hue movement** (ink → paper-warm) at **full opacity**, not arbitrary `#64748b`. Bloomberg and FT keep text near black; GIS shifts **saturation** before **value**.

**PIH:** Prefer saturation reduction or warm-shift over cool grey.  
**A2A:** Demote aspect **word** ink; orb keeps applying/separating hue.

### 3.2 Saturation hierarchy — often underrated

Desaturating duplicate digits toward `--paper` (`color-mix(in srgb, var(--ink) 72%, var(--paper))`) preserves dignity cell readability better than neutral grey because the digit stays in the **palette family**.

### 3.3 Figure-ground hierarchy

Cell-local `::before` inset wash at 3–4% ink (not 10%+) pushes duplicate cells **visually backward** without touching glyph contrast. Atlas hatching uses the same logic: pattern = ground, label = figure.

### 3.4 Local contrast hierarchy

CAD lineweight mapping: unique = 600, duplicate = 400. **No hue change.** Peripheral vision is more sensitive to weight blobs than to slight hue shift on 1-digit PIH.

### 3.5 Edge treatments

GIS/CAD **inset vertical hairlines** on duplicate cells create pairwise grouping without fill. ATC **data block borders** teach that enclosure marks *category*, not *off*.

### 3.6 Texture and micro-patterns

Fractal noise at 18–25% opacity in cell ground, `mix-blend-mode: multiply`, keeps digits crisp (z-index above). Works as **secondary channel** combined with weight demotion.

### 3.7 Peripheral vision cues

Wider letter-spacing (+0.03–0.04em) on duplicates reduces **spatial frequency** — gist pass sees "open" column. Smaller optical size (−1px) on PIH digits is surprisingly effective and fully recoverable on fixation.

### 3.8 Color-temperature shifts

Warm paper UI: duplicates shift **toward amber/paper**, not toward blue-grey. Cool shift increases salience (instrument panel effect) — wrong for "ignore me".

### 3.9 Density-based techniques

Row compression, smaller row height for dup-heavy rows — **rejected**. Implies missing data; breaks scan rhythm.

### 3.10 Cell-local techniques

**Non-negotiable.** Row fade, zebra, reference-city column, and opacity on `<td>` all read as selection or disabled state. Only `dup-cell` on matching `<td>` elements.

---

## 4. Anti-patterns (explicit)

| Technique | Why it fails |
|-----------|--------------|
| `opacity < 0.85` on value | Disabled control metaphor; dignity tint muddied |
| Cool slate grey `#64748b` | Off-palette; reads "inactive field" |
| Full-row fade | Selection / hover metaphor |
| Strikethrough, parentheses, "(same)" | Implies negation or annotation, not fact |
| Hiding duplicate text | Violates never-hidden |
| Bolding duplicates | **Increases** salience — opposite of goal |
| Greying A/S orb color | Loses motion semantics (doctrine) |

---

## 5. Practical recommendations — PIH

**Goal:** House number in duplicate Boston/NY cells recedes; Omaha column pops; dignity tints remain authoritative.

### Recommended stack (cell-local, layered)

1. **Local contrast:** `font-weight: 400` on `.v` in `dup-cell`; unique stays `600`.
2. **Figure-ground:** `::before` inset wash `rgba(51,41,31,.032)` — slightly weaker on dignity cells (`.028`).
3. **Peripheral:** `letter-spacing: .03em` on duplicate digits only.
4. **Optional ink (if weight alone too subtle):** warm saturation mix — `color-mix(in srgb, var(--ink) 72%, var(--paper))` at **opacity 1**.

### Do not use on PIH

- Opacity on `<td>` or `.v`
- Cool grey ink
- Row background
- Bolding or larger dup digits

### Dignity interaction

Dignity background = **semantic** (supportive/challenging). Duplicate demotion = **attention rank**. Layers must compose: demotion never reduces dignity tint opacity.

---

## 6. Practical recommendations — A2A

**Goal:** Duplicate aspect **contact** (same aspect word + same orb class) recedes; differing orbs (Omaha Mars separating 4°31′ vs BOS/NY 2°14′ applying) stay primary.

### Recommended stack

1. **Split within cell:** Demote `.asp` (weight 400, optional warm-shift ink); keep `.orb-num` at weight 600 with full applying/separating color.
2. **Edge:** Light inset vertical rules on `dup-cell` only (`box-shadow: inset 1px 0 0 rgba(51,41,31,.09)` both sides) — pairs BOS|NY visually.
3. **When aspect matches but orb differs:** **Not** a duplicate cell — full primary register on both (Omaha Mars row: BOS/NY dup each other; Omaha unique).

### A2A-specific rule

Duplicate detection is **value equality** on displayed facts (aspect + orb to display precision), not row label. Partial dupes (Saturn: BOS=OMA, NY differs) get per-cell `dup-cell` only where equal.

---

## 7. Recommended production direction (study only)

| Surface | Primary technique | Secondary | Avoid |
|---------|-------------------|-----------|-------|
| **PIH** | Weight 400 + cell micro-wash | Tracking + warm saturation mix | Opacity, cool grey |
| **A2A** | Split: word demote, orb primary | Inset edge on dup pair | Greying orb, row fade |

**CSS sketch (not wired):**

```css
td.rm-cmp-diff-duplicate { position: relative; }
td.rm-cmp-diff-duplicate::before {
  content: ""; position: absolute; inset: 3px 5px; border-radius: 3px;
  background: rgba(51,41,31,.032); pointer-events: none; z-index: 0;
}
td.rm-cmp-diff-duplicate .pih-house-val,
td.rm-cmp-diff-duplicate .a2a-aspect-lbl {
  font-weight: 400; letter-spacing: .03em; position: relative; z-index: 1;
  color: color-mix(in srgb, var(--ink) 72%, var(--paper));
}
/* orb / motion colors unchanged */
```

Replace current `.rm-cmp-diff-duplicate { opacity: 0.48; … }` entirely.

---

## 8. Visual study variants (HTML)

`information_hierarchy_study_1.html` demonstrates:

| ID | Name | Dimensions exercised |
|----|------|----------------------|
| **AP** | Anti-pattern (production-like) | Opacity — **rejected** |
| **R1** | Weight + tracking | Local contrast, peripheral |
| **R2** | Saturation toward paper | Saturation, ink (warm) |
| **R3** | Cell micro-wash only | Figure-ground |
| **R4** | Inset edge brackets | Edge treatments |
| **R5** | Ground grain texture | Texture, figure-ground |
| **R6** | Optical size −1px | Peripheral, local contrast |
| **R7** | PIH composite (recommended) | Weight + wash + tracking |
| **R8** | A2A split + edge (recommended) | Split cell, edge, orb primary |

All variants: Boston · New York · Omaha mixed scenario, dignities ON, dup cells only.

---

## 9. Evaluation summary

| Criterion | Best variants |
|-----------|---------------|
| Ignorable at gist | R1, R3, R7 (PIH); R8 (A2A) |
| Instantly recoverable | R7, R2 — full opacity glyphs |
| Not disabled | All except AP |
| Dignity-safe | R1, R3, R7 — no opacity on tint |
| Palette-coherent | R2, R7 — warm saturation not cool grey |
| Implementation cost | R7/R8 — pure CSS, no JS change to diff logic |

**Study conclusion:** Hierarchy should be built from **orthogonal channels** (weight, ground wash, tracking, warm saturation, edge, split orb/word) scoped **cell-locally**. Grey ink and opacity are **optional channels**, not defaults — and cool grey + opacity are **actively harmful** on this paper instrument palette.

---

## 10. Next steps (out of scope)

- Wire R7/R8 CSS into `app_shell.html` replacing `.rm-cmp-diff-duplicate` opacity rule
- Motion QA: ensure diff class toggle doesn't fight A2A orb animations
- Screenshot pass for design review
- User test: gist task ("which city differs on Mars?") vs recovery task ("what is NY Sun house?")

**No production implementation in this study.**
