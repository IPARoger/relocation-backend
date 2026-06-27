# WEB2 Shell Init Smoke Fix

**Date:** 2026-06-27  
**Scope:** Diagnose and fix `window.__rmAppShell.viewModel()` Playwright timeout (`WEB2-SHELL-INIT-SMOKE-FIX`)

---

## Root cause

Two **JavaScript syntax errors** in the `app_shell.html` inline script prevented the entire script from parsing. As a result:

- `window.__rmAppShell` was never assigned
- `bootstrap()` never ran
- `viewModel()` never became available

### Error 1 — orphaned `.forEach` (primary `pageerror`)

**File:** `app_shell.html` — `bindScreenActions()` (~line 10094)

**Introduced:** `32248557` (*city-intelligence: hydrate canonical UI*) — when `ci-back` handler was added, the opening line for the data-nav binder was accidentally deleted:

```javascript
// BROKEN (missing querySelectorAll line)
  });
.forEach((btn) => {

// FIXED
  });
  root.querySelectorAll("[data-nav]").forEach((btn) => {
```

**Browser error:** `pageerror: Unexpected token '.'`

### Error 2 — duplicate `const` declaration

**File:** `app_shell.html` — save-settings handler (~line 10955)

Duplicate block declared `dignityColorModeEl` and `digColors` twice in the same scope:

**Browser error (node --check):** `SyntaxError: Identifier 'dignityColorModeEl' has already been declared`

---

## `family_resemblance.css` 404 — harmless for shell init

| Asset | HTTP on uvicorn | Blocks shell? |
|-------|-----------------|---------------|
| `/theme/family_resemblance.css` | 404 (no route) | **No** — CSS missing does not prevent JS parse or `__rmAppShell` assignment |
| `/validation/mockups/beta/notes_canonical.js` | 404 (no route) | **No** — external script 404 does not abort inline script parse |
| `/validation/mockups/beta/help_canonical.js` | 404 | **No** |

These 404s are pre-existing static route gaps in `main_centerline_FIXER.py`. They may affect styling/notes/help features but were **not** the shell init blocker.

---

## Fix applied

**File:** `app_shell.html` only (no Settings feature changes)

1. Restored `root.querySelectorAll("[data-nav]").forEach(...)` in `bindScreenActions`
2. Removed duplicate `dignityColorModeEl` / `digColors` block in save-settings handler

**Verification:**

```bash
node --check <inline script extracted from app_shell.html>  # OK
```

Authenticated Playwright check after fix:

| Check | Before | After |
|-------|--------|-------|
| `window.__rmAppShell` | false | **true** |
| `viewModel()` | false | **true** |
| `pageerror` | `Unexpected token '.'` | **none** |

---

## Smoke re-run results

All four smokes **pass shell init** (`viewModel()` ready within 60s) but still **FAIL** on a new, isolated assertion:

| Script | Shell init | New failure |
|--------|------------|-------------|
| `smoke_settings_navigation.py` | **PASS** | `#rm-settings-minor-aspects` not **visible** (inside closed `<details>`) |
| `smoke_settings_account.py` | **PASS** | same |
| `smoke_h6_settings_slice1.py` | **PASS** | same |
| `smoke_h6_3_settings_wire.py` | **PASS** | same |

Example Playwright log:

```
waiting for locator("#rm-settings-minor-aspects") to be visible
34 × locator resolved to hidden <input type="checkbox" id="rm-settings-minor-aspects"/>
```

This is **smoke automation drift** (minor aspects moved behind advanced `<details>` gate in S2 settings UI), not a shell initialization defect.

---

## Acceptance

| Criterion | Status |
|-----------|--------|
| Root cause identified with file/line | **Met** |
| `family_resemblance.css` assessed | **Harmless for shell init** |
| Shell init timeout fixed | **Met** |
| Smokes fail only for isolated new reason | **Met** (hidden minor-aspects selector) |
| No Settings feature changes | **Met** |

---

## Commands run

```bash
node --check <extracted inline script>
python3 scripts/smoke_settings_navigation.py
python3 scripts/smoke_settings_account.py
python3 scripts/smoke_h6_settings_slice1.py
python3 scripts/smoke_h6_3_settings_wire.py
```
