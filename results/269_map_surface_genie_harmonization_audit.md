# M2 — Map Surface QA + Genie Harmonization Audit

**Date:** 2026-06-26  
**Status:** Read-first audit complete (no implementation in this slice)  
**Production surface:** `map_CURRENT.html` only (`/map_CURRENT.html` via `main_centerline_FIXER.py`)  
**Authority:** `docs/BETA_MASTER_CHECKLIST.md`, `results/265_map_control_overlay_trust_audit.md`, `docs/canon/MATERIAL_SYSTEM_CANON.md`, `results/264_family_resemblance_final_audit.md`, `results/263_material_system_delta.md`

**Constraints honored:** No overlay math changes · no renderer substrate changes · no smoothing · no broad redesign.

---

## Executive summary

M1 closed the **control-truth** and **overlay-instrumentation** gaps (A–D). M2 asks whether the map **reads** as an instrument at beta zooms, whether **Genie** looks like the same product family as Profile / Comparison / Notes, and whether the **first overlay demo** is mechanically usable without coaching.

**Verdict:**

| Area | Status | Risk |
|------|--------|------|
| Map readability (instrument vs clutter) | **Partial** — M1-C city tiers help; medium zoom still dense; OSM raster ≠ chart stone ground | P1 |
| Genie / GV harmonization | **Outlier** — isolated `--gv-*` card on system-ui panel; not `family_resemblance` / G3 stack | P1 (visual) |
| Control truth (M1 regression) | **Pass (static)** — M1 smokes 90/90; single Search Map path; legacy hidden | P1 until PO QA |
| Overlay final-stage QA | **Pass (instrumentation)** — `data-overlay-final` reliable; jagged edges are truth artifacts | P0 trust (PO) |
| First overlay demo (mechanical) | **Partial** — path exists; ghost NOT still engine-deferred; screenshots blocked on auth | P0 |

**Nothing in Map detail is Release Ready.** PO must run an authenticated session pass before any column advances.

---

## Method

1. **Code + canon review** of `map_CURRENT.html`, `genie_map_engine_adapter.js`, M1 closeouts in `results/265_*`.
2. **Static smokes:** `smoke_m1a`–`m1d` (all pass) + new `smoke_m2_map_surface_audit.py` (18/18).
3. **Screenshot attempt:** Playwright against `:8004`. Unauthenticated loads redirect to `auth.html` (expected). Authenticated capture blocked: sandbox has no outbound Supabase DNS; `/config/supabase` project ref ≠ `.env.staging` ref when network available — storage key must match live config URL.
4. **Visual claims** below marked **(PO)** where screenshot evidence is missing.

Evidence folder: `validation/mockups/beta/screenshots/m2_map_genie_audit/` — contains **auth-redirect placeholders only** until PO re-captures with session.

---

## 1. Map readability QA

### 1.1 Zoom ladder (code + partial capture)

| Zoom band | Policy (M1-C) | Readability assessment |
|-----------|-----------------|------------------------|
| **World (z≤2)** | cap 14, minPop 5M | Major hubs only; coastlines from OSM tiles; **instrument-like** at this scale **(PO)** |
| **Continent (z3–4)** | cap 14–20 | Country context readable; borders from raster tiles, not custom vector emphasis |
| **Country (z5)** | cap 32, minPop 1M | Major labels appear at z≥5 (`rm-city-label--major`); hierarchy emerging |
| **Region / city (z6–7)** | cap 42–52 | **Worst clutter band** — up to 42–52 markers + major permanent tooltips; still better than pre-M1-C uncapped spray |
| **Medium clutter (z6)** | intentional stress test | Tiered radii (major/mid/minor) + population sort prevents bubble-cloud at cap, but **Northeast US / Western Europe still busy** **(PO)** |
| **City (z8+)** | cap 60, minPop 50k | Click targets shrink (minor r=4); labels only on major |

**City hierarchy (implemented):**

- `getCityMarkerTier`: major ≥1M, mid ≥250k, minor ≥50k.
- `getCityMarkerStyle`: distinct radius/weight/color; major white fill + heavy outline.
- Viewport cap via `CITY_VIEWPORT_CAP_BY_ZOOM` — highest population wins inside bounds.

**Label readability:** Major cities use permanent Leaflet tooltips with white halo (`text-shadow`). Mid/minor are dot-only — correct hierarchy, but at z6–7 major label stack can overlap in dense corridors **(PO)**.

**Country borders / coastlines:** Entirely from OSM raster (`tile` layer). No custom political linework. Acceptable for beta; does not match chart “stone instrument” material.

**Marker density:** Capped and tiered — **no longer an unbounded bubble cloud**. Residual risk: 42–60 dots in viewport at regional zoom still feels busy against faint map typography.

**Clickability:** `circleMarker` click → `openDatasetCityPopup`; `L.DomEvent.stopPropagation` on marker. Pane `CITY_MARKER_PANE` keeps z-order above tiles. Minor markers at r=3–4 are **hard targets on trackpads** **(PO)**.

**Orientation:** Standard north-up Leaflet; explore mode collapses panel (FLIP) — map remains geographically literate.

**Overlay interference:** House regions use truth_grid polygons (`smoothFactor: 0`). At regional zoom, semi-transparent fills can obscure city dots underneath — acceptable if overlay is the user’s intent; confusing if cities remain primary **(PO)**.

**Instrument vs bubble cloud:** **Improved post-M1-C** — population-sorted caps + tier styling move toward instrument. OSM colorful basemap + uncapped **feel** of dots at z6 prevents full “sextant” calm.

### 1.2 Findings — map readability

| ID | Severity | Finding |
|----|----------|---------|
| MR-1 | P1 | z6–7 remains the clutter peak; consider tighter cap or label collision policy (M2-B) |
| MR-2 | P2 | Mid-tier cities lack labels — users may not know which dot is which without click |
| MR-3 | P2 | OSM raster palette competes with overlay yellow/red/blue — material harmonization deferred |
| MR-4 | P2 | Minor marker hit targets below comfortable touch size |

---

## 2. Genie / GV visual harmonization

### 2.1 Family comparison

Reference family per `264_family_resemblance_final_audit.md`: Profile / Relocated / Comparison V5 — `rm-instrument-surface`, `tband_foundation.css`, Avenir 15.5px body, Iowan plates, G3 double-border cards, stone `--rm-paper` ground.

**Genie builder (`#gv-builder-host`):**

| Dimension | Chart family | Genie today | Aligned? |
|-----------|--------------|-------------|----------|
| Materials | Stone/paper G3 | Isolated `--gv-card` / `--gv-line` inline block; cool blue-gray `#fbfdff` | **No** |
| Typography | Avenir body + Iowan plate | GV 13–14px system stack inside card; ghost labels use `--serif` | **Partial** |
| Controls | D2 dropdown family site-wide | Custom `.gv-g-dd` / `.gv-gddmenu` — visually similar intent, separate CSS | **Partial** |
| Buttons | Instrument primary/secondary | Gold gradient Add + blue gradient Search Map | **Partial** (Genie v6 spec, not chart buttons) |
| Spacing | Fibonacci t-band | 12px card padding, 6–14px gaps — tighter than chart pages | **No** |
| Chrome | Recessed shell | Fixed 304px `#panel` — `#fafbfc` + `system-ui` — **debug-ship sidebar** | **No** |
| Carets | D2 caret grammar | `.gv-g-dd-car` 11px faint chevron | **Partial** |
| Condition chips | Table rows / G3 | `.gv-chip` with inset glow — own vocabulary | **Partial** |
| Ghost strip | N/A on charts | Glass-lite tokens, serif labels, Mute/Solo grid | **Unique to map** |
| Save disk | Notes save elsewhere | Floating `#rm-save-disk` + inline `gv-save-inline` (hidden in explore) | **Map-specific** |
| Hamburger / bottle | App shell nav | Explore-only dissolve — bottle FAB + `rm-mainmenu` | **Coherent within map** |
| Hover / disabled | Doctrine states | GV `:hover` on dd/chips; `:disabled` on search/add with opacity/grayscale | **Adequate** |
| NOT control | — | Hidden unless `ENGINE_EXCLUDE_SUPPORTED` — honest | **Yes** |

**Answer:** Genie does **not** yet look like part of the same product family as Profile / Comparison / Notes. It reads as a **polished map sidebar prototype** (Genie v6 lineage) on a **geography basemap**, not an instrument room on stone ground.

### 2.2 Findings — harmonization

| ID | Severity | Finding |
|----|----------|---------|
| GH-1 | P1 | Map panel uses `system-ui` + `#fafbfc`; chart pages use Avenir + stone ground |
| GH-2 | P1 | No `family_resemblance.css` / `tband_foundation.css` on map |
| GH-3 | P1 | GV tokens duplicate but do not share `--rm-paper` / G3 hatch vocabulary |
| GH-4 | P2 | Gold Search/Add gradients are Genie-specific — acceptable if documented as “map forge” accent |
| GH-5 | P2 | Explore chrome (ghost, disk, bottle) is internally consistent but unlike Settings/Help recession |

---

## 3. Control truth regression check

Static verification (M1 smokes + code):

| Check | Result |
|-------|--------|
| One canonical user-facing search path | **Pass** — `#gv-searchBtn` “Search Map”; `findBtn` + legacy sections `rm-panel-section-hidden` |
| Legacy controls hidden from beta path | **Pass** — planet/house/aspect legacy blocks aria-hidden |
| Mute/Solo behavior | **Pass (partial)** — re-executes plan; mute sets `enabled: false` |
| NOT honestly disabled/hidden | **Pass** — hidden unless `RelocationGenieMapEngineAdapter.EXCLUDE_POLARITY_SUPPORTED`; ghost NOT column gated same way |
| Save Investigation reachable in explore | **Pass** — `#rm-save-disk` + hamburger `rm-explore-menu-save`; inline save hidden in explore |
| Pin state understandable | **Pass (copy)** — sessionStorage scope documented; no Comparison consumer |
| In-map history replay | **Pass** — `replayAt` awaits plan; ghost sync via `syncGhostFromReplayedPlan` |
| Popup “View overlays here” | **Pass (code)** — `popup-action-view-overlays` → `buildPlanForPopupOverlayDiscovery` → `executeSearchPlan` |

**Residual mechanical risks (PO):**

- Ghost NOT still **client-filter only** when engine exclude unsupported (`exclude_not_supported_in_engine_v1`).
- History stack max 20 — no user-visible count.
- Profile picker required before search — first-time users must complete intake (P0 upstream).

---

## 4. Overlay QA (M1-B hooks)

**Do not screenshot during `settling`.** Wait for `html[data-overlay-final="true"]` or `rm-overlay-final` event.

| Check | Result |
|-------|--------|
| Jagged-edge severity at final stage | **Expected** — truth_grid 0.75° + `smoothFactor: 0` |
| Rough edges acceptable truth artifacts? | **Yes** per M1 doctrine — not bugs |
| Staging visibly confusing? | **Risk** — aspect searches pass coarse→medium→final; house-only completes immediately |
| Debug metadata hidden? | **Pass** — `#debugStatus` / `renderStatus` require `?debugGeometry=1`; `genieRenderStatus` requires `?debug=1`; `overlayDebug` URL-gated |

`window.__rmOverlayTrust` exposes `generation_mode`, `truth_grid_resolution`, `boundary_refined`, `final_complete` for automated QA.

---

## 5. First overlay demo path (mechanical)

Expected stranger path:

```
auth → map (profile loaded) → GV Add Variable → pick planet/house → Search Map
  → wait data-overlay-final=true → explore (panel collapses)
  → ghost strip shows tokens → click city OR View overlays here in popup
  → Save disk or hamburger Save investigation
```

| Step | Built? | PO verified? |
|------|--------|--------------|
| Enter map with profile | Yes (auth_guard) | **No** (screenshots blocked) |
| Build simple condition | Yes (GV builder) | **No** |
| Search Map | Yes | **No** |
| See overlay | Yes (truth_grid) | **No** |
| Understand ghost strip | Partial — fades in at 45% opacity; Mute/Solo labels terse | **No** |
| Inspect city/point | Yes (popup + relocated chart) | **No** |
| View overlays here | Yes (M1-C) | **No** |
| Save investigation | Yes (M1-D disk + menu) | **No** |

**Blockers for automated demo capture:** `auth_guard.js` requires Supabase session; Playwright must inject `sb-<project-ref>-auth-token` matching **`/config/supabase` URL**, not `.env` URL if they differ.

---

## 6. Screenshot evidence

**Folder:** `validation/mockups/beta/screenshots/m2_map_genie_audit/`

| File | Status |
|------|--------|
| `01_initial_map.png` | **Missing** — auth redirect captured instead in early attempts |
| `02_genie_builder_panel.png` | **Missing** |
| `03_world_zoom_z2.png` | Stale (auth page duplicate bytes) — **replace in PO session** |
| `04_country_zoom_z4.png` | Not captured |
| `04_overlay_final.png` | **Missing** — requires authenticated search + `data-overlay-final` |
| `06_city_clutter_medium_zoom_z6.png` | Stale (auth) — **replace** |
| `07_explore_mode.png` | **Missing** |
| `07b_ghost_strip.png` | **Missing** |
| `08_save_disk.png` / `08b_save_dialog.png` | **Missing** |
| `09_history_pin_controls.png` | **Missing** |
| `10_popup_view_overlays_here.png` | **Missing** |

**PO capture recipe:**

```bash
set -a && source .env.staging && set +a
export BASE_URL=http://127.0.0.1:8004
# Use /config/supabase url ref for localStorage key — see smoke_onboarding.py
# After Search Map:
# await page.waitForFunction(() => document.documentElement.getAttribute('data-overlay-final') === 'true')
```

---

## 7. Recommended implementation slices

Small, testable, in priority order:

### M2-A — PO screenshot + first-demo validation gate
- Authenticated Playwright capture script (storage key from `/config/supabase`).
- Checklist: all §6 shots at final overlay stage.
- **Exit:** manifest complete; no Release Ready promotion without human sign-off.

### M2-B — City clutter pass (readability, no overlay math)
- Tighten z6 cap or defer minor tier one zoom band.
- Optional: collision-aware major labels or raise minPop at z6.
- Smoke: extend `smoke_m1c` caps regression.

### M2-C — Genie panel material bridge (visual only)
- Link `family_resemblance.css` + panel `rm-instrument-surface` scoped to `#panel` only.
- Map `#gv-*` tokens → `--rm-paper` / ink aliases (no geometry).
- Smoke: `smoke_m2` + visual diff PO.

### M2-D — Explore chrome polish
- Ghost strip default opacity / hint copy (“active variables”).
- Save disk tooltip + first-save empty title guard.
- Pin tooltip reaffirm session scope.

### M2-E — First overlay demo copy (mechanical)
- One-line status under Search Map during `settling` (“Refining overlay…”).
- Walkthrough step asserts `data-overlay-final` before advance.
- No onboarding modal scope creep.

### M2-F — Popup overlay discovery UX
- Ensure “View overlays here” visible without scroll on mobile popup.
- Error toast if profile missing (already partially implemented).

**Explicitly deferred (per constraints):** overlay math, substrate, smoothing, D2 full token system, OSM basemap replacement.

---

## 8. Smoke / validation

| Script | Result |
|--------|--------|
| `smoke_m1a_map_control_truth.py` | PASS 24/24 |
| `smoke_m1b_overlay_truth.py` | PASS 23/23 |
| `smoke_m1c_popup_city_readability.py` | PASS 19/19 |
| `smoke_m1d_map_chrome_history.py` | PASS 20/20 |
| `smoke_m2_map_surface_audit.py` | PASS 18/18 (new) |

---

## 9. Checklist updates

See `docs/BETA_MASTER_CHECKLIST.md` (M2 row): Map UI risk elevated for Genie harmonization; M2-A marked next map slice; **no Release Ready** changes.

---

*End of M2 read-first audit.*


---

## M2-X implementation closeout (2026-06-26)

**Commit slice:** `map: harmonize production map visual language`

### Shipped (presentation only)

- Linked `/theme/family_resemblance.css`; `body.rm-instrument-surface.rm-map-workspace`
- Panel + chrome tokens aligned to warm instrument family (`--rm-*`); removed cool blue-gray chrome override
- Genie builder: `--gv-*` aliases to `--rm-*`; calmer card, full-width actions, instrument buttons
- Ghost strip quieter (lower default opacity, softer controls)
- Explore chrome: topbar, save disk, bottle, nav, profile picker, save dialog, popup actions
- City readability: z6 cap 34 / minPop 750k; major labels from z4 for 2M+ cities; warm label styling

### Unchanged (per rules)

Overlay math · truth grid · renderer · cache · smoothing · backend · search engine

### Smokes

M1-A/B/C/D + M2 static: all pass.

### PO still required

Authenticated screenshots · first-session overlay demo · family resemblance side-by-side sign-off before Release Ready.
