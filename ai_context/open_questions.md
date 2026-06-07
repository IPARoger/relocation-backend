# Open Questions

## Product and UX

- What is the minimum elegant sidebar/control model for MVP without over-designing?
- Should the current native select controls remain, or should only unstable controls become custom dropdowns later?
- **Optional first planet-in-house condition:** allow search with only aspect-to-angle or angle-in-sign (no house A) — deferred until drawer/control redesign; see `validation/narratives/map_current_qa_cleanup_pass.md`.
- How should overlap colors communicate "candidate city shopping cart" semantics without muddy alpha stacking?
- How should overlap hot zones signal “this matters” without becoming paternalistic ranking?
- What mobile drawer/progressive-disclosure pattern can support mute, solo, send-to-background, send-to-foreground, and negative / NOT mode without becoming a Photoshop layer panel?
- What is the right onboarding hint for point-and-click chart inspection?

## Astrology and Search

- When should `truth_grid` become the default for house overlays?
- When should `DC` and `IC` be added to Angle-in-Sign and Aspect-to-Angle searches?
- How should negative/exclusion conditions such as Saturn not in 12th be represented visually?
- What is the correct MVP treatment for aspect aura/orb intensity around angular centerlines?
- Does the transported-material beta renderer survive real Leaflet map context with labels, zoom levels, pane ordering, and production-density overlays?
- When should rain/virga discovery work resume relative to map-context validation and overlap governance?

## Validation

- Which additional chart fixtures should be added before broader release?
- Can the `+/-65` latitude cap be safely relaxed after a polar stress suite?
- How should future validation records distinguish visual artifact, mathematical contradiction, and acceptable MVP roughness?

## Infrastructure

- How much repo context should the local AI reviewer include by default without producing noisy reviews?
- Should future reviewer outputs be archived by timestamp, or should only latest files be kept in git?
- Which parts of `ai_context/` should remain durable public project memory versus private local notes?

## Consolidated from archaeology (needs ongoing reconciliation with code)

- What is the single public definition of **MC geometry** in product language (relocated ecliptic MC vs culmination-style framing), and how is it tested?
- How should **latitude policy** be communicated when ASC, houses, and global sampling grids use different practical limits?
- Should **brute-force validators** live forever as reference tooling, CI fixtures, or occasional manual scripts?
- What is the final **overlap color system** when more than two conditions saturate opacity?
- How do we rank and disambiguate **city search** globally (importance vs population vs user intent) without astro.com-style cryptic labels?
- What is the right **tradeoff UX** for constrained relocation decisions (compare two or three cities) in a map-first layout?
