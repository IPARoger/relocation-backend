# FEATURE STATUS BOARD

**Last updated:** 2026-06-14  
**Purpose:** Current-state reality report. A founder, engineer, QA reviewer, or AI should be able to determine the state of this product in under 5 minutes without reading any other document.

This is not an architecture document. This is not a roadmap. It contains no wishlist items and no speculation. If something is uncertain, it is marked uncertain.

---

## 1. EXECUTIVE SUMMARY

**Current phase:** Web2 backend wiring — functional core is complete, production readiness is partial.

**Overall production readiness:** Not ready for public launch. Safe for closed single-user beta.

### Biggest Risks

1. **`/profiles` returns all users' data.** The endpoint uses a service-role key with no account filter. Every user on the server sees every other user's profiles. This is a data exposure bug, not a polish issue. Must be fixed before any second user exists.

2. **Port 8000 is required for core map features.** Angular overlays (aura lines) and popup relocated charts all call `http://127.0.0.1:8000`. Port 8000 is the legacy server. If it is not running, these features silently fail. None of these endpoints are migrated to port 8004.

3. **City search is inadequate for real users.** "NYC" returns nothing. "Bombay" returns nothing. "Praha" returns nothing. The current implementation is prefix-only English canonical name matching. Recall@1 is estimated at ~60%. Users who don't type the exact canonical English city name get zero results.

4. **Comparison facts are mocked.** The comparison screen shows static placeholder text. No real astrological data is computed for comparison cities. Diffs are blocked entirely.

5. **Notes are localStorage-only.** Notes are lost on device switch, browser clear, or private mode. They are not in Supabase. This is not labeled anywhere in the UI.

### Biggest Strengths

1. Auth, profile intake, map launch, Find Regions, and favorites are fully wired end-to-end on the new Web2 stack (port 8004 + Supabase).
2. The handoff contract between `app_shell.html`, `first_profile_intake.js`, and `map_CURRENT.html` is stable and documented.
3. ~68,032 GeoNames cities are loaded in Supabase — the dataset is there, the search layer is inadequate.
4. RLS is in place on all key tables. Data is scoped by `account_id` everywhere except the `/profiles` endpoint bug.
5. The production documentation set (wiring schema, smoke tests, handoff registry, dependency matrix, acceptance checklist) is complete.

---

## 2. STATUS LEGEND

| Status | Meaning |
|---|---|
| **READY** | Wired, smoke-tested, evidence exists |
| **PARTIAL** | Functional but with known limitations that affect users |
| **BLOCKED** | Cannot function until a hard dependency is resolved |
| **MOCKED** | Placeholder or static data — no real values |
| **DEFERRED** | Not implemented; intentionally out of scope for now |

---

## 3. FEATURE STATUS TABLE

| Feature | Status | Evidence | Known Issues | Next Action |
|---|---|---|---|---|
| **Auth — Email/Password** | READY | Smoke-tested: signup → accounts row created; login → session restored; logout → guard fires | `handle_new_user()` trigger must exist in each Supabase environment | Verify trigger in production project before launch |
| **Google Auth** | DEFERRED | Not implemented | No code exists. No OAuth app configured. | Wire `signInWithOAuth({provider:'google'})` when prioritized |
| **Apple Auth** | DEFERRED | Not implemented | No code exists. Requires Apple Developer account ($99/yr). | Wire when prioritized |
| **First Profile Intake** | READY | Smoke-tested: overlay fires → city search → profile + birth record created → handoff URL correct | City search quality limits usability for non-English/non-canonical city names | No action for intake itself; city search is the gap |
| **Profile Selector** | PARTIAL | Dropdown populates from `/profiles`; active profile auto-selects from URL `chartRecordId` | `/profiles` returns ALL users' profiles (no account filter) — multi-tenant data leak | Fix `profiles_repository.py list_profiles()` to scope by authenticated user |
| **Settings** | PARTIAL | Settings save to `user_settings.settings_json`; values reload on refresh | `house_system` stored but does not drive the chart engine; setting has no functional effect | Wire `house_system` to chart engine in `map_CURRENT.html` Find Regions call |
| **Current Location** | READY | Smoke-tested: city search → `current_location_history` write → Account Drawer updates | GPS/auto-detect not implemented (manual only) | No action required |
| **Map Launch** | READY | Smoke-tested: Leaflet renders; profile dropdown populated; handoff URL consumed correctly | New-tab navigation breaks Genie sessionStorage handoff | No action required for core launch |
| **Find Regions** | READY | Smoke-tested: `POST /search-regions` → 200 → polygons on map | Status messages hidden by default (`#renderStatus` hidden unless `?debugGeometry=true`) — silent failure for users | Consider surfacing error state to user without requiring debug mode |
| **Angular Overlays** | BLOCKED | Not testable without port 8000 | `/aura-raster`, `/aura-raster-adaptive`, `/aura-field` hardcode `http://127.0.0.1:8000`. No migration. | Migrate endpoints to port 8004 |
| **Popup Relocated Chart** | BLOCKED | Not testable without port 8000 | `/relocated-chart`, `/aspect-orb-at-point` hardcode `http://127.0.0.1:8000`. No migration. | Migrate endpoints to port 8004 |
| **Favorites** | PARTIAL | Write path smoke-tested: `favorite_places` row created; duplicate check works; button state updates | Soft-delete (remove favorite) not surfaced in UI; favorites list in `app_shell.html` needs final verification | Smoke-test favorites list display in app_shell; surface soft-delete UI |
| **Notes** | PARTIAL | Notes save to localStorage per `chartRecordId`; reload on same chart | localStorage-only — lost on device switch, browser clear, private mode. Supabase `notes` table NOT wired. | Label as "local only" in UI, or wire to Supabase `notes` table |
| **Saved Investigations** | DEFERRED | Backend CRUD exists (`saved_searches` table + endpoints) | No frontend UI wired | Build save/load UI when prioritized |
| **Saved Comparisons** | PARTIAL | Comparison screen renders; `comparison_sets` table readable from bridge | Comparison creation not user-accessible; comparison facts are MOCKED | Do not advance until compare facts are real |
| **Comparison Facts** | MOCKED | Static placeholder text only | No computation occurs. `/relocated-chart` not migrated. No fact values are real. | Migrate `/relocated-chart` to port 8004, then wire to comparison screen |
| **Diffs** | BLOCKED | Not implemented | Requires real comparison facts. Comparison facts are MOCKED. | Do not implement until Comparison Facts are READY |
| **Help** | PARTIAL | Screen renders; all sections visible; no network errors | Content is static placeholder text — not final copy. Requires code change to update. | Replace placeholder copy with real help content |
| **Onboarding** | PARTIAL | Modal appears once per browser; "Skip" dismissal works; localStorage flag set | Minimal content; no multi-step walkthrough; no visual design; dismissal state is browser-local (resets on device switch) | Apply visual design; write real onboarding copy |
| **Exports** | DEFERRED | Screen exists as placeholder | No export functionality (no PDF, PNG, or data download) | Implement when prioritized |
| **City Search** | PARTIAL | Prefix search works for English canonical names; ~68,032 cities loaded | "NYC" → no results; "Bombay" → no results; "Praha" → no results; admin1 shows numeric codes. Estimated Recall@1 ~60%. | Load `alternateNamesV2.txt` into `places.alternate_names_json`; add full-text index; add abbreviation pre-processing |
| **Genie Integration** | PARTIAL | Genie infrastructure loaded in `app_shell.html` and `map_CURRENT.html`; adapter exposed on `window` | Genie is NOT the production render driver. Python engine renders polygons. Genie sessionStorage handoff breaks on new-tab navigation. | Clarify and document Genie's role; fix or document sessionStorage handoff limitation |
| **Email Styling** | DEFERRED | Supabase default templates in use | No branded email templates. Confirmation and reset emails are Supabase defaults. | Configure Supabase email templates before user launch |
| **Onboarding Styling** | DEFERRED | Minimal HTML structure | No visual design applied to onboarding modal | Apply design when onboarding content is finalized |

---

## 4. BLOCKERS REGISTER

Ordered by severity. Each blocker must be resolved before the stated condition.

---

### B-1: `/profiles` Multi-Tenant Data Leak — CRITICAL before multi-user deployment

**File:** `repositories/profiles_repository.py` → `list_profiles()`  
**Issue:** Uses service-role key with no account filter. Returns every profile in the database to every authenticated request. Any second user can see all first user's profiles.  
**Condition to resolve:** Must fix before any second user account exists on the same server.  
**Fix:** Add account-scoped filter using the authenticated user's JWT claims in `list_profiles()`.

---

### B-2: Port 8000 Legacy Endpoints — BLOCKING angular overlays and popup charts

**Files:** `map_CURRENT.html` — `renderRasterAura()`, `renderAdaptiveAuraProgressive()`, `renderAuraField()`, `fetchRelocatedChart()`, `getAspectOrbAtPoint()`  
**Issue:** Five endpoints hardcode `http://127.0.0.1:8000`. Port 8000 is a legacy server not running in the Web2 stack. Angular overlays and popup relocated charts silently fail when port 8000 is down. No user-visible error is shown.  
**Condition to resolve:** Must migrate before angular overlays or popup charts are claimed as working features.  
**Fix:** Re-implement these five endpoints in `main_centerline_FIXER.py` on port 8004.

---

### B-3: City Search Quality — BLOCKING production user launch for non-English users

**Files:** `first_profile_intake.js`, `current_location_editor.js`, `places` table  
**Issue:** Current search is `ILIKE display_name%` only. No alternate names, no transliterations, no historical names, no abbreviations. "NYC", "Bombay", "Praha", "Saigon" all return zero results. Recall@1 estimated ~60%.  
**Condition to resolve:** Must resolve before launch to any user who might not type the exact canonical English city name.  
**Fix:** Load `alternateNamesV2.txt` (GeoNames) into `places.alternate_names_json`; create full-text index; add abbreviation pre-processing. See `CITY_SEARCH_PRODUCTION_REQUIREMENTS.md` Appendix for full path.

---

### B-4: Comparison Facts Are Mocked — BLOCKING any comparison or diff feature

**Files:** `app_shell.html` → `screenCompare()`  
**Issue:** All fact values in the comparison screen are static placeholder text. No relocated chart computation occurs. Diffs are entirely unimplemented.  
**Condition to resolve:** Must resolve before comparison or diff features can be claimed as functional.  
**Fix:** Depends on B-2 (migrate `/relocated-chart` to 8004), then wire comparison cities through the chart engine.

---

### B-5: `handle_new_user()` Trigger — BLOCKING new user signup in any fresh environment

**Issue:** If the trigger `on_auth_user_created` is not present in the target Supabase project, signup succeeds at the auth level but `accounts` and `account_memberships` rows are never created. The user authenticates but the entire app fails silently thereafter.  
**Condition to resolve:** Must verify in every Supabase environment (staging, production) before any signup flow is tested.  
**Check:** `SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = 'on_auth_user_created';`

---

### B-6: Notes Not Persistent — BLOCKING any user who expects notes across devices

**Files:** `app_shell.html` → notes panel  
**Issue:** Notes are localStorage-only. No Supabase write. A user who switches devices, clears their browser, or uses private mode loses all notes.  
**Condition to resolve:** Must either: (a) wire to Supabase `notes` table, or (b) explicitly label in UI as "saved locally on this browser only."  
**Current risk:** Users assume persistence; none exists.

---

## 5. IMMEDIATE EXECUTION QUEUE

Ordered by: production impact vs effort. Smallest safe wins first.

---

**1. Fix `/profiles` user scoping** (B-1)  
One-line backend fix: add `.eq('account_id', account_id)` to `list_profiles()` using the authenticated user's claims. Zero frontend change. Eliminates the highest-severity production risk.

**2. Verify `handle_new_user()` trigger in production Supabase project** (B-5)  
One SQL query to confirm. Apply migration if absent. Must be done before any user creates an account on the production database.

**3. Label Notes as "local only" in UI** (B-6 — mitigation path)  
One-line copy change: add "Note: saved locally in this browser only" below the notes textarea. Zero backend work. Eliminates the user expectation gap immediately. Wiring to Supabase can follow later.

**4. Surface Find Regions errors to the user**  
`#renderStatus` is hidden unless `?debugGeometry=true`. A one-line CSS/JS change to show the status div (or a toast/banner) would make "Birth data required" and "No profile selected" visible to users. Currently these errors are silent.

**5. Load GeoNames `alternateNamesV2.txt` into `places.alternate_names_json`** (B-3, step 1 of 3)  
The dataset is free, already known, and the infrastructure exists. This alone adds historical names and transliterations. Requires: download file → parse → update `places` rows with alternate names JSON. No schema change required.

**6. Add full-text search index on `places` and switch from `ILIKE`** (B-3, step 2 of 3)  
After alternate names are loaded: create `tsvector` index, replace `ILIKE display_name%` with ranked full-text search. This is the single change that moves city search from ~60% Recall@1 to estimated 88–92%.

**7. Add client-side abbreviation pre-processing** (B-3, step 3 of 3)  
Small JS lookup: `NYC → New York`, `St → Saint`, `Ft → Fort`, `LA → Los Angeles`. Runs before the search query is sent. Zero backend change.

**8. Migrate `/relocated-chart` and `/aspect-orb-at-point` to port 8004** (B-2, highest-value endpoints)  
Popup relocated chart is a core differentiating feature. Start with these two endpoints before tackling the three aura endpoints.

**9. Fix `admin1` numeric codes in city search display**  
Load `admin1CodesASCII.txt` during GeoNames ingest and replace numeric admin1 values in existing rows. Pure data fix. Makes city search results human-readable ("16" → "Montenegro").

**10. Wire `house_system` setting to chart engine**  
Settings save correctly but `house_system` has no functional effect. Wire the saved value to the `house_system` parameter in `postSearchRegions()`. Small change; makes Settings a complete feature.

---

*Stop here. Everything below this line is polish, not production stability.*
