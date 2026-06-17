# Visual Hierarchy Doctrine Audit

Status: provisional doctrine extraction (Phase 2.8H)
Type: hierarchy / attention-flow archaeology only
Question answered: "Where should attention go?" — NOT "What should it look like?"

No code changes. No prototypes. No colors. No fonts. No redesign.

Hierarchy must be established before typography, spacing, color, or animation
can be finalized. This document records the attention/authority hierarchy
already implied by the prototypes and names where it must become doctrine.

Builds on: Plate Doctrine (2.8C), Badge & Metadata Doctrine (2.8D),
Control & Action Doctrine (2.8E), Table & Information Density Doctrine (2.8F),
Visual Language Inventory (2.8G).

Surfaces: Map (`map_CURRENT.html`), Profile
(`prototype_profile_workspace_v11.html`), Relocated Location
(`prototype_relocated_location_v1.html`), Comparison (`comparison_v2`–`v5`),
City Intelligence (`city_profile_v1`–`v4`), plus `app_shell.html` as scaffold.

---

## 1. Page Attention Flow

Documented from actual DOM order, viewport priority, and visual weight in the
prototypes.

### Map
1. The map canvas itself (primary instrument, full surface).
2. Right-click popup / relocated chart preview at point of contact.
3. Control panel (profile select, condition builders, find).
4. Long-term working surface: popup chart work + favoriting + region finding.
- Note: the governing **profile selector is currently low in the attention
  flow** (buried in the side panel), which conflicts with profile authority.

### Profile
1. Wheel (chart object, largest and most atmospheric element).
2. Profile identity plate (name + birth context beside the wheel).
3. View pills (Natal / Current Location / Comparison) as context switch.
4. Reference tables (PiH / AiS / A2A), then lower favorites/comparisons/searches.
- Long-term working surface: tables + saved lists + notes entry points.

### Comparison
1. Comparison title + the comparison matrices (the working surface).
2. Sticky city bar (which places are being compared).
3. Profile band (governing profile context, currently visually subordinate).
4. City intelligence cards + notes areas.
- Long-term working surface: fact matrices across cities.

### Relocated Location
1. Location plate subject ("Kyoto, Japan" + "For {profile}") at page top.
2. Wheel (guest, present in the initial viewport).
3. Reference tables (PiH / AiS / A2A).
4. System metadata block, then mini intelligence + notes.
- Long-term working surface: wheel + reference tables, with notes/intel support.
- Tension: the location plate is read before the wheel; doctrine must ensure the
  wheel still reads as the central object (see Section 3).

### City Intelligence
1. City hero name + snapshot KPIs.
2. Photo/orientation strip.
3. Section accordions (cost, safety, weather, etc.).
4. Visa / intentions / detail tables.
- Long-term working surface: expandable detail sections.
- No chart wheel; this surface is place-authoritative and astrology-secondary.

---

## 2. Authority Hierarchy

The authority stack (highest to lowest) implied across chart-bearing surfaces:

1. **Profile / owner** — the governing lens.
2. **Active chart (wheel)** — the rendered consequence of the profile + place.
3. **Location / context** (Natal / Current / Relocated / Comparison set).
4. **Reference tables** (chart facts derived from the above).
5. **Metadata** (lat/lon, UTC, system settings).
6. **Provenance / system / debug information**.

Must always remain visible (chart-bearing pages):
- Profile authority (or its selector).
- The wheel.
- The current context label (which chart is being shown).

May collapse:
- Detailed metadata blocks.
- City intelligence detail.
- Comparison sections.
- Notes composers.

May move:
- Metadata placement (beside/below wheel).
- Mini intelligence and notes panels.
- Provenance/source into tooltips/footnotes.

Must never outrank the wheel:
- Plates, metadata, badges, notes, and provenance must not visually dominate the
  chart wheel on chart-bearing pages.

City Intelligence is the deliberate exception: it is place-authoritative and has
no wheel; profile does not govern it.

---

## 3. Chart Hierarchy

Implied hierarchy already present on chart surfaces (Profile, Relocated, and the
Map popup preview):

- **Wheel vs Plate:** Wheel is the largest, most atmospheric object; the plate
  orients but is lighter. On Profile the plate sits beside the wheel; on
  Relocated the location plate sits above. Doctrine: plate orients, wheel
  dominates. Plate must not displace the wheel from the central/initial view.
- **Wheel vs Tables:** Tables follow the wheel (after a divider/`.ref-row`).
  Tables are the working detail; the wheel is the focal object. Wheel ranks above
  tables visually; tables rank above wheel for sustained analysis time.
- **Wheel vs Notes:** Notes are lower on the page and lighter. Notes never
  compete with the wheel for primary attention.
- **Wheel vs Controls:** Controls (view pills, angle pills, profile selector,
  favorite) frame the wheel but should not outweigh it. The profile selector is
  the one control whose authority is conceptually above the wheel even while it
  stays visually restrained.
- **Wheel vs Metadata:** Metadata is supporting and ranks below the wheel; it may
  sit beside or below but must not dominate.

Special doctrine: **the wheel remains visually central and must not be displaced
by plates or metadata.** On the Relocated page specifically, the location plate
is read first but must not push the wheel out of the initial viewport.

Map popup is the bounded exception: it is a preview (ASC/MC + compact PiH), not
the full chart; the wheel "promise" is fulfilled on the destination page.

---

## 4. Plate Hierarchy

What each plate teaches, reading order, and memory value (per Plate Doctrine).

### Profile authority plate
- **Learn:** who the chart belongs to and the birth basis.
- **Read order:** first or alongside the wheel.
- **Remember:** profile identity (the lens).
- **Forget:** exact lat/lon and offset details (recallable, not memorized).

### Location context plate (Relocated)
- **Learn:** which place is the subject, and that it is viewed "for {profile}".
- **Read order:** first on the relocated page (page subject), then the wheel.
- **Remember:** the place + that profile remains the authority.
- **Forget:** precise coordinates and UTC after orientation.

### Comparison plates (profile band + city plates)
- **Learn:** the governing profile (band) and which places are being compared
  (city nameplates).
- **Read order:** city plates dominate; profile band is contextual.
- **Remember:** the set of places under comparison.
- **Forget:** per-column coordinate detail.

### City Intelligence hero plate
- **Learn:** which place this is and its top-level livability snapshot.
- **Read order:** first on the city page.
- **Remember:** the place and its headline KPIs.
- **Forget:** granular sub-metrics until needed.

### Map micro plate (popup)
- **Learn:** the clicked point, coordinates, and a minimal chart hint.
- **Read order:** first within the popup.
- **Remember:** little; it is transient orientation.
- **Forget:** most of it after navigating or closing.

Cross-cutting: the profile lens should be memorable on every chart-bearing
surface; place/coordinate precision is reference, not memory.

---

## 5. Table Hierarchy

Ranking from Table Doctrine evidence.

### Primary working tables
- **A2A (Aspect to Angle):** the densest analytical organism; the carousel/All
  mode is where sustained comparison happens.
- **Comparison matrices:** the entire reason the Comparison surface exists;
  cross-place analysis.

### Secondary supporting tables
- **PiH (Planet in House):** core chart reference, moderate density, consulted
  alongside the wheel.
- **Mini city intelligence (Relocated):** supports the location decision but is
  secondary to the chart.

### Reference-only tables
- **AiS (Angle in Sign):** small, quickly scanned, rarely the sustained focus.
- **Map popup preview table:** orientation/preview only.
- **App shell tables:** scaffold; not product hierarchy.

Reasoning: rank reflects **time-on-surface for analysis**, not visual size. AiS
is visually simple and quickly absorbed (reference); A2A and comparison matrices
are where the user actually works. PiH sits between: essential but consulted, not
puzzled over.

City Intelligence detail tables (cost/weather) are primary *within* the City
Intelligence surface but secondary to the chart on chart-bearing pages.

---

## 6. Notes Hierarchy

Emerging doctrine reaffirmed: **notes belong to entities/pages, not to PiH rows,
AiS rows, A2A rows, or individual table cells.**

Note systems, ranked by ownership clarity and intended prominence:

1. **Profile notebook (clearinghouse):** highest — the Profile page should
   eventually surface filtered access to all notes across owners.
2. **Favorite-location notebook:** a favorite place owns its notes; viewable/
   editable from both Profile favorites and the Relocated Location page (same
   underlying record).
3. **Comparison notebook:** notes attached to a comparison entity (not to its
   sub-tables).
4. **Saved-search notebook:** notes attached to a saved search entity.
5. **Future map research session notebook:** reserved owner; not yet built.

Hierarchy notes:
- Notes are a **supporting layer**; they never outrank the wheel or the working
  tables on chart pages.
- Current comparison prototypes attach note controls beside table sections; this
  is provisional UI, not canonical ownership — doctrine treats those notes as
  belonging to the comparison entity/page.
- The Profile-as-clearinghouse role makes Profile the top of the notes hierarchy
  even though individual notes are owned by other entities.

This documents hierarchy only; the notebook is not designed here.

---

## 7. Visual Weight Inventory

Actual distribution of visual weight (independent of color/font choices).

### Heavy
- **Wheel** (size, glow, texture, depth) — the dominant object on chart pages.
- **City hero snapshot** — dominant on City Intelligence pages.
- **Comparison matrices** — dominant on Comparison (width + density).
- **Map canvas** — dominant on Map.

### Medium
- **Profile / location plates** (identity, serif scale, beside/above wheel).
- **Reference table cards** (`.tcard` depth and outline).
- **Sticky comparison city bar** (persistent, bordered).
- **Modal surfaces** when open (backdrop + elevation).
- **Favorite control on Relocated** (page-level button competing with plate).

### Light
- **Badges / status labels** (view pills, city tags, favorited state).
- **Metadata blocks and system rows**.
- **Notes composers and links** (lower placement, restrained).
- **Secondary buttons, nav links, account control**.
- **AiS table** (small reference).
- **Provenance/source/debug** (lowest; tooltip/footnote candidates).

Observed imbalances:
- On **Map**, the highest-authority element (profile) carries the least weight.
- On **Comparison**, the profile (authority) is lighter than the comparison set
  (subject), so authority and weight diverge.
- On **Relocated**, the favorite button and location plate both carry top-level
  weight, risking competition with the wheel.

---

## 8. Open Questions

Unresolved tensions; not resolved here.

- **Wheel vs authority plate:** on Relocated the plate is read first while the
  wheel must stay central — how is that balance held?
- **Location vs profile prominence:** when place is the subject but profile is the
  authority, which carries more visual weight, and where?
- **Profile authority weight on Map:** the selector is currently least prominent
  while being highest authority — should its weight rise?
- **Comparison authority vs subject:** comparison set dominates; profile band is
  light. Is that correct, or should profile authority read more strongly?
- **Notes visibility:** how present should entity notebooks be on each page
  without competing with the wheel/tables?
- **Comparison density:** how many city columns/sections before the working
  surface overwhelms attention flow?
- **Metadata visibility:** how much metadata stays visible vs collapses, given it
  must never outrank the wheel?
- **Long-name handling:** long city/country/region/profile names in plates and
  sticky columns can distort weight and reading order.
- **Profile switching visibility:** switching profile re-renders chart-bearing
  pages — how visible must that authority action and its consequence be?
- **A2A All mode prominence:** the densest table is also the most analytical —
  should it ever be the default focus, or remain opt-in?
- **City Intelligence exception:** place-authoritative, no wheel — how does its
  hierarchy relate to chart-bearing pages without implying chart authority?

---

## 9. Highest Value Standardization Targets

Hierarchy decisions that should become doctrine first (prioritization only).

1. **Wheel centrality rule** — codify that the wheel is the central object on all
   chart-bearing pages and must not be displaced by plates or metadata.
2. **Profile authority visibility** — make profile authority legible and
   consistently ranked across Map / Profile / Relocated / Comparison (especially
   raising it on Map).
3. **Subject-vs-authority balance** — define how location/comparison subject
   weight relates to profile authority weight when they differ.
4. **Table working-rank** — establish A2A and comparison matrices as primary
   working tables, PiH/mini-intel as secondary, AiS/popup as reference.
5. **Notes as supporting layer** — lock that notes attach to entities/pages,
   never to tables/rows/cells, with Profile as clearinghouse.
6. **Always-visible vs collapsible set** — define what must stay visible (profile,
   wheel, context) vs what may collapse (detail metadata, city detail, sections,
   notes).
7. **Map popup vs destination** — confirm the popup is preview-rank and the full
   wheel/chart is destination-rank.
8. **Visual-weight rebalancing targets** — flag the Map profile selector,
   Comparison profile band, and Relocated favorite/plate competition as the first
   weight imbalances to resolve.

Hierarchy first; styling later.
