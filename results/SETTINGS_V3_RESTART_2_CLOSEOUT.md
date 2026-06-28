# SETTINGS-V3-RESTART-2 Closeout — My Data Hub

**Date:** 2026-06-29  
**Base:** `origin/main` + uncommitted Restart-2 work  
**Route:** `#/settings-v3/data` (hub), `#/settings-v3/data/{kind}` (manage)  
**Status:** Ready for PO QA — **not committed**

---

## Summary

Implemented the V3 **My Data** summary hub to match `prototype_settings_v2.html` layout and fields. Live counts come from production S0 collectors. **Manage** / **View** opens an inline manage panel reusing `settingsSavedObjectPanelHtml` for searches, comparisons, favorites, and notes; history/export use static production panels. Delete/export/AI/account controls remain disabled per prototype honesty rules.

Legacy `#/settings` is unchanged.

---

## Files changed

| File | Change |
|------|--------|
| `settings_v3/settings_v3.js` | Full prototype `secData()` hub + manage host; live count rows; hash `#/settings-v3/data` |
| `settings_v3/settings_v3.css` | Hub/manage panel styles |
| `app_shell.html` | V3-only data hub glue (counts refresh, open/close manage, delegation, bridge) |

---

## Production S0 handlers reused

| Handler | Use in V3 My Data |
|---------|-------------------|
| `settingsDataHubCounts()` | Live hub counts (searches, comparisons, favorites, notes, history) |
| `collectSettingsSearchItems()` | Search count (via hub counts) |
| `collectSettingsComparisonItems()` | Comparison count |
| `collectSettingsFavoriteItems()` | Favorites count |
| `collectSettingsNoteItems()` | Notes count |
| `settingsDataHistoryCount()` | History count |
| `settingsSavedObjectPanelHtml()` | Manage panels for searches/comparisons/favorites/notes |
| `settingsSavedObjectListHtml()` / toolbar | List + search/sort inside manage |
| `refreshSettingsSavedObjectPanel(type)` | Refresh manage lists; refreshes hub counts on V3 route |
| `ensureSettingsDataDelegation()` | All manage actions (archive, open, folder, notes, etc.) |
| `ensureSettingsObjectNotesDialog()` | Favorites/comparison notes |
| `prefetchSettingsInvestigationNotesCache()` | Saved search notes prefetch |
| `settingsDataHistoryPanelHtml()` | History manage view |
| `settingsDataExportPanelHtml()` | Export placeholder view |

### V3-only glue (does not modify `#/settings`)

- `refreshSettingsV3DataHub()`
- `openSettingsV3DataManage(kind)` / `closeSettingsV3DataManage()`
- `wireSettingsV3Data()`
- `SETTINGS_V3_DATA_MANAGE` map
- Delegation: `settings-v3-data-manage`, `settings-v3-data-back`
- `window.__rmSettingsV3Bridge`: `refreshDataHub`, `wireData`, `dataHubCounts`, `openDataManage`, `closeDataManage`

---

## Not wired (prototype-visible, disabled/honest)

- Export button (disabled)
- AI & privacy toggle (locked + soon)
- All Delete data buttons (disabled)
- Delete account (disabled + soon)
- Charts, Map, Appearance, Language, Sharing, Help, City Intelligence (unchanged stubs)

---

## Browser QA checklist (PO — signed in on FIXER :8000)

### Hub (`#/settings-v3/data`)

- [ ] My Data card matches prototype sections: Data management, Export, AI & privacy, Delete data, Account deletion
- [ ] Live counts shown for Saved searches, comparisons, favorites, notes, history
- [ ] Manage opens inline panel for searches / comparisons / favorites / notes
- [ ] View opens History panel (static/disabled clear buttons)
- [ ] Back returns to hub; counts unchanged unless data changed
- [ ] Export row present; Export button disabled
- [ ] Delete rows present; all delete buttons disabled
- [ ] Legacy `#/settings/data` unchanged

### Manage panels

- [ ] Saved searches: list, search, sort, archive (production behavior)
- [ ] Comparisons: list, search, sort, archive
- [ ] Favorites: list, folders, notes, archive
- [ ] Notes: list from `collectSettingsNoteItems`
- [ ] History: static panel with soon/disabled clears

### Regression

- [ ] `#/settings-v3` My Profiles still works (Restart-1)
- [ ] No changes to `#/settings` routes or layout

---

## Screenshots

| | Path | Status |
|---|------|--------|
| Prototype My Data | `results/screenshots/SETTINGS_V3_RESTART_2_prototype_data.png` | Captured (scrolled to `#sec-data`) |
| V3 My Data hub | `results/screenshots/SETTINGS_V3_RESTART_2_v3_data_hub.png` | **PO capture** — requires signed-in session on `http://127.0.0.1:8000/app_shell.html#/settings-v3/data` |

---

## How to test

```text
# Use FIXER backend (not static python http.server)
http://127.0.0.1:8000/auth.html   → sign in
http://127.0.0.1:8000/app_shell.html#/settings-v3/data
```

Feature flag: `localStorage.relocation.flag.settingsV3 = "1"` (default on).

---

## Commit gate

Do **not** commit until PO checks all hub + manage items above.
