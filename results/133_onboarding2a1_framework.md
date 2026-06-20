# ONBOARDING-2A1: Walkthrough Framework

**Date:** 2026-06-20
**Scope:** `map_CURRENT.html`, `scripts/smoke_onboarding_walkthrough_framework.py`
**Plan:** `results/132_onboarding2a_map_walkthrough_execution_plan.md`

---

## Summary

Peep-hole overlay walkthrough framework implemented in `map_CURRENT.html`.
Amended canonical step sequence (Location Search removed; Profile Selector added as Step 1).

---

## Amended step sequence

| # | Step | Selector | Status |
|---|------|----------|--------|
| 1 | **Profile selector** | `#chartProfile` | Wired |
| 2 | **Genie** | `.condition-block` | Wired |
| 3 | Current-location popup | `#map` | Stub (graceful skip) |
| 4 | Mute / Solo / Not | `[data-role="ghost-tools"]` | Stub |
| 5 | Pin | `[data-role="pin-control"]` | Stub |
| 6 | History | `[data-role="history-controls"]` | Stub |
| 7 | Save Search | `#saveInvestigationBtn` | Wired (id present) |
| 8 | Map Notes *(optional)* | `[data-role="map-notes"]` | Stub/optional |

**Removed:** Location Search (universal map pattern; no onboarding value).

---

## What was built

### CSS (`map_CURRENT.html`)

- `#rm-walkthrough` — fixed-position overlay container, hidden by default
- `#rm-walkthrough.rm-wt-active` — shows overlay
- SVG mask for peep-hole backdrop (semi-transparent outside spotlight)
- `#rm-walkthrough-card` — instruction card, pointer-events: all; position: absolute
- `.rm-wt-step-label`, `.rm-wt-instruction`, `.rm-wt-actions`, `.rm-wt-skip`, `.rm-wt-next`

### DOM

```html
<div id="rm-walkthrough" …>
  <svg id="rm-walkthrough-mask" …>
    <defs><mask id="rm-wt-mask">…<rect id="rm-wt-spotlight-rect"/></mask></defs>
    <rect … mask="url(#rm-wt-mask)"/>
  </svg>
  <div id="rm-walkthrough-card">
    <div id="rm-wt-step-label"/>
    <p id="rm-wt-instruction"/>
    <div class="rm-wt-actions">
      <button id="rm-wt-dismiss">Dismiss</button>
      <button id="rm-wt-next">Next</button>
    </div>
  </div>
</div>
```

### JS controller

- `STEPS` array: 8 entries; `optional: true` on Map Notes
- `shouldSuppress()`: checks `rm_map_walkthrough_dismissed`, `rm_map_walkthrough_completed`, and `handoff=app_shell`; does **not** check `skipOnboarding` (new walkthrough has independent gating)
- `positionSpotlight(el)`: sets SVG `<rect>` bounds from `getBoundingClientRect()` + 12 px padding
- `positionCard(spotBounds)`: places card below/above/right/left of spotlight, clamped to viewport
- `showStep(idx)`: resolves target; skips with console.warn if required target absent; updates card copy
- `finishWalkthrough()` / `dismissWalkthrough()`: set respective keys; hide overlay
- `startWalkthrough()`: auto-starts 800 ms after `window.load`
- `window.rmWalkthroughClear()` / `window.rmWalkthroughReplay()`: exposed for Help/About replay

### Storage keys

| Key | Set when |
|-----|---------|
| `rm_map_walkthrough_dismissed` | User clicks Dismiss at any step |
| `rm_map_walkthrough_completed` | User clicks Finish on last step |

---

## Smoke (8 checks, all PASS)

```
PASS: ow_trigger_on_first_map
PASS: ow_no_trigger_if_dismissed
PASS: ow_step1_label
PASS: ow_next_advances
PASS: ow_dismiss_hides
PASS: ow_dismiss_sets_key
PASS: ow_replay_clears_state
PASS: ow_no_console_errors
PASS: smoke_onboarding_walkthrough_framework
```

---

## Out of scope (this slice)

- Steps 3–6 data-role selectors (depend on map chrome implementation)
- Mobile adaptation (ONBOARDING-2B)
- Replay trigger wired into Help/About surface (app_shell.html)
- Per-account state (ONBOARDING-7)
