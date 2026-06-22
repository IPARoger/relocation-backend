# 229 — PROFILE-HARMONIZATION-1 Audit

**Date:** 2026-06-22  
**Mode:** Audit only (no code, no commits)  
**Baseline:** `validation/mockups/beta/profile_standard.html` (approved Profile UX)  
**Live surface:** `#/chart-record` · `screenChartRecord()` · `hydrateProfileNatalFacts()` · `renderProfileNatalChartHtml()` in `app_shell.html`  
**Prior wiring:** `results/212_profile_wiring_reality_audit.md`, `results/224_profile_natal_wheel_1_closeout.md`

---

## Executive summary

**Data wiring is no longer the gap.** PROFILE-NATAL-WHEEL-1 successfully hydrates natal wheel, PIH, AIS, and A2A from canonical natal data.

**The live Profile page still reads as an application-shell dashboard**, not the approved Profile mockup. Natal facts exist but are rendered inside generic `.panel` stacks with shell table chrome, wrong section order, and dashboard placement for notes / favorites / saved work.

The approved design is a **two-band chart page**:

1. **Chart stage** — identity plate left, natal wheel right (peer elements, not nested).
2. **Table band (`tband`)** — AIS · PIH · A2A · Notes in one horizontal row (4-column grid).
3. **Lower band** — favorites, saved comparisons, saved searches/investigations below a rule (mockup HTML defers this block; CSS and defer-note confirm intended placement).

Live Profile inverts or scatters all three bands.

---

## Approved structure (reference)

From `profile_standard.html`:

| Zone | Approved contents | Visual system |
|------|-------------------|---------------|
| **chart-stage** | `zone-b` identity (name switcher, birth lines, coords, zodiac/house system) + `wheel-slot` (560px disc, enlarge affordance) | `identity_stamp.css`, warm paper, serif name |
| **sec-rule** | Hairline between stage and tables | — |
| **tband.std** | Col 1: **Angle in Sign** · Col 2: **Planet in House** · Col 3: **Aspect to Angle** (matrix + angle pills) · Col 4: **Notes** card | `tcard` + `tint-ais` / `tint-pih` / `tint-a2a`, collapse, texture-stripe tables |
| **lower** *(deferred in mockup HTML, specified in CSS)* | City search + favorites + compare CTA · saved comparisons list · saved searches/investigations | `.lower` 3-column grid below tables |

Mockup defer-note explicitly places **Favorites / Saved Comparisons / Saved Searches below** the table band — not beside identity, not above tables.

Relocated chart mockup (`relocated_standard.html`) shares the same **chart-stage + tband** grammar; Profile differs only in identity content (natal birth facts, no relocated location block) and omits Location Intelligence.

---

## Live structure (today)

`screenChartRecord()` renders, top to bottom:

1. Breadcrumb `Profile · {name}` + `<h2>Profile</h2>` + purpose paragraph
2. Time-uncertainty warning (if applicable)
3. **Identity** — `.panel` with text summary, raw `chartRecordId` code, birth-data / set-location buttons
4. **Natal chart** — `.panel` > `#rm-profile-natal-facts` hydrated as vertical stack:
   - `Natal wheel` (h4)
   - `Planet houses` (h4) + `simple` table with **Longitude** column
   - `Angles in Signs (AIS)` (h4) + `simple` table
   - `Aspect to Angle` (h4) + flat `rm-a2a-table`
5. **Notes** — separate `.panel`, plain textarea + Save
6. **Launch row** — Open Map, Export/share status, Notes Library, Settings
7. **grid-2** — Favorites | Saved explorations
8. **Comparison sets** — separate `.panel` with async list

Shell nav still labels route **"Screen 1 — Chart Record Page"** (`NAV_ITEMS`).

---

## Deviation matrix

### 1. Missing sections

| Approved | Live | Gap |
|----------|------|-----|
| `chart-stage` layout wrapper | — | No identity+wheel stage band |
| `sec-rule` between wheel and tables | — | Missing visual section break |
| `tband` 4-column table band | — | Tables not in horizontal band |
| Notes inside `tband` col 4 (`notes-card`) | Notes in standalone panel above launches | Wrong placement + chrome |
| Wheel popout / enlarge affordance | — | No disc popout on Profile wheel |
| PIH dignities toggle (`dig-toggle` footer) | `dignitiesOn: false`, no toggle UI | Missing approved control |
| A2A angle pills (ASC / DSC / MC / IC / All) + matrix viewport | Flat single-place A2A table | Wrong A2A surface |
| Profile name switcher + Edit / + tools | Text-only identity | Missing approved identity tools |
| `identity_stamp.css` warm profile theme | `genie_variable_builder.css` shell panels | Wrong visual family |

**Not missing (data present, layout wrong):** natal wheel, PIH, AIS, A2A, notes (functional), favorites, saved explorations, comparison sets, map/chart/compare launches.

**Correctly absent on Profile (per mockup):** Location Intelligence block (relocated-only).

---

### 2. Incorrect section ordering

| Approved order | Live order | Issue |
|----------------|------------|-------|
| Identity **beside** wheel | Identity **above** wheel panel | Wheel not peer to identity |
| AIS → PIH → A2A → Notes (horizontal) | Wheel → PIH → AIS → A2A (vertical) | Wrong table order and orientation |
| Notes in tband col 4 | Notes before launch buttons, before favorites | Notes pulled up into dashboard middle |
| Favorites / saved work **below** tband | Favorites / explorations / comparison sets **after** notes + launch row | Lower band content exists but sits in wrong vertical position relative to chart facts |

`renderProfileNatalChartHtml()` order (`wheel → PIH → AIS → A2A`) does not match mockup tband order (`AIS → PIH → A2A`).

---

### 3. Legacy labels

| Location | Live label | Approved label |
|----------|------------|----------------|
| Shell nav | `Screen 1 — Chart Record Page` | Profile |
| Page title area | `Profile` + breadcrumb `Profile · …` | Nav context only; mockup uses inline name plate |
| PIH section | `Planet houses` | `Planet in House` |
| AIS section | `Angles in Signs (AIS)` | `Angle in Sign` |
| Notes placeholder | `Notes for this Chart Record` | `Write or dictate a note…` |
| Saved block | `Saved explorations` | Mockup lower band: saved searches / investigations (same concept, different naming) |
| Identity meta | `Current city:` line in identity panel | Mockup: birth facts in zone-b only (current location is relocated-chart concern) |

---

### 4. Placeholder labels / copy

| Live copy | Nature |
|-----------|--------|
| `Identity, natal chart, notes, favorites, saved explorations, and launches…` (purpose paragraph) | Shell walkthrough copy — not in mockup |
| `Loading natal chart…` / `Loading comparison sets…` | Acceptable hydration states; mockup has no async |
| `No favorite places saved yet. Open the map…` | Functional empty state; mockup uses list chrome not paragraph coaching |
| `Favorite place` sublabel on each favorite | Dashboard list artifact |
| `Export / share status` button | Points to non-profile route; not in approved Profile chrome |
| Raw `<code>{chartRecordId}</code>` in Identity | Dev/debug artifact |

---

### 5. Missing wheel placement

| Approved | Live |
|----------|------|
| `#wheel` in `wheel-slot`, centered in chart-stage, ~560px disc, gold home glow, `⤢ Enlarge` chip | Wheel nested inside **Natal chart** panel under h4 heading; shell SVG wheel (`renderRelocatedWheelHtml`) without disc wrapper or popout |

Wheel is **present but mis-placed** — buried one level too deep and lacking mockup disc container.

---

### 6. Missing table placement

| Approved | Live |
|----------|------|
| AIS, PIH, A2A as sibling `tcard` cells in `tband.std` (8 : 8 : 13 : 5 grid) | Each table stacked vertically inside `#rm-profile-natal-facts` |
| Tables share row with Notes | Notes separated into own panel |

Table **data** renders; **placement** does not match approved band.

---

### 7. Missing notes placement

| Approved | Live |
|----------|------|
| `notes-card` as 4th `tband` column; toolbar (B/I/U/list/mic); popout button; hint text | Plain textarea in isolated panel between natal facts and action buttons |
| Same vertical band as AIS/PIH/A2A | Notes interrupt flow between chart facts and favorites |

Save path (`save-chart-note`) is live; **layout and chrome** are not harmonized.

---

### 8. Missing favorites placement

| Approved | Live |
|----------|------|
| Lower band col 1: city search input, favorites list with star/checkbox/trash, compare-selected CTA | `grid-2` panel with checkbox list + per-row action button cluster |
| Below table band | Above comparison sets but below notes/launches — not in lower band |

Favorites **function** is wired; **placement and list chrome** do not match mockup lower band.

---

### 9. Missing saved investigation placement

| Approved | Live |
|----------|------|
| Lower band col 3: saved searches list with meta + notes-link | `Saved explorations` panel in `grid-2` beside favorites |
| Grouped with favorites/comparisons below charts | Mixed into mid-page dashboard grid |

Resume / rename / archive actions are live; **section placement and naming** diverge.

---

### 10. Dashboard-era artifacts (remaining)

| Artifact | On Profile route? |
|----------|-------------------|
| `.panel` / `.grid-2` shell scaffolding | **Yes** — entire page |
| `purpose` paragraph | **Yes** |
| Breadcrumb + generic `<h2>` | **Yes** |
| `Module:` headings | **No** (dashboard only) |
| `stateDebugBlock()` | **No** (dashboard only) |
| `must-not` box | **No** on chart-record (dashboard only) |
| Nav label `Screen 1 — Chart Record Page` | **Yes** (shell nav) |
| `simple` table class vs `rt`/`tcard` | **Yes** — all natal tables |
| Per-favorite button row (Open map / View chart / Archive) | **Yes** — denser than mockup fav list |
| Launch row (Settings, Notes Library, Export) | **Yes** — not in profile mockup header area |
| PIH **Longitude** column | **Yes** — mockup PIH is planet + house only on Profile |
| A2A **Orb limit** column + list rows | **Yes** — mockup uses matrix cells |
| `engineEligibilityLine` / UUID in identity | **Yes** — dev-facing |

---

## Table / renderer specifics (live vs mockup)

| Surface | Mockup | Live (`renderProfileNatalChartHtml` + shared renderers) |
|---------|--------|--------------------------------------------------------|
| **PIH** | Planet + house only; late-house `?` marker; dignities toggle | Planet + house + **longitude**; no late-house marker; no dignities toggle |
| **AIS** | Fixed 3-col grid: label \| deg · sign · min (centered) | Two-col: Angle \| combined longitude string |
| **A2A** | Matrix: planet column + angle viewport + ASC/DSC/MC/IC/All pills | Single-place sortable table (planet, aspect, angle, orb, orb limit) |
| **Wheel** | Mock SVG in disc; stroke sign glyphs | Production `renderRelocatedWheelHtml` (WHEEL-v2 grey palette); functionally correct, visually different container |

Reuse of canonical renderers is correct architecturally; **Profile needs mockup-facing adapters or a profile-specific layout shell** around the same data — not new endpoints.

---

## What not to change (explicit)

Per task constraints — **out of scope for harmonization slices:**

- No new profile concept or alternate information architecture
- No changes to Comparison or Relocated Chart page concepts
- No country-first UX
- No new backend endpoints (natal hydration path stays)
- Mockup items explicitly deferred in `profile_standard.html` defer-note: animated table drawer, full typography/font pass, aspect-label setting UX, animation pacing, centered logo menu — **document only**, do not invent

---

## Punch-list: smallest implementation slices

Ordered for minimal diff risk. Each slice should touch `app_shell.html` + profile-scoped CSS only unless noted. Reuse existing renderers; wrap/reorder rather than rewrite astrology.

### PH-1 — Profile chart-stage shell
Introduce `chart-stage` / `identity-stack` / `zone-b` / `wheel-slot` markup in `screenChartRecord()`. Move wheel out of `#rm-profile-natal-facts` into `wheel-slot`. Load `identity_stamp.css` (or extracted tokens) on chart-record route only.

### PH-2 — Identity plate harmonization
Replace Identity `.panel` text block with mockup-shaped zone-b (name, birth date/time, birth place, coords, zodiac/house system). Wire existing profile switcher / Edit / + only if already available in shell; otherwise stub buttons with approved labels only (no new flows).

### PH-3 — Extract wheel from natal facts renderer
Split `renderProfileNatalChartHtml()` so wheel renders to `wheel-slot` and tables render to `tband`. Remove nested `h4` section headings.

### PH-4 — Profile tband grid + section order
Add `tband std` container. Render **AIS → PIH → A2A** in mockup order (horizontal). Apply `tcard` / `tint-*` / `card-head` / `ch-title` labels: **Angle in Sign**, **Planet in House**, **Aspect to Angle**.

### PH-5 — Notes into tband col 4
Move `#rm-chart-note` into `notes-card notes-slot` as 4th tband column. Keep existing save handler. Defer toolbar/mic/popout unless already implemented elsewhere.

### PH-6 — PIH profile column shape
On Profile only: drop longitude column from PIH (mockup shows house only). Optional: wire late-house `?` marker when dignity/house-proximity data exists.

### PH-7 — PIH dignities toggle on Profile
Add mockup `dig-toggle` footer to Profile PIH card; bind to existing dignities renderer path (`dignitiesOn` toggle) already used on relocated/comparison.

### PH-8 — AIS profile cell layout
Profile-only adapter: render AIS rows in mockup `vgrid` (deg · sign · min) instead of plain text longitude cells. Reuse glyph-aware longitude formatters.

### PH-9 — A2A profile matrix
Replace Profile `renderA2aSinglePlaceHtml` list with comparison-style A2A matrix + angle pills (`ASC`/`DSC`/`MC`/`IC`/`All`). Reuse matrix builders with single column.

### PH-10 — Lower band placement
Move Favorites, Saved explorations, Comparison sets into `.lower` 3-column grid **below** `sec-rule` + `tband`. Match mockup list chrome incrementally (star, trash, compare CTA).

### PH-11 — Launch / dev chrome cleanup
Remove or relocate: purpose paragraph, raw UUID, Export/share + Settings from primary Profile body (keep launches mockup implies: map via favorites / lower band). Rename nav item to **Profile**.

### PH-12 — Wheel disc affordances
Wrap production wheel SVG in mockup `disc` container; add non-blocking enlarge/popout hook (can remain stub modal if production popout not ready).

### PH-13 — Visual QA smoke
Add static smoke: profile route contains `chart-stage`, `tband`, `wheel-slot`, correct tband child order, `notes-slot` — no assertion on dashboard `.panel` wrapping natal tables.

---

## Suggested slice grouping (release windows)

| Window | Slices | Outcome |
|--------|--------|---------|
| **A** | PH-1, PH-2, PH-3, PH-11 | Profile reads as chart page: identity beside wheel, dev chrome gone |
| **B** | PH-4, PH-5, PH-6, PH-7, PH-8 | Table band matches mockup structure and labels |
| **C** | PH-9, PH-10, PH-12 | A2A matrix + lower band + wheel polish |
| **D** | PH-13 | Regression guard |

---

## Conclusion

The live Profile page **has the right natal facts** after PROFILE-NATAL-WHEEL-1 but **does not match the approved Profile UX**. The gap is almost entirely **layout, labeling, and shell chrome** — not data or architecture.

**Smallest path to harmonization:** adopt the mockup's three-band page grammar (chart-stage → tband → lower), reorder sections to **AIS · PIH · A2A · Notes**, place identity and wheel as peers, and demote dashboard `.panel` scaffolding. Implement as PH-1 through PH-13 without redesigning the settled Profile concept.
