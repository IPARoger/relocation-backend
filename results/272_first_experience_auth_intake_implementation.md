# BI-0C — First Experience Auth + Birth Intake Implementation

**Date:** 2026-06-27  
**Slice:** BI-0C (auth reskin + birth intake instrument family)  
**Reference:** [271 mockups](271_first_experience_mockups.md) · [270 archaeology §14](270_first_experience_archaeology_audit.md)

## Summary

Production auth (`auth.html`) and birth intake (`first_profile_intake.js`) now use the instrument surface family (warm paper, serif titles, `--rm-*` tokens, card layout) aligned with Profile, Comparison, Notes, Settings, and M2-X map. Presentation-only — no auth logic, OAuth, routing, or profile API flow changes.

## Changes

### auth.html
- Linked `/theme/family_resemblance.css`; `body.rm-instrument-surface`
- Replaced cool gray / blue SaaS inline tokens with `--rm-*` instrument palette
- Journey layout: wordmark + purpose line + card (matches BI-0B mockups)
- Typography: Iowan serif titles, Avenir body; warm error/ok alerts
- OAuth + form logic untouched

### first_profile_intake.js
- Replaced purple developer modal with full-page instrument surface + centered card
- Beta fields: Birth date, Birth time (required), Birth location
- Removed Unknown time toggle; always `birth_time_mode: "exact"`
- Display name hidden on first-run (hidden input); auto-filled from Google metadata or `"My chart"` fallback
- Add-profile mode retains visible display name field
- Place search uses `rm-sls-*` classes (map family)
- Button copy: **Continue**; title: **Birth information**
- Redirect to map unchanged (no transition screen)

### Smoke updates
- `scripts/smoke_bi0_archaeology.py`: checks instrument CSS on auth, exact-time-only intake

## Screenshots

| | Path |
|---|------|
| Before | `validation/mockups/beta/screenshots/bi0c_impl/before/` (from bi_archaeology) |
| After | `validation/mockups/beta/screenshots/bi0c_impl/after/` |

Capture script: `scripts/capture_bi0c_impl.py`

## Smoke results

| Script | Result |
|--------|--------|
| `smoke_bi0_archaeology.py` | PASS 30/30 (HTTP skipped — server down) |
| `smoke_google_oauth.py` | PASS 16/16 |
| `smoke_intake_google_name_prefill.py` | PASS 10/10 |

## Preserved (unchanged)

- Supabase auth / OAuth flows
- `MAP_URL` redirect targets
- `POST /profiles/create-with-birth` contract
- Chart calculation, engine, map overlays
- Add-profile mode handoff to app shell

## Blockers / follow-ups

- PO visual QA on live auth + authenticated intake path
- `smoke_bi0_archaeology.py` HTTP checks need running server for full pass
- Next slice: first map session harmonization (popup/save per mockups 06–08)

## Status

**BI-0C complete.**
