# Profile → Map Wiring Audit

**Date:** 2026-06-13  
**Step:** 5D pre-implementation audit  
**Status:** Read-only. No code changes were made.  
**Verdict:** 🔴 RED — Profile switching in `app_shell.html` is cosmetic with respect to all chart calculations.

---

## Scope

Traces the complete path from `switchChartRecord()` in `app_shell.html` through every execution path in `map_CURRENT.html` to determine whether selecting a different Supabase profile actually changes what the calculation engine computes.

---

## Architecture Diagram

```
app_shell.html                          map_CURRENT.html
──────────────────────────              ───────────────────────────────────────

switchChartRecord(supabase_uuid)
  ↓
navContext.chartRecordId = supabase_uuid
  ↓
_savePersistedChartRecord()             #chartProfile <select>
  [localStorage]                               ↑
  ↓                                     loaded from GET /chart-profiles
buildMapHandoffUrl()                          ↑
  ↓                                     charts/chart_profiles.json (3 hardcoded)
/map_CURRENT.html                       + library/library.json (Phase 2.0)
  ?handoff=app_shell                    + GET /profiles (Supabase display_name only)
  &chartRecordId=supabase_uuid                 │
  &genieRenderRef=ref (if Genie)               │
  ↓                                            ↓
readAppShellHandoff()              getBirthParamsFromProfile()
  "INFORMATIONAL ONLY —               reads dataset.profile from selected option
   no map mutations"                  → { date, time } in legacy format
  ↓                                            │
  chartRecordId in URL                         │ ← NULL for Supabase options
  ↓                                            │   (intentionally omitted, Phase 2.5B)
PATH A: Legacy DOM (Find Regions)              ↓
  buildPlanFromLegacyDom()           birth_year/month/day/hour_utc
    → getBirthParamsFromProfile()              ↓
    → dataset.profile (legacy JSON)   POST /aura-field or /find-regions
    → Supabase profile → NULL ❌               ↓
                                       SwissEph calculation engine
PATH B: Genie render                           ↑
  resolveBirthParamsForGenieRender()           │
  if isAppShellGenieHandoffActive():           │
    fetchEngineBirthForChartRecord(UUID)       │
      → GET /chart-records/UUID/engine-birth   │
      → local_product_store.py                │
      → TEMPORARY_product_store.json          │
      → 404: UUID not found ❌                 │
  else (no Genie handoff):                     │
    getBirthParamsFromProfile() ❌              │
                                               │
PATH C: Popup chart (click on map)             │
  fetchRelocatedChart(lat, lon)                │
    → getActiveProfileBirthParams()            │
    → dataset.profile → NULL ❌                │
    → throws "no_profile"                      │
                                               │
 ─ ─ ─ ─ ─ MISSING LINK ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
        supabase_uuid → birth_records
        → birth_year/month/day/hour_utc
```

---

## Code Path Detail

### 1. How active profile is stored

`app_shell.html` stores the active profile in `navContext.chartRecordId` (in-memory JS object). This is a **Supabase profile UUID** (e.g. `4cb4e713-6991-48ac-ad9e-9fc865f0c912`).

`switchChartRecord()` writes it via:
```javascript
// app_shell.html:1351
function switchChartRecord(newId, noticePrefix) {
  if (newId === navContext.chartRecordId) return;
  _savePersistedChartRecord(newId);           // localStorage (Step 5C)
  navigate(navContext.route, { chartRecordId: newId, explorationId: null });
}
```

Persistence: `localStorage["rm_selected_chart_<userId>"]` (Step 5C). Survives page reload within `app_shell.html`.

### 2. How active birth record is stored

It is not stored in a dedicated variable. `app_shell.html` builds `vm.chartRecords` in `adaptStoreToView()`, where each chart record includes `birthDate`, `birthTime`, `birthTimeDisplay`, `birthCity`, `confidenceTier` for UI rendering. These come from `supabase_store_bridge.js` → Supabase `profiles` + `birth_records` tables.

However, these fields exist only as **display data** in the view model. They are never passed to the calculation engine.

### 3. How active chart record is determined

```javascript
// app_shell.html:830
function activeRecord() {
  return getChartRecord(navContext.chartRecordId);
}

function getChartRecord(id) {
  const vm = requireViewModel();
  return vm.chartRecords.find((r) => r.chartRecordId === id) || vm.chartRecords[0];
}
```

`vm.chartRecords[N].chartRecordId` = Supabase profile UUID (set in `adaptStoreToView()` at line ~570).

### 4. What is passed into chart calculations

**Legacy DOM path** (`findRegions`, Find Regions button):

```javascript
// map_CURRENT.html:5329
function buildPlanFromLegacyDom() {
  const birth = getBirthParamsFromProfile();   // reads #chartProfile.selectedOptions[0].dataset.profile
  // ... returns { birth_year, birth_month, birth_day, birth_hour_utc }
}
```

`dataset.profile` is populated from `GET /chart-profiles` (→ `charts/chart_profiles.json`). It contains fields `date` and `time` in legacy string format. Supabase profile options have `data-profile-source="supabase"` and **no `dataset.profile`** — `getBirthParamsFromProfile()` returns `null` for them (line 1816: `if (!selectedOption.dataset.profile) return null`).

### 5. What is passed into map calculations (aura field / search regions)

`executeSearchPlan(plan)` receives `plan.birth` which is the output of `getBirthParamsFromProfile()` or `fetchEngineBirthForChartRecord()`. Both are broken for Supabase profiles (see below).

```javascript
// map_CURRENT.html:5392
const birth = plan.birth;
const basePayload = {
  birth_year: birth.birth_year,
  birth_month: birth.birth_month,
  birth_day: birth.birth_day,
  birth_hour_utc: birth.birth_hour_utc,
  ...
};
// → POST /aura-field or POST /find-regions
```

### 6. What is passed into Genie

**When Genie handoff is active** (app_shell → map via `prepareGenieRenderHandoff()`):

```javascript
// map_CURRENT.html:3201
async function resolveBirthParamsForGenieRender(payload) {
  if (!isAppShellGenieHandoffActive()) {
    return { ok: true, birth: getBirthParamsFromProfile(), source: "chart_profile" };
                                                            // ↑ legacy DOM, broken for Supabase
  }
  const urlChartRecordId = handoffChartRecordIdForBirth();  // reads URL ?chartRecordId=
  return fetchEngineBirthForChartRecord(urlChartRecordId);  // ← see §7 below
}
```

The `chartRecordId` IS correctly carried through the URL via `buildMapHandoffUrl()`. But the backend lookup fails.

**When no Genie handoff** (direct map access, no `?handoff=app_shell`):

Falls back to `getBirthParamsFromProfile()` (legacy DOM) — broken for Supabase.

Genie in `app_shell.html` receives only display data:

```javascript
// app_shell.html:1365
const r = activeRecord();
window.RelocationGenieVariableBuilder.mount(el, {
  chartRecordId: navContext.chartRecordId || r.chartRecordId,
  chartRecordName: r.displayName,
  onSearchMap(payload) { ... }
});
```

Genie in `app_shell.html` gets `chartRecordId` and `chartRecordName` — no birth data. Birth data is resolved on the map side.

### 7. What is passed into relocation calculations

**Popup chart path** (`fetchRelocatedChart`):

```javascript
// map_CURRENT.html:1823
async function fetchRelocatedChart(lat, lon) {
  const p = getActiveProfileBirthParams();  // = getBirthParamsFromProfile()
  if (!p) throw new Error("no_profile");   // ← throws for Supabase profiles
  const { year, month, day, birthHourUTC } = p;
  const response = await fetch(`/relocated-chart?lat=...&birth_year=${year}...`);
}
```

**Genie engine birth path** (`fetchEngineBirthForChartRecord`):

```javascript
// map_CURRENT.html:3179
async function fetchEngineBirthForChartRecord(chartRecordId) {
  const response = await fetch(`/chart-records/${chartRecordId}/engine-birth`);
  // → main_centerline_FIXER.py → local_product_store.py
  // → loads TEMPORARY_product_store.json
  // → looks for chart_record_id matching the UUID
  // → 404 for any real Supabase UUID (not in mock JSON)
}
```

Backend endpoint:
```python
# main_centerline_FIXER.py:2083
@app.get("/chart-records/{chart_record_id}/engine-birth")
def get_chart_record_engine_birth(chart_record_id: str):
    state = load_product_store(LOCAL_PRODUCT_STORE_SCAFFOLD)
    # LOCAL_PRODUCT_STORE_SCAFFOLD = scaffold/local_product/TEMPORARY_product_store.json
    return resolve_engine_birth_params(state, chart_record_id)
    # → raises ChartRecordBirthResolutionError("chart_record_not_found") for Supabase UUIDs
    # → HTTP 404
```

### 8. Paths still using local product store / hardcoded IDs

| Path | Data Source | For Supabase Profiles |
|---|---|---|
| `GET /chart-profiles` | `charts/chart_profiles.json` (3 entries) | Not included |
| `GET /chart-records/{id}/engine-birth` | `TEMPORARY_product_store.json` | 404 for Supabase UUIDs |
| `getBirthParamsFromProfile()` | `#chartProfile.dataset.profile` | Returns `null` |
| `app_shell.html` → `vm.chartRecords` | Supabase bridge (correct) | Works ✅ |
| `app_shell.html` UI rendering | Supabase bridge (correct) | Works ✅ |

---

## Question Answers

### Q1: If user creates Profile A and Profile B, then switches — will map calculations change?

**No.**

`switchChartRecord()` correctly updates `navContext.chartRecordId` and re-renders `app_shell.html`'s screens. When the user then navigates to the map:

- The `chartRecordId` UUID is carried in the URL as `?chartRecordId=<uuid>`.
- `map_CURRENT.html` marks this as "informational only — no map mutations" (line 998).
- `#chartProfile` is re-populated from `chart_profiles.json` (3 hardcoded profiles). No Supabase profile appears with birth data.
- All calculation paths (`getBirthParamsFromProfile`, `fetchEngineBirthForChartRecord`) fail for the Supabase UUID.

**Proof — key lines:**

```javascript
// map_CURRENT.html:997-999
if (lastAppShellHandoff) {
    console.info("[app-shell-handoff] Received (informational only — no map mutations):", ...);
}
```

```javascript
// map_CURRENT.html:1406-1412
// Phase 2.5B: bridge real Supabase profiles into #chartProfile so a
// #profileId=<uuid> handoff can select an actual profile. These options
// carry no birth math payload (profiles have no date/time), so we mark
// them with data-profile-source="supabase" and intentionally omit
// dataset.profile.
```

```javascript
// map_CURRENT.html:1816
if (!selectedOption || !selectedOption.dataset.profile) return null;
// ↑ returns null for any Supabase profile option
```

### Q2: Can two profiles produce different maps today?

**Yes, but only for profiles in `charts/chart_profiles.json`.**

There are 3 hardcoded profiles: `baseline_validated`, `edge_high_north`, `edge_southern`. Switching between these in `#chartProfile` produces different map calculations because their `dataset.profile` contains distinct `date`/`time` values.

Supabase profiles cannot produce different maps because they carry no birth data into any calculation path.

### Q3: Is there any place where profile selection updates UI only but not calculations?

**Yes — the entire `app_shell.html` layer.**

`switchChartRecord()` is correctly wired to:
- Re-render chart record page, library, birth data display
- Update `navContext.chartRecordId`
- Persist to localStorage
- Pass `chartRecordId` in the map handoff URL

But none of these actions changes the actual birth data used by `SwissEphemeris` (via `/relocated-chart`, `/aura-field`, `/find-regions`).

Additionally, Phase 2.5B in `map_CURRENT.html` adds Supabase profile names to `#chartProfile` as display entries — but these intentionally carry no `dataset.profile`, so selecting them in the map's own selector also breaks calculations.

### Q4: What is the next missing link?

```
navContext.chartRecordId (Supabase UUID)
         ↓
         ? ← MISSING LINK
         ↓
birth_year, birth_month, birth_day, birth_hour_utc
         ↓
SwissEphemeris → chart calculations → map overlay
```

The missing link is: **a backend endpoint that resolves a Supabase `profile_id` / `chart_record_id` to UTC birth parameters by reading from the `birth_records` table.**

Specifically needed:
1. `GET /chart-records/{profile_id}/engine-birth` must query Supabase `birth_records` when the ID is a Supabase UUID (not found in mock JSON).
2. `GET /profiles` must return birth data (`birth_date`, `birth_time_start`, `timezone_id`) alongside display data so `map_CURRENT.html` can populate `dataset.profile`.

One of these two is sufficient for v1. The second option (enriching the profiles endpoint) is slightly simpler and keeps `map_CURRENT.html` changes minimal.

---

## Verdict

**🔴 RED — Profile switching is cosmetic only with respect to calculations.**

| Layer | Status | Notes |
|---|---|---|
| `app_shell.html` profile selection UI | ✅ Correctly wired | Library, selector, persistence all work |
| `app_shell.html` → `map_CURRENT.html` URL handoff | ✅ `chartRecordId` in URL | Carries the UUID correctly |
| `map_CURRENT.html` receives `chartRecordId` | ⚠️ Informational only | Explicitly marked, no mutations |
| `#chartProfile` populated with Supabase birth data | ❌ Missing | Options present, `dataset.profile` intentionally absent |
| `/chart-records/{uuid}/engine-birth` resolves Supabase UUID | ❌ Missing | 404 for real UUIDs |
| Legacy popup / relocated chart | ❌ Blocked | Returns `null` → `"no_profile"` error |
| Aura field / search regions | ❌ Blocked | `birth` is `null` from Supabase profile |
| Genie render with `chartRecordId` | ❌ Blocked | Backend returns 404 for Supabase UUID |

---

## Smallest Safe Next Implementation Step

**Step 5E — Birth Record Engine-Birth Endpoint (Supabase)**

Create a new authenticated FastAPI endpoint that resolves a Supabase `profile_id` to UTC birth parameters:

```
GET /supabase/chart-records/{profile_id}/engine-birth
```

Reads from Supabase `birth_records` table (joining `places` for `timezone_id`), converts `birth_date` + `birth_time_start` + `timezone_id` to `birth_year/month/day/birth_hour_utc` (same output shape as the existing `local_product_store.py` function).

Then modify `map_CURRENT.html`'s `fetchEngineBirthForChartRecord()` to:
1. Try the new `/supabase/chart-records/{id}/engine-birth` endpoint first
2. Fall back to `/chart-records/{id}/engine-birth` (mock store) if the first returns 404

This is a single addition that unblocks all three blocked paths (Genie, popup chart, and aura field) without touching `app_shell.html`, the Supabase schema, or any existing logic. The existing mock profiles continue to work exactly as before.

**Prerequisite:** The FastAPI server must have a Supabase service-role or authenticated-user connection to read `birth_records`. This exists already via `services/supabase_client.py`.

**Estimated scope:** One new Python endpoint (~40 lines) + one change to `fetchEngineBirthForChartRecord()` in `map_CURRENT.html` (~10 lines).

---

## Files Traced (Read-Only)

| File | Role |
|---|---|
| `app_shell.html` | Profile state, chart record wiring, handoff building |
| `map_CURRENT.html` | Map calculation engine, birth resolution, Genie rendering |
| `main_centerline_FIXER.py` | FastAPI endpoints: `/chart-profiles`, `/chart-records/*/engine-birth`, `/relocated-chart` |
| `local_product_store.py` | `resolve_engine_birth_params()` — reads from `TEMPORARY_product_store.json` |
| `charts/chart_profiles.json` | 3 hardcoded profiles with `date`/`time` fields |
| `genie_map_engine_adapter.js` | Genie payload structure (not detailed here; birth params flow through from map_CURRENT) |
| `supabase_store_bridge.js` | Builds `vm.chartRecords` from Supabase — correct for UI, not connected to calculation engine |
