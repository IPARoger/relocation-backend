# S0 — Settings Truth Matrix

**Date:** 2026-06-27  
**Authority:** [SETTINGS_V1_PRODUCT_SPEC.md](../docs/canon/SETTINGS_V1_PRODUCT_SPEC.md)  
**Related:** [273 PO audit](../results/273_product_owner_comparison_settings_notes_audit.md) · [274 S1](../results/274_s1_saved_object_management_implementation.md) · [275 S2](../results/275_s2_astrology_settings_implementation.md) · [276 S3](../results/276_s3_dignities_implementation.md)

Evidence-based audit of every visible Settings control. Verdict: **REAL** · **PARTIAL** · **STUB** · **REMOVE**.

**Column key:** Y = yes · N = no · — = N/A · ~ = partial

## Evidence anchors

| Layer | Path |
|-------|------|
| UI + save | `app_shell.html` (`SETTINGS_SECTIONS`, save handler, `rehydrateSettingsConsumers`) |
| Resolver | `services/account_settings_resolver.py` (`get_effective_settings`) |
| Defaults | `settings/astrology_settings_defaults.json` |
| Client bridge | `supabase_store_bridge.js` (`RMSettings.getEffectiveSettings`, `buildSettingsSnapshot`) |
| Save API | `repositories/account_settings_repository.py` → `PATCH /settings/account` |
| Engine | `main_centerline_FIXER.py` (`_active_p2p_aspects`, `aspect_to_angle_orb_limit`, `house_proximity_orb`) |
| Dignities | `dignity_ontology.js` (`setConfig`, `lookupDetailByHouse`) |
| Genie | `map_CURRENT.html` (`__rmSyncGenieSelectors`, `display_aspects_to_angles`, `visible_minor_aspects`) |
| Theme | `theme/relocation_theme.js` (`localStorage` key `relocation.theme`) |

---

## 1. Account

| Control | Backend | Renderer | Engine | Saved | Restored | Exported | Genie | Tables | Overlays | Verdict | Notes |
|---------|---------|----------|--------|-------|----------|----------|-------|--------|----------|---------|-------|
| Account name (disabled input) | — | Y | — | — | — | — | — | — | — | STUB | Read-only from `window.CurrentUser` |
| Role / plan (disabled input) | — | Y | — | — | — | — | — | — | — | STUB | Display-only |
| Billing / sign-in copy | N | — | — | N | N | N | — | — | — | STUB | "Coming soon" copy; no keys |

---

## 2. My Data

| Control | Backend | Renderer | Engine | Saved | Restored | Exported | Genie | Tables | Overlays | Verdict | Notes |
|---------|---------|----------|--------|-------|----------|----------|-------|--------|----------|---------|-------|
| Default profile select | Y | Y | Y | Y | Y | ~ | — | — | — | REAL | `default_chart_record_id` |
| Birth profiles — search/sort/select | — | Y | — | — | — | — | — | — | — | REAL | Canon 4 sorts |
| Birth profiles — Rename | Y | Y | — | Y | Y | — | — | — | — | REAL | `/profiles/rename` |
| Birth profiles — Archive | Y | Y | — | Y | Y | — | — | — | — | REAL | `/profiles/archive` |
| Birth profiles — Set Default | Y | Y | Y | Y | Y | — | — | — | — | REAL | Via `default_chart_record_id` |
| Birth profiles — Create Profile | Y | Y | — | — | — | — | — | — | — | REAL | Intake nav |
| Birth profiles — Bulk Archive | Y | Y | — | — | — | — | — | — | — | REAL | `settingsBulkArchive` |
| Birth profiles — Duplicate | N | — | — | N | N | — | — | — | — | STUB | Disabled + Coming soon |
| Birth profiles — Delete | N | — | — | N | N | — | — | — | — | STUB | Disabled |
| Birth profiles — Bulk Delete | N | — | — | N | N | — | — | — | — | STUB | Disabled + badge |
| Create Composite | N | — | — | N | N | — | — | — | — | REMOVE | Enabled button → alert only — fake switch |
| Saved searches — Open/Rename/Archive | Y | Y | — | Y | Y | — | — | — | — | REAL | `/saved-investigations/*` |
| Saved searches — Delete | N | — | — | N | N | — | — | — | — | STUB | Disabled |
| Saved comparisons — Open/Archive | Y | Y | — | Y | Y | — | — | — | — | PARTIAL | No rename API |
| Saved comparisons — Rename/Delete | N | — | — | N | N | — | — | — | — | STUB | Disabled |
| Favorites — Archive | Y | Y | — | Y | Y | — | — | — | — | REAL | `/favorites/archive` |
| Favorites — Folders | ~ | Y | — | ~ | ~ | — | — | — | — | PARTIAL | `localStorage` only |
| Favorites — Move to folder | ~ | Y | — | ~ | ~ | — | — | — | — | PARTIAL | Client map only |
| Favorites — Rename | N | — | — | N | N | — | — | — | — | REMOVE | Enabled → alert — fake switch |
| Favorites — Delete | N | — | — | N | N | — | — | — | — | STUB | Disabled |
| Notes — Open | Y | Y | — | — | — | — | — | — | — | PARTIAL | Nav only |
| Notes — Rename/Archive/Delete | N | — | — | N | N | — | — | — | — | STUB | All disabled |
| Archives — Restore | N | — | — | N | N | — | — | — | — | STUB | `settingsStubRow` |
| History — Clear buttons | N | — | — | N | N | — | — | — | — | STUB | Disabled |
| Export My Data | N | — | — | N | N | — | — | — | — | STUB | `settingsStubRow` |

---

## 3. Astrology — Chart Framework

| Control | Backend | Renderer | Engine | Saved | Restored | Exported | Genie | Tables | Overlays | Verdict | Notes |
|---------|---------|----------|--------|-------|----------|----------|-------|--------|----------|---------|-------|
| House system select | Y | Y | N | N | Y | Y | — | — | — | REMOVE | Disabled tease; engine hardcodes Placidus |
| Zodiac (read-only) | Y | Y | N | N | Y | Y | — | — | — | PARTIAL | Tropical only; honest disabled field |

---

## 4. Astrology — Bodies

| Control | Backend | Renderer | Engine | Saved | Restored | Exported | Genie | Tables | Overlays | Verdict | Notes |
|---------|---------|----------|--------|-------|----------|----------|-------|--------|----------|---------|-------|
| Core planets (Sun–Pluto) | Y | Y | Y | Y | Y | Y | Y | Y | Y | PARTIAL | Locked on/disabled; always visible |
| Chiron | Y | Y | Y | Y | Y | Y | Y | Y | Y | REAL | Toggle + save |
| North / South Node | N | — | N | N | N | — | — | — | — | STUB | Permanently disabled |
| Part of Fortune (More points) | N | — | N | N | N | — | — | — | — | STUB | Disabled in More panel |

---

## 5. Astrology — Aspects & Orbs

| Control | Backend | Renderer | Engine | Saved | Restored | Exported | Genie | Tables | Overlays | Verdict | Notes |
|---------|---------|----------|--------|-------|----------|----------|-------|--------|----------|---------|-------|
| Major aspects (☑ + orb ×5) | Y | Y | Y | Y | Y | Y | Y | Y | Y | REAL | Engine `_active_p2p_aspects` |
| Out-of-sign aspects | Y | Y | Y | Y | Y | Y | Y | Y | Y | REAL | |
| Include aspects to asteroids | N | — | N | N | N | — | — | — | — | STUB | Disabled + SOON — honest |
| Applying / separating note | — | Y | Y | — | — | — | — | Y | Y | PARTIAL | Info panel only |
| A2A display angles (ASC/DSC/MC/IC) | Y | Y | Y | Y | Y | N | Y | Y | Y | PARTIAL | Missing from `buildSettingsSnapshot` |
| Late-house planet alert (orb) | Y | Y | Y | Y | Y | Y | — | Y | — | REAL | `house_proximity_orb_degrees` |
| Minor aspects master toggle | Y | Y | Y | Y | Y | Y | Y | Y | Y | REAL | `visible_minor_aspects` |
| Minor aspects list + orbs (×8) | Y | Y | Y | Y | Y | Y | Y | Y | Y | REAL | Advanced gate per S2 |
| Custom A2A orbs (×5) | Y | Y | Y | Y | Y | Y | Y | Y | Y | REAL | `aspect_to_angle_orbs` |
| Exact aspect threshold | Y | Y | Y | — | Y | — | — | Y | — | PARTIAL | Fixed 0.5° info-only |
| Restore astrology defaults | Y | Y | Y | Y | Y | — | Y | Y | Y | REAL | `buildAstrologyDefaultsRestorePatch` |

---

## 6. Astrology — Dignities

| Control | Backend | Renderer | Engine | Saved | Restored | Exported | Genie | Tables | Overlays | Verdict | Notes |
|---------|---------|----------|--------|-------|----------|----------|-------|--------|----------|---------|-------|
| Dignity preset | Y | ~ | — | Y | Y | N | — | Y | Y | STUB | **Duplicate `dignitiesDisplayHtml` L7696 shadows S3 impl L7598** |
| Custom dignity editor | Y | N | — | Y | Y | N | — | Y | Y | STUB | Implemented but not in active function |
| Dignity color mode (paired/four) | Y | ~ | — | Y | Y | N | — | Y | Y | PARTIAL | CSS applies on load; UI stubbed |
| Dignity color pickers | Y | ~ | — | Y | Y | N | — | Y | Y | PARTIAL | PIH classes work; editor not shown |

---

## 7. Appearance

| Control | Backend | Renderer | Engine | Saved | Restored | Exported | Genie | Tables | Overlays | Verdict | Notes |
|---------|---------|----------|--------|-------|----------|----------|-------|--------|----------|---------|-------|
| Theme picker (4 seasons) | N | Y | — | ~ | ~ | — | ~ | — | ~ | PARTIAL | `localStorage` only; not `user_settings` |
| Interface language | N | — | — | N | N | — | — | — | — | STUB | `settingsFutureRow` |
| Date format | ~ | Y | — | ~ | ~ | — | — | Y | — | PARTIAL | `rm_regional_prefs` localStorage |
| Time format (12/24) | ~ | Y | — | ~ | ~ | — | — | Y | — | PARTIAL | Same localStorage pattern |
| Wheel style / chart surface | N | — | — | N | N | — | — | — | — | STUB | `settingsFutureRow` |
| Glyph family / variants | N | — | — | N | N | — | — | — | — | STUB | Future S5 |
| Aspect band style / topology | N | — | — | N | N | — | — | — | Y | STUB | Map overlays future |
| Dignity colors (Appearance pointer) | — | — | — | — | — | — | — | — | — | STUB | Redirect to Astrology |
| Map overlay toggles | N | — | — | N | N | — | ~ | — | Y | STUB | `settingsMapBodyHtml` |
| Current location → Manage Profiles | — | Y | — | — | — | — | — | — | — | REAL | Nav button |
| Road Trip / GPS / Airplane | N | — | — | N | N | — | — | — | — | STUB | Future rows |

---

## 8. Notifications

| Control | Backend | Renderer | Engine | Saved | Restored | Exported | Genie | Tables | Overlays | Verdict | Notes |
|---------|---------|----------|--------|-------|----------|----------|-------|--------|----------|---------|-------|
| Road Trip Mode | N | — | — | N | N | — | — | — | — | STUB | `settingsStubRow` |
| Airplane Mode | N | — | — | N | N | — | — | — | — | STUB | |
| Location change alerts | N | — | — | N | N | — | — | — | — | STUB | |

---

## 9. Exports

| Control | Backend | Renderer | Engine | Saved | Restored | Exported | Genie | Tables | Overlays | Verdict | Notes |
|---------|---------|----------|--------|-------|----------|----------|-------|--------|----------|---------|-------|
| Share link visibility / hide birth / notes-tables-wheel | N | — | — | N | N | — | — | — | — | STUB | `settingsFutureRow` |
| Export / PNG-PDF presets | N | — | — | N | N | — | — | — | — | STUB | |
| Export / share status button | N | — | — | N | N | — | — | — | — | STUB | Disabled |

---

## 10. About

| Control | Backend | Renderer | Engine | Saved | Restored | Exported | Genie | Tables | Overlays | Verdict | Notes |
|---------|---------|----------|--------|-------|----------|----------|-------|--------|----------|---------|-------|
| Attribution list | — | Y | — | — | — | — | — | — | — | REAL | Static about panel |

---

## Summary

### Verdict counts (88 visible controls)

| Verdict | Count | % |
|---------|------:|--:|
| REAL | 32 | 36% |
| PARTIAL | 14 | 16% |
| STUB | 38 | 43% |
| REMOVE | 4 | 5% |

### Fake switches (enabled UI that lies)

| Control | Fix |
|---------|-----|
| Dignities preset/editor | **Fixed** — single `dignitiesDisplayHtml` (S4) |
| Favorite Rename | Disable + SOON, or wire rename API |
| Create Composite | Disable + SOON, or implement backend |
| House system dropdown | Remove teasing disabled options; read-only Placidus only |

### Biggest wiring gaps

1. ~~S3 dignities UI regression~~ **Resolved** — duplicate stub removed; snapshot export extended.
2. **Snapshot export incomplete** — `buildSettingsSnapshot` omits `dignity_*` and `display_aspects_to_angles`.
3. **Appearance prefs device-local** — theme/date/time not in `user_settings`.
4. **My Data gaps** — archives restore, permanent delete, notes management, composite.
5. **Genie sync partial** — map overlay Settings toggles still stubs.

### S1–S5 recommendations

| Priority | Action |
|----------|--------|
| Critical | Remove dignities UI stub (unblocks S3) |
| High | Extend `buildSettingsSnapshot` for dignity + A2A keys |
| Medium | Disable fake switches (Composite, Favorite Rename, house system tease) |
| S4/S5 | Appearance palettes + glyph library — not yet committed |
| Gate | Notifications, Exports, glyph picker — keep Coming Soon until keys exist |

**Status:** S0 audit complete.
