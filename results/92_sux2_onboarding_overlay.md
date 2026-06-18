# S-UX-2 — Guided Onboarding Overlay

**Roadmap ID:** S-UX-2  
**Checkpoint:** c5b9b31 (S-UX-1 complete)  
**Status:** VERIFIED (smoke-gated)

## Files Changed

| File | Change |
|------|--------|
| `app_shell.html` | Multi-slide guided onboarding overlay, `ONBOARDING_SLIDES` config, Help replay button |
| `scripts/smoke_onboarding.py` | Minimal Playwright smoke for slides, dismiss, replay |
| `relay/ROADMAP_QUEUE.md` | S-UX-2 ✅ entry |

## Slide Content

| # | Title | Summary |
|---|-------|---------|
| 1 | Welcome | Relocation astrology overview — explore, save, compare |
| 2 | Meet Genie | Build searches (e.g. ASC in Aries), Search Map → overlays, reopen saved |
| 3 | Map Controls | Find regions, Save Investigation, city search, Chart Library, profile switch |
| 4 | Ghost Tools | Mute, Solo, Not, Color chip (Genie layer controls + Exploration Mode) |
| 5 | Layer Visibility | Mute/Solo + Preview Exploration Mode to reduce clutter |
| 6 | Save & Compare | Favorites, saved investigations, Compare places |
| 7 | You're Ready | Launch Map CTA; dismiss permanently |

Copy lives in `ONBOARDING_SLIDES` inside `app_shell.html` (single config object).

## Persistence / Dismissal

- **Key:** `localStorage.rm_guided_onboarding_dismissed === "1"`
- **Auto-show:** `maybeShowGuidedOnboarding()` after bootstrap when key absent
- **Dismiss anytime:** Dismiss button, backdrop click, Launch Map (final slide)
- **Manual relaunch:** Help & Learn → **Replay app tour** (clears key, calls `showGuidedOnboarding()`)
- **Not per-account:** browser-local only (existing S-UX-1 contract)

## Validation

```bash
set -a && source .env.staging && set +a
venv/bin/python scripts/smoke_map_current.py
venv/bin/python scripts/smoke_saved_investigations.py
venv/bin/python scripts/smoke_onboarding.py
```

## Deferred

- Floating map chrome (Back/Forward/Pin/Saved searches toolbar) — prototype-only; slide 3 uses existing map panel controls instead
- Opacity slider for layers — not in production Genie; slide 5 uses Mute/Solo/Exploration Mode
- Per-account onboarding state in `user_settings` — future production requirement

## Validation Results

| Smoke | Result |
|-------|--------|
| `smoke_map_current.py` | PASS |
| `smoke_saved_investigations.py` | PASS (retry after transient auth 403) |
| `smoke_onboarding.py` | PASS |

**Commit:** `2a9ca9e`

## Verdict

**PASS** — Placeholder onboarding replaced with 7-slide app-usage tour. Dismissal persists via localStorage; replay wired through Help. Scope limited to `app_shell.html` + smoke; no renderer/backend changes.
