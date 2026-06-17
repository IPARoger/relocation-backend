# USER FLOWS AND HANDOFFS

**Status:** Production reference  
**Last updated:** 2026-06-14  
**Purpose:** Document every major user flow as an executable sequence. Use this to eliminate handoff drift, URL shape guessing, and AI memory loss about how pages connect.  
**Scope:** Current implemented state. Deferred and unimplemented flows are explicitly marked.

---

## READING THIS DOCUMENT

Each flow is written as:

```
User action → Page → Function/Script → API/Storage → Resulting State → Next Screen
```

For every handoff between pages, the full URL shape, required params, optional params, and localStorage/sessionStorage state are documented.

---

## FLOW 1: SIGNUP (EMAIL/PASSWORD)

**Entry:** User navigates to `http://127.0.0.1:8004/auth.html`

```
User fills email + password → auth.html
  → supabase.auth.signUp({ email, password })
  → Supabase Auth: creates auth.users row
  → handle_new_user() SECURITY DEFINER trigger fires:
      INSERT accounts (id, name, account_type='personal', created_at)
      INSERT account_memberships (account_id, user_id, role='owner')
  → If email confirmation required:
      User checks email → clicks confirmation link
      → Supabase redirectTo callback
      → supabase.auth.onAuthStateChange() detects SIGNED_IN event
  → window.location.href = '/map_CURRENT.html'
```

**Resulting state:**
- `auth.users` row created
- `accounts` + `account_memberships` rows created
- Supabase session active (stored in browser localStorage by Supabase SDK)

**Next screen:** `map_CURRENT.html` (bare, no handoff params)

**Failure symptoms:**
- Stays on auth.html → check browser console for `supabase.auth` errors
- `accounts` row missing → `handle_new_user()` trigger not applied; apply migration `supabase/migrations/2026_06_13_phase6_signup_bootstrap.sql`

---

## FLOW 2: LOGIN (EMAIL/PASSWORD)

**Entry:** User navigates to `auth.html` and toggles to "Sign In"

```
User fills email + password → auth.html
  → supabase.auth.signInWithPassword({ email, password })
  → Supabase Auth: validates credentials, creates session
  → supabase.auth.onAuthStateChange() detects SIGNED_IN
  → window.location.href = '/map_CURRENT.html'
```

**Resulting state:** Supabase session restored in browser localStorage

**Next screen:** `map_CURRENT.html` (bare)

**Failure symptoms:**
- Stays on auth.html → invalid credentials or network error; check console
- Redirects then immediately bounces back to auth.html → `auth_guard.js` detecting no session; check `window.SupabaseReady`

---

## FLOW 3: EMAIL CONFIRMATION

**Entry:** User clicks confirmation link in email after signup

```
Supabase confirmation email → user clicks link
  → Supabase redirects to configured redirectTo URL (e.g., /auth.html or /map_CURRENT.html)
  → supabase.auth.onAuthStateChange() fires with event = 'SIGNED_IN'
  → auth.html: window.location.href = '/map_CURRENT.html'
```

**Note:** The exact `redirectTo` URL must be configured in Supabase Auth settings and in the `supabase.auth.signUp()` call. If absent, Supabase defaults to the site URL.

---

## FLOW 4: FIRST PROFILE INTAKE

**Precondition:** Authenticated session exists. Account has zero profiles (new signup, or profiles deleted).

**Entry:** Any navigation to `map_CURRENT.html` or `app_shell.html`

```
map_CURRENT.html or app_shell.html loads
  → supabase_store_bridge.js runs:
      → SELECT profiles WHERE account_id IN (app_account_ids())
      → Returns 0 rows
      → SupabaseStoreReady Promise rejects
  → first_profile_intake.js detects rejection
  → Intake overlay renders (full-screen modal)
  
User fills intake form:
  → Display name (text)
  → Birth date (date picker)
  → Birth time mode (exact / approximate / unknown)
  → Birth time (time picker, if exact)
  → Birth city (typeahead search against places table)
  
City search:
  → User types ≥2 chars
  → Supabase JS: SELECT places WHERE display_name ILIKE 'query%' LIMIT 8
  → Results rendered in dropdown
  → User selects a place → place UUID stored in form state
  
User clicks "Create my chart":
  → POST http://127.0.0.1:8004/profiles
      { display_name, account_id, profile_type: 'human' }
      → INSERT profiles → returns { id: <profile_uuid> }
  → POST http://127.0.0.1:8004/birth-records
      { profile_id: <uuid>, account_id, birth_date, birth_time_mode, birth_time_start, birth_place_id: <place_uuid> }
      → INSERT birth_records → returns { id: <birth_record_uuid> }
  → On success:
      window.location.href = buildIntakeHandoffUrl(profileId)
```

**Handoff URL produced:**
```
/map_CURRENT.html?skipOnboarding=1&handoff=app_shell&handoffCreatedAt=<iso>&chartRecordId=<profile_uuid>
```

**Failure symptoms:**
- City search returns no results → `places` table empty; run `scripts/ingest_cities_to_places.py`
- Birth record INSERT fails → check `birth_records` table; check for compensating profile delete in console
- Intake overlay reappears after redirect → profile created but birth record failed; OR account already has profiles but `SupabaseStoreReady` rejected for other reason (network/RLS)

---

## FLOW 5: PROFILE SELECTION

**Entry:** `map_CURRENT.html` loaded with a valid handoff URL containing `chartRecordId`

```
map_CURRENT.html loads:
  → loadChartProfiles() runs:
      → try: GET http://127.0.0.1:8000/chart-profiles (legacy, optional)
           catch → silently ignored
      → GET http://127.0.0.1:8004/profiles
           → Returns all profiles (service-role, no user scoping — see Risk R2)
           → Populates #chartProfile <select> element
  → readActiveProfileIdFromUrlOrSession() runs:
      → Reads URL param: chartRecordId
      → If absent: reads sessionStorage key rm_active_profile_id
      → If absent: selects first profile in dropdown
  → applyActiveProfileSelection() runs:
      → Sets #chartProfile.value to matched UUID
      → sessionStorage.setItem('rm_active_profile_id', <uuid>)
      → Triggers birth data resolution
```

**Manual profile switch:**
```
User selects different profile in #chartProfile dropdown
  → applyActiveProfileSelection() runs
  → sessionStorage updated
  → Birth data re-resolved
  → Polygons cleared, awaiting new Find Regions click
```

**Failure symptoms:**
- Dropdown shows "Loading…" → `GET /profiles` failed; check server running on 8004
- Wrong profile auto-selected → URL `chartRecordId` doesn't match any profile UUID in response

---

## FLOW 6: CURRENT LOCATION

**Entry:** `app_shell.html` → Account Drawer → "Set Current Location"

```
User clicks "Set Current Location" → app_shell.html
  → window.__showCurrentLocationEditor() called
  → current_location_editor.js overlay renders

User types city name:
  → Supabase JS direct: SELECT places WHERE display_name ILIKE 'query%' LIMIT 8
  → Results shown in dropdown

User selects city and clicks Save:
  → Supabase JS: UPDATE current_location_history
        SET is_current = false
        WHERE profile_id = <active_profile_id> AND account_id = <account_id>
  → Supabase JS: INSERT current_location_history
        { profile_id, account_id, place_id, is_current: true, source: 'manual', selected_at: now() }
  → Overlay closes
  → window.location.reload()
```

**After reload:** `supabase_store_bridge.js` re-reads `current_location_history` where `is_current=true` → Account Drawer shows new city name

**Failure symptoms:**
- City search empty → same as intake city search (places table or RLS issue)
- Account Drawer still shows old city → reload not triggering bridge re-read; check `current_location_history` query in bridge

---

## FLOW 7: MAP LAUNCH (from app_shell.html)

**Entry:** User navigates to "Map" screen in `app_shell.html`

```
app_shell.html screenMap():
  → buildMapHandoffUrl() constructs full handoff URL
  → <a href="<url>" target="_blank"> opens map in new tab
```

**Handoff URL shape:**
```
/map_CURRENT.html?skipOnboarding=1&handoff=app_shell&handoffCreatedAt=<iso>&chartRecordId=<uuid>[&placeId=<uuid>][&explorationId=<uuid>][&comparisonSetId=<uuid>][&returnTo=<encoded>][&genieRenderRef=<ref>]
```

**On map_CURRENT.html load:**
```
readAppShellHandoff() runs:
  → Checks URL param handoff === 'app_shell'
  → Parses all params into lastAppShellHandoff object
  → window.__rmAppShellHandoff = lastAppShellHandoff
  → chartRecordId drives applyActiveProfileSelection()
  → placeId (if present) drives map centering
```

**Genie render side-channel (when genieRenderRef is present):**
```
app_shell.html prepareGenieRenderHandoff(ctx, payload):
  → sessionStorage.setItem('rm_genie_render:<ref>', JSON.stringify(payload))
  → Adds genieRenderRef=<ref> to handoff URL

map_CURRENT.html loadGenieRenderPayloadFromHandoff(ref):
  → sessionStorage.getItem('rm_genie_render:<ref>')
  → Executes Genie render payload
```

**WARNING — new tab limitation:** sessionStorage is tab-scoped. `target="_blank"` opens a new tab that does NOT inherit sessionStorage. Genie render payload is silently absent for new-tab map opens from app_shell.

**Failure symptoms:**
- Map opens but no profile selected → `readAppShellHandoff()` not parsing `chartRecordId`; verify URL contains `handoff=app_shell`
- Intake overlay fires instead of map → user's profiles not loading; check `SupabaseStoreReady` resolution

---

## FLOW 8: FIND REGIONS

**Entry:** User has a profile selected on `map_CURRENT.html`, selects planet/house conditions, clicks "Find Regions"

```
User selects condition (e.g. Sun in house 10) → findRegions() called
  → Reads active profile UUID from #chartProfile dropdown
  → GET http://127.0.0.1:8004/supabase/chart-records/<profile_uuid>/engine-birth
      → Backend reads birth_records + places WHERE profile_id = <uuid>
      → Returns { birth_year, birth_month, birth_day, birth_hour_utc, chart_record_id }
  → POST http://127.0.0.1:8004/search-regions
      { birth params + planet/house condition + bounding box }
      → Python math engine computes GeoJSON polygon set
      → Returns FeatureCollection
  → Polygons rendered on Leaflet map as overlay layers
```

**Failure symptoms:**
- Nothing happens on click → debounce delay normal (~400ms); check Network tab after 1s
- "Birth data required" → engine-birth endpoint failed; check `/supabase/chart-records/<uuid>/engine-birth` response
- "No profile selected" → dropdown has no Supabase UUID; profile selection failed (see Flow 5)
- Status messages hidden → `setRenderStatus()` writes to `#renderStatus` which is hidden unless `?debugGeometry=true`
- `/search-regions` returns 500 → Python math engine error; check server log

---

## FLOW 9: POPUP RELOCATED CHART

**Entry:** User right-clicks a location on the map → popup opens → popup shows relocated chart data

```
map click / right-click → popup opens
  → getAspectOrbAtPoint() called:
      GET http://127.0.0.1:8000/aspect-orb-at-point?lat=...&lon=...&<birth params>
      → Returns aspect orb values for display in popup
  → fetchRelocatedChart() called:
      GET http://127.0.0.1:8000/relocated-chart?<birth params + location>
      → Returns relocated chart houses/planets for popup display
```

**STATUS: BLOCKED — Port 8000 required.** Neither endpoint is migrated to port 8004. If port 8000 is not running, popup shows no chart data and throws `TypeError: Failed to fetch`.

---

## FLOW 10: FAVORITES

**Entry:** User right-clicks a city on `map_CURRENT.html` → popup opens → "Favorite" button

```
User clicks "Favorite" button in popup:
  → resolvePlaceFromMapSelection() via RMPlaceResolution:
      → GET http://127.0.0.1:8004/places/search?q=<city_name>
          If found: returns existing place UUID
          If not found:
      → POST http://127.0.0.1:8004/places
          { display_name, canonical_name, latitude, longitude, country_code, ... }
          → INSERT places → returns { id: <place_uuid> }
  → SupabaseClient.from('favorite_places').select('id')
      .eq('profile_id', profileId).eq('place_id', placeId)
      → If row exists: shows "Already in favorites." — stops
  → SupabaseClient.from('favorite_places').insert({
        account_id, profile_id, place_id, label, rank: null
      })
  → sessionStorage.setItem('rm_recent_favorite_place_id', place.id)
  → Button changes to "Favorited ✓"
```

**Failure symptoms:**
- "Select a saved profile to favorite places." → `getActiveFavoriteProfileId()` returned null; no Supabase profile is selected
- "no_account_id" error → `window.CurrentUser` is null; auth/profile load failed
- "supabase_client_unavailable" → `window.SupabaseClient` not loaded; check script load order

---

## FLOW 11: SETTINGS

**Entry:** `app_shell.html` → "Settings" screen

```
screenSettings() renders settings form:
  → Reads window.__rmAppShell.viewModel().chartRecords for profile list
  → Reads SupabaseStore.user_settings for current values (settings_json)
  → Form displays: Default chart selector, House system selector

User changes values and clicks "Save Settings":
  → SELECT user_settings WHERE account_id = <account_id>
  → If no row: POST http://127.0.0.1:8004/user-settings
        { account_id, profile_id: null, settings_json: { default_chart_record_id, house_system } }
  → If row exists: PATCH http://127.0.0.1:8004/user-settings/<id>
        { settings_json: { default_chart_record_id, house_system } }
  → Success/error message displayed
```

**Failure symptoms:**
- Controls remain disabled → `screenSettings()` not enabling them; check branch logic in render
- Duplicate row error → unique constraint on `user_settings`; check SELECT-before-INSERT logic
- Values don't persist on reload → `supabase_store_bridge.js` not re-reading settings after save

---

## FLOW 12: NOTES

**Entry:** `app_shell.html` → chart record screen → Notes panel

```
screenChartRecord() renders notes panel:
  → localStorage.getItem('rm_note_<chartRecordId>') → pre-fills textarea

User types note and clicks "Save Note":
  → localStorage.setItem('rm_note_<chartRecordId>', <value>)
  → Success message shown
```

**WARNING:** Notes are localStorage-only. The Supabase `notes` table is not wired. Notes are lost on: browser data clear, private/incognito mode, different device, different browser.

---

## FLOW 13: HELP

**Entry:** `app_shell.html` → Account Drawer → "Help / Learn"

```
User clicks "Help / Learn" → account_drawer.js fires ad-help action
  → app_shell.html navigates to 'help' route
  → screenHelp() renders static content:
      Sections: Start Here, How to Use the Map, Beginner Path, Professional Path, Feedback
  → No API calls. No storage reads.
```

---

## FLOW 14: GUIDED ONBOARDING

**Entry:** `app_shell.html` first load after bootstrap, if onboarding not yet dismissed

```
app_shell.html bootstrap() runs → data loads → maybeShowGuidedOnboarding():
  → if localStorage.getItem('rm_guided_onboarding_dismissed') === '1': skip
  → else: render onboarding modal overlay

User clicks "Start here":
  → navigate to 'help' route
  → localStorage.setItem('rm_guided_onboarding_dismissed', '1')

User clicks "Skip":
  → localStorage.setItem('rm_guided_onboarding_dismissed', '1')
  → Modal closes
```

**After dismissal:** Modal never appears again on this browser until localStorage is cleared.

---

## FLOW 15: ACCOUNT DRAWER

**Entry:** `app_shell.html` → Account Drawer button in header

```
User clicks Account Drawer button:
  → window.__showAccountDrawer() called
  → account_drawer.js overlay renders:
      → reads window.CurrentUser: { accountId, userId, accountName, accountType, role }
      → reads window.__rmAppShell.viewModel().chartRecords for profile list
      → renders: account name, account type, list of profiles, Set Current Location button, Help/Learn link, Logout button
```

**No API calls.** Reads only already-loaded in-memory data.

---

## FLOW 16: LOGOUT

**Entry:** Account Drawer → Logout button

```
User clicks Logout:
  → window.logout() (from auth_guard.js)
  → supabase.auth.signOut()
  → Supabase session cleared from browser localStorage
  → window.location.href = '/auth.html'
```

**After logout:** Any navigation to a guarded page (`map_CURRENT.html`, `app_shell.html`) redirects back to `auth.html`.

---

## FLOW 17: SAVED INVESTIGATIONS

**STATUS: NOT WIRED.** Backend CRUD endpoints exist (`POST /saved-searches`, `GET /saved-searches/{profile_id}`). No frontend UI is wired. The `saved_searches` table and repository exist but are not exposed in any page.

---

## FLOW 18: SAVED COMPARISONS

**STATUS: PARTIAL.**

```
app_shell.html screenCompare() renders:
  → Reads SupabaseStore.comparison_sets + comparison_set_places
  → Lists comparison sets (if any exist in Supabase)
  → Fact values (e.g., "Sun in 10th", "ASC in Gemini") are PLACEHOLDER/STATIC text
  → Real comparison facts require relocated chart computation — NOT wired
```

Backend endpoints exist (`POST /comparison-sets`, `POST /comparison-sets/{id}/places`). Creating sets is possible via API but not surfaced in UI as a user-facing workflow.

---

## FLOW 19: EXPORTS

**STATUS: NOT IMPLEMENTED.** `screenExport()` function exists in `app_shell.html` as a placeholder. No export functionality (PDF, PNG, data download) is implemented.

---

## FLOW 20: GOOGLE AUTH

**STATUS: NOT WIRED.** No `signInWithOAuth({provider: 'google'})` call exists in `auth.html`.

---

## FLOW 21: APPLE AUTH

**STATUS: NOT WIRED.** The string "apple" may appear in auth.html UI but no `signInWithOAuth({provider: 'apple'})` call is implemented.

---

## HANDOFF REGISTRY

### H-1: app_shell.html → map_CURRENT.html

**Creator:** `app_shell.html buildMapHandoffUrl()` (called from `screenMap()`, `openMap()` action buttons, `prepareGenieRenderHandoff()`)

**Consumer:** `map_CURRENT.html readAppShellHandoff()`

**Activation condition:** Only active when URL contains `handoff=app_shell`

**Full URL shape:**
```
/map_CURRENT.html
  ?skipOnboarding=1
  &handoff=app_shell
  &handoffCreatedAt=<ISO 8601 timestamp>
  &chartRecordId=<profiles.id UUID>
  [&placeId=<places.id UUID>]
  [&explorationId=<UUID>]
  [&comparisonSetId=<UUID>]
  [&returnTo=<encoded: route|chartRecordId|placeId|explorationId|comparisonSetId>]
  [&genieRenderRef=<string key>]
```

| Param | Type | Required | Purpose |
|---|---|---|---|
| `handoff` | string | Yes — must equal `"app_shell"` | Activates handoff object |
| `skipOnboarding` | `"1"` | Yes | Skips map onboarding overlay |
| `handoffCreatedAt` | ISO 8601 | Yes | Timestamp for staleness checks |
| `chartRecordId` | UUID | Conditional | Profile UUID; drives birth data resolution |
| `placeId` | UUID | Optional | Pre-selected place to center map |
| `explorationId` | UUID | Optional | Resume saved exploration |
| `comparisonSetId` | UUID | Optional | Active comparison set |
| `returnTo` | encoded string | Optional | Back-navigation context |
| `genieRenderRef` | string | Optional | Key to Genie payload in sessionStorage |

**Without `handoff=app_shell`:** `lastAppShellHandoff` is null. Profile must be selected manually from dropdown.

---

### H-2: first_profile_intake.js → map_CURRENT.html

**Creator:** `first_profile_intake.js` success handler (after profile + birth record creation)

**URL shape:**
```
/map_CURRENT.html?skipOnboarding=1&handoff=app_shell&handoffCreatedAt=<ISO>&chartRecordId=<profiles.id>
```

**Note:** `chartRecordId` here is `profiles.id` (the UUID of the newly created profile). This is identical in shape to H-1. The map reads it identically.

**Failure:** If handoff URL is missing or malformed, map loads without profile context. Profile dropdown shows first available profile (may be wrong).

---

### H-3: Genie render side-channel

**Creator:** `app_shell.html prepareGenieRenderHandoff(ctx, payload)`:
```js
sessionStorage.setItem('rm_genie_render:<ref>', JSON.stringify(payload))
// genieRenderRef=<ref> added to handoff URL
```

**Consumer:** `map_CURRENT.html loadGenieRenderPayloadFromHandoff(ref)`:
```js
sessionStorage.getItem('rm_genie_render:<ref>')
```

**Constraint:** Same-tab navigation only. `target="_blank"` breaks this handoff — new tab has empty sessionStorage.

---

## STORAGE KEY REGISTRY

### localStorage Keys

| Key | Owner | Written by | Read by | Purpose |
|---|---|---|---|---|
| `rm_selected_chart_<accountId>` | app_shell.html | chart selection handler | app_shell bootstrap | Persist active chart record per account |
| `rm_guided_onboarding_dismissed` | app_shell.html | onboarding dismiss handler | `maybeShowGuidedOnboarding()` | Suppress onboarding after first dismissal |
| `rm_note_<chartRecordId>` | app_shell.html | `save-chart-note` action | `screenChartRecord()` | Per-chart note text |
| Supabase session keys | Supabase SDK | SDK auto-managed | SDK auto-managed | Auth session persistence |

### sessionStorage Keys

| Key | Owner | Written by | Read by | Purpose |
|---|---|---|---|---|
| `rm_active_profile_id` | map_CURRENT.html | `applyActiveProfileSelection()` | `readActiveProfileIdFromUrlOrSession()` | Persist active Supabase profile across reloads |
| `rm_library_active` | map_CURRENT.html (legacy) | legacy library handler | `readActiveLibraryChartIdFromUrlOrSession()` | Persist active legacy chart ID |
| `rm_map_onboarding_dismissed` | map_CURRENT.html | onboarding handler | onboarding check | Skip map-level onboarding overlay |
| `rm_recent_favorite_place_id` | map_CURRENT.html | `favoriteMapSelectionFromButton()` | (external profile page) | Highlight recently favorited place |
| `rm_genie_render:<ref>` | app_shell.html | `prepareGenieRenderHandoff()` | `loadGenieRenderPayloadFromHandoff()` | Genie render payload side-channel |
