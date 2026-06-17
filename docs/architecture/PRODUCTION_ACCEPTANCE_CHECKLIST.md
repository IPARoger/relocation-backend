# PRODUCTION ACCEPTANCE CHECKLIST

**Status:** Founder-facing production readiness gate  
**Last updated:** 2026-06-14  
**Purpose:** Brutally clear verdict on what is production-ready and what is not. No feature may be claimed "done" without the evidence listed here.

**Rules:**
- Do not claim production-ready unless smoke evidence exists.
- Do not call placeholder UI complete.
- Do not mark Diffs complete while Compare facts are mocked.
- Do not treat city search as production-ready until CITY_SEARCH_PRODUCTION_REQUIREMENTS.md §11 acceptance tests pass.

---

## STATUS LEGEND

| Symbol | Meaning |
|---|---|
| ✅ READY | Wired, smoke-tested, evidence on record |
| ⚠️ PARTIAL | Functional but incomplete; listed limitations must be acknowledged |
| ❌ NOT READY | Blocked, mocked, or unimplemented; must not ship to users |
| 🔒 BLOCKED | Cannot proceed until a hard dependency is resolved |
| ⏸ DEFERRED | Not planned for current phase; no action required now |

---

## SECTION 1: CORE ACCOUNT / AUTH

### 1.1 Email/Password Signup

**Status:** ✅ READY  
**Required evidence before marking done:**
- [ ] `auth.users` row created in Supabase after signup
- [ ] `accounts` row created by `handle_new_user()` trigger
- [ ] `account_memberships` row created
- [ ] Browser redirects to `map_CURRENT.html` after confirmation

**Blocking defects:** None  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §1  
**Production readiness verdict:** READY — requires `handle_new_user()` trigger applied to Supabase project

---

### 1.2 Email/Password Login

**Status:** ✅ READY  
**Required evidence:** Existing session restored; browser redirects to map  
**Blocking defects:** None  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §1  
**Production readiness verdict:** READY

---

### 1.3 Session Persistence

**Status:** ✅ READY  
**Required evidence:** Map loads without auth redirect after closing and reopening tab  
**Blocking defects:** None  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §1 (session persistence steps)  
**Production readiness verdict:** READY

---

### 1.4 Logout

**Status:** ✅ READY  
**Required evidence:** Session cleared; revisiting map redirects to auth.html  
**Blocking defects:** None  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §1 (logout steps)  
**Production readiness verdict:** READY

---

### 1.5 Google Auth

**Status:** ❌ NOT READY  
**Required evidence before marking done:**
- [ ] `signInWithOAuth({provider:'google'})` wired in `auth.html`
- [ ] Google OAuth app created in Google Cloud Console
- [ ] Google provider configured in Supabase Auth Providers
- [ ] End-to-end smoke test: login → profile → map

**Known open issue:** Not implemented. No code exists.  
**Blocking defects:** Entire implementation absent  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §2 (skipped until wired)  
**Production readiness verdict:** NOT READY — DEFERRED

---

### 1.6 Apple Auth

**Status:** ❌ NOT READY  
**Required evidence before marking done:**
- [ ] `signInWithOAuth({provider:'apple'})` wired in `auth.html`
- [ ] Apple Developer account + Sign In with Apple capability configured
- [ ] Apple provider configured in Supabase Auth Providers
- [ ] End-to-end smoke test

**Known open issue:** Not implemented.  
**Blocking defects:** Entire implementation absent. Requires $99/yr Apple Developer account.  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §3 (skipped until wired)  
**Production readiness verdict:** NOT READY — DEFERRED

---

## SECTION 2: PROFILES AND BIRTH DATA

### 2.1 First Profile Intake

**Status:** ✅ READY  
**Required evidence before marking done:**
- [ ] Intake overlay fires on `map_CURRENT.html` for zero-profile account
- [ ] City search returns results for "New York"
- [ ] `profiles` row created in Supabase
- [ ] `birth_records` row created with valid `birth_place_id`
- [ ] Redirect URL shape: `map_CURRENT.html?skipOnboarding=1&handoff=app_shell&handoffCreatedAt=<iso>&chartRecordId=<uuid>`

**Known limitations:**
- City search quality is inadequate for production (prefix-only, no alternate names) — see §7.2
- One-profile intake only; multi-profile addition not surfaced after first session

**Blocking defects:** City search is inadequate but intake itself is functional for English canonical city names  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §4  
**Production readiness verdict:** READY with caveat — city search quality must be resolved before broad user launch

---

### 2.2 Profile Selector

**Status:** ⚠️ PARTIAL  
**Required evidence before marking done:**
- [ ] `#chartProfile` dropdown populated after map load
- [ ] Active profile auto-selected from URL `chartRecordId`
- [ ] sessionStorage `rm_active_profile_id` set correctly

**Known open issue:** `/profiles` endpoint returns ALL profiles (service-role, no user scoping). Multi-tenant data leak risk. Multiple users on the same server will see each other's profiles.  
**Blocking defects:** User-scoping fix required before multi-user production deployment  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §6  
**Production readiness verdict:** NOT READY for multi-user production — safe for single-user or gated beta

---

### 2.3 Birth Data → Engine Resolution

**Status:** ✅ READY  
**Required evidence:**
- [ ] `GET /supabase/chart-records/<uuid>/engine-birth` returns 200 with `{birth_year, birth_month, birth_day, birth_hour_utc}`
- [ ] Profile with `birth_time_mode='exact'` required

**Blocking defects:** Profiles with `birth_time_mode='unknown'` return 422 — engine cannot compute without time  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §8 (network tab verification)  
**Production readiness verdict:** READY for exact-time profiles

---

## SECTION 3: MAP AND CALCULATIONS

### 3.1 Map Launch

**Status:** ✅ READY  
**Required evidence:**
- [ ] Leaflet map renders
- [ ] Profile dropdown populated
- [ ] No intake overlay fires (profile exists)

**Blocking defects:** None for basic launch  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §8  
**Production readiness verdict:** READY

---

### 3.2 Find Regions (house/planet polygons)

**Status:** ✅ READY  
**Required evidence:**
- [ ] POST /search-regions returns 200 with GeoJSON
- [ ] Polygon overlays render on map

**Blocking defects:** Status messages hidden by default (`#renderStatus` hidden unless `?debugGeometry=true`) — silent failure mode for users  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §9  
**Production readiness verdict:** READY (with noted silent failure risk)

---

### 3.3 Angular Overlays (aura/aspect lines)

**Status:** 🔒 BLOCKED  
**Required evidence before marking done:**
- [ ] `/aura-raster`, `/aura-raster-adaptive`, `/aura-field` migrated to port 8004
- [ ] Overlay renders with port 8004 server only

**Known open issue:** All three endpoints hardcode `http://127.0.0.1:8000`. Port 8000 must be running. No migration scheduled.  
**Blocking defects:** Port 8000 dependency not resolved  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §10  
**Production readiness verdict:** NOT READY — BLOCKED on port 8000

---

### 3.4 Popup Relocated Chart

**Status:** 🔒 BLOCKED  
**Required evidence before marking done:**
- [ ] `/relocated-chart` migrated to port 8004
- [ ] `/aspect-orb-at-point` migrated to port 8004
- [ ] Popup shows real relocated chart data

**Known open issue:** Both endpoints hardcode `http://127.0.0.1:8000`. Not migrated.  
**Blocking defects:** Port 8000 dependency not resolved  
**Smoke test:** None (blocked)  
**Production readiness verdict:** NOT READY — BLOCKED on port 8000

---

### 3.5 Old Controller Still Active

**Known open issue:** The `LIBRARY_API_BASE = "http://127.0.0.1:8000"` variable remains in `map_CURRENT.html`. Library-related endpoints (chart-profiles, library/state, library/views) still attempt port 8000. These are guarded with try/catch but represent technical debt and a potential confusion source.  
**Required action:** Remove or replace LIBRARY_API_BASE references as part of port 8000 migration.  
**Current verdict:** Non-blocking for core flows; blocking for library features.

---

### 3.6 Genie Not Integrated into Production Map

**Known open issue:** Genie variable builder infrastructure is loaded but is NOT the production polygon render driver. The map renders via Python engine. Genie sessionStorage handoff breaks on new-tab navigation.  
**Required evidence before claiming Genie is production-integrated:**
- [ ] Genie drives the production render path OR is clearly marked as Layer 2 only
- [ ] sessionStorage handoff failure documented and handled

**Current verdict:** PARTIAL infrastructure; not production-integrated.

---

## SECTION 4: SAVED USER DATA

### 4.1 Favorites

**Status:** ⚠️ PARTIAL  
**Required evidence before marking done:**
- [ ] Favorite button writes to `favorite_places` table
- [ ] Duplicate click prevented (no second row)
- [ ] Favorites list appears in `app_shell.html` chart record screen
- [ ] Soft-delete (archived_at) surfaced in UI

**Known open issue:** Favorites list display in `app_shell.html` needs final smoke verification. Soft-delete UI not implemented.  
**Blocking defects:** None for core write path  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §11  
**Production readiness verdict:** PARTIAL — write path READY; list management (ordering, delete) DEFERRED

---

### 4.2 Notes

**Status:** ⚠️ PARTIAL  
**Required evidence before marking done:**
- [ ] Note saves to localStorage per `chartRecordId`
- [ ] Note reloads on same chart record

**Known open issue:** localStorage-only. Notes are lost on device switch, browser clear, private mode. Supabase `notes` table not wired.  
**Blocking defects:** Not a persistent feature in current state  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §14  
**Production readiness verdict:** NOT READY for production — must be clearly labeled as "local only" or migrated to Supabase before launch

---

### 4.3 Saved Investigations

**Status:** ❌ NOT READY  
**Required evidence before marking done:**
- [ ] UI to save a map investigation state
- [ ] `saved_searches` row created in Supabase
- [ ] Saved investigation can be loaded/resumed

**Known open issue:** No frontend UI wired. Backend ready.  
**Blocking defects:** Entire frontend implementation absent  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §12 (skipped)  
**Production readiness verdict:** NOT READY — DEFERRED

---

### 4.4 Saved Comparisons

**Status:** ⚠️ PARTIAL  
**Required evidence before marking done:**
- [ ] User can create a comparison set with real city choices
- [ ] Comparison facts show real astrological data (not placeholder)
- [ ] Diffs show real differences between city charts

**Known open issue:** Comparison facts are placeholder/static text. Creating comparison sets is not surfaced as a user action. Diffs not implemented.  
**Blocking defects:** Compare facts are MOCKED. Diffs are BLOCKED.  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §13  
**Production readiness verdict:** NOT READY — comparison screen is a shell; no real data flows through it

---

### 4.5 Compare Facts

**Status:** ❌ MOCKED  
**Known open issue:** All comparison fact values in the UI are static placeholder text. Zero real computation occurs.  
**Required evidence before marking done:**
- [ ] `/relocated-chart` endpoint migrated to 8004 (unblocks port 8000 dependency)
- [ ] Each comparison city triggers a real chart calculation
- [ ] Fact values are computed house/planet placements, not static text
**Production readiness verdict:** NOT READY — must not claim done until real values replace placeholder

---

### 4.6 Diffs

**Status:** 🔒 BLOCKED  
**Known open issue:** Diffs are blocked until comparison facts are real. Cannot compute "how does my chart change" if the underlying facts are placeholder.  
**Production readiness verdict:** NOT READY — do not implement diffs until §4.5 is READY

---

## SECTION 5: SETTINGS

### 5.1 Settings Save/Load

**Status:** ⚠️ PARTIAL  
**Required evidence before marking done:**
- [ ] Settings save to `user_settings.settings_json`
- [ ] Settings reload on page refresh
- [ ] `default_chart_record_id` drives default profile selection in map
- [ ] `house_system` drives chart engine house system selection

**Known open issue:** Settings save correctly, but `house_system` does not currently affect the chart engine in `map_CURRENT.html`. The setting is stored but has no effect on output.  
**Blocking defects:** `house_system` has no effect on calculations — incomplete  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §15  
**Production readiness verdict:** PARTIAL — save/load works; functional effect incomplete

---

## SECTION 6: HELP AND ONBOARDING

### 6.1 Help Page

**Status:** ⚠️ PARTIAL  
**Required evidence before marking done:**
- [ ] Help screen renders without error
- [ ] All sections visible

**Known open issue:** Help page content is static placeholder text. Not production copy. Cannot be updated without a code change.  
**Blocking defects:** None for rendering; content is incomplete  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §17  
**Production readiness verdict:** NOT READY for production — requires real copy and potentially a CMS or editable content layer

---

### 6.2 Guided Onboarding Overlay

**Status:** ⚠️ PARTIAL  
**Required evidence before marking done:**
- [ ] Modal appears on first load (no dismissal flag)
- [ ] "Start here" navigates to help
- [ ] "Skip" closes modal and sets localStorage flag
- [ ] Modal does not reappear after dismissal

**Known open issues:**
- Onboarding overlay is minimal — one modal, two buttons, no multi-step walkthrough
- Onboarding styling absent (no visual design)
- Dismissal is localStorage-only (not per-account — resets on browser/device switch)

**Blocking defects:** None for basic functionality; polish and real content absent  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §18  
**Production readiness verdict:** NOT READY for production as a compelling first-time experience

---

## SECTION 7: SEARCH AND PLACES

### 7.1 City Search — Functional

**Status:** ⚠️ PARTIAL  
**Required evidence:**
- [ ] Prefix search returns results for English canonical city names
- [ ] ~68,032 places loaded in Supabase

**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §5  
**Production readiness verdict:** FUNCTIONAL for basic English prefix queries

---

### 7.2 City Search — Production Quality

**Status:** ❌ NOT READY  
**Required evidence before marking production-ready (from CITY_SEARCH_PRODUCTION_REQUIREMENTS.md §11):**
- [ ] Recall@1 ≥ 85% on required test set
- [ ] Recall@5 ≥ 97% on required test set
- [ ] "Bombay" → Mumbai passes
- [ ] "NYC" → New York City passes
- [ ] "Praha" → Prague passes
- [ ] Response time ≤ 300ms at p95
- [ ] `alternate_names_json` loaded from GeoNames `alternateNamesV2.txt`
- [ ] Full-text search index created
- [ ] `admin1` full names loaded (not numeric codes)

**Known open issues:**
- "New York" returns results; "New York City" may not (the "New York City vs New York" disambiguation symptom)
- "NYC" → no results (no abbreviation normalization)
- "Bombay" → no results (no historical name support)
- "Praha" → no results (no transliteration support)
- Admin1 shows numeric codes ("16") not region names

**Blocking defects:** Entire alternate names layer missing  
**Production readiness verdict:** NOT READY — current implementation is a development placeholder, not production search

---

## SECTION 8: COMPARISON AND DIFFS

### Summary Verdict

❌ COMPARISON IS NOT PRODUCTION-READY IN ANY DIMENSION

- Comparison sets: list renders, creation not surfaced
- Comparison facts: MOCKED (placeholder text)
- Diffs: BLOCKED (requires real comparison facts)

Do not claim any comparison or diff feature complete until real astrological fact values are computed and displayed.

---

## SECTION 9: EXPORT AND SHARING

### 9.1 Exports

**Status:** ❌ NOT READY  
**Known open issue:** Export screen is a placeholder. No PDF, PNG, or data download implemented.  
**Smoke test:** OPERATIONAL_SMOKE_TESTS.md §16 (skipped)  
**Production readiness verdict:** NOT READY — DEFERRED

---

### 9.2 Share Links

**Status:** ❌ NOT READY  
**Known open issue:** Backend `share_links` table and CRUD endpoints exist. No frontend UI wired.  
**Production readiness verdict:** NOT READY — DEFERRED

---

## SECTION 10: STYLING AND UX

### 10.1 Email Styling

**Status:** ❌ NOT READY  
**Known open issue:** Supabase default email templates in use. Confirmation emails, password reset emails have no branding.  
**Production readiness verdict:** NOT READY — requires Supabase email template customization before user launch

---

### 10.2 Onboarding Styling

**Status:** ❌ NOT READY  
**Known open issue:** Onboarding modal has no visual design — minimal HTML structure only. Not a compelling first-time experience.  
**Production readiness verdict:** NOT READY

---

## SECTION 11: PRODUCTION OPERATIONS

### 11.1 Server Startup

**Status:** ⚠️ PARTIAL  
**Required procedure:**
```bash
cd /path/to/relocation-backend
set -a && source .env.staging && set +a
venv/bin/uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8004 --reload
```

**Known open issue:** `services/supabase_client.py` calls `load_dotenv()` without explicit path. If server started from wrong directory or `.env` absent, backend silently connects to wrong/no Supabase project.  
**Production readiness verdict:** PARTIAL — manual startup works; no process manager (systemd, supervisor, etc.) configured

---

### 11.2 `/profiles` Service-Role All-Profile Leak Risk

**Status:** ❌ CRITICAL RISK before multi-user production  
**Known open issue:** `GET /profiles` uses service-role key with no account filter. All users' profiles are returned to all users who call this endpoint. This is a multi-tenant data exposure.  
**Required fix:** Add `account_id` filter to `repositories/profiles_repository.py list_profiles()` using the authenticated user's JWT claims.  
**Production readiness verdict:** NOT SAFE for multi-user production deployment

---

### 11.3 Port 8000 Legacy Dependencies

**Status:** 🔒 PARTIAL BLOCKER  
**Known open issues:**
- Angular overlays: `aura-raster`, `aura-raster-adaptive`, `aura-field` → port 8000
- Popup relocated chart: `relocated-chart`, `aspect-orb-at-point` → port 8000
- Screen pixel truth (debug): `screen-pixel-truth` → port 8000

These features are silently unavailable if port 8000 is down. No user-visible error is shown for aura failures.

**Production readiness verdict:** These features are NOT available without port 8000. Must migrate to 8004 before they can be considered production-ready.

---

### 11.4 `handle_new_user()` Trigger

**Status:** ✅ REQUIRED — must verify in each environment  
**Check:** 
```sql
SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = 'on_auth_user_created';
```
If absent: apply migration `supabase/migrations/2026_06_13_phase6_signup_bootstrap.sql`

---

### 11.5 GeoNames Dataset in `places` Table

**Status:** ✅ REQUIRED — must verify before any launch  
**Check:**
```sql
SELECT count(*) FROM places WHERE provider = 'geonames';
-- Expected: ~68032
```
If 0: run `scripts/ingest_cities_to_places.py` with `.env.staging` sourced.

---

## SECTION 12: AI / LAYER 2 QUARANTINE

### 12.1 AI Output Quarantine

**Status:** ✅ QUARANTINE MAINTAINED  
**Rule:** AI-generated interpretation (Layer 2) is not wired to any production data, not stored in Supabase, not a source of truth for chart calculations, and not the driver of the production polygon render.

**Required evidence before any AI output reaches production users:**
- [ ] AI output clearly labeled as interpretation, not calculation
- [ ] AI output sourced from real chart engine data (not placeholder)
- [ ] AI output reviewed against product doctrine

**Production readiness verdict:** Layer 2 is NOT in production. Quarantine maintained.

---

## OVERALL PRODUCTION READINESS SUMMARY

| Section | Verdict |
|---|---|
| Email/password auth | ✅ READY |
| Google/Apple auth | ❌ NOT READY |
| First profile intake | ✅ READY (city search caveat) |
| Profile selector | ⚠️ NOT SAFE for multi-user |
| Birth data → engine | ✅ READY |
| Map launch | ✅ READY |
| Find Regions | ✅ READY |
| Angular overlays | 🔒 BLOCKED (port 8000) |
| Popup relocated chart | 🔒 BLOCKED (port 8000) |
| Favorites | ⚠️ PARTIAL |
| Notes | ⚠️ LOCAL ONLY |
| Saved investigations | ❌ NOT READY |
| Saved comparisons | ❌ NOT READY |
| Compare facts | ❌ MOCKED |
| Diffs | 🔒 BLOCKED |
| Settings | ⚠️ PARTIAL |
| Help | ⚠️ PLACEHOLDER CONTENT |
| Guided onboarding | ⚠️ MINIMAL |
| City search quality | ❌ NOT PRODUCTION-READY |
| Email styling | ❌ NOT READY |
| Onboarding styling | ❌ NOT READY |
| `/profiles` user scoping | ❌ CRITICAL RISK |
| Port 8000 migration | 🔒 BLOCKING AURA/POPUP |
| AI / Layer 2 | ✅ QUARANTINED |

---

**Minimum production gate (must all be ✅ before first real-user launch):**

1. `handle_new_user()` trigger verified in production Supabase
2. GeoNames `places` dataset loaded (~68,032 rows)
3. `/profiles` endpoint scoped to authenticated user's account
4. Pre-release smoke suite (OPERATIONAL_SMOKE_TESTS.md) passed in full
5. City search quality acknowledged and labeled (or fixed to §11 criteria)
6. Email templates styled (or explicitly deferred with user communication)
7. Port 8000 dependencies documented for any aura/popup features claimed as available
