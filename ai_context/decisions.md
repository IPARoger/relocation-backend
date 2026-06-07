# Decisions

## Architecture

- Preserve a strict distinction between canonical astrology truth and frontend display geometry.
- Do not solve seam/dateline issues by changing canonical region membership.
- Use truth-grid generation for house/sign regions where binary membership must match point-and-click truth.
- Keep contour generation as fallback until truth-grid is broadly validated.
- Do not change ASC/MC aspect astrology semantics while optimizing rendering or staging.
- **2026-05-21: Phase-C production migration path.** The production visible-overlay path for `map_CURRENT.html` will be migrated to `/screen-pixel-truth` via a substrate-adapter layer (Path A in `PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` §10 Step 0). The Phase-2 cache integration follows the substrate migration.

## Map Strategy

- Stay on Leaflet for MVP.
- Reassess MapLibre, Mapbox, or Google Maps later only if concrete rendering, city-density, or vector-interaction blockers remain.
- Display-layer imperfections are acceptable only when canonical truth remains correct and traceable.

## UX Strategy

- Map-first experience.
- Avoid major drawer/genie redesign until the broader design system is considered.
- Account, intake, comparison, settings, and saved chart screens should help define the app's premium design language.
- AI features come after the non-AI professional core is strong.

## Validation Strategy

- Preserve validation reports, screenshots, and narratives as proof-of-work.
- Stress test incrementally rather than through large rewrites.
- Prefer small reversible changes with focused validation.
- Keep local browser junk out of git.

## Archaeology-hardened engineering doctrine (process)

- Treat **wrong active file / wrong running module / stale server** as first-class bug categories before rewriting math.
- Separate **debugging mode** responses from **architecture mode** responses; avoid speculative musings during surgical fixes.
- Prefer **full-file or diff-based edits** for indentation-critical Python when the operator is not a full-time programmer.
- Independent **brute-force or dense sampling truth exports** remain a valid way to settle “is this math or rendering?” disputes.

## Product semantics (from repeated user corrections)

- **House + angle-sign regions** are binary truth surfaces for users: “inside means true.”
- **Aspect-to-angle** overlays are anchored on exact centerlines; **soft aura** expresses strength but must not pretend to redefine membership.
- **Overlap zones** are often the primary decision object in relocation exploration, not isolated bands.
- **2026-05-26: transported-material renderer doctrine.** Aspect-to-angle beta visuals should be treated as transported material strips, not aura/glow/fog around splines. The accepted validation architecture uses local `(s,u)` texture-coordinate transport, independent side normalization, and proportional material scaling under asymmetry. Aesthetic/material language remains flexible, but transport architecture should not reopen unless map-context validation proves structural failure.
- **2026-05-26: overlap hot-zone doctrine.** Overlaps are semantically important discovery zones, not merely clutter. Future hotspot signaling must balance readability with “this matters,” remain optional or user-controlled when intensifying, and avoid paternalistic ranking language.

## Rejected institutional lessons (do not revive casually)

- Backend **seam surgery** that alters canonical polygon topology to satisfy map-window edges.
- Replacing Swiss Ephemeris truth with **placeholder constants** during debugging.
