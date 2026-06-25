# Comparison Freeze Audit (H4)

**Date:** 2026-06-25  
**Rollback anchor:** `checkpoint/h4b_start_clean` (`e37bf9d`)  
**Canonical mockup:** `validation/mockups/beta/comparison_v5_beta.html`  
**Surface:** `#/compare` — `body.rm-beta-compare` in `app_shell.html`

## Executive summary

Comparison beta harmonization (H4) is **complete through slice 7**. The page renders a frozen visual shell: authority header, city bar, bottled AIS/PIH/A2A/CI blocks, and a sticky notes rail. Live data hydrates through the existing `hydrateComparisonColumns → _comparisonColsCache → render*ComparisonHtml` path. Profile, Relocated, Map, backend APIs, and wheel colors were not modified.

## Frozen layout regions

| Region | DOM / CSS anchor | Data wired | Notes |
|--------|------------------|------------|-------|
| Beta root | `body.rm-beta-compare`, `.rm-comparison-beta-root` | n/a | Legacy comparison chrome hidden |
| Authority header | `.cmp-profile-block`, `.cmp-zone-b` | partial | Zone B name/meta; profile block shell |
| City bar | `.city-bar-wrap`, `.city-bar-table` | yes | Place columns, hide/show chips |
| AIS bottle | `#rm-cmp-bottle-ais`, `.cmp-block-ais` | yes | Workspace `rm-cmp-sec-ais` hidden in beta |
| PIH bottle | `#rm-cmp-bottle-pih`, `.cmp-block-pih` | yes | Dignities toggle preserved |
| A2A bottle | `#rm-cmp-bottle-a2a`, `.cmp-block-a2a` | yes | `data-a2a-shape="matrix"` preserved |
| CI bottle | `#rm-cmp-bottle-ci`, `.cmp-block-ci` | **no** | `data-cmp-ci-wired="false"` placeholder |
| Notes rail | `.comparison-notes-rail`, `#cmp-notes-rail` | yes | `rm-cmp-note` + `saveComparisonSetNote` |
| Body grid | `.comparison-body-grid` | n/a | Main + 268px sticky aside |

## Hidden in beta (intentional)

- `.rm-comparison-legacy-chrome`
- `.screen-meta`, shell banner/footer chrome overrides
- Workspace sections: `ais`, `pih`, `a2a`, `city_intelligence` (`.rm-cmp-section[data-cmp-section=…]`)
- `.rm-cmp-workspace-places-row`

## Renderer ownership (must not change without new slice)

| Concern | Canonical functions |
|---------|---------------------|
| AIS comparison tables | `renderAisComparisonHtml`, `renderAisWorkbookSectionBody` |
| PIH comparison tables | `renderPihComparisonHtml`, `renderPihWorkbookSectionBody` |
| A2A matrix | `renderA2aComparisonHtml`, `renderA2aWorkbookSectionBody` |
| Bottle shells | `renderComparison{Ais,Pih,A2a,Ci}BlockShellHtml` |
| Notes | `renderComparisonNotesRailHtml`, `saveComparisonSetNote` |
| CI placeholder | `renderComparisonCiWorkbookSectionBody` (`wired: false`) |

**Do not** route comparison through Profile t-band renderers (`renderProfileAisCardBodyHtml`, etc.).

## Workspace state keys

`CMP_WS_SECTIONS`: `ais`, `pih`, `a2a`, `city_intelligence`, `notes`

Collapse toggles sync between bottled blocks and legacy workspace section bodies via `initComparisonWorkspace` / `applyComparisonWorkspaceToDom`.

## Slice commit map

| Slice | Description | Status |
|-------|-------------|--------|
| H4B-1 | Authority shell | `e37bf9d` |
| H4-2 | AIS bottle | `52cbf07` |
| H4-3 | PIH bottle | `662cf2e` |
| H4-4 | A2A bottle + angle pills | `ced5365` |
| H4-5 | Notes rail | `ad25532` |
| H4-6 | CI shell (placeholder) | this session |
| H4-7 | Freeze audit | this document |

## Regression smokes (required before any post-freeze change)

```bash
python3 scripts/smoke_h4b_comparison_authority.py
python3 scripts/smoke_h4_slice2_ais_shell.py
python3 scripts/smoke_h4_slice3_pih_shell.py
python3 scripts/smoke_h4_slice4_a2a_shell.py
python3 scripts/smoke_h4_slice5_notes_rail.py
python3 scripts/smoke_h4_slice6_ci_shell.py
python3 scripts/smoke_comparison_a2a_matrix.py
```

## Out of scope / future work

- City Intelligence content engine (`wired: false` in `CMP_MODULE_REGISTRY`)
- Full CI card grid per mockup `.ci-section` inner cards
- Comparison diff/hints keys (reserved in workspace schema)
- Non-beta comparison chrome removal beyond current CSS hide rules

## Verdict

**FROZEN** for beta comparison layout. Further product changes require a new harmonization slice with explicit scope and smoke additions.
