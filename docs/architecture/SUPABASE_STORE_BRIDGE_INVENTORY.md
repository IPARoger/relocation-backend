# Supabase Store Bridge Inventory

**Date:** 2026-06-13  
**Phase:** Frontend Wiring Step 5 — Pre-Implementation Inventory  
**Sources read:** `AUTH_FRONTEND_WIRING_PLAN.md`, `user_profile.js`, `app_shell.html`, `main_centerline_FIXER.py`, `TEMPORARY_product_store.json`, `2026_06_08_schema_v1.sql`, Phase 1–2 migrations  
**Status:** Read-only inventory. No code changes.

---

## 1. What Endpoint / File Supplies the Local Product Store?

`app_shell.html` fetches two endpoints on load:

| Endpoint | Serving code | Source file | Purpose |
|---|---|---|---|
| `GET /local-product-store.json` | `serve_local_product_store_json()` in `main_centerline_FIXER.py` | `scaffold/local_product/TEMPORARY_product_store.json` | Full store — professional_account, user_settings, places, birth_profiles, clients, saved_investigations, favorite_cities, comparison_sets, chart_record_history |
| `GET /chart-records` | `list_chart_records_api()` in `main_centerline_FIXER.py` | Same TEMPORARY file, via `list_chart_record_summaries()` | Engine-birth parameters and summary metadata for each Chart Record (for compute wiring) |

Both endpoints are gated by `_ensure_local_product_store_read_enabled()`. Neither requires authentication. Neither reads from Supabase.

---

## 2. What JS Code Fetches It?

Inside `app_shell.html`, the load sequence is:

```
bootstrap()
  └── loadViewModelFromStore()
        ├── fetch(STORE_JSON_URL)          → GET /local-product-store.json
        │     └── adaptStoreToView(payload) → builds viewModel
        └── attachEngineSummaries(viewModel) → fetch(CHART_RECORDS_API_URL) → GET /chart-records
              └── merges engineBirth into each chartRecord

render()  → uses viewModel
```

`STORE_JSON_URL = "/local-product-store.json"` (line 198)  
`CHART_RECORDS_API_URL = "/chart-records"` (line 199)

The `bootstrap()` call is the **last line** of `app_shell.html`. It runs unconditionally on page load with no session guard, no Supabase dependency, and no `CurrentUser` check.

---

## 3. What Global Variables / State Objects Hold It?

| Variable | Scope | Set by | Contains |
|---|---|---|---|
| `storeRaw` | module-level `let` in `app_shell.html` | `loadViewModelFromStore()` | Raw JSON from `/local-product-store.json` |
| `viewModel` | module-level `let` in `app_shell.html` | `adaptStoreToView(storeRaw)` | Processed view: `{ defaultChartRecordId, chartRecords[], comparisonSets[], placeNameById }` |
| `navContext` | module-level object | `syncNavContextFromLocation()` | Active chart record ID, route, comparison set — drives all rendering |
| `uiState` | module-level object | UI events | Drawer open/close, popup state — pure UI, not data |

The entire app renders from `viewModel`. All drawer panels, record lists, and map launch parameters derive from it.

`viewModel` is exposed externally as `window.__rmAppShell.viewModel()`.  
`storeRaw` is exposed as `window.__rmAppShell.storeRaw()`.

---

## 4. What Exact Fields Does `app_shell.html` Expect?

`adaptStoreToView()` reads these fields from the raw store object:

### Required (throws if missing)

| Field | Type | Accessed as |
|---|---|---|
| `storage_schema_version` | integer | Must equal `STORE_SCHEMA_VERSION` (3) |
| `user_settings.default_chart_record_id` | string | Sets `viewModel.defaultChartRecordId`; throws if absent |
| `clients[]` | array | Must have at least one entry |
| `clients[].id` | string | Becomes `chartRecord.chartRecordId` |
| `clients[].display_name` | string | Becomes `chartRecord.displayName` |
| `clients[].birth_profile_id` | string | FK into `birth_profiles[]`; throws if no match |
| `clients[].record_type` | string | `'self'` / `'client'` / `'research'` |
| `clients[].current_location_place_id` | string\|null | FK into `places[]` |
| `birth_profiles[].id` | string | PK |
| `birth_profiles[].birth_date` | string | `chartRecord.birthDate` |
| `birth_profiles[].birth_time` | string\|null | `chartRecord.birthTime` |
| `birth_profiles[].confidence_tier` | string | `'T0'`/`'T1'`/`'T2'`/`'T3'` |
| `birth_profiles[].confidence_metadata` | object | Used for time range display |
| `birth_profiles[].birth_place_id` | string | FK into `places[]` |
| `places[].id` | string | PK |
| `places[].display_name` | string | Shown in UI for birth city, current city, favorite city names |
| `places[].lat` / `places[].lon` | number | Used for viewport matching in `placesForInvestigationIds()` |

### Optional (gracefully absent)

| Field | Type | Used for |
|---|---|---|
| `favorite_cities[]` | array | `chartRecord.favorites[]` — filtered by `client_id` |
| `favorite_cities[].id` | string | Favorite row ID |
| `favorite_cities[].client_id` | string | FK into `clients[]` |
| `favorite_cities[].place_id` | string | FK into `places[]` |
| `favorite_cities[].sort_order` | integer | Sort order |
| `favorite_cities[].notes` | string | Notes text |
| `saved_investigations[]` | array | `chartRecord.explorations[]` — filtered by `client_id` |
| `saved_investigations[].id` | string | Row ID |
| `saved_investigations[].client_id` | string | FK into `clients[]` |
| `saved_investigations[].name` / `.title` | string | Display name |
| `saved_investigations[].conditions` | object | Formatted for display |
| `saved_investigations[].updated_at` | string | "Saved N days ago" label |
| `saved_investigations[].viewport` | object | `{ center_lat, center_lon, zoom }` for place matching |
| `comparison_sets[]` | array | `viewModel.comparisonSets[]` |
| `comparison_sets[].id` | string | Row ID |
| `comparison_sets[].client_id` | string | FK into `clients[]` |
| `comparison_sets[].place_ids[]` | string[] | FK into `places[]` |
| `comparison_sets[].notes` | string | Notes text |
| `professional_account` | object | **Not consumed by `adaptStoreToView()`** — present in raw store but not read by any app_shell logic |

### Not read by `adaptStoreToView()` at all

`professional_account`, `chart_record_history`, `tags`, `notes`, `supabase_mirror_version`, `_storage`, `_warning`.

---

## 5. Which Expected Fields Map Cleanly to Supabase Tables?

All Supabase tables have `account_id` column (Phase 2 migration), indexed, and RLS-protected (Phase 5). Tables exist on staging.

| Store field | Maps to | Supabase columns needed |
|---|---|---|
| `clients[].id` | `profiles.id` | `id` |
| `clients[].display_name` | `profiles.display_name` | `display_name` |
| `clients[].record_type` | `profiles.profile_type` | `profile_type` (`'human'` / `'research'`) |
| `birth_profiles[].birth_date` | `birth_records.birth_date` | `birth_date` |
| `birth_profiles[].birth_time` | `birth_records.birth_time_start` (when mode=exact) | `birth_time_start`, `birth_time_mode` |
| `birth_profiles[].birth_place_id` | `birth_records.birth_place_id` | `birth_place_id` |
| `birth_profiles[].timezone_id` | `birth_records.timezone_id` | `timezone_id` |
| `birth_profiles[].confidence_tier` | `birth_records` (derived from `birth_time_mode`) | `birth_time_mode` |
| `places[].display_name` | `places.display_name` | `display_name` |
| `places[].lat` / `.lon` | `places.latitude` / `places.longitude` | `latitude`, `longitude` |
| `favorite_cities[].place_id` | `favorite_places.place_id` | `place_id` |
| `favorite_cities[].notes` | `favorite_places.label` | `label` |
| `comparison_sets[].place_ids[]` | `comparison_set_places.place_id` | `comparison_set_id`, `place_id`, `sort_order` |
| `user_settings.house_system` | `user_settings.settings_json.house_system` | `settings_json` (JSONB) |
| `user_settings.default_chart_record_id` | `user_settings.settings_json.default_chart_record_id` | `settings_json` (JSONB) |

---

## 6. Which Expected Fields Do NOT Exist in Supabase Yet?

### Schema gaps / naming mismatches

| Store field | Gap | Notes |
|---|---|---|
| `clients[].current_location_place_id` | No direct column on `profiles`. Lives in `current_location_history.place_id WHERE is_current = true` | Requires join to resolve; different table, different access pattern |
| `birth_profiles[].confidence_tier` (`'T0'`/`'T1'`/`'T2'`/`'T3'`) | `birth_records` stores `birth_time_mode` (`'exact'`/`'approximate'`/`'unknown'`) with no T-tier vocabulary | Tier must be derived: `exact` → T0, `approximate` → T2/T3, `unknown` → T3. No `confidence_metadata` column exists. |
| `birth_profiles[].confidence_metadata` (time range display) | No column in `birth_records` | The `'T2'` time range string (`"9:47 AM–12:30 PM"`) has no schema home. Would need JSONB column or computed field. |
| `birth_profiles[].representative_time` | No column in `birth_records` | Legacy field; maps to `birth_time_start` in approximate mode but semantics differ |
| `favorite_cities[].saved_investigation_id` | `favorite_places` has no FK to `saved_searches` | No linkage between favorites and saved investigations at the database level |
| `favorite_cities[].sort_order` | `favorite_places` has `rank integer` | Field exists but named differently (`rank` vs `sort_order`) |
| `saved_investigations[].conditions` | `saved_searches.conditions_json` | Exists as JSONB. Naming and nested structure must be compatible. Not yet verified. |
| `saved_investigations[].viewport` | `saved_searches.viewport_json` | Exists as JSONB. |
| `saved_investigations[].settings_snapshot` | `saved_searches.settings_snapshot_json` | Exists as JSONB. |
| `comparison_sets[].place_ids[]` | `comparison_set_places` (separate table, one row per place) | Requires SELECT from join table, not a flat array |
| `clients[].tags[]` | No tags column on `profiles` | `tags` is a separate table with no FK to `profiles` in base schema |
| `chart_record_history[]` | No equivalent Supabase table | `location_events` exists but has different semantics and no `event_type` like `'map_search'` |
| `professional_account.display_name` | `accounts.name` | Field exists in `accounts` but `app_shell.html` never reads `professional_account` |

### The `account_user_id` problem

`profiles.account_user_id` and `user_settings.account_user_id` are legacy columns from the pre-Phase-1 schema. They are NOT the same as `account_id`. The wiring plan explicitly forbids using `account_user_id` in new code. Any new profile or user_settings INSERT must use `account_id` only.

---

## 7. Which Supabase Tables Must Be Queried for v1?

Minimum required to reproduce the store shape that `adaptStoreToView()` consumes:

| Query | Supabase table | RLS gate | Returns |
|---|---|---|---|
| 1 | `profiles` WHERE `account_id = $accountId` | `profiles_select` via `app_account_ids()` | clients[] equivalent |
| 2 | `birth_records` WHERE `account_id = $accountId` | `birth_records_select` | birth_profiles[] equivalent |
| 3 | `places` WHERE `id IN (birth_place_ids ∪ favorite_place_ids)` | `places_select` (no account filter, authenticated read) | places[] for lookup |
| 4 | `user_settings` WHERE `account_id = $accountId` | `user_settings_select` | user_settings.settings_json |
| 5 | `favorite_places` WHERE `account_id = $accountId` | `favorite_places_select` | favorite_cities[] equivalent |
| 6 | `comparison_sets` + `comparison_set_places` WHERE `account_id = $accountId` | `comparison_sets_select` | comparison_sets[] equivalent |

Optional for v1, required for full fidelity:

| Query | Supabase table | Notes |
|---|---|---|
| 7 | `saved_searches` WHERE `account_id = $accountId` | Provides `saved_investigations[]` equivalent |
| 8 | `current_location_history` WHERE `account_id = $accountId AND is_current = true` | Resolves `clients[].current_location_place_id` |

---

## 8. Minimum Adapter Shape to Avoid Rewriting `app_shell.html`

`adaptStoreToView()` is the only entry point. It expects a raw object with specific top-level keys. The minimum adapter for Step 5 is a function that **assembles a conforming store object from Supabase data** and passes it to the existing `adaptStoreToView()` unchanged.

The required output shape of the adapter is:

```javascript
{
  storage_schema_version: 3,          // must match STORE_SCHEMA_VERSION
  professional_account: { ... },      // not consumed by adaptStoreToView — can be stub
  user_settings: {
    default_chart_record_id: string,  // REQUIRED — first profile.id if no setting saved
    house_system: string,
    zodiac_mode: string,
    // ... other settings from settings_json JSONB
  },
  places: [
    { id, display_name, lat, lon }    // lat/lon from Supabase latitude/longitude columns
  ],
  birth_profiles: [
    {
      id,                             // birth_records.id (used as PK for this join object)
      birth_date,
      birth_time,                     // birth_time_start (when birth_time_mode = 'exact')
      birth_place_id,
      timezone_id,
      confidence_tier,                // derived: exact→'T0', approximate→'T2', unknown→'T3'
      confidence_metadata: {},        // stub for v1 (no Supabase home for T2 range display)
    }
  ],
  clients: [
    {
      id,                             // profiles.id
      display_name,                   // profiles.display_name
      birth_profile_id,               // birth_records.id for this profile
      record_type,                    // profiles.profile_type (map 'human'→'self' for owner)
      current_location_place_id: null // stub for v1 (current_location_history query deferred)
    }
  ],
  favorite_cities: [
    {
      id,                             // favorite_places.id
      client_id,                      // favorite_places.profile_id (re-keyed)
      place_id,                       // favorite_places.place_id
      sort_order,                     // favorite_places.rank
      notes: ""                       // favorite_places.label (re-keyed)
    }
  ],
  comparison_sets: [
    {
      id,                             // comparison_sets.id
      client_id,                      // comparison_sets.profile_id (re-keyed)
      place_ids: [],                  // from comparison_set_places SELECT
      notes: ""
    }
  ],
  saved_investigations: [],           // stub for v1 (saved_searches deferred)
  chart_record_history: [],           // stub for v1 (no Supabase equivalent)
  tags: [],
  notes: []
}
```

This shape passes directly into `adaptStoreToView()` with zero changes to `app_shell.html`.

---

## 9. What Data Should Remain Local UI State?

These should NOT be bridged to Supabase in Step 5 or any near-term step:

| State | Location | Reason |
|---|---|---|
| `navContext` (active chart record, route, comparison set) | In-memory in `app_shell.html` | Per-tab navigation state. Restoring it across sessions requires a richer "last open" feature. Deferred. |
| `uiState.drawerOpen` | In-memory | Pure rendering state, meaningless outside the current tab |
| Viewport center/zoom | Derived from nav context | Transient map state — no persistent value for basic v1 |
| `sessionStorage rm_genie_render:*` | sessionStorage | Cross-page payload for the current tab's Genie render. Tab-scoped, intentionally ephemeral. |
| `sessionStorage rm_active_profile_id` | sessionStorage | Acceptable cross-page handoff within a session. Not a source of truth; derived from profiles on page load. |
| `sessionStorage rm_map_onboarding_dismissed` | sessionStorage | One-time per-tab dismiss. |

---

## 10. What Should Absolutely NOT Be Bridged Yet?

### Hard non-goals for Step 5

| Item | Reason |
|---|---|
| `saved_investigations` / `saved_searches` | The `conditions_json` JSONB structure has not been verified to match the local `conditions` format. Risk of silent mismatch. Stub with `[]` for v1. |
| `notes` | Notes UI does not yet exist. `notes` table is RLS-protected and ready, but there is nothing to render them into. |
| `chart_record_history` | No Supabase equivalent exists. `location_events` has different semantics. Not needed for map launch. |
| `tags` | No tags column on `profiles`. Separate `tags` table has no FK to profiles in base schema. |
| `current_location_place_id` | Requires a query to `current_location_history WHERE is_current = true`. This is a second join, not a scalar. Stub with `null` for v1. |
| `confidence_metadata` (T2 time range display) | No Supabase column for the time range string. Stub with `{}` for v1. |
| `professional_account.display_name` | `app_shell.html` never reads `professional_account`. Can be stubbed with `CurrentUser.accountName`. Not rendered anywhere in the current UI. |
| User settings persistence (write path) | `user_settings` read is needed for `default_chart_record_id`. Writes (changing house system, etc.) are UI-layer changes deferred to the settings step. |
| `share_links` | Not rendered in `app_shell.html`. Deferred. |
| `comparison_set_places` detail UI | The places array is needed in the store adapter, but the full comparison detail UI is not wired yet. |
| Any changes to `adaptStoreToView()` | The adapter function must be treated as read-only. Step 5 builds a conforming input, not a rewrite of the consumer. |
| Any FastAPI endpoint retirements | The wiring plan schedules endpoint retirement for Step 8. Step 5 adds Supabase reads alongside the existing local store. The local store path remains functional until Step 8. |
| Auth guard on `app_shell.html` | `app_shell.html` is loaded inside `map_CURRENT.html` as a fragment, not as a standalone route. The guard on `map_CURRENT.html` (already in place) is sufficient. |
| RLS policy changes | All Phase 5 policies are already correct for the queries in Section 7. No migration needed. |

---

## Recommended Smallest Step 5 Implementation

**One new file:** `supabase_store_bridge.js`

Responsibilities:
1. Wait for `window.CurrentUserReady`
2. Extract `accountId` from `window.CurrentUser`
3. Run the six Supabase queries from Section 7 (queries 1–6)
4. Assemble the conforming store object (shape from Section 8)
5. Expose `window.SupabaseStore` — the assembled object
6. Expose `window.SupabaseStoreReady` — a Promise that resolves when done

**One modification to `app_shell.html`'s `loadViewModelFromStore()`:**  
Add a branch: if `window.SupabaseStoreReady` is available, await it and use the resolved object instead of fetching `/local-product-store.json`. No changes to `adaptStoreToView()`.

**One modification to `map_CURRENT.html`:**  
Inject `<script src="/supabase_store_bridge.js"></script>` after `user_profile.js`, before `app_shell.html` is initialized.

**One FastAPI route:** `GET /supabase_store_bridge.js`

This is a pure parallel path. The existing local store fetch remains intact as a fallback. Step 5 does not retire any endpoints. It does not change any schema. It does not modify `adaptStoreToView()`.

---

## Summary Table

| Store key | Supabase source | v1 status |
|---|---|---|
| `professional_account` | `accounts` | Stub — not consumed by `adaptStoreToView()` |
| `user_settings` | `user_settings.settings_json` | **Bridge** — `default_chart_record_id` required |
| `places[]` | `places` | **Bridge** — read-only, no account filter |
| `birth_profiles[]` | `birth_records` JOIN `profiles` | **Bridge** — core identity data |
| `clients[]` | `profiles` | **Bridge** — core Chart Record data |
| `favorite_cities[]` | `favorite_places` | **Bridge** — render-ready |
| `comparison_sets[]` | `comparison_sets` + `comparison_set_places` | **Bridge** — needs join |
| `saved_investigations[]` | `saved_searches` | Stub `[]` — conditions_json compatibility unverified |
| `chart_record_history[]` | None | Stub `[]` — no Supabase equivalent |
| `tags[]` | None | Stub `[]` — no FK to profiles |
| `notes[]` | `notes` | Stub `[]` — UI not yet built |
| `current_location_place_id` | `current_location_history` | Stub `null` — second join, deferred |
| `confidence_metadata` | None | Stub `{}` — no Supabase column |
