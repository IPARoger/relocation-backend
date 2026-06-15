# City Search And Polar Strategy Notes

Date: 2026-05-17

## City/Search Limitations

Current city search is useful for quick lookup but remains MVP-level.

Known limitations:

- Search returns the first partial name match, not a ranked result list.
- Country display exists in city markers/popups, but search discoverability is limited.
- City density is controlled mainly by population threshold and zoom level, not by visible density per square inch.
- Dense regions and sparse regions are not normalized, so some map areas can feel cluttered while others feel empty.
- Search does not yet handle alternate names, accents, administrative regions, or multiple cities with the same name.

Likely future approach:

- Add a small search result list for ambiguous city names.
- Rank by exact match, population, country, and viewport proximity.
- Tune city rendering by screen density or tile/viewport bins instead of only population.
- Keep country in all displayed city results.
- Consider precomputed city tiers or clustered display before considering a map-library migration.

Recommendation:

- Do not redesign city UX yet.
- First improve search result clarity and country display consistency.
- Then tune density heuristics after broader manual QA reveals actual clutter patterns.

## Polar Strategy

Current behavior:

- Truth-grid house and angle-sign regions use the existing `+/-65` latitude cap.
- Popup truth outside the cap warns that Placidus relocation charts are capped for now.

Likely risks above `+/-65`:

- Placidus houses can become undefined or unstable at high latitudes.
- ASC/MC sign fields may still be computable where house systems become pathological, which can confuse users if mixed with capped house overlays.
- Region topology can compress sharply near polar latitudes.
- Visual continuity near the cap could imply unsupported mathematical certainty.

Recommended strategy:

- Keep the `+/-65` cap for MVP.
- Add explicit professional override later, not now.
- Treat override output as advanced/experimental and visibly label it.
- Build a polar stress suite before considering default cap expansion.

Future polar fixtures:

- June solstice high Arctic.
- December solstice high Antarctic.
- Equinox high north.
- Equinox high south.
- Same charts sampled at `65`, `66`, `70`, and `75` degree latitudes.

Recommendation:

- Keep cap now.
- Add configurable override only after baseline MVP stabilizes.
- Do not remove the cap until mathematical failure modes are documented and UX warnings are designed.
