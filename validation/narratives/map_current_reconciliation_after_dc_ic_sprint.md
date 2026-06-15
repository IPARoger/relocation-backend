# map_CURRENT.html reconciliation after DC/IC sprint

**Date:** 2026-05-18  
**Status:** Reconciled in working tree; **not committed** (per explicit instruction).

## Executive summary

- **Git / repo archives:** The UX described in `docs/current_sidebar_ux_audit.md` (e.g. `rmCitiesPane`, city pick list, removed `setMaxBounds`, shared popup pipeline) **did not exist in any committed revision** or in-repo HTML backup (`rg rmCitiesPane` / `city-search-pick` across `*.html` → **no hits**). The truth-grid backup (`backups/truth_grid_staged_asc_success_20260517_184401/map_CURRENT.html`) matches the **887-line** committed prototype, not the audit UI.
- **Cursor local history:** No recoverable `map_CURRENT.html` snapshot was found under `~/.cursor` from this environment (search returned **0** files). **Manual recovery** in Cursor **Local History** on the user machine may still surface the lost buffer if it was ever saved.
- **Actual loss:** The “full” sidebar/popup/geocoder UI was **uncommitted**; it was **not** retrievable from `git` after the sprint checkpoint. It was **reconstructed** from project docs/narratives + sprint backend contract, then merged with **sprint** behavior (DC/IC, `aspectAura`, cusp rows, angle-in-sign, staged contour overlays).
- **Bug fixed:** Pre-reconciliation tree had **`getSelectedAspectOverlay` referencing `planet` without defining it** (aspect overlay would throw at runtime). Restored correct `planet` read from `#overlayPlanet`.

## Stabilization follow-up (same product surface)

**Canonical notes:** `validation/narratives/stabilization_after_dc_ic_regressions.md` — corrective pass: **UI order/label ASC, DSC, MC, IC** with **DSC** (API **`DC`**); **compact popup** ASC+MC only; **bounded map** (`maxBounds` + viscosity); **Enter-only** city search (no sidebar pick list); **`?aspectAura`** = Gaussian **offset bands** for **ASC/DSC** aspect lines only (no MC/IC aura); **`doubleClickZoom`** + wheel tuning; panel legend with **`?debugGeometry` / `?showLegend` / `?traceConditions`**.

## What is present after reconciliation

| Capability | Present |
|------------|---------|
| Compact ~300px panel, section titles, tinted condition cards | Yes |
| Legend hidden by default; `?debugGeometry` or `?showLegend` | Yes |
| Reset map (○) control | Yes |
| **No** `setMaxBounds` (comment cites audit / dateline behavior) | Yes |
| `rmCitiesPane` + city markers on top pane, density by zoom | Yes |
| City search **feedback** + **pick list** (exact / prefix ≥4, pop-ranked) | Yes |
| Shared popup: `fetchRelocatedChart`, `buildRelocatedPopupHtml`, table alignment, DC/IC, cusp hint | Yes |
| Onboarding card + `sessionStorage` + skip via `skipOnboarding` / `debugGeometry` / `traceConditions` / `showLegend` | Yes |
| Panel select **wheel** + **spurious-change** guards | Yes |
| `?traceConditions` → `console.info("[traceConditions]", …)` on polygon debug bind | Yes |
| `?aspectAura` → wide low-opacity underlay for aspect **LineStrings** | Yes |
| Angle-in-sign **ASC / MC / DC / IC** | Yes |
| Aspect-to-angle **MC / ASC / DC / IC** + staged **ASC|DC|IC + aspect any** | Yes |
| `renderStatus` hidden unless `?debugGeometry` | Yes |
| `moveend` → refresh cities | Yes |

## Sprint parity vs commit `af89fd6`

| Sprint item | Reconciled file |
|-------------|-----------------|
| DC/IC in angle + overlay selects | Yes |
| `aspectAura` query flag | Yes |
| `angle_sign_conditions` + purple `angle_sign` polygons | Yes |
| Popup DC/IC + geometric cusp rows | Yes |
| `isStagedContourAngleOverlay` (ASC/DC/IC + aspect `any`) | Yes |
| Aura approximate weights | Yes |

## Conflicts resolved

- **Sprint-only minimal HTML** vs **audit UX:** Merged by **rewriting** `map_CURRENT.html` once (avoid incremental drift), keeping sprint **JS contract** with **audit** structure/CSS.
- **`setMaxBounds`:** Removed to match audit; tiles still use `bounds` on the layer.
- **Pre-reconciliation `planetC` typo:** Duplicate/erroneous `<option value="pluto">Uranus` removed during reconciliation.

## Validation performed (automated)

- `python3 scripts/validate_sprint_dc_ic.py` → **`overall_pass: true`** (relocated-chart DC/IC parity, DC/IC angle-in-sign containment smoke, aspect-to-DC linestring count). **Does not** load the HTML in a browser.

## Manual QA checklist (recommended before commit)

1. Open `http://127.0.0.1:8000/map_CURRENT.html` — page loads, panel scrolls, map pans.
2. City search: ambiguous name → **pick list**; single hit → fly + **same popup** as right-click.
3. **○** reset restores world view.
4. Right-click: **table** populates; **DC/IC** lines; cusp tint when API sends `near_cusp`.
5. Angle-in-sign **DC** + **truth_grid** (`?generation_mode=truth_grid`) — purple regions.
6. Aspect **DC** / **IC** — lines render; with `?aspectAura=1` no JS errors.
7. `?traceConditions=1` — console lines when opening polygon **Geometry Debug** popups (with `?debugGeometry=1`).
8. Native selects: no accidental changes from **click-through** (quick click regression).

## Files changed (uncommitted)

- `map_CURRENT.html` — full reconciliation rewrite.
- *This narrative* — `validation/narratives/map_current_reconciliation_after_dc_ic_sprint.md`.

## Remaining risks

- **No headless browser test** in CI; Leaflet behavior is **manually** verified.
- **Local History** might still hold a variant with minor differences; diff against this file if recovered.
- **Payload size / perf** unchanged logically; richer HTML/CSS increases download size slightly.

## Classification

- **Reconciliation map:** **Durable** pattern (one file, docs-aligned).
- **`aspectAura` / trace logging:** **Experimental / debug** surfaces.
