# Table & Information Density Doctrine Audit

Status: provisional audit (Phase 2.8F)
Type: archaeology / doctrine extraction only
Scope: tables, grids, matrices, dense panels, visibility, ownership, hierarchy

No implementation. No prototype changes. No CSS changes. No commits.

Out of scope for this phase: final colors, typography, spacing, glow/shadow
systems, animation/hover timing.

Product principle: **Tables are working surfaces, not decoration.** Do not
remove useful information merely to make a page feel cleaner. Density is allowed
when it supports analysis; hierarchy must make dense information readable.

Files audited:
`prototype_profile_workspace_v11.html`, `prototype_relocated_location_v1.html`,
`map_CURRENT.html`, `comparison_v2.html`, `comparison_v3.html`,
`comparison_v4.html`, `comparison_v5.html`, `city_profile_v1.html`,
`city_profile_v2.html`, `city_profile_v3.html`, `city_profile_v4.html`,
`app_shell.html`.

---

## 1. Table Inventory

| Organism | File(s) | Selector / function | Purpose | Data type | Visible density | Ownership family |
|---|---|---|---|---|---|---|
| Planet in House chart card | profile v11, relocated v1 | `pihTable()`, `pihCard()`, `.rt.pih`, `.tcard` | Show planet→house placements | Chart reference | 11 planet rows; moderate | Chart / Profile / Relocated |
| Angle in Sign chart card | profile v11, relocated v1 | `aisTable()`, `aisCard()`, `.rt` | Show ASC/DSC/MC/IC sign positions | Chart reference | 4 rows; sparse | Chart / Profile / Relocated |
| Aspect to Angle carousel/table | profile v11, relocated v1 | `a2aCard()`, `a2aBody()`, `.a2a-track`, `.vcol`, `.ar` | Show aspect contacts by angle and planet | Chart reference | 13 rows × up to 4 angle columns; dense in All mode | Chart / Profile / Relocated |
| Combined compact PiH + AiS card | profile v11, relocated v1 | `pihCard(data, cls, true)` | Compact sxs chart reference | Chart reference | moderate | Chart / Profile |
| Chart modal wheel context | profile v11, relocated v1 | `.modal-head` + enlarged wheel | Dense visual chart context | Chart visual | not table, but dense | Chart |
| Map popup angle summary | `map_CURRENT.html` | `.popup-angles-summary` | Compact ASC/MC summary | Chart preview | 2 label/value rows; sparse | Map Popup |
| Map popup planet-house preview | `map_CURRENT.html` | `.popup-planet-table`, `buildPlanetHouseRowsFromData()` | Preview planet→house placements from map click | Chart preview | 11 planet rows; dense for popup | Map Popup |
| Map popup debug table | `map_CURRENT.html` | `.popup-aura-debug table` | Internal aura/debug diagnostics | System/debug | dense internal | System / non-canon |
| Comparison matrix v2 | `comparison_v2.html` | `.fact-matrix`, `.fact-matrix-wrap` | Compare facts across cities | Comparison chart facts | 3 city columns + label column; moderate/dense | Comparison |
| Comparison matrix v3–v5 | `comparison_v3.html`–`comparison_v5.html` | `buildTable()`, `.fact-table`, `.label-col`, `.val-col` | Render AiS/PiH/A2A facts across visible cities | Comparison chart facts | dynamic width; 3+ columns; moderate/dense | Comparison |
| Comparison city intelligence cards | comparison v2–v5 | `.ci-cards` / `.ci-grid`, `.ci-card`, `.ci-list` | Compact city intelligence per comparison city | City intelligence reference | 3 cards; several bullets each; moderate | Comparison / City Intelligence |
| Comparison city info modal list | comparison v3–v5 | `.ci-modal-list` | Expanded city facts | City intelligence reference | moderate | City Intelligence |
| Relocated location metadata block | relocated v1 | `.meta-block` | Country/region/lat/lon/UTC for location | Metadata | 5 fields; moderate | Relocated Location / Location |
| Relocated Birth/Relocated/System block | relocated v1 | `.sys-meta` | Persistent birth + relocated + system context | Metadata | 3 groups × 3 rows; moderate | System / Profile / Location |
| Relocated mini intelligence list | relocated v1 | `.intel-list` | Compact city facts plus remote-only fields | City intelligence | 5 base rows; 9 rows if remote; moderate | Relocated Location / City Intelligence |
| City intelligence snapshot grid | city_profile v1–v4 | `.snapshot`, `.snap-row`, `.snap-cell` | At-a-glance city KPIs | City intelligence | 7 cells; moderate | City Intelligence |
| City profile accordion rows | city_profile v1–v4 | `.acc-row`, `.acc-trigger`, `.acc-panel` | Reveal detailed city facts by category | City intelligence | many rows; dense when expanded | City Intelligence |
| City cost detail list | city_profile v1–v4 | `.cost-grid`/`.cost-item` (v1), `.cost-major`, `.cost-line` (v2–v4) | Detailed cost categories and values | Cost data | dense in expanded Cost row | City Intelligence |
| Weather grid/table | city_profile v1–v4 | `.weather-grid` (v1), `.wx-table` (v2–v4) | Monthly high/low/rain/humidity | Weather data | 12 months × 5 values; dense | City Intelligence |
| Language detail group | city_profile v2–v4 | `.lang-section`, `.lang-group`, `.lang-line` | Official/practical languages | City intelligence | sparse/moderate | City Intelligence |
| Remote place fact rows | city_profile v1 | `.remote-row` | Remote location nearest settlement/airport/hospital | City intelligence / remote metadata | 4 rows; moderate | Location / City Intelligence |
| App shell simple tables | `app_shell.html` | `table.simple` | Placeholder relocated chart and comparison facts | Scaffold utility | sparse/moderate | System / Scaffold |
| App shell grid/list panels | `app_shell.html` | `.grid-2`, `ul.plain`, `.panel` | Placeholder dashboard/favorites/explorations | Scaffold utility | moderate | System / Scaffold |

---

## 2. Information Density Findings

### Sparse
- **Angle in Sign chart card**: 4 rows. Efficient and not overloaded.
- **Map popup angle summary**: ASC/MC only. Correctly compact for popup context.
- **Language details**: small grouped text blocks.
- **App shell simple relocated chart table**: intentionally scaffold-level.

### Moderate
- **Planet in House chart card**: 11 rows but only two values per row; useful analysis density.
- **Relocated metadata blocks**: 5-field location block and 3×3 system block; informative but not overloaded.
- **Relocated mini intelligence list**: base 5 rows; reasonable.
- **City snapshot grid**: 7 KPIs; useful orientation density.
- **Comparison city intelligence cards**: short bullet lists per city; moderate.

### Dense
- **Aspect to Angle All mode**: 13 rows across ASC/DSC/MC/IC. Density helps analysis by making angle comparison visible in one organism.
- **Comparison matrices**: label column + multiple city columns. Density is the point; supports cross-place analysis.
- **City cost detail**: multiple categories and sub-lines. Dense but useful when expanded.
- **Weather table**: 12-month table with multiple metrics. Dense but appropriate for detail view.
- **City profile accordions**: many categories across page. Dense, but hidden-by-default detail prevents immediate overload.

### Overloaded
- **Map popup planet-house preview** can be overloaded for its surface: 11 planet rows plus actions inside a narrow popup. It is still useful because it gives a meaningful chart preview, but it risks becoming too much if more facts are added.
- **Comparison v2** is more overloaded than v5: city bar, matrix, notes, popup facts, and city intelligence coexist with less refined separation.
- **City profile expanded rows** can become overloaded if many accordions are open, especially Stability/Freedom and Cost.

### Under-informative
- **Comparison wheel note / wheel-reserved placeholders**: explicitly reserve future chart comparison but provide no chart visual; useful as placeholder only.
- **App shell tables**: intentionally under-informative scaffold; not product doctrine.
- **Relocated mini intelligence** is intentionally compact; not under-informative for prototype, but insufficient as a full city profile.

Where density helps analysis:
- A2A All mode.
- Comparison matrices.
- Weather and cost details.
- PiH/AiS reference tables beside chart wheel.

Where density creates clutter:
- Narrow popup preview if expanded further.
- Multiple open city accordions.
- Comparison v2 matrix + city info popup + notes all in one pass.

Where information has been over-reduced:
- Comparison placeholder wheel area.
- App shell scaffold tables.
- Map popup if it promises “Open chart” but only shows non-wheel preview.

---

## 3. Visibility Rules

This section records likely default visibility vs collapsible/hidden candidates.
It does not implement behavior.

### PiH (Planet in House)
- **Visible by default:** yes on Profile and Relocated chart pages.
- **May collapse later:** no, not on chart-bearing pages; it is core chart reference.
- **Comparison:** visible in matrix section; can be section-collapsible because comparison contains many tables.

### AiS (Angle in Sign)
- **Visible by default:** yes on Profile and Relocated chart pages.
- **May collapse later:** no on chart-bearing pages; it is small and core.
- **Comparison:** section-collapsible acceptable.

### A2A (Aspect to Angle)
- **Visible by default:** yes on Profile and Relocated chart pages, at least one angle view.
- **May collapse later:** avoid collapsing the whole organism on chart pages; All mode can remain a selectable denser view.
- **Comparison:** section-collapsible acceptable due to matrix width/density.

### Comparison city facts
- **Visible by default:** core comparison matrices and city nameplate facts.
- **May collapse later:** city intelligence cards/details, notes, and expanded modal lists.
- **Should not hide:** city identity, coords, visible/hidden state, selected comparison places.

### City-intelligence essentials
- **Visible by default:** snapshot KPIs; overview summary.
- **May collapse later:** detail categories (cost breakdown, weather months, safety narrative, infrastructure specifics).
- **Should not remove:** population/cost/climate/weather/infrastructure cues; density is product value.

### Popup previews
- **Visible by default:** title, lat/lon, ASC/MC, compact PiH preview, actions.
- **May collapse later:** debug/provenance/policy notes if they grow.
- **Should not add by default:** full A2A, city intelligence detail, notes composer. Popup is preview, not destination.

### Metadata grids
- **Visible by default:** relocated page location metadata and Birth/Relocated/System block.
- **May collapse later:** source/provenance details, advanced system details.
- **Should not group:** Tier 1 birth identity (Profile Name, Birth Date, Birth Time, Birth Place) with lower-priority technical metadata.

---

## 4. Visual Hierarchy Inventory

Inventory only. No final style choices.

### Row shading / alternating rows
- Profile/Relocated chart tables: alternating body rows in `.rt` and A2A `.ar` rows.
- Comparison matrices: alternating rows in `.fact-matrix` / `.fact-table`.
- City profile cost/weather detail: mostly row separators rather than alternating rows.
- Map popup table: no alternating row shading; compact row structure only.

### Column shading / column separators
- Comparison matrices: label column separated from value columns; dynamic `colgroup` widths.
- Map popup table: hidden spacer column used to balance layout.
- Chart reference cards: no column shading; alignment and label/value hierarchy do the work.

### Row separators
- Comparison matrices: row borders.
- City profile accordions: row borders between accordion triggers.
- City cost/weather: line separators between rows.
- Relocated intel list: row separators between label/value facts.
- Map popup: header separator in popup table; minimal row separation.

### Table outlines / card borders
- Profile/Relocated chart references live inside `.tcard` cards.
- Comparison matrices are table-first, not card-first, inside section blocks.
- City snapshot uses individual cells; weather uses a true table; cost uses list rows.
- App shell uses simple full-border tables for scaffold only.

### Inner glow / outer glow
- Chart reference cards use card depth and top treatment; no table-internal glow doctrine should be inferred.
- Wheels have glow/depth but are not table organisms.
- Map and comparison tables are largely flat/functional.

### Alternating rows
- Present in chart reference and comparison matrix families.
- Not present in city cost detail or map popup preview.

### Section / subsection headers
- Chart reference: card headings (`Planet in House`, `Angle in Sign`, `Aspect to Angle`).
- Comparison: block headers with section titles.
- City profile: section titles plus accordion row labels; cost has category headers.
- Relocated metadata: group headings (`Birth`, `Relocated`, `System`).

### Label/value hierarchy
- Chart reference: planet/angle labels vs positions/houses/orbs.
- Comparison: fixed label column vs city value columns.
- Relocated metadata/intel: label left/value right or grouped rows.
- City profile: snapshot labels/values; accordion label/short value.
- Map popup: ASC/MC labels and values; planet/house columns.

### Empty-value formatting
- Chart A2A uses `·` placeholder via `.ph`.
- Comparison uses `&mdash;` for missing values.
- Map popup uses `—` for missing ASC/MC values.
- App shell uses `—` placeholders.

### Hover states
- Present for controls around tables (pills, tabs, disclosures, city controls), not central to table doctrine.
- No table row hover doctrine is established.

---

## 5. Table Ownership

| Table family / organism | Owner |
|---|---|
| PiH / AiS / A2A chart reference cards | Profile on Profile page; Relocated Location on relocated page, under Profile authority |
| A2A carousel/table | Same as chart reference; belongs to the chart/page, not a note owner |
| Comparison matrices | Comparison |
| Comparison city intelligence cards/modals | Comparison surface displaying City Intelligence-owned facts |
| Map popup planet/angle preview | Map Popup under active Profile if chart data is shown |
| Relocated metadata grid | Relocated Location / Location, under Profile authority |
| Relocated Birth/Relocated/System block | Profile + Location + System |
| Relocated mini intelligence list | Relocated Location displaying City Intelligence-owned facts |
| City snapshot grid / accordions / cost/weather tables | City Intelligence |
| App shell simple tables/grids | System/Settings scaffold only |
| Debug/aura tables | System/internal, non-canon |

Notes doctrine confirmed:
- Notes attach to **entities/pages**, not individual tables.
- Allowed note owners remain: profile, favorite location, comparison, saved search, future map research session.
- Do **not** create or recommend PiH Notes, AiS Notes, A2A Notes, row-level notes, or individual-card notes.
- Current comparison prototypes contain table-section note controls; doctrine should treat these as provisional and not canonical table ownership.

---

## 6. Proposed Table Families

### 6.1 Chart Reference Table
- **Likely canonical source:** `prototype_profile_workspace_v11.html`.
- **Variants:** Profile full, Relocated guest/junior, compact sxs.
- **Includes:** PiH, AiS, A2A card organisms.
- **Should not mutate:** core chart facts; PiH/AiS/A2A must remain visible on chart-bearing pages; empty-value convention must remain explicit.

### 6.2 Aspect Carousel / Aspect Table
- **Likely canonical source:** `prototype_profile_workspace_v11.html` / `prototype_relocated_location_v1.html`.
- **Variants:** single-angle frame, All frame, comparison matrix angle tabs.
- **Should not mutate:** planet rows, angle labels, orb visibility, empty placeholders.

### 6.3 Comparison Matrix
- **Likely canonical source:** `comparison_v5.html`.
- **Variants:** AiS matrix, PiH matrix, A2A matrix; dynamic column width; hidden/restored columns.
- **Should not mutate:** fixed label column, place columns, visible city identity, missing value marker.

### 6.4 City Intelligence Fact Grid
- **Likely canonical source:** `city_profile_v4.html` for full city profile; `comparison_v5.html` for compact comparison cards.
- **Variants:** hero snapshot grid, comparison city cards, relocated mini intelligence list.
- **Should not mutate:** essential city facts should not be removed for cleanliness; compact variants may select fewer facts but must remain useful.

### 6.5 Cost / Weather Detail Table
- **Likely canonical source:** `city_profile_v4.html`.
- **Variants:** cost category rows, monthly weather table, currency/weather unit toggles.
- **Should not mutate:** category labels, numeric values, month rows, unit clarity.

### 6.6 Popup Preview Table
- **Likely canonical source:** `map_CURRENT.html`.
- **Variants:** chart-success popup, fallback popup, debug popup.
- **Should not mutate:** popup remains preview-only; include enough chart facts to justify `Open chart`, but not full chart or city intelligence.

### 6.7 Metadata Grid
- **Likely canonical source:** `prototype_relocated_location_v1.html`.
- **Variants:** location metadata block, Birth/Relocated/System block, remote-only rows.
- **Should not mutate:** identity/chart data must not be demoted into low-priority technical metadata; source/provenance may be lower visibility.

### 6.8 Utility / Scaffold Table
- **Likely canonical source:** `app_shell.html` only as scaffold.
- **Variants:** simple chart table, comparison placeholder table, settings forms.
- **Should not mutate:** do not promote scaffold visual style into product canon.

---

## 7. Open Questions

- **Dense vs beautiful:** where is the point at which useful density becomes intimidating? Do not resolve by deleting analysis data.
- **Table vs card:** chart references are card-wrapped tables; comparison is matrix-first; city intel uses cards/accordions/lists. Which data types deserve true tables?
- **Grid vs list:** mini city intelligence currently uses a list; full city intelligence uses snapshot grid + accordions. Should relocated mini intel remain list, grid, or compact cards?
- **Always visible vs collapsible:** chart PiH/AiS/A2A likely remain visible; comparison sections and city details may collapse. Exact defaults unresolved.
- **Row shading intensity:** row alternation exists in chart/comparison families but not popup/city details. Standardization later must tune intensity without removing density.
- **Table glow / border treatment:** chart cards and wheel have depth, comparison/city/map are flatter. Do not decide yet.
- **Compact mobile versions:** comparison matrices and A2A All mode are width-sensitive; mobile behavior unresolved.
- **Comparison table width:** v5 computes dynamic width; how many city columns before horizontal scroll becomes a product problem?
- **Popup preview scope:** how much chart data belongs in the popup before it becomes a destination? Current popup includes ASC/MC + PiH only.
- **A2A All default:** should All be a user-selectable dense mode only, or ever default?
- **Empty-value marker:** `·`, `—`, and `&mdash;` all appear. Canonical marker unresolved.
- **City detail overflow:** if many accordions are opened, does the page remain usable? Defaults and persistence unresolved.
- **Notes adjacency:** comparison prototypes place notes beside table sections, but notes should not belong to tables. Where should comparison notes live?
- **Source/provenance visibility:** source rows and debug/provenance notes exist, but likely not primary table content.

---

## 8. Highest-Value Standardization Targets

1. Define **Chart Reference Table** doctrine from profile v11 + relocated v1: PiH/AiS/A2A are working reference surfaces and should remain visible on chart-bearing pages.
2. Define **Comparison Matrix** doctrine from comparison v5: label column, city columns, dynamic width, missing values, and section collapsibility.
3. Define **Popup Preview Table** limits: ASC/MC + compact PiH preview is appropriate; full chart belongs on the destination page.
4. Separate **City Intelligence essentials** (snapshot/mini facts) from **detail tables** (cost/weather/accordion expansions), without under-informing the user.
5. Canonicalize **empty-value formatting** across chart, comparison, map, and scaffold tables.
6. Clarify **notes ownership around tables**: notes may sit near analysis, but must attach to entities/pages, not PiH/AiS/A2A or rows.
7. Decide which dense organisms are **always visible** vs **collapsible**, with chart reference tables protected from over-collapse.
8. Treat `app_shell.html` tables as scaffold only; do not inherit its utility table style into product doctrine.
