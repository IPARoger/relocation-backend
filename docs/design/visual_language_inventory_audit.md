# Visual Language Inventory Audit

Status: provisional audit (Phase 2.8G)
Type: archaeology / classification only
Scope: visual mechanisms that create hierarchy, atmosphere, grouping, emphasis,
warmth, depth, readability, and orientation.

No code changes. No prototype changes. No final color selection. No redesign.

Out of scope for this phase: final colors, final typography, final spacing,
final animation timing, final hover behavior, final shadow/glow values.

Product goal framing: visual language is functional infrastructure, not
decoration. The target is quiet vitality: warmth, depth, and atmosphere without
interfering with decision-making.

Files audited:
`prototype_profile_workspace_v11.html`, `prototype_relocated_location_v1.html`,
`map_CURRENT.html`, `comparison_v2.html`, `comparison_v3.html`,
`comparison_v4.html`, `comparison_v5.html`, `city_profile_v1.html`,
`city_profile_v2.html`, `city_profile_v3.html`, `city_profile_v4.html`,
`app_shell.html`.

---

## 1. Visual Inventory

Catalog of mechanisms currently used. This is descriptive only.

| Mechanism | File(s) / selector(s) | Purpose | Surface |
|---|---|---|---|
| Page atmospheric gradients | profile v11 `body`, relocated v1 `body` | Provide warmth/atmosphere behind content | Profile / Relocated |
| Body noise texture | comparison v2 `body` embedded SVG noise | Subtle surface life | Comparison v2 |
| Wheel outer glow | profile v11 `.disc.home`, `.disc.guest`; relocated v1 `.disc.guest` | Elevate wheel and separate chart object from page | Chart surfaces |
| Wheel inner/inset boundary | profile/relocated `.disc` inset shadow | Contain wheel edge | Chart surfaces |
| Wheel SVG radial glow | `buildWheel()` radialGradient `glow` | Atmosphere and focal center | Chart wheel |
| Wheel SVG paper noise | `buildWheel()` `feTurbulence` + low-opacity rect | Make wheel surface feel alive | Chart wheel |
| Wheel ring hierarchy | `buildWheel()` outer ring, zodiac band, house wedges, core rings, ticks | Readability/orientation inside wheel | Chart wheel |
| Wheel alternating wedges | `buildWheel()` zodiac/house alternating wedge fills | Segment grouping without heavy color | Chart wheel |
| Card outlines | profile/relocated `.tcard`, `.panel`; comparison/city `.ci-card`, `.snap-cell`, `.modal-box` | Group related dense information | Cards / tables / city intel |
| Card depth shadows | profile v11 `.tcard`, `.panel`, `.suggest`, `.modal`; relocated `.tcard`, `.panel`, `.modal`; comparison modal boxes | Lift interactive or dense panels | Profile / Relocated / Comparison |
| Functional flat borders | comparison v2–v5 `.fact-table`, `.profile-block`, `.city-bar-wrap`; city profile sections | Structure without strong atmosphere | Comparison / City intel |
| Row separators | comparison `.fact-table td`, city `.acc-row`, `.cost-line`, `.wx-table td`, relocated `.intel-list li`, map popup table header | Readability in dense data | Tables / lists |
| Section separators | profile `.ref-row`, `.lower`; comparison `.block-header`, `.ci-section-title`, `.wheel-note`; city `.section-title`, `.visa-block`, `.intentions` | Separate major regions | All dense surfaces |
| Alternating rows | profile/relocated `.rt tbody tr:nth-child(even)`, A2A `.ar:nth-child(even)`, comparison `.fact-table tr:nth-child(even)` / v2 odd rows | Dense table legibility | Chart / Comparison |
| Label/value hierarchy | profile `.rt td.pl/.hs`, comparison `.label-col/.val-col`, map `.pa-lbl/.pa-val`, relocated `.intel-list li span/b`, city `.snap-label/.snap-value` | Make dense fields scannable | Tables / metadata / city intel |
| Empty-value formatting | chart `.ph` dot; comparison `&mdash;`; map popup `—`; app shell `—` | Preserve grid structure with missing data | Chart / Comparison / Popup |
| Hover states | nav links, pills/tabs, city controls, notes controls, accordion triggers, profile account, map buttons | Affordance for interactable elements | All interactive surfaces |
| Selected/active states | profile `.chip.on`, `.apill.on`; comparison `.angle-tab.active`, nav active; city `.curr-btn.active`, `.wt-btn.active`; relocated `.fav-btn.on` | Current selection/status clarity | Controls |
| Disabled states | map `button#findBtn:disabled`; comparison `.cc:disabled`, `.modal-btn-save`; relocated disabled `.intel-open`; app shell disabled buttons | Signal unavailable actions | Controls |
| Modal backdrops | profile/relocated `.modal-back`; comparison/city `.modal-overlay`; app shell `.modal-backdrop` | Focus/contain dialog task | Modals |
| Popup shell | map `.leaflet-popup-content-wrapper`, `.popup-chart` | Compact preview grouping | Map Popup |
| Dashed borders | comparison `.add-city-btn`, `.stub-restore`, app shell `.stub`/`.future-only`; map/debug placeholders | Indicate placeholder/future/scaffold/restore affordance | Comparison / Shell / Debug |
| Warning boxes | app shell `.warn-box`, map popup policy note | Communicate constraint/risk | Scaffold / Map |
| Notice boxes | app shell `.notice-box` | Confirm state/context | Scaffold |
| Photo placeholders | city profiles `.photo-block` | Atmospheric city-intel grouping | City Intelligence |
| Accordion indentation | city profiles `.acc-panel-inner` left border/padding | Nest detail under row | City Intelligence |
| Genie drawer placeholder | app shell `.drawer-placeholder`, `.genie-drawer-mount .genie-panel` | Scaffold grouping for future assistant panel | App Shell / Genie scaffold |

---

## 2. Wheel Atmosphere Systems

Inventory of wheel treatments only.

### Natal wheel
- **File:** `prototype_profile_workspace_v11.html`.
- **Selector / functions:** `.disc.home`, `buildWheel()`, `discHtml()`, `renderChart()`.
- **Glow system:** outer wheel glow on `.disc.home`; internal radial glow inside SVG.
- **Shadow system:** outer elevation plus inset boundary.
- **Texture system:** SVG `feTurbulence` paper texture applied at low opacity.
- **Ring hierarchy:** outer boundary, zodiac band, sign dividers, house wedges, aspect ring, core ring, angle lines, ticks.
- **Hover behavior:** wheel container has `cursor: zoom-in`; popout affordance visually signals enlarge.
- **Purpose:** home/native chart focal object with warmth and authority.

### Current location / guest wheel
- **File:** `prototype_profile_workspace_v11.html`.
- **Selector / functions:** `.disc.guest`, same `buildWheel()`.
- **Glow system:** guest allele uses different atmospheric color role from home; same structural mechanics.
- **Shadow system:** same elevation/inset model as natal.
- **Texture system:** same SVG paper texture.
- **Ring hierarchy:** identical to natal.
- **Hover behavior:** same enlarge affordance.
- **Purpose:** visually related but contextually secondary chart.

### Relocated Location guest wheel
- **File:** `prototype_relocated_location_v1.html`.
- **Selector / functions:** `.disc.guest`, relocated copy of `buildWheel()`.
- **Glow system:** slightly cooler/lighter guest glow and smaller wheel size than Profile full wheel.
- **Shadow system:** lighter outer depth and inset edge.
- **Texture system:** same SVG paper texture.
- **Ring hierarchy:** identical chart grammar.
- **Hover behavior:** same `cursor: zoom-in` and popout affordance.
- **Purpose:** same organism, junior/contextual location page.

### Modal enlarged wheel
- **Files:** profile v11, relocated v1.
- **Selector / functions:** modal content includes `.disc` with larger inline width; `buildWheel()` called at larger SVG size.
- **Glow/shadow system:** inherits `.disc.home`/`.disc.guest` class treatment when present; relocated modal uses guest.
- **Texture/ring hierarchy:** identical to source wheel, enlarged.
- **Hover behavior:** modal wheel cursor is set non-zooming; modal itself is terminal enlarged view.
- **Purpose:** focus/enlargement, not a new chart organism.

### Non-wheel placeholders
- **Files:** comparison v2–v5.
- **Selectors:** `.wheel-reserved`, `.wheel-note`.
- **Treatment:** border/section note only; no wheel atmosphere.
- **Purpose:** reserve future wheel space; under-informative by design.

### Map
- **File:** `map_CURRENT.html`.
- **Treatment:** no wheel; popup preview table only.
- **Important distinction:** map contains aura/raster field language, but not the chart wheel organism.

---

## 3. Table Atmosphere Systems

Inventory of grouping mechanisms in dense data surfaces.

### PiH / AiS chart reference tables
- **Files:** profile v11, relocated v1.
- **Selectors:** `.tcard`, `.rt`, `.rt.pih`, `.tcard h3`, `.deco`.
- **Row shading:** alternating rows.
- **Border strategy:** card boundary, not full grid borders.
- **Separator strategy:** card heading + top divider between wheel and reference row.
- **Hover strategy:** none on table rows; table is reference, not interactive.
- **Grouping strategy:** card shell, heading, small heading deco, label/value alignment.
- **Low-color grouping:** layout, alignment, alternating row fields, and card boundaries do most work.

### A2A aspect carousel/table
- **Files:** profile v11, relocated v1.
- **Selectors:** `.a2a-top`, `.apills`, `.a2a-rows`, `.a2a-planetcol`, `.a2a-track`, `.frame`, `.vcol`, `.ar`.
- **Row shading:** alternating row backgrounds in planet/value rows.
- **Border strategy:** contained by `.tcard`.
- **Separator strategy:** controls above, row rhythm below.
- **Hover strategy:** pills hover/selected state; rows do not hover.
- **Grouping strategy:** planet label column + angle value frames + pills.
- **Low-color grouping:** structural columns and carousel frames.

### Comparison tables
- **Files:** comparison v2–v5.
- **Selectors:** `.fact-matrix`, `.fact-table`, `.label-col`, `.val-col`, `.fact-table-wrap`.
- **Row shading:** alternating rows (v2 odd, later even).
- **Border strategy:** bottom row separators, label-column separator, no card shell.
- **Separator strategy:** block header for section; label column holds row identity.
- **Hover strategy:** none on table rows.
- **Grouping strategy:** fixed label column + dynamic city columns.
- **Low-color grouping:** column structure and row separators.

### City intelligence tables / grids
- **Files:** city_profile v1–v4, comparison v2–v5, relocated v1.
- **Selectors:** `.snapshot`, `.snap-cell`, `.acc-row`, `.cost-line`, `.wx-table`, `.ci-card`, `.ci-list`, `.intel-list`.
- **Row shading:** mostly absent; uses row separators instead.
- **Border strategy:** snapshot cells, accordion row separators, table borders in weather.
- **Separator strategy:** section titles, accordion boundaries, cost category headings.
- **Hover strategy:** accordion triggers and action controls, not data rows.
- **Grouping strategy:** snapshot grid for top-level facts; accordions for details; cost/weather use category/table structure.
- **Low-color grouping:** borders, labels, indentation, category headings.

### Popup preview tables
- **File:** `map_CURRENT.html`.
- **Selectors:** `.popup-angles-summary`, `.popup-planet-table`, `.popup-hr-tight`, `.popup-aura-debug table`.
- **Row shading:** absent.
- **Border strategy:** compact header separator and popup shell.
- **Separator strategy:** horizontal rule, angle summary grid, table header line.
- **Hover strategy:** popup actions only.
- **Grouping strategy:** title/coords, compact angle summary, planet-house table, action row.
- **Low-color grouping:** micro layout and lines.

---

## 4. Separator Language

Classification of existing separator mechanisms by strength.

### Strong
- Profile/relocated modal backdrops: strong focus separator between page and dialog.
- City profile major section tops (`.visa-block`, `.intentions`) and section-title lines.
- Comparison city bar bottom rule / sticky column boundary.
- Profile lower-section divider separating chart from saved lists.

### Medium
- Profile/relocated `.ref-row` top border separating wheel from reference tables.
- Chart reference card outlines (`.tcard`).
- Comparison `.block-header` bottom border.
- City snapshot cell outlines.
- Relocated `.sys-meta` block outline.
- Map popup table header line and `hr.popup-hr-tight`.

### Subtle
- Alternating table rows in `.rt`, `.a2a`, `.fact-table`.
- Relocated `.meta-block` background/outline.
- Relocated `.intel-list li` row separators.
- City `.cost-line` and `.ci-list li` separators.
- Notes composer toolbar border.

### Nearly invisible
- Spacing-only separation inside plates and text groups.
- Low-opacity wheel paper texture.
- Fine zodiac/house wedge fills in wheel.
- App shell context/debug boundaries when visually treated as scaffold.

Separator types observed:
- Horizontal lines and rules.
- Card boundaries.
- Alternating row shading.
- Grid/cell outlines.
- Indentation/left borders for nested city detail.
- Backdrop separation for modals.
- Placeholder/future dashed borders.

---

## 5. Texture Systems

### Paper / page textures
- **Profile v11:** page atmosphere from layered radial gradients and warm paper base.
- **Relocated v1:** similar layered gradients, cooler/lighter guest emphasis.
- **Comparison v2:** SVG noise background creates subtle surface life.
- **Comparison v3–v5 / city v1–v4:** rely more on flat theme surfaces and borders.
- **App shell:** utilitarian flat scaffold, little/no atmosphere.
- **Map:** functional Leaflet/runtime UI; not a paper-surface system.

### Wheel textures
- **Profile/relocated wheels:** SVG `feTurbulence` paper texture inside wheel; low-opacity overlay.
- **Wheel gradients:** radial glow centered in wheel; alternating zodiac/house wedges.
- **Purpose:** chart object feels alive and materially separate from UI chrome.

### Card textures / gradients
- **Chart reference cards:** subtle top gradients in `.tcard.home` / `.tcard.guest`.
- **Relocated panels:** light border/depth but less pronounced than Profile.
- **Comparison/city cards:** mostly flat card surfaces; rely on outline and separators rather than texture.

Surfaces that feel alive because of texture:
- Profile page.
- Relocated Location page.
- Wheel surfaces.
- Comparison v2 background.

Surfaces that rely mostly on color/border/structure:
- Comparison v3–v5.
- City profiles v1–v4.
- Map popup/control panel.
- App shell.

---

## 6. Aura / Glow Systems

Inventory of glow/depth treatments and their current purpose.

| Surface | Selector / source | Glow/depth purpose |
|---|---|---|
| Natal wheel | profile v11 `.disc.home`, SVG radial glow | hierarchy, warmth, atmosphere, focal object |
| Guest/current wheel | profile v11 `.disc.guest` | distinguish guest context while preserving same organism |
| Relocated wheel | relocated v1 `.disc.guest`, SVG radial glow | cooler/lighter atmosphere, junior profile context |
| Modal wheel | profile/relocated modal `.disc` | focus and enlargement, not new doctrine |
| Chart reference cards | `.tcard`, `.tcard.home/.guest` gradients + shadows | grouping and soft elevation |
| Profile/relocated panels | `.panel`, `.modal`, `.suggest` | contain saved lists, notes, modal tasks |
| Comparison modals | `.modal-box` | dialog focus, not atmosphere |
| Map popups | Leaflet popup + `.popup-chart` shell | compact grouping, not glow-heavy |
| App shell modals/panels | `.modal`, `.panel`, `.stub`, `.future-only` | scaffold grouping and warning/status separation |
| Genie drawer scaffold | app shell `.drawer-placeholder`, `.genie-drawer-mount .genie-panel` | future panel grouping; scaffold only |
| Aura/raster map field | map comments/legend (`aura` pixel field) | data visualization atmosphere on map, explicitly not chart-wheel glow |

Current purpose of glow:
- **Hierarchy:** wheel is the primary visual object.
- **Warmth/atmosphere:** Profile/home chart and paper context.
- **Grouping:** chart cards and modals use softer depth.
- **Focus:** modal depth/backdrops isolate tasks.
- **Context:** home vs guest wheel/card variants.

No final glow doctrine is selected here.

---

## 7. Grouping Mechanisms

### Profile Workspace
- Groups by: topbar/nav, view pills, plate + wheel, `.ref-row` divider, `.tcard` cards, lower `.panel` cards, modal backdrop.
- Mechanisms: atmospheric background, wheel glow, card outlines/depth, row alternation, saved-list separators.

### Relocated Location
- Groups by: topbar, location plate, wheel/side plate, chart reference cards, `sys-meta`, lower intel/notes panels.
- Mechanisms: page gradients, guest wheel glow, card borders, metadata grid outlines, row separators.

### Map
- Groups by: side panel sections, Leaflet popup shell, angle summary, popup planet table, action row, debug overlays.
- Mechanisms: functional borders, compact lines, micro grid, warning/policy notes, popup containment.

### Comparison v2
- Groups by: nav/profile strip, sticky city bar, city columns, fact matrices, city info popups, CI cards.
- Mechanisms: noise texture, table lines, column separators, popups, card outlines.

### Comparison v3–v5
- Groups by: profile block, sticky city bar, section blocks, matrix tables, notes areas, city intelligence cards, modals.
- Mechanisms: flat borders, row shading, label columns, block headers, card outlines, modal overlays.

### City Profiles v1–v4
- Groups by: app nav, hero snapshot, photo strip, sections, accordions, cost/weather panels, visa block, intentions block.
- Mechanisms: card outlines, section separators, accordion row borders, indentation, cost/weather table/list structure.

### App Shell
- Groups by: banner/header, route nav buttons, panels, stubs/future boxes, context chip, debug block, modal backdrop.
- Mechanisms: scaffold boxes, dashed borders, warning/notice boxes, utility tables.

---

## 8. Open Questions

Unresolved tensions only; no answers selected.

- **Glow vs shadow:** when should hierarchy come from atmospheric glow vs ordinary elevation?
- **Texture vs color:** which surfaces need texture to avoid sterility, and which should remain flat/functional?
- **Border vs spacing:** how much grouping should be explicit lines/cards versus implied by layout?
- **Dense vs airy:** dense data is product value; how much air can be added without under-informing?
- **Atmosphere vs distraction:** how much wheel/card/page atmosphere supports confidence before it becomes decorative?
- **Home vs guest visual distinction:** current mechanisms exist; final language not selected.
- **Chart-table vitality:** chart reference cards currently have gentle depth; comparison matrices are flat. Should these families remain different?
- **Map visual language:** map is utilitarian/slate and runtime-heavy; how much product warmth should enter map controls/popups?
- **City intelligence vitality:** city pages rely mostly on structure and content; should they gain more atmospheric surface treatment later?
- **Modal language:** chart modal, comparison modal, city modal, app-shell modal differ. Should all modal focus systems converge?
- **Dashed/future/scaffold styling:** several placeholder/future elements use dashed boundaries. Keep this as scaffold-only or promote a future-state language?
- **Aura vs chart glow:** map aura/raster field and chart-wheel glow are different systems; relationship unresolved.
- **Selected/active states:** many controls use selected states, but no cross-surface doctrine exists yet.

---

## 9. Highest Value Standardization Targets

Prioritized visual organisms worth standardizing next. No solutions proposed.

1. **Wheel atmosphere system** — home/guest/relocated/modal wheel treatments, including glow, texture, ring hierarchy, and popout affordance.
2. **Chart reference card system** — `.tcard`, row shading, heading separators, card boundary/depth for PiH/AiS/A2A.
3. **Comparison matrix system** — row shading, column separation, block headers, sticky city bar grouping.
4. **Metadata / system block grouping** — `.meta-block`, `.sys-meta`, plate-adjacent dense metadata.
5. **Separator strength scale** — strong/medium/subtle/nearly-invisible separators across chart, comparison, city, and popup surfaces.
6. **Modal/backdrop language** — chart enlargement vs picker/info vs scaffold modal.
7. **City intelligence grouping** — snapshot grid, accordion rows, cost/weather detail tables, CI cards.
8. **Map popup preview grouping** — micro table, angle summary, action row, policy/provenance notes.
9. **Selected/active/disabled state language** — pills, tabs, buttons, currency/weather toggles, city controls.
10. **Scaffold/future/debug visual language** — app shell, dashed stubs, future-only boxes, debug tables should stay quarantined or be explicitly standardized.
