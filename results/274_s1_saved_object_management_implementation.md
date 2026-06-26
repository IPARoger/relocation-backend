# S1 — Saved Object Management

**Date:** 2026-06-27  
**Scope:** `app_shell.html`, `scripts/smoke_s1_saved_objects.py`, `docs/BETA_MASTER_CHECKLIST.md`  
**Canon:** [SETTINGS_V1_PRODUCT_SPEC.md](../docs/canon/SETTINGS_V1_PRODUCT_SPEC.md) · [SAVED_OBJECTS_PRODUCT_CANON.md](../docs/canon/SAVED_OBJECTS_PRODUCT_CANON.md)

## Summary

Settings → My Data now hosts saved-object management panels for birth profiles, favorites, saved searches, saved comparisons, and notes. Each panel uses the existing Settings visual language (`loc-row`, `settings-panel`, instrument surface) with search, canonical sort options, row selection, archive actions, and a confirmation dialog.

## Wired

| Object | Rename | Archive | Search | Sort | Bulk archive |
|--------|--------|---------|--------|------|--------------|
| Birth Profiles | ✅ `/profiles/rename` | ✅ `/profiles/archive` | ✅ | ✅ | ✅ |
| Saved Searches | ✅ `/saved-investigations/rename` | ✅ `/saved-investigations/archive` | ✅ | ✅ | ✅ |
| Saved Comparisons | — | ✅ `/comparison-sets/archive` | ✅ | ✅ | ✅ |
| Favorites | SOON (label API) | ✅ `/favorites/archive` | ✅ | ✅ | ✅ |
| Notes | SOON | SOON | ✅ | ✅ | — |

**Profiles:** Create Profile (intake), Set Default, Rename, Archive.  
**Favorites folders:** Client-side folder map (`localStorage`) with Create / Rename / Delete Folder and Move to Folder.  
**Composite:** Entry point + canon copy (“creates a **new** profile… never changes source profiles”); backend SOON.

## Stubbed / SOON

- Permanent **Delete** and **Bulk Delete** (irreversible warning present; action disabled)
- Profile **Duplicate**, **Delete**, **Create Composite** backend
- Comparison **Rename**
- Favorite **Rename** (display label API)
- Notes **Rename / Archive / Delete** (no JWT-owned archive route)
- **Archives** restore list

## Smoke

`scripts/smoke_s1_saved_objects.py` — static checks for sections, sort law, folder hooks, composite language, confirmation dialog.
