# Task: C2-2 — Verify profiles legacy write 410 quarantine

**Roadmap ID:** C2-2

## Objective
Confirm POST /profiles, PATCH /profiles/{id}, POST /profiles/{id}/archive return HTTP 410 with JWT replacement hints. No production UI caller uses legacy paths.

## Scope
- Read `main_centerline_FIXER.py` profile handlers
- Grep production UI (map_CURRENT.html, app_shell.html, first_profile_intake.js)
- Run `scripts/smoke_legacy_writes_deprecated.py` (profile rows only minimum)

## Hard stops
No code changes unless smoke fails.

## Closeout
Write `results/57_c2_2_quarantine_profiles.md` with VERIFIED or NOT VERIFIED.
