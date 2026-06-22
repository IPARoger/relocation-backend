# 224 — PROFILE-NATAL-WHEEL-1 Closeout

**Date:** 2026-06-22  
**Ticket:** PROFILE-NATAL-WHEEL-1  
**Audit gap:** `results/212_profile_wiring_reality_audit.md` §1.4 — Profile lacked natal wheel and natal fact hydration  
**Status:** **DONE**

---

## Summary

Profile `#/chart-record` now hydrates the chart owner's **natal** facts using existing canonical machinery — no new endpoint, no alternate architecture, no layout redesign.

| Doctrine item | Status | Implementation |
|---------------|--------|----------------|
| Natal wheel | **Live** | `renderRelocatedWheelHtml(canonical)` via `renderProfileNatalChartHtml` |
| Natal PIH | **Live** | `renderPihTableRowsFromCanonical` |
| Natal AIS | **Live** | `renderAisSinglePlaceHtml` |
| Natal A2A | **Live** | `renderA2aSinglePlaceHtml` |

---

## Implementation (`app_shell.html` only)

### UI slot

`screenChartRecord()` — **Natal chart** panel with `#rm-profile-natal-facts` (below Identity, above Notes).

### Hydration

`hydrateProfileNatalFacts(root)`:

1. Resolves birth place coords via `resolveBirthPlaceId` → `resolvePlaceLatLon`
2. Fetches birth engine payload: `GET /supabase/chart-records/{id}/engine-birth`
3. Calls `fetchCanonicalRelocatedChart({ birth, lat, lon, placeName, locationKind: "natal" })`
4. Renders `renderProfileNatalChartHtml(canonical, false)` into the container
5. Race-safe via `_profileNatalToken` + route/container guards

### Renderer

`renderProfileNatalChartHtml(canonical, dignitiesOn)` — mirrors relocated chart fact stack:

- Natal wheel → `renderRelocatedWheelHtml`
- Planet houses → `renderPihTableRowsFromCanonical` + `rm-pih-table`
- AIS → `renderAisSinglePlaceHtml`
- A2A → `renderA2aSinglePlaceHtml`

Post-render: `hydrateProfileNatalFacts(root)` wired in main render path.

---

## Requirements checklist

| Requirement | Met |
|-------------|-----|
| Existing canonical machinery | Yes — `/relocated-chart` + `canonical_chart` |
| `location_kind="natal"` | Yes — `locationKind: "natal"` in fetch |
| Reuse wheel renderer | Yes — `renderRelocatedWheelHtml` |
| Reuse existing tables | Yes — PIH / AIS / A2A single-place renderers |
| No new endpoint | Yes |
| No redesign | Yes — panel + headings only |
| No alternate profile architecture | Yes — extends `#/chart-record` in place |

---

## Validation

```text
python3 scripts/smoke_profile_natal_wheel.py
10/10 passed
```

| Check | Asserts |
|-------|---------|
| `static_natal_wheel_container` | `#rm-profile-natal-facts` on chart-record screen |
| `static_hydrate_natal_wheel` | `hydrateProfileNatalFacts` exists |
| `static_natal_location_kind` | `locationKind: "natal"` |
| `static_natal_reuses_wheel_renderer` | `fetchCanonicalRelocatedChart` + `renderProfileNatalChartHtml` |
| `static_post_render_wires_natal` | post-render hydration call |
| `static_birth_place_resolver` | `resolveBirthPlaceId` |
| `static_profile_natal_wheel_section` | wheel section |
| `static_profile_natal_pih_section` | PIH section |
| `static_profile_natal_ais_section` | AIS section |
| `static_profile_natal_a2a_section` | A2A section |

---

## Commit lineage

Implementation landed in two slices (same ticket scope):

| Commit | Scope |
|--------|-------|
| `d602959` | Initial natal wheel hydration + smoke (`PROFILE-RX-AS-VISIBILITY-FIX-1` Task C) |
| `2d58b7d` | Expanded to full natal facts (PIH/AIS/A2A) + smoke extensions (`COMPARISON-PROFILE-REALITY-FIX-1` Task B) |

This closeout formally closes **PROFILE-NATAL-WHEEL-1** against audit `212`.

---

## Not in scope

- Profile visual harmonization vs `profile_standard.html` mockup
- Dignities toggle on profile natal PIH (passed `false`; same as minimal wiring)
- Comparison / relocated chart changes

---

## Files

| Path | Role |
|------|------|
| `app_shell.html` | Profile natal hydration + renderer |
| `scripts/smoke_profile_natal_wheel.py` | Static contract smoke |
| `results/224_profile_natal_wheel_1_closeout.md` | This document |
