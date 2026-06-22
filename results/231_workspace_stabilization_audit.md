# 231 — WORKSPACE STABILIZATION AUDIT

**Date:** 2026-06-22  
**Mode:** Read-only audit (no code changes, no commits)  
**Scope:** Untracked and artifact inventory since approximately `results/100_*`  
**Goal:** Reduce chaos before Profile Harmonization Window B

---

## Executive summary

The workspace has **~6,366 untracked files** and **7 modified tracked files**. The chaos is concentrated in three zones:

| Zone | Files (approx) | Disk | Severity |
|------|----------------|------|----------|
| `Fonts and Glyphs/` duplicate unpacks | 6,142 untracked | **107 MB** | **High** — accidental duplication, not product code |
| `results/` numbered docs (100+) | 156 entries / 386 files | **27 MB** | **Medium** — valuable docs mostly **uncommitted** |
| `validation/` phase artifacts | 1,394 tracked + 5 untracked | **178 MB** | **Medium** — large screenshot/geojson cache |

**Critical governance gap:** Of ~156 numbered `results/` entries at 100+, **~83 top-level entries (218 file paths) are untracked**, including active work (`229_profile_harmonization_audit.md`, `230_information_hierarchy_study_1.md`) and the entire diffs study chain mockups. Only recent closeouts **224–228** are reliably committed.

**Uncommitted implementation work (separate from artifact chaos):**
- `app_shell.html` — PROFILE-HARMONIZATION Window A (PH-1/2/3/11)
- `scripts/smoke_profile_natal_wheel.py` — smoke update for PH-3 wheel-slot path

These are **not** stabilization deletions; they need their own commit window.

---

## 1. Inventory method

Sources:
- `git status --porcelain -uall`
- `git ls-files results/ validation/`
- `du -sh` on major directories
- Filename/type classification for `results/100+`

**Approximate cutoff:** `results/100_comparison_workflow_gap_audit.md` onward (156 numbered entries through `230_information_hierarchy_study_1.md`).

---

## 2. Git workspace snapshot

| State | Count | Notes |
|-------|------:|-------|
| Untracked (`??`) | **6,366** | Dominated by `Fonts and Glyphs/` |
| Modified (` M`) | **7** | Includes PH Window A + regenerated JSON |
| Deleted (` D`) | **4** | Font zip archives removed (good) |

### Modified tracked files

| File | Category | Note |
|------|----------|------|
| `app_shell.html` | **Implementation WIP** | PH Window A — commit separately |
| `scripts/smoke_profile_natal_wheel.py` | **Implementation WIP** | PH-3 assertion update |
| `results/42_read_path_audit.md` | Pre-100 | Out of scope; stray edit |
| `validation/reports/map_current_smoke.json` | Temp regen | Stale validation output |
| `validation/reports/sprint_dc_ic_validation.json` | Temp regen | Stale validation output |
| `relay-sandbox/handoffs/status.json` | Temp | Sandbox handoff state |
| `supabase/.temp/cli-latest` | Temp | CLI cache — should be gitignored |

---

## 3. File counts by category

### A — Keep permanently

| Subcategory | File count (approx) | Disk (approx) | Recommendation |
|-------------|--------------------:|--------------:|----------------|
| `results/` audits | 31 md | — | **Keep + commit** |
| `results/` closeouts | 25 md | — | **Keep + commit** |
| `results/` doctrines | 11 md | — | **Keep + commit** |
| `results/` plans / QA | 21 md | — | **Keep** (archive superseded plans in-place with header note) |
| `results/` design studies | 10 md | — | **Keep** (active research chain) |
| `results/` screenshot dirs | 11 dirs / 138 png | **16.6 MB** | **Keep** representative sets; archive redundant variants |
| `results/` generated JSON | 6 json | <1 MB | **Keep** if tied to closeout; else archive |
| `validation/mockups/beta/` HTML mockups | 35 html + css | **6.9 MB** | **Keep** — includes approved `profile_standard.html`, `relocated_standard.html` |
| Untracked study mockups (diffs + hierarchy) | 5 html | ~200 KB | **Keep + commit** |
| Recent closeouts (tracked) | 224–228 | — | **Keep** — authoritative |

**A subtotal (results 100+ content):** ~156 entries, ~240 `.md`, ~138 `.png`, ~8 `.json` → **~27 MB**

### B — Temporary artifacts

| Subcategory | File count (approx) | Disk (approx) | Recommendation |
|-------------|--------------------:|--------------:|----------------|
| `Fonts and Glyphs/` duplicate unpack folders | **6,142** untracked | **107 MB** | **Archive/delete** — keep `.zip` sources only; production glyphs live in `theme/fonts/` |
| `validation/screenshots/` | 1,044 | **113 MB** | **Archive** — phase2/phase3 brute-force reproduction captures |
| `validation/mockups/screenshots/` | 12 | **21 MB** | **Archive** — mockup capture cache |
| `validation/geojson/` truth-field raw files | 30 | **24 MB** | **Archive** — generated geometry; keep merged/small proofs only |
| `validation/reports/*.json` | 56 | **1.5 MB** | **Regenerable** — keep latest smoke JSON; archive phase2/phase3 iteration board |
| `validation/visual_targets/` | 70 | **9.5 MB** | **Review** — likely keep if referenced by active map work |
| Modified smoke JSON (map_current, sprint_dc_ic) | 2 | <100 KB | **Discard regen** or commit only if CI depends |
| `supabase/.temp/cli-latest` | 1 | tiny | **Gitignore** |

**B subtotal:** ~7,200+ files → **~276 MB** recoverable or relocatable

### C — Unknown / needs decision

| Item | Files | Question |
|------|------:|----------|
| `scripts/motion_visual_qa_genie_v7.py` | 1 untracked | Used by Genie v7 QA (`228` closeout) — **should commit** |
| `Fonts and Glyphs/13093396-zodiac` vs `zodiac 2`…`zodiac 9` | 10 duplicate trees | Which unpack is canonical? **Delete 2–9** after confirming |
| `palette_study.html` … `palette_study5.html` | 5 mockups | Design exploration — **keep all** unless palette locked in doctrine |
| `results/221_focus_reset_status.md` | 1 | Governance freeze doc — **keep** until reset acknowledged |
| `results/223_retro_smoke_classification.md` | 1 | Smoke triage — **keep** short-term |
| `results/214_*` number collision | 2 md + 1 study dir | City-search plan vs diffs study share prefix **214** — rename future docs |
| `results/211_city_search_phase2_plan.md` vs `214_city_search_phase2_plan.md` | 2 | **214 supersedes 211** per its header — archive 211 |

---

## 4. Estimated disk usage (artifact zones)

| Path | Size | Files |
|------|-----:|------:|
| `validation/` (total) | **178 MB** | ~1,399 |
| `results/` (total) | **27 MB** | ~389 |
| `Fonts and Glyphs/` | **107 MB** | ~6,200+ |
| **Combined** | **~312 MB** | **~7,900+** |

Breakdown within `validation/`:
- `validation/screenshots/` — 113 MB (64% of validation)
- `validation/mockups/` — 28 MB (includes 21 MB mockup screenshots subfolder)
- `validation/geojson/` — 24 MB
- `validation/visual_targets/` — 9.5 MB
- `validation/reports/` — 1.6 MB

Breakdown within `results/`:
- Screenshot dirs — 16.6 MB (62% of results)
- Markdown + JSON — ~10 MB

---

## 5. Duplicate studies

### 5.1 Diffs / information hierarchy (active chain)

| # | Report | Mockup | Screenshots | Status |
|---|--------|--------|-------------|--------|
| 119 | doctrine v1 | — | — | **Anchor — keep** |
| 120 | mockup study | — | — | Historical |
| 214 | visual study 1 | `diffs_visual_study.html` ⚠️ untracked | 18 png / 2.6 MB | **Superseded by 220** |
| 219 | revision | `diffs_visual_study_revision.html` ⚠️ | 10 png / 0.7 MB | **Superseded by 220** |
| 220 | visual study 2 | `diffs_visual_study_2.html` ⚠️ | 36 png / 2.3 MB | **Keep** — cell-local baseline |
| 222 | grey study 3 | `diffs_grey_study_3.html` ⚠️ | 19 png / 1.1 MB | **Keep** — channel test; grey not assumed final |
| 230 | hierarchy study 1 | `information_hierarchy_study_1.html` ⚠️ | none yet | **CURRENT research** — first principles |

⚠️ All five diffs/hierarchy mockups are **untracked**.

**Duplicate overlap:** Studies 214 → 219 → 220 iterate the same Boston/NY/Omaha scenarios. Screenshot folders **214 + 219** are largely redundant with **220** for design review purposes.

### 5.2 Palette exploration

Five variants: `palette_study.html` … `palette_study5.html` (all tracked). Not duplicates — sequential exploration. **Keep** unless a single palette is canonized in doctrine.

### 5.3 City search plans (duplicate content)

| File | Relationship |
|------|--------------|
| `211_city_search_phase2_plan.md` | Draft plan |
| `214_city_search_phase2_plan.md` | **Supersedes 211** (references it explicitly) |
| `216_city_search_popular_index_plan.md` | Follow-on |
| `225` / `227` closeouts | **Authoritative shipped state** |

**Number collision:** `214_city_search_phase2_plan.md` and `214_diffs_visual_study_1.md` share prefix 214 — confusing for humans and scripts.

### 5.4 Glyph / font asset duplication

`Fonts and Glyphs/` contains **45 subdirectories**, including:
- `13093396-zodiac` through `13093396-zodiac 9` (10 copies)
- `13206780-astrology` through `13206780-astrology 7` (8 copies)
- Multiple `.zip` sources **plus** unpacked eps/png/psd/svg/font trees

Production wired font: `theme/fonts/AstroDotBasic.ttf` (`226_glyph_wiring_1_closeout`). The Flaticon unpack forest is **not** product code.

### 5.5 Motion QA screenshots

`results/215_motion_visual_qa_screenshots/` — 30 png / **8.2 MB** (largest single screenshot dir). Tied to Genie v7 sandbox QA. **Keep** while map motion work is active; archive when production map motion ships.

---

## 6. Obsolete reports

Reports that remain valuable as history but should **not** drive new implementation:

| Report | Why obsolete for forward work |
|--------|------------------------------|
| `147_export_architecture_v1.md` | Superseded by `148_export_architecture_revision_v2.md` |
| `150_settings_reality_audit_1.md` | Superseded by `158_settings_reality_audit_3_final.md` |
| `211_city_search_phase2_plan.md` | Superseded by `214_city_search_phase2_plan.md` |
| `214_diffs_visual_study_1.md` + screenshots | Superseded by `220` (row-wash era) |
| `219_diffs_visual_study_revision.md` + screenshots | Superseded by `220` |
| `108_port8000_verification_screenshots/` | Early wire verification — historical |
| `170_wheel1_qa_*` | Superseded in practice by `180_wheel_v2_qa_*` |
| `193_diffs_mvp_1_closeout.md` | **Still in production** (opacity rule) but **design-superseded** by 220/230 research — do not treat as UX authority |

Governance docs (not obsolete, but frozen):
- `221_focus_reset_status.md` — explicit stop-list until reviewed

---

## 7. Reports superseded by later reports

### Authoritative “current” pointers by thread

| Thread | Read this | Not this |
|--------|-----------|----------|
| **Profile harmonization** | `229_profile_harmonization_audit.md` | `210_profile_page_reality_audit`, `212_profile_wiring_reality_audit` |
| **Profile natal data** | `224_profile_natal_wheel_1_closeout.md` | pre-224 profile audits |
| **Diffs UX research** | `230_information_hierarchy_study_1.md` | `214`, `219`, `222` as final answers |
| **Diffs production** | `193_diffs_mvp_1_closeout.md` (code) + `230` (design direction) | `193` alone for UX |
| **City search perf** | `227_city_search_2b_2c_closeout.md` | `204`, `211`, `214` plans |
| **Chart truth** | `174_canonical_truth_audit_final.md` + `162_chart_truth_hierarchy_amendment.md` | `151` initial audit |
| **Export** | `148_export_architecture_revision_v2.md` | `147` v1 |
| **Settings** | `158_settings_reality_audit_3_final.md` | `150` audit 1 |
| **Web2 wiring** | `149_web2_closeout_audit_1.md` | `104` priority plan |
| **Wheel** | `198_wheel_orient_1_closeout.md` + `180_wheel_v2_qa_verification.md` | `170` v1 QA |
| **Glyphs (production)** | `226_glyph_wiring_1_closeout.md` | `Fonts and Glyphs/` unpack dirs |

---

## 8. Untracked inventory detail (since ~100)

| Location | Untracked paths | Action |
|----------|----------------:|--------|
| `Fonts and Glyphs/` | 6,142 | **Archive/delete duplicates** |
| `results/` | 218 | **Batch commit** (high value) |
| `validation/mockups/beta/` | 5 html | **Commit with studies** |
| `scripts/motion_visual_qa_genie_v7.py` | 1 | **Commit** (supports 228 QA) |

### Untracked `results/` highlights (must not lose)

- Entire chart-truth tranche: `151`–`174` series (many untracked)
- Diffs chain: `209`, `214`–`222`, `230`
- Profile: `229_profile_harmonization_audit.md`
- City search: `204`, `211`, `214`, `216` (plans/audits)
- Governance: `221`, `223`

### Tracked closeouts (good baseline)

`224_profile_natal_wheel_1_closeout.md` through `228_genie_v7_savedisk_fix_1_closeout.md`

---

## 9. Recommendations — archive vs keep

### Keep in repo (commit if untracked)

1. **All `results/100+` markdown** — primary institutional memory (~218 untracked paths).
2. **Study mockups:** five untracked diffs/hierarchy HTML files + existing `profile_standard.html` / `relocated_standard.html`.
3. **`scripts/motion_visual_qa_genie_v7.py`** — referenced by motion QA closeout path.
4. **Screenshot dirs for active threads:** `220`, `222`, `230` (when captured), `229` (when Window A/B QA runs).
5. **Doctrines** (`119`, `130`, etc.) — permanent reference.

### Archive (move off main tree or external storage)

1. **`validation/screenshots/`** (113 MB) → `validation/archive/screenshots/` or off-repo storage.
2. **`validation/mockups/screenshots/`** (21 MB) → same.
3. **`validation/geojson/*-raw.geojson`** large truth-fields → archive; keep merged proofs.
4. **Diffs screenshot dirs `214` + `219`** (3.3 MB combined) — superseded by `220`/`222`/`230`.
5. **Phase2/phase3 `validation/reports/phase2_*` and `phase3_*` JSON boards** — historical parameter sweeps.

### Delete or gitignore (after confirmation)

1. **`Fonts and Glyphs/` unpacked duplicates** (`zodiac 2`–`9`, etc.) — retain `.zip` sources only → **~90+ MB** recovery.
2. **`supabase/.temp/`** — add to `.gitignore`.
3. **Regenerated smoke JSON** unless CI pins them.

### Do not touch before Window B

- `app_shell.html` / `smoke_profile_natal_wheel.py` — finish PH Window A commit as its own slice.
- `profile_standard.html`, `relocated_standard.html` — approved UX references.
- `229`, `230` — active Profile / diffs research inputs.

---

## 10. Pre–Window B stabilization checklist (recommended order)

| Step | Action | Risk | Recovery |
|------|--------|------|----------|
| 1 | Commit untracked `results/100+` docs (batch) | Low | git revert |
| 2 | Commit 5 untracked study mockups + `motion_visual_qa_genie_v7.py` | Low | git revert |
| 3 | Commit PH Window A (`app_shell.html` + smoke) as separate commit | Low | git revert |
| 4 | Delete/gignore `Fonts and Glyphs/` unpack dupes; keep zips | Medium | re-unzip |
| 5 | Move `validation/screenshots/` to archive | Low | git history / backup |
| 6 | Add header to `211` noting superseded by `214` | None | — |
| 7 | Adopt numbering rule: one primary doc per result ID | None | — |

**Do not implement Window B until steps 1–3 are done** — otherwise Profile harmonization work sits atop an uncommitted documentation and mockup base.

---

## 11. Conclusion

Chaos is **not** in the approved mockups or closeout docs — it is in **(a)** six thousand font duplicate unpacks, **(b)** hundred-megabyte validation screenshot caches, and **(c)** a large untracked `results/` backlog that includes the very documents needed for Window B (`229`, `230`).

Minimum path to stability:
1. Commit the knowledge base (`results/` + study mockups).
2. Excise or archive the font unpack forest and validation screenshot cache.
3. Land PH Window A as a focused commit.
4. Proceed to Window B with `229` as the sole layout authority and `230` as diffs design input (not `193` opacity alone).

**No files were changed by this audit.**
