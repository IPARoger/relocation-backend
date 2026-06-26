# 271 — First Experience Mockups (BI-0B)

**Date:** 2026-06-26  
**Mode:** Mockups only — no implementation, backend, routing, or animation design.  
**Authority:** [270 First Experience Archaeology](270_first_experience_archaeology_audit.md) · [270 §14 calibration](270_first_experience_archaeology_audit.md#14-bi-0b-calibration-read-before-mockups) · [Beta Master Checklist](../docs/BETA_MASTER_CHECKLIST.md) · [264 Family Resemblance](264_family_resemblance_final_audit.md) · [Material System Canon](../docs/canon/MATERIAL_SYSTEM_CANON.md) · [Interface & Design Canon](../docs/canon/INTERFACE_AND_DESIGN_CANON.md)

---

## Executive summary

Eight static mockups plus three validation states document the **first five minutes** of Beta as one continuous instrument journey:

**Auth → Birth Information → Preparing Your Personal Map → Personalized Map (explore + popup + save)**

All surfaces use the established `--rm-*` stone/paper token stack (`rm-instrument-surface`), serif wordmark, G3-adjacent cards, sage accent CTAs, and production-mapped controls. Auth and intake are **re-skinned**, not re-architected. Unknown birth time is **absent** (doctrine correction per 270 §14.1). Animation is **layout-reserved only**.

**Artifacts:**

| Artifact | Path |
|----------|------|
| Mockup index | `validation/mockups/beta/first_experience/index.html` |
| Shared mockup CSS | `validation/mockups/beta/first_experience/fe-mockup-shared.css` |
| Screenshots | `validation/mockups/beta/first_experience/screenshots/` |
| Family resemblance panel | `validation/mockups/beta/first_experience/screenshots/family_resemblance/family_resemblance_panel.html` |
| This audit | `results/271_first_experience_mockups.md` |

**Gate:** No production implementation until PO approves these mockups.

---

## Journey map

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────────┐    ┌────────────────────┐
│ 1–2 Auth    │ →  │ 3–4 Birth info   │ →  │ 5 Transition        │ →  │ 6–8 Map instrument │
│ Sign in /   │    │ exact time only  │    │ layout reserve only │    │ map · popup · save │
│ Create acct │    │ RMPlaceSearch    │    │ no animation design │    │ no walkthrough yet │
└─────────────┘    └──────────────────┘    └─────────────────────┘    └────────────────────┘
```

Progress dots (mockups 2–5) signal **one journey**, not separate apps.

---

## Mockup 1 — Welcome / Sign In

### Purpose

Entry into the same product family as Profile, Comparison, and Settings — calm, premium, instrument-grade. Not generic gray/blue SaaS.

### Existing production screen

`auth.html` — login view (`data-view="login"`). See archaeology screenshots `validation/mockups/beta/screenshots/bi_archaeology/02_auth_login.png`.

### Problems

| Issue | Detail |
|-------|--------|
| Visual outlier | System-ui stack, `#f0f4f8` gray ground, `#1d4ed8` blue primary — documented outlier in [264](264_family_resemblance_final_audit.md) and [270](270_first_experience_archaeology_audit.md) |
| Typography | Sans-only; no Iowan wordmark plate |
| Materials | White card on cool gray — not stone/paper gradients |
| Hierarchy | Functional but reads as separate auth product |
| Logo | Text wordmark only — acceptable; placement/spacing not aligned with instrument surfaces |

OAuth, email/password, forgot password, and create-account **flows are correct** — presentation only.

### Mockup

- HTML: `validation/mockups/beta/first_experience/01_welcome_sign_in.html`
- Screenshot: `validation/mockups/beta/first_experience/screenshots/01_welcome_sign_in.png`

### Primitive reuse

| Mockup class | Production target | Status |
|--------------|-------------------|--------|
| `body.rm-instrument-surface` | `family_resemblance.css` / Settings H10 layer | **Reuse** |
| `fe-wordmark` | Profile name plate serif (`--rm-serif`) | **Reuse** (typography) |
| `fe-card` | G3 `tcard` / Settings panel card | **Adapt** — wire to `tcard` or shared auth card primitive at implement |
| `fe-btn-primary` | Map M2-X GV `.gv-btn-search` / instrument sage CTA | **Reuse** (token-aligned) |
| `fe-btn-oauth` | `auth.html` `.btn-oauth` | **Reskin** — keep DOM contract |
| `fe-input`, `fe-label` | Settings field stack / `auth.html` `.field` | **Reskin** |
| `fe-pw-toggle` | `auth.html` `.pw-toggle` | **Reuse** behavior |
| `fe-link` | `auth.html` `.link-btn` | **Reskin** |
| `fe-divider` | `auth.html` `.oauth-divider` | **Reuse** |

### Implementation difficulty

**Medium** — CSS/token swap on `auth.html`; no auth logic changes.

### Dependencies

- Approved mockup
- `family_resemblance.css` token import on `auth.html`
- No backend/OAuth changes

---

## Mockup 2 — Create Account

### Purpose

Same family as sign-in; communicates **one continuous journey** (auth → birth → map), not a standalone signup funnel.

### Existing production screen

`auth.html` — signup view (default on cold load). Screenshot: `bi_archaeology/01_auth_signup.png`.

### Problems

Same material/typography outliers as Mockup 1.

### Mockup

- HTML: `validation/mockups/beta/first_experience/02_create_account.html`
- Screenshot: `validation/mockups/beta/first_experience/screenshots/02_create_account.png`
- Journey signal: `fe-progress-dots` (step 1 of 4)

### Primitive reuse

Same mapping as Mockup 1. `fe-progress-dots` is a **mockup-only journey indicator** — no production primitive today.

### Implementation difficulty

**Medium** — paired with Mockup 1 auth reskin.

### Dependencies

- Mockup 1 approved token layer

---

## Mockup 3 — Birth Information

### Purpose

Single calm step collecting **only Beta-required fields**: Display name, Birth date, Birth time (exact), Birth location. One conceptual step — payoff is the personalized map, not per-field micro-rewards (270 §14.3).

### Existing production screen

`first_profile_intake.js` overlay (`#rm-first-profile-intake`). Screenshot: `bi_archaeology/10_birth_intake_default.png`.

### Problems

| Issue | Detail |
|-------|--------|
| Visual outlier | Dark purple inline CSS — developer overlay, not instrument family |
| Doctrine mismatch | Exact / Unknown time toggle — **remove from Beta path** (270 §14.1) |
| Context | Full-screen overlay on map feels like interruption, not journey step |
| Location search | Uses `RMPlaceSearch` correctly but styled unlike map `rm-sls-*` chrome |

### Mockup

- HTML: `validation/mockups/beta/first_experience/03_birth_information.html`
- Screenshot: `validation/mockups/beta/first_experience/screenshots/03_birth_information.png`
- **No Unknown Time control**

### Primitive reuse

| Mockup class | Production target | Status |
|--------------|-------------------|--------|
| `fe-card`, `fe-input`, `fe-label` | Intake fields / Settings fields | **Reskin** |
| `fe-sls-wrap`, `fe-sls-input`, `fe-sls-panel`, `fe-sls-item` | `map_CURRENT.html` `.rm-sls-*` via `RMPlaceSearch` | **Reuse** |
| `fe-btn-primary` | Intake `.submit-btn` → instrument CTA | **Reskin** |
| `fe-progress-dots` | — | **Mockup-only** (step 2 of 4) |

### Implementation difficulty

**Medium–High** — replace inline purple stylesheet; remove Unknown toggle from Beta path; consider full-page route vs overlay (journey decision for BI-0C).

### Dependencies

- `RMPlaceSearch` / `place_search_client.js` (unchanged)
- `POST /profiles/create-with-birth` (unchanged)
- Mockup 5 transition slot in navigation flow

---

## Mockup 4 — Validation (three states)

### Purpose

Show real Beta validation messages — invalid time, missing location, missing birth time.

### Existing production screen

`first_profile_intake.js` client validation + `#rm-intake-err`. Screenshot: `bi_archaeology/12_birth_intake_validation_error.png`.

### Mockups

| State | HTML | Screenshot | Message |
|-------|------|------------|---------|
| Invalid time | `04_validation_invalid_time.html` | `screenshots/04_validation_invalid_time.png` | Birth time must be a valid time on a 24-hour clock. |
| Missing location | `04_validation_missing_location.html` | `screenshots/04_validation_missing_location.png` | Birth place is required. Search and select a city from the list. |
| Missing time | `04_validation_missing_time.html` | `screenshots/04_validation_missing_time.png` | Birth time is required for Beta relocation. |

### Primitive reuse

| Mockup class | Production target | Status |
|--------------|-------------------|--------|
| `fe-alert-err` | `auth.html` `.alert-err` / shell alerts | **Reskin** |
| `fe-input.is-error` | Invalid field border state | **Reuse** |
| `fe-sls-wrap.is-error` | Search wrapper error state | **Adapt** |

### Implementation difficulty

**Low** — CSS + copy alignment only.

### Dependencies

- Mockup 3 birth form shell
- Exact-time-only doctrine

---

## Mockup 5 — Transition (Preparing Your Personal Map)

### Purpose

Reserve a **full-screen bridge layout** for future virga/chart construction. **No animation design.**

### Existing production screen

**None** — intake success redirects directly to map ([270 §3](270_first_experience_archaeology_audit.md)).

### Mockup

- HTML: `validation/mockups/beta/first_experience/05_transition_preparing.html`
- Screenshot: `validation/mockups/beta/first_experience/screenshots/05_transition_preparing.png`

### Primitive reuse

| Element | Status |
|---------|--------|
| `fe-transition-full` / `fe-transition-stage` | **New layout primitive** — full-viewport stage |
| `fe-reserved` | Animation mount placeholder (future) |
| `fe-wordmark`, `fe-progress-dots` | Journey chrome (mockup-only dots) |

### Implementation difficulty

**Low (static)** / **High (animated)** — animation deferred.

### Dependencies

- Navigation insert between intake success and map

---

## Mockup 6 — First Personalized Map

### Purpose

First map view after birth entry — explore chrome, Genie, ghost, city search, save disk, nameplate. **No walkthrough overlays.**

### Existing production screen

`map_CURRENT.html` post-intake (M2-X harmonized).

### Mockup

- HTML: `validation/mockups/beta/first_experience/06_first_personalized_map.html`
- Screenshot: `validation/mockups/beta/first_experience/screenshots/06_first_personalized_map.png`

### Primitive reuse

| Mockup class | Production target | Status |
|--------------|-------------------|--------|
| `fe-nameplate` | Profile selector chip | **Reuse** |
| `fe-sls-*` | `.rm-citysearch-wrap` / `.rm-sls-*` | **Reuse** |
| `fe-gv-builder`, `fe-gv-chip`, `fe-gv-dd` | Genie v6 builder | **Reuse** |
| `fe-ghost`, `fe-save-disk` | Map explore chrome | **Reuse** |

### Implementation difficulty

**Low** — journey wiring; map exists.

### Dependencies

- Profile + birth record created before this view

---

## Mockup 7 — First Popup

### Purpose

First city popup as a first-time user would see it — **real production popup structure**.

### Existing production screen

`map_CURRENT.html` `buildRelocatedPopupHtml()` — `.popup-chart-shell`, `.popup-chart`.

### Mockup

- HTML: `validation/mockups/beta/first_experience/07_first_popup.html`
- Screenshot: `validation/mockups/beta/first_experience/screenshots/07_first_popup.png`

### Primitive reuse

`.popup-chart*` classes — **Reuse verbatim** from `map_CURRENT.html`.

### Implementation difficulty

**None** — already production.

---

## Mockup 8 — First Save

### Purpose

Save investigation flow consistent with Notes and Comparison.

### Existing production screen

`map_CURRENT.html` `#rm-save-dialog` / `.rm-sdlg-*`.

### Mockup

- HTML: `validation/mockups/beta/first_experience/08_first_save.html`
- Screenshot: `validation/mockups/beta/first_experience/screenshots/08_first_save.png`

### Primitive reuse

`rm-sdlg-card`, `rm-sdlg-field`, `rm-sdlg-btn-*` — **Reuse**; buttons **reskin** to instrument tokens.

### Implementation difficulty

**Low**

---

## Primitive audit (complete)

### Reused from production

| Primitive | Source | Mockups |
|-----------|--------|---------|
| `rm-instrument-surface` / `--rm-*` | `family_resemblance.css` | All |
| `rm-sls-*` location search | `map_CURRENT.html`, `RMPlaceSearch` | 3–4, 6 |
| `popup-chart*` | `map_CURRENT.html` | 7 |
| `rm-sdlg-*` save dialog | `map_CURRENT.html` | 8 |
| Genie / ghost / save disk | Map M2-X | 6 |
| Auth field layout | `auth.html` DOM | 1–2 |

### Mockup-only (flagged, not silently invented)

| Primitive | Purpose |
|-----------|---------|
| `fe-progress-dots` | Journey step indicator |
| `fe-transition-full` | Bridge layout container |
| `fe-reserved` | Animation mount placeholder |

### Gaps

| Gap | Notes |
|-----|-------|
| Unified auth stylesheet | Extract from `auth.html` inline styles |
| First-run route vs overlay | BI-0C decision |
| Official Google brand asset | Mockup uses typographic placeholder |

---

## Family resemblance review

**Panel:** `validation/mockups/beta/first_experience/screenshots/family_resemblance/family_resemblance_panel.html`

### Verdict

| Surface | Same app? | Notes |
|---------|-----------|-------|
| Auth mockups 1–2 | **Yes (mockup)** | Production `auth.html` is outlier — see `auth_family_row.png` |
| Birth mockups 3–4 | **Yes (mockup)** | Production purple intake is outlier |
| Transition 5 | **Yes** | Neutral bridge fits family |
| Map 6–8 | **Yes** | M2-X lineage; popup typography partially aligned ([264]) |

**Overall:** Mockups belong with Profile, Comparison, Notes, Settings. Production auth/intake **today would not**.

### Gaps (not solved in BI-0B)

1. Production auth and intake remain outliers until implement.
2. Popup typography cooler than chart plates.
3. Save dialog production buttons still legacy blue.
4. Progress dots have no production equivalent.

---

## Recommended next slices (BI-0C+)

| Slice | Scope |
|-------|-------|
| **BI-0C** | Auth reskin on `auth.html` |
| **BI-0D** | Birth information page; remove Unknown time from Beta |
| **BI-0E** | Transition route (static layout) |
| **BI-0F** | Journey routing auth → birth → transition → map |
| **BI-0G** | Save dialog token harmonization |
| **Defer** | Virga/rain, walkthrough auto-start, Apple OAuth |

---

## Success criteria

- [x] `results/271_first_experience_mockups.md`
- [x] `validation/mockups/beta/first_experience/` complete
- [x] Screenshots + family resemblance panel
- [x] Primitive audit
- [x] No production code changes

**Status:** BI-0B complete — awaiting PO mockup approval.

---

*End of BI-0B first experience mockups.*
