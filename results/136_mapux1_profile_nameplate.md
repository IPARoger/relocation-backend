# MAP-UX-1: Production Map Profile Nameplate

**Date:** 2026-06-20
**Slice:** MAP-UX-1
**Status:** Complete

---

## Goal

Migrate the profile nameplate/caret concept from `map_SANDBOX_genie_v7.html` into
`map_CURRENT.html`, keeping `map_CURRENT.html` as the single production file with
full auth, real overlays, and backend wiring intact.

---

## What was implemented

### 1. Profile nameplate DOM

A new overlay element `#rm-map-nameplate` was injected inside `#map`, positioned
`top: 12px; left: 12px` (absolute, above the Leaflet canvas):

```html
<div id="rm-map-nameplate"
     data-role="map-profile-selector"
     class="rm-np-loading"
     title="Active profile">
  <div class="rm-np-name-row">
    <span class="rm-np-name" id="rm-np-name">Loading…</span>
    <button type="button" class="rm-np-caret" id="rm-np-caret"
            title="Switch profile — opens profile selector in side panel">▾</button>
  </div>
  <div class="rm-np-meta" id="rm-np-meta"></div>
</div>
```

- `data-role="map-profile-selector"` — stable onboarding target.
- Name row: profile display name + caret button.
- Meta row: birth date and birth place when available via `dataset.profile`;
  hidden for Supabase-only profiles that carry no birth data.
- `.rm-np-loading` fades opacity while profiles are loading.

### 2. CSS

Conservative styling: white-frosted card, `border-radius: 10px`, subtle
box-shadow, `backdrop-filter: blur(4px)`. No sandbox chrome.

### 3. JavaScript controller

`initNameplate()` IIFE:

- `renderNameplate()` reads `#chartProfile.selectedOptions[0]`, strips `[library]`
  prefix, parses `dataset.profile` for birth date/place when present.
- Listens to `document.change` for `#chartProfile` changes.
- Awaits `window.__rmChartProfilesReady` so nameplate populates at load time.
- `openProfileSelector()` — caret click scrolls panel to `#chartProfile`, focuses
  it, and dispatches `mousedown` to open the native dropdown.

### 4. Walkthrough step 1 selector updated

Step 1 selector changed from `#chartProfile` (panel, behind overlay mask) to
`[data-role="map-profile-selector"]` (the new visible nameplate element).

### 5. Map smoke hardened

`scripts/smoke_map_current.py` injects `rm_map_walkthrough_dismissed=1` into
localStorage at auth init so the walkthrough overlay does not block map-level tests.

---

## Files changed

| File | Change |
|------|--------|
| `map_CURRENT.html` | Added nameplate CSS, DOM, JS; updated walkthrough step 1 selector |
| `scripts/smoke_map_current.py` | Suppress walkthrough via localStorage during smoke |

---

## Validation

| Smoke | Result |
|-------|--------|
| `smoke_map_current.py` | PASS |
| `smoke_onboarding_walkthrough_framework.py` | PASS (all 9 checks) |

---

## Non-goals (deferred)

- Ghost tools (Mute/Solo/Not)
- History controls, Pin, centered map search, Save Search pill
- Explore-mode ghost nameplate effect
- Full sandbox chrome import
