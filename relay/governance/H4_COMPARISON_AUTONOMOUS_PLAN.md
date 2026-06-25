# H4 Autonomous Comparison Harmonization — Executor Contract

**Roadmap ID:** H4 (Comparison visual harmonization)  
**Generated:** 2026-06-25  
**Mode:** Autonomous overnight execution (human asleep)  
**Planner:** GPT + user approved contract  
**Executor:** Cursor agent / relay

---

## Safety checkpoint (CLEAN — use this only)

| Item | Value |
|------|-------|
| **Rollback commit** | `e37bf9d6d572973e9b4f834ed084cd2f39878fff` |
| **Tag** | `checkpoint/h4b_start_clean` |
| **Message** | `comparison: harmonize authority system with beta shell` |
| **Includes** | H4B Slice 1 complete (authority shell only) |

### ⚠️ Do NOT use `5f76990` or old `checkpoint/h4b_start`

Commit `5f76990` was an accidental `git add -A` checkpoint that bundled ~6,429 files (Fonts/Glyphs duplicates, archaeology clutter). It was **removed from branch history** on 2026-06-25. Rollback to it would restore repo pollution.

### On ANY smoke failure in ANY slice

```bash
git reset --hard checkpoint/h4b_start_clean_clean
# or: git reset --hard e37bf9d
```

**Then STOP.** Do not attempt fixes. Write `results/H4_SLICE<N>_FAILURE_AUDIT.md` and exit.

---

## Autonomy contract (binding)

- **Maximum 6 implementation slices** (Slices 2–7 below; Slice 1 already done).
- Each slice: **implement → smoke → commit → STOP** (no chaining slices in one turn without human).
- **Never modify more than one surface** (Comparison only).
- **Never continue after smoke failure.**
- **Never skip a smoke.**
- **Never refactor unrelated code.**
- **Never "clean up while you're there."**
- **Never create doctrine.**
- **Never invent UX.**

### Discovery kill switch

> If a slice discovers unexpected architecture, hidden renderer paths, conflicting doctrine, missing ownership, smoke failures, or ambiguity — **STOP immediately**. Do not solve it. Produce an audit document (`results/H4_SLICE<N>_DISCOVERY_STOP.md`) and wait for human review.

---

## Frozen surfaces (DO NOT TOUCH)

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

Also forbidden: performance optimization, renaming functions, removing dead code, visual redesign beyond approved mockup shell.

---

## Authority sources (read-only doctrine)

| Doc | Use |
|-----|-----|
| `validation/mockups/beta/comparison_v5_beta.html` | **Canonical layout winner** |
| `COMPARISON_VISUAL_ARCHAEOLOGY.md` | Philosophy, column/table doctrine |
| `COMPARISON_RENDERER_OWNERSHIP_AUDIT.md` | Renderer paths — do not fork data layer |
| `COMPARISON_IMPLEMENTATION_READINESS.md` | Slice order, do-not-touch list |
| `docs/product/PROFILE_VISUAL_CANON.md` | Profile-bound comparison rules |
| `docs/product/UI_STANDARDIZATION_CANON_v1_2026-06-12.md` | Bottle layout lock |
| `TBAND_COLLAPSE_DOCTRINE_AUDIT.md` | Do NOT import Profile t-band collapse |
| `NOTES_SYSTEM_CANON_AUDIT.md` | Entity-owned comparison notes |

---

## Completed before checkpoint

| Slice | Commit | Deliverable |
|-------|--------|-------------|
| **H4B Slice 1 — Authority** | `e37bf9d` | Beta header, `cmp-zone-b`, sticky city bar shell, `rm-beta-compare` |

Rollback anchor `e37bf9d` is H4B Slice 1 + all prior H3E work.

---

## Slice queue (execute in order)

### Slice 2 — Comparison AIS bottled shell

**Goal:** Port mockup `#ais` collapsible block chrome around **existing** AIS comparison output. Shell/CSS/DOM only.

**May use:** `renderAisComparisonHtml`, `renderComparisonAngleRowsHtml`, `refreshAisWorkbookSection` — wrap, do not rewrite data logic.

**May NOT:** Change PIH, A2A, Notes, CI, city bar behavior, hydration.

**Read budget:** ≤5 files.

**Commit message:**
```
comparison: add AIS bottled block shell (H4 slice 2)
```

**Smokes (all must pass before commit):**
```bash
python3 scripts/smoke_h4b_comparison_authority.py
python3 scripts/smoke_comparison_a2a_matrix.py
python3 scripts/smoke_h2_profile_transplant.py
python3 scripts/smoke_h3e_relocated_shell_completion.py
```
Add/update `scripts/smoke_h4_slice2_ais_shell.py` if needed (static DOM/CSS assertions only).

**Stop after commit.**

---

### Slice 3 — Comparison PIH bottled shell

**Goal:** Port mockup `#pih` block chrome around **existing** `renderPihComparisonHtml` output.

**May NOT:** Touch AIS shell from Slice 2 except shared block CSS if already extracted.

**Commit message:**
```
comparison: add PIH bottled block shell (H4 slice 3)
```

**Smokes:** Slice 2 smokes + `smoke_comparison_sets.py` static sections if present (do not require live server unless already standard).

**Stop after commit.**

---

### Slice 4 — Comparison A2A bottled shell

**Goal:** Port mockup `#ata` block chrome + angle pill strip UI around **existing** `renderA2aComparisonHtml` matrix.

**Critical:** Preserve `data-a2a-shape="matrix"` and `smoke_comparison_a2a_matrix.py` guards.

**May NOT:** Change matrix data logic or Profile carousel renderer.

**Commit message:**
```
comparison: add A2A bottled block shell (H4 slice 4)
```

**Smokes:** All prior + `smoke_comparison_a2a_matrix.py` **required**.

**Stop after commit.**

---

### Slice 5 — Comparison Notes rail

**Goal:** Port mockup `comparison-notes-rail` (268px sticky aside). Move **existing** `comparison-notepad` + `saveComparisonSetNote` into rail layout.

**Doctrine:** Entity-owned notes (`comparison_set`) — no per-block notes resurrection.

**May NOT:** Change notes API or storage.

**Commit message:**
```
comparison: add notes rail shell (H4 slice 5)
```

**Smokes:** All prior + notes save handler symbols preserved (static).

**Stop after commit.**

---

### Slice 6 — Comparison CI shell

**Goal:** Port mockup collapsible `ci-section` **shell only** — placeholder content acceptable (`wired: false`).

**May NOT:** Wire City Intelligence content engine or backend.

**Commit message:**
```
comparison: add location intelligence shell (H4 slice 6)
```

**Smokes:** All prior.

**Stop after commit.**

---

### Slice 7 — Freeze audit (read-only)

**Goal:** Produce `COMPARISON_FREEZE_AUDIT.md` — same format as `H3E_RELOCATED_FREEZE_AUDIT.md`.

**Mode:** READ ONLY. No code changes. No commit unless audit file alone:

**Optional commit message:**
```
docs: comparison freeze audit (H4 slice 7)
```

**Stop. Done.**

---

## Regression smokes (run every implementation slice)

| Script | Purpose |
|--------|---------|
| `smoke_h4b_comparison_authority.py` | H4B authority shell |
| `smoke_h2_profile_transplant.py` | Profile frozen |
| `smoke_h3e_relocated_shell_completion.py` | Relocated frozen |
| `smoke_comparison_a2a_matrix.py` | A2A matrix shape |
| `smoke_h3c_tband_foundation.py` | T-band unchanged |

---

## Renderer ownership reminder

**Live data path (do not replace):**
```
hydrateComparisonColumns → _comparisonColsCache → render*ComparisonHtml
```

**Do not route compare through Profile t-band renderers** (`renderProfileAisCardBodyHtml`, etc.).

**No hidden AIS shortcut** — use explicit `renderAisComparisonHtml` family.

---

## Morning review checklist (human)

1. `git log checkpoint/h4b_start_clean..HEAD --oneline` — expect ≤6 commits
2. Each commit message matches slice table above
3. `git diff checkpoint/h4b_start_clean..HEAD --stat` — only `app_shell.html`, `theme/*`, `scripts/smoke_h4*`, audit docs
4. Run full smoke battery once
5. If anything feels wrong: `git reset --hard checkpoint/h4b_start_clean`

---

## Executor prompt (paste to start next session)

```
Execute H4 Comparison harmonization relay plan:
relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md

Start at Slice 2 only.
Checkpoint: checkpoint/h4b_start_clean (e37bf9d).
On smoke failure: git reset --hard checkpoint/h4b_start_clean and STOP.
One slice per session turn: implement, smoke, commit, stop.
Discovery kill switch applies.
```

