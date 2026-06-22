# 234 — Settings Live Wiring Audit

**Date:** 2026-06-23
**Mode:** Audit only — no implementation
**Task:** SETTINGS-LIVE-WIRING-AUDIT-1-COST-CAPPED
**Read budget used:** app_shell.html (targeted sections), results/158_settings_reality_audit_3_final.md (summary + blockers), results/90_settings_ux_prototype_alignment_audit.md (summary), results/230_information_hierarchy_study_1.md (Diffs recommendations), docs/roadmaps/active/WEB2_COMPLETION__ACTIVE__2026-06-18.md (Settings items)
**External file noted (stop rule):** supabase_store_bridge.js (window.RMSettings source — not read per stop rule)

---

## 1. What Settings controls are live

All controls below are wired end-to-end: save handler persists to DB → `rehydrateSettingsConsumers()` clears cache and re-fetches → consumer reads `_settingsEff()` at render time.

| Setting key | UI element IDs | Consumer / effect |
|---|---|---|
| `default_chart_record_id` | `rm-settings-default-cr` | Map/chart default profile selection |
| `visible_planets` | `rm-settings-planet-{id}` × 10 | `getVisibleBodyNamesSet()` → PIH rows on all pages |
| `visible_bodies` (chiron) | `rm-settings-body-chiron` | Same — chiron row show/hide |
| `visible_minor_aspects` | `rm-settings-minor-aspects` | Genie overlay minor optgroup visibility |
| `visible_minor_aspects_list` | `rm-settings-minasp-{id}` × 8 | Genie per-minor aspect option |
| `visible_major_aspects` | `rm-settings-majasp-{id}` × 5 | Genie per-major aspect option |
| `house_proximity_orb_degrees` | `rm-settings-house-proximity-orb` | `/relocated-chart` near_cusp flag on Comparison table + popup; **not wired to Profile** (see §5) |
| `aspect_to_angle_orbs` | `rm-settings-a2aorb-{id}` × 5 | Stored + sent to map overlay as metadata; does not change line geometry |
| `display_aspects_to_angles` | `rm-settings-a2d-{asc/mc/dsc/ic}` × 4 | `getA2aDisplayAngles()` → AIS angle rows, A2A rows on all pages, map angle selector |

**Propagation note:** `rehydrateSettingsConsumers()` conditionally re-fetches based on `navContext.route`. Route `"chart"` → `hydrateRelocatedChart()`. Route `"compare"` → `hydrateComparisonColumns()` + AIS/A2A workbook refresh. Route `"chart-record"` (Profile) → **nothing** (see §5 gap #1).

---

## 2. What Settings controls are placeholders

Rendered via `settingsStubRow()` or `settingsSoonBadge()`. No save handler wired; no consumer. Disclosed to the user at point of render.

| Control | State | Disclosure |
|---|---|---|
| House system select | `disabled`, Placidus only | "Placidus is the active house system" |
| Zodiac mode input | `disabled`, Tropical only | "Tropical zodiac is active" |
| Out-of-sign aspects checkbox | `disabled`, title="Coming soon" | "Stored for future aspect tables and is not active yet" |
| North / South Node checkboxes | `disabled`, unchecked | Engine does not calculate Nodes |
| Wheel style | stub row | Appearance — not wired |
| Chart surface | stub row | Appearance — not wired |
| Glyphs | stub row | Appearance — not wired |
| Aspect bands | stub row | Appearance — not wired |
| Themes | stub row | Appearance — not wired |
| Exact aspect lines (map) | stub row | Map — not wired |
| Exclusion style (map) | stub row | Map — not wired |
| City labels (map) | stub row | Map — not wired |
| Share / export / PNG presets | disabled buttons | Exports — not wired |
| Road trip alert | stub row | Notifications — not wired |
| Airplane alert | stub row | Notifications — not wired |
| Location alert | stub row | Notifications — not wired |
| Language | stub row | Regional — not wired |
| Date / time format | stub row | Regional — not wired |
| Dignities ontology | description text only | Redirects to per-table footer toggle; no Settings-level storage |

Approximately 47 stub rows total across the Settings panel.

---

## 3. What is stored but not consumed

These settings are persisted to the database on save but have no live consumer in any chart or table surface as of this audit.

- **`major_aspect_orbs`** (`rm-settings-majorb-{id}` × 5) — saved; no chart table reads this value; Genie map overlay does not use per-major orbs.
- **`minor_aspect_orbs`** (`rm-settings-minorb-{id}` × 8) — saved; same gap as major orbs.
- **`out_of_sign_aspects`** — saved per the disabled checkbox; no calculation or filter effect anywhere.
- **`aspect_to_angle_orbs`** — saved and forwarded to map overlay as metadata, but map line geometry is not recalculated from it.
- **`subsequent_house_policy`** checkbox — interactive (not `disabled`), saves value; direction-aware house assignment is not calculated. The orb threshold portion is live; the policy-assignment portion is not (see §5 gap #4).

---

## 4. What is consumed but not editable

These values are read from `_settingsEff()` at render time but have no corresponding Settings UI control that takes effect.

- **House system** — engine always uses Placidus; no UI toggle that takes effect. Post-Web2 roadmap item.
- **Zodiac mode** — engine always uses Tropical; no UI toggle that takes effect.
- **Node visibility** — engine does not compute Nodes; checkboxes exist but are disabled.

---

## 5. What silently fails or has no validation

| # | Gap | Severity | Detail |
|---|---|---|---|
| 1 | **Profile page not in `rehydrateSettingsConsumers`** | High | Route `"chart-record"` is absent from the rehydrate function. Saving settings while on the Profile page produces no re-render. User must navigate away and back to see any effect. |
| 2 | **`house_proximity_orb_degrees` missing from Profile hydration** | High | `hydrateProfileNatalFacts()` / `fetchCanonicalRelocatedChart()` for the natal path does not pass `house_proximity_orb_degrees`. The Comparison page passes it; the Profile page does not. Near-cusp flags are therefore inconsistent across pages. |
| 3 | **Major / minor aspect toggles have no chart table consumer** | Medium | `visible_major_aspects` and `visible_minor_aspects_list` only affect the Genie map overlay selector. PIH, AIS, and A2A tables are unaffected regardless of what the user toggles. |
| 4 | **Subsequent house checkbox creates false expectation** | Medium | The checkbox is interactive and saves, but direction-aware house policy reassignment is not implemented. Users who toggle it observe no change in house assignments. |
| 5 | **A2A Comparison table is a stub** | Medium | The A2A workspace section on the Comparison page is not yet live. `refreshA2aWorkbookSection()` is called in `rehydrateSettingsConsumers` but the table has no rendered rows. |
| 6 | **Map settings sync is load-time only** | Low | Genie selector sync runs on map load (`map_CURRENT.html`). Settings saved after the map is open do not propagate live; user must reload the map tab. |
| 7 | **`aspect_to_angle_orbs` stored but geometry unchanged** | Low | Saved and sent to map overlay as metadata. Map line geometry is rendered from a pre-computed value; orb changes require a map reload to take effect (if wired at all). |

---

## 6. Smallest implementation slices

### SET-1: Display controls (Rx, A/S, Late-in-house)

**Scope:** Add retrograde (Rx) markers on planet name cells, applying/separating (A/S) aspect coloring, and late-in-house / early-with-retro `?` flag near house number. Apply to Profile, Relocated Chart, and Comparison pages.

**Expected files:**
- `app_shell.html` — add render logic in PIH/AIS/A2A row builders; add Settings UI toggles for each display flag
- `supabase_store_bridge.js` — add keys to effective settings schema

**Validation command:**
```
open validation/mockups/beta/relocated_standard.html
# Verify Rx suffix appears on retrograde planets in PIH, AIS rows
# Verify A/S coloring renders on aspect cells
# Verify ? marker appears for late-in-house planets
```

**Rollback:** Revert `app_shell.html` to prior commit; the store bridge key additions are additive and safe to leave.

---

### SET-2: Astrology / orb controls

**Scope:** Wire `major_aspect_orbs` and `minor_aspect_orbs` to PIH, AIS, and A2A table renderers so aspect rows reflect user-configured orbs (not hardcoded defaults). Wire `visible_major_aspects` / `visible_minor_aspects_list` toggles to chart tables in addition to the Genie overlay.

**Expected files:**
- `app_shell.html` — pass orb values from `_settingsEff()` into aspect-row filter/renderer; add major/minor visibility filter to chart table builders

**Validation command:**
```
# In Settings, tighten a major aspect orb to 0° → verify wide-orb aspects disappear from PIH rows on Relocated Chart
# Toggle off one minor aspect type → verify row disappears from AIS
```

**Rollback:** Revert `app_shell.html`; no schema changes required.

---

### SET-3: Dignities / Diffs defaults

**Scope:** Wire dignities PIH cell tinting toggle to Profile and Relocated Chart pages (already partially wired per-page on Comparison). Apply information hierarchy doctrine for Diffs duplicate demotion: replace `.rm-cmp-diff-duplicate { opacity: 0.48; color: #64748b }` with warm-ink shift + weight demotion only (`color-mix(in srgb, var(--ink) 72%, var(--paper))` at opacity 1, `font-weight: 400`).

**Expected files:**
- `app_shell.html` — extend dignities tinting logic to Profile + Relocated Chart page hydrators
- CSS (inline or linked stylesheet) — replace `.rm-cmp-diff-duplicate` rule

**Validation command:**
```
# Enable dignities tinting in Settings → verify tinted cells appear on Profile and Relocated Chart, not just Comparison
# Inspect .rm-cmp-diff-duplicate elements → confirm no opacity < 0.85, no #64748b color
```

**Rollback:** Revert CSS rule; revert tinting wiring in hydrators.

---

### SET-4: Location / current-place controls

**Scope:** Wire `house_proximity_orb_degrees` into `hydrateProfileNatalFacts()` / `fetchCanonicalRelocatedChart()` natal path so near-cusp flags are consistent with the Comparison page. Add `"chart-record"` to `rehydrateSettingsConsumers()` so Profile re-renders after a settings save.

**Expected files:**
- `app_shell.html` — two changes: (a) pass `house_proximity_orb_degrees` to Profile natal fetch, (b) add `chart-record` branch to `rehydrateSettingsConsumers()`

**Validation command:**
```
# Set house proximity orb to 1° in Settings → navigate to Profile → verify near-cusp flag appears/disappears on expected planets
# Save settings while on Profile page → verify page reflects change without requiring navigation
```

**Rollback:** Revert `app_shell.html`.

---

### SET-5: Settings propagation smoke

**Scope:** Regression check for the full `rehydrateSettingsConsumers()` call path after SET-1 through SET-4 land. Confirm no stale-cache race between `_screen4ChartCache` / `_comparisonColsCache` clears and any new Profile cache introduced in SET-4.

**Expected files:**
- No new files; review `rehydrateSettingsConsumers()` and any cache variables introduced in SET-4

**Validation command:**
```
# Save settings rapidly while toggling between routes → confirm no stale renders
# Check browser console for uncaught errors in hydrate calls after cache clear
```

**Rollback:** N/A (audit/smoke only).

---

## 7. Open blockers before Web2 beta

Ordered by impact on user-visible correctness:

1. **Profile page not rehydrated on settings save** (§5 gap #1) — any settings change while on Profile is silently dropped until the user navigates. Blocks all of §6 SET-4.

2. **`house_proximity_orb_degrees` inconsistent between Profile and Comparison** (§5 gap #2) — same setting produces different near-cusp results on different pages. High user-confusion risk.

3. **Major/minor aspect toggles not wired to chart tables** (§5 gap #3) — users can toggle aspects off in Settings and see them reappear in PIH/AIS/A2A rows. Contradicts stated behavior.

4. **Subsequent house checkbox interactive but non-functional** (§5 gap #4) — should be `disabled` with a disclosure (same pattern as house system / zodiac mode) until the policy-assignment calculation is implemented.

5. **A2A Comparison table stub** (§5 gap #5) — `display_aspects_to_angles` and `aspect_to_angle_orbs` controls are live but the primary consumer table does not render. Controls have no visible effect on the Comparison page.

6. **`major_aspect_orbs` / `minor_aspect_orbs` stored but unconsumed** (§3) — schema and save handler exist; calculation layer does not read them. Deferred unless aspect-table work (SET-2) lands pre-beta.

7. **Map settings sync is load-time only** (§5 gap #6) — acceptable for Web2 beta given the map is a separate page, but needs a disclosure or map-reload prompt when settings are saved while the map is open.
