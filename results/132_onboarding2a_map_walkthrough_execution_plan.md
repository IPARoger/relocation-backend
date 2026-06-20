# ONBOARDING-2A: Map Walkthrough Execution Plan

**Date:** 2026-06-20
**Type:** Implementation plan only — no implementation authorized by this document
**Doctrine:** `results/124_onboarding_map_walkthrough_doctrine_correction.md`
**Supersedes:** ONBOARDING-3/4/5 walkthrough scope in `results/122_onboarding1_audit_implementation_plan.md`

---

## Purpose

Convert the map walkthrough doctrine into concrete implementation slices. This is the execution plan for **peep-hole overlay onboarding on the live map** — not an app shell tour, not a modal.

**Goal:** teach the map, not the application.

---

## 1. Overlay Sequence

Eight canonical overlays (7 required + 1 optional). Each overlay is a **peep-hole spotlight** on a live map target with a single short instruction line and Next / Dismiss.

| # | Step | Target | Instruction copy (draft) |
|---|------|--------|--------------------------|
| 1 | **Genie** | Genie panel / variable builder | "Add a chart condition — Genie builds your search." |
| 2 | **Current location popup** | Map canvas (right-click target) | "Right-click anywhere to open the location popup and see chart facts here." |
| 3 | **Mute / Solo / Not** | Ghost tool buttons | "Mute, Solo, and Not refine which conditions are active without deleting them." |
| 4 | **Location search** | Search input on map | "Search for a city or coordinate to jump to a specific place." |
| 5 | **Pin** | Pin control | "Pin a location to hold it visible while you keep exploring." |
| 6 | **History** | Back/forward controls | "History lets you move through your search states." |
| 7 | **Save Search** | Save Search button | "Save this search to come back to it from Chart Record." |
| 8 | **Map Notes** *(optional)* | Map Notes entry point | "Map Notes attach a personal note to this search state." |

**Invariant:** Steps are shown in order. Skipping advances to the next; overlay 8 is omitted if scope is narrow.

---

## 2. Trigger Conditions

### Initial trigger (first run)

- Profile intake complete (`first_profile_intake.js` has written a profile to store).
- User arrives on `map_CURRENT.html` for the first time under this account context.
- A Genie session with **≥3 preloaded variables** is present (map must not be empty on arrival per doctrine).
- Neither dismiss nor completion key is set in storage (see §7).

### Suppression (do not show if any true)

- Dismiss key or completion key present.
- Deep-link navigation with existing handoff payload (treat as returning-user context).
- `skipOnboarding` flag set (future: per-account state).

### Replay trigger

- User opens Help / About and activates **Replay walkthrough**.
- Clears both storage keys and restarts from overlay 1.

---

## 3. Dismiss / Replay Behavior

| Trigger | Behavior |
|---------|---------|
| **× (Dismiss)** on any overlay | Hides all overlays; sets `rm_map_walkthrough_dismissed`. |
| **Skip all** (overlay 1 link) | Same as dismiss. |
| **Finish** on final overlay | Sets `rm_map_walkthrough_completed` (distinct from dismissed-mid). |
| **Map pan / zoom** outside spotlight | Does **not** dismiss — map stays interactive; overlay persists. |

### Replay

- Replay clears both keys via a single `clearWalkthroughState()` function.
- Navigates back to map if needed, then restarts from overlay 1.

---

## 4. Desktop Flow

1. Map loads; ≥3 Genie variables visible.
2. Overlay 1: spotlight on Genie panel; instruction card attached below or right (~280 px).
3. Spotlight area is **not** click-blocked — user can interact with Genie target live.
4. **Next** advances and repositions spotlight (animated or snap).
5. Overlays 2–6 follow same pattern: spotlight, one-line copy, Next / Dismiss.
6. Overlay 7 (Save Search): **Next** becomes **Finish** (or Next → overlay 8 if Map Notes included).
7. After Finish: overlay layer removed, completion key set, map fully interactive.

### Spotlight sizing

- Cutout: bounding rect of target + 12 px padding.
- Semi-transparent backdrop over remainder of viewport.
- Instruction card: fixed width, does not cover spotlight target.

---

## 5. Mobile Flow

**Phase: deferred.** Desktop map first (per doctrine).

When implemented as **ONBOARDING-2B**:

- Instruction card anchors to bottom of viewport.
- Long-press replaces right-click in overlay 2 copy.
- Same 7 (or 8) targets — no new steps added for mobile.
- Requires responsive spotlight positioning and touch-event handling.

---

## 6. Peep-Hole Targets

| Step | Selector (draft) | Presence guarantee |
|------|------------------|--------------------|
| 1 — Genie | `#genie-panel` or `[data-role="genie"]` | Present on map load with active Genie session |
| 2 — Location popup | Map canvas element | Always present |
| 3 — Mute/Solo/Not | `[data-role="ghost-tools"]` | Present when ≥1 variable active |
| 4 — Location search | `#map-location-search` | Always present |
| 5 — Pin | `[data-role="pin-control"]` | Present on map chrome |
| 6 — History | `[data-role="history-controls"]` | Present after first search |
| 7 — Save Search | `[data-role="save-search"]` | Present after first search |
| 8 — Map Notes | `[data-role="map-notes"]` | Optional: present if feature active |

### Fallback

If a target element is missing when an overlay is due: skip that step silently, advance to next, log a console warning (not error).

---

## 7. State Persistence

### v1 — localStorage (acceptable for initial release)

| Key | Value | Set when |
|-----|-------|---------|
| `rm_map_walkthrough_dismissed` | `"1"` | User hits × at any step |
| `rm_map_walkthrough_completed` | `"1"` | User reaches Finish on last overlay |

If either key is present, walkthrough does not auto-trigger. Replay removes both.

### v2 — per-account (deferred to ONBOARDING-7)

Persist `onboarding_map_walkthrough_completed` in account settings snapshot once `user_settings` schema supports it. Fall back to localStorage on auth failure. **Do not implement in 2A.**

---

## 8. Smoke Strategy

### New script: `scripts/smoke_onboarding_map_walkthrough.py`

Playwright; runs against port 8004 with a clean session (no walkthrough keys).

| ID | Check | Method |
|----|-------|--------|
| `ow_trigger_on_first_map` | Overlay 1 appears on first map load | Navigate; assert overlay 1 selector visible |
| `ow_no_trigger_if_dismissed` | No overlay when dismiss key set | Pre-set key; load; assert overlay absent |
| `ow_dismiss_mid_hides_all` | × removes overlay from DOM | Show overlay; click ×; assert container gone |
| `ow_dismiss_sets_key` | × writes correct localStorage key | Evaluate after dismiss |
| `ow_next_advances` | Next on step N shows N+1 | Click Next 3×; assert active step = 4 |
| `ow_finish_sets_completed` | Finish on last step sets completed key | Advance to last; click Finish; evaluate |
| `ow_replay_clears_state` | Replay removes both keys | Pre-set both; trigger replay; evaluate |
| `ow_no_console_errors` | No errors during sequence | Monitor console throughout |

**Pre-implementation baseline:** script exits with `SKIP` sentinel (not `FAIL`) when overlay DOM is absent so CI is not broken before the feature ships.

### Existing smoke updates (when overlay ships)

- `smoke_map_current.py`: assert overlay container element exists in DOM (even when suppressed).
- `smoke_settings_navigation.py`: assert Help surface contains replay trigger element.

---

## Implementation files (future)

| File | Role |
|------|------|
| `map_CURRENT.html` | Overlay DOM layer, spotlight CSS, step controller JS |
| `scripts/smoke_onboarding_map_walkthrough.py` | New smoke |
| `app_shell.html` | Replay trigger in Help/About; calls `clearWalkthroughState()` |

No backend changes required for v1.

---

## Out of scope

- Favorites, Comparisons, Profile management, Settings tour
- Mobile adaptation (ONBOARDING-2B)
- Per-account persistence (ONBOARDING-7)
- Night mode (not a product feature)
- Multi-slide app shell modal as primary onboarding

---

## Related slices

| Slice | Note |
|-------|------|
| ONBOARDING-2 (modal interaction fix) | Should ship first — avoid modal/overlay collision on first session |
| ONBOARDING-2B | Mobile adaptation of this plan |
| ONBOARDING-7 | Per-account persistence of walkthrough state |
