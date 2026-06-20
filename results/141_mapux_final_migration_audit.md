# MAP-UX Final Migration Audit

**Date:** 2026-06-20
**Type:** Audit only — no implementation
**Scope:** map_SANDBOX_genie_v7.html (intended UX) vs map_CURRENT.html (production)
**Status:** Pre-MAP-UX-4 checkpoint

---

## Important Context Note

The user has flagged that the map was "95% right and working almost perfectly" at some
earlier state, with only a few remaining items: Map Notes section, some animation
roughness, and nameplate positioning. This audit is intended to verify the current
state honestly and prevent unnecessary rework.

---

## 1. Complete Inventory of UX Elements in Sandbox

### Fixed overlays (always visible, positioned on map)

| Element | CSS class/ID | Position |
|---------|-------------|----------|
| Zoom controls | `.mapctrls .ctrl-card.zoomcol` | `left:16px; top:62px` |
| History Back / Forward / Pin group | `.mapctrls .ctrl-card.navgrp` | `left:16px; top:62px` (beside zoom) |
| Centered city search | `.ov.citysearch` | `left:50%; top:60px; transform:translateX(-50%)` |
| Profile nameplate (plate) | `.ov.plate` | `left:16px; top:188px` |
| Genie builder rail | `.ov.rail` | `right:16px; top:62px` |

### Explore-mode-only overlays (hidden until search executes)

| Element | CSS class/ID | Behavior |
|---------|-------------|---------|
| Reopen-Genie bottle button | `.ov.bottle` | Appears when `body.explore`; builder collapses |
| Ghost variable strip | `.ov.ghoststrip` | Appears when `body.explore`; per-variable NOT/Mute/Solo/color |
| Overlay depth slider | `.ov.lab` | Appears when `body.explore` |
| Save disk (floating floppy) | `.ov.save-disk` | Appears when `body.explore`; morphs from inline pill |

### Topbar (persistent header)

| Element | Notes |
|---------|-------|
| Brand wordmark ("Relocation") | Left |
| Hamburger (`menu-handle`) — appears in explore mode | Left |
| Main nav: Map / Profile / Comparison / Help / Settings | Collapses in explore |
| Share button | Right; morphs to square icon in explore |
| Account label / owner | Right |

### Save popover (modal, triggered by disk or inline pill)

| Element | Notes |
|---------|-------|
| Auto-named title input | Editable |
| Rich-text note area (Bold/Italic/Underline) | Contenteditable |
| Mic button ("Record a voice note") | Stub/future |
| Save / Close actions | Standard |

### Animations / transitions of note

| Transition | What happens |
|-----------|-------------|
| `body.explore` class toggle | Builder shrinks and fades; bottle appears; ghost strip appears; topbar dissolves |
| Navbtn Full → Mini labels | 2.4 s cubic-bezier; text labels cross-fade to `‹ ›` glyphs |
| Ghost strip entrance | `ghostStripIn` animation: blur + translateX from right |
| Plate ghost-over-map | Box/shadow/backdrop drop; name text gets white halo outline |
| Save pill → disk fly | `flySave()` — inline pill animates to floating disk position |
| Bottle "breathe" pulse | `@keyframes breathe` on the reopen button |

---

## 2. What Already Exists in Production (map_CURRENT.html)

### Full production wiring (pre-MAP-UX work)

| Element | Production equivalent | Notes |
|---------|-----------------------|-------|
| Genie variable builder | Right-side panel with Genie builder via `genie_variable_builder.js` | Fully wired to real API |
| Chart profile selector | `<select id="chartProfile">` in side panel | Wired to `/chart-profiles` + Supabase |
| Map location search | `<div id="rm-map-loc-search-mount">` | Wired to saved-location search service |
| Save investigation | `#saveInvestigationBtn` + `saveCurrentInvestigation()` | POSTs to `/saved-investigations/create` |
| Onboarding walkthrough | `#rm-walkthrough` overlay | 7-step peep-hole framework |
| Zoom controls | Via Leaflet default control | Native Leaflet; positioned differently |

### No existing production equivalent (pre-MAP-UX)

These were missing before the MAP-UX slice series began:
- Profile nameplate on map canvas
- History back/forward buttons on map canvas
- Pin button on map canvas
- Save Search pill on map canvas

---

## 3. What Was Already Migrated (MAP-UX-1 through MAP-UX-3)

| Slice | Element | Status | data-role |
|-------|---------|--------|-----------|
| MAP-UX-1 | Profile nameplate (`#rm-map-nameplate`) | ✅ Migrated | `map-profile-selector` |
| MAP-UX-1 | Caret → opens `#chartProfile` | ✅ Wired | — |
| MAP-UX-2 | History back button (`#rm-ctrl-back`) | ✅ Migrated | `map-history-back` |
| MAP-UX-2 | History forward button (`#rm-ctrl-fwd`) | ✅ Migrated | `map-history-forward` |
| MAP-UX-2 | Pin button (`#rm-ctrl-pin`) | ✅ Migrated | `map-pin` |
| MAP-UX-2 | History stack (wraps `executeSearchPlan`) | ✅ Wired | — |
| MAP-UX-2 | Pin state (sessionStorage) | ✅ Wired | — |
| MAP-UX-3 | Save Search pill (`#rm-save-pill`) | ✅ Migrated | `map-save-search` |
| MAP-UX-3 | Pill → calls `saveCurrentInvestigation()` | ✅ Wired | — |

**Left-rail column position:**

| Element | top | left |
|---------|-----|------|
| Nameplate | 12px | 12px |
| History/Pin strip | 90px | 12px |
| Save Search pill | 136px | 12px |

---

## 4. Remaining Migration Items

### Tier A — Clearly intended, not yet migrated

| Item | Sandbox reference | Notes |
|------|------------------|-------|
| **Ghost variable strip** | `.ov.ghoststrip` — per-variable NOT / Mute / Solo / color swatch | The most meaningful UX feature; appears in explore mode; shows active conditions |
| **Reopen-Genie bottle button** | `.ov.bottle` | Appears when builder collapses in explore mode; badge shows active variable count |
| **Explore mode toggle** (`body.explore`) | Triggered when map search executes | The state transition that collapses builder, reveals ghost strip, dissolves topbar |
| **Map Notes** | `.sp-notes` in save popover (contenteditable) | User noted this was missing; needed before MAP-UX is called done |

### Tier B — Likely intended but requires review

| Item | Sandbox reference | Question |
|------|------------------|---------|
| **Centered city search** | `.ov.citysearch` at `left:50%; top:60px` | Production already has location search in side panel (`#rm-map-loc-search-mount`). Does the centered overlay replace it, or supplement? |
| **Overlay depth slider** | `.ov.lab` — right side, explore mode only | Controls overlay opacity/blending depth. Does production Genie adapter support this? |
| **Save disk → morph animation** | `flySave()` — pill flies to floating disk | The pill (MAP-UX-3) is static. Should it morph/fly in explore mode? |
| **Topbar dissolve in explore mode** | `body.explore .topbar { background:transparent }` | Production map has no topbar — it's embedded in `app_shell.html`. This likely does not apply to the production iframe/handoff flow. Needs review. |
| **Share button** | `.share` in topbar | Same topbar question — applies to standalone map URL only, not app shell flow. |

### Tier C — Sandbox-only / mock / prototype artifacts

| Item | Reason to skip |
|------|---------------|
| Mock overlay engine | `seededZones()` — production uses real `/search-regions` API |
| Mock profile data | Hardcoded `PROFILE` object — production reads from Supabase |
| Save popover rich-text formatting (Bold/Italic/Underline) | Over-engineered for v1; plain text sufficient |
| Mic button ("Record a voice note") | Stub in sandbox; no backend; defer |
| Topbar brand / nav | Production map is accessed via `app_shell.html` which provides nav; map file itself has no topbar |

---

## 5. Design Inconsistencies / Unfinished Areas in Sandbox

| Area | Observation |
|------|------------|
| **Nameplate position** | Sandbox: `top:188px` (below zoom + navgroup, which are at `top:62px`). Production MAP-UX-1: `top:12px`. The production nameplate sits at the very top-left — above where the sandbox places it. **This is a known positioning issue the user noted.** |
| **Nameplate size/font** | Sandbox uses `font-family:var(--serif); font-size:25px; font-weight:600` — large serif treatment. Production nameplate is `system-ui; 14px; 600` — much smaller. The intended treatment is the large serif nameplate. |
| **History/Pin strip** | Sandbox groups zoom + history/pin in a single `.mapctrls` row with two `ctrl-card` cards side by side. Production separates them (no zoom card; just a history/pin pill). Functionally equivalent but visually different from sandbox. |
| **Save disk** | Sandbox uses a floating disk at `right:46px; bottom:34px` that morphs from inline pill. Production has a pill at `top:136px; left:12px`. Different visual concept — pill is correct UX idea, position is different from sandbox. |
| **Explore mode** | Sandbox has a complete `body.explore` state machine. Production has no equivalent `explore` class mechanism — this is the largest structural gap. |
| **Ghost strip** | Sandbox ghost strip is right-side, vertically centered (`top:46%; transform:translateY(-50%)`). Production has no ghost strip. |

---

## 6. Areas Requiring User Review Before Migration

| Area | Question |
|------|---------|
| **Nameplate position and size** | User noted "the placement for the nameplate needed to be perfected." The intended position is `top:188px` (below the zoom/nav controls at `top:62px`). The intended font is large serif (25px). Should MAP-UX-1 nameplate be repositioned and restyled to match? |
| **Zoom controls** | Sandbox has a styled zoom column (`+/–/○`) at `top:62px`. Production uses native Leaflet zoom control. Should the styled zoom card be migrated, or is native Leaflet zoom acceptable? |
| **Centered city search** | Sandbox places the city search as a centered overlay at `top:60px`. Production has it in the side panel. Does the centered overlay replace the panel search, or is the panel placement acceptable? |
| **Explore mode** | The `body.explore` state machine (builder collapses, ghost strip appears, topbar dissolves) is the largest missing structural piece. Is this an intended migration target? It requires wiring to Genie's search execution. |
| **Map Notes** | The sandbox save popover includes a Map Notes field. The production save form (`#saveInvestigationNote`) already has a plain-text note field. Does the contenteditable rich-text notes field need to be migrated, or is the plain text field sufficient? |
| **Animations** | User noted "some animations were still a little rough." The sandbox has named keyframes (`ghostStripIn`, `bottleIn`, `breathe`, `flySave`). Which specific animations need to be implemented or smoothed? |

---

## 7. Recommended Final Migration Order

Based on user intent (minimum rework, maximum value):

### Immediate (blocking or near-complete)

| Priority | Item | Rationale |
|----------|------|-----------|
| 1 | **Fix nameplate position + size** | User explicitly noted this; known gap; small CSS change |
| 2 | **Map Notes** in save popover | User explicitly noted this was missing |

### Next (core explore-mode features)

| Priority | Item | Rationale |
|----------|------|-----------|
| 3 | **Explore mode state machine** (`body.explore`) | Prerequisite for ghost strip, bottle, animations |
| 4 | **Ghost variable strip** (Mute/Solo/Not tokens) | Core product UX; most novel control; key onboarding step |
| 5 | **Bottle / reopen-Genie button** | Part of explore mode; simple once explore mode exists |

### Review-gated (needs user decision)

| Priority | Item | Rationale |
|----------|------|-----------|
| 6 | **Zoom controls styling** | Replace native Leaflet zoom with styled card? |
| 7 | **Centered city search** | Replace or supplement panel search? |
| 8 | **Save disk morph animation** | Cosmetic; can be deferred |
| 9 | **Topbar dissolve in explore** | May not apply to app-shell flow |

---

## Summary Assessment

The MAP-UX-1/2/3 work added the correct chrome elements (nameplate, history/pin, save
pill) with proper onboarding selectors and production wiring. No rework of those slices
is needed.

The two items the user identified as missing — **nameplate position/styling** and
**Map Notes** — are the highest-priority remaining items and are small in scope.

The largest remaining structural work is the **explore mode state machine** and
**ghost variable strip**, which together represent the "collapse builder on search,
show active conditions as ghost tokens" flow that is the most distinctive UX difference
between sandbox and current production. This is a larger slice (MAP-UX-4 or MAP-UX-5)
and should be scoped carefully.

No rework of MAP-UX-1/2/3 is recommended. Proceed with nameplate refinement and Map
Notes first.
