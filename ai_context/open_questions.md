# Open Questions

## Product and UX

- What is the minimum elegant sidebar/control model for MVP without over-designing?
- Should the current native select controls remain, or should only unstable controls become custom dropdowns later?
- How should overlap colors communicate "candidate city shopping cart" semantics without muddy alpha stacking?
- What is the right onboarding hint for point-and-click chart inspection?

## Astrology and Search

- When should `truth_grid` become the default for house overlays?
- When should `DC` and `IC` be added to Angle-in-Sign and Aspect-to-Angle searches?
- How should negative/exclusion conditions such as Saturn not in 12th be represented visually?
- What is the correct MVP treatment for aspect aura/orb intensity around angular centerlines?

## Validation

- Which additional chart fixtures should be added before broader release?
- Can the `+/-65` latitude cap be safely relaxed after a polar stress suite?
- How should future validation records distinguish visual artifact, mathematical contradiction, and acceptable MVP roughness?

## Infrastructure

- How much repo context should the local AI reviewer include by default without producing noisy reviews?
- Should future reviewer outputs be archived by timestamp, or should only latest files be kept in git?
- Which parts of `ai_context/` should remain durable public project memory versus private local notes?
