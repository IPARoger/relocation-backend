# SETTINGS-V3 Runtime Reconciliation

**Task:** SETTINGS-V3-RUNTIME-RECONCILIATION  
**Date:** 2026-06-25  
**Scope:** Read-only inspection — no UI behavior changes  
**PR under comparison:** [#23](https://github.com/IPARoger/relocation-backend/pull/23)  
**Branch tip:** `23774db` — `settings-v3: both lunar nodes above fold, Tables/Chart bodies, table orbs grid`

---

## 1. Current branch + HEAD (this workspace / cloud agent)

```text
$ git branch --show-current
cursor/settings-v3-4b-charts-4b87

$ git log -1 --oneline
23774db settings-v3: both lunar nodes above fold, Tables/Chart bodies, table orbs grid
```

| Ref | SHA |
|-----|-----|
| `HEAD` | `23774db649ecb8e5cbb12d2f0a08675190edd907` |
| `origin/cursor/settings-v3-4b-charts-4b87` | `23774db` (matches HEAD) |
| `origin/main` | `fbe486e` (no Settings V3 code) |

**Worktree integrity:** `app_shell.html` MD5 `aa5d2e207aaa0e533c12d86e28c7f38d` — **byte-identical** to `23774db:app_shell.html`.  
No committed or staged diffs on tracked files.

---

## 2. Marker proof — what the served `app_shell.html` contains

Backend serves the repo-root file directly:

```text
GET /app_shell.html  →  FileResponse(APP_DIR / "app_shell.html")
```

Inspection of **this workspace's** `app_shell.html` (what would be served if this checkout is running):

| Marker | Present? | Count / notes |
|--------|----------|---------------|
| `screenSettingsV3` | **YES** | 2 (declaration + `SCREEN_RENDERERS` registration) |
| `My Profiles` | **NO** | 0 — not anywhere in `app_shell.html` |
| `rm-sv3-oa-table` | **YES** | 16 (HTML table orbs grid at `23774db`) |
| `settings_v3/settings_v3.js` | **NO** | Directory does not exist; no `<script src>` reference |

**Related markers (for UI attribution):**

| Marker | Worktree (`23774db`) | `main` |
|--------|----------------------|--------|
| `settings-v3` route in `ALL_ROUTES` | YES | NO |
| `SETTINGS_V3_SECTIONS` (nav) | YES — **only "Charts"** | NO |
| `Advanced Bodies` | YES | NO |
| `Mean Node` | NO | NO |
| `North Node` / `South Node` | YES (above-fold bodies) | North Node only in legacy settings |
| `rm-sv3-oa-grid` / `display: contents` | NO (removed at `23774db`) | NO |
| `planetsBodiesHtml` (legacy `#/settings`) | YES | YES |
| `My Account` | NO | NO |

**Where "My Profiles" *does* exist in this repo:**

- `prototype_settings_v1.html`
- `prototype_settings_v2.html`

Not wired into `app_shell.html` on any remote branch.

---

## 3. Which implementation is the visible UI from?

### What this repo can prove

| Source | Can produce your screenshot UI? | Evidence |
|--------|----------------------------------|----------|
| **`main`** (`fbe486e`) | **NO** | No `settings-v3` route; `#/settings-v3` silently resolves to `dashboard`. Legacy `#/settings` uses single-checkbox `planetsBodiesHtml()`, not Tables/Chart or Advanced Bodies. |
| **`cursor/settings-v3-4b-charts-4b87`** (`23774db`) | **PARTIAL** | Has `#/settings-v3/charts`, Tables/Chart bodies, Advanced Bodies, table orbs — but **no** My Account / My Profiles sidebar, **no** Mean Node label. |
| **Another remote branch** | **NO** | Scanned all `origin/*` branches: only `cursor/settings-v3-4b-charts-4b87` contains `screenSettingsV3`. None contain `My Profiles` in `app_shell.html`. |
| **Uncommitted local files (your Mac)** | **MOST LIKELY** | Your screenshots show UI elements that exist **nowhere** in this repo's `app_shell.html` — closest match is `prototype_settings_v2.html`. |
| **`settings_v3/settings_v3.js`** | **Not in repo** | If your browser loads this path, it is local-only and not tracked here. |

### Route → renderer map (branch `23774db`)

```text
#/settings-v3/charts  →  screenSettingsV3()  →  settingsV3ChartsBodyHtml()
                         Nav: single "Charts" item only
                         Bodies: Sun–Pluto, Chiron, North Node, South Node (above fold)
                         Advanced Bodies: Lilith, True Node, Vertex, Part of Fortune

#/settings/astrology  →  settingsChartsBodyHtml()  →  planetsBodiesHtml() (legacy)
#/settings/charts    →  alias to astrology (same legacy renderer)
```

### Conclusion on visible UI

**Your screenshots are not produced by the committed code on `main` or by the committed code on PR #23 (`23774db`) as it exists in this repository.**

The sidebar (My Account, My Profiles, Charts, My Map, Language & Regional, Data, Technical, Personalization) and Mean Node labels align with **`prototype_settings_v2.html`**, or with **local `app_shell.html` edits that were never pushed** to `origin`.

This cloud workspace **is** running the PR #23 implementation (branch tip, clean worktree).  
Your Mac browser, based on screenshot evidence, is **almost certainly running a different, richer Settings V3** than what is in PR #23.

---

## 4. Uncommitted files

```text
$ git status --short
?? results/settings_v3_4b_charts_preview.html
?? results/settings_v3_4b_charts_screenshot.png
?? scripts/capture_settings_v3_4b_screenshot.py
```

- **No** uncommitted changes to `app_shell.html` or any tracked source.
- Untracked files are agent-generated preview/screenshot artifacts only; they do not affect runtime.

**On your Mac, also run:**

```bash
git status --short
git diff --stat app_shell.html
md5sum app_shell.html   # compare to aa5d2e207aaa0e533c12d86e28c7f38d if on 23774db
```

---

## 5. Comparison: what you are running vs PR #23 / `23774db`

### Commits on branch, not on `main`

```text
23774db  settings-v3: both lunar nodes above fold, Tables/Chart bodies, table orbs grid
06d083e  settings-v3: fix Orbs & Aspects grid alignment (4C)
```

`app_shell.html` delta vs `main`: **+548 lines** (entire Settings V3 subsystem).

### Exists only on branch (`23774db`) — not on `main`

| Item | Description |
|------|-------------|
| Route `#/settings-v3` | Registered in `ALL_ROUTES`, `parseLocation`, `SCREEN_RENDERERS` |
| `screenSettingsV3()` + helpers | `settingsV3BodiesHtml`, `settingsV3OrbsAspectsHtml`, `settingsV3ZodiacHouseHtml`, `settingsV3AdvancedCalcHtml` |
| Bodies Tables/Chart columns | `sv3BodyRow`, `rm-sv3-bodies-tbl`, `rm-sv3-bodies-cht` |
| Above-fold bodies | Chiron, North Node, South Node in main table |
| `Advanced Bodies` | Lilith, True Node, Vertex, Part of Fortune |
| Orbs table grid | `rm-sv3-oa-table`, `sv3OaHeadHtml` — Name \| Tables \| Chart \| Orb |
| Advanced unlock | `applySettingsV3AdvancedState` — any Advanced section unlocks body locks; orbs Advanced unlocks major aspects |
| Save path | `collectSettingsV3Patch`, `save-settings-v3` handler |
| Smokes | `scripts/smoke_settings_v3_4b_charts.py`, `scripts/smoke_settings_v3_4c_orbs_grid.py` |

### Exists only locally (your screenshots / inferred Mac state) — not in PR #23

| Item | Description |
|------|-------------|
| Full settings sidebar | My Account, My Profiles, Charts, My Map, Language & Regional, Data, Technical, Personalization |
| Mean Node label | Screenshot uses Mean/True Node; branch uses North/South Node |
| Chiron inside Advanced (old state) | Your earlier screenshots; branch now has Chiron above fold |
| `settings_v3/settings_v3.js` | Not in any branch of this repo |
| Prototype styling | Card layout, theme tokens from `prototype_settings_v2.html` |

### Exists on both `main` and branch (unchanged legacy)

| Item | Route |
|------|-------|
| `planetsBodiesHtml()` | `#/settings` → Astrology |
| `SETTINGS_SECTIONS` nav | Account, My Data, Astrology, Appearance, … |
| `settingsChartsBodyHtml()` | Legacy astrology subpage |

### Regression note: `06d083e` vs `23774db` (orbs only)

| Commit | Orbs layout | Known issue |
|--------|-------------|-------------|
| `06d083e` | CSS grid + `display: contents` | Column headers misalign in Chrome (ORB over wrong column) |
| `23774db` | HTML `<table class="rm-sv3-oa-table">` | Intended fix — only if this commit is actually served |

### What must be ported (if reconciling)

**From branch → your richer local UI:**

1. `rm-sv3-oa-table` orbs layout (replace any `display: contents` grid)
2. `applySettingsV3AdvancedState` — any-Advanced unlock for bodies; orbs-Advanced unlock for major aspects
3. Above-fold body placement (Chiron + North + South Node)
4. `collectSettingsV3Patch` — Tables/Chart columns, `helper_layers.chart_planets` / `chart_bodies`
5. Bodies Tables/Chart column structure (`sv3BodyRow` pattern)

**From your local UI → branch (if replacing branch scaffold):**

1. Full `SETTINGS_V3_SECTIONS` nav (account, profiles, charts, map, …)
2. Prototype card/chrome styling
3. Mean Node / True Node naming (if preferred over North/South)
4. Any logic in `settings_v3/settings_v3.js` (if that file exists locally)

---

## 6. One recommendation

### **Port branch fixes into your current richer Settings V3 — do not replace your UI with the branch scaffold.**

**Reasoning:**

1. **Your visible UI is richer than PR #23.** PR #23 is a minimal Charts-only scaffold (~546 lines) added alongside legacy settings. Your screenshots match the prototype/full-settings direction, not the branch renderer.

2. **PR #23 fixes are behavioral and structural, not cosmetic.** The valuable work is: table-based orbs alignment, Advanced unlock rules, above-fold node placement, and save wiring. These can be transplanted without discarding your sidebar and layout.

3. **Replacing with the branch implementation would be a downgrade** — you would lose My Account, My Profiles, and the full nav, and gain only a single "Charts" nav item.

4. **`settings_v3/settings_v3.js` does not exist in this repo.** If your Mac loads it, that is additional local surface area the branch does not cover; replacing with the branch would not automatically reconcile that file.

### Immediate verification on your Mac (before any port)

```bash
git branch --show-current && git log -1 --oneline
rg -n "screenSettingsV3|My Profiles|rm-sv3-oa-table|settings_v3" app_shell.html
test -f settings_v3/settings_v3.js && echo "local js module exists" || echo "no js module"
md5sum app_shell.html
# If on 23774db, md5 should be: aa5d2e207aaa0e533c12d86e28c7f38d
```

If `My Profiles` appears in your `app_shell.html` but `md5` differs from above, you have **local-only Settings V3** — port branch fixes into that file.

If `My Profiles` is absent and `md5` matches `23774db`, you **are** on PR #23 code; the UI you expected (prototype sidebar) was never in this branch — only the minimal Charts page exists at `#/settings-v3/charts`.

---

## Appendix: PR #23 status

| Field | Value |
|-------|-------|
| URL | https://github.com/IPARoger/relocation-backend/pull/23 |
| State | OPEN (draft) |
| Base | `main` |
| Head | `cursor/settings-v3-4b-charts-4b87` @ `23774db` |
| Merged to `main` | **No** |

**VERIFIED** (read-only reconciliation complete; no product code changed)
