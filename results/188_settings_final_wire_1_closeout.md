# SETTINGS-FINAL-WIRE-1 Closeout

**Date:** 2026-06-21  
**Type:** Implementation closeout  
**Scope:** Honest astrology Settings controls, restore defaults, consumer rehydration before Quick Share

---

## Summary

Remaining misleading astrology Settings controls were wired honestly or disabled with clear "coming soon" copy. **Restore Default Astrology Settings** was added. Settings save/restore now rehydrates all chart consumers and attempts map Genie selector sync.

**Note:** `results/187_settings_final_wiring_audit.md` was not present in the workspace at implementation time; this closeout is grounded in `results/176_settings_source_1_closeout.md`, `results/158_settings_reality_audit_3_final.md`, and live code inspection.

---

## Files changed

| File | Change |
|------|--------|
| `app_shell.html` | Honesty copy; enable out-of-sign; quarantine subsequent-house toggle; restore defaults; `rehydrateSettingsConsumers()` |
| `scripts/smoke_comparison_sets.py` | Six `static_final_wire_*` checks |
| `results/188_settings_final_wire_1_closeout.md` | This document |

---

## Active settings — consumer truth (post slice)

| Setting | Consumer(s) | Status |
|---------|-------------|--------|
| `visible_planets` / `visible_bodies` | `/relocated-chart` compute; PIH; wheel; comparison; map Genie body selectors | **Live** |
| `visible_major_aspects` / `visible_minor_aspects` / `visible_minor_aspects_list` | Server P2P + A2A majors; wheel spokes; map Genie aspect options | **Live** |
| `major_aspect_orbs` / `minor_aspect_orbs` | Server P2P orb limits; wheel spoke inclusion | **Live** |
| `aspect_to_angle_orbs` | Server A2A orb limits; map search `max_orb` metadata | **Live** (map line geometry unchanged) |
| `display_aspects_to_angles` | AIS; comparison angle rows; A2A tables; map Genie `overlayAngle` | **Live** |
| `house_proximity_orb_degrees` | `/relocated-chart` `near_cusp` on PIH / canonical planets | **Live** |
| `out_of_sign_aspects` | Server P2P + A2A sign-gate | **Live** (checkbox re-enabled) |
| `default_chart_record_id` | Account default profile (My Data subpage) | **Live** |

---

## Disabled / honest future settings

| Control | UI treatment |
|---------|----------------|
| North / South Node | Disabled checkboxes + coming soon |
| Part of Fortune / advanced points | Disabled in "More points" |
| House system | Disabled select — Placidus only |
| Zodiac mode | Disabled read-only — Tropical only |
| Direction-aware subsequent house | Stub row with coming soon badge (misleading checkbox removed) |
| Glyph family / wheel style / themes / map appearance | Stub rows + coming soon |
| Exports / notifications / billing | Stubs or disabled |
| Dignities ontology presets | Redirect to PIH footer toggle |
| Sidereal / alternate house systems / nodes engine / AI / export wizard | Not implemented (out of scope) |

---

## Restore Default Astrology Settings

- Button on **Settings → Astrology** save bar
- Confirms before write
- Resets astrology keys from `settings/astrology_settings_defaults.json` via `RMSettings.DEFAULTS`
- Does **not** change `default_chart_record_id` (owned on My Data)

---

## Rehydration after save / restore

`applyAccountSettingsPatch()` → `mirrorUserSettingsPatch()` (updates `storeRaw` + `window.SupabaseStore`) → `render()` → `rehydrateSettingsConsumers()`:

| Consumer | Behavior |
|----------|----------|
| Screen 4 chart | Clears `_screen4ChartCache`; re-fetches on chart route |
| Wheel / PIH / AIS / A2A | Re-rendered from fresh `/relocated-chart` payload |
| Comparison columns | Clears `_comparisonColsCache`; re-fetches on compare route |
| AIS / A2A workbook sections | Refreshed after comparison hydrate |
| Map Genie selectors | `window.__rmSyncGenieSelectors()` when map script loaded (separate tab may need revisit) |

---

## Copy fixes (misleading → honest)

| Area | Before | After |
|------|--------|-------|
| Chart display orbs | "when renderers are live" | Live on wheel + server P2P |
| A2A display angles | "tables ship in a later slice" | Lists AIS, comparison, A2A, map Genie |
| Subsequent house | Interactive "Treat late sign…" checkbox | Near-cusp orb only; direction logic coming soon |
| Out-of-sign | Disabled "not active yet" | Enabled — live on server P2P/A2A |
| A2A orbs | Implied geometry change | Metadata / row filter; map lines exact crossing |

---

## Validation

| Check | Result |
|-------|--------|
| Static smoke (`static_*` + `static_final_wire_*`) | **33/33 PASS** |
| Playwright full smoke | Not run (pre-existing AIS workbook flake) |

---

## Remaining honest future work (post Quick Share)

1. **Direction-aware `subsequent_house_policy`** — requires motion-aware house-edge doctrine (`results/130`)
2. **Map overlay orb → visible band geometry** — `max_orb` is metadata today
3. **Cross-tab map live sync** — Genie sync on map load; shell save calls sync when map script present
4. **Glyph selector, sidereal, alternate house systems, nodes, export wizard, AI** — explicitly deferred

---

*SETTINGS-FINAL-WIRE-1 complete.*
