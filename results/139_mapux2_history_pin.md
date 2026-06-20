# MAP-UX-2: Production Map History and Pin Controls

**Date:** 2026-06-20
**Slice:** MAP-UX-2
**Status:** Complete

---

## Goal

Add stable History (back/forward) and Pin controls to `map_CURRENT.html`, matching the
intended UX from `map_SANDBOX_genie_v7.html`, with real wiring to existing production
behavior where it exists and documented placeholder wiring where it does not.

---

## What was implemented

### 1. History & Pin control strip DOM

A new `#rm-map-controls` element was injected inside `#map`, positioned
`top: 90px; left: 12px` (below the nameplate from MAP-UX-1):

```html
<div id="rm-map-controls"
     data-role="history-controls"
     aria-label="Map search history and pin">
  <button id="rm-ctrl-back"  data-role="map-history-back"    disabled>‹</button>
  <button id="rm-ctrl-fwd"   data-role="map-history-forward" disabled>›</button>
  <button id="rm-ctrl-pin"   data-role="map-pin">⟨pin SVG⟩</button>
</div>
```

All three buttons carry the required `data-role` attributes for onboarding targeting.

### 2. CSS

Single-pill frosted card — styled to match the MAP-UX-1 nameplate:
- `background: rgba(251,253,255,0.93)`, `border: 1px solid #cfdde6`, `border-radius: 10px`,
  `backdrop-filter: blur(4px)`, matching shadow.
- `.rm-ctrl-btn`: inline flex buttons separated by a right border.
- `.rm-ctrl-btn:disabled`: `opacity: 0.35` so back/forward read as inactive initially.
- `.rm-ctrl-pinned`: blue highlight when pin is active.

### 3. JavaScript controller — History stack

`initMapControls()` IIFE:

**History stack** (`_stack`, `_cursor`):
- 20-entry circular stack.
- `pushState(plan)` captures the `plan` argument each time `executeSearchPlan` runs.
- `syncButtons()` enables/disables back/forward and updates tooltips.
- Back button: `replayAt(_cursor - 1)`. Forward button: `replayAt(_cursor + 1)`.
- `replayAt(idx)` calls `window.executeSearchPlan(entry.plan, { source: 'history_replay' })`
  and guards against re-pushing the replayed plan via `_replaying` flag.

**Wiring to `executeSearchPlan`:**

```javascript
var _origExecuteSearchPlan = window.executeSearchPlan;
if (typeof _origExecuteSearchPlan === 'function') {
    window.executeSearchPlan = async function(plan, meta) {
        var result = await _origExecuteSearchPlan.call(this, plan, meta);
        if (plan && (meta || {}).source !== 'history_replay') pushState(plan);
        return result;
    };
}
```

`executeSearchPlan` is the existing production entry point in `genie_map_engine_adapter.js`.
The wrapper intercepts each successful search and captures the plan snapshot.

**Future integration path** (documented inline):
> When `genie_map_engine_adapter.js` gains its own plan-completion event/promise,
> listen to that instead of wrapping here. The adapter could expose
> `window.rmGenieAdapter.on('searchComplete', fn)`.

### 4. JavaScript controller — Pin

**Pin** (`rm_map_pinned_plan` in `sessionStorage`):
- Clicking pin stores the current plan snapshot; button turns blue (`rm-ctrl-pinned`).
- Clicking again removes the key and resets the button.
- State restores across page reload within the session.
- `window.rmGetPinnedPlan()` exposed for the future comparison workspace.

**Future integration path** (documented inline):
> When the comparison workspace ships (COMPARE-1), the pinned plan is available via
> `window.rmGetPinnedPlan()`. No DOM coupling required.

### 5. Walkthrough step selectors updated

Two step selectors were updated to match the new DOM:

| Step | Old selector | New selector |
|------|-------------|-------------|
| Pin (step 5) | `[data-role="pin-control"]` | `[data-role="map-pin"]` |
| History (step 6) | `[data-role="history-controls"]` | (unchanged, container added) |

### 6. Walkthrough smoke hardened

`scripts/smoke_onboarding_walkthrough_framework.py` sections 1 and 3 previously used
a fixed `wait_for_timeout(1800ms)` after `domcontentloaded`. With more JS on the page,
the `load` event (which fires `startWalkthrough`) can land later than 1800ms in a fresh
browser context. Both sections now use `page.wait_for_function` to wait for `rm-wt-active`
class before reading state — making the checks robust regardless of page load speed.

---

## Files changed

| File | Change |
|------|--------|
| `map_CURRENT.html` | Added controls CSS, DOM, JS controller; updated walkthrough step 5 selector |
| `scripts/smoke_onboarding_walkthrough_framework.py` | Replaced fixed wait with wait_for_function in sections 1 and 3 |

## Files NOT changed

- `genie_map_engine_adapter.js` — wired from the outside; untouched
- `app_shell.html` — no handoff changes
- Rendering engine, overlays, Genie — untouched

---

## Behavior summary

| Control | State at page load | After first search | After pin |
|---------|-------------------|-------------------|-----------|
| Back | Disabled (no history) | Enabled (1 entry) | Unchanged |
| Forward | Disabled | Disabled (at head) | Unchanged |
| Pin | Unpinned | Unpinned | Blue; plan stored in sessionStorage |

---

## Validation

| Smoke | Result |
|-------|--------|
| `smoke_map_current.py` | PASS (overall_pass: true) |
| `smoke_onboarding_walkthrough_framework.py` | PASS (all 8 checks) |

---

## Non-goals (deferred)

- Ghost tools (Mute/Solo/Not)
- Centered map search
- Save Search pill
- Comparison workspace pin integration (COMPARE-1)
- Plan-completion event on `genie_map_engine_adapter.js` (future adapter work)
