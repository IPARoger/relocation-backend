# Profile → Map Wiring Re-Audit
**Step 5E.5 — Post-Implementation Verdict**
Date: 2026-06-13

---

## Context

Step 5D produced a **RED** verdict.
Step 5E implemented:
- `GET /supabase/chart-records/{profile_id}/engine-birth` (FastAPI)
- UUID routing in `fetchEngineBirthForChartRecord()` (map_CURRENT.html)
- Supabase fallback in `fetchRelocatedChart()` (map_CURRENT.html)

This document re-examines every calculation path against the current codebase
and issues an updated verdict.

---

## Original Step 5D Failures (Recap)

| Failure | Root Cause |
|---------|-----------|
| Genie render fails for Supabase UUIDs | `/chart-records/{id}/engine-birth` returned 404 for UUIDs not in mock store |
| Popup relocated chart fails | `getBirthParamsFromProfile()` returned null (no `dataset.profile` on Supabase options) |
| Find Regions fails | `getBirthParamsFromProfile()` returned null → `null.birth_year` crash |
| Aura overlays fail | Same — all aura paths flow through `buildPlanFromLegacyDom()` → `getBirthParamsFromProfile()` |

---

## What Step 5E Fixed

### 1. New backend endpoint: `GET /supabase/chart-records/{profile_id}/engine-birth`

Reads `birth_records` + `places` from Supabase via service-role client.
Returns `{birth_year, birth_month, birth_day, birth_hour_utc, chart_record_id}` —
identical shape to the legacy endpoint.

### 2. UUID routing in `fetchEngineBirthForChartRecord()`

```
SUPABASE_UUID_PATTERN.test(chartRecordId)?
  → /supabase/chart-records/{id}/engine-birth   (new)
    200  → use Supabase birth data
    422  → surface "birth time required" error
    404  → fall through to legacy endpoint
  → /chart-records/{id}/engine-birth             (legacy, unchanged)
```

### 3. Supabase fallback in `fetchRelocatedChart()`

```
getActiveProfileBirthParams() returned something?
  → use it (legacy profile, dataset.profile present)
else
  → fetchEngineBirthForChartRecord(lastAppShellHandoff.chartRecordId)
    → resolves from Supabase if UUID, legacy store if not
```

---

## Q1 — Does Switching Profiles Change Chart Calculations?

**Answer: YES for the primary path (Genie). NO for the secondary path (Find Regions).**

### Primary path proof (Genie via app_shell handoff)

```
app_shell.html switchChartRecord(profileB_uuid)
  → navContext.chartRecordId = "7c8ec65f-..."
  → navigate to map_CURRENT.html?handoff=app_shell&profileId=7c8ec65f-...&genieRenderRef=...
  → maybeExecuteGenieRenderHandoff()
  → executeGenieRender(payload)
  → resolveBirthParamsForGenieRender()
  → isAppShellGenieHandoffActive() = true
  → handoffChartRecordIdForBirth() = "7c8ec65f-..."    ← Profile B UUID
  → fetchEngineBirthForChartRecord("7c8ec65f-...")
  → SUPABASE_UUID_PATTERN.test(...) = true
  → GET /supabase/chart-records/7c8ec65f-.../engine-birth
  → reads birth_records from Supabase for Profile B
  → returns birth_year=1985, birth_month=12, birth_day=21, birth_hour_utc=2.0
  → engine calculates from Profile B birth data  ✅
```

Validated in Step 5E: Profile A (1990-06-15) and Profile B (1985-12-21) return
different birth data from the same endpoint. Two different maps are produced.

### Secondary path (Find Regions button — `#findBtn`)

```
User clicks "Find regions"
  → findRegions()
  → buildPlanFromLegacyDom()
  → getBirthParamsFromProfile()
  → selectedOption.dataset.profile   ← undefined for Supabase options
  → JSON.parse(undefined)
  → SyntaxError: Unexpected token u in JSON  ❌  CRASHES
```

Switching to a Supabase profile and clicking Find Regions throws a JavaScript
runtime error. The calculation never reaches the engine.

---

## Q2 — Can Two Real Supabase Profiles Produce Different Maps Today?

**YES via Genie. NO via Find Regions.**

### Path that works (Genie, standard flow)

1. User in `app_shell.html` selects Profile A → profile_id = `fa9b575f-...`
2. Genie trigger opens `map_CURRENT.html` with `handoff=app_shell&chartRecordId=fa9b575f-...`
3. Endpoint returns `birth_year=1990, birth_month=6, birth_day=15, birth_hour_utc=7.5`
4. Engine calculates natal chart for 1990-06-15
5. User returns to `app_shell.html`, switches to Profile B → profile_id = `7c8ec65f-...`
6. Genie trigger opens `map_CURRENT.html` with `chartRecordId=7c8ec65f-...`
7. Endpoint returns `birth_year=1985, birth_month=12, birth_day=21, birth_hour_utc=2.0`
8. Engine calculates natal chart for 1985-12-21 → **different map** ✅

### Path that still fails (Find Regions)

Find Regions reads birth data only from `selectedOption.dataset.profile`
(line 3163 of `map_CURRENT.html`). Supabase profile options carry no `dataset.profile`
(intentionally omitted in Phase 2.5B). The function crashes before any calculation occurs.

---

## Q3 — Remaining Legacy / Broken Calculation Paths

### Path A — Find Regions (`#findBtn`) — **PRIMARY FEATURE**

```
findRegions()
  → buildPlanFromLegacyDom()            line 5384
  → getBirthParamsFromProfile()          line 3163
  → JSON.parse(selectedOption.dataset.profile)
       dataset.profile = undefined for Supabase options
       → SyntaxError crash
```

**Impact:** The main map exploration feature (house regions, aspect overlays, aura
field overlays, centerlines) cannot be triggered at all for Supabase profiles.
This is not a debug path — it is the primary user-facing calculation feature for
exploring natal charts on the map.

### Path B — Genie (non-handoff, direct DOM use) — **DEV / DEBUG**

```
resolveBirthParamsForGenieRender()
  → isAppShellGenieHandoffActive() = false  (no "handoff=app_shell" in URL)
  → getBirthParamsFromProfile()             line 3162
  → JSON.parse(selectedOption.dataset.profile)
       → SyntaxError crash for Supabase options
```

**Impact:** Minimal. This path is only reached when Genie is invoked without an
`app_shell` URL handoff (dev console, direct URL). Standard users always arrive
via `app_shell.html` which sets `handoff=app_shell`. Crash is contained to the
Genie block; it does not affect the legacy map or popup.

### Path C — Aura Debug Popup (`?debugAura=1`) — **DEBUG ONLY**

```
map click handler (debugAuraMode only)
  → fetchRelocatedChart()          ← ✅ fixed (Supabase fallback)
  → getBirthParamsFromProfile()    ← called AGAIN for the aspect-orb debug query
  → crash for Supabase options
```

**Impact:** Negligible. Only active when `?debugAura=1` is in the URL. Production
users never see this. The `fetchRelocatedChart()` part now works correctly; only
the secondary `aspect-orb-at-point` debug annotation call crashes.

### Path D — Aura Raster Overlays (`?rasterAura=1`, `?debugAdaptive=1`) — **DEBUG ONLY**

```
executeSearchPlan()
  → plan.birth = getBirthParamsFromProfile()   (via buildPlanFromLegacyDom)
  → renderAdaptiveAuraProgressive(birth, ...)
  → renderRasterAuraProgressive(birth, ...)
```

**Impact:** None in production. All aura rendering is gated behind URL parameters
(`?rasterAura=1`, `?debugAdaptive=1`, `?debugProgressiveReveal=1`). These are
archaeology/PoC overlays, not shipped features. The crash from Path A
(`buildPlanFromLegacyDom`) would already prevent reaching this point.

### Path E — `local_product_store.json` / `TEMPORARY_product_store.json`

The legacy `/chart-records/{id}/engine-birth` endpoint still reads from
`scaffold/local_product/TEMPORARY_product_store.json`. This file contains
`cr-anna-rivera`, `cr-jordan-lee`, `cr-research-event` — not real Supabase
profile IDs. However, since `fetchEngineBirthForChartRecord()` now routes UUIDs
to the Supabase endpoint before touching the mock store, this is not a blocking
concern. It remains as the fallback for non-UUID IDs (library charts, etc.).

### Path F — `chart_profiles.json` (hardcoded library profiles)

`loadChartProfiles()` fetches from `/chart-profiles`, which returns the hardcoded
profiles. These carry `dataset.profile` with birth date/time and work correctly
through `getBirthParamsFromProfile()`. This path is unaffected and correct.

---

## Q4 — Classification by Path

| Path | Feature | Users Affected | Verdict | Reasoning |
|------|---------|----------------|---------|-----------|
| Genie (app_shell handoff) | Primary chart rendering | All app_shell users | **GREEN** | UUID routes to Supabase endpoint; birth data resolves correctly; different profiles produce different charts. Proven by V1–V8 validation. |
| Popup relocated chart (app_shell handoff) | Map click → relocated chart | All app_shell users | **GREEN** | `fetchRelocatedChart()` fallback resolves UUID via Supabase endpoint using `lastAppShellHandoff.chartRecordId`. |
| Popup relocated chart (no handoff) | Map click when opened directly | Direct-URL users | **YELLOW** | `lastAppShellHandoff` is null if map opened without app_shell handoff; fallback has no `cid`; throws `no_profile`. Not the standard user path. |
| Find Regions (`#findBtn`) | House region / aspect / aura overlays | All users | **RED** | `getBirthParamsFromProfile()` crashes for Supabase profiles. Core production feature completely blocked. |
| Genie (non-handoff, direct DOM) | Dev/debug Genie | Dev only | **RED** | Same crash, but never reached by standard users. |
| Aura debug popup (`?debugAura=1`) | Debug annotation | Dev only | **RED** | `getBirthParamsFromProfile()` called after already-fixed `fetchRelocatedChart()`. Debug URL only. |
| Aura raster overlays (`?rasterAura=1`) | Debug overlays | Dev only | **RED** | Debug URL only. Blocked by Path A crash before reaching aura. |
| Legacy mock profiles (chart_profiles.json) | Hardcoded test charts | Dev / demo | **GREEN** | Fully functional; `dataset.profile` present; no change needed. |

---

## Q5 — Final Verdict

## YELLOW

**Primary calculation path (Genie via app_shell) is now fully wired to real Supabase
profiles. Profile switching produces different charts. The main user flow works.**

**However, Find Regions — the core manual calculation feature — still crashes for
Supabase profiles. It must be fixed before Supabase profiles can be considered
fully functional on the map.**

### Verdict progression

| Step | Verdict | What changed |
|------|---------|-------------|
| Step 5D | **RED** | Profile switching was entirely cosmetic; nothing reached the engine |
| Step 5E | **YELLOW** | Genie and popup now work end-to-end with real Supabase profiles |
| Next step | **GREEN** | Fix `getBirthParamsFromProfile()` / `buildPlanFromLegacyDom()` for Supabase profiles |

---

## Smallest Remaining Gap

**The single blocking issue:** `getBirthParamsFromProfile()` at line 3162 calls
`JSON.parse(selectedOption.dataset.profile)` without guarding for `undefined`.
Supabase profile options have `data-profile-source="supabase"` but no `dataset.profile`.

**Step 5F fix — two options:**

### Option A: Guard `getBirthParamsFromProfile()` + async resolution (recommended)

Convert `getBirthParamsFromProfile()` to an async function that:
1. If `selectedOption.dataset.profile` is present → parse it (legacy path, unchanged)
2. If `selectedOption.dataset.profileSource === "supabase"` → call
   `fetchEngineBirthForChartRecord(selectedOption.value)` and return the result

Then update the three callers:
- `buildPlanFromLegacyDom()` → make it async, await birth resolution
- `resolveBirthParamsForGenieRender()` non-handoff branch → already async
- Aura debug popup → already inside an async block

**Risk:** Low. Does not change the birth resolution logic; only adds async/await
to an existing sync function. Legacy profiles continue to work synchronously via
the existing parse path.

### Option B: Populate `dataset.profile` for Supabase options at load time

In `loadChartProfiles()`, when adding Supabase profile options, fetch birth data
from the new endpoint and populate `dataset.profile` in the engine-birth format.

**Risk:** Medium. Requires an async pre-fetch of all profile birth data at page
load; adds load time proportional to the number of profiles; may fail silently
if birth data is missing.

**Recommendation:** Option A. It is the minimal safe change. It reuses the
already-validated `fetchEngineBirthForChartRecord()` UUID path and requires no
schema changes, no new endpoints, and no data pre-loading.

---

## Summary Table

| Concern | Step 5D | Step 5E | Next (5F) |
|---------|---------|---------|-----------|
| Genie render (Supabase profile) | ❌ 404 | ✅ Resolved | — |
| Popup chart (Supabase profile) | ❌ null birth | ✅ Resolved | — |
| Find Regions (Supabase profile) | ❌ null birth | ❌ Crashes | Fix getBirthParamsFromProfile() |
| Aura debug (Supabase profile) | ❌ | ❌ Debug only | Fix (same root cause) |
| Legacy chart_profiles.json | ✅ | ✅ | — |
| Legacy mock store (`cr-*` IDs) | ✅ | ✅ | — |
| Two profiles → different maps (Genie) | ❌ | ✅ | — |
| Two profiles → different maps (Find Regions) | ❌ | ❌ | Fix (5F) |
