# RESULT: 01_BACKEND_WIRING_INVENTORY

**Author:** Cursor (results/ lane)
**Originating task:** tasks/01_backend_wiring_inventory (relay trial)
**Date:** 2026-06-15

## Files changed

None. Read-only audit.

## Files read

- `app_shell.html`
- `map_CURRENT.html`
- `supabase_store_bridge.js`
- `account_drawer.js`
- `current_location_editor.js`
- `main_centerline_FIXER.py`

## Findings summary

| Workflow | Complete | Partial | Missing |
|---|---|---|---|
| Chart Record | load, display, create profile | birth edit, notes (localStorage only) | birth edit persistence, profile rename frontend |
| Favorites | create, read, archive, open-on-map, view-chart | label edit | individual favorite notes |
| Saved Investigations | full lifecycle (create, resume, rename, archive, auto-search) | save-time title prompt | nothing material |
| Comparison Sets | full lifecycle (create, read, open, archive, columns) | title edit, notes | notes persistence |
| Screen 4 | engine-birth fetch, relocated facts render, blocked states | notes (placeholder), favorite btn, add-to-comparison pre-select | notes write, favorite-from-screen-4 |
| Current Location | read, write, all three entry points | three duplicated entry points, not in Saved Places | pinned-row surface, Screen 4 / compare entry |
| Settings | default chart record save, house system save | house system is saved but NEVER consumed by engine (hardcoded Placidus) | history clear, system location visibility toggle |
| Export | — | share URL placeholder (wrong domain) | PNG export, real share-link wiring, chart export |
| Account Drawer | display, set default, set location, add profile, logout | settings/help links functional but thin | profile rename, profile archive, profile notes |
| Dashboard | default record, list, investigations, open map | duplicate of Profile Mgmt list | — |

**Critical honesty gap:** House system setting is saved to `user_settings` but the
engine hardcodes Placidus (`b'P'`) in every `swe.houses` call. The setting is
currently inert. This is the largest misleading wiring in the app.

**Largest missing backend connections:**
1. Notes (Chart Record, Screen 4, Comparison) — backend routes exist (`POST /notes`
   etc.), frontend not wired.
2. Birth data edit persistence — backend `PATCH /birth-record/{id}` exists,
   frontend save handler absent.
3. Export / share links — backend `POST /share-links` exists, frontend not wired.
4. House system → engine — requires backend route param threading and `swe.houses`
   hsys parameter.

## Validation evidence

- All findings sourced from live file reads (rg + Python extract on the authorized
  files). Evidence marked (E) vs inference (I) in the audit doc.
- No database queries performed.
- No production files written.

## Rollback procedure

```bash
# No production files were changed. To remove only the audit/result docs:
rm -f audits/01_backend_wiring_inventory.md
rm -f results/01_backend_wiring_inventory.md
```

## Rejected scope

- No code changes.
- No backend / schema / data changes.
- No implementation of any discovered gap.
- No self-selected follow-up tasks. Findings are observations, not authorization.

## Remaining unknowns

- `favorite_places` schema not fully inspected for a notes column — marked
  inference in audit.
- Visited places (`POST /visited-places`) exists in backend; no frontend usage
  found in this audit — purpose unclear, not investigated further.

## Result

VERIFIED
