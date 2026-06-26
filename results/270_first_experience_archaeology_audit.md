# BI-0 — First Experience Archaeology & Design Canon Audit

**Date:** 2026-06-26  
**Slice:** BI-0A (read-only discovery)  
**Status:** Archaeology complete — no implementation  
**Authority:** `docs/BETA_MASTER_CHECKLIST.md`, `results/264_family_resemblance_final_audit.md`, `docs/canon/MATERIAL_SYSTEM_CANON.md`, `docs/product/INTERFACE_AND_DESIGN_CANON.md`, `results/262_settings_harmonization_audit.md`

**Method:** Targeted read of production surfaces (max 8 files). No redesign. No proposals in body sections — inventory and continuity only.

**Screenshots:** `validation/mockups/beta/screenshots/bi_archaeology/` (production routes; authenticated map shots require PO session — see manifest).

---

## Executive summary

The first five minutes today traverse **at least four visual dialects** and **three routing owners**:

1. **`auth.html`** — standalone gray/blue SaaS card (system-ui, `#1d4ed8` accent)
2. **`first_profile_intake.js`** — dark purple developer overlay (inline CSS, not instrument family)
3. **`map_CURRENT.html`** — warm instrument workspace (M2-X `family_resemblance` bridge)
4. **`app_shell.html` guided onboarding** — exists but is **not on the default first-run path** (auth → map, not app_shell)

**Continuity verdict:** Six disconnected pages masquerading as one product. Canon (`INTERFACE_AND_DESIGN_CANON` §6.1) says intake should feel calm/premium and users should not be dropped into a cluttered map; production drops authenticated users on the map immediately, then blocks with intake overlay or shows map chrome before profile exists.

**Primitive verdict:** No single primitive library for First Experience. Auth, intake, and map each implement their own buttons, fields, alerts, and overlays.

---

## 1. Screen inventory — Authentication

**Production file:** `auth.html`  
**Route:** `/auth.html` (`main_centerline_FIXER.py`)  
**Renderer:** Standalone HTML + inline CSS + IIFE script  
**Dependencies:** `supabase_client.js`, Supabase Auth CDN (via client), `/config/supabase`  
**Backend:** Supabase Auth (signup, login, OAuth, reset email, resend confirmation)  
**Post-auth redirect:** Always `MAP_URL` = `/map_CURRENT.html` (never `app_shell.html`)

| Screen / state | Route | How reached | Visual quality | UX quality |
|----------------|-------|-------------|----------------|------------|
| **Signup** | `/auth.html` (default view on cold load) | First visit, no session | Gray card, blue primary — generic SaaS | Clear fields; Google + email paths |
| **Login** | `/auth.html` `data-view="login"` | “Sign in” link from signup | Same family as signup | Clear; forgot password inline |
| **Google OAuth** | `/auth.html` → Supabase → `/auth.html` | Buttons on signup/login | Same card; OAuth divider | Redirect round-trip; errors surfaced |
| **Apple OAuth** | — | **Not present in DOM or JS** | N/A | N/A — deferred per acceptance checklist |
| **Forgot password** | `/auth.html` login view | “Forgot password?” — uses email field | Success alert inline (`#reset-ok`) | No separate screen; requires email pre-filled |
| **Password reset completion** | `/map_CURRENT.html` (redirect target) | Email link `redirectTo: origin + MAP_URL` | **No dedicated reset UI found on map or auth** | User lands on map/auth session flow — archaeology gap |
| **Email verification / confirm** | `/auth.html` `data-view="confirm"` | After signup when no immediate session | Envelope icon, resend timer | 60s resend cooldown; back to signup |
| **Session recovery** | `/auth.html` init | `getSession()` on load | N/A | Existing session → immediate redirect to map |
| **Returning user** | Login → map | `signInWithPassword` / OAuth session | N/A | Same map entry as new user |
| **Existing account** | Signup footer → login | `goto-login` | N/A | Obvious cross-link |
| **Auth errors** | Inline `#signup-err`, `#login-err`, `#confirm-err` | API failures | Red alert boxes | Friendly error mapping in `friendlyError()` |
| **Init / server down** | Signup view + error | SupabaseReady catch | Same | “Could not connect to the server” |

**Shared controls:** Custom `.btn-primary`, `.btn-oauth`, `.link-btn`, `.pw-toggle`, `.alert` — **auth-local only**, not shared with chart family.

**Stale doctrine note:** `PRODUCTION_ACCEPTANCE_CHECKLIST.md` §1.5 marks Google as “not implemented”; production `auth.html` **does** wire `signInWithOAuth({ provider: "google" })`. Apple remains absent — aligns with checklist.

**Screenshots:** `01_auth_signup.png` … `05_auth_login_error.png`

---

## 2. Screen inventory — Birth intake

**Production file:** `first_profile_intake.js` (served at `/first_profile_intake.js`)  
**Renderer:** JS-injected full-screen overlay (`#rm-first-profile-intake`) + inline stylesheet  
**Dependencies:** `window.SupabaseReady`, `window.CurrentUser`, `window.RMPlaceSearch` (`place_search_client.js`), `POST /profiles/create-with-birth`  
**Activation paths:**
- `app_shell.html`: `SupabaseStoreReady` rejects → `INTAKE_REQUIRED` → `__showFirstProfileIntake()`
- `map_CURRENT.html`: script loaded; `SupabaseStoreReady.catch` on message containing `"Intake overlay required"`
- Add-profile mode: `__showFirstProfileIntake({ mode: "add", onCreated })` from Settings/Profile management in shell

| Field / flow | Implementation | Notes |
|--------------|----------------|-------|
| **Birth date** | `<input type="date" id="rm-intake-date">` | Native date picker |
| **Birth time exact** | `<input type="time">` when mode=exact | Native time picker |
| **Unknown time** | Toggle buttons `#rm-mode-exact` / `#rm-mode-unknown` | Hides time field; sends `birth_time_mode: "unknown"` |
| **Birth location search** | Text input + `RMPlaceSearch.searchPlaces` → `GET /places/search` | Debounced 300ms; dropdown results |
| **Location ambiguity** | User must click a result row | No disambiguation UI beyond list |
| **Timezone** | From selected place `timezone_id` in POST body | Not shown to user |
| **Validation** | Client-side + server errors in `#rm-intake-err` | Required name, date, place; time if exact |
| **Error handling** | `.err-msg` red panel; rollback/orphan messages | Compensation delete on birth_record failure |
| **Cancel path** | **None in `mode: "first"`** | Overlay is modal with no dismiss — reload only |
| **Edit path** | Place clear button (✕); mode toggle | No post-create edit in overlay |
| **Existing profile path** | `mode: "add"` with optional “Switch to new profile” checkbox | Shell only — not first-run |
| **Google name prefill** | `prefillNameFromGoogleMetadata()` on show | OAuth display name → name field |

**Visual quality:** Dark theme (`#1a1a2e` card, `#7b61ff` CTA) — reads as **legacy developer overlay**, not Material Canon instrument.

**UX quality:** Functional for happy path; **no escape hatch** on first run; unknown time allowed in UI but engine returns **422** for chart resolution per acceptance §2.3.

**Success redirect:** `/map_CURRENT.html?skipOnboarding=1&handoff=app_shell&handoffCreatedAt=<iso>&chartRecordId=<uuid>`

**Screenshots:** `10_birth_intake_default.png`, `11_birth_intake_unknown_time.png`, `12_birth_intake_validation_error.png`

---

## 3. Chart creation (post-intake)

**What happens after intake succeeds:**

1. Full-page redirect to `map_CURRENT.html` with query params (see above).
2. `auth_guard.js` passes (session exists).
3. `skipOnboarding` true → **skips** `#mapOnboarding` right-click card (`rm_map_onboarding_dismissed` not set, but URL flag bypasses).
4. `loadChartProfiles()` runs (`chartProfilesReady` promise):
   - Fetches `/chart-profiles` (legacy) and `GET /profiles` (Supabase).
   - `applyActiveProfileSelection()` uses `chartRecordId` query param.
5. Nameplate `#rm-np-name` shows **“Loading…”** until profile hydration completes.
6. **No dedicated chart-computation spinner, progress bar, or “building chart” screen.**
7. **No blank interstitial** — map tiles render immediately under overlay/panel.
8. App-shell handoff banner (`#appShellHandoff`) may show informational JSON — debug/handoff artifact, not user-facing onboarding.

**Actual behavior:** Silent async profile list hydration on an already-visible map. User may see Genie panel + OSM map before nameplate resolves.

**Reserved animation opportunity:** Post-intake “chart record ready” / “preparing your map” — **no container exists today**.

---

## 4. First map state

**Route:** `/map_CURRENT.html`  
**Gate:** `auth_guard.js` → unauthenticated users sent to `/auth.html` (screenshot: `20_unauthenticated_map_redirect.png`)

| Element | First-session state |
|---------|---------------------|
| **Default overlay** | None until user runs Genie search (no auto overlay) |
| **Controls visible** | GV builder panel, topbar nav, zoom/history/pin cluster, city search mount, nameplate |
| **Walkthrough** | `#rm-walkthrough` 7-step coach marks — **not auto-started** in code reviewed; separate from `#mapOnboarding` |
| **Onboarding card** | `#mapOnboarding` right-click hint — **suppressed** when `skipOnboarding=1` (intake success path) |
| **Popup** | Right-click map or city marker → relocated chart popup; “View overlays here” after M1-C |
| **Help** | No Help link in map topbar; Profile/Comparison/Settings → `app_shell.html` |
| **Save** | `#gv-save-inline` in panel; `#rm-save-disk` + menu item only in **explore mode** (after search) |

**Guided onboarding (`app_shell.html` ONBOARDING_SLIDES):** 7 slides, modal — **not shown** on default auth→map first run.

---

## 5. First investigation — mechanical dead-end audit

| Action | Reachable without coaching? | Dead-end risk |
|--------|----------------------------|---------------|
| **Inspect overlay** | After Genie Search Map + explore mode | User must discover Genie first |
| **Click popup** | Right-click map or city | Onboarding card skipped after intake |
| **Open relocated chart** | Popup shows PIH rows | Requires profile + click gesture |
| **Save investigation** | Explore save disk / menu | Hidden until post-search explore |
| **Favorite** | Popup action | Requires popup open |
| **Comparison** | Topbar link → `app_shell.html#/comparison` | Leaves map; chart context handoff varies |
| **Notes** | Not in map topbar | Dead end from map — must open Profile/shell |

**Intake → map with skipOnboarding:** User misses both app_shell guided tour and map right-click onboarding.

---

## 6. Primitive audit

Objective: one primitive, one implementation, many contexts.

| Primitive | Canonical implementation (chart family) | First Experience implementation | Verdict |
|-----------|-------------------------------------------|----------------------------------|---------|
| **Primary button** | Settings/shell `.btn-primary` / instrument CTAs | Auth `.btn-primary` (blue); intake `.submit-btn` (purple); GV `.gv-btn-search` (sage, M2-X) | **Duplicate ×3** |
| **Secondary button** | Shell linkish / outline | Auth `.link-btn`; GV `.gv-btn-add` | **Duplicate** |
| **OAuth button** | — | Auth `.btn-oauth` only | **Local** |
| **Text field** | Settings panels | Auth inputs; intake inputs; map city search `.rm-sls-input` | **Duplicate** |
| **Password field + toggle** | — | Auth `.pw-toggle` only | **Local** |
| **Dropdown** | D2 custom (Comparison, Settings) | Native `<select id="chartProfile">`; GV `.gv-g-dd` | **Duplicate** |
| **Checkbox** | Settings | Intake add-mode switch only | **Partial** |
| **Radio / mode toggle** | Settings segments | Intake `.mode-btn` pair | **Duplicate** |
| **Date picker** | Profile management | Native `type=date` intake | **Native only** |
| **Time picker** | Profile management | Native `type=time` intake | **Native only** |
| **Location search** | `RMPlaceSearch` + `saved_location_search_ui` (map) | Intake uses `RMPlaceSearch` with **custom** results UI | **Shared API, duplicate UI** |
| **Search field** | Map `.rm-sls-input` | Intake place input | **Duplicate UI** |
| **Modal** | `app_shell` `.modal-backdrop` | Intake full-screen overlay; map `#rm-save-dialog` | **Duplicate ×3** |
| **Dialog** | Save dialog `.rm-sdlg-*` | Auth alerts; intake err-msg | **Duplicate** |
| **Section header** | G3 `.meta` / t-band | Intake uppercase labels | **Duplicate** |
| **Page header** | Iowan plates (Profile) | Auth `.card-title`; intake `h2` | **Duplicate** |
| **Card** | G3 `tcard` / `--rm-card` | Auth `.card`; intake `.card`; GV `.gv-builder` | **Duplicate ×4** |
| **Info box** | Handbook panels | Auth `.alert`; map onboarding card | **Duplicate** |
| **Notes surface** | `NotesCanonical` | Not in first path | N/A |
| **Tooltip** | Map city labels | Limited | **Partial** |
| **Spinner / progress** | — | “Searching…” text intake; “Loading…” nameplate | **Ad hoc text only** |
| **Empty state** | Notes library patterns | Ghost strip `:empty::after` | **Local** |
| **Error state** | Auth alert / intake err-msg | Multiple patterns | **Duplicate** |
| **Success state** | — | Auth `#reset-ok`; save disk states | **Duplicate** |
| **Confirmation** | — | None on intake submit | **Missing** |
| **Autocomplete list** | `rm-sls-panel` (map) | Intake `.place-results` | **Duplicate** |
| **Badge / chip** | Comparison / GV chips | GV `.gv-chip` | **Map-local** |
| **List row** | Settings, Notes library | Intake `.place-result` | **Duplicate** |
| **Navigation** | `app_shell` primary-nav | Map `.rm-mainmenu` | **Duplicate** |
| **Back / Continue** | Onboarding modal | Walkthrough Next/Skip | **Duplicate** |

**Summary:** First Experience pulls **zero** shared components from `family_resemblance.css` / shell modal system. Intake is the strongest outlier (dark theme). Auth is second (gray SaaS).

**Needs extraction (for later — not this slice):** unified field, button, alert, location-search, and modal primitives.  
**Needs retirement:** intake inline CSS theme; auth isolated token block (or bridge, not rewrite in BI-0).

---

## 7. Family resemblance audit

| Screen | Recognizable beside Profile / Comparison / Settings? | WHY not (if no) |
|--------|------------------------------------------------------|-----------------|
| **auth.html** | **No** | Cool gray/blue SaaS; system-ui; no stone/paper; no Avenir/Iowan; no `rm-instrument-surface` |
| **first_profile_intake.js** | **No** | Dark purple dev overlay; uppercase micro-labels; neon accent; unrelated to G3 cards |
| **map_CURRENT.html** (M2-X) | **Partial** | Panel/chrome bridged to instrument; auth/intake precede it |
| **app_shell guided onboarding** | **Partial** | Uses shell modal styling but **not seen** on first run |
| **map walkthrough** | **Partial** | Coach-mark card; map chrome only |

Reference: `264_family_resemblance_final_audit.md` — chart family = Profile, Relocated, Comparison V5, Notes (post-H10 Settings/Help).

---

## 8. Transition audit

```
Signup/Login (auth.html)
    ↓  window.location = /map_CURRENT.html
Map load (tiles + panel visible)
    ↓  SupabaseStoreReady rejects → intake overlay OR profile hydrate
Birth intake overlay (if zero profiles)
    ↓  POST create-with-birth → redirect map ?skipOnboarding=1&chartRecordId=…
Map (again, onboarding suppressed)
    ↓  user builds GV conditions → Search Map
Explore mode (panel collapse, ghost strip)
    ↓  optional save disk / popup / favorite
Profile / Comparison (app_shell via topbar — new document)
```

**Continuity assessment:**

| Transition | Feels connected? | Evidence |
|------------|------------------|----------|
| Auth → Map | **No** | Visual whiplash; no “welcome” bridge |
| Map → Intake | **Disorienting** | Map visible behind dark overlay; not shell |
| Intake → Map | **Weak** | Query-param handoff; skipOnboarding skips help |
| Map → Explore | **Yes** | FLIP animation; same document |
| Map → app_shell | **No** | Full navigation; different chrome |

**Not one experience — six surfaces stitched by redirects.**

---

## 9. Reserved animation opportunities

Document only — no design.

| Moment | Container exists? |
|--------|-------------------|
| Post-signup “check email” | Static confirm view only |
| Preparing personal map / chart record | **No** |
| Building chart / engine birth resolution | **No** (silent fetch) |
| Loading overlays | `data-overlay-phase` hooks (M1-B) — machine, not user animation |
| Transition into map (first time) | **No** |
| Transition into profile/comparison | **No** |
| Intake overlay enter/exit | CSS none beyond display |
| Explore mode enter | FLIP exists (panel/bottle/ghost) — **only polished transition in first path** |

---

## 10. Existing doctrine (references — do not recreate)

| Topic | Source | Decision captured |
|-------|--------|-------------------|
| Entry / intake tone | `INTERFACE_AND_DESIGN_CANON.md` §6.1 | Calm, premium; exact birth assumed in base workflow |
| Unknown birth time | Same canon §6.1; deferred layers A.40, A.77 | Conversational/confidence intake is **later** |
| Unknown time engine | `PRODUCTION_ACCEPTANCE_CHECKLIST.md` §2.3 | `birth_time_mode=unknown` → 422 on engine-birth |
| Google OAuth | `auth.html` (wired); checklist §1.5 **stale** | Production has Google buttons; checklist says absent |
| Apple OAuth | Checklist §1.6 | Deferred — no UI |
| IATA / city search | `PRODUCTION_ACCEPTANCE_CHECKLIST.md` §2.1, §7.2; `CITY_SEARCH` arch docs | Alias quality inadequate; `GET /places/search` |
| One-profile intake | Checklist §2.1 | First-run one profile; add mode in shell |
| Auth wiring plan | `docs/architecture/AUTH_FRONTEND_WIRING_PLAN.md` | (Referenced — not re-read in full; auth is standalone HTML) |
| Material family | `MATERIAL_SYSTEM_CANON.md`, `264` audit | Chart surfaces instrument; map bridged M2-X; auth/intake not |
| Settings harmonization | `262_settings_harmonization_audit.md` | H6 layout; instrument surface on settings |

---

## 11. Screenshot inventory

**Folder:** `validation/mockups/beta/screenshots/bi_archaeology/`

| File | Screen |
|------|--------|
| `01_auth_signup.png` | Signup + Google |
| `02_auth_login.png` | Login |
| `03_auth_forgot_password_sent.png` | Forgot password success inline |
| `04_auth_email_confirm.png` | Email verification holding |
| `05_auth_login_error.png` | Login error |
| `10_birth_intake_default.png` | Birth intake (exact time) |
| `11_birth_intake_unknown_time.png` | Unknown time mode |
| `12_birth_intake_validation_error.png` | Validation error |
| `20_unauthenticated_map_redirect.png` | Auth gate (map → sign-in) |

**PO session still needed:** authenticated first map, Genie, popup, explore, save dialog, returning user with profile, place search results with live API.

---

## 12. BI-0B recommendation — mockups before implementation

Per canon: **Audit → Mockups → Implementation**. Read **§14 BI-0B calibration** before any mockup work.

**Mockup spine (one journey, not separate apps):**

```
Auth → Birth Information → Preparing Your Personal Map → Personalized Map
```

| Priority | Screen / flow | Why mockup first |
|----------|---------------|------------------|
| P0 | **Continuous first journey** (§14.4) | Auth + birth intake + preparing + personalized map as one instrument |
| P0 | **Birth Information step** | Single conceptual step (date + time + place); reward = personalized map, not per-field micro UI |
| P0 | **“Preparing Your Personal Map”** | Transition container reserved (§14.5); no animation design in BI-0B |
| P0 | **Personalized map landing** | First frame where birth data visibly powers the instrument |
| P1 | **Pre-birth map** (§14.2) | City search, favorites, geography, save — astrology fields show `—` only |
| P1 | **Birth location search** (results, empty, no match) | Reuse `RMPlaceSearch` / map search primitives (§14.6) |
| P1 | **Password reset completion** | No production screen located |
| P2 | **Returning user login → personalized map** | Shorter path; same journey chrome |
| P2 | **Auth edge states** (confirm email, OAuth cancel/error) | Same card family as journey step 1 |
| **Do not mockup** | **Unknown birth time onboarding** | Beta requires exact time (§14.1); current UI is doctrine mismatch to **remove**, not improve |
| Defer | Apple OAuth | Not built |
| Defer | Birth time confidence/range | Deferred doctrine — not Beta |
| Defer | Rain/virga / progressive reveal animation | Reserve container only (§14.5) |
| Defer | app_shell guided onboarding | Not on first-run path — merge into journey or cut |

---

## 13. Validation

**Smoke:** `scripts/smoke_bi0_archaeology.py` (read-only) — routes, assets, production links.

---

---

## 14. BI-0B calibration (read before mockups)

**Status:** Product doctrine corrections to BI-0A assumptions. **No implementation in this slice.**

### 14.1 Exact birth time is the Beta assumption

- Relocation requires an **accurate birth time** for Beta.
- Do **not** design Unknown Birth Time as a normal onboarding path.
- Do not fabricate relocated overlays or approximate charts.
- Future birth-time confidence/range workflow exists in doctrine (`INTERFACE_AND_DESIGN_CANON` §6.1; deferred A.40/A.77) — **intentionally not Beta**.
- **Production mismatch:** `first_profile_intake.js` exposes Exact / Unknown toggle. Treat as **doctrine bug to resolve** (remove or hide from Beta path), **not** a workflow to polish in mockups.

### 14.2 Popups and map work without astrology

- Do **not** suppress map functionality before birth data exists.
- Users may still: search cities, explore the map, favorite locations, inspect geographic information, save investigations.
- Only astrology-dependent values are unavailable — e.g. `Sun House: —`, `Venus House: —`.
- Everything else continues normally.
- **BI-0A note:** `auth_guard.js` currently blocks unauthenticated map access; authenticated users without profiles see intake overlay (blocks map). Mockups should distinguish **pre-birth** (geography-only) from **post-birth** (personalized instrument).

### 14.3 Not “micro rewards” per field

- Goal is **not** that every field unlocks a visible widget.
- Birth date, time, and location are **one conceptual step** — “Birth Information.”
- The reward is the **personalized map** appearing as a whole, not feedback after each keystroke.
- First experience should not feel like paperwork, but payoff is **instrument creation**, not gamified field-by-field unlocks.

### 14.4 The transition is the experience

Mockup concentration:

| Step | Purpose |
|------|---------|
| Auth | Entry into the same product — not a separate SaaS app |
| Birth Information | One calm step; exact time required |
| Preparing Your Personal Map | Bridge state (copy + layout + reserved animation container) |
| Personalized Map | User’s chart context powers the workspace |

Do not treat Auth and Birth Intake as separate applications with different visual languages.

### 14.5 Reserve animation space only

- Do **not** design animations in BI-0B.
- Reserve containers for later (once per profile): birth chart construction, rain/virga, progressive reveal.
- Flow must work with static states; animation is enhancement, not dependency.

### 14.6 Reuse primitives

Before any new control in mockups: search production for an existing primitive.

| Need | Search first |
|------|----------------|
| Buttons, fields, alerts | Settings / `app_shell` / map M2-X GV |
| Location search | `RMPlaceSearch`, `saved_location_search_ui` |
| Modal / dialog | `app_shell` modal, `#rm-save-dialog` |
| Cards / surfaces | `family_resemblance.css`, G3 `tcard` |

**One primitive. Many contexts.** New primitives only when no equivalent exists.

### 14.7 BI-0A assumptions corrected

| BI-0A assumption | Correction |
|------------------|------------|
| Unknown time UX deserves P1 mockup | **Withdrawn** — remove from Beta onboarding, not improve |
| Intake is only blocker before map | Pre-birth geography-only map is valid product surface |
| Per-field unlock would reduce paperwork feel | **Withdrawn** — single-step birth info + personalized map payoff |
| Auth → intake → map are three apps | **One continuous journey** mockup required |

---

*End of BI-0A archaeology audit (BI-0B calibration appended).*
