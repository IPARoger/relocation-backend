# TASK: 50_smoke_quarantine_routes

**Author:** relay (manual — planner PAUSE bypass)
**Model:** Auto

## Objective

Update smoke scripts that still call quarantined read routes to expect HTTP 410, then run smokes so task 49 can close as VERIFIED.

## Scope

- Smoke scripts only (`scripts/smoke_*.py` referencing `/account-store` or `/local-product-store.json`)
- No product feature changes

## Files to read

- `results/49_remove_local_store_fallback.md`
- `scripts/smoke_map_current.py`
- `scripts/smoke_saved_investigations.py`
- Grep: `account-store`, `local-product-store` under `scripts/`

## Files expected to change

- Any `scripts/smoke_*.py` that still assert 200 on quarantined routes (expect 410 or remove dead assertions)

## Required behavior

1. Grep scripts for quarantined route callers.
2. Update expectations: `/account-store`, `/profile-library/*`, `/local-product-store.json` → 410 Gone (or skip with comment if smoke is unrelated).
3. Run `python scripts/smoke_map_current.py` and `python scripts/smoke_saved_investigations.py` if env allows; document exit codes in closeout.
4. Do not change `app_shell.html` or backend routes.

## Hard stops

- schema / database / migration / credentials / renderer changes

## Validation plan

- py_compile changed smokes
- smoke exit codes in closeout

## Rollback

`git revert HEAD`

## Closeout

results/50_smoke_quarantine_routes.md — VERIFIED or NOT VERIFIED
