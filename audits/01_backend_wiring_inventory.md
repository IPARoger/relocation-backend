# AUDIT: 01_BACKEND_WIRING_INVENTORY

**Type:** Read-only ownership / implementation audit
**Author:** Cursor (relay trial)
**Date:** 2026-06-15
**Status:** Read-only — no code/backend/schema/data changes authorized

---

## Objective

Produce a complete inventory of backend wiring (complete / partial / missing)
across the Web2 application, organized by workflow.

---

## Files read

- `app_shell.html`
- `map_CURRENT.html`
- `supabase_store_bridge.js`
- `account_drawer.js`
- `current_location_editor.js`
- `main_centerline_FIXER.py`

---

## Method

Evidence sourced from: route declarations in `main_centerline_FIXER.py`;
frontend `.from()` / `.insert()` / `.update()` calls; `supabase_store_bridge.js`
read queries; action handlers in `app_shell.html` and `account_drawer.js`.
All findings marked as evidence (E) or inference (I).

---

## Inventory

---

### Chart Record

**Complete:**
- Read: `supabase_store_bridge.js` loads `profiles` + `birth_records` and
  assembles the full chart record view model on every app load. (E)
- Display: Chart Record page renders summary, birth data, current city, favorites,
  explorations, comparison sets, notes. (E)
- Profile create: `first_profile_intake.js` inserts `profiles` + `birth_records`
  via Supabase client. Backend also exposes `POST /profiles` + `POST /birth-records`. (E)
- Profile archive: `POST /profiles/{profile_id}/archive` exists in backend. (E)
- Profile update: `PATCH /profiles/{profile_id}` exists in backend. (E)

**Partial:**
- Birth data editing: Screen exists but is **read-only** (display only since
  `BIRTH-DATA-HONESTY-2`). Backend `PATCH /birth-record/{record_id}` is fully
  implemented and accepts `birth_date`, `birth_time_mode`, `birth_time_start`,
  `birth_place_id`, etc. Frontend save handler is absent. (E)
- Chart record notes: UI has "Save Note" button; handler writes to `localStorage`
  only (`rm_note_<id>`). No Supabase write. Notes are device-local, not
  cross-device. Backend has `POST /notes`, `PATCH /note/{id}`, `POST /note/{id}/archive`
  fully wired but unused by frontend. (E)

**Missing:**
- Birth data edit persistence: no frontend handler calling `PATCH /birth-record/{id}`. (E)
- Chart record rename/update: no frontend action for `PATCH /profiles/{id}`. (E)
- Chart record hard-delete or restore: not exposed in frontend. (I, not audited in detail)

**Recommended owner:** Chart Record screen  
**Difficulty:** Birth edit = medium (needs place resolver + timezone); notes Supabase
  wiring = small; profile rename = small.

---

### Favorites

**Complete:**
- Read: `supabase_store_bridge.js` loads `favorite_places` joined with `places`
  for lat/lon. (E)
- Create (map): `map_CURRENT.html` inserts into `favorite_places` (with
  `place_resolution.js` for place lookup/create) and into `places` if new. (E)
- Archive (shell): `archive-favorite` handler in `app_shell.html` updates
  `favorite_places.archived_at` via Supabase client. (E)
- Open on map: `open-map-favorite` builds map handoff URL with `placeId`. (E)
- View chart (Screen 4): `data-nav="chart"` with `data-place-id` navigates to
  Screen 4 with `chartRecordId + placeId`. (E)
- Backend routes exist: `GET/POST /favorite-places`, `PATCH /favorite-place/{id}`,
  `POST /favorite-place/{id}/archive`. (E)
- Map "Saved Places" sidebar: loads profile-scoped favorites into a dropdown for
  map recentering. (E)

**Partial:**
- Favorite label / rename: `favorite_places.label` is stored; frontend has no
  UI to edit the label after creation. (E)

**Missing:**
- Notes on individual favorites: no frontend UI; `favorite_places` table may
  support a notes field but it is not exposed. (I, not fully confirmed)

**Recommended owner:** Favorites module (Chart Record + map sidebar)  
**Difficulty:** Label edit = small; favorite notes = small–medium.

---

### Saved Investigations

**Complete:**
- Create: `map_CURRENT.html` `saveCurrentInvestigation()` inserts into
  `saved_searches`. (E)
- Read: `supabase_store_bridge.js` loads `saved_searches` per profile. (E)
- Resume: `app_shell.html` `resume-exploration` builds map handoff with
  `explorationId`; `map_CURRENT.html` replays the saved conditions. (E)
- Rename: `rename-exploration` handler calls `saved_searches.update({ title })`. (E)
- Archive: `archive-exploration` handler calls `saved_searches.update({ archived_at })`. (E)
- Auto-search on resume: implemented (`SAVED-INVESTIGATIONS-MVP-6`). (E)
- Backend routes: `GET/POST /saved-searches`, `PATCH /saved-search/{id}`,
  `POST /saved-search/{id}/archive`. (E)

**Partial:**
- Investigation title on save: map saves a generated title but there is no
  user-editable title prompt at save time; rename is post-hoc only. (E)

**Missing:**
- Nothing material missing for core lifecycle.

**Recommended owner:** Map + Chart Record  
**Difficulty:** Save-time title prompt = small.

---

### Comparison Sets

**Complete:**
- Create: `compare-build` action inserts into `comparison_sets` +
  `comparison_set_places` via Supabase client. (E)
- Read: `hydrateChartRecordComparisonSets` loads `comparison_sets` +
  `comparison_set_places` per profile. (E)
- Open: comparison module navigates to Compare screen with `comparisonSetId`. (E)
- Archive: `rm-cr-cmp-archive` handler updates `comparison_sets.archived_at`. (E)
- Non-destructive versioning: building a changed comparison creates a new set
  (doctrine enforced). (E)
- Backend routes: `GET/POST /comparison-sets`, `PATCH /comparison-set/{id}`,
  `POST /comparison-set/{id}/archive`, `GET/POST /comparison-set/{id}/places`,
  `DELETE /comparison-set/{id}/places/{place_id}`. (E)

**Partial:**
- Comparison title: auto-generated ("Comparison · Name · N places"), not
  user-editable. (E)
- Comparison notes: notepad textarea present on Compare screen but explicitly
  "(placeholder — not saved)"; no handler. (E)

**Missing:**
- Comparison title editing: no frontend action. (E)
- Comparison notes persistence: no write path; backend has `POST /notes` unused. (E)

**Recommended owner:** Comparison screen  
**Difficulty:** Title edit = small; notes persistence = small–medium.

---

### Screen 4 — Relocated Chart

**Complete:**
- Fetch engine-birth: `hydrateRelocatedChart` calls
  `GET /supabase/chart-records/{profile_id}/engine-birth`. (E)
- Fetch relocated facts: calls `GET /relocated-chart?lat&lon&...` and renders
  ASC/MC/DSC/IC + planet houses. (E)
- Entry from favorites: Chart Record → "View chart" passes `chartRecordId +
  placeId`. (E)
- Entry from comparison: column header click navigates to Screen 4 with context. (E)
- Blocked state: honest blocked/error states when `chartRecordId` or `placeId`
  missing or coordinates unresolvable. (E)

**Partial:**
- Notes on Screen 4: textarea "(placeholder — not saved)"; no handler. (E)
- "Favorite this place" button: disabled. (E)
- "Add to comparison": navigates to Compare screen but does not pre-select the
  current place. (E)
- Entry from map: "Back to map" button works; "Full chart (Screen 4)" in
  in-shell map action panel is present but requires `chartRecordId + placeId`
  context that the in-shell map placeholder does not provide. (E)

**Missing:**
- Screen 4 notes write path: no Supabase insert for inline notes. (E)
- "Favorite this place" from Screen 4: no handler; would need place create +
  favorite insert flow. (E)

**Recommended owner:** Screen 4 + notes owner  
**Difficulty:** Notes small–medium; favorite-from-screen-4 = medium (needs
  place resolution).

---

### Current Location

**Complete:**
- Read: `supabase_store_bridge.js` loads `current_location_history` (most recent
  `is_current=true` per profile) and resolves to display name via `places`. (E)
- Write: `current_location_editor.js` retires old current row and inserts new
  `current_location_history` row; place is looked up or created via `places`. (E)
- Entry points: Chart Record ("Set Current Location"), Profile Management
  ("Set Current Location"), Account Drawer ("Set Location") — all call
  `__showCurrentLocationEditor(profileId)`. (E)

**Partial:**
- Three duplicated entry points (Chart Record, Profile Mgmt, Account Drawer).
  Functionally equivalent but ownership ambiguous. (E)
- Current Location not yet surfaced as a pinned system row in Saved Places / map
  sidebar. (E — doctrine for this captured in
  `CURRENT_LOCATION_SAVED_PLACES_DOCTRINE.md`)

**Missing:**
- Current Location not selectable as a destination for Screen 4 or Comparison
  from the Saved Places surface. (E — deferred per doctrine)

**Recommended owner:** Profile / current-location owner  
**Difficulty:** Pinned-row surfacing = medium; Screen 4 / compare entry = small
  once pinned-row exists.

---

### Settings

**Complete:**
- Read: `saveAccountSettingsPatch` reads existing `user_settings` row and merges
  the patch. (E)
- Write (default chart record): "Save Settings" calls `saveAccountSettingsPatch`
  with `default_chart_record_id`; persists to `user_settings.settings_json`
  via Supabase. (E)
- Write (house system): same patch saves `house_system` to
  `user_settings.settings_json`. (E)
- Backend: `GET/POST/PATCH /user-settings` all wired. (E)

**Partial / Honesty gap:**
- House system saved but **never consumed by the calculation engine**.
  `main_centerline_FIXER.py` hardcodes `b'P'` (Placidus) in every `swe.houses`
  call; `/relocated-chart` accepts no house-system parameter. The saved setting
  is inert. (E — critical honesty gap)

**Missing:**
- History clear buttons: disabled placeholders (no handler, no backend route). (E)
- System location visibility toggle (Natal / Current Location show/hide):
  doctrine captured but not yet in `user_settings`. (E — deferred per doctrine)

**Recommended owner:** Settings + engine owner  
**Difficulty:** House-system engine wiring = large (requires engine param
  threading through backend routes, `swe.houses` param, and `/relocated-chart`);
  history clear = medium.

---

### Export

**Complete:**
- Nothing.

**Partial:**
- Export screen exists; generates a hash URL pointing to `https://example.com`
  (placeholder domain, not a real share link). (E)

**Missing:**
- Export map PNG: button disabled, no handler. (E)
- Share link: `POST /share-links` and `POST /share-link/{id}/revoke` exist in
  backend; frontend does not call them. (E)
- Export chart data: no handler. (E)
- AI session summary: disabled `future-only` label. (E)

**Recommended owner:** Export / share owner  
**Difficulty:** Share-link wiring = medium; PNG export = large; AI summary = out of scope.

---

### Account Drawer

**Complete:**
- Display: active profile name, current city, all profiles with city and
  default-star. (E)
- Set default: `ad-set-default` calls Supabase `user_settings` patch via
  `saveAccountSettingsPatch`. (E)
- Set location: `ad-set-location` calls `__showCurrentLocationEditor`. (E)
- Add profile: `ad-add-profile` calls `__showFirstProfileIntake`. (E)
- Logout: `ad-logout` calls `window.logout()` from auth_guard. (E)

**Partial:**
- Settings link (`ad-settings`) navigates to Settings route; correct but the
  settings screen itself has gaps (see Settings above). (E)
- Help (`ad-help`) renders a static help screen; no live content. (E)

**Missing:**
- No profile rename from drawer. (E)
- No profile archive from drawer. (E)
- No profile-level notes or metadata from drawer. (E)

**Recommended owner:** Account Drawer / Profile owner  
**Difficulty:** Profile rename/archive from drawer = small–medium.

---

### Dashboard

**Complete:**
- Displays account default chart record summary. (E)
- Lists all chart records with "Open Chart Record" links. (E)
- Lists all saved investigations across records with Resume/Rename/Archive. (E)
- "Open Map (default Chart Record)" navigates to real `map_CURRENT.html`. (E)
- Primary nav "Map" now also opens real `map_CURRENT.html` (post
  `SHELL-PLACEHOLDER-HONESTY-1`). (E)

**Partial:**
- Dashboard is a duplicate of the Profile Management list for chart records;
  both show the same records. Ownership between them is ambiguous. (E)
- "+ Add Profile" present in Dashboard, Profile Mgmt, and Account Drawer —
  same action, three entry points. (E)

**Missing:**
- Last-used / recently opened chart record: Dashboard always opens the account
  default, not last used. (E — by doctrine; acceptable placeholder behavior)

**Recommended owner:** Navigation / shell owner  
**Difficulty:** Deduplication = medium; last-used tracking = small.

---

## Cross-cutting observations

1. **Notes backend is fully wired, frontend is not.** `POST /notes`,
   `PATCH /note/{id}`, `POST /note/{id}/archive` exist. The frontend has notes
   textareas on Chart Record (localStorage only), Screen 4 (placeholder), and
   Comparison (placeholder). Connecting one or all to the backend is a medium
   task.

2. **House system is the largest honesty gap after Export.** It is saved,
   displayed, and communicated as meaningful, but the engine always uses
   Placidus. Fixing requires threading the setting through backend routes and
   `swe.houses`.

3. **Share / export is entirely placeholder.** Backend share-link routes exist
   but no frontend wiring exists.

4. **Birth data editing is the most wanted missing feature** with the largest
   usability implication. Backend is fully ready; frontend needs a save handler
   and a place-resolution step for birth city changes.

---

## Explicitly NOT done (rejected scope)

- No code changes.
- No backend / schema / data changes.
- No implementation of any gap.
- No self-selected follow-up tasks.

---

## Result

VERIFIED (read-only; no files changed)
