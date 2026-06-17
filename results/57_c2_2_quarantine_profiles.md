# RESULT: 57_c2_2_quarantine_profiles

**Roadmap ID:** C2-2  
**Originating task:** tasks/57_c2_2_quarantine_profiles_legacy_writes.md  
**Date:** 2026-06-17 UTC

## Summary verdict

**VERIFIED** — no code changes required. Legacy profile write routes were already quarantined via `_deprecated_legacy_write()` before this task.

## Route status

| Route | HTTP | Replacement hint |
|-------|------|------------------|
| POST /profiles | 410 | POST /profiles/create-with-birth |
| PATCH /profiles/{id} | 410 | POST /profiles/rename |
| POST /profiles/{id}/archive | 410 | POST /profiles/archive |

## Production UI callers

| File | Call | Verdict |
|------|------|---------|
| first_profile_intake.js | POST /profiles/create-with-birth (JWT) | OK — JWT path |
| app_shell.html | POST /profiles/archive, /profiles/rename (JWT) | OK — JWT paths |
| map_CURRENT.html | GET /profiles only (read, optional) | OK — no legacy writes |

No production fetch to legacy POST/PATCH profile write paths found.

## Smoke evidence

```
./venv/bin/python scripts/smoke_legacy_writes_deprecated.py
PASS: POST /profiles — replacement='/profiles/create-with-birth'
PASS: PATCH /profiles/... — replacement='/profiles/rename'
PASS: POST /profiles/.../archive — replacement='/profiles/archive'
Summary: 25/25 deprecated routes return 410
PASS: smoke_legacy_writes_deprecated
```

## Files changed

None (verification-only).

## Rollback

N/A.

## Rejected scope

Implementing new 410 handlers — already present.
