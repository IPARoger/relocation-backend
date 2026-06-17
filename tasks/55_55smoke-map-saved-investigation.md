# Task 55 — Smoke-test map page and saved-investigation routes with Playwright

## Objective
Run targeted Playwright smoke tests against the map page (`map_CURRENT.html`) and the saved-investigation read route, which were explicitly **not** covered by the quarantine-route smokes in Task 54. Produce a pass/fail evidence file.

---

## Scope
Read-only test execution. No source code changes. No schema changes. No backend changes.

---

## Files to Read
- `relay/results/54_54run-quarantine-smoke-tests.md` — prior smoke results; understand what passed and what was explicitly deferred
- `tests/smoke/` — existing smoke scripts; confirm what exists and what is missing for map + saved-investigation routes
- `map_CURRENT.html` — understand which endpoints the map page calls on load (profile load, engine-birth resolution)
- `main_centerline_FIXER.py` — confirm `/supabase/chart-records/{id}/engine-birth` and `/profiles` route signatures
- `supabase_store_bridge.js` — confirm saved-investigation read path (if any frontend call exists)
- `.env.staging` — confirm environment variables (read only; never log secrets)

---

## Files Expected to Change
- **Create:** `relay/results/55_smoke-map-saved-investigation.md` — evidence file with test outcomes

No production source files are modified.

---

## Required Behavior

### Step 1 — Audit existing smoke scripts
List every file under `tests/smoke/` (or equivalent). Identify whether a map-page smoke script and a saved-investigation smoke script already exist. If they exist, note their names. If they do not exist, write minimal new scripts (Step 2).

### Step 2 — Write missing smoke scripts (if absent)
Write the smallest Playwright scripts needed:

**map-page-smoke.spec.js** (if absent):
- Navigate to `http://127.0.0.1:8004/map_CURRENT.html` with a valid session cookie or via the auth flow
- Assert Leaflet map container is present in DOM (`#map` or `.leaflet-container`)
- Assert `GET /profiles` returns 200 (intercept network or read console log)
- Assert `GET /supabase/chart-records/<uuid>/engine-birth` returns 200 (use a known test profile UUID from `.env.staging` or skip with a clear SKIP note if no test UUID is available)
- Assert no unhandled JS errors on load

**saved-investigation-smoke.spec.js** (if absent):
- Call `GET http://127.0.0.1:8004/saved-searches/<profile_id>` directly (HTTP request, no browser needed) with a valid auth token from the staging session
- Assert HTTP 200 or 404 (both are acceptable — 404 means no saved searches exist, which is valid; any 5xx is a failure)
- Assert response is valid JSON

### Step 3 — Run the scripts
```bash
cd /path/to/project
npx playwright test tests/smoke/map-page-smoke.spec.js tests/smoke/saved-investigation-smoke.spec.js --reporter=line
```
If a test profile UUID is unavailable in the environment, mark that assertion SKIP with a written reason. Do not fabricate a UUID.

### Step 4 — Record results
Write `relay/results/55_smoke-map-saved-investigation.md` containing:
- Date/time of run
- Playwright version and Chromium version
- Server port confirmed running (`curl http://127.0.0.1:8004/health`)
- For each assertion: PASS / FAIL / SKIP with brief reason
- Full stdout/stderr from Playwright (trimmed to relevant lines if very long)
- Any console errors captured from the map page
- Overall verdict: VERIFIED / PARTIALLY VERIFIED / NOT VERIFIED

---

## Hard Stops
- Do **not** modify `map_CURRENT.html`, `main_centerline_FIXER.py`, or any backend file
- Do **not** change any route, endpoint, or schema
- Do **not** run against production — staging only (`127.0.0.1:8004`)
- Do **not** log or record actual secret values from `.env.staging`; reference variable names only
- Do **not** attempt to migrate port 8000 endpoints — those are BLOCKED per FEATURE_STATUS_BOARD.md B-2 and out of scope here
- If Playwright is not installed or Chromium is missing, **STOP** and record the blocker in the results file; do not attempt re-installation (that was Task 51–52's scope)

---

## Validation Plan
The task is VERIFIED if:
1. `relay/results/55_smoke-map-saved-investigation.md` exists
2. Map container assertion is PASS (Leaflet DOM present)
3. `/profiles` 200 assertion is PASS or SKIP with written reason
4. `engine-birth` assertion is PASS or SKIP with written reason
5. Saved-investigation endpoint returns 200 or 404 (not 5xx)
6. No unhandled JS errors on map page load (or errors are listed and understood)

The task is PARTIALLY VERIFIED if any assertion is FAIL or SKIP with reason documented, but the results file exists and explains each outcome.

The task is NOT VERIFIED if the results file does not exist.

---

## Rollback Plan
No production code was changed. Rollback = delete any newly created smoke script files under `tests/smoke/` if they introduced syntax errors. The results file is append-only evidence; it does not affect runtime behavior.

---

## Closeout Contract
Cursor must produce `relay/results/55_smoke-map-saved-investigation.md` with:
- Overall verdict on first line: `VERIFIED`, `PARTIALLY VERIFIED`, or `NOT VERIFIED`
- Per-assertion table (assertion name | result | notes)
- Raw Playwright output (or error if Playwright could not run)
- List of any new smoke script files created and their paths
- Explicit statement of what remains untested and why
