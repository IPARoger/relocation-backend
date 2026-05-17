# Decisions

## Architecture

- Preserve a strict distinction between canonical astrology truth and frontend display geometry.
- Do not solve seam/dateline issues by changing canonical region membership.
- Use truth-grid generation for house/sign regions where binary membership must match point-and-click truth.
- Keep contour generation as fallback until truth-grid is broadly validated.
- Do not change ASC/MC aspect astrology semantics while optimizing rendering or staging.

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
