# CHART-TRUTH-FIX-1 Closeout
**Date:** 2026-06-21  
**Task:** Implement three pre-beta chart-truth fixes from `results/151_chart_truth_audit_1.md`  
**Files changed:** `main_centerline_FIXER.py`, `map_CURRENT.html`, `app_shell.html`,
`scripts/smoke_saved_investigations.py`, `scripts/smoke_settings_account.py`, `scripts/smoke_settings_navigation.py`

---

## What Changed

### FIX 1 — Remove Silent Default Birth Params (`main_centerline_FIXER.py`)

**Audit finding addressed:** `/relocated-chart` had hardcoded `birth_year=1976, birth_month=1,
birth_day=13, birth_hour_utc=12.78333` as parameter defaults. Any client call that omitted any of
these four params silently received a chart calculated for the wrong person, with no error.

**Change:** Removed all four defaults. FastAPI now returns **422 Unprocessable Entity** if any
birth parameter is missing.

```python
def relocated_chart(
    lat: float,
    lon: float,
    birth_year: int,
    birth_month: int,
    birth_day: int,
    birth_hour_utc: float,
):
```

**Smoke:** `be_relocated_chart_422_on_missing_birth` in `smoke_settings_account.py`.
- `GET /relocated-chart?lat=40.0&lon=-74.0` → **422** (PASS)
- `GET /relocated-chart?lat=40.0&lon=-74.0&birth_year=1990&...` → **200** (PASS)

---

### FIX 2 — Saved Investigation Birth Anchoring (`map_CURRENT.html`)

**Audit finding addressed:** `buildPlanFromSavedConditions` called `getBirthParamsFromProfile()`
at replay time, using the currently active profile. Switching profiles after saving an investigation
caused it to replay with the wrong birth data.

**Save path:** `saveCurrentInvestigation` now calls `fetchEngineBirthForChartRecord(profileId)`
before building `conditions_json` and snapshots all four birth fields plus `chart_record_id` into it.
Failure is non-blocking with a console warning.

**Replay path:** `buildPlanFromSavedConditions` checks for anchored birth params first:

```javascript
if (c.chart_record_id && Number.isFinite(c.birth_year) && ...) {
    birth = { birth_year: c.birth_year, ... };  // use saved anchor
} else {
    // Legacy fallback: old investigations lack anchored birth params.
    birth = await getBirthParamsFromProfile();
}
```

**Smoke:** `be_birth_anchored` added to `smoke_saved_investigations.py`.
Test `cond` now includes all birth fields; assertion verifies they round-trip through the backend.

---

### FIX 3 — Disable North/South Node Controls (`app_shell.html`)

**Audit finding addressed:** Node toggles appeared functional (saved to DB) but the engine never
calculates Nodes. Users enabling them received false confirmation with no actual chart effect.

**Changes:**
1. `north_node` and `south_node` in `ADDITIONAL` array: always `disabled: true`, always
   `checked: false` — regardless of DB value.
2. Disclosure note added: "North and South Node calculations are not yet available. Coming soon."
3. `bodyIds` in the save handler reduced to `["chiron"]` — Nodes can never be saved as enabled.

**Smoke:** `fe_nodes_disabled` and `fe_nodes_unchecked` added to `smoke_settings_navigation.py`.

---

## Audit Findings Fixed

| Finding | Status |
|---|---|
| CRITICAL-1: `/relocated-chart` silent default birth params | FIXED |
| CRITICAL-2: Saved investigation replay uses active profile birth | FIXED |
| CONCERN-1: North/South Node toggles mislead users | FIXED |

---

## Remaining Chart-Truth Risks

1. **Old saved investigations:** Investigations saved before this fix have no birth anchor.
   Replay falls back to active profile birth (legacy behavior, clearly commented in code).

2. **Comparison cache staleness** (`_comparisonColsCache`): Cleared on profile navigation.
   Low-risk; not addressed in this slice.

3. **Hardcoded Placidus in engine:** `/relocated-chart` always uses Placidus regardless of
   house system setting. Documented in `results/150_settings_reality_audit_1.md`; tracked
   separately as a settings-wiring gap.

4. **Birth fetch failure at save time:** If `fetchEngineBirthForChartRecord` fails (e.g. cold
   network), the investigation saves without birth anchoring. Fallback activates on replay.
   Acceptable for v1; UI-level warning is a future improvement.

---

## Smoke Results

| Smoke | Result | Notes |
|---|---|---|
| `smoke_settings_account.py` | **23/23 PASS** | Includes `be_relocated_chart_422_on_missing_birth` |
| `smoke_saved_investigations.py` | Infra failure | Supabase magic link expired — pre-existing. `be_birth_anchored` assertion added. |
| `smoke_settings_navigation.py` | Infra failure | Same expired magic link. `fe_nodes_disabled` + `fe_nodes_unchecked` added. |
| `smoke_map_current.py` | Infra failure | Same. |

Playwright smokes require a live Supabase session. The backend-only assertions in
`smoke_settings_account.py` confirm FIX-1 is operational against the live server on port 8004.
