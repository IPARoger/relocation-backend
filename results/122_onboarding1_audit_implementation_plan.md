# ONBOARDING-1: Onboarding Flow Audit + Implementation Plan

**Date:** 2026-06-19  
**Type:** Audit + plan only — no implementation authorized  
**Sources:** `results/92_sux2_onboarding_overlay.md`, `results/85_web2_completion_audit.md`, `results/101b_profile_workflow_truth_audit.md`, `results/101c_settings_polish_backlog.md`, `results/104_web2_wiring_priority_plan.md`

---

## Current Onboarding Surfaces (as-built)

| Surface | Location | Trigger | Persistence | Status |
|---------|----------|---------|-------------|--------|
| First profile intake | `first_profile_intake.js` | Store bootstrap → `INTAKE_REQUIRED` (no profiles) | N/A (writes profile) | **Functional** |
| Guided app tour | `app_shell.html` `#guidedOnboardingModal` | `maybeShowGuidedOnboarding()` after bootstrap if key absent | `localStorage.rm_guided_onboarding_dismissed` | **Functional** (7 slides, S-UX-2) |
| Map tooltip | `map_CURRENT.html` `.map-onboarding` | First map visit per session | `sessionStorage.rm_map_onboarding_dismissed` | **Minimal** (one sentence) |
| Help replay | Settings → About area / Help | Manual `replay-guided-onboarding` | Clears dismiss key | **Functional** |
| Add Profile intake | `first_profile_intake.js` mode `add` | Profile Management → Add | Same write path as first-run | **Plumbing present** |

---

## Doctrine / Product Expectations (synthesized)

1. **First-run path:** intake → optional orientation → map — must not feel broken (85, 101b).
2. **Guided tour:** concrete app-usage steps, dismissible, replayable (92 — **met** post S-UX-2).
3. **Map orientation:** more than one sentence for relocated-chart discovery (85 — **partial**).
4. **No click interception:** guided modal must not block Settings / Manage Profiles on first visit (101b, 101c #8, 104).
5. **Comparison guidance:** explain favorites / place-picker flow (85 — **partial**, no dedicated onboarding).
6. **Per-account onboarding state:** deferred in 92; localStorage-only is acceptable interim.
7. **Genie / Ghost tools:** power-user features need guided entry (85 — tour covers at high level).

---

## Gap Analysis

| Gap | Severity | Evidence |
|-----|----------|----------|
| Guided modal intercepts shell clicks until dismissed | **High** | 101b: Settings / Manage Profiles appear broken on first session |
| Map onboarding is single session tooltip | **Medium** | 85: no multi-step map tips; no favorites/compare mention on map |
| No comparison-workspace onboarding | **Medium** | 85: comparison intake guidance listed PARTIAL |
| Intake → tour sequencing undefined | **Low** | Intake redirects to map with `skipOnboarding`; tour shows on next `app_shell` visit — can double-orient or miss map-first users |
| Notes / PIH / dignities not in tour | **Low** | Product grew since slide copy written (Notes Library, PIH dignities) |
| Per-account dismiss / replay sync | **Low** | 92 deferred; new browser = tour replays |

---

## Implementation Plan (ordered slices)

### ONBOARDING-2 — Modal interaction fix (P0)

**Goal:** Guided tour does not block navigation to Settings, Profiles, or sidebar routes.

**Approach options (pick one in implementation):**
- A) Render tour non-blocking (corner card, no full-screen backdrop capture)
- B) Defer auto-show until after first explicit navigation away from dashboard
- C) Auto-dismiss on first nav click outside tour (with “Resume tour” in Help)

**Files:** `app_shell.html` (modal CSS, `maybeShowGuidedOnboarding`, backdrop handler)  
**Smoke:** extend `scripts/smoke_onboarding.py` — navigate to Settings while tour visible  
**Estimate:** 2–4 h

### ONBOARDING-3 — Map tooltip expansion (P1)

**Goal:** 2–3 step map onboarding (right-click chart, favorites star, Compare entry) with persistent dismiss.

**Files:** `map_CURRENT.html`, optional shared copy config  
**Smoke:** `scripts/smoke_map_current.py` assertion for tooltip steps  
**Estimate:** 3–5 h

### ONBOARDING-4 — Comparison overlay primer (P2)

**Goal:** First visit to comparison route shows one-time inline hint (Family A/B, 2–5 places) — not a modal.

**Files:** `app_shell.html` compare screen / overlay; `localStorage.rm_cmp_onboarding_seen`  
**Smoke:** extend `smoke_comparison_sets.py`  
**Estimate:** 3–4 h

### ONBOARDING-5 — Tour content refresh (P2)

**Goal:** Update `ONBOARDING_SLIDES` for Notes Library, comparison workspace, PIH dignities toggle (mention only), saved-location search.

**Files:** `app_shell.html` (`ONBOARDING_SLIDES` only)  
**Smoke:** `smoke_onboarding.py` slide count + keyword checks  
**Estimate:** 1–2 h

### ONBOARDING-6 — Intake ↔ tour sequencing (P3)

**Goal:** Document and implement clear rule: intake success → map first **or** shell dashboard with tour; avoid duplicate blocking overlays.

**Files:** `first_profile_intake.js`, `app_shell.html` bootstrap  
**Estimate:** 2–3 h

### ONBOARDING-7 — Per-account state (future / P4)

**Goal:** Persist onboarding completion in `user_settings` / account snapshot (92 deferred item).

**Files:** backend settings schema + `app_shell.html`  
**Blocked by:** settings persistence slices (SETTINGS-2+)

---

## Recommended execution order

1. ONBOARDING-2 (unblock Settings — highest user-reported friction)
2. ONBOARDING-3 (map discoverability)
3. ONBOARDING-5 (cheap copy alignment)
4. ONBOARDING-4 (comparison)
5. ONBOARDING-6 → ONBOARDING-7

---

## Explicit non-goals (this plan)

- Renderer / Genie engine changes
- Video or interactive spotlights on live map canvas
- Onboarding for admin / dev tools
