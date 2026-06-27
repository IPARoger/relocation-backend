# 272 — BI-0C First Experience Implementation

**Date:** 2026-06-27  
**Scope:** Auth reskin + birth intake instrument family (presentation only)  
**Authority:** [271 mockups](271_first_experience_mockups.md) · [270 archaeology §14](270_first_experience_archaeology_audit.md) · [Beta Master Checklist](../docs/BETA_MASTER_CHECKLIST.md)

---

## Summary

BI-0C reskins `auth.html` and `first_profile_intake.js` into the established stone/paper instrument family (`family_resemblance.css`, `rm-instrument-surface`, sage CTAs). Beta birth intake collects **Birth date**, **Birth time** (required), and **Birth location** only; display name is resolved silently; Unknown time UI is removed. Intake success still redirects directly to the map (no transition screen).

---

## Before / after

| Surface | Before | After |
|---------|--------|-------|
| Auth signup | Gray SaaS card, blue CTA | Instrument surface, serif wordmark, sage CTA |
| Auth login | Same outlier family | Matched to signup |
| Birth intake | Purple developer overlay, Unknown toggle | Stone/paper card, rm-sls-* search, exact time only |

**Screenshots:** `validation/mockups/beta/screenshots/bi0c_implementation/before/` (pre-implementation) · `.../after/` (post-implementation)

---

## Primitive mapping

| Mockup / target | Production |
|-----------------|------------|
| `body.rm-instrument-surface` | `auth.html` body; intake overlay class |
| `family_resemblance.css` | Linked on auth; injected on intake show |
| `fe-wordmark` / serif title | `.wordmark` (auth), `.rm-intake-wordmark` (intake) |
| `fe-card` | `.card` on both surfaces |
| `fe-btn-primary` / sage CTA | `.btn-primary` / `.submit-btn` using `--rm-accent` |
| `fe-sls-*` | `.rm-sls-wrap`, `.rm-sls-input`, `.rm-sls-panel`, `.rm-sls-item` |
| Hidden display name | `#rm-intake-name` hidden input + `resolveDisplayName()` |

---

## Smoke results

| Script | Result |
|--------|--------|
| `smoke_bi0c_first_experience.py` | **PASS 20/20** |
| `smoke_bi0_archaeology.py` | **PASS 30/30** (HTTP skipped if server down) |
| `smoke_google_oauth.py` | **PASS 16/16** |
| `smoke_intake_google_name_prefill.py` | **PASS 10/10** |

Checks: family_resemblance on auth, rm-instrument-surface, no blue SaaS tokens, no Unknown time in intake, hidden display name on first-run, rm-sls-* place search, create-with-birth + map redirect preserved.

---

## Files changed

- `auth.html` — instrument token reskin (presentation only)
- `first_profile_intake.js` — instrument overlay, Beta field doctrine, silent display name
- `scripts/smoke_bi0c_first_experience.py` — static QA gate
- `scripts/capture_bi0c_impl.py` — Playwright before/after capture
- `validation/mockups/beta/screenshots/bi0c_implementation/` — screenshots + capture harness
- `docs/BETA_MASTER_CHECKLIST.md` — BI-0C complete

---

## Not changed (per scope)

OAuth logic, backend routes, chart calculation, transition screen (none added), add-profile shell path (display name still visible in `mode: "add"`).

## Commits

- `c216047` — implementation
- `fbdae94` — smoke gate, screenshots, report
