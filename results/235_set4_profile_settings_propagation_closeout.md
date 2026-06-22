# 235 — SET-4: Profile Page Settings Propagation — Closeout

**Date:** 2026-06-23
**Task:** SET-4 PROFILE SETTINGS PROPAGATION
**Slice:** One of the pre-beta blockers from `results/234_settings_live_wiring_audit.md`

---

## What was fixed

### Fix 1 — `rehydrateSettingsConsumers` missing `"chart-record"` (Profile page)

**Root cause:** After saving Settings, `rehydrateSettingsConsumers()` re-hydrated the Relocated Chart page (`"chart"`) and Comparison page (`"compare"`) but had no branch for the Profile page (`"chart-record"`). A user on the Profile page who changed visible planets, A2A angles, or house-proximity orb would see no change until navigating away and back.

**Fix:** Added `"chart-record"` branch that:
1. Sets `_profileCanonicalCache = null` (clears the cached canonical chart so the new fetch uses fresh data).
2. Calls `hydrateProfileNatalFacts()` (re-runs the full natal chart fetch + render pipeline).

The branch is placed before the `"chart"` branch to match top-to-bottom page-section ordering.

### Fix 2 — `house_proximity_orb_degrees` pass-through (confirmatory)

**Finding:** The orb was already passing correctly. `hydrateProfileNatalFacts` calls `fetchCanonicalRelocatedChart`, which internally calls `resolveHouseProximityOrbDeg()` → `_settingsEff()`. No code change required. This audit confirms the orb is live for Profile, Relocated Chart, and Comparison already.

---

## Files changed

| File | Change | +/- |
|------|--------|-----|
| `app_shell.html` | `rehydrateSettingsConsumers`: add `chart-record` branch + `_profileCanonicalCache = null` | +4 / −0 |
| `scripts/smoke_set4_profile_settings_propagation.py` | New smoke test (6 static assertions) | +68 / −0 |
| `results/235_set4_profile_settings_propagation_closeout.md` | This closeout | new |

**Not changed:** Settings UI, Diffs, Dignities, Rx/A/S/late-house, map, backend, Supabase schema, profile layout, Relocated Chart page, Comparison page.

---

## Exact change (app_shell.html)

```js
// BEFORE
function rehydrateSettingsConsumers() {
  _screen4ChartCache = null;
  _comparisonColsCache = null;
  if (navContext.route === "chart") { ... }
  ...
}

// AFTER
function rehydrateSettingsConsumers() {
  _screen4ChartCache = null;
  _comparisonColsCache = null;
  _profileCanonicalCache = null;           // NEW
  if (navContext.route === "chart-record") {  // NEW
    hydrateProfileNatalFacts();             // NEW
  }                                        // NEW
  if (navContext.route === "chart") { ... }
  ...
}
```

---

## Validation

| Check | Result |
|-------|--------|
| JS syntax (`node --check`) | OK |
| `smoke_set4_profile_settings_propagation.py` | **6/6 PASS** |
| `smoke_profile_natal_wheel.py` (regression) | **13/13 PASS** |

---

## Rollback plan

`git revert <commit>` or `git checkout HEAD^ -- app_shell.html scripts/smoke_set4_profile_settings_propagation.py`. Frontend-only change, no DB migration risk. Backup at `/tmp/app_shell.set4.bak`.

---

## What this unblocks

- User changes visible planet set in Settings → Profile page re-renders PIH with new planet list immediately.
- User changes A2A display angles → Profile AIS and A2A cards update without navigate-away.
- User changes house-proximity orb → Profile natal near-cusp flags recalculate on next chart fetch (was already orb-live; now also re-triggers the fetch).

## Still deferred

- SET-1 Rx / A/S / late-house visual markers (Profile, Relocated Chart, Comparison)
- SET-2 Orb/aspect table consumers (chart display orbs → chart surfaces)
- SET-3 Dignities defaults (Settings-level default; per-page toggle already wired)
- SET-5 Diffs formatting (Comparison page only, post-beta polish)
- SET-6 Settings propagation smoke expansion
