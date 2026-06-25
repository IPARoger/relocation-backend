# Comparison Surface Freeze Audit (H4)

**Roadmap ID:** H4 — Comparison visual harmonization  
**Audit slice:** H4-7 (freeze audit, read-only)  
**Audit date:** 2026-06-25  
**Auditor:** Cursor cloud executor (relay H4-7)  
**Audit HEAD:** `f084386` (`main`)  
**Rollback checkpoint:** `checkpoint/h4b_start_clean` → `e37bf9d`  
**Authority:** `relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md`

---

## Executive summary

The Comparison route (`#/compare`, `body.rm-beta-compare`) has received **shell/CSS/DOM harmonization** aligned to `validation/mockups/beta/comparison_v5_beta.html`. Slices 1–5 are **merged on `main` and smoke-verified**. Slice 6 (City Intelligence shell) is **implemented on branch** `origin/cursor/h4-slice6-ci-shell-4eae` (`9530090`) but **not merged to `main` at audit time**.

**Renderer/data paths are unchanged.** All bottled blocks wrap existing `render*ComparisonHtml` / `render*WorkbookSectionBody` output. Profile t-band renderers are not routed through Comparison.

This document freezes the Comparison **visual shell layer** only. Backend, Map, Settings, Profile, and Relocated surfaces remain out of scope.

---

## Freeze checkpoint

| Item | Value |
|------|-------|
| Tag | `checkpoint/h4b_start_clean` |
| Commit | `e37bf9d6d572973e9b4f834ed084cd2f39878fff` |
| Message | `comparison: harmonize authority system with beta shell` |
| Includes | H4B Slice 1 (authority shell) + all prior H3E work |

**Rollback (any smoke failure or morning reject):**

```bash
git reset --hard checkpoint/h4b_start_clean
# or: git reset --hard e37bf9d
```

---

## Slice completion matrix

| Slice | Goal | Commit | On `main`? | Smoke script |
|-------|------|--------|------------|--------------|
| **H4B-1** Authority shell | Beta header, `cmp-zone-b`, sticky city bar, `rm-beta-compare` | `e37bf9d` | Yes (checkpoint) | `smoke_h4b_comparison_authority.py` |
| **H4-2** AIS bottled shell | Collapsible `cmp-block-ais` around existing AIS output | `52cbf07` | Yes | `smoke_h4_slice2_ais_shell.py` |
| **H4-3** PIH bottled shell | Collapsible `cmp-block-pih` around existing PIH output | `662cf2e` | Yes | `smoke_h4_slice3_pih_shell.py` |
| **H4-4** A2A bottled shell | Collapsible `cmp-block-a2a` + angle pill strip | `ced5365` | Yes | `smoke_h4_slice4_a2a_shell.py` |
| **H4-5** Notes rail | 268px sticky `comparison-notes-rail` | `ad25532` | Yes | `smoke_h4_slice5_notes_rail.py` |
| **H4-6** CI shell | Collapsible `ci-section` placeholder (`data-ci-wired="false"`) | `9530090` | **No** (branch only) | `smoke_h4_slice6_ci_shell.py` |
| **H4-7** Freeze audit | This document | — | — | `test -f COMPARISON_FREEZE_AUDIT.md` |

**Commits on `main` since checkpoint (comparison product code only):**

```
ad25532 comparison: add notes rail shell (H4 slice 5)
ced5365 comparison: add A2A bottled block shell (H4 slice 4)
662cf2e comparison: add PIH bottled block shell (H4 slice 3)
52cbf07 comparison: add AIS bottled block shell (H4 slice 2)
```

---

## Authorized scope (Comparison shell only)

### In scope — frozen as implemented

| Layer | Elements |
|-------|----------|
| **Body class** | `body.rm-beta-compare` toggled when `navContext.route === "compare"` |
| **Root wrapper** | `.rm-comparison-beta-root[data-beta-comparison-visual="true"]` |
| **Authority header** | `.cmp-profile-block` → `renderComparisonZoneBHtml` (zone-b name/meta/tools) |
| **City bar** | `#rm-cmp-city-bar-mount` → `renderComparisonCityBarHtml` (sticky horizontal place strip) |
| **Body grid** | `.comparison-body-grid` — two-column layout (main + notes rail) |
| **Bottled blocks** | `#rm-cmp-bottle-ais`, `#rm-cmp-bottle-pih`, `#rm-cmp-bottle-a2a` with collapse toggles |
| **A2A chrome** | `.cmp-angle-pills` / `.cmp-angle-pill` angle tab strip in A2A header |
| **Notes rail** | `#cmp-notes-rail.comparison-notes-rail` — entity-owned `comparison_set` notes |
| **Legacy hide** | `.rm-comparison-legacy-chrome` hidden; legacy `rm-cmp-section` AIS/PIH/A2A hidden in beta |
| **Nav** | `COMPARISON_BETA_NAV` used when route is `compare` |

### Out of scope — DO NOT TOUCH (frozen elsewhere)

| Surface | Status |
|---------|--------|
| Profile (`rm-beta-profile`, `#/chart-record`) | **FROZEN** |
| Relocated (`rm-beta-relocated`, `#/chart`) | **FROZEN** |
| Map | **FORBIDDEN** |
| Settings | **FORBIDDEN** |
| Auth / account drawer behavior | **FORBIDDEN** |
| Backend / DB / APIs | **FORBIDDEN** |
| `/relocated-chart` contract | **FORBIDDEN** |
| Wheel colors / SVG renderer | **FORBIDDEN** |
| Comparison set create/archive/state APIs | **FORBIDDEN** (use existing) |
| CI content engine (slice 6 shell only; no wiring) | **NOT WIRED** |

---

## Surface inventory (`app_shell.html`)

### Shell render functions (H4 additions)

| Function | Purpose |
|----------|---------|
| `renderComparisonZoneBHtml(r)` | Profile authority block (zone-b) |
| `renderComparisonCityBarHtml(origin, cs, ws)` | Sticky city comparison bar |
| `renderComparisonAisBlockShellHtml(ws)` | AIS bottled chrome wrapper |
| `renderComparisonPihBlockShellHtml(ws)` | PIH bottled chrome wrapper |
| `renderComparisonA2aAnglePillsHtml(ws)` | A2A angle tab pills |
| `renderComparisonA2aBlockShellHtml(ws)` | A2A bottled chrome wrapper |
| `renderComparisonNotesRailHtml(cs)` | Sticky notes aside |

### Data render functions (unchanged — ownership preserved)

| Function | Role |
|----------|------|
| `hydrateComparisonColumns(root)` | Fetches relocated facts; populates `_comparisonColsCache` |
| `renderAisComparisonHtml` / `renderAisWorkbookSectionBody` | AIS table data |
| `renderPihComparisonHtml` / `renderPihWorkbookSectionBody` | PIH table data |
| `renderA2aComparisonHtml` / `renderA2aWorkbookSectionBody` | A2A matrix (`data-a2a-shape="matrix"`) |
| `refreshAisWorkbookSection` / `refreshPihWorkbookSection` / `refreshA2aWorkbookSection` | Re-hydrate bottled bodies from cache |
| `saveComparisonSetNote` | Entity-owned notes persistence (API unchanged) |

### Live data path (verified intact)

```
hydrateComparisonColumns → _comparisonColsCache → render*WorkbookSectionBody → bottled shell innerHTML
```

**No Profile t-band routing.** `renderProfileAisCardBodyHtml` / `renderProfilePihTableHtml` appear only in Profile/Relocated contexts, not in Comparison bottled blocks.

### CSS scope

- **88** rules/selectors under `body.rm-beta-compare`
- All H4 visual rules are scoped to `body.rm-beta-compare` — no global leakage to Profile or Relocated

### Workspace state sync

- Collapse toggles (`cmp-toggle-bottle-ais|pih|a2a`) persist to `collapsed_sections` via `initComparisonWorkspace` / `scheduleComparisonWorkspaceSave`
- Dual-sync: bottled toggles also update legacy `rm-cmp-sec-*` bodies (legacy sections hidden in beta, state kept for compatibility)
- Notes rail: `cmp-notes-hide` / `cmp-notes-show` toggle `.comparison-notes-rail.collapsed` (DOM-only, not persisted)

---

## Files changed since checkpoint (product surface)

| File | Δ since `e37bf9d` | Notes |
|------|-------------------|-------|
| `app_shell.html` | +428 / −26 lines | Comparison shell/CSS/DOM only |
| `scripts/smoke_h4b_comparison_authority.py` | +3 | Minor assertion update |
| `scripts/smoke_h4_slice2_ais_shell.py` | +70 (new) | Slice 2 static smoke |
| `scripts/smoke_h4_slice3_pih_shell.py` | +74 (new) | Slice 3 static smoke |
| `scripts/smoke_h4_slice4_a2a_shell.py` | +78 (new) | Slice 4 static smoke |
| `scripts/smoke_h4_slice5_notes_rail.py` | +78 (new) | Slice 5 static smoke |

No `theme/*` changes. No backend files. No Profile/Relocated route changes in comparison commits.

---

## Smoke verification matrix (audit run 2026-06-25)

| Script | Result | Notes |
|--------|--------|-------|
| `smoke_h4b_comparison_authority.py` | **PASS 14/14** | Authority shell |
| `smoke_h4_slice2_ais_shell.py` | **PASS 10/10** | AIS bottle |
| `smoke_h4_slice3_pih_shell.py` | **PASS 11/11** | PIH bottle |
| `smoke_h4_slice4_a2a_shell.py` | **PASS 14/14** | A2A bottle + pills |
| `smoke_h4_slice5_notes_rail.py` | **PASS 15/15** | Notes rail |
| `smoke_comparison_a2a_matrix.py` | **PASS 10/10** | Matrix shape + diffs |
| `smoke_h2_profile_transplant.py` | SKIP | Not on disk in this workspace |
| `smoke_h3e_relocated_shell_completion.py` | SKIP | Not on disk in this workspace |

All available H4 smokes pass on audit HEAD.

---

## Doctrine compliance

| Doctrine | Status |
|----------|--------|
| Mockup authority (`comparison_v5_beta.html`) | Shell layout ported; legacy chrome hidden |
| Entity-owned notes (`comparison_set`) | Preserved — `saveComparisonSetNote` + `rm-cmp-note` in rail |
| No per-block notes resurrection | Confirmed — single rail notes textarea |
| A2A matrix shape (`data-a2a-shape="matrix"`) | Preserved in `renderA2aComparisonHtml` |
| No Profile t-band collapse import | Confirmed — separate `cmp-block` collapse model |
| No hidden AIS shortcut | Confirmed — explicit `renderAisComparisonHtml` family |
| CI content engine | **Not wired** on `main`; slice 6 branch has shell-only placeholder |

---

## Known gaps and pending integration

1. **Slice 6 not on `main`.** City Intelligence collapsible shell exists on `origin/cursor/h4-slice6-ci-shell-4eae` (`9530090`, VERIFIED closeout on branch). Merge required before H4 slice queue is fully complete on trunk.
2. **Profile/Relocated regression smokes missing** from workspace (`smoke_h2_*`, `smoke_h3e_*` not on disk). Cannot statically verify frozen surfaces from this environment; rely on separate CI or manual check.
3. **Legacy workspace panel** (`comparisonWorkspacePanelHtml`, `rm-cmp-section`) remains in DOM under `.rm-comparison-legacy-chrome` / hidden sections — intentional compatibility layer, not user-visible in beta.

---

## Morning review checklist

- [ ] `git log e37bf9d..HEAD --oneline -- app_shell.html scripts/smoke_h4*` — expect ≤5 comparison commits on `main` (+ slice 6 if merged)
- [ ] Each commit message matches slice table (`comparison: add … (H4 slice N)`)
- [ ] `git diff e37bf9d..HEAD --stat -- app_shell.html scripts/smoke_h4*` — only comparison shell files
- [ ] Run full smoke battery once on target branch
- [ ] Merge slice 6 branch if not yet on `main`
- [ ] If anything feels wrong: `git reset --hard checkpoint/h4b_start_clean`

---

## Freeze verdict

| Criterion | Status |
|-----------|--------|
| Comparison shell harmonization (slices 1–5) | **FROZEN** on `main` |
| Renderer/data ownership | **INTACT** |
| Frozen surfaces untouched | **NO COMPARISON COMMITS** touched Profile/Relocated/Map/Settings/backend |
| Slice 6 CI shell | **PENDING MERGE** to `main` |
| H4-7 audit artifact | **THIS FILE** |

**Comparison visual shell (H4 slices 1–5) is frozen pending human merge review. Slice 6 integration remains open.**
