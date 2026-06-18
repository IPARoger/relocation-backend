# Task T13: Inventory Port 8000 Endpoints and Map Hard Dependencies

**Roadmap ID:** T13_1

## Objective
Create a definitive inventory of all endpoints hardcoded to `http://127.0.0.1:8000` in the active codebase, classify their migration status, and identify which ones block core features from functioning. Document the exact file locations, endpoint names, current behavior, and rollback safety.

## Scope
- **Read-only diagnosis** of frontend and backend code
- Identify every hardcoded port 8000 reference
- Classify as: migrated, partially migrated, not migrated, or archaeology
- Map which feature blocks depend on each endpoint
- No code changes; no server restarts; no deletions

## Files to Read
- `frontend/map_CURRENT.html` — search for `127.0.0.1:8000` and `LIBRARY_API_BASE`
- `frontend/app_shell.html` — search for port 8000 references
- `backend/main_centerline_FIXER.py` — identify which endpoints exist on 8004 vs. missing
- `docs/architecture/FEATURE_STATUS_BOARD.md` — cross-check blocker register (§4, B-2)
- `docs/architecture/PRODUCTION_ACCEPTANCE_CHECKLIST.md` — cross-check angular overlays (§3.3) and popup chart (§3.4)
- Any `.html` files in `frontend/` that call `/relocated-chart`, `/aura-*`, `/aspect-orb-at-point`

## Files Expected to Change
None. This is read-only diagnosis.

## Required Behavior
1. **Inventory all port 8000 calls** in HTML/JS files. For each call, record:
   - File name
   - Line number (approximate)
   - Endpoint path (e.g., `/relocated-chart`, `/aura-raster`)
   - Function/context where called
   - Whether endpoint is wrapped in try/catch or error handling

2. **Check current endpoint availability** by inspecting `main_centerline_FIXER.py`:
   - Run `grep -n "^@app\." main_centerline_FIXER.py | grep -E "(relocated|aura|aspect-orb)"` to find route definitions
   - Record which endpoints exist on port 8004

3. **Classify each endpoint:**
   - **MIGRATED**: endpoint exists on 8004, port 8000 call can be rewired
   - **PARTIAL**: endpoint exists on 8004 but with reduced functionality
   - **NOT_MIGRATED**: endpoint does not exist on 8004, migration required
   - **ARCHAEOLOGY**: endpoint is dead code (not called from active UI)

4. **Map feature blocking:**
   - For each NOT_MIGRATED endpoint, identify which feature cannot function without it
   - Cross-reference against `FEATURE_STATUS_BOARD.md` blockers

5. **Produce a structured output table** with columns:
   - Endpoint
   - Frontend file(s) calling it
   - Status (MIGRATED/PARTIAL/NOT_MIGRATED/ARCHAEOLOGY)
   - Feature(s) blocked
   - Estimated migration effort (S/M/L)
   - Next action

## Hard Stops
- Do not modify any files
- Do not restart servers
- Do not attempt live endpoint testing (read-only inspection only)
- Do not change architecture or router definitions
- Do not delete any code or references

## Validation Plan
1. **Output artifact**: `T13_port8000_inventory.md` markdown table with at least these columns:
   - Endpoint
   - Status
   - Frontend caller(s)
   - Feature blocked
   - Migration effort
   
2. **Completeness check**: Verify every grep match from step 1 is represented in the table

3. **Cross-check against blockers**: Confirm that B-2 (port 8000 legacy endpoints) findings match this inventory

4. **No false negatives**: Ensure no port 8000 calls are missed by searching:
   - `grep -r "127\.0\.0\.1:8000" frontend/`
   - `grep -r "8000" frontend/*.html`
   - `grep -r "LIBRARY_API_BASE\|aura\|relocated-chart" frontend/*.html`

## Rollback Plan
None needed — this is read-only diagnosis. If the inventory is inaccurate, the next task will catch it during implementation planning.

## Closeout Contract
**PASS criteria:**
- `T13_port8000_inventory.md` created and complete
- Every port 8000 endpoint is classified
- Every blocked feature is identified
- Table is sorted by migration effort and impact
- Findings align with `FEATURE_STATUS_BOARD.md` B-2

**Output location:** `relay/T13_port8000_inventory.md`

**Status after closeout:** NOT_VERIFIED — this is a diagnostic; next task will use this inventory to plan migrations. Human review recommended before migration begins.
