# 202 — MAP-PRODUCTION-MOTION-A Closeout

**Date:** 2026-06-22  
**Type:** Implementation — Phase A object permanence only  
**Prerequisite:** `201_production_migration_plan.md`  
**File changed:** `map_CURRENT.html` only (no `app_shell.html`, no new chrome)

---

## Goal

Port Phase A animation architecture from sandbox doctrine into production:

- Bottle always in DOM (`opacity:0`, never `display:none`)
- Panel ↔ bottle two-rAF FLIP in `enterExplore()` / `exitExplore()`
- Ghost strip opacity/visibility permanence (no `display` toggle)
- Save pill pre-rendered state spans (no `innerHTML` state swaps)

**Explicitly out of scope:** notebook, share, hamburger, fader creation; visual/timing/easing redesign.

---

## Changes Applied

### 1. Panel CSS (`#panel` explore rule)

- Removed `width:0 !important`, padding collapse, and CSS-driven opacity collapse
- `body.rm-explore #panel` now sets only `pointer-events: none`
- Added `.rm-panel--flip-hidden` helper class for post-FLIP hide

### 2. Bottle CSS (`#rm-bottle`)

- Base: `display:flex; opacity:0; pointer-events:none` (always measurable)
- Removed `body.rm-explore #rm-bottle` display toggle and `@keyframes rmBottleIn`
- Added `.rm-bottle--revealed` (opacity + pointer-events) revealed by JS after FLIP arrival
- Kept `rmBreathe` hover animation on `.rm-bottle--revealed:hover`

### 3. Ghost strip CSS (`#rm-ghost-strip`)

- Base: `display:flex; opacity:0; visibility:hidden` with explore chrome styles always present
- Explore: `opacity:.72; visibility:visible` + existing `rmGhostStripIn` animation
- Removed `display:none` / `display:flex` toggle

### 4. Save pill HTML + CSS + JS

- Pre-rendered spans: `.rsp-idle`, `.rsp-saving`, `.rsp-saved`, `.rsp-error`
- CSS class toggles show/hide spans per state
- `setPillState()` toggles classes only; error text via `textContent` on `.rsp-error`
- Removed all `pill.innerHTML` usage

### 5. `enterExplore()` / `exitExplore()` JS

- **enterExplore:** measure panel + bottle rects → FROM state (no transition) → `rm-explore` class → two-rAF TO transform → reveal bottle at t=1950ms → fade panel → `.rm-panel--flip-hidden`
- **exitExplore:** reverse FLIP — snap panel to bottle rect → fade bottle → two-rAF expand panel → remove `rm-explore` at 500ms → cleanup at 1800ms

---

## Validation

### Static smoke

```bash
python3 scripts/smoke_map_production_motion_a.py
```

**Result:** PASS 12/12

| Check | Result |
|-------|--------|
| `#rm-bottle` never `display:none` | PASS |
| No `body.rm-explore #rm-bottle` rule | PASS |
| No `@keyframes rmBottleIn` | PASS |
| Panel no `width:0` collapse | PASS |
| Ghost strip no `display` toggle | PASS |
| `.rm-bottle--revealed` present | PASS |
| `.rm-panel--flip-hidden` present | PASS |
| `enterExplore` two-rAF FLIP | PASS |
| `exitExplore` two-rAF FLIP | PASS |
| `setPillState` no `innerHTML` | PASS |
| Save pill pre-render spans | PASS |

### Architecture invariants (post-change)

- Bottle `getBoundingClientRect()` valid before explore (always `display:flex`)
- Panel geometry driven by JS transform, not CSS width collapse
- Ghost strip always in layout flow; visibility via opacity/visibility only
- Save pill child nodes persist across state changes

---

## Rollback Scope

Revert single commit touching `map_CURRENT.html`. No backend, settings, or app shell changes.

---

## Not Migrated (unchanged from 201)

Sandbox-only elements remain absent from production:

- Notepad
- Share button
- Hamburger/navigation
- Fader

Nameplate: already DOM-permanent; no Phase A work required.

---

## Recommended Next Step

Manual browser QA: run a search → confirm panel morphs to bottle (not pop/substitute) → click bottle → confirm reverse FLIP. Then Phase B (nameplate explore visuals) or sandbox chrome creation as separate slices.
