# RESULT: 80_c5_6_back_compat_state_removal

**Roadmap ID:** C5-6  
**Checkpoint:** `75a3443`  
**Date:** 2026-06-18

---

## Files Changed

| File | Change |
|------|--------|
| `app_shell.html` | Removed back-compat `const state = { … }` proxy and `state,` from `window.__rmAppShell` export |
| `scripts/smoke_app_shell_context_transport.py` | Supabase session injection + dynamic viewModel fixtures + in-shell `navigate()` for hash transport tests |
| `scripts/smoke_app_shell_map_handoff.py` | Same auth/fixture repair + handoff URL build via in-shell map context |

---

## Provenance Evidence

| Commit | Role |
|--------|------|
| `eedce8b` | Introduced back-compat `state` proxy; `navContext` became canonical |
| `96a4a7a` | Removed last `__rmAppShell.state.activeChartRecordId` smoke assertion |
| Product evolution | `open-map-*` actions now call `openMap()` → `map_CURRENT.html`; hash-route transport tests use `navigate()` |

---

## Caller Grep

**Pre-flight:** 0 matches for `__rmAppShell.state`, `rmAppShell.state`, `.state.activeChartRecordId`.

**Post-change:** 0 matches repo-wide.

**app_shell.html:**
- No back-compat `const state = {` block
- No `state,` in `window.__rmAppShell` export
- `get navContext()` / `get uiState()` retained (lines ~3324–3325)

---

## Change Made

Removed transitional getter/setter proxy (`activeChartRecordId` → `chartRecordId`, etc.) and export key. Canonical surfaces unchanged.

---

## Validation

```bash
set -a && source .env.staging && set +a
venv/bin/python scripts/smoke_app_shell_context_transport.py
venv/bin/python scripts/smoke_app_shell_map_handoff.py
```

**Exit code:** 0 / 0

### smoke_app_shell_context_transport.py

```
PASS: dashboard_chart_record_map
PASS: favorite_to_map — skipped (no favorites in account)
PASS: exploration_to_map
PASS: compare_to_map_return
PASS: contract_surface
PASS: smoke_app_shell_context_transport
```

### smoke_app_shell_map_handoff.py

```
PASS: shell_builds_url_chart_record
PASS: stub_link_matches_build
PASS: map_handoff_contract_surface
PASS: map_receives_chart_record
PASS: no_renderer_mutations_chart_record
PASS: shell_builds_url_favorite — skipped (no favorites)
PASS: map_receives_favorite — skipped
PASS: shell_builds_url_exploration
PASS: map_receives_exploration
PASS: shell_builds_url_comparison
PASS: map_without_handoff
PASS: no_renderer_mutations_without_handoff
PASS: rm_app_shell_zero_map
PASS: smoke_app_shell_map_handoff
```

### Smoke repair notes (validation-only)

- **Auth:** magic-link OTP + `localStorage` session injection (pattern from `smoke_map_current.py`)
- **Onboarding:** `rm_guided_onboarding_dismissed` localStorage preset (modal blocked clicks)
- **Fixtures:** dynamic IDs from authenticated `viewModel()` (replaces mock `cr-anna-rivera` IDs)
- **Transport vs handoff:** context transport uses `navigate()` for in-shell hash routes; handoff smoke builds URLs on in-shell map context

---

## Remaining App Shell Test Surfaces

| Export | Status |
|--------|--------|
| `window.__rmAppShell.navContext` | **live** — primary smoke surface |
| `window.__rmAppShell.uiState` | **live** — exported |
| `window.__rmAppShell.state` | **removed** |
| `buildMapHandoffUrl()`, transport contracts | **unchanged** |

---

## C5-6 Verdict

**VERIFIED**
