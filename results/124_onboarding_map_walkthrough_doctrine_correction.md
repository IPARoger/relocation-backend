# Onboarding Map Walkthrough — Doctrine Correction

**Status:** Authoritative product doctrine (correction)  
**Date:** 2026-06-19  
**Type:** Onboarding doctrine — supersedes conflicting plan language  
**Supersedes:** Onboarding plan language in `results/122_onboarding1_audit_implementation_plan.md` that centered Favorite, Profile, or Compare teaching in the main walkthrough

---

## Core Rule

**The onboarding walkthrough is MAP ONLY.**

Do not teach Favorite, Profile, or Compare in the main walkthrough. Those flows are obvious enough or are taught contextually when the user reaches them.

---

## Entry Sequence

1. User completes first chart / profile creation (intake).
2. App opens the **map** (not a shell tour blocking navigation).
3. **Preload three Genie variables** so the map is not empty on arrival.
4. User **adds one variable** (hands-on, minimal).
5. User **launches / searches the map** (Search Map).

---

## Walkthrough Mechanics

- Use **peep-hole overlays** (spotlight cutouts) on the live map — short, focused steps.
- **Dismissible** at any time; **replayable** from Help (or equivalent).
- Target **5–7 overlays** total — keep it short.
- **Mobile adaptation** is a later phase; desktop map first.

---

## Peep-Hole Overlay Curriculum (canonical order)

| # | Topic |
|---|--------|
| 1 | Genie variable controls |
| 2 | Right-click / current-location popup |
| 3 | Mute / Solo / Not ghost tools |
| 4 | Location search |
| 5 | Pin and <> history controls |
| 6 | Night mode |
| 7 | Save search |
| 8 | Map notes *(optional — include only if scope stays within 5–7 overlays with grouping)* |

---

## Explicit Non-Goals (main walkthrough)

- Favorites workflow
- Profile management / switching
- Comparison workspace
- Shell Settings navigation
- Multi-slide modal app tour as the primary onboarding surface

---

## Relation to Other Onboarding Artifacts

| Artifact | Role after this correction |
|----------|----------------------------|
| `first_profile_intake.js` | Unchanged — birth/profile creation gate |
| `app_shell.html` guided tour (`ONBOARDING_SLIDES`) | **Not** the canonical first-run walkthrough; may remain as optional Help replay or be retired in favor of map walkthrough |
| Map tooltip (single sentence) | Subsumed by peep-hole sequence |
| `results/122_onboarding1_audit_implementation_plan.md` | Audit remains valid; **implementation slices ONBOARDING-3/4/5** that emphasized Favorites/Compare tour copy are **superseded** by this document for walkthrough scope |

---

## Engineering Notes (future implementation)

- Peep-hole overlays should not block map pan/zoom where the step requires interaction.
- Preloaded variables + “add one” should use the same Genie variable builder path as production.
- Dismissal persistence: browser-local acceptable for v1; per-account sync deferred.
- Replay clears dismissal and restarts from overlay 1 on the map.
