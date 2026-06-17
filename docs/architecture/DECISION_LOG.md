# DECISION LOG

**Last updated:** 2026-06-14  
**Purpose:** Permanent memory of major product, architecture, UX, and governance decisions. Future AI systems, engineers, and founders should read this before re-litigating any decision listed here. If a decision needs to change, amend it here with a new entry — do not silently revert.

---

## FORMAT

Each entry contains:
- **ID** — sequential, prefixed by category
- **Date** — when known or inferable
- **Status** — ACTIVE | AMENDED | SUPERSEDED
- **Decision** — the decision itself, stated plainly
- **Reason** — why this decision was made
- **Consequences** — what this decision constrains or enables

---

## CATEGORY PREFIXES

- `CONST` — Constitutional / foundational principles
- `ARCH` — Architecture decisions
- `DATA` — Data ownership and persistence decisions
- `UX` — User experience decisions
- `GOV` — Governance and operational decisions
- `TECH` — Specific technology choices

---

## CONSTITUTIONAL DECISIONS

---

### CONST-01
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** The First Law is: Reveal structure. Preserve judgment.

**Reason:** Relocation astrology involves symbolic judgment. A chart condition is not universally good or bad. It becomes meaningful in relation to intention, context, timing, client temperament, and personal agency. The software reveals where conditions hold. The human decides what those conditions mean.

**Consequences:**
- The system may never say "therefore this city is best" as a product truth
- Hidden ranking engines are prohibited
- AI cannot be the final interpreter
- The non-AI professional workflow must remain fully functional
- Every feature is evaluated against this sentence before acceptance

---

### CONST-02
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** The system must never perform automatic city ranking, deterministic life advice, or hidden symbolic scoring.

**Reason:** These behaviors seize judgment from the user. They corrupt the nature of the work. A ranking engine hidden behind a beautiful map is an oracle wearing a professional UI. This product must not become that.

**Consequences:**
- No "best cities for you" output
- No single machine verdict from symbolic tradeoffs
- Tradeoffs must remain visible to the user, not collapsed into winner/loser language
- Future AI integration must never secretly rank or suppress options

---

### CONST-03
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Layer 2 interpretation must remain quarantined from Layer 1 calculation truth.

**Reason:** Chart conditions are factual computation outputs. Interpretation is downstream, symbolic, and human-governed. Allowing AI to generate or alter what appears to be factual chart data destroys epistemic integrity.

**Consequences:**
- AI outputs must be labeled as interpretation, not calculation
- AI must not invent astrological facts
- Layer 2 (Genie, AI summaries, narrative) may not overwrite Layer 1 polygon or point truth
- Comparison facts shown as placeholder must not be presented as computed truth

---

### CONST-04
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Beauty cannot substitute for truth. A visual that lies is unconstitutional.

**Reason:** Cosmetic smoothing, blur, glow, and palette changes can make incorrect geometry appear correct. On a geographic truth instrument, visual plausibility is not validation.

**Consequences:**
- Aesthetic improvements to overlays require truth validation, not just visual approval
- Smoothing that moves polygon boundaries without truth support is prohibited
- Screenshot "looks right" does not constitute a validation pass
- Popup point truth outranks overlay visual impression — if they disagree, the popup wins

---

### CONST-05
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Professional sovereignty must be protected. Professional astrologers must remain in charge of symbolic reasoning.

**Reason:** The product accelerates professional work. It must not replace professional judgment, quietly overrule it, or make AI interpretation mandatory for operating the instrument.

**Consequences:**
- Non-AI professional mode must be fully usable
- AI assists; it does not operate the core instrument
- Shared client views must not expose debug internals as professional truth
- AI cannot produce client-facing content without human review gates

---

### CONST-06
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Unknowns must remain visible. The system must not pretend certainty it has not earned.

**Reason:** Epistemic hygiene. Plausible answers can be expensive, confident, and wrong. The project must prefer evidence over confidence.

**Consequences:**
- Draft features must be labeled as drafts
- Partial validation must not be presented as a pass
- Placeholder UI must not be called complete
- AI must state uncertainty plainly

---

### CONST-07
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Future features are not active law until explicitly promoted through doctrine and validation.

**Reason:** Future ideas in design documents and transfer briefs have repeatedly leaked into active instructions, causing scope creep, confusion about shipped vs. roadmap features, and wasted implementation effort.

**Consequences:**
- Rain/Virga, travel mode, Web3 models, advanced AI, certification ecosystems, and regulatory frameworks are inventoried but not active
- A future feature must be explicitly promoted to doctrine before it can be required in a build
- Transfer documents and roadmap items must never be treated as current specification

---

## ARCHITECTURE DECISIONS

---

### ARCH-01
**Date:** 2026-06 (Web2 phase)  
**Status:** ACTIVE

**Decision:** Supabase is the production system of record for all account, profile, place, birth record, settings, favorites, current location, and comparison data.

**Reason:** Supabase provides hosted Postgres with RLS, Auth, and a JavaScript SDK. It eliminates a self-managed database tier and provides row-level security as first-class infrastructure.

**Consequences:**
- localStorage and sessionStorage are caches and temporary state, never canonical
- The old port 8000 flat-file and in-memory stores are legacy and will be retired
- RLS must be enabled on all tables
- All canonical reads/writes go through Supabase — not through local JSON, not through port 8000 library endpoints

---

### ARCH-02
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** Port 8004 (FastAPI, `main_centerline_FIXER.py`) is the production Web2 backend. Port 8000 is the legacy backend.

**Reason:** The migration to Web2 required a new server without disrupting the existing codebase. Port 8004 was chosen as the clean Web2 surface.

**Consequences:**
- All new API endpoints are implemented on port 8004
- Port 8000 endpoints are not migrated on a schedule; they remain until explicitly migrated
- Any endpoint still calling port 8000 is a known legacy dependency
- `/aura-raster`, `/aura-raster-adaptive`, `/aura-field`, `/relocated-chart`, `/aspect-orb-at-point` remain on port 8000 and are blocked until migrated

---

### ARCH-03
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Rendered map overlays are not stored. They are derived output, computed fresh on every "Find Regions" call.

**Reason:** Overlay polygons are computed from birth data and geographic truth. Storing them would require invalidation on any chart or settings change and would conflate computation with persistence. The computation is fast enough to re-run.

**Consequences:**
- No `overlay_renders` table or blob storage for polygons
- Reloading the map discards all overlays
- Saved investigations store semantic state (conditions, settings, profile) — not rendered output
- Cache (if implemented) is an optimization layer, not canonical storage

---

### ARCH-04
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Rendered search payloads must be immutable. Save/pin/share functions attach to a snapshot, not the live editor state.

**Reason:** Silent mutation of saved meaning destroys trust and produces irreproducible sessions. A user who pins a search should be able to return to exactly that search.

**Consequences:**
- Re-render creates a new snapshot — it does not overwrite the saved one
- Saved investigations preserve: condition, profile UUID, settings snapshot, bounds, timestamp
- Renderer internals must not leak into semantic saved investigations

---

### ARCH-05
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Popup point truth outranks overlay visual impression. When they disagree, the popup wins.

**Reason:** The popup inspects computed truth at an exact coordinate. The overlay is an approximate rendered representation. A discrepancy means the overlay has an error, not the point.

**Consequences:**
- Overlay visual smoothing must not change point truth
- Polygon boundary rendering must not contradict popup inspection values
- Popup correctness is a hard validation requirement; overlay aesthetics are not

---

### ARCH-06
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Cities are secondary to geographic truth. The product is condition-first, not city-recommendation.

**Reason:** The instrument computes where chart conditions hold in continuous geographic space. Cities are markers inside that space, not the source of truth. Centering the product on city search would collapse it into a city recommendation engine — which violates CONST-01 and CONST-02.

**Consequences:**
- City search is a tool for locating places in the `places` table, not a product feature in its own right
- No "best cities" output
- The map shows conditions across geography; cities are labels on that landscape

---

### ARCH-07
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** `handle_new_user()` is the sole account bootstrap path. No browser code may create accounts or account_memberships directly.

**Reason:** Account creation is security-sensitive. The SECURITY DEFINER trigger runs with elevated privileges and enforces that every auth user gets exactly one account with owner membership. Browser RLS policies prohibit writes to `accounts`.

**Consequences:**
- If the trigger is missing, signup succeeds but everything downstream silently fails
- The trigger must be verified in every Supabase environment before any user creates an account
- No alternative account creation path may be added without amending this decision

---

### ARCH-08
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** The `profiles` endpoint must scope results to the authenticated user's account before production deployment with multiple users.

**Reason:** `GET /profiles` currently uses a service-role key with no account filter. This is a multi-tenant data exposure. In single-user development this is acceptable. With more than one user on the same server it is a data leak.

**Consequences:**
- Must fix `repositories/profiles_repository.py list_profiles()` before any second user exists
- The fix requires using the authenticated user's JWT claims to filter by `account_id`
- This is a P0 blocker for multi-user production

---

### ARCH-09
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** The Genie render sessionStorage side-channel (H-3 handoff) is tab-scoped and breaks on new-tab navigation. This limitation is documented and accepted for now.

**Reason:** sessionStorage is browser-defined as tab-scoped. `target="_blank"` opens a new tab with empty sessionStorage. The app_shell map link uses `target="_blank"`. Solving this would require either URL-encoding the Genie payload (size issue) or a server-side temporary store.

**Consequences:**
- Genie render payloads silently fail for new-tab map opens from app_shell
- This must be acknowledged before Genie integration is called production-ready
- Fix options: store payload in Supabase with short TTL, or encode in URL

---

### ARCH-10
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Canonical backend truth and frontend display geometry are separate. Display adaptation must never redefine the truth.

**Reason:** Layer sovereignty. Frontend pane ordering, clipping, smoothing, wrapping, or visual material language are display choices. They must not change logical astrology semantics.

**Consequences:**
- A styling change must not move polygon boundaries
- A palette change must not redefine membership
- An animation must not create the appearance of a condition that does not exist at a point
- Any doubt: inspect the truth substrate, not the visual result

---

## DATA DECISIONS

---

### DATA-01
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** Notes are stored in localStorage per `chartRecordId` in v1. The Supabase `notes` table exists but is not wired. Notes are non-canonical and non-persistent across devices.

**Reason:** localStorage notes were implemented as a quick MVP to unblock the notes UI. The Supabase `notes` table was created but not wired in the same phase.

**Consequences:**
- Notes are lost on device switch, browser clear, or private mode
- This must be disclosed in the UI ("saved locally in this browser")
- Wiring to Supabase `notes` is the correct resolution path — it is deferred, not abandoned
- Do not call notes a persistent feature until the Supabase table is wired

---

### DATA-02
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** Comparison facts must be real before Diffs can exist.

**Reason:** A diff is a computation over two real values. If the comparison facts are placeholder text, any diff is meaningless and would mislead the user about their chart comparisons.

**Consequences:**
- The comparison screen must not be called functional until real relocated chart data drives it
- Diffs must not be implemented until comparison facts are REAL (not MOCKED)
- The path to real comparison facts runs through migrating `/relocated-chart` to port 8004

---

### DATA-03
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** Saved investigations store semantic state, not rendered state.

**Reason:** Rendered polygons are derived output and should not be stored (ARCH-03). An investigation is meaningful as: which chart, which conditions, which settings, which time. These can recreate the render.

**Consequences:**
- `saved_searches` rows contain: profile_id, condition parameters, settings snapshot, bounds, timestamp
- Loading a saved investigation re-renders from its semantic parameters
- Sharing an investigation shares the semantic state, which the recipient can re-render in their own context

---

### DATA-04
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** `account_id` is denormalized onto child tables (`profiles`, `birth_records`, `places`, `favorite_places`, `current_location_history`, `user_settings`, `comparison_sets`, `notes`, `saved_searches`) for RLS performance.

**Reason:** RLS policies that join back to `account_memberships` on every row read are expensive. Storing `account_id` directly allows simple `WHERE account_id IN (app_account_ids())` policies.

**Consequences:**
- `account_id` must be written on INSERT for all child tables
- `app_account_ids()` RLS helper function is the canonical source of the current user's account IDs
- This is the correct pattern to follow for any new tables added to the schema

---

### DATA-05
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** The browser uses the Supabase anon key. The backend uses the service-role key. Service-role writes are never exposed to the browser.

**Reason:** The service-role key bypasses RLS. Exposing it in the browser would allow any user to read or write any row in the database.

**Consequences:**
- `supabase_client.js` (browser) uses `SUPABASE_ANON_KEY`
- `services/supabase_client.py` (backend) uses `SUPABASE_SERVICE_ROLE_KEY`
- Any new browser-side Supabase operation uses the anon key and is subject to RLS
- Any operation that must bypass RLS (e.g., admin bulk operations) runs server-side only

---

### DATA-06
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** Favorites write directly via Supabase JS from the browser (FAV-4). The legacy server-side favorite endpoints on port 8004 are not the active write path.

**Reason:** Direct Supabase JS writes are simpler, require no server round-trip for this operation, and allow the duplicate check and insert to use the authenticated user's session for RLS automatically.

**Consequences:**
- `favoriteMapSelectionFromButton()` in `map_CURRENT.html` uses `SupabaseClient` directly
- The `POST /favorite-places` endpoint on port 8004 is legacy — do not route new code through it
- `window.SupabaseClient` and `window.CurrentUser.accountId` must be present for favorites to work

---

### DATA-07
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Validation artifacts (smoke test results, brute-force wall comparisons, popup parity checks, screenshots, reports) are first-class project assets and must be retained.

**Reason:** Chat context is fragile. Validation artifacts are institutional memory. They prevent future AI sessions from reopening resolved issues, repeating expensive loops, or misrepresenting what has and has not been validated.

**Consequences:**
- Validation reports must not be deleted because they are old
- Superseded documents must be labeled with a banner, not removed
- Archaeology files preserve failed paths — this protects future contributors from repeating expensive mistakes

---

## UX DECISIONS

---

### UX-01
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** The map is the primary instrument face. But the product is map-first, not map-only. Chart records, saved searches, comparisons, favorites, notes, settings, and shared views are necessary for coherent human work.

**Reason:** A product that puts everything on one screen collapses the instrument into a dashboard. The instrument face (map) and the management shell (app_shell) are deliberately separate.

**Consequences:**
- `map_CURRENT.html` is the calculation and visualization surface
- `app_shell.html` is the profile, data management, and navigation shell
- The handoff contract between them (H-1) must remain stable
- Neither page should absorb the other's responsibility

---

### UX-02
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Debug surfaces must never appear in production UX.

**Reason:** Debug information (sampling internals, status metrics, render debug overlays, validation output) leaking into the commercial interface confuses users and makes the product appear broken or unfinished.

**Consequences:**
- `#renderStatus` in `map_CURRENT.html` is hidden by default (visible only with `?debugGeometry=true`)
- `?screenPixelTruth=1` mode is debug-only
- Validation overlays must not appear in normal production use
- Any error state shown to users must be human-readable, not a debug dump

---

### UX-03
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** User intent must be preserved when reopening saved investigations. A saved search reproduces the exact semantic conditions that were active when it was saved.

**Reason:** A user who returns to a saved investigation expects to see the same chart, the same conditions, the same settings context. Silent mutation of saved state is a trust failure.

**Consequences:**
- Saved investigations store: profile UUID, condition parameters, settings snapshot, bounds, and timestamp
- Reloading a saved investigation re-renders from these parameters — it does not use the current live editor state
- The "same search" must produce the same overlays (modulo any deliberate engine changes)

---

### UX-04
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Tradeoffs must remain visible. The product must not collapse symbolic complexity into comfort language.

**Reason:** Relocation astrology is valuable because it exposes tradeoffs. A location may support one life domain while pressuring another. Flattening this into "good/bad" or suppressing difficult configurations paternalizes the user and misrepresents the work.

**Consequences:**
- UI copy must not spin every configuration as positive
- Difficult configurations must remain visible and labeled — not suppressed
- "May," "can suggest," "one possible expression," "often relates to" — not "will," "definitely," "best"
- Saturn remains Saturn. Hard aspects remain hard.

---

### UX-05
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Shared client views must not allow the client to unknowingly mutate the professional's selected conditions. Shared views expose selected content only; they are not live editing sessions.

**Reason:** A professional prepares a curated view for a client. If a client can change the conditions being shown, the professional's intended presentation is corrupted.

**Consequences:**
- Shared links expose specific overlays in read-only mode
- Clients do not get access to the condition selector
- Debug internals must not appear in shared client views
- Explicit permission must be granted for any mutating client action

---

### UX-06
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** The onboarding overlay and help screen are functional in structure but contain placeholder content. They must be labeled as incomplete until real copy and visual design are applied.

**Reason:** Shipping placeholder content as though it were final misleads the team about production readiness.

**Consequences:**
- Do not count onboarding as "done" until real content and visual design are present
- `rm_guided_onboarding_dismissed` localStorage flag is the current dismissal mechanism — it is browser-local, not per-account
- The onboarding experience is a deferred polish item, not a current blocker for beta

---

## GOVERNANCE DECISIONS

---

### GOV-01
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Small boring wins over giant rewrites.

**Reason:** Giant rewrites introduce multiple instabilities simultaneously, lose rollback paths, and frequently re-introduce problems that previous small fixes had already solved. The project has demonstrated repeatedly that small isolated changes are safer and faster.

**Consequences:**
- One change, one hypothesis, one validation gate, one rollback path per task
- Refactors must be isolated from feature changes
- "Let's just rewrite X" requires explicit justification and a defined rollback path
- The Immediate Execution Queue in `FEATURE_STATUS_BOARD.md` is ordered smallest-safe-win first

---

### GOV-02
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** An AI must not declare success before a smoke test, parity check, or explicit human validation.

**Reason:** AI can be wrong while sounding confident. The anti-Cursor-bullshit protocol exists because plausible answers have been repeatedly expensive and wrong. "Looks right" is not validation.

**Consequences:**
- Every significant change defines its validation gate before implementation
- "Done" means: code changed, smoke test run, evidence exists
- If validation was not run, that must be stated explicitly — not implied as passed
- A change that cannot define its validation gate is not ready for implementation

---

### GOV-03
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** One instability source at a time.

**Reason:** Debugging math, renderer, cache, UI state, endpoint contracts, and UX simultaneously has repeatedly caused the project to lose track of what actually changed. Isolation is the only reliable diagnostic method.

**Consequences:**
- If the issue is geometry, do not also change palette
- If the issue is cache invalidation, do not also refactor search UI
- If the issue is stale server state, do not touch math
- Multi-instability tasks must be decomposed before starting

---

### GOV-04
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Documentation is infrastructure, not paperwork. Governance artifacts are the project's externalized memory.

**Reason:** Chat context is fragile. Important decisions made verbally or in chat are lost between sessions. The only durable record is written documentation promoted to a named file.

**Consequences:**
- Decisions made in chat must be promoted to durable docs
- The documentation set (wiring schema, smoke tests, handoff registry, dependency matrix, acceptance checklist, decision log, status board) is maintained as infrastructure
- An AI that has not read the relevant docs before making a claim is operating from chat memory, not project truth

---

### GOV-05
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** Archaeology must be labeled, not deleted. Failed paths and superseded documents are preserved with status banners.

**Reason:** Deleted history causes teams and AI systems to repeat expensive mistakes. The record of why something was tried and why it failed is more valuable than the disk space it occupies.

**Consequences:**
- Superseded documents get a banner (`[SUPERSEDED BY ...]`) — they are not deleted
- AI must not copy from superseded archaeology without explicit reconciliation
- Archaeology files in `memory_archaeology_raw/` are raw history — they are not current law

---

### GOV-06
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** An AI must not hallucinate architecture. It must not invent endpoints, database schemas, renderer behavior, UI contracts, or validation status not present in the source files.

**Reason:** Invented architecture is worse than admitted uncertainty. Acting on hallucinated endpoints or schemas creates real bugs from fictional specifications.

**Consequences:**
- Before claiming an endpoint exists, read the server file
- Before claiming a table exists, read the schema migrations
- Before claiming validation passed, point to the evidence artifact
- "I believe" or "probably" without a file reference is an admission that the claim is unverified

---

### GOV-07
**Date:** Project founding  
**Status:** ACTIVE

**Decision:** The closeout protocol is the task's internal conscience. Every significant task ends with: files changed, validation run, evidence location, rollback scope, deferred items, rejected scope, and next step.

**Reason:** Tasks that end with only "done" leave no trail. Future sessions cannot determine what was changed, what remains uncertain, or what was intentionally not done.

**Consequences:**
- "Done" requires a statement of what changed and what was validated
- "No validation run" is an acceptable closeout only when stated explicitly
- Rejected scope must be named — not silently omitted

---

## TECHNOLOGY DECISIONS

---

### TECH-01
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** Google Places API is disqualified for any flow that stores city data. Mapbox standard tier is disqualified for storing birth cities.

**Reason:**
- Google Places ToS explicitly prohibits permanent storage of autocomplete results or geocoding data. Birth cities, current locations, and favorites require permanent storage. Using Google Places would violate ToS.
- Mapbox standard tier prohibits permanent storage of results. Enterprise tier is required and is significantly more expensive.

**Consequences:**
- Do not integrate Google Places API for birth city, current location, or favorites flows
- Mapbox is only acceptable if the project moves to Enterprise pricing and requires it
- Acceptable options: GeoNames (current), Geoapify (storage explicitly permitted), Photon/Pelias (open license)
- See `CITY_SEARCH_PRODUCTION_REQUIREMENTS.md` §10 for full vendor analysis

---

### TECH-02
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** City search must be solved architecturally (alternate names + full-text index), not through alias patches.

**Reason:** Maintaining a manual alias list (NYC → New York, Bombay → Mumbai, etc.) does not scale. GeoNames `alternateNamesV2.txt` contains 13.4M name variants including historical names, transliterations, native scripts, and abbreviations. The correct solution is loading this dataset into `places.alternate_names_json` and using PostgreSQL full-text search. Patching aliases individually would produce a maintainability disaster.

**Consequences:**
- The correct fix for city search is: load `alternateNamesV2.txt`, create full-text index, switch from `ILIKE` to `tsquery`
- No alias patch table should be created
- Abbreviation normalization (`NYC → New York`, `St → Saint`) is acceptable as a lightweight client-side pre-processing step
- City search must meet `CITY_SEARCH_PRODUCTION_REQUIREMENTS.md` §11 acceptance criteria before production launch

---

### TECH-03
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** The app_shell → map handoff URL contract is:
```
/map_CURRENT.html?skipOnboarding=1&handoff=app_shell&handoffCreatedAt=<ISO>&chartRecordId=<profiles.id UUID>[&placeId=<uuid>][&explorationId=<uuid>][&comparisonSetId=<uuid>][&returnTo=<encoded>][&genieRenderRef=<string>]
```
`chartRecordId` carries the `profiles.id` UUID — not a legacy chart ID.

**Reason:** The handoff contract was established during the Web2 migration (MAP-ENTRY phases). The `chartRecordId` param name was preserved from the legacy system but now refers to `profiles.id` in Supabase. Both `first_profile_intake.js` and `app_shell.html buildMapHandoffUrl()` produce the same URL shape. `map_CURRENT.html readAppShellHandoff()` consumes it.

**Consequences:**
- Any code that produces a map navigation URL must use this exact shape
- `handoff=app_shell` must be present or `lastAppShellHandoff` is null (profile selects manually)
- `chartRecordId` is always a Supabase `profiles.id` UUID — never a legacy integer ID
- This shape must not be changed without updating all three producers and the consumer

---

### TECH-04
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** Exact birth time is required for production chart calculations. Profiles with `birth_time_mode='unknown'` cannot drive Find Regions.

**Reason:** The Python chart engine requires a UTC birth hour to compute planetary positions and house cusps. Without a time, house placements cannot be calculated. The engine returns 422 for unknown-time profiles.

**Consequences:**
- Intake must collect a birth time (exact or approximate range)
- The engine-birth endpoint returns 422 for `birth_time_mode='unknown'`
- Future work: rectification workflow or range-mode computation for unknown times
- Users with unknown birth times cannot use Find Regions in the current system

---

### TECH-05
**Date:** 2026-06  
**Status:** ACTIVE

**Decision:** `cities.js` (GeoNames ~12MB) is loaded synchronously via `<script>` tag in `map_CURRENT.html`.

**Reason:** This was the fastest path to implement city typeahead on the map. Async loading was deferred.

**Consequences:**
- `cities.js` blocks map initialization on slow connections
- This is a known performance risk (PRODUCTION_WIRING_SCHEMA R8)
- The correct fix (async/lazy loading) is deferred
- Do not add more synchronous large-file `<script>` tags to `map_CURRENT.html`

---

## AMENDMENT PROTOCOL

When a decision must change:

1. Mark the original entry `Status: AMENDED`
2. Add a note: `Amended by: <new decision ID>, <date>, <reason>`
3. Create a new entry with `Status: ACTIVE` that references the original
4. Do not delete the original entry

This preserves the history of why the change was made and prevents future systems from reverting to the old decision without understanding the history.
