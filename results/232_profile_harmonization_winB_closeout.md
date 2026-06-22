# 232 — PROFILE-HARMONIZATION WINDOW B Closeout

**Date:** 2026-06-22  
**Mode:** Implementation slice (Window B only)  
**Authority:** `results/229_profile_harmonization_audit.md`, `validation/mockups/beta/profile_standard.html`  
**Slices:** PH-4, PH-5, PH-6, PH-7, PH-8  
**Scope guard:** No Window C/D, no Diffs, no Comparison, no Settings, no backend/canonical/endpoint/repository changes.

---

## 1. Implementation summary

Window B moves the live Profile (`#/chart-record`) natal facts from a vertical stack of `simple` tables into the approved **tband** horizontal band, matching `profile_standard.html` structure. Content was **moved and re-laid-out only** — no chart truth, data source, or renderer math changed.

| Slice | What shipped |
|-------|--------------|
| **PH-4** | New `renderProfileTbandHtml()` produces `<div class="tband std rm-profile-tband">` with 4 cards in mockup order: **Angle in Sign → Planet in House → Aspect to Angle → Notes**. Each card has `card-head` + `ch-title` and a `tint-ais/pih/a2a` signature accent. Scoped CSS added under `#rm-profile-natal-facts` (grid `8fr 8fr 13fr 5fr`, responsive collapse at 1100px/680px). |
| **PH-5** | Notes moved out of its standalone `.panel` into the 4th tband column as a `notes-card notes-slot`. **Existing save path preserved** — same `#rm-chart-note`, `#rm-chart-note-msg`, `data-action="save-chart-note"` (delegated handler untouched). Placeholder updated to approved `Write or dictate a note…`. Toolbar/mic/popout intentionally **deferred** (not in PH-5). |
| **PH-6** | Profile PIH card is **house-only**. Shared `renderPihTableRowsFromCanonical()` now honors its already-present `showLongitude` option (previously computed but unused); Profile passes `showLongitude:false`. Relocated/Comparison keep the default (longitude shown) — backward compatible. |
| **PH-7** | Profile PIH card footer uses `pihDignitiesFooterHtml(on,"profile")`. New `"profile"` scope added to `getPihDignitiesEnabled` / `setPihDignitiesEnabled`; toggling re-renders **only** `#rm-profile-pih-slot` via `renderProfilePihTableHtml()` using cached canonical (`_profileCanonicalCache`), so Notes/AIS/A2A are not disturbed. Reuses the existing dignities renderer path (`pihHouseCellHtml` + `pihDignityClass`). |
| **PH-8** | New `renderProfileAisCardBodyHtml()` + `aisVgridCellHtml()` render AIS angles as a **deg · sign · min** `rm-ais-vgrid` (3-column baseline grid) instead of a single longitude string. Same data source (`canonical.angles`, `AIS_ANGLE_ROWS`, `getA2aDisplayAngles()` gating). |

**Renderer reuse (unchanged math):** `renderPihTableRowsFromCanonical`, `pihHouseCellHtml`, `renderA2aSinglePlaceHtml`, `formatSignDisplayHtml`, `formatAngleLabelHtml`, `getVisibleBodyNamesSet`, `getA2aDisplayAngles`. A2A keeps the existing single-place table (matrix + angle pills is **PH-9 / Window C** — not implemented).

**Resilience:** Hydration error branches (coords missing, birth data unavailable, relocated_failed, request failure) now render the tband shell with the message in the AIS/PIH/A2A bodies and **Notes still present**, so notes never disappear on chart-load failure.

---

## 2. Files changed

| File | Change | +/- |
|------|--------|-----|
| `app_shell.html` | screenChartRecord tband CSS + container; new profile tband renderers; `showLongitude` honored; profile dignities scope; hydration wiring (success + 4 error branches) | **+119 / −29** |
| `scripts/smoke_profile_natal_wheel.py` | Updated profile assertions to validate tband structure (PH-4..PH-8) | **+39 / −5** |
| `results/232_profile_harmonization_winB_closeout.md` | This closeout (new) | — |
| `results/232_profile_harmonization_winB_screenshots/` | before/after HTML + PNGs (new) | — |

**No backend, canonical_chart, endpoint, repository, Settings, Diffs, or Comparison files touched.**

---

## 3. Exact lines changed (anchors)

`app_shell.html`:
- **screenChartRecord()** — replaced `#rm-profile-natal-facts` loading block + standalone Notes `.panel` with a scoped `<style>` (profile tband rules) + the natal-facts container (Notes panel removed; now lives in tband).
- **renderProfileNatalChartHtml()** region — replaced the single function with: `aisVgridCellHtml`, `renderProfileAisCardBodyHtml`, `renderProfilePihTableHtml`, `renderProfileNotesCardHtml`, `renderProfileTbandHtml`, and a thin `renderProfileNatalChartHtml` wrapper.
- **renderPihTableRowsFromCanonical()** — `showLongitude` now gates the longitude `<td>`.
- **Declarations** — added `let _profilePihDignities = false;` and `let _profileCanonicalCache = null;` beside `_screen4PihDignities`.
- **getPihDignitiesEnabled() / setPihDignitiesEnabled()** — added `"profile"` scope branches.
- **hydrateProfileNatalFacts()** — cache reset at start; success path caches canonical, renders tband with `_profilePihDignities`, binds dignities toggle; 4 error branches render tband-with-notes.

---

## 4. Validation summary

| Check | Result |
|-------|--------|
| JS syntax (`node --check` on extracted shell script) | **OK** |
| Structural harness (executed actual renderers w/ mock canonical) | **20/20 PASS** — tband order, 3 tcards, tint classes; Notes id+save handler+msg+placeholder; PIH no-longitude header/value + pih-slot; profile dignities scope; AIS vgrid deg/sign/min (ASC 41.07° → `11° / Taurus / 04′`); shared renderer backward-compat (default keeps longitude, `showLongitude:false` drops it); error path keeps Notes |
| `scripts/smoke_profile_natal_wheel.py` | **13/13 PASS** |
| `scripts/smoke_dignities_pih.py` (live browser) | **PASS** — pihCells 44, colored 8, no console errors → shared PIH 3-col default intact for relocated/comparison |
| `scripts/smoke_comparison_a2a_matrix.py` | **10/10 PASS** |
| `scripts/smoke_dignities_house.py` | **15/15 PASS** |
| Before/after screenshots (served HTTP, ~1280px) | Captured; AFTER checks a–e **PASS** |

**AFTER visual confirmation (a–e):** four cards horizontal in order AIS · PIH · A2A · Notes; PIH = Planet+House only (no Longitude); AIS = deg/sign/min split; Dignities toggle at PIH foot; Notes textarea + Save Note.

**Live in-app validation:** the authenticated `#/chart-record` route is behind a login wall; deterministic harness + standalone HTTP render of the real renderers + CSS were used instead. Truth/data flow unchanged (renderers reused verbatim).

**Screenshots:**
- `results/232_profile_harmonization_winB_screenshots/01_before_stacked.png`
- `results/232_profile_harmonization_winB_screenshots/02_after_tband.png`
- Source: `before.html`, `after.html` (same folder)

---

## 5. Rollback plan

1. **Full revert:** `git revert <this commit>` (or `git checkout <prev> -- app_shell.html scripts/smoke_profile_natal_wheel.py`). Pre-change backup at `/tmp/app_shell.ph_winB.bak`.
2. **Surgical:** the change is additive + one shared-renderer guard. To restore the stacked layout without reverting helpers, repoint `hydrateProfileNatalFacts` success to render the prior stacked tables and re-add the standalone Notes `.panel` in `screenChartRecord`. The `showLongitude` guard is backward-compatible and safe to leave.
3. **No data/migration risk:** zero backend/DB/endpoint changes — rollback is frontend-only and instant.

---

## 6. Intentionally deferred (not in Window B)

| Item | Belongs to |
|------|-----------|
| A2A matrix + ASC/DSC/MC/IC/All angle pills | PH-9 (Window C) |
| Lower band (favorites / saved / comparisons relocation) | PH-10 (Window C) |
| Wheel disc/enlarge popout | PH-12 (Window C) |
| Notes toolbar (B/I/U/list) · mic · popout | PH-5 explicitly defers |
| Late-house `?` marker on PIH | optional half of PH-6, deferred (no house-proximity wiring added) |
| Static smoke slice formalization | PH-13 (Window D) |
| Warm paper palette / `identity_stamp.css` full theme | doctrine-deferred; tband uses app-shell tokens + tint accents |

---

## 7. Recommended next slice

**Window C → PH-9 first** (A2A matrix + angle pills on Profile, reusing comparison matrix builders with a single column), then PH-10 (lower band) and PH-12 (wheel popout). Defer PH-13 smoke formalization to Window D.

**Stop:** Window B complete. Not proceeding into Window C.
