# MAP-UX-4 — Ghost Strip and Explore Mode

**Date:** 2026-06-20  
**Slice:** MAP-UX-4  
**Files changed:** `map_CURRENT.html`  
**Reference design:** `map_SANDBOX_genie_v7.html`

---

## Goal

Add Ghost Strip (per-variable Mute/Solo/Not tokens) and Explore Mode state machine
to production `map_CURRENT.html` — so that after a search executes, the Genie builder
panel collapses, a ghost strip of active conditions appears, and a bottle button
restores the builder.

---

## What Was Added

### 1. Explore mode (`body.rm-explore` class)

A CSS class on `<body>` drives all explore-mode transitions:

```css
body.rm-explore #panel       { width: 0; padding: 0; opacity: 0; pointer-events: none; }
body.rm-explore #rm-ghost-strip { display: flex; animation: rmGhostStripIn … }
body.rm-explore #rm-bottle      { display: flex; animation: rmBottleIn … }
```

The panel collapses smoothly via `width` + `opacity` transition (800ms cubic-bezier),
causing `#map` (flex:1) to expand into the freed space. Ghost strip and bottle animate in.

### 2. Ghost Strip (`#rm-ghost-strip`, `data-role="map-ghost-strip"`)

Positioned `right: 18px; top: 46%` inside `#map` (absolute). Shows up to 4 condition tokens.

Each token (`.rm-gtok`) is a grid row: `label | NOT | Mute | Solo | color swatch`.

Button behaviors:
- **NOT** (✕): Marks variable as redacted — token gets `rm-notc` class, label dims, swatch squares
- **Mute** (M): Hides variable from overlays — token gets `rm-muted` class (opacity .32)
- **Solo** (S): Shows only this variable — others get `rm-dim` class (opacity .2)
- All are `aria-pressed` toggled; `syncGhost()` is called in-place (no innerHTML rebuild = no flash)

### 3. Bottle / Reopen button (`#rm-bottle`, `data-role="map-reopen-genie"`)

Positioned `right: 18px; top: 62px` inside `#map`. Hidden in setup mode, appears in explore mode
with `bottleIn` animation + `breathe` pulse after 2.1s. Clicking removes `body.rm-explore`,
restoring the panel with transition.

### 4. JS: `initGhostStrip()` IIFE

**`snapshotConditions()`** — reads up to 4 active conditions from production panel DOM at search time:
- Planet–House (Condition A / B / C): reads `#planetA` + `#houseA` etc.
- Angle–Sign: reads `#angleSignAngle` + `#angleSignSign`
- Aspect–Angle: reads `#overlayPlanet` + `#overlayAspect` + `#overlayAngle`
- Returns max 4 conditions; gracefully skips empty/partial rows

**`executeSearchPlan` wrap** — stacks on top of MAP-UX-2's wrapper:
```
MAP-UX-4 outer → MAP-UX-2 middle → original genie adapter
```
After the real search completes and MAP-UX-2 has captured its history snapshot,
MAP-UX-4 calls `enterExplore()`. History replays (`meta.source === 'history_replay'`)
do not re-trigger explore.

**Public API** on `window.__rmGhostStrip`:
```js
window.__rmGhostStrip.enterExplore()   // for onboarding step 4
window.__rmGhostStrip.exitExplore()
window.__rmGhostStrip.syncGhost()
window.__rmGhostStrip.conditions       // getter — snapshot array
```

---

## Preserved (untouched)

- Rendering engine, overlay calculations, chart math
- Onboarding walkthrough (`#rm-walkthrough`) and its step selectors
- Centered location search (`#rm-map-loc-search-mount`)
- MAP-UX-2 history/pin controls (`#rm-map-controls`, `#rm-ctrl-back/fwd/pin`)
- MAP-UX-2 `executeSearchPlan` wrapper (history stack)
- MAP-UX-2.6 identity stamp / nameplate (`#rm-map-nameplate`)
- MAP-UX-3 save pill (`#rm-save-pill`)
- Notes scratchpad (no change)

---

## Conservative Wiring — Future Integration Points

Two documented integration hooks left for future slices:

**1. Real overlay filtering (Mute/Solo/Not → overlays)**
```js
// When genie_map_engine_adapter exposes redrawWithFilters():
window.rmGenieAdapter.redrawWithFilters(activeConditions, soloId)
// Currently: Mute/Solo/Not are visual-only (CSS class toggles)
```

**2. Live condition sync**
```js
// When genie adapter exposes variableChange event:
window.rmGenieAdapter.on('variableChange', function(vars) {
    activeConditions = vars;
    syncGhost();
});
// Currently: conditions snapshot is taken once at search time from DOM
```

Both hooks are documented in code comments in the IIFE.

---

## Functional Test Results (Selenium, 1280×900)

| Check | Result |
|-------|--------|
| `#rm-ghost-strip` exists with `data-role="map-ghost-strip"` | PASS |
| `#rm-bottle` exists with `data-role="map-reopen-genie"` | PASS |
| Ghost strip hidden on load (setup mode) | PASS — `display: none` |
| Bottle hidden on load (setup mode) | PASS — `display: none` |
| Panel width in setup mode | 300px |
| After `enterExplore()`: `body.rm-explore` class | PASS |
| Ghost strip visible in explore | PASS — `display: flex` |
| Bottle visible in explore | PASS — `display: flex` |
| Panel width in explore | 0px (fully collapsed) |
| Condition tokens rendered (Mars 7th + ASC Scorpio) | 3 tokens (incl. combined) |
| First token label | `"Ma · 7"` |
| NOT button toggles `aria-pressed` + `.on` + `.rm-notc` | PASS |
| Bottle click removes `body.rm-explore` | PASS |
| Panel width restored after bottle | >50px |
| Nameplate x/y unchanged at (80, 132) | PASS |
| MAP-UX-2 controls preserved (`#rm-ctrl-back`) | PASS |
| MAP-UX-3 save pill preserved (`#rm-save-pill`) | PASS |
| Onboarding walkthrough preserved (`#rm-walkthrough`) | PASS |
| **OVERALL** | **PASS** |

---

## Onboarding Selector Added

Step 4 in the walkthrough can now target:
```js
data-role="map-ghost-strip"   // container
.rm-notb                      // NOT button  
.rm-mb                        // Mute button
.rm-sb                        // Solo button
```

`window.__rmGhostStrip.enterExplore()` can be called directly from the walkthrough
controller to demonstrate explore mode without requiring a real search execution.

---

## Deferred

- Overlay redraw with Mute/Solo/Not state (needs `rmGenieAdapter.redrawWithFilters`)
- Save disk morph animation (pill → floating disk in explore mode)
- Topbar dissolve (production map embedded in app_shell; topbar belongs to shell)
- Depth slider overlay (requires adapter support for opacity parameter)
