# SETTINGS V3 Port Guide — PR #23 fixes into your richer local UI

**For:** Dave Goodman local `main` @ `3b82b573`  
**Your `app_shell.html` MD5:** `543021be2d111aebf4ac6bd942a1fd46`  
**PR #23 reference:** `23774db` on `cursor/settings-v3-4b-charts-4b87`  
**Rule:** Port fixes only. **Do not replace** your richer Settings V3 sidebar/layout.

---

## Confirmed: your Mac ≠ PR #23

| Fingerprint | MD5 | Has My Profiles | Has `rm-sv3-oa-table` |
|-------------|-----|-----------------|------------------------|
| `origin/main` (remote) | `7501c898…` | No | No |
| PR #23 / `23774db` | `aa5d2e20…` | No | Yes |
| **Your Mac** | **`543021be…`** | **(run verify)** | **(run verify)** |

Your local `main` (`3b82b573`) is **not pushed** to `origin`. The cloud agent cannot read your `app_shell.html` until you push.

---

## Step 0 — Verify on your Mac (grep, no rg)

```bash
cd relocation-backend
bash scripts/verify_settings_v3_local.sh app_shell.html
```

Or manually:

```bash
grep -nE "screenSettingsV3|My Profiles|rm-sv3-oa-table|rm-sv3-oa-grid|display: contents" app_shell.html
md5sum app_shell.html
```

**Expected on your Mac today:**

- `My Profiles` → **YES** (richer UI)
- `screenSettingsV3` → **YES** (you use `#/settings-v3`)
- `rm-sv3-oa-table` → likely **NO** (orbs still broken)
- `rm-sv3-oa-grid` or `display: contents` → likely **YES** (misaligned orbs)

---

## Step 1 — Push your local main (required for agent merge)

```bash
git push origin main
```

After push, the cloud agent can open a proper merge PR against your real file. Until then, use the manual port below.

---

## What to port (5 surgical changes)

Reference files in this branch (`cursor/settings-v3-port-rich-ui-4b87`):

| File | Purpose |
|------|---------|
| `settings_v3/pr23_charts_fixes.fragment.js` | Bodies/orbs builders + `applySettingsV3AdvancedState` |
| `settings_v3/pr23_collect_patch.fragment.js` | `collectSettingsV3Patch` save wiring |
| `settings_v3/pr23_charts_fixes.fragment.css` | Table orbs + bodies column CSS |
| `patches/settings-v3-pr23-app_shell.patch` | Full diff vs `origin/main` (reference only — will **not** apply cleanly to your richer file) |

### 1. CSS — add table orbs, remove broken grid

**Find** (grep):

```bash
grep -n "rm-sv3-oa-grid\|display: contents" app_shell.html
```

**Action:**

- **Delete** `.rm-sv3-oa-grid`, `.rm-sv3-oa-head { display: contents }`, and related grid rules.
- **Add** contents of `settings_v3/pr23_charts_fixes.fragment.css` inside your `<style>` block (merge with existing `.rm-sv3-*` rules).

### 2. Bodies — Chiron + North + South Node above Advanced Bodies

**Find:**

```bash
grep -n "SV3_ABOVE_FOLD\|SV3_SPECIAL_BODIES\|Advanced Bodies\|foldRows" app_shell.html
```

**Action:**

- Ensure constants match `settings_v3/pr23_charts_fixes.fragment.js`:
  - Above fold: `chiron`, `north_node`, `south_node`
  - Advanced only: `lilith`, `true_node`, `vertex`, `part_of_fortune`
- In your **bodies HTML builder** (keep your card/chrome wrapper):
  - Main `<tbody>`: planets, then fold rows, **before** `<details id="rm-sv3-advanced-bodies">`
  - Use `sv3BodyRow` with **Tables | Chart** columns (`rm-sv3-bodies-tbl`, `rm-sv3-bodies-cht`)
  - All body rows: `data-sv3-advanced-lock="1"` + `class="is-locked"` by default

**Do not move** your My Account / My Profiles sidebar — only fix the Charts section body list.

### 3. Orbs — HTML table, column order Name | Tables | Chart | Orb

**Find:**

```bash
grep -n "settingsV3OrbsAspectsHtml\|rm-sv3-oa-grid\|rm-sv3-oa-table" app_shell.html
```

**Action:**

- Replace `<div class="rm-sv3-oa-grid">` structure with:

```html
<table class="rm-sv3-oa-table simple">
  ${sv3OaHeadHtml()}
  <tbody>${majorRows}</tbody>
</table>
```

- `sv3AspectRow` must emit `<tr>` cells in order: label, tbl, cht, orb.
- Major aspects: `lockMajor: true` — checked + disabled until Advanced Orbs opens.
- Advanced toggle label: **Advanced Orbs & Aspects**.

### 4. Advanced unlock — any Advanced → all body checkboxes editable

**Find:**

```bash
grep -n "applySettingsV3AdvancedState" app_shell.html
```

**Action:** Replace function body with `settings_v3/pr23_charts_fixes.fragment.js` version:

- `anyOpen = bodiesOpen || orbsOpen || calcOpen`
- `[data-sv3-advanced-lock]` unlocks when **`anyOpen`** (not only bodies panel)
- `[data-sv3-major-lock]` unlocks when **`orbsOpen`** only

### 5. Save — `collectSettingsV3Patch`

**Find:**

```bash
grep -n "collectSettingsV3Patch\|collectChk\|rm-sv3-planet-" app_shell.html
```

**Action:** Replace with `settings_v3/pr23_collect_patch.fragment.js` if your checkbox IDs use `rm-sv3-{kind}tbl-{id}` / `rm-sv3-{kind}cht-{id}` pattern.

If your richer UI uses **different IDs**, keep your IDs but port the **logic**:

- `anyAdvOpen` gate for planets/bodies/chart_planets/chart_bodies
- `orbsAdvOpen` gate for major/minor aspects and orbs
- Save all three above-fold bodies: `chiron`, `north_node`, `south_node`

---

## Step 2 — Verify after port

```bash
bash scripts/verify_settings_v3_local.sh app_shell.html
```

**Pass criteria:**

| Check | Expected |
|-------|----------|
| `My Profiles` | YES (unchanged) |
| `rm-sv3-oa-table` | YES |
| `rm-sv3-oa-grid` | NO |
| `display: contents` in sv3 orbs | NO |
| MD5 | **New** (not `543021be…`) |

Hard-refresh browser: `Cmd+Shift+R` on `app_shell.html#/settings-v3/charts`.

---

## What NOT to change

- My Account / My Profiles / full settings sidebar
- Legacy `#/settings` route
- Your card styling / theme tokens
- `settings_v3/settings_v3.js` if you have one locally — wire it to call the ported `applySettingsV3AdvancedState` + `collectSettingsV3Patch`

---

## After you push main

Tell the agent: *"main pushed, port PR23 fixes into app_shell.html"*

The agent will:

1. `git fetch origin main`
2. Diff your `app_shell.html` against `23774db` fix hunks
3. Open a merge PR that preserves your richer UI + applies the 5 surgical fixes

---

## Reference MD5 map

```text
7501c898…  origin/main        — no settings-v3
aa5d2e20…  PR #23 (23774db)   — minimal settings-v3 + fixes
543021be…  your Mac           — richer settings-v3, fixes not yet ported
```
