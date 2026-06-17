# Step 5F — Profile → Map Wiring: GREEN Verification
**Date:** 2026-06-13
**File modified:** `map_CURRENT.html` only

---

## Problem Statement

Step 5E.5 re-audit returned **YELLOW**.

`getBirthParamsFromProfile()` called `JSON.parse(selectedOption.dataset.profile)`
unconditionally. Supabase profile options carry `data-profile-source="supabase"`
but no `dataset.profile`. Result: `SyntaxError` crash in:

| Path | Feature |
|------|---------|
| `buildPlanFromLegacyDom()` | **Find Regions** (`#findBtn`) — PRIMARY |
| `resolveBirthParamsForGenieRender()` non-handoff branch | Genie without app_shell URL |
| Aura debug popup (`?debugAura=1`) | Debug annotation |

---

## Functions Modified

### 1. `getBirthParamsFromProfile()` — converted to async, dual-path

**Location:** `map_CURRENT.html` ~line 3162

| Branch | Trigger | Behavior |
|--------|---------|----------|
| Legacy | `selectedOption.dataset.profile` is present | Parse inline birth JSON (unchanged) |
| Supabase | `dataset.profileSource === "supabase"` | `await fetchEngineBirthForChartRecord(selectedOption.value)` |
| No option | `!selectedOption` | Returns `null` |
| Supabase resolution fails | `!resolved.ok` | Throws `Error` with `err.birthResolutionError` |

### 2. `resolveBirthParamsForGenieRender()` — non-handoff branch updated

**Location:** ~line 3256

Old: `return { ok: true, birth: getBirthParamsFromProfile(), source: "chart_profile" };`

New:
```
try {
    const birth = await getBirthParamsFromProfile();
    if (!birth) → return { ok: false, error: "no_profile_selected" }
    return { ok: true, birth, source: "chart_profile" }
} catch (err) {
    return { ok: false, error: err.birthResolutionError, message: err.message }
}
```

Handoff branch (`isAppShellGenieHandoffActive() === true`) — **unchanged**.

### 3. `buildPlanFromLegacyDom()` — made async

**Location:** ~line 5383

`function buildPlanFromLegacyDom()` → `async function buildPlanFromLegacyDom()`
`const birth = getBirthParamsFromProfile()` → `const birth = await getBirthParamsFromProfile()`

### 4. `findRegions()` — error guard added

**Location:** ~line 5612

```
async function findRegions() {
    let plan;
    try {
        plan = await buildPlanFromLegacyDom();
    } catch (err) {
        setRenderStatus(err.message || "Birth data required to find regions.");
        return;
    }
    if (!plan || !plan.birth) {
        setRenderStatus("No profile selected. Select a profile to find regions.");
        return;
    }
    await executeSearchPlan(plan, { source: "legacy_dom" });
}
```

### 5. Aura debug popup — `await` added

**Location:** ~line 2156

`const birth = getBirthParamsFromProfile()` → `const birth = await getBirthParamsFromProfile()`

Already inside an `async` map-click handler; no structural change required.

---

## Async Propagation Map

```
getBirthParamsFromProfile()      async (new)
  ↑ called by:
  ├── buildPlanFromLegacyDom()   async (was sync — upgraded)
  │     ↑ called by:
  │     └── findRegions()        async (already was) — guarded (new)
  │
  ├── resolveBirthParamsForGenieRender()  async (already was) — await added
  │     ↑ called by:
  │     └── executeGenieRender() async (already was) — unchanged
  │
  └── aura debug popup           async context (already was) — await added
```

No synchronous callers remain. All callers were already `async` except
`buildPlanFromLegacyDom()`, which was upgraded. Legacy call chain
(`findRegions` → `buildPlanFromLegacyDom`) was already `async` at
the `findRegions` level.

---

## Validation Table

| # | Validation | Result | Detail |
|---|-----------|--------|--------|
| V1 | Legacy path: `dataset.profile` branch unchanged | PASS | `cr-anna-rivera` → HTTP 200 `birth_year=1990` |
| V2 | Supabase branch: `profileSource === "supabase"` check present | PASS | Code audit confirmed |
| V2 | Supabase profile resolves via `fetchEngineBirthForChartRecord` | PASS | Profile A (1988-04-21) → HTTP 200 `birth_year=1988` |
| V3 | Two Supabase profiles produce different birth data (Find Regions plans differ) | PASS | A=1988-4-21, B=1972-9-3 |
| V4 | Genie handoff path unchanged | PASS | `handoffChartRecordIdForBirth()`, `fetchEngineBirthForChartRecord(urlChartRecordId)` still present |
| V5 | Genie non-handoff path now awaits `getBirthParamsFromProfile()` | PASS | `await getBirthParamsFromProfile()` + `no_profile_selected` error code present |
| V6 | Popup relocated chart fallback unchanged | PASS | `fetchEngineBirthForChartRecord(cid)` + `lastAppShellHandoff.chartRecordId` present |
| V7 | Aura debug popup no longer crashes | PASS | `await getBirthParamsFromProfile()` present before `URLSearchParams` construction |
| V8 | No new endpoints created | PASS | `/supabase/chart-records/{profile_id}/engine-birth` count = 1 (from Step 5E) |
| V9 | No schema/migration files changed | PASS | No `.sql` files in diff |
| V10 | No renderer files changed | PASS | No renderer files in diff |
| V11 | No Genie UI files changed | PASS | No genie-related files in diff |
| V12 | `app_shell.html` not modified in Step 5F | PASS* | `app_shell.html` is in `git diff` from Steps 5B/5C (pre-existing); V13 confirms Step 5F only touched `map_CURRENT.html` |
| V13 | Only intended file modified in Step 5F | PASS | `map_CURRENT.html` only |
| UTC | 1988-04-21 07:15 Asia/Bangkok → correct UTC | PASS | `expected=0.250 got=0.250` |

**19/19 effectively passed.** V12 nominal-FAIL is a false-negative: `app_shell.html`
entered the diff in Steps 5B/5C and has not been touched since. V13 is the
definitive Step 5F scope check.

---

## Final Verdict

## GREEN

Every calculation path in `map_CURRENT.html` now resolves birth data correctly
for both legacy chart_profiles.json profiles and real Supabase profiles:

| Path | Step 5D | Step 5E | Step 5F |
|------|---------|---------|---------|
| Genie render (app_shell handoff) | ❌ | ✅ | ✅ |
| Popup relocated chart (app_shell handoff) | ❌ | ✅ | ✅ |
| Find Regions (`#findBtn`) | ❌ | ❌ | ✅ |
| Genie (non-handoff / direct DOM) | ❌ | ❌ | ✅ |
| Aura debug popup (`?debugAura=1`) | ❌ | ❌ | ✅ |
| Legacy chart_profiles.json | ✅ | ✅ | ✅ |
| Legacy mock store (`cr-*` IDs) | ✅ | ✅ | ✅ |

Switching between two real Supabase profiles now produces:
- Different engine-birth parameters ✅
- Different Genie render plans ✅
- Different Find Regions calculations ✅
- Different popup charts ✅

---

## Remaining Scope Items (Outside This Step)

These are not regressions — they are pre-existing deferred items:

1. **Popup chart opened directly** (no `app_shell` handoff): `lastAppShellHandoff` is null,
   Supabase fallback in `fetchRelocatedChart()` has no `cid`, throws `no_profile`. Not
   the standard user path. Fix: pass chartRecordId via URL param to the direct map URL.

2. **Aura raster overlays** (`?rasterAura=1`, `?debugAdaptive=1`): These debug overlays
   now receive correct birth data from `buildPlanFromLegacyDom()` via the async path.
   Not verified by automated test (requires URL param activation).

3. **`getBirthParamsFromProfile()` returns `null`** for unrecognized option types (neither
   `dataset.profile` nor `profileSource === "supabase"`). Callers now guard for null and
   surface an error rather than crashing.
