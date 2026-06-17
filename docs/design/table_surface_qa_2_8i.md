# Table Surface QA — Phase 2.8I

Status: QA + inventory pass (not a doctrine)
Type: read-only review of existing table organisms
Constraint: no new doctrine, no color values, no typography, no animation, no redesign

Goal: identify the **minimum visual mechanisms** required to make tables feel
alive, readable, and connected — before any atmosphere layer is added.

Sources inspected: `prototype_profile_workspace_v11.html`,
`prototype_relocated_location_v1.html`, `comparison_v5.html`,
`city_profile_v4.html`, `map_CURRENT.html`.

Mechanisms are described qualitatively (presence/role), not by value.

---

## Cross-Cutting Answers (all families)

**1. What currently separates rows?**
- Chart tables (PiH/AiS/A2A): **alternating-row background tint only** — no row
  lines.
- Comparison matrix: **per-row bottom border** + a near-imperceptible
  alternating tint; last row clears its border.
- Mini intelligence lists (relocated `intel-list`, comparison `ci-list`, city
  `cost-line`): **bottom border per row**, last-child cleared.
- City weather table: **bottom border per row**.
- Popup planet table: **nothing** between body rows (padding only).

**2. What currently separates sections?**
- Chart pages: a **top-border divider** (`.ref-row`) between wheel and tables;
  each table sits in its own bordered card (`.tcard`).
- Comparison: **block headers** with a bottom border, each collapsible; a strong
  sticky **city-bar boundary** (heavier bottom border) divides identity from data.
- City intelligence: **section titles** with an underline rule; accordion rows
  separate sub-sections.
- Popup: a **thin horizontal rule** plus an angles-summary grid.

**3. What currently separates tables?**
- Chart pages: each table is a **bordered, rounded card** with a serif heading +
  short accent underline (`deco`).
- Comparison: tables are **grouped under block headers**, not carded; separation
  is the header + collapse boundary.
- City/relocated: **panel/card borders** and section titles.
- Popup: the **popup shell** itself bounds the table.

**4. What hover behaviors exist?**
- **Controls only.** Pills (`apill`), angle tabs, accordion triggers, nav links,
  notes/city buttons, popup action buttons, links all have hover feedback.
- **Data rows have no hover** in any family.

**5. What active/selected states exist?**
- A2A **pills** (`.apill.on`): tinted background + accent + bold.
- Comparison **angle tabs** (`.angle-tab.active`): underline + bold.
- Relocated favorite (`.fav-btn.on`); city toggles (`.curr-btn.active`,
  weather toggle); nav active link (underline).
- **No selected/active state on any data row or cell.**

**6. What disclosure/collapse behaviors exist?**
- Comparison: **block headers collapse** their tables (`toggleBlock`); angle tabs
  swap which angle column shows.
- A2A: **carousel** swaps ASC/DSC/MC/IC/All frames (pill-driven).
- City intelligence: **accordion rows** expand/collapse detail; chevron rotates;
  left-border indent marks nested content.
- Relocated/city: "Open …" **links** lead to fuller detail.
- Chart PiH/AiS: **none** (always fully visible).

**7. What treatments could be promoted into a standard?**
- **Alternating-row tint** (chart tables) — the lightest "alive but quiet" row
  rhythm.
- **Single bottom-border row separator with last-child cleared** (comparison /
  lists / cost / weather) — the most reused readable separator.
- **Label/value column split** with tabular-aligned numeric values — present in
  every family in some form.
- **Bordered card + serif heading + short accent underline** (`tcard` + `deco`)
  — the cleanest table-as-object wrapper.
- **Block header + collapse** (comparison) — the cleanest section grouping.
- **Accordion row + chevron + left-indent** (city) — the cleanest disclosure.
- **Header underline rule** (`thead th` border / `section-title`) — consistent
  header-vs-body division.
- **Empty value placeholder** (em dash / dot) — already shared across families.

---

## Per-Family Review

### PiH (Planet in House) — `.rt.pih` in profile v11 / relocated v1
- **A. Current mechanisms:** card wrapper (`tcard`); serif heading + `deco`
  underline; **alternating-row tint**, no row lines; centered house column,
  soft-ink planet label; no header row shown; no hover; no selected state;
  always visible (no collapse).
- **B. Strengths:** quiet and readable; card makes it a clear object; alternating
  tint gives rhythm without lines; numeric alignment is clean.
- **C. Weaknesses:** no column header labels (relies on familiarity); no hover to
  aid row tracking on wide rows; row separation is the weakest of all families.
- **D. Candidate standard elements:** alternating-row tint; card+heading+`deco`
  wrapper; label/value alignment.

### AiS (Angle in Sign) — `.rt` in profile v11 / relocated v1
- **A. Current mechanisms:** same `tcard` + `.rt` system as PiH; alternating-row
  tint; right-aligned position column; no row lines; no hover; no selected state;
  always visible.
- **B. Strengths:** smallest/quickest to scan; consistent with PiH; alignment
  makes sign/position readable.
- **C. Weaknesses:** so light it can read as "empty/decorative"; no header; little
  to distinguish it from PiH at a glance beyond content.
- **D. Candidate standard elements:** shares PiH's alternating tint + wrapper;
  reinforces a single chart-reference-table standard.

### A2A (Aspect to Angle) — `.a2a*` in profile v11 / relocated v1
- **A. Current mechanisms:** `tcard` wrapper; **pills** with hover + `.on`
  selected; planet label column + value frames; **alternating-row tint** on
  `.ar:nth-child(even)`; serif value-headers (`.ar.vh`); carousel frames
  (ASC/DSC/MC/IC/All); orb sub-values; placeholder dot for empties.
- **B. Strengths:** the only chart table with real interactive state (pills);
  alternating tint + column structure handles density well; All-mode aligns
  multiple angles cleanly.
- **C. Weaknesses:** rows still don't hover, so cross-reading a wide All-mode row
  is unaided; selected state lives only in the pills, not echoed in the columns;
  header rows are intentionally transparent (can feel headerless).
- **D. Candidate standard elements:** pill hover + selected pattern; alternating
  tint shared with PiH/AiS; placeholder-dot empty treatment.

### Comparison Matrix — `.fact-table` in comparison v5
- **A. Current mechanisms:** **per-row bottom border** + faint alternating tint +
  last-row cleared; **label column with right border**; tabular numeric values;
  **block header** (bottom border) that collapses the table; **angle tabs**
  (hover + active underline); **sticky city bar** with a strong bottom boundary;
  no row hover.
- **B. Strengths:** strongest structure of all families — borders + label column
  make a true matrix; collapse keeps long pages manageable; sticky city bar keeps
  column identity; the most "connected" grid.
- **C. Weaknesses:** flat (intentional) but risks feeling inert next to the
  carded chart tables; no row hover to track across many city columns; alternating
  tint is nearly invisible, so the bottom borders do all the work.
- **D. Candidate standard elements:** **single bottom-border row separator
  (last-child cleared)** — strongest reuse candidate; label-column divider; block
  header + collapse; sticky identity boundary.

### Mini City Intelligence — relocated `.intel-list`, comparison `.ci-list`, city v4 `snap-cell`/`acc-row`/`cost-line`/`wx-table`
- **A. Current mechanisms:** list rows with **bottom border, last-child cleared**,
  flex label/value; city **snapshot** = bordered cells in a grid; **accordion
  rows** (border-bottom, chevron rotate, left-indent panel); **cost lines** with
  row borders; **weather table** with header underline (heavier) + row borders;
  "Open …" links (hover underline).
- **B. Strengths:** label/value rows are highly readable; accordion disclosure is
  clean and consistent; snapshot grid gives strong at-a-glance scanning; multiple
  surfaces already share the same bottom-border row idiom.
- **C. Weaknesses:** three different containers (list vs grid vs accordion) for
  similar data; no hover on list/cost rows; snapshot cells vs list rows aren't
  visually reconciled.
- **D. Candidate standard elements:** bottom-border row + last-child cleared;
  accordion row + chevron + left-indent; label/value flex row; snapshot
  bordered-cell grid.

### Metadata Blocks — relocated `.meta-block`, `.sys-meta`
- **A. Current mechanisms:** `meta-block` = definition list (uppercase faint
  label `dt`, value `dd`) inside a tinted bordered box, **spacing-only** between
  pairs (no row lines); `sys-meta` = bordered box, **multi-column grid** with
  serif sub-headings and label/value rows, grouped by grid + heading (no lines);
  tabular numerics; no hover; no selected state; always visible.
- **B. Strengths:** spacing + grouping reads cleanly without lines; sub-headings
  organize Birth/Relocated/System; respects the "identity vs technical" grouping
  from the Badge doctrine.
- **C. Weaknesses:** different grouping logic from the line-based tables (could
  feel disconnected); label treatment (uppercase faint) differs from table
  headers; no shared idiom with snapshot cells that show similar key/value data.
- **D. Candidate standard elements:** label/value pair with spacing-only grouping
  for low-density identity data; grid + sub-heading grouping; tabular numerics.

### Popup Preview Tables — map `.popup-planet-table`, `.popup-angles-summary`
- **A. Current mechanisms:** **header underline** (`thead th` bottom border) +
  uppercase header; **no body row separators** (padding only); angles summary as a
  small label/value grid; **thin horizontal rule** between regions; near-cusp row
  flag class; action buttons with hover; flat utilitarian shell.
- **B. Strengths:** compact and legible at preview scale; header underline clearly
  divides head from body; minimal chrome suits a transient preview.
- **C. Weaknesses:** visually disconnected from product tables (utilitarian/slate
  vs warm carded); no alternating tint or row lines, so longer previews lose row
  tracking; its own header style differs from `tcard` headings.
- **D. Candidate standard elements:** header-underline pattern; label/value
  angles grid; empty-value em dash (already shared).

---

## Minimum Mechanisms to Make Tables Alive, Readable & Connected

The smallest reusable set already present that, if standardized, would make every
table feel alive and connected **before** any atmosphere layer:

1. **One row-separation idiom per density** — alternating tint for dense scan
   tables (PiH/AiS/A2A); single bottom border with last-child cleared for
   list/matrix/detail tables. (Both already exist; pick per density, apply
   everywhere.)
2. **A shared header/heading treatment** — header underline (`thead`/section
   title) and the carded serif heading + `deco` accent, reconciled into one
   "table title" idiom.
3. **A label/value + tabular-numeric standard** — present in every family; lock
   one alignment idiom.
4. **A row hover for cross-reading** — currently absent on all data rows; a single
   restrained row-hover is the biggest missing readability mechanism, especially
   for wide A2A All-mode and multi-column comparison rows.
5. **One disclosure idiom** — accordion row + chevron + left-indent (city) and
   block-header collapse (comparison) reconciled into a single collapse pattern.
6. **One empty-value placeholder** — em dash / dot already shared; make it the
   single standard.
7. **One table-as-object wrapper rule** — when a table is carded (`tcard`) vs
   grouped under a block header — so chart tables and comparison/city tables read
   as the same family at different densities.

Observation: the **single biggest gap** is the total absence of **data-row hover
and any row/cell selected state** — every interactive state currently lives in
controls (pills/tabs/accordions), never in the table body. That is the first
readability mechanism to add, ahead of any atmosphere.
