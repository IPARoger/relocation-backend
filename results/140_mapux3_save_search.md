# MAP-UX-3: Production Save Search Pill

**Date:** 2026-06-20
**Slice:** MAP-UX-3
**Status:** Complete

---

## Goal

Add a visible Save Search pill to the production map chrome, wired to the existing
`saveCurrentInvestigation()` backend infrastructure, matching MAP-UX-1/2 visual language.

---

## What was implemented

### 1. Save Search pill DOM

```html
<button id="rm-save-pill"
        type="button"
        data-role="map-save-search"
        title="Save this search state to your investigations">
  <svg><!-- floppy disk icon --></svg>
  Save Search
</button>
```

Positioned `top: 136px; left: 12px` inside `#map` — directly below the
MAP-UX-2 history/pin strip, continuing the left-rail overlay column.

### 2. CSS

Frosted-card pill matching MAP-UX-1/2 visual language:
- Base: `background: rgba(251,253,255,0.93)`, `border: 1px solid #cfdde6`,
  `border-radius: 10px`, matching shadow and `backdrop-filter`.
- `.rm-save-saved`: green highlight (`color: #16a34a`, `border-color: #bbf7d0`)
  shown for 2.5 s after a successful save.
- `.rm-save-error`: red highlight shown for 3.5 s on failure.
- `:disabled`: `opacity: 0.55` during in-flight save.

### 3. JavaScript controller

`initSavePill()` IIFE:

- Clicking the pill:
  1. Disables itself and shows "⏳ Saving…"
  2. Calls `window.__rmSaveCurrentInvestigation()` — the existing, fully-wired
     production function that POSTs to `/saved-investigations/create` via Supabase JWT.
  3. Reads `#saveInvestigationStatus.classList` to detect whether the panel form
     reported an error.
  4. On success: transitions to green "✓ Saved" for 2.5 s, then reverts.
  5. On error: transitions to red "⚠ …" for 3.5 s, then reverts.

**Production wiring:**
`window.__rmSaveCurrentInvestigation` was already exposed in the MAP-UX-1 era from
`window.__rmSaveCurrentInvestigation = saveCurrentInvestigation` (line ~1908). No new
backend wiring required.

**Future integration path** (documented in JS comment):
> When the Save Search flow is decoupled from the panel form (e.g., `saveCurrentInvestigation`
> is refactored to be panel-independent), replace the `__rmSaveCurrentInvestigation` call
> with a direct call to the new save API. The error-detection via `#saveInvestigationStatus`
> can also be replaced by a returned status object at that point.

`window.__rmSavePillReset` exposed for smoke test / future integration testing.

### 4. Panel save button preserved

The existing `#saveInvestigationBtn` (in the side panel with the note textarea) is
untouched. It remains available for users who want to add a note before saving.
The pill is a one-click convenience trigger for the same backend path.

### 5. Walkthrough step 7 selector updated

| Step | Old selector | New selector |
|------|-------------|-------------|
| Save Search (step 7) | `#saveInvestigationBtn` | `[data-role="map-save-search"]` |

The new selector targets the pill (visible on map canvas) rather than the panel button
(behind the walkthrough mask).

---

## Files changed

| File | Change |
|------|--------|
| `map_CURRENT.html` | Added save pill CSS, DOM, JS controller; updated walkthrough step 7 selector |

## Files NOT changed

- `app_shell.html` — no handoff changes
- Backend save endpoint (`/saved-investigations/create`) — untouched
- Genie, rendering engine, overlays — untouched
- `#saveInvestigationBtn` panel button — preserved

---

## Visual hierarchy (left rail, top to bottom)

| Element | top | left |
|---------|-----|------|
| `#rm-map-nameplate` (MAP-UX-1) | 12px | 12px |
| `#rm-map-controls` history/pin (MAP-UX-2) | 90px | 12px |
| `#rm-save-pill` (MAP-UX-3) | 136px | 12px |

---

## Validation

| Smoke | Result |
|-------|--------|
| `smoke_map_current.py` | PASS (overall_pass: true) |
| `smoke_onboarding_walkthrough_framework.py` | PASS (all 8 checks) |

---

## Non-goals (deferred)

- Morph-to-disk animation (present in sandbox; not migrated)
- Panel form independence (note textarea remains in panel for now)
- Offline / unsaved indicator badge
- Ghost strip / Mute-Solo-Not controls (MAP-UX-4 or later)
