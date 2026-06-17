# Auth Frontend Wiring Inventory

**Date:** 2026-06-13  
**Sources:** `PHASE_6_CLOSEOUT.md`, `PROJECT_STATE_AND_NEXT_PHASE.md`, `main_centerline_FIXER.py`, `map_CURRENT.html`, `app_shell.html`, `prototype_settings_v1/v2.html`, `repositories/profiles_repository.py`, `services/supabase_client.py`, `scaffold/local_product/TEMPORARY_product_store.json`  
**Status:** Inventory only. No code changes.

---

## 1. What auth UI already exists?

**None.** There is no login screen, signup screen, session guard, or auth state UI anywhere in the product. The HTML files (`map_CURRENT.html`, `app_shell.html`, `prototype_profile_workspace_v11.html`, `prototype_settings_v1/v2.html`, `library.html`) contain no forms, modals, or routes gated on authentication. No Supabase Auth JS client (`@supabase/supabase-js`) is imported or initialized in any frontend file.

---

## 2. What signup UI exists?

**None.** No signup form, no email/password input, no OAuth button, no "Create account" route exists in any HTML or JavaScript file. The `app_shell.html` routes list (Screens 0–6) contains no auth screen. The `prototype_settings_v2.html` has a single disabled `<input type="email">` field labeled "Email" with a hardcoded placeholder (`you@example.com`) — this is a UI stub in the account section, not a functional form.

---

## 3. What login UI exists?

**None.** No login form, no email/password challenge, no OAuth redirect handler, no session-restore screen exists anywhere in the frontend. There is no `signIn`, `signInWithPassword`, or `onAuthStateChange` call in any HTML or JS file in the project.

---

## 4. What logout/session handling exists?

**None.** No `signOut()` call, no session expiry handler, no token refresh logic, and no auth state listener (`onAuthStateChange`) exists in any frontend file. The frontend has no concept of a user session.

---

## 5. What profile creation UI exists?

**Partial stub — no Supabase wiring.**

`app_shell.html` contains a birth-data intake screen (`S6 — Birth data intake`) with fields for birth date, birth time, time uncertainty range, and birth city. These fields are rendered in the HTML and labeled, but they are **not wired to any API call** — the form reads from a hardcoded in-memory JS object (`STORE`) loaded from `scaffold/local_product/TEMPORARY_product_store.json`. No `POST /profiles` call is made from the frontend.

`prototype_profile_workspace_v11.html` renders a hardcoded natal profile (`Avery Rhodes`) and has "Edit" / "+" buttons for profiles, but these are visual stubs with no backend connection.

The backend **does** have a working `POST /profiles` endpoint (`main_centerline_FIXER.py:2204`) that routes through `repositories/profiles_repository.py` → Supabase service-role key. This endpoint is functional but is not called from any frontend page.

---

## 6. What birth record/intake UI exists?

**Stub only — not wired.**

`app_shell.html` Screen S6 renders:
- Birth date: `<input type="date">`
- Birth time (exact): `<input type="time">`
- Time uncertainty range: `<input type="text">`
- Birth city: `<input type="text">`

These inputs display values read from the in-memory JS store. They are not connected to `POST /birth-records` or any other backend endpoint. No `birth_record_id` is written or persisted.

The backend has `POST /birth-records` and `PATCH /birth-record/{record_id}` endpoints fully implemented.

---

## 7. What current-location UI exists?

**None as a dedicated screen.** `map_CURRENT.html` allows the user to click a location on the Leaflet map and see a relocated chart computed on the fly via `GET /relocated-chart`. The selected location is not persisted as a `current_location_history` or `location_events` record. There is no "Set as current location" workflow or form.

---

## 8. What routes/screens are currently protected?

**None.** The FastAPI backend (`main_centerline_FIXER.py`) has no auth middleware, no JWT verification, no `Depends(get_current_user)`, and no `Authorization` header check on any endpoint. All API endpoints are public. The HTML files have no client-side route guards.

---

## 9. What data still uses localStorage?

| Storage | Key | Content | File |
|---|---|---|---|
| `localStorage` | `relocation.settings` | User preferences (house system, zodiac mode, orb defaults, overlay depth, date/time format, aspect style, texture toggle) | `prototype_settings_v1.html`, `prototype_settings_v2.html` |
| `localStorage` | `relocation.theme` | Active color theme name (`spring`, etc.) | `theme/relocation_theme.js` |
| `sessionStorage` | `rm_genie_render:{ref}` | Genie render payload for same-tab map handoff | `app_shell.html`, `map_CURRENT.html` |
| `sessionStorage` | `rm_library_active` | Active chart record ID for library → map handoff | `library.html`, `map_CURRENT.html` |
| `sessionStorage` | `rm_active_profile_id` | Active Supabase profile UUID for map → profile handoff | `map_CURRENT.html`, `prototype_profile_workspace_v11.html` |
| `sessionStorage` | `rm_recent_favorite_place_id` | Most recently favorited place ID for profile page highlight | `map_CURRENT.html`, `prototype_profile_workspace_v11.html` |
| `sessionStorage` | `rm_map_onboarding_dismissed` | One-time onboarding overlay dismiss flag | `map_CURRENT.html` |
| `sessionStorage` | `rm_fav_notes_kyoto_demo` | Demo city notes stub | `prototype_relocated_location_v1.html` |

The primary **user data** (Chart Records, birth profiles, favorites, comparison sets, notes) is stored in `scaffold/local_product/TEMPORARY_product_store.json` — a local JSON file read at server startup, not in the browser. This is explicitly labeled `TEMPORARY_LOCAL_SCAFFOLD`.

---

## 10. What is already wired to Supabase?

All Supabase connections use the **service-role key** via `services/supabase_client.py`. No publishable/anon key is present in any frontend file. The following are live and wired through the FastAPI backend:

| Endpoint | Repository | Table | Notes |
|---|---|---|---|
| `GET /health/supabase` | direct | `profiles` | Health check only |
| `GET /profiles` | `profiles_repository` | `profiles` | Lists all profiles — no auth gate, no account filter |
| `GET /profiles/{id}` | `profiles_repository` | `profiles` | No auth gate |
| `POST /profiles` | `profiles_repository` | `profiles` | Creates via `account_user_id` (legacy column) |
| `PATCH /profiles/{id}` | `profiles_repository` | `profiles` | No auth gate |
| `POST /profiles/{id}/archive` | `profiles_repository` | `profiles` | No auth gate |
| `GET /birth-records/{profile_id}` | `birth_records_repository` | `birth_records` | No auth gate |
| `POST /birth-records` | `birth_records_repository` | `birth_records` | No auth gate |
| `PATCH /birth-record/{id}` | `birth_records_repository` | `birth_records` | No auth gate |
| `GET /places`, `/places/search`, `/place/{id}` | `places_repository` | `places` | No auth gate |
| `POST /places` | `places_repository` | `places` | No auth gate |
| `GET /favorite-places/{profile_id}` | `favorite_places_repository` | `favorite_places` | No auth gate |
| `POST /favorite-places` | `favorite_places_repository` | `favorite_places` | Called from `map_CURRENT.html` via JS fetch |
| `GET /comparison-sets/{profile_id}` | `comparison_sets_repository` | `comparison_sets` | No auth gate |
| `POST /comparison-sets` | `comparison_sets_repository` | `comparison_sets` | No auth gate |
| `GET /user-settings/{account_user_id}` | `user_settings_repository` | `user_settings` | No auth gate |
| `POST /user-settings` | `user_settings_repository` | `user_settings` | No auth gate |
| `GET /notes` (implied), `POST /notes` | `notes_repository` | `notes` | No auth gate |

**Key facts:**
- Every Supabase call uses `SUPABASE_SERVICE_ROLE_KEY`, bypassing all RLS policies applied in Phases 1–5.
- The staging RLS policies are entirely bypassed in the current backend architecture.
- The `profiles` create call passes `account_user_id` (legacy column), not `account_id` — incompatible with the Phase 4 integrity lock on staging.
- `map_CURRENT.html` is the only frontend file that calls the backend API directly, using `LIBRARY_API_BASE = "http://127.0.0.1:8000"` — a localhost FastAPI server, not Supabase directly.

---

## 11. What remains to achieve the full workflow?

**Target workflow:** Signup → account auto-created → owner membership created → profile created → birth record created → map launches → logout → login → restore session/data

---

### Gap Analysis

| Step | State | What's missing |
|---|---|---|
| **Signup** | Nothing exists | Auth UI (email/password form or OAuth button), Supabase JS client initialization with anon/publishable key in frontend |
| **Account auto-created** | ✅ Backend done | `handle_new_user()` trigger is live on staging. Will fire on first real `signUp()`. No frontend gap here — it's automatic. |
| **Owner membership created** | ✅ Backend done | Same trigger. Automatic. No frontend gap. |
| **Profile created** | Backend API exists (service-role) | Frontend has no profile creation form wired to an auth session. The backend `POST /profiles` endpoint must be migrated to use the publishable key + user JWT (not service-role) so RLS governs the insert. `account_user_id` parameter must be replaced with `account_id` derived from the authenticated user's membership. |
| **Birth record created** | Backend API exists (service-role) | Same gap as profiles: must be re-wired to a user session + `account_id`. The `app_shell.html` birth intake form exists but is not connected to `POST /birth-records`. |
| **Map launches** | `map_CURRENT.html` exists and renders | The map already works with a hardcoded/static profile. The gap is passing a real authenticated `profile_id` from the user's session into the map (replacing the sessionStorage handoff with a session-aware profile selector). |
| **Logout** | Nothing exists | `supabase.auth.signOut()` call, session destruction, and redirect to login screen. |
| **Login** | Nothing exists | Auth UI for email/password (or OAuth). `supabase.auth.signInWithPassword()` or OAuth flow. Session token storage and restoration. |
| **Restore session/data** | Nothing exists | `supabase.auth.getSession()` on page load, followed by fetching profiles/favorites/comparison sets scoped to the authenticated user's `account_id` via the publishable key (not service-role). |

---

### Structural gaps that block the full workflow

1. **No Supabase JS client in the frontend.** `@supabase/supabase-js` is not imported in any HTML or JS file. The publishable/anon key is not present anywhere.

2. **Backend uses service-role key exclusively.** All 12+ repository calls go through `SUPABASE_SERVICE_ROLE_KEY`. This bypasses RLS entirely. The backend architecture must either: (a) be refactored to pass the user's JWT to Supabase, or (b) be replaced with direct Supabase JS client calls from the frontend using the anon key.

3. **No session concept on the frontend.** The frontend uses sessionStorage for same-tab handoffs between pages, not an authenticated session. There is no persistent auth state, no token, and no user identity available to any HTML page.

4. **Profile creation is incompatible with staging schema.** The current `POST /profiles` call passes `account_user_id` (a legacy column). Staging Phase 4 requires `account_id NOT NULL` on `profiles`. Any create call without a valid `account_id` tied to an `account_memberships` row will be rejected by the NOT NULL constraint and RLS policy on staging.

5. **No route protection exists.** Every screen is reachable without authentication. A session guard must be added before any screen that reads or writes user data.

6. **`chart_profiles.json` is a separate static data source.** `map_CURRENT.html` loads both hardcoded chart profiles from a local JSON file and Supabase profiles from the API. When real auth is added, only profiles belonging to the authenticated user should appear. The static profiles must be removed or gated.

---

## Summary

The frontend is a pre-auth prototype. It has working map rendering, a birth-data intake stub, a settings preferences stub, and API endpoints for profiles/birth records/favorites all wired to Supabase through a service-role key on a FastAPI server. **Zero auth UI exists.** The backend trigger for account + membership creation on signup is complete and validated on staging. Everything between the trigger and a working end-to-end session — Supabase JS client initialization, signup/login screens, JWT propagation to the backend, route protection, session restoration — remains to be built.
