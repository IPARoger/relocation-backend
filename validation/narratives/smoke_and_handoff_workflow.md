# Smoke tests and UI handoff workflow

**Purpose:** Catch catastrophic UI regressions before human QA — without building enterprise test architecture or letting tests drive production design.

## Required workflow

```
IMPLEMENT
  → VALIDATE MATH      (scripts/validate_sprint_dc_ic.py)
  → RUN SMOKE          (scripts/smoke_map_current.py)
  → REPORT KNOWN ISSUES
  → HUMAN QA
  → COMMIT
```

Every UI handoff must pass:

1. **Backend validation** — astrology/API parity scripts
2. **Browser smoke** — Playwright catastrophic-regression checks
3. **Console sanity** — no page errors during smoke
4. **Basic interaction sanity** — dropdowns, map, popup, Find Regions

## Smoke scope (automated)

Focus on **“is the app broken?”** not **“is it beautiful?”**

| Covered now | Examples |
|-------------|----------|
| Page load | 200, title, profiles fetched |
| Native controls | All dropdowns focus + change value |
| Find Regions | Clickable; overlay layers appear; re-click works |
| Map interaction | Bounds snapback; double-click zoom |
| Popup | Right-click open; one map click close |
| Console | No JS exceptions |
| Coords sanity | No non-finite lat/lng in rendered layers (basic) |
| Backend | validate_sprint_dc_ic.py bundled in smoke |

## Human QA scope (not automated)

- Astrology correctness
- UX feel and visual coherence
- Overlap semantics and color meaning
- Smoothing aesthetics
- Edge-case interpretation
- “Does this feel trustworthy?”

## Principles

- **Lightweight.** One script, one JSON report, Playwright + existing validators.
- **Pragmatic.** Add checks only when they prevent repeat regressions.
- **Minimal production hooks.** `window.__rmMap` and `window.__rmSmokeState()` only — no test-driven abstractions in app code.
- **Incremental backlog.** Do not implement everything at once.

## Commands

```bash
# Server
./venv/bin/python -m uvicorn main_centerline_FIXER:app --host 127.0.0.1 --port 8000

# Math
./venv/bin/python3 scripts/validate_sprint_dc_ic.py

# Browser smoke (one-time: pip install playwright && playwright install chromium)
./venv/bin/python3 scripts/smoke_map_current.py
```

Report: `validation/reports/map_current_smoke.json`

## Standard handoff format

```
What changed
Root cause (if fix)
Automated validation result
Browser smoke result
Known remaining issues
Exact URL to test (?bust=<new>&skipOnboarding=1)
```

## Smoke backlog (add incrementally)

| Check | Status |
|-------|--------|
| Overlay generation success (layers > 0) | **in smoke** |
| Repeated Find Regions clicks | **in smoke** |
| Non-finite coordinates in rendered layers | **in smoke** |
| Profile switch + re-render | **in smoke** |
| Empty GeoJSON response | backlog |
| Invalid polygon winding | backlog (math validator) |
| Detached overlay fragments near seam/poles | backlog (visual + geo QA) |
| Overlay removal/re-render cycles | backlog |
| Popup open/close cycles (stress) | backlog |
| NaN in API response (pre-render) | backlog |

Add backlog items when a regression slips through or human QA repeats the same failure twice.
