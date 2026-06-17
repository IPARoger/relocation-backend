# ROADMAP AND SEQUENCE

**Last updated:** 2026-06-14  
**Purpose:** Official implementation order for the project. Future AI systems must not invent priorities. They must follow this sequence unless the founder explicitly changes it and updates this document.

This document represents execution discipline, not aspiration. Every item is grounded in current system state. No item is included because it sounds good — every item is included because it is the correct next thing given what exists.

---

## SECTION 1: CURRENT POSITION

### What is actually working today

The following is confirmed working and smoke-tested:

| Feature | State |
|---|---|
| Email/password auth (signup, login, logout, session) | Working |
| Account + membership bootstrap via `handle_new_user()` | Working |
| First profile intake (city search → profile → birth record → handoff) | Working |
| App_shell → map handoff contract (URL shape, chartRecordId) | Working |
| Profile dropdown in map (loads from `/profiles` on port 8004) | Working |
| Birth data resolution (`/supabase/chart-records/{id}/engine-birth`) | Working |
| Find Regions (POST `/search-regions` → GeoJSON polygons on Leaflet) | Working |
| Favorites write path (Supabase JS direct, duplicate check) | Working |
| Current location set/edit (account drawer → Supabase write) | Working |
| Settings save/load (`user_settings.settings_json`) | Working (save works; house_system has no functional effect yet) |
| Notes (localStorage per chartRecordId) | Working (non-persistent, local only) |
| Help screen | Working (static placeholder content) |
| Guided onboarding modal | Working (minimal content, localStorage dismissal) |
| Account drawer | Working |
| ~68,032 GeoNames cities in `places` table | In place |

### What is partially working

| Feature | Gap |
|---|---|
| Settings | `house_system` stored but not wired to chart engine |
| Favorites | Soft-delete not in UI; list display in app_shell needs final verification |
| Notes | localStorage only — lost on device switch or browser clear |
| Help | Static placeholder text — not final copy |
| Onboarding | Minimal modal — no walkthrough, no visual design |
| City search | Prefix-only on canonical English names; "NYC", "Bombay", "Praha" return nothing |
| Profile selector | `/profiles` has no user scoping — multi-tenant data leak risk |
| Comparison screen | Renders; comparison facts are mocked placeholder text |
| Genie | Infrastructure loaded; not the production render driver |

### What is blocked or absent

| Feature | Blocker |
|---|---|
| Angular overlays (aura) | Port 8000 required; not migrated |
| Popup relocated chart | Port 8000 required; not migrated |
| Diffs | Comparison facts must be real first |
| Saved investigations | No frontend UI wired |
| Google / Apple auth | Not implemented |
| Exports | Not implemented |
| Email styling | Supabase default templates in use |

---

## SECTION 2: IMMEDIATE PRODUCTION TRACK

This is the official implementation sequence. Do not skip steps. Do not reorder without amending this document.

---

### TRACK 0 — PRODUCTION SAFETY (do these before any new feature)

**These are not features. They are production bugs. They must be fixed before any user other than the founder touches the system.**

---

#### T0-1: Fix `/profiles` user scoping
**File:** `repositories/profiles_repository.py` → `list_profiles()`  
**Change:** Add account filter using authenticated user's JWT claims  
**Why now:** Multi-tenant data leak. Any second user sees all other users' profiles. This is the highest-severity open defect.  
**Validation:** Two test accounts on the same server — each sees only their own profiles  
**Effort:** Small (single function change)

---

#### T0-2: Verify `handle_new_user()` trigger in every Supabase environment
**Check:** `SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = 'on_auth_user_created';`  
**Why now:** If this trigger is missing, signup succeeds but the entire app fails silently. Must be confirmed before any new user attempts signup.  
**Effort:** One SQL query; apply migration if absent

---

### TRACK 1 — COMPLETE THE CORE SHELL (settings → favorites → notes → port 8000)

These are the features users will use immediately after the map works. They must be complete and honest before any expansion.

---

#### Step 1: Settings — wire `house_system` to chart engine
**File:** `map_CURRENT.html` → `postSearchRegions()` or Find Regions call  
**Change:** Read `user_settings.settings_json.house_system` and pass it to `/search-regions` payload  
**Why now:** Settings save correctly but have no functional effect. A settings feature that does nothing is misleading.  
**Validation:** Set house system to "Whole Sign" → Find Regions → verify different polygon output vs Placidus  
**Effort:** Small (add one field to the search-regions payload; verify backend accepts it)

---

#### Step 2: Favorites — complete list display and add soft-delete UI
**Files:** `app_shell.html` (chart record screen, favorites list), possibly `supabase_store_bridge.js`  
**Change:** (a) Smoke-test that favorited cities appear in app_shell favorites list. (b) Add "Remove" action that sets `archived_at` on `favorite_places` row.  
**Why now:** Favorites write path is confirmed but the user has no way to see or remove their favorites. The feature is half-built.  
**Validation:** Favorite a city → view in app_shell → remove → confirm row has `archived_at` set  
**Effort:** Small to medium

---

#### Step 3: Notes — migrate to Supabase `notes` table
**Files:** `app_shell.html` (save-chart-note action, screenChartRecord render), backend `GET /notes/{profile_id}`, `POST /notes`  
**Change:** Replace `localStorage.setItem/getItem` with Supabase reads/writes through the existing backend endpoints. Keep localStorage as a fallback for unauthenticated state if needed.  
**Why now:** Notes are currently lost on device switch. This is a trust failure for any user who writes notes.  
**Validation:** Write a note → switch device or clear browser → note still present  
**Effort:** Medium (swap two localStorage calls for two API calls; verify backend endpoint works)

---

#### Step 4: Port 8000 migration — `/relocated-chart` and `/aspect-orb-at-point`
**Files:** `main_centerline_FIXER.py` (add endpoints), `map_CURRENT.html` (change URLs from 8000 to 8004)  
**Change:** Re-implement `/relocated-chart` and `/aspect-orb-at-point` in FastAPI on port 8004. These are the endpoints behind popup relocated charts.  
**Why now:** Popup relocated charts are a core product feature. They are silently broken whenever port 8000 is down. Angular overlays also depend on port 8000 but are lower priority than popup charts.  
**Validation:** Open popup on map → confirm relocated chart data shows without port 8000 running  
**Effort:** Medium (depends on how much logic lives in the legacy endpoint handlers)

---

#### Step 5: Port 8000 migration — aura/angular overlay endpoints
**Files:** `main_centerline_FIXER.py` (add endpoints), `map_CURRENT.html` (change URLs)  
**Change:** Re-implement `/aura-raster`, `/aura-raster-adaptive`, `/aura-field` on port 8004.  
**Why now:** Angular overlays silently fail without port 8000. No user-visible error is shown.  
**Validation:** Select an aspect condition → Find Regions → angular overlay renders without port 8000 running  
**Effort:** Medium to large (depends on complexity of aura computation)

---

### TRACK 2 — SAVED USER DATA (investigations → comparisons → compare facts → diffs)

Do not start Track 2 until Track 1 is complete. Compare Facts depend on Step 4 (relocated-chart).

---

#### Step 6: Saved Investigations — wire frontend UI
**Files:** `app_shell.html` (save investigation UI, list screen), `map_CURRENT.html` (save current map state action)  
**Backend:** `POST /saved-searches`, `GET /saved-searches/{profile_id}` already exist  
**Change:** Add a "Save this investigation" action to the map that captures: profile UUID, condition parameters, settings snapshot, viewport bounds. Wire a list view in app_shell that loads and resumes investigations.  
**Why now:** Backend is ready. This is a high-value user feature with no technical blocker.  
**Validation:** Save an investigation → reload page → load investigation → same conditions reproduced  
**Effort:** Medium (UI wiring; semantic state capture; replay logic)

---

#### Step 7: Saved Comparisons — wire creation UI
**Files:** `app_shell.html` (comparison creation, comparison set management)  
**Backend:** `POST /comparison-sets`, `POST /comparison-sets/{id}/places` already exist  
**Change:** Add UI to create a comparison set and add cities to it. This is the structure step — compare facts come later.  
**Why now:** The structure must exist before facts can be computed. Also unlocks the user-visible comparison screen as a real feature rather than a placeholder.  
**Validation:** Create a comparison set with 2 cities → cities appear in comparison screen  
**Effort:** Medium

---

#### Step 8: Compare Facts — wire real relocated chart data to comparison screen
**Dependency:** Step 4 (relocated-chart on port 8004) must be complete  
**Files:** `app_shell.html` (screenCompare rendering), chart engine calls per comparison city  
**Change:** For each comparison city in a comparison set, call the chart engine with that city's coordinates + active profile birth data → populate real house/planet placements in the comparison display.  
**Why now:** Without this, the comparison screen is mocked. Do not claim comparisons work until this is done.  
**Validation:** Create comparison set with 2 real cities → both show real planet/house placements (not placeholder text)  
**Effort:** Large (requires coordinating multiple engine calls and rendering results)

---

#### Step 9: Diffs
**Dependency:** Step 8 (Compare Facts) must be complete and REAL  
**Files:** `app_shell.html` (diff rendering), comparison engine  
**Change:** Show what changes between two comparison cities — which planets change house, which angles change sign, etc.  
**Why now:** Do not implement diffs until comparison facts are real. A diff over placeholder data is meaningless and misleading.  
**Validation:** Two cities with real facts → diff shows changed conditions  
**Effort:** Medium (given real facts exist)

---

### TRACK 3 — SEARCH QUALITY

City search quality is independent and can be worked in parallel with Track 2 if resources allow. But it must be complete before public beta.

---

#### Step 10: City Search — load alternate names
**Files:** `scripts/ingest_cities_to_places.py` (extend to load alternateNamesV2.txt), `places` table  
**Change:** Download `alternateNamesV2.zip` from GeoNames. For each `geonames_id` in `places`, collect alternate name rows and store in `places.alternate_names_json`.  
**Why now:** This is the foundation of production city search. Without it, historical names, transliterations, and non-English inputs return zero results.  
**Validation:** "Bombay" → Mumbai appears; "Moskva" → Moscow appears; "Leningrad" → Saint Petersburg appears  
**Effort:** Medium (data pipeline work; no schema change required)

---

#### Step 11: City Search — full-text index and ranked search
**Files:** `main_centerline_FIXER.py` or a separate search service, `places` table (add `tsvector` index)  
**Change:** Create a PostgreSQL full-text index on `display_name || canonical_name || alternate_names_text`. Replace `ILIKE display_name%` with `to_tsquery` ranked search weighted by `importance_rank`.  
**Why now:** Alternate names are useless without a search layer that uses them. This is the step that actually enables "Praha → Prague".  
**Validation:** Run Recall@1 test set from `CITY_SEARCH_PRODUCTION_REQUIREMENTS.md §9.3` — must achieve ≥85% Recall@1  
**Effort:** Medium

---

#### Step 12: City Search — client-side abbreviation normalization
**Files:** `first_profile_intake.js`, `current_location_editor.js`  
**Change:** Before sending the query to the backend, apply a small lookup: `NYC → New York`, `LA → Los Angeles`, `SF → San Francisco`, `DC → Washington`, `St → Saint`, `Ft → Fort`, `Mt → Mount`.  
**Why now:** These common abbreviations will never match canonical names even with full-text search. Client-side pre-processing is the correct lightweight solution.  
**Validation:** "NYC" → New York City; "St Louis" → Saint Louis; "Ft Worth" → Fort Worth  
**Effort:** Very small (a JS lookup table and one pre-processing step)

---

### TRACK 4 — CONTENT AND UX POLISH

Do not start Track 4 before Track 1 is substantially complete. Content and polish on a broken foundation is wasted effort.

---

#### Step 13: Help content — replace placeholder copy
**Files:** `app_shell.html` `screenHelp()`  
**Change:** Replace placeholder sections ("Start Here", "How to Use the Map", etc.) with real, reviewed copy.  
**Why now:** Help is visible to every user. Placeholder copy signals an unfinished product.  
**Effort:** Content work (no code complexity)

---

#### Step 14: Onboarding — real content and multi-step flow
**Files:** `app_shell.html` (onboarding modal), possibly a dedicated `onboarding.js`  
**Change:** Replace the single modal with a genuine first-time experience: 2–3 steps, real copy, visual design applied. Move dismissal flag to Supabase (per-account) rather than localStorage.  
**Why now:** The current onboarding is a thin placeholder. It is the first thing new users see.  
**Validation:** New account → onboarding appears → user completes steps → dismissal persists across devices  
**Effort:** Medium

---

#### Step 15: Email styling — configure Supabase email templates
**Platform:** Supabase dashboard → Auth → Email Templates  
**Change:** Replace default Supabase email templates (confirmation, password reset) with branded, styled templates.  
**Why now:** Every signup sees the confirmation email. Default Supabase templates undermine trust.  
**Effort:** Small (template configuration, not code)

---

### TRACK 5 — AUTH EXPANSION

Do not start Track 5 until the core shell (Tracks 0–1) is stable and smoke-tested.

---

#### Step 16: Google Auth
**Files:** `auth.html`, Supabase Auth Providers configuration  
**Change:** Add Google OAuth button; wire `supabase.auth.signInWithOAuth({provider:'google'})`; configure Google Cloud Console OAuth app.  
**Why now:** Required for public launch. Many users prefer OAuth over email/password.  
**Validation:** Google login → accounts row created → profile intake fires → map loads  
**Effort:** Medium (OAuth app setup + auth.html changes)

---

#### Step 17: Apple Auth
**Files:** `auth.html`, Supabase Auth Providers configuration, Apple Developer account  
**Change:** Add Apple Sign In button; wire OAuth flow.  
**Why now:** Required for App Store compliance if iOS app is planned. Secondary priority to Google.  
**Validation:** Apple login → full flow through to map  
**Effort:** Medium plus Apple Developer account requirement

---

### TRACK 6 — GENIE INTEGRATION

Genie integration is deferred until core data flows are stable. The infrastructure is in place.

---

#### Step 18: Genie production integration
**Files:** `map_CURRENT.html` (render pipeline), `app_shell.html` (Genie payload handoff), sessionStorage handoff fix  
**Change:** (a) Fix sessionStorage handoff for new-tab navigation — replace with Supabase-stored short-TTL payload. (b) Define whether Genie drives the production render path or remains a Layer 2 overlay. (c) Document the integration point formally.  
**Why now:** This must be done before Genie is positioned as a production feature, not before it.  
**Effort:** Medium to large (depends on architectural decision about Genie's role)

---

### TRACK 7 — EXPORTS

Exports require stable data (comparisons, saved investigations, favorites) before they are worth implementing.

---

#### Step 19: Exports
**Files:** `app_shell.html` `screenExport()`, new backend export endpoint  
**Change:** Implement at minimum: PDF export of a comparison set, or PNG export of a map view.  
**Why now:** Exports are last because they are presentation layer — they depend on everything underneath being real.  
**Effort:** Large

---

### TRACK 8 — STYLING PASS

A full visual design pass is the final step before each launch gate, not an ongoing parallel workstream.

---

#### Step 20: Styling pass
**Scope:** App_shell UI polish, map UI polish, onboarding visuals, auth page design, account drawer design  
**Why last:** Styling a partially working product is waste. Style what is fully functional, final-copy, and smoke-tested.  
**Effort:** Large (design + implementation)

---

## SECTION 3: PRODUCTION GATES

Each gate defines the minimum state required before opening to a new audience. Do not open a gate if any required item is incomplete. Do not claim a gate is reached by announcing it — it requires the items below to actually be true.

---

### GATE 1: PRIVATE ALPHA
**Audience:** Founder + 2–3 trusted testers who know the product is unfinished

**Required:**
- [ ] T0-1: `/profiles` user scoping fixed
- [ ] T0-2: `handle_new_user()` trigger verified
- [ ] Pre-release smoke suite passed (OPERATIONAL_SMOKE_TESTS.md)
- [ ] GeoNames dataset confirmed loaded (~68,032 rows)
- [ ] Auth, profile intake, map launch, Find Regions, favorites confirmed working
- [ ] Notes labeled as "local only" in UI
- [ ] Port 8004 server stable under `.env.staging` config

**Not required yet:** Settings completion, port 8000 migration, content, styling, OAuth

---

### GATE 2: CLOSED BETA
**Audience:** 10–50 invited users; known astrologers or interested early adopters

**Required:**
- [ ] Everything in Gate 1
- [ ] Settings: `house_system` wired to engine (Step 1)
- [ ] Favorites: list display confirmed + soft-delete in UI (Step 2)
- [ ] Notes: migrated to Supabase (Step 3)
- [ ] Popup relocated charts working (Step 4 — port 8000 relocated-chart migrated)
- [ ] Saved Investigations: UI wired (Step 6)
- [ ] Help content: real copy (Step 13)
- [ ] Email templates: styled (Step 15)
- [ ] City search: alternate names loaded + full-text index active (Steps 10–11)
- [ ] All pre-release smoke suite items passing

**Not required yet:** Angular overlays, Google/Apple Auth, Compare Facts, Diffs, Exports, full styling pass

---

### GATE 3: PUBLIC BETA
**Audience:** Open signups; any interested user

**Required:**
- [ ] Everything in Gate 2
- [ ] Angular overlays working (Step 5 — aura endpoints migrated)
- [ ] Saved Comparisons: creation UI wired (Step 7)
- [ ] Compare Facts: real data (Step 8)
- [ ] City search abbreviation normalization (Step 12) — Recall@1 ≥ 85% confirmed
- [ ] Onboarding: real content + multi-step + per-account dismissal (Step 14)
- [ ] Google Auth wired (Step 16)
- [ ] Admin1 full names loaded (city search display fix)
- [ ] No known multi-tenant data exposure

**Not required yet:** Apple Auth, Diffs, Exports, full styling pass, Genie production integration

---

### GATE 4: PAID LAUNCH
**Audience:** Paying subscribers

**Required:**
- [ ] Everything in Gate 3
- [ ] Diffs (Step 9)
- [ ] Apple Auth wired (Step 17) — if iOS app is planned
- [ ] Genie integration defined and stable (Step 18)
- [ ] Exports: at minimum one format working (Step 19)
- [ ] Full styling pass complete (Step 20)
- [ ] Billing / subscription infrastructure (not yet defined — requires its own plan)
- [ ] City search Recall@1 ≥ 85% confirmed on full test set
- [ ] Comparison screen: no placeholder text anywhere visible to users
- [ ] Error states user-visible (not hidden behind `?debugGeometry=true`)
- [ ] Professional workflow smoke-tested independently

---

## SECTION 4: DEFERRED FEATURES

These features are documented and preserved. They are not active implementation targets. They must not be worked on until explicitly promoted through the roadmap promotion checklist (`FUTURE_FEATURES_ROADMAP.md §12`).

| Feature | Category | Why Deferred |
|---|---|---|
| Travel mode (GPS alerts, in-flight tracking) | Core product | Requires mobile/GPS infrastructure not yet designed |
| Transits to relocated houses | Core product | Requires transit engine + governance on natal vs. relocated behavior |
| GPS auto-detect for current location | Core product | Manual location works; GPS adds complexity and permissions |
| Rain / Virga reveal animation | Visual | Requires stable production renderer first |
| Overlap child colors / NOT exclusion visual refinement | Visual | Visual polish dependent on stable geometry |
| Style presets (technical, organic, premium) | Visual | Post-launch differentiation |
| Mobile / tablet ergonomics | Platform | Requires responsive redesign; not current platform |
| Cusp-gradient display | Visual | Prototype-only; production governance TBD |
| Professional workspace (multi-client accounts) | Platform | Requires account model expansion |
| Shared / client views | Platform | Requires professional workspace + permissions model |
| Custom ontology dictionaries / glyph packs | Platform | Requires ontology architecture decision |
| Certification / referral ecosystem | Platform | Requires legal and governance review |
| AI consumer intake (intent → condition translation) | AI / Layer 2 | Requires stable Layer 1 production first |
| AI comparison summaries | AI / Layer 2 | Requires real comparison facts first |
| AI professional assist | AI / Layer 2 | Deferred until professional workflow is stable |
| AI client report generation | AI / Layer 2 | Requires review gate framework first |
| AI model/version registry | Infrastructure | Future operational maturity |
| Web3 / portable ontology ownership | Speculative | Not active scope |
| Offline / airplane mode | Platform | Requires native app or service worker architecture |
| Export PDF / client-branded reports | Platform | Step 19 covers basic export; professional branding is later |
| Course / education system | Platform | Out of scope for current product phase |
| Canonical renderer migration (Phase C) | Architecture | Governed by adapter, smoke gates, and explicit promotion |
| Cache maturity (Phase C integration) | Infrastructure | After production is stable |
| CI validation pipeline | Infrastructure | After smoke tests stabilize |

---

## SECTION 5: EXPLICIT ANTI-PRIORITIES

The following must not be worked on until their stated dependencies exist. Any AI or engineer who proposes these out of order should be redirected to this document.

---

**Do not implement Diffs before Compare Facts are real.**  
Diffs are a computation over two real values. Comparison facts are currently mocked placeholder text. Diffing placeholder text produces meaningless output and misleads the user.

---

**Do not implement Compare Facts before `/relocated-chart` is migrated to port 8004.**  
Compare Facts require the relocated chart engine. That engine lives on port 8000. Until it is migrated, Compare Facts have no data source.

---

**Do not add styling before the feature is functional and smoke-tested.**  
Styling partially working features creates the illusion of completion. It slows down diagnosis when features break and makes it harder to ship real fixes without breaking visual work.

---

**Do not add AI interpretation before production calculations are real and verified.**  
AI interpretation must be grounded in factual chart data. If the underlying computation is incomplete, wrong, or mocked, AI outputs will be wrong in ways that are not detectable from the surface.

---

**Do not build a new feature while a production safety defect (Track 0) is unresolved.**  
T0-1 (`/profiles` scoping) and T0-2 (`handle_new_user()` trigger verification) are production safety items, not feature requests. Adding features before they are fixed creates a situation where users can accidentally see each other's data.

---

**Do not build Genie production integration before the core data flows (Tracks 1–3) are stable.**  
Genie integration is complex and touches the render pipeline. Building it while other data flows are unstable creates multi-instability debugging situations that are expensive to untangle.

---

**Do not build Google/Apple Auth before the email/password auth flow is fully stable.**  
OAuth adds another authentication code path. If the base auth flow has edge cases (session handling, trigger failures, edge cases in `handle_new_user()`), OAuth will inherit and obscure them.

---

**Do not treat city search as production-ready until Recall@1 ≥ 85% is confirmed on the test set in `CITY_SEARCH_PRODUCTION_REQUIREMENTS.md §9.3`.**  
Current city search is a development placeholder. Deploying it to users as production quality sets a false standard.

---

**Do not implement Exports before the data being exported is real.**  
Exporting comparison facts that are placeholder text, or saved investigations that don't exist, produces useless exports. Exports are the final presentation layer and depend on everything underneath being real.

---

**Do not expand the platform (professional workspaces, multi-client accounts, shared views) before the single-user core is fully working.**  
Multi-user complexity on top of a partially working single-user core is the fastest path to a system no one can debug.
