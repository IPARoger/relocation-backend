# Relocation App Product Roadmap

This document preserves the current product strategy, development sequence, UX philosophy, and validation priorities for future work.

## 1. Current Stable Milestone

The app has reached an important early professional-tool milestone:

- `truth_grid` house overlays are working and remain opt-in.
- Staged/shared-grid ASC overlays are working.
- Angle-in-Sign MVP for `ASC` and `MC` is working.
- Seam behavior is visually coherent in current manual QA.
- Popup truth generally matches overlays in current validation.
- Validation contradictions are `0` in current truth-grid and angle-sign tests.
- Difficult High Northern and Southern edge cases have passed manual QA.
- The app is now viable as an early professional astrology exploration tool, pending UX cleanup and broader fixture testing.

Current caveats:

- The UI is still prototype-like.
- `truth_grid` is not yet default.
- The `+/-65` latitude cap remains in place.
- Stress-test coverage needs to expand before broad release.

## 2. Product Philosophy

The app should be a map-first experience. The map is the product surface; controls exist to serve exploration, not dominate it.

Core principles:

- Elegance, usability, beauty, and intuitiveness matter.
- Avoid self-indulgent bells and whistles.
- Avoid "too clever" UI that creates artificial stupidity.
- The environment should feel professional-grade, calm, inviting, premium, restrained, and trustworthy.
- Users should enjoy spending time in the app.
- Visual design should communicate confidence without becoming flashy.
- Controls should make exploration easier, not compete with the map.
- Professional users need power, but not clutter.
- Lay users need guidance, but not patronizing simplification.

The app should feel like a refined professional instrument, not a dashboard full of gimmicks.

## 3. Core Search Types

Current and near-term search types:

- Planet in House
- Angle in Sign
- Planet Aspect to Angle

Important domain note:

- Planet-to-planet relocation search is not meaningful because planets do not move relative to each other under relocation. Relocation changes angles, houses, and place-dependent relationships, not natal planet-to-planet geometry.

Future search types:

- `DC` and `IC` support for Angle in Sign.
- Possibly `DC` and `IC` support for Aspect to Angle.
- Negative/exclusion conditions, such as Saturn not in 12th.
- Multi-condition intersection searches.
- More sophisticated combinations such as required, optional, and excluded factors.

## 4. Overlay/Color System Roadmap

Overlap is the answer. Overlap regions are the "shopping cart" of candidate cities: the map should make it obvious where multiple desired conditions coincide.

Overlay design requirements:

- Overlap regions must be visually explicit.
- Overlays must stay transparent enough to read map labels and cities.
- Avoid naive alpha stacking when it makes purple or dark colors dominate.
- Design a semantic "child color" blending system for overlaps.
- Overlap can be brighter or more luminous, but should not simply become more opaque.
- Search controls should eventually reflect the selected overlay color, so the UI itself acts as the legend.
- The current legend is too space-consuming and should eventually be removed or replaced.

Color families should distinguish:

- Planet in House
- Angle in Sign
- Aspect to Angle
- NOT/exclusion regions

Exclusion/NOT regions:

- Should not light up the whole inverse region.
- Should use subtle grey, black, desaturated, or "off limits" treatment.
- May use texture or pattern.
- Should communicate constraint without visually overwhelming positive search intent.

Longer term:

- The color system should become theme-aware for light/dark maps.
- Color semantics should remain readable for colorblind users.
- Overlap treatment should scale to multi-condition searches without visual mud.

## 5. Aspect Aura Roadmap

Current aspect overlays are centerlines only.

The next visual layer should add a frontend-rendered aura/intensity field around ASC/MC aspect lines:

- Approximate orb: 5-8 degrees on either side.
- Aura should not look like a fat speed bump.
- Aura should be subtle at the outer edge and intensify sharply/nonlinearly toward the centerline.
- Use an exponential/Gaussian-like ramp, but tuned to feel visually concave and elegant.
- The centerline remains the darkest/strongest point.
- Aura shows "extra juice" inside broader house/sign regions.
- Frontend rendering is preferred initially so visual tuning is easier.
- Backend should remain the source of exact centerlines.

Purpose:

- House/sign regions show broad placement.
- Aspect aura shows intensified angular contact inside or across those regions.
- The aura should help professional users quickly see where a city is close enough to matter without pretending every part of a broad band has equal strength.

## 6. UX/Layout Roadmap

Known current issues:

- The current sidebar is too tall and wastes map real estate.
- Scrolling is awkward.
- Dropdown auto-advance behavior still exists and must be fixed.
- User-facing status text such as "Angular overlay ready" should not remain in its current form.
- Debug badge should remain debug-only.
- Popup UI needs aesthetic refinement.
- The right-click point-and-click feature needs an onboarding hint.

Design sequence:

- Before building the drawer/genie interaction, think deeply about the overall design system.
- The map is the primary visual instrument, but account, intake, comparison, and settings screens may define the soul and tone of the app because they contain more traditional interface design and long-form user interaction.
- Do not treat accounts, intake, and settings as boring utility screens.
- They should establish the app's premium, calm, elegant design language.
- The map control drawer/genie should grow out of that design language, not precede it as an isolated clever interaction.
- Avoid over-clever UI that hides obvious controls.
- Prioritize elegance, usability, beauty, intuitiveness, and common sense.
- Avoid artificial stupidity caused by overdesign.

Layout principles:

- The map should dominate.
- Controls should collapse or retract elegantly.
- Investigate drawer, genie, side-pocket, or compact panel concepts carefully.
- Do not over-design or make the UI too clever.
- Restore-control affordance must be obvious if controls are hidden.
- Avoid hiding essential controls in confusing ways.
- Mobile, tablet, ultrawide, and narrow desktop layouts must be considered.
- Controls should be discoverable and calm, not buried.

Onboarding:

- A small "Got it" dismissible overlay for map click/right-click instructions may be useful.
- The app should teach interaction affordances once, then get out of the way.

## 7. City Search / Geocoder Roadmap

Current city search needs improvement.

Required improvements:

- Add country names and readable disambiguation.
- Prioritize human relevance: population, historical importance, cultural prominence, and likely user intent.
- Atlanta, Georgia should rank before obscure Atlanta variants.
- Avoid astro.com-style cryptic country abbreviations.
- Support duplicate city names, especially in Brazil, India, and other countries with many repeated place names.
- Support old names and spelling variants, such as Cochin/Kochi.
- Support transliteration and non-Latin scripts eventually.
- Support multilingual users and international input.

Future geocoder direction:

- The geocoder should be much smarter than the current local city list.
- It should support ambiguity gracefully rather than pretending the first match is always right.
- It should eventually combine local curated data with a stronger geocoding source.
- City density should be based on visible map density and user relevance, not only raw population.

## 8. Birth Data / Accounts / Professional Mode Roadmap

Accounts are eventually needed, but not before the professional core stabilizes.

Future design areas:

- Account/chart library.
- Saved charts.
- Favorite cities.
- Comparison workspace.
- Settings, orbs, and preferences.
- Birth data intake.
- Later uncertain birth time intake.
- Professional/dumb mode vs AI-assisted mode.

Design priority:

- These screens should carry the app's premium design language.
- They should be calm and beautiful, not merely administrative.
- Their interaction patterns should inform the eventual map drawer/genie controls.

Birth data intake should become beautiful and trustworthy:

- Date
- Time
- Birthplace
- Historical timezone correctness
- Daylight saving correctness

Current-location interpretation is also a valid primary path, not just a prelude to searching elsewhere. The product should support users asking where they are now, why they moved there, what they moved toward or away from, what has worked or not worked after moving, and what the relocated chart explains, supports, or contradicts. Exploration remains the main draw for many target users — executives, digital nomads, students, van lifers, and professionals — but AI/intake may later suggest current-location review when appropriate without forcing that path. Stated intention should be respected without assuming it is perfectly fixed or equally committed in every case: future AI/intake may estimate confidence or commitment level, emphasizing supportive tradeoffs for strongly held aims while surfacing broader noteworthy opportunities for exploratory aims. Locations are never universally good or bad, only differently supportive for different aims.

Saved work:

- Multiple saved charts.
- Saved favorite cities.
- Comparison of multiple cities for one chart.
- Comparison of multiple charts, family charts, or client charts later.

### Saved Object Taxonomy

Use three product-layer meanings so "saved view" does not become ambiguous doctrine:

1. **Birth profile / client profile** — natal birth data and identity-level chart record.
2. **Relocated chart** — birth profile plus a specific destination, city, or location. This is a future durable object, not Phase 2.3 scope.
3. **Saved investigation** — birth profile / chart id plus semantic search conditions plus viewport/display context. Phase 2.3 implements this under the existing saved-view scaffold.

For saved investigations, persist inquiry semantics and viewport. Cache mathematical/truth substrate where useful. Do not persist graphic artifacts, renderer substrate, debug flags, resolution settings, aura/virga/raindrop output, or the full renderer request payload as durable product truth.

Local JSON is scaffold persistence only, not permanent product storage. Renderer behavior remains environment-controlled; the legacy production default remains unchanged.

### Phase 2.4 Sampling / Cache Scaffold

The Phase 2.4 sampling/cache scaffold should key off semantic investigation intent plus viewport/screen sampling scope. It must not key off saved rendered graphics, debug state, temporary aura flags, or renderer internals.

Point-level relocated chart calculation remains the truth source; pixel/subpixel sampling is a rendering strategy over that truth. Aura, raindrop, and virga outputs are deferred, but future outputs must derive from sampled truth/orb distance, not visual blur or fudge. Local/in-memory cache remains scaffold only, not permanent product storage.

### Phase 2.5 Sampling / Cache Population Strategy

User-requested conditions render first. User input always preempts background cache work. Scheduler tiers should be: Tier 0 foreground request, Tier 1 same-request likely next zooms and pan-adjacent scopes, Tier 2 boundary-focused adaptive refinement, and Tier 3 alternate semantic investigations. If the user selects a new variable, lower tiers immediately yield to the new Tier 0/Tier 1 work.

Cache population should cluster around meaningful structure: boundaries, cusps, overlaps, seams, and condition transitions. Broad homogeneous spaces need fewer samples; borders and ambiguity domains need more. Same-request zoom depth is usually more valuable than speculative alternate variables until the foreground inquiry is served.

Truth and reveal remain separate. The point-level relocated chart engine is the truth source, pixel/subpixel sampling discovers truth, and raindrop/virga are later visualizations of discovery/cache population rather than fake loading animations. Their rhythm may be aesthetic, but scheduler correctness must not depend on animation.

Pre-map idle time during birth-data intake, AI intake, onboarding, or the few seconds before first search may eventually precompute chart-stable or likely first-map scopes. This is an optimization only; it must not assume one immutable exact chart state. Future cache/scheduler semantics must tolerate multiple candidate chart domains and overlap-confidence rendering for uncertain birth data without implementing ambiguity rendering now.

Complexity management should support mute/solo-style exploration without becoming nannying. The product should help users isolate variables, confidence bands, and overlaps, but should not block professional users from inspecting ambiguity when they understand the tradeoff. Overlap-confidence language should communicate uncertainty honestly rather than collapse it to false precision.

Optimization candidates require validation before use: six-house boundary derivation may reduce house-mapping work if shared boundaries safely derive all 12 houses; ASC/DC and MC/IC opposition reuse may reduce angle-sign work if seam/cusp/high-latitude verification passes; aspect-to-angle semantics must not be collapsed, such as treating planet opposite ASC as planet conjunct DC, unless a future doctrine explicitly permits it.

### Phase 2.6 In-Memory Cache Store Scaffold

The Phase 2.6 cache store remains local/in-memory scaffold only. It may store sanitized semantic cache payloads and scaffold metadata, but must not persist renderer output, debug/aura state, account/user data, backend IDs, fetch responses, workers, GeoJSON, canvas pixels, or map layers.

### Phase 2.7 Runtime Orchestration Contract

The Phase 2.7 orchestration layer remains contract-only. It defines foreground/background ownership, cancellation, stale-job handling, and sanitized cache-hydration envelopes without fetch execution, rendering, workers, UI changes, persistent storage, or runtime map wiring.

### Phase 2.8 Mock Runtime Harness

The Phase 2.8 mock runtime harness proves the saved-investigation to cache-key to store to orchestration chain coheres without production runtime wiring. It remains semantic-flow proof only: no fetch, rendering, workers, persistence, map integration, UI integration, or renderer output hydration.

### Phase 2.9 Mock Execution Bridge

The Phase 2.9 execution bridge remains lifecycle-contract only. It simulates job state transitions, foreground ownership, stale propagation, logical preemption, observer-safe progress, and conceptual hydration eligibility without real execution, fetches, workers, rendering, persistence, or map/UI integration.

### Phase 2.10 Observer / Progress Semantics

The Phase 2.10 observer contract defines what future visual layers may safely know about queued, running, partial, hydrated, completed, stale, cancelled, and error states. Observers remain read-only and must not fabricate progress, imply truth before validation, expose runtime internals, or control scheduler/execution behavior.

### Phase 2.11 Execution Policy Semantics

The Phase 2.11 execution policy remains contract-only. It defines foreground guarantees, concurrency budgets, throttling, cancellation propagation, hydration gates, readiness distinctions, observer cadence, and speculative work limits without executing jobs, fetching, rendering, interpreting astrology, or implementing AI/intake.

### Phase 2.12 Dev Runtime Bridge

The Phase 2.12 bridge is dev/smoke-only metadata plumbing. It proves the committed semantic/cache/orchestration/lifecycle/observer/policy chain can run in a browser context without fetches, workers, rendering, DOM or map writes, persistence, production feature flags, or renderer takeover.

### Phase 2.13 Dev Execution Runtime

The Phase 2.13 runtime remains dev/smoke-only and single-request. It may simulate one controlled queued-to-running-to-completed metadata lifecycle and write sanitized metadata into the in-memory cache store, but must not fetch, render, hydrate renderer output, mutate map state, start workers, persist, or execute speculative/background work.

Professional mode:

- Non-AI professional mode should remain fully usable.
- AI support should be optional, not mandatory.
- Professionals may prefer raw/dumb mode.
- The app should respect users who know what they are doing.

Uncertain birth time:

- Natural-language handling comes later with AI.
- Examples: "early morning", "between 7 and 7:30", or "around sunrise".
- Uncertainty should trigger appropriate warnings and workflows, not false precision.

## 9. AI Strategy Roadmap

AI comes after the non-AI professional core is strong.

First likely AI layer:

- Professional assistant mode.
- Infer what a client is asking for.
- Suggest alternative placements when ideal combinations are impossible.
- Compare chosen cities intelligently.
- Support constrained comparisons, such as college towns, job options, or family constraints.
- Support open "blue ocean" exploration.

Lay-user intake comes later:

- Current location
- Birth location
- Desired change
- Purpose of relocation
- Relationship, career, spiritual, and lifestyle priorities
- Language, culture, weather, and practical preferences
- Dream cities

Interpretive philosophy:

- AI should optimize for native intention, not abstract benefic/malefic scoring only.
- Dignity theory matters, but lived context matters more.
- Sun or Saturn out of 12th may be useful even if dignity theory is not directly involved.
- Jupiter in 10th may be desirable despite technical weakness.
- If Venus 7th is impossible, alternatives such as Venus sextile DC may be useful.

The AI should support astrologers and informed users, not flatten astrology into generic scoring.

## 10. Education / Ecosystem Roadmap

Education can become part of the product ecosystem:

- Mini-courses to teach relocation astrology.
- Help lay users ask better questions.
- Professional certification or training possibility.
- Eventual marketplace/referral ecosystem for trained astrologers.

Principle:

- AI can support professionals but should not replace them.
- Education should raise user sophistication rather than hiding astrology behind a black box.

## 11. Travel / Road Trip Mode Roadmap

Travel mode is a later-stage feature, not MVP.

Possible capabilities:

- GPS/location-aware relocation changes.
- Notify when planets change relocated houses.
- Notify when the user enters aspect-to-angle zones.
- Support road trips and flights.
- Offline/airplane support where routes or coordinates are downloaded before departure.
- GPS may work without cellular or Wi-Fi.

Use cases:

- Road trips through changing relocated chart regions.
- Flight path awareness.
- Planning retreats, tours, moves, or temporary stays.

This should come after the core map/search/professional workflow is stable.

## 12. Polar / Latitude Cap Strategy

Do not remove the `+/-65` cap yet.

Current position:

- Truth-grid may allow reevaluation of the cap.
- A polar stress suite should be created before changing cap behavior.
- Advanced-user override may be useful later.
- Warnings are preferred over nanny limitations where mathematically honest.
- Compare against astro.com and extreme northern/southern examples later.

Risks:

- Placidus behavior can become unstable or undefined at high latitudes.
- Regions can compress sharply near polar areas.
- Users may misread rendered regions as more mathematically certain than they are.

Recommendation:

- Keep cap for MVP.
- Add optional professional override only after stress testing.
- Clearly label any above-cap output as advanced/experimental if introduced.

## 13. Stress Testing Strategy

Stress testing should happen throughout development, not only near release.

Create and preserve fixtures for:

- Baseline
- High north
- High south
- Antimeridian
- Solstice/equinox
- Cusp-heavy
- Polar/above cap
- Multi-condition overlap
- Exclusion/NOT
- Dense city regions
- Mobile/zoomed-in UX

Proof-of-work matters:

- Preserve validation records.
- Preserve screenshots when useful.
- Preserve validation narratives explaining what was tested and why.
- Keep enough artifacts to reconstruct why a design is trusted.

## 14. Development Discipline

Implementation should be chunked into manageable steps.

Rules of motion:

- Each chunk should have validation.
- Avoid huge rewrites.
- Keep the current working milestone stable.
- Preserve backups before major changes.
- Use archive/junk drawer folders for experiments.
- Keep the repo clean.
- Distinguish valuable archaeology from disposable browser junk.
- Do not mix risky math changes with UI redesign.
- Do not make `truth_grid` default until broader QA says it is ready.

The product should advance through stable, validated layers rather than big speculative jumps.

## 15. Suggested Immediate Next Chunks

Recommended order:

1. Commit/backup current Angle-in-Sign milestone if not already committed.
2. Fix dropdown auto-advance and remove/hide the current user-facing status box.
3. Create overlay color/overlap design prototype.
4. Add aspect aura prototype for centerlines.
5. Improve city search/disambiguation plan.
6. Add `DC`/`IC` to Angle-in-Sign.
7. Broaden stress-test fixture suite.
8. Begin thoughtful UX layout exploration, but no major drawer redesign yet.

Near-term bias:

- Stabilize and commit working feature chunks.
- Improve UX pain without redesigning the entire app.
- Keep map-first exploration at the center.
