# Auth Frontend Wiring Plan

**Date:** 2026-06-13  
**Sources:** `AUTH_FRONTEND_WIRING_INVENTORY.md`, `PHASE_6_CLOSEOUT.md`, `WEB2_ONBOARDING_AND_GUIDED_DISCOVERY_V2.md`  
**Status:** Planning only. No code changes.

---

## 1. Architecture Decision: Direct Supabase JS vs FastAPI JWT Pass-Through

### Recommendation: Direct Supabase JS client for all user-owned data CRUD

**Path A (recommended):** Initialize `@supabase/supabase-js` in the frontend using the publishable (anon) key. All user-owned data reads and writes — profiles, birth records, favorite places, comparison sets — go directly from the browser to Supabase. RLS policies applied in Phases 4–5 enforce authorization at the database layer. The FastAPI backend handles only compute: chart calculation (`/relocated-chart`), aura rendering (`/aura-field`, `/aura-raster`), search regions, city math. These endpoints do not read or write user-owned rows.

**Path B (not recommended for v1):** Refactor FastAPI to accept a bearer token per request, forward it to Supabase as the session JWT, and let RLS run server-side. This approach preserves the existing repository pattern but requires rewriting every repository to accept a caller-supplied JWT rather than using the service-role key, adding middleware for every route, and validating the token at the FastAPI layer. It adds two moving parts (token forwarding and FastAPI middleware) with no benefit over Path A for a single-developer v1.

**Why Path A:**
- The auth trigger and RLS policies were designed and validated to work with the anon key + JWT sessions. Path A uses them as designed.
- The FastAPI compute endpoints have no access to user-owned rows; they receive chart inputs from the frontend and return computed values. No refactoring is needed for those endpoints.
- Eliminates the service-role key from the frontend attack surface entirely. The service-role key stays server-side for admin operations only.
- Simpler session model: the Supabase JS client manages token refresh, session persistence, and `onAuthStateChange` automatically.

### Service-role endpoints to retire or restrict

The following FastAPI repository-backed endpoints currently use the service-role key and have no auth gate. They must be **retired** for user-data paths once direct Supabase JS is in place:

| Endpoint | Disposition |
|---|---|
| `GET /profiles`, `GET /profiles/{id}` | Retire. Frontend fetches direct from Supabase via anon key + RLS. |
| `POST /profiles` | Retire. Frontend inserts direct via anon key + RLS (with `account_id`). |
| `PATCH /profiles/{id}`, `POST /profiles/{id}/archive` | Retire. |
| `GET /birth-records/{profile_id}`, `POST /birth-records`, `PATCH /birth-record/{id}` | Retire. |
| `GET /favorite-places/{profile_id}`, `POST /favorite-places` | Retire. |
| `GET /comparison-sets/{profile_id}`, `POST /comparison-sets` | Retire. |
| `GET /user-settings/{account_user_id}`, `POST /user-settings` | Retire after schema update. |
| `POST /places`, `GET /places/search` | `GET /places/search` and `GET /place/{id}` can remain (read-only, no user data). `POST /places` should be restricted to server-side import scripts only. |
| `GET /health/supabase` | Retain as an internal health check. |

Compute-only endpoints (`/relocated-chart`, `/aura-field`, `/aura-raster`, `/aura-raster-adaptive`, `/aura-raster-convergence`, `/search-regions`, `/classify-points`, `/brute-force-grid`, `/screen-pixel-truth`) are **unaffected**. They accept chart inputs and return computed values; they never read or write user-owned rows.

---

## 2. Required Frontend Files / Modules

### A — Supabase client initialization module

**New file:** `supabase_client.js` (shared across all HTML pages)

Contains:
- `createClient()` with the publishable anon key and staging/production project URL.
- Exports a single `supabase` instance used by all other modules.
- Does not contain any auth logic.

The anon key is not a secret and can be embedded inline. The service-role key must not appear in any frontend file.

### B — Auth screen

**New file:** `auth.html`

Responsibilities:
- Signup form: email field, password field (min 8 chars, show/hide toggle). Single submit button calling `supabase.auth.signUp()`.
- Login form: same fields. Submit calls `supabase.auth.signInWithPassword()`.
- Toggle between signup and login without page navigation.
- "Continue with Google" button calling `supabase.auth.signInWithOAuth({ provider: 'google' })`. (Requires Google provider to be configured in the Supabase dashboard first — this is a prerequisite, not a code task.)
- "Forgot password?" link calling `supabase.auth.resetPasswordForEmail()`.
- Email confirmation holding screen (shown after email/password signup until confirmation link is clicked).
- Error handling for all cases listed in `WEB2_ONBOARDING_AND_GUIDED_DISCOVERY_V2.md` Section 1.
- On successful session: redirect to `map_CURRENT.html`.
- On page load: if a session already exists (`supabase.auth.getSession()` returns a user), redirect to `map_CURRENT.html` immediately — the auth screen is never shown to an already-authenticated user.

### C — Session guard module

**New file:** `session_guard.js`

Responsibilities:
- A single function: `requireAuth()`. Called at the top of every protected page.
- Calls `supabase.auth.getSession()`. If no session is found, redirects to `auth.html`.
- Sets up `supabase.auth.onAuthStateChange()` to handle token expiry and sign-out events anywhere in the app. On `SIGNED_OUT` event, redirect to `auth.html`.
- Does not contain any data-fetching logic.

### D — Profile and birth intake overlay

**New module:** `intake_overlay.js` (inserted into `map_CURRENT.html` or loaded as a script)

Responsibilities (per `WEB2_ONBOARDING_AND_GUIDED_DISCOVERY_V2.md` Section 2):
- Shown on map load when no complete profile + birth record exists for the authenticated user.
- Fields: display name, birth date, birth time (Exact / Approximate / Unknown), birth city (city search via `supabase.from('places').select(...)` with `ilike`), current location (optional), language selector.
- On submit: atomic insert of `profiles` row and `birth_records` row, both with correct `account_id` (derived from `app_account_ids()` RPC or direct `account_memberships` query). If either insert fails, the overlay stays open with an error. Form data is not cleared on failure.
- After successful submit: closes overlay, fires chart calculation request.
- Resume routing: on page load, if profile exists but birth record does not, show overlay with birth-data fields only. If both exist, skip overlay entirely.

### E — Map launch integration changes to `map_CURRENT.html`

Required changes (not new files):

1. Add `supabase_client.js` import and `session_guard.js` call at the top of the page's init sequence.
2. Replace the `LIBRARY_API_BASE = "http://127.0.0.1:8000"` profile-fetching call with a direct Supabase query scoped to the authenticated user's `account_id`.
3. Remove the static `chart_profiles.json` options from the profile selector when a real session is active. Only profiles belonging to the authenticated user's account are shown.
4. Attach the session `access_token` as a bearer header on the compute endpoint calls (`/relocated-chart`, `/aura-field`) so the backend can optionally log the user context (not for authorization — the compute endpoints remain public for now).
5. Wire the "Favorite" button to call `supabase.from('favorite_places').insert(...)` directly instead of `POST /favorite-places`. The `resolvePlaceFromMapSelection` function can continue calling the local FastAPI for `POST /places` (place resolution/creation) since that is a server-side operation.

---

## 3. Required Data Flow

### Signup path

```
User submits auth.html signup form
→ supabase.auth.signUp({ email, password })
→ Supabase creates auth.users row
→ handle_new_user() trigger fires (server-side, automatic)
  → accounts row inserted (name='Personal', account_type='personal')
  → account_memberships row inserted (role='owner', accepted_at=now())
→ [email/password: user confirms email]
→ [OAuth: session issued immediately]
→ Redirect to map_CURRENT.html
→ session_guard.js: session present, proceed
→ Intake overlay check: no profile → show intake overlay over live map
→ User fills intake fields, submits
→ Step 1: supabase.from('profiles').insert({ display_name, account_id, profile_type: 'human' })
→ Step 2: supabase.from('birth_records').insert({ profile_id, account_id, birth_date, birth_time_mode, birth_place_id, ... })
→ [best-effort] supabase.from('current_location_history').insert(...)
→ [best-effort] supabase.from('user_settings').insert({ language, ... })
→ Intake overlay closes
→ Chart calculation fires via /relocated-chart endpoint
→ Map renders lines
→ Guided discovery Overlay 1 activates
```

### Login / session restore path

```
User submits auth.html login form
→ supabase.auth.signInWithPassword({ email, password })
→ Session issued
→ Redirect to map_CURRENT.html
→ session_guard.js: session present, proceed
→ Intake overlay check:
    profile exists + birth record exists → skip overlay, map loads directly
    profile missing → show intake overlay
→ Profile selector populated from:
    supabase.from('profiles').select('*').eq('account_id', account_id)
    (account_id derived from supabase.auth.getUser() → app_account_ids() RPC)
→ Active profile_id passed to chart calculation
→ Favorites, comparison sets loaded on demand via direct Supabase queries
```

### account_id derivation

The frontend needs the user's `account_id` for every insert. Derivation:

```
const { data: { user } } = await supabase.auth.getUser()
const { data } = await supabase.rpc('app_account_ids')
// returns array of account UUIDs for the current user
const account_id = data[0]  // personal account is always first
```

This call is made once on page load after session confirmation and the result is held in memory for the session duration.

### Logout path

```
User triggers logout
→ supabase.auth.signOut()
→ onAuthStateChange fires SIGNED_OUT
→ session_guard.js redirects to auth.html
→ All in-memory state cleared (profile_id, account_id)
→ sessionStorage entries cleared
```

---

## 4. Required Schema Compatibility Changes

### profiles

The current `POST /profiles` repository call sets `account_user_id` (legacy) with no `account_id`. This is incompatible with the staging Phase 4 schema.

Required insert payload (from the frontend, direct Supabase JS):

```
{
  display_name:   string,
  account_id:     uuid,   ← from app_account_ids() RPC
  profile_type:   'human',
  -- account_user_id is NOT sent; it is legacy
}
```

`account_user_id` must not be populated in any new write path. It remains in the schema until the Phase 7 column drop. It must not be used as an auth identifier anywhere in new code.

### birth_records

Birth record inserts must include `account_id`:

```
{
  profile_id:      uuid,
  account_id:      uuid,   ← same value used for the parent profile insert
  birth_date:      date,
  birth_time_mode: 'exact' | 'approximate' | 'unknown',
  birth_place_id:  uuid | null,
  ...
}
```

### favorite_places

```
{
  profile_id:  uuid,
  account_id:  uuid,
  place_id:    uuid,
  label:       string
}
```

### comparison_sets

```
{
  profile_id:  uuid,
  account_id:  uuid,
  name:        string
}
```

### user_settings

The existing `GET /user-settings/{account_user_id}` endpoint uses the legacy `account_user_id` column. Any new `user_settings` writes must use `account_id`. The `account_user_id` lookup must not be used in new code.

---

## 5. Required Changes to localStorage / sessionStorage

### What can remain as UI-only state (no change needed)

| Key | Stays | Reason |
|---|---|---|
| `localStorage` `relocation.theme` | Yes | UI-only. Theme is not user-critical data. |
| `localStorage` `relocation.settings` | Temporary | Can remain for prototype_settings pages until those pages are wired to `user_settings` in Supabase. Must be migrated before production. |
| `sessionStorage` `rm_genie_render:{ref}` | Yes | Same-tab navigation payload. Not user data. |
| `sessionStorage` `rm_map_onboarding_dismissed` | Yes | One-time per-tab UI state. No persistence value. |
| `sessionStorage` `rm_fav_notes_kyoto_demo` | Remove | Demo stub. Has no function once real auth exists. |

### What must move to Supabase

| Key | Move to | Notes |
|---|---|---|
| `sessionStorage` `rm_library_active` | In-memory only, not persisted | The active chart record is determined by the session's profiles. No need to persist across sessions. |
| `sessionStorage` `rm_active_profile_id` | In-memory (session-scoped state) | Derived from the authenticated session's profile list on page load. The sessionStorage handoff is acceptable within a session but must not be the source of truth for the user identity. |
| `sessionStorage` `rm_recent_favorite_place_id` | Retain as-is | This is a cross-page highlight signal, not user data. The underlying favorite write goes to Supabase. |
| `localStorage` `relocation.settings` | `user_settings` table (account-level row) | Required before production. The settings stored here (house system, zodiac mode, orb defaults) must be the same values RLS-protected in `user_settings`. |
| Guided discovery sequence state | `user_settings` `onboarding_overlay_sequence` key | Required before production. Per `WEB2_ONBOARDING_AND_GUIDED_DISCOVERY_V2.md` Section 4, this state must persist across devices. |

---

## 6. Required Route Protection

### Screens that require authentication

| Screen / File | Protection required | Unauthenticated behavior |
|---|---|---|
| `map_CURRENT.html` | Yes — primary app | Redirect to `auth.html` |
| `library.html` | Yes | Redirect to `auth.html` |
| `app_shell.html` | Yes | Redirect to `auth.html` |
| `prototype_profile_workspace_v*.html` | Yes (once wired) | Redirect to `auth.html` |
| `prototype_settings_v*.html` | Yes (once wired) | Redirect to `auth.html` |

### Screens that do not require authentication

| Screen / File | Notes |
|---|---|
| `auth.html` | The auth screen itself. Redirects to map if already authenticated. |
| Any public share link page (future) | Renders via `get_shared_chart()` RPC. No session required. |
| Landing / marketing page (future) | Not yet built. |

### What unauthenticated users see

Any attempt to access a protected screen without a session redirects immediately to `auth.html`. There is no "view-only" mode for unauthenticated users on the main map. The redirect is performed by `session_guard.js` before any data fetch or render occurs.

---

## 7. Required Validation Tests

These tests are run in sequence on staging after implementation. All tests use the publishable key + real sessions. Service-role must not be used for any assertion.

| # | Test | Pass Criteria |
|---|---|---|
| T1 | Signup (email/password) | Auth session created. `auth.users` row exists. `accounts` row exists. `account_memberships` row with `role='owner'` and `accepted_at IS NOT NULL` exists. |
| T2 | Profile create | `profiles.insert()` succeeds with `account_id` from `app_account_ids()`. No `account_user_id` in payload. Row is readable back under the same session. |
| T3 | Birth record create | `birth_records.insert()` succeeds with `profile_id` and `account_id`. Row is readable back. |
| T4 | Map launch | Map loads and chart calculation fires using the authenticated profile's birth data. Compute endpoint returns a valid chart payload. |
| T5 | Favorite save | `favorite_places.insert()` succeeds under the anon key + session. Row is readable back under the same session. |
| T6 | Comparison save | `comparison_sets.insert()` succeeds with `account_id`. Row is readable back. |
| T7 | Logout | `supabase.auth.signOut()` called. Session destroyed. Any subsequent direct Supabase query returns RLS denial (or empty result). Redirect to `auth.html` occurs. |
| T8 | Login (returning user) | `signInWithPassword()` with same credentials. Session restored. Profiles, favorites, and comparison sets from T2/T5/T6 are recovered via direct Supabase query. |
| T9 | Session restore on reload | Page reloaded while session is active. `getSession()` returns existing session. Map loads without re-authentication. |
| T10 | Isolation: User A cannot see User B | Create User B. User A queries `profiles`, `birth_records`, `favorite_places`. All return empty (no rows from User B visible). |
| T11 | Intake overlay routing | Sign in with a new user who has no profile. Confirm overlay is shown. Submit overlay. Confirm overlay does not re-appear on next page load (profile + birth record exist). |

---

## 8. Explicit Non-Goals

The following are out of scope for this wiring phase. They must not be added during implementation:

- Notes system: `notes` table is structured and RLS-protected. UI wiring is explicitly deferred.
- Settings UI: `prototype_settings_v*.html` → `user_settings` Supabase migration is deferred.
- AI / Genie integration: no AI session, no intent translation, no prompt engineering.
- Google OAuth configuration: required as a dashboard prerequisite, but the Supabase dashboard change is a human task. OAuth button can be present in the UI but may be non-functional until the provider is enabled.
- Production database apply: staging only. Production cutover follows the documented `PRODUCTION_CUTOVER_PLAN.md` separately.
- Notes, comparison comparison detail UI, share link page rendering: all deferred.
- `profile_relationships` table: remains blocked (no `account_id`, default-deny RLS). Not touched.
- Any changes to chart rendering, aura field engine, or astrology calculation logic.
- Design changes: no layout, styling, or UX redesign. The auth screen is functional; visual polish is a separate phase.
- Road Trip Mode, Diff Mode, dignity light-ups, time slider: not in scope.

---

## Implementation Sequence

Execute in this order. Do not proceed to the next step until the current step passes its validation tests.

| Step | Deliverable | Tests |
|---|---|---|
| 1 | `supabase_client.js` — client init with staging anon key | Manual: confirm `supabase.auth.getSession()` returns null on fresh load |
| 2 | `auth.html` — signup + login forms, email/password only | T1, T7, T8, T9 |
| 3 | `session_guard.js` — requireAuth() + onAuthStateChange | Confirm map redirects to auth.html without session |
| 4 | Update `map_CURRENT.html` — add session guard, replace profile API fetch with direct Supabase query | T2 (profile load), T4 (map launch) |
| 5 | Intake overlay — profile + birth record insert with correct account_id | T2, T3, T11 |
| 6 | Favorites — replace POST /favorite-places with direct Supabase insert | T5 |
| 7 | Comparison sets — replace POST /comparison-sets with direct Supabase insert | T6 |
| 8 | Retire service-role repository endpoints for user-owned data | T10 (isolation) |
| 9 | Full T1–T11 pass | All 11 tests green |
