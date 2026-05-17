# Product Brief

## Product

This is a relocation astrology mapping app. Its core value is a map-first professional workflow where astrologers can search for geographically meaningful relocation conditions and visually inspect candidate places.

The app should become a calm, premium, trustworthy instrument for exploration, not a cluttered dashboard.

## Current Core Capabilities

- `truth_grid` house overlays for Planet-in-House searches.
- Staged/shared-grid ASC overlays for faster ASC all-major aspect rendering.
- Angle-in-Sign MVP for `ASC` and `MC`.
- Planet Aspect to Angle overlays using backend centerlines.
- Point-and-click popup truth checks for local chart details.
- Debug geometry mode for tracing backend canonical features through frontend display features.

## Product Philosophy

- The map is the primary visual instrument.
- Controls should serve exploration, not dominate it.
- Prefer elegance, usability, beauty, intuitiveness, and common sense.
- Avoid "too clever" UI that creates artificial stupidity.
- Keep the experience professional-grade, calm, inviting, premium, restrained, and trustworthy.
- Users should enjoy spending time in the app.
- Professional users need power without clutter.
- AI should support the professional core later, not replace it.

## Overlay Truth Standard

The app should not casually accept mathematical inaccuracies. Canonical backend geometry must be trustworthy and stable. Frontend wrapping, clipping, and display adaptation must never change logical astrology semantics.

Acceptable MVP imperfections:

- Rough visual edges.
- Imperfect seam cosmetics.
- Visible discontinuities where display rendering is limited.

Not acceptable:

- False region membership.
- Misleading fills.
- Topology corruption.
- Overlay identity changing at the dateline.

## Current Architecture Direction

- Keep canonical truth and display geometry conceptually separate.
- Keep `truth_grid` opt-in until broader validation supports making it default.
- Keep contour fallback available.
- Keep Leaflet for MVP unless concrete blockers remain after display-geometry cleanup.
- Avoid map-library migration until there is evidence the remaining issues are Leaflet-specific.

## Validation Corpus

Validation records, reports, screenshots, and narratives are part of the proof corpus. They preserve evidence for:

- Baseline charts.
- High northern charts.
- High southern charts.
- Antimeridian/seam behavior.
- Truth-grid contradictions.
- Angle-in-Sign behavior.
- ASC staged overlay behavior.
- Dropdown and UX regressions.

Validation should remain visible and durable enough that future chats can continue without losing the reasoning trail.
