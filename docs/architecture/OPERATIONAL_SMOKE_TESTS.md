# OPERATIONAL SMOKE TESTS

**Status:** Canonical verification procedure  
**Last updated:** 2026-06-14  
**Purpose:** Executable test procedure for all production-critical workflows.  
**Audience:** Any engineer with no prior project history.

**Legend:**  
- `[IMPLEMENTED]` — fully wired and testable  
- `[PARTIAL]` — partially wired; limitations noted  
- `[BLOCKED]` — depends on port 8000 legacy service being available  
- `[NOT WIRED]` — backend or frontend not yet connected  

---

## ENVIRONMENT SETUP

Before running any test:

1. Start the Web2 server:
   ```bash
   cd /path/to/relocation-backend
   set -a && source .env.staging && set +a
   venv/bin/uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8004 --reload
   ```

2. Verify server health:
   ```bash
   curl http://127.0.0.1:8004/health
   # Expected: {"status":"ok"}
   ```

3. Open browser and navigate to: `http://127.0.0.1:8004/auth.html`

4. Have access to Supabase dashboard (staging project) to verify database writes.

5. Have a test account email and password for staging.

---

## 1. AUTHENTICATION — Email/Password `[IMPLEMENTED]`

**Preconditions:**
- Server running on port 8004
- Supabase staging project accessible
- Test email not previously registered (for signup test) OR previously registered (for login test)

**Test Steps — Signup:**
1. Navigate to `http://127.0.0.1:8004/auth.html`
2. Confirm page shows "Create your account" heading
3. Enter a new email address
4. Enter a password ≥ 8 characters
5. Click signup button
6. If email confirmation is required: check inbox, click link
7. Confirm redirect to `http://127.0.0.1:8004/map_CURRENT.html`

**Test Steps — Login:**
1. Navigate to `http://127.0.0.1:8004/auth.html`
2. Toggle to "Sign in" mode
3. Enter existing email and password
4. Click sign in
5. Confirm redirect to `map_CURRENT.html`

**Test Steps — Session persistence:**
1. After login, close and reopen the browser tab
2. Navigate to `http://127.0.0.1:8004/map_CURRENT.html`
3. Confirm map loads without redirect to auth

**Test Steps — Logout:**
1. On `map_CURRENT.html`, confirm a logout mechanism is accessible
2. Trigger logout
3. Confirm redirect to `auth.html`
4. Confirm revisiting `map_CURRENT.html` redirects back to `auth.html`

**Expected Results:**
- Signup: `auth.users` row created; `accounts` row created; `account_memberships` row created (verify in Supabase dashboard)
- Login: existing session restored
- Session: persists across tab close
- Logout: session cleared, auth guard fires

**Failure Indicators:**
- Stays on `auth.html` after signup/login → check browser console for `supabase.auth` errors
- Redirects but immediately bounces back to `auth.html` → `auth_guard.js` detecting no session; check `window.SupabaseReady`
- `accounts` row not created after signup → `handle_new_user()` trigger not applied to Supabase project

**Recovery Notes:**
- If `handle_new_user()` trigger is missing, apply migration `supabase/migrations/2026_06_13_phase6_signup_bootstrap.sql`
- If RLS blocks session check, confirm `auth_guard.js` uses `supabase.auth.getSession()` not a direct table query

---

## 2. GOOGLE AUTH `[NOT WIRED]`

**Current state:** Google OAuth is not implemented in `auth.html`. No `signInWithOAuth({provider: 'google'})` call exists.

**Preconditions for future implementation:**
- Google Cloud Console OAuth app created
- `GOOGLE_CLIENT_ID` configured in Supabase Auth → Providers → Google
- `auth.html` updated with Google OAuth button

**Skip this test until Google OAuth is implemented.**

---

## 3. APPLE AUTH `[NOT WIRED]`

**Current state:** The string "apple" appears in `auth.html` but no `signInWithOAuth({provider: 'apple'})` call is implemented. Apple Auth UI and wiring are absent.

**Preconditions for future implementation:**
- Apple Developer account ($99/yr)
- Sign in with Apple capability configured
- `auth.html` updated with Apple OAuth button

**Skip this test until Apple Auth is implemented.**

---

## 4. FIRST PROFILE CREATION `[IMPLEMENTED]`

**Preconditions:**
- Authenticated session exists (test completed in §1)
- The test account has NO existing profiles (new account, or existing profiles deleted from Supabase)
- Port 8004 running

**Test Steps:**
1. Navigate to `http://127.0.0.1:8004/map_CURRENT.html`
2. Confirm the first-profile intake overlay appears (not the map)
3. Enter a display name (e.g. "Test Profile")
4. Enter birth date (e.g. 1990-06-15)
5. Select birth time mode: "Exact"
6. Enter birth time (e.g. 14:30)
7. In birth city field, type at least 2 characters (e.g. "New York")
8. Confirm city search results appear in a dropdown
9. Select "New York City, NY, United States" from results
10. Click "Create my chart"
11. Confirm redirect to `map_CURRENT.html?handoff=app_shell&chartRecordId=<uuid>&...`
12. Confirm map loads (not intake overlay)
13. Confirm profile dropdown shows the new profile name

**Expected Results:**
- `profiles` table: new row with `display_name`, `account_id`, `profile_type="human"`
- `birth_records` table: new row with `birth_date`, `birth_time_mode="exact"`, `birth_time_start`, `birth_place_id` (a valid UUID from `places`)
- `places` table: "New York City, NY, United States" row exists (was pre-loaded by GeoNames ingest)
- Redirect URL contains `handoff=app_shell&chartRecordId=<profiles.id>`

**Failure Indicators:**
- "Birth place is required" error → city search returned no results; check `places` table row count (`SELECT count(*) FROM places`)
- Intake overlay reappears after redirect → profile INSERT succeeded but birth_record INSERT failed; check `birth_records` table; check console for compensating delete messages
- Profile dropdown shows "Loading…" after redirect → `GET /profiles` call failing; check server log for errors

**Recovery Notes:**
- If `places` table has fewer than 100 rows, run `scripts/ingest_cities_to_places.py` to load GeoNames dataset
- If birth_record INSERT fails with timezone error, confirm `places.timezone_id` is populated for the selected city

---

## 5. CITY SEARCH `[IMPLEMENTED]`

**Preconditions:**
- Authenticated session
- `places` table has GeoNames dataset loaded (~68,032 rows)
- Either intake overlay is visible OR `current_location_editor.js` overlay is accessible

**Test Steps — from intake overlay:**
1. Begin first profile intake (see §4)
2. In birth city field, type "New York" — expect results within ~300ms debounce
3. Confirm "New York City, NY, United States" appears in results
4. Clear field, type "Pod" — confirm "Podgorica, 16, Montenegro" appears
5. Clear field, type "Chiang" — confirm "Chiang Mai" appears
6. Clear field, type "XYZNonexistent" — confirm no results / "No results" state

**Test Steps — verify result shape:**
1. Select a city
2. Confirm selected city text appears in input
3. Confirm "Create my chart" becomes active (not disabled)

**Expected Results:**
- Results appear for prefix queries of ≥2 characters
- Each result includes display_name, country_code, admin1
- No results for nonsense queries

**Failure Indicators:**
- No results for known cities → RLS blocking authenticated read; verify `places_select` policy is `for select to authenticated using (true)`
- Results appear for service-role probe but not in browser → user is not authenticated; session missing
- Admin1 shows numeric codes (e.g. "16" instead of "Podgorica") → `admin1CodesASCII.txt` was not used during GeoNames ingest; display-only issue, does not affect functionality

**Recovery Notes:**
- Verify row count: `SELECT count(*) FROM places WHERE provider = 'geonames'` should return ~68,032
- If count is 0: run `scripts/ingest_cities_to_places.py` with `.env.staging` sourced

---

## 6. PROFILE LOADING `[IMPLEMENTED]`

**Preconditions:**
- Authenticated session
- At least one profile with a birth record exists on the account
- Port 8004 running

**Test Steps:**
1. Navigate to `http://127.0.0.1:8004/map_CURRENT.html`
2. Confirm map loads (not intake overlay)
3. Open browser DevTools console
4. Inspect `#chartProfile` select element — confirm it contains the profile name (not "Loading…")
5. Run in console: `window.__rmChartProfilesReady.then(r => console.log('profiles:', r))`
6. Confirm console output shows profile UUID matching the Supabase `profiles.id`

**Test Steps — multi-profile account:**
1. Create a second profile (via Account Drawer → Add Profile)
2. Reload map
3. Confirm both profiles appear in `#chartProfile` dropdown
4. Switch profiles — confirm selection persists in sessionStorage (`rm_active_profile_id`)

**Expected Results:**
- Dropdown populated from `GET /profiles` (8004)
- Active profile UUID from URL `chartRecordId` param is auto-selected
- `window.CurrentUser.accountId` matches the profile's `account_id`

**Failure Indicators:**
- "Loading…" stays → `loadChartProfiles()` threw; check console for "chart-profiles" error
- Wrong profiles appear → server loaded from wrong `.env` (not `.env.staging`); restart with correct env
- Profiles appear but wrong one is selected → `applyActiveProfileSelection()` couldn't match URL `chartRecordId`; verify URL contains the correct UUID

---

## 7. CURRENT LOCATION `[IMPLEMENTED]`

**Preconditions:**
- Authenticated session with at least one profile
- Account Drawer accessible in `app_shell.html`
- Port 8004 running

**Test Steps:**
1. Navigate to `http://127.0.0.1:8004/app_shell.html`
2. Open Account Drawer (button in header)
3. Find "Set Current Location" button under active profile
4. Click it — confirm `current_location_editor.js` overlay opens
5. Type a city name (e.g. "Bangkok")
6. Confirm results appear
7. Select a result
8. Click Save
9. Confirm overlay closes
10. Confirm page reloads
11. After reload, open Account Drawer again — confirm current location displays the selected city name

**Expected Results:**
- `current_location_history` table: old rows for this profile have `is_current=false`
- New row: `profile_id`, `account_id`, `place_id`, `is_current=true`, `source="manual"`, `selected_at=now()`
- Account Drawer shows new city name under active profile

**Failure Indicators:**
- City search returns no results → same root cause as §5 (places table empty or RLS issue)
- Save fails with RLS error → verify `current_location_history_insert` policy exists in Supabase
- Account Drawer still shows old city after reload → `supabase_store_bridge.js` not re-reading bridge; check bridge queries `current_location_history` with `is_current=true`

---

## 8. MAP LAUNCH `[IMPLEMENTED]`

**Preconditions:**
- Authenticated session with profile + birth record
- Port 8004 running

**Test Steps — via post-intake redirect:**
1. Complete §4 (first profile creation)
2. Confirm URL is: `map_CURRENT.html?skipOnboarding=1&handoff=app_shell&handoffCreatedAt=<iso>&chartRecordId=<uuid>`
3. Confirm Leaflet map renders (not blank)
4. Confirm profile dropdown shows profile name (not "Loading…")
5. Confirm no "Birth data required" message visible

**Test Steps — via app_shell handoff:**
1. Navigate to `http://127.0.0.1:8004/app_shell.html`
2. After profile loads, navigate to "Map" screen
3. Click "Open production map" link
4. Confirm `map_CURRENT.html` opens in new tab with full handoff URL

**Test Steps — console verification:**
1. Open DevTools Network tab before navigating to map
2. Load map with handoff URL
3. Confirm `GET /profiles` returns 200
4. Confirm `GET /supabase/chart-records/<uuid>/engine-birth` returns 200 with birth params

**Expected Results:**
- Map renders with Leaflet tiles
- Profile selector populated and active profile selected
- `lastAppShellHandoff` object populated (run `window.__rmAppShellHandoff()` in console)
- `GET /supabase/chart-records/<uuid>/engine-birth` returns: `{birth_year, birth_month, birth_day, birth_hour_utc, chart_record_id}`

**Failure Indicators:**
- Blank map or Leaflet container missing → JS error during initialization; check console
- Intake overlay fires despite having a profile → `SupabaseStoreReady` rejected; check `supabase_store_bridge.js` console errors; verify RLS policies allow reading profiles
- Engine-birth returns 404 → birth_record missing for this profile; check `birth_records` table

---

## 9. FIND REGIONS `[IMPLEMENTED]`

**Preconditions:**
- Map loaded with a Supabase profile selected (§8 complete)
- Profile has an exact birth time (mode = "exact")
- Port 8004 running (`/search-regions` endpoint active)

**Test Steps:**
1. Load map with handoff URL (from §8)
2. Verify profile name appears in dropdown (not "Loading…")
3. Select planet condition: e.g. "Sun" in house "10"
4. Click "Find regions"
5. Confirm button disables briefly, then re-enables
6. Confirm colored polygon overlays appear on the map

**Test Steps — console verification:**
1. Open DevTools Network tab
2. Click "Find regions"
3. Confirm `GET /supabase/chart-records/<uuid>/engine-birth` → 200
4. Confirm `POST /search-regions` → 200 with GeoJSON body

**Expected Results:**
- Planet/house polygons render on the map
- Button re-enables after render completes
- No console errors

**Failure Indicators:**
- Nothing happens on click → look for debounce (400ms delay is normal); wait ~1 second
- "Birth data required" → engine-birth failed; check Network tab for `/engine-birth` response
- "No profile selected" → profile dropdown has no selection; verify `applyActiveProfileSelection()` matched the `chartRecordId` in URL
- Polygons don't appear but no error → `setRenderStatus` message hidden (requires `debugGeometry` mode); check Network tab for `/search-regions` response
- `/search-regions` returns 500 → check server log for Python math engine error

**Recovery Notes:**
- To see status messages: append `?generation_mode=contour` to URL (does not enable debugGeometry but may help)
- Profiles with birth_time_mode="unknown" will fail engine-birth with 422

---

## 10. ANGULAR OVERLAYS `[BLOCKED — port 8000]`

**Current state:** Aura/angular overlays (`/aura-raster`, `/aura-raster-adaptive`, `/aura-field`) all call `http://127.0.0.1:8000`. Port 8000 must be running for these to work. They are not migrated to port 8004.

**Preconditions:**
- Port 8000 legacy server running
- Map loaded with active profile (§8 complete)

**Test Steps:**
1. Load map with handoff URL
2. In the aspect overlay selector, choose "Sun · conjunction · ASC"
3. Click "Find regions"
4. Confirm angular overlay layer appears in addition to house polygons

**Expected Results:**
- Both house region polygons and angular overlay rendered
- Network: `POST http://127.0.0.1:8000/aura-raster` or `/aura-field` → 200

**Failure Indicators:**
- House regions appear but no angular overlay → port 8000 down; aura call fails silently
- Console shows `TypeError: Failed to fetch` for port 8000 endpoints

**Recovery Notes:**
- Start the legacy calculation server on port 8000
- Migrating these endpoints to port 8004 is a future step

---

## 11. FAVORITES `[IMPLEMENTED]`

**Preconditions:**
- Map loaded with Supabase profile selected (§8 complete)
- `window.CurrentUser.accountId` is populated
- Port 8004 running

**Test Steps — add favorite:**
1. Right-click a city on the map — confirm popup opens
2. Locate "Favorite" button in popup
3. Click "Favorite"
4. Confirm button text changes to "Favorited ✓"
5. Confirm status message "Saved to favorites." appears

**Test Steps — verify in Supabase:**
1. Open Supabase dashboard → Table Editor → `favorite_places`
2. Confirm new row with:
   - `account_id` matching `window.CurrentUser.accountId`
   - `profile_id` matching selected profile UUID
   - `place_id` matching the city
   - `label` matching the city display name
   - `archived_at = null`

**Test Steps — duplicate check:**
1. Close and reopen the same city popup
2. Confirm "Favorite" button shows "Favorited ✓" state immediately (from `applyMapFavoriteButtonState()`)
3. Click "Favorite" again
4. Confirm "Already in favorites." message — no new row added

**Test Steps — favorites appear in app_shell:**
1. Navigate to `app_shell.html`
2. Open chart record screen for the active profile
3. Confirm favorited city appears in favorites list

**Expected Results:**
- Exactly one `favorite_places` row per profile/place pair
- Duplicate click produces no new row
- `supabase_store_bridge.js` reads `favorite_places` → appears in app_shell store

**Failure Indicators:**
- "Select a saved profile to favorite places." → `getActiveFavoriteProfileId()` returned null; profile dropdown has no Supabase option selected
- "no_account_id" error → `window.CurrentUser` is null; session/profile loading failed (check §6)
- "supabase_client_unavailable" → `window.SupabaseClient` not loaded; check script load order

---

## 12. SAVED INVESTIGATIONS `[NOT WIRED]`

**Current state:** Backend endpoints exist (`POST /saved-searches`, `GET /saved-searches/{profile_id}`). No frontend UI is wired to these endpoints. The `saved_searches` Supabase table and repository exist but are not exposed in `app_shell.html` or `map_CURRENT.html` as a user-visible feature.

**Skip this test until frontend wiring is implemented.**

---

## 13. SAVED COMPARISONS `[PARTIAL]`

**Current state:** `screenCompare()` function exists in `app_shell.html`. Backend comparison endpoints exist (`POST /comparison-sets`, etc.). `supabase_store_bridge.js` reads `comparison_sets` and `comparison_set_places`. However, comparison facts shown in the UI are placeholder/static text, not computed relocated-chart data.

**Preconditions:**
- Authenticated session with profile + birth record
- Port 8004 running

**Test Steps — comparison screen loads:**
1. Navigate to `app_shell.html`
2. Navigate to "Compare" screen
3. Confirm screen renders without error

**Test Steps — comparison data:**
1. Confirm comparison rows show city names (real data) or placeholder text
2. Note: fact values ("Sun in 10th", "ASC in Gemini") are currently placeholder/static

**Expected Results:**
- Compare screen renders
- If comparison sets exist in Supabase: they appear listed
- Fact data is acknowledged as placeholder

**Failure Indicators:**
- Comparison screen shows "undefined" or crashes → `adaptStoreToView()` failing; check `comparison_sets` schema alignment

---

## 14. NOTES `[PARTIAL — localStorage only]`

**Current state:** Notes v1 is implemented in `app_shell.html` using `localStorage` only. The Supabase `notes` table exists but is not connected. Notes do not persist across devices or cleared storage.

**Preconditions:**
- Authenticated session with active chart record
- `app_shell.html` loaded

**Test Steps:**
1. Navigate to a chart record screen in `app_shell.html`
2. Locate the "Notes" panel / textarea
3. Type a note
4. Click "Save Note"
5. Confirm success message appears
6. Reload the page
7. Navigate to the same chart record
8. Confirm note text is still present

**Test Steps — isolation:**
1. Navigate to a different chart record
2. Confirm note field is empty (notes are per `chartRecordId`)
3. Return to original chart record — confirm original note is still there

**Expected Results:**
- Note saved to: `localStorage key = rm_note_<chartRecordId>`
- Note reloads on same chart record
- Different chart records have independent notes

**Failure Indicators:**
- Note not saved → `save-chart-note` action handler not bound; check `bindScreenActions()` in `app_shell.html`
- Note disappears after reload → localStorage was cleared or `chartRecordId` changed

**Known Limitation:** Notes are lost on: browser data clear, private/incognito mode, different device, different browser.

---

## 15. SETTINGS `[IMPLEMENTED]`

**Preconditions:**
- Authenticated session
- At least one profile exists
- Port 8004 running

**Test Steps:**
1. Navigate to `app_shell.html`
2. Navigate to "Settings" screen via Account Drawer or navigation
3. Confirm settings controls are enabled (not disabled)
4. Change "Default chart" to a different profile
5. Change "House system" to "Whole Sign"
6. Click "Save Settings"
7. Confirm success/error message appears
8. Reload page
9. Navigate back to Settings
10. Confirm saved values persist

**Test Steps — Supabase verification:**
1. Open Supabase dashboard → `user_settings` table
2. Confirm row exists with:
   - `account_id` matching current user
   - `settings_json` containing `default_chart_record_id` and `house_system`

**Expected Results:**
- Controls enabled (not greyed out)
- Values save to `user_settings.settings_json`
- Values reload correctly after page refresh

**Failure Indicators:**
- Controls still disabled → `screenSettings()` not enabling them; possible branch issue in render
- Save fails → check `POST /user-settings` or `PATCH /user-settings/{id}` response in Network tab
- Duplicate row error → unique constraint issue on `user_settings`; check `SELECT-before-INSERT` logic

---

## 16. EXPORTS `[NOT WIRED]`

**Current state:** `screenExport()` function exists in `app_shell.html` as a placeholder. No export functionality is implemented (no PDF, no PNG, no data download). The screen renders but contains no functional controls.

**Skip this test until exports are implemented.**

---

## 17. HELP `[IMPLEMENTED — static]`

**Preconditions:**
- `app_shell.html` loaded with authenticated session

**Test Steps:**
1. Open Account Drawer
2. Click "Help / Learn" link
3. Confirm navigation to "help" route in `app_shell.html`
4. Confirm Help screen renders with sections: "Start Here", "How to Use the Map", "Beginner Path", "Professional Path", "Feedback"
5. Confirm "Back to Dashboard" link navigates to dashboard
6. Confirm no network requests are made (static screen)

**Expected Results:**
- Help screen renders
- All sections visible
- No 404 errors
- No Supabase calls triggered

**Failure Indicators:**
- Blank screen → `screenHelp()` function missing or `help` route not in `SCREEN_RENDERERS`
- Navigation link doesn't work → `ad-help` action not bound in `account_drawer.js`

---

## 18. ONBOARDING `[IMPLEMENTED — static]`

**Preconditions:**
- Authenticated session with at least one profile
- `localStorage key = rm_guided_onboarding_dismissed` is absent or set to anything other than `"1"`

**Test Steps — first-time experience:**
1. Open browser DevTools → Application → Local Storage
2. Delete key `rm_guided_onboarding_dismissed` if it exists
3. Reload `app_shell.html`
4. Confirm onboarding modal appears after data loads
5. Confirm modal contains welcome copy, "Start here" button, "Skip" button
6. Click "Start here" → confirm navigation to "help" route
7. Repeat test; this time click "Skip" → confirm modal closes
8. Reload page → confirm modal does NOT reappear (dismissed state persisted)

**Test Steps — already dismissed:**
1. Confirm `localStorage.rm_guided_onboarding_dismissed === "1"`
2. Reload `app_shell.html`
3. Confirm onboarding modal does NOT appear

**Expected Results:**
- Modal appears exactly once per browser (until storage cleared)
- "Start here" navigates to help screen
- "Skip" closes modal and sets localStorage flag
- Modal never appears again after dismissal

**Failure Indicators:**
- Modal does not appear on first load → `maybeShowGuidedOnboarding()` not called after bootstrap; check `bootstrap()` function in `app_shell.html`
- Modal appears every reload → localStorage write failing (private browsing mode)

---

## PRE-RELEASE SMOKE SUITE

This is the minimum test sequence required before any production deployment. Estimated time: 15 minutes.

Run in order. Do not proceed past any FAIL.

```
STEP  TEST                           FILE(S)                    PASS CRITERIA
────  ─────────────────────────────  ─────────────────────────  ────────────────────────────────────────────
  1   Server health                  —                          GET /health → 200 {"status":"ok"}
  2   Auth page loads                auth.html                  Page renders, no console errors
  3   Email/password signup          auth.html → Supabase       New auth.users row; accounts + memberships rows created
  4   Auth redirect                  auth.html → map_CURRENT    Browser lands at /map_CURRENT.html after signup
  5   Intake overlay fires           map_CURRENT.html           Intake overlay appears (no prior profiles)
  6   City search works              first_profile_intake.js    "New York" query returns results from places table
  7   Profile creation               first_profile_intake.js    profiles + birth_records rows created; redirect fires
  8   Handoff URL correct            map_CURRENT.html           URL contains handoff=app_shell&chartRecordId=<uuid>
  9   Profile dropdown loads         map_CURRENT.html           #chartProfile shows profile name (not "Loading…")
 10   Engine-birth resolves          /supabase/chart-records/   GET → 200 with birth_year/month/day/hour_utc
 11   Find regions renders           map_CURRENT.html           POST /search-regions → 200; polygons visible on map
 12   Favorite a city                map_CURRENT.html           favorite_places row created; button shows "Favorited ✓"
 13   Duplicate favorite blocked     map_CURRENT.html           Re-click → "Already in favorites."; no second row
 14   Settings save                  app_shell.html             user_settings row created/updated; values persist on reload
 15   Logout / re-login              auth.html                  Session clears; re-login restores same profile
```

### Pre-release database checks (run before step 1)

```sql
-- Confirm GeoNames dataset loaded
SELECT count(*) FROM places WHERE provider = 'geonames';
-- Expected: ~68032

-- Confirm handle_new_user trigger exists
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE trigger_name = 'on_auth_user_created';
-- Expected: one row

-- Confirm RLS enabled on key tables
SELECT tablename, rowsecurity
FROM pg_tables
WHERE tablename IN ('profiles','birth_records','favorite_places','places','user_settings')
AND schemaname = 'public';
-- Expected: rowsecurity = true for all

-- Confirm places_select policy
SELECT policyname, cmd, qual
FROM pg_policies
WHERE tablename = 'places';
-- Expected: places_select policy with qual = 'true' FOR SELECT TO authenticated
```

### Known non-blocking failures (do not fail release for these)

| Symptom | Reason | Severity |
|---|---|---|
| Angular overlays don't render | Port 8000 not running | Non-blocking — feature gated |
| Popup relocated chart fails | Port 8000 not running | Non-blocking — feature gated |
| Admin1 shows numeric codes | admin1CodesASCII.txt not used in GeoNames ingest | Display-only, non-blocking |
| Notes lost after device switch | localStorage implementation, not Supabase | Known limitation, documented |
| Comparison facts are placeholder | Backend real data not wired to compare UI | Known limitation, documented |
