# RESULT: C2-1_audit-legacy-write-routes

**Roadmap ID:** C2-1
**Author:** Cursor (manual copy-paste track)
**Date:** 2026-06-17 UTC

## Summary

Audit of `main_centerline_FIXER.py` write routes vs production UI callers (`map_CURRENT.html`, `app_shell.html`, `first_profile_intake.js`, `place_resolution.js`).

**Finding: Chat 2 write-route 410 quarantine is largely already implemented** via `_deprecated_legacy_write()` (returns HTTP 410 with JWT replacement hint). C2-2..C2-6 code changes may be **already done**; remaining work is likely **C2-7 smokes** and verification.

## Legacy service-role writes → already 410 (26 routes)

| Family | Legacy routes | Status |
|--------|---------------|--------|
| Profiles | POST /profiles, PATCH /profiles/{id}, POST …/archive | 410 → JWT rename/archive/create-with-birth |
| Birth records | POST /birth-records, PATCH/archive variants | 410 |
| Places | POST /places | 410 → /places/resolve-or-create |
| Saved searches | POST /saved-searches, PATCH/archive | 410 → saved-investigations JWT routes |
| Comparison sets | POST /comparison-sets, PATCH/archive, place add/remove | 410 → JWT create/archive |
| Favorite places | POST /favorite-places, PATCH/archive | 410 → /favorites/save, /favorites/archive |
| Notes | POST /notes, PATCH /note/{id}, archive | 410 → scoped /notes/chart-record etc. |
| User settings | POST/PATCH /user-settings | 410 → PATCH /settings/account |

## Live writes production UI uses (31 live — keep)

JWT ownership routes: `/profiles/create-with-birth`, `/profiles/rename`, `/profiles/archive`, `/favorites/save`, `/favorites/archive`, `/comparison-sets/create`, `/comparison-sets/archive`, `/saved-investigations/*`, `/settings/account`, `/notes/chart-record`, `/notes/comparison-set`, `/notes/saved-investigation`, `/places/resolve-or-create`.

Computation (not ownership): `POST /search-regions`, aura endpoints, library sandbox routes, `POST /current-location/set`.

## Production UI — no callers found for legacy 410 paths

Grep of production JS/HTML shows **no** fetch to legacy POST /profiles, /favorite-places, /saved-searches, /comparison-sets (non-JWT), or /notes (generic).

`place_resolution.js` still POSTs — verify targets `/places/resolve-or-create` not deprecated `/places`.

## Recommended next tasks

1. **C2-7 (S):** Add/update smokes asserting 410 on all `_deprecated_legacy_write` paths.
2. Verify `place_resolution.js` POST target (if still `/places`, migrate caller not route).
3. Library write routes (`/library/*`) — out of Chat 2 scope (legacy port-8000 library); defer.

## Validation

- Static grep of `main_centerline_FIXER.py` and production UI files.
- Python route classifier: 26 deprecated writes, 31 live writes.

**VERIFIED** (audit only — no runtime smokes run in this task).
