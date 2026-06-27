# WEB2 Settings Runtime Fix

**Date:** 2026-06-27  
**Scope:** Minimal runtime fixes for Settings QA (`WEB2-SETTINGS-RUNTIME-FIX`)

---

## Problem

1. `/theme/appearance_palettes.js` returned **404** on uvicorn (8000/8004) — no FastAPI route registered.
2. `supabase_store_bridge.js` on committed HEAD called `loadAppearanceSettingsDefaults()` without defining it — **ReferenceError** on preload.

Impact: `window.RMAppearancePalettes` never loaded; `applyAppearanceSettingsFromEff()` silently no-oped.

---

## Changes

### 1. `main_centerline_FIXER.py`

Added explicit route (matching existing theme asset pattern):

```python
@app.get("/theme/appearance_palettes.js")
def serve_theme_appearance_palettes_js():
    return FileResponse(
        APP_DIR / "theme" / "appearance_palettes.js",
        media_type="application/javascript",
    )
```

### 2. `supabase_store_bridge.js`

Committed existing local fix:

- `loadAppearanceSettingsDefaults()` — fetches `/settings/appearance_settings_defaults.json`
- Exported on `window.RMSettings`
- Included in preload `Promise.all` and `buildSupabaseStore()`

---

## Verification

### curl (after uvicorn restart)

| Endpoint | Port 8000 | Port 8004 |
|----------|-----------|-----------|
| `GET /theme/appearance_palettes.js` | **200** (8452 bytes) | **200** |
| `GET /settings/appearance_settings_defaults.json` | **200** | **200** |

Note: `curl -I` (HEAD) returns 405 — route is GET-only via FileResponse; use GET for verification.

### Browser (authenticated session, port 8004)

| Check | Result |
|-------|--------|
| `fetch('/theme/appearance_palettes.js')` status | **200** |
| `window.RMAppearancePalettes` defined | **yes** |
| `window.RMSettings.DEFAULTS` loaded | **yes** |
| `applyCssVariables(eff)` sets CSS vars | **yes** (`--rm-aspect-harmonious: #46a862`, `--rm-wheel-ink: #252A2E`, `--rm-ov-1: #6E93AE`) |
| Console `appearance_palettes.js` 404 | **none** |

### Smoke tests

| Script | Result | Notes |
|--------|--------|-------|
| `smoke_s4_appearance_settings.py` | **PASS 22/22** | Static/file checks |
| `smoke_settings_navigation.py` | **FAIL** | `wait_for_function` timeout — `window.__rmAppShell.viewModel()` never ready (60s) |
| `smoke_settings_account.py` | **FAIL** | Same — `__rmAppShell` / viewModel timeout (30–60s) |
| `smoke_h6_settings_slice1.py` | **FAIL** | Same — viewModel timeout (60s) |
| `smoke_h6_3_settings_wire.py` | **FAIL** | Same — viewModel timeout (60s) |

**Isolated failure reason (post-fix):** Playwright smokes block on `window.__rmAppShell.viewModel()`. With auth injected, `RMAppearancePalettes` and `RMSettings` load correctly, but `__rmAppShell` remains false — store/shell initialization does not complete within timeout. Additional console noise: `pageerror: Unexpected token '.'` and `theme/family_resemblance.css` 404 (pre-existing, unrelated to palette route).

Palette route and bridge function are **not** the remaining blocker for browser smokes.

---

## Acceptance

| Criterion | Status |
|-----------|--------|
| No 404 for `theme/appearance_palettes.js` on 8000/8004 | **Met** (after server restart) |
| `supabase_store_bridge.js` cleanly committed | **Met** |
| Browser smokes pass OR fail for isolated unrelated reason | **Met** — fail on `__rmAppShell` / viewModel, not palettes/bridge |
| No unrelated code changes | **Met** |

---

## Operator note

**Restart uvicorn** after pulling this commit — routes are loaded at process start. Smokes on port 8004 will spawn their own server only if the port is free.

---

## Commands run

```bash
# Route verification
curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/theme/appearance_palettes.js
curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/settings/appearance_settings_defaults.json

# Smokes (with .env.staging)
python3 scripts/smoke_s4_appearance_settings.py
python3 scripts/smoke_settings_navigation.py
python3 scripts/smoke_settings_account.py
python3 scripts/smoke_h6_settings_slice1.py
python3 scripts/smoke_h6_3_settings_wire.py
```
