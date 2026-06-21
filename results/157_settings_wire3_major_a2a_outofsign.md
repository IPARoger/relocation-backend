# SETTINGS-WIRE-3 Closeout: Major Aspects, A2A Angle Consumers, Out-of-Sign Disclosure

**Date:** 2026-06-21  
**Commit:** SETTINGS-WIRE-3: wire major aspects and A2A angle displays  
**Status:** COMPLETE

---

## Summary

Finished the remaining misleading astrology settings where wiring was possible without new engine logic. Major/minor aspect toggles now control the Genie overlay selector. A2A display angles now filter live angle surfaces. Out-of-sign is honestly disabled/disclosed.

---

## PART 1 — Major / Minor Aspect Toggles (WIRED)

### What changed (`map_CURRENT.html`)

- Added `syncGenieAspectSelectorsToSettings()` with major, minor, and composite (`hard` / `soft` / `any`) rules.
- Composite sets require **all** constituent majors enabled (conservative behavior).
- Per-minor aspect toggles (`visible_minor_aspects_list`) now hide individual minor `<option>` elements; master toggle still controls optgroup visibility.
- Disabled options are hidden + disabled; selection resets to first available valid aspect.
- Unified `syncGenieSelectorsToSettings()` calls body + aspect + angle sync on load.
- Exported: `__rmSyncGenieAspectSelectors`, `__rmSyncGenieAngleSelectors`, `__rmSyncGenieSelectors`.

### Surfaces affected

- Genie `overlayAspect` selector (map A2A overlay search path)

### Not in scope (unchanged)

- Comparison / PIH do not show aspects — toggles do not claim to affect those tables.

---

## PART 2 — A2A Display Angles (WIRED)

### Settings copy updated (`app_shell.html`)

> Choose which relocated angles appear in map aspect searches and angle lists. ASC and MC are shown by default. Full aspect-to-angle tables ship in a later slice.

### Live consumers

| Surface | Behavior |
|---------|----------|
| Map `overlayAngle` selector | Hides disabled angles; resets selection |
| Screen 4 relocated chart | Hides disabled angle rows (`getA2aDisplayAngles()`) |
| Map popup relocated chart | Shows only enabled angles in summary grid |
| Comparison PIH angle rows | Hides disabled ASC/MC/DSC/IC rows at render time |
| Comparison A2A stub | Honest copy — no fake rows |

### Helper

- `getA2aDisplayAngles()` in `app_shell.html` (defaults: ASC/MC on, DSC/IC off)
- `getA2aDisplayAngles()` in `map_CURRENT.html` for popup + overlay sync
- `window.__rmGetA2aDisplayAngles` exported for smoke verification

### Workspace angle tabs

- `active_angle_tab` remains session UI (bookmark filter on visible rows).
- Settings preference is applied at **render** time, not conflated with workspace tabs.

---

## PART 3 — Out-of-Sign Aspects (DISCLOSED / DISABLED)

- Checkbox disabled with `title="Coming soon"`.
- Meta: *"Out-of-sign filtering is stored for future aspect tables and is not active yet."*
- Save handler skips patching `out_of_sign_aspects` while control is disabled.
- No engine sign-gate added (per scoping audit — would be new calculation logic).

---

## PART 4 — Applying / Separating / Exact (FUTURE)

**Not implemented.** Doctrine note for future A2A / aspect table renderer:

| State | Color | Rules |
|-------|-------|-------|
| Applying | Blue | Layer-1 factual display |
| Separating | Red | No gradients |
| Exact | Green | No scoring or strength ranking |

Requires planet speed / separation direction in engine plus a live aspect table renderer.

---

## Smoke Results

| Suite | Result | Notes |
|-------|--------|-------|
| `smoke_comparison_sets.py` | **PASS** (21 checks) | Includes `fe_a2a_display_defaults` |
| `smoke_map_current.py` | **INFRA FAIL** (pre-existing) | `trigger_find_regions_and_wait` click timeout; WIRE-3 sync verified separately |
| `smoke_settings_navigation.py` | **AUTH INFRA FAIL** | Expired magic link (`Email link is invalid or has expired`) |
| `smoke_settings_account.py` | **AUTH INFRA FAIL** | Playwright settings landing timeout |

### WIRE-3 isolated verification (map page)

Manual Playwright snippet against `map_CURRENT.html` confirmed:

- `conjunction` visible, `square` hidden when `visible_major_aspects: ['conjunction']`
- `quincunx` visible, `novile` hidden when list is `['quincunx']`
- ASC/MC visible, DSC/IC hidden by default
- Enabling DSC in settings makes DSC option visible after re-sync

### New assertions added

- `smoke_map_current.py`: `wire3_major_aspect_hidden`, `wire3_minor_aspect_hidden`, `wire3_a2a_angle_defaults`, `wire3_dsc_enabled_visible`
- `smoke_settings_navigation.py`: `fe_oos_disabled`, `fe_oos_disclosed`
- `smoke_settings_account.py`: `be_major_asp_persists`
- `smoke_comparison_sets.py`: `fe_a2a_display_defaults`

---

## Known Limitations

1. **Chart display orbs** — still annotated as future chart-wheel consumers (WIRE-2).
2. **A2A comparison table** — stub only; no aspect rows fabricated.
3. **Out-of-sign** — stored preference only until sign-gate engine ships.
4. **Applying/Separating/Exact** — no settings UI; future work.
5. **Settings save on map page** — map is a separate document; Genie sync runs on map load (not live cross-page after settings save without revisit).

---

## Files Modified

| File | Change |
|------|--------|
| `map_CURRENT.html` | Aspect/angle sync; popup angle filtering |
| `app_shell.html` | `getA2aDisplayAngles`, Screen 4 + comparison angle rows, settings copy, OOS disable, A2A stub |
| `scripts/smoke_map_current.py` | WIRE-3 Genie sync assertions |
| `scripts/smoke_settings_navigation.py` | OOS disclosure assertions |
| `scripts/smoke_settings_account.py` | Major aspect persistence assertion |
| `scripts/smoke_comparison_sets.py` | A2A display defaults assertion |
