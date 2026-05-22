# Leaflet Edge And Wrap Notes

Date: 2026-05-17

## Current Issue Description

Leaflet remains viable for MVP after the truth-grid milestone, but the map can still feel less polished near world edges:

- Gray or blank empty regions can appear near the edge of the constrained world.
- Dragging toward map bounds can expose non-map background.
- `noWrap: true` keeps tile behavior honest but can make the finite world edge feel abrupt.
- Longitude seam behavior is now visually coherent for overlays, but the base map edge can still feel mechanically clipped.
- Empty background around the map can make the app feel cheaper than the underlying astrology deserves.

These are visual polish issues, not current evidence that Leaflet is mathematically blocking the product.

## Lightweight Fixes To Evaluate

### Map Background Color

- Set a deliberate map/container background color instead of default gray.
- Choose a restrained ocean-like or paper-like background compatible with the tile theme.
- Low risk and likely worth doing early.

### Tile Wrapping / `noWrap`

- Current tile layer uses `noWrap: true`.
- Allowing tile wrap could make horizontal dragging feel more continuous.
- Risk: visual wrapped tiles may imply overlays also repeat unless overlay behavior is carefully handled.
- Recommendation: test cautiously; keep overlay truth/display separation explicit.

### `worldCopyJump`

- Leaflet `worldCopyJump` can keep the map centered by jumping between wrapped world copies.
- May improve panning continuity if tile wrapping is enabled.
- Risk: can be confusing with no-wrap overlays or fixed antimeridian behavior.
- Recommendation: prototype only after confirming tile wrapping behavior with current overlay layers.

### Max Bounds / Viscosity

- Current max bounds protect against dragging too far into empty space.
- Tuning max-bound viscosity may reduce edge exposure.
- This is likely safer than enabling full wrap immediately.

### Alternate Tile Themes

Evaluate restrained tile themes that keep labels readable beneath overlays:

- Light, low-contrast basemap.
- Slightly desaturated geography.
- Good city/country label readability.
- Minimal visual competition with overlays.

Avoid themes that are too dark, too saturated, or too decorative until the overlay color system is settled.

## Migration Considerations

Do not migrate now.

Leaflet is currently acceptable because:

- Truth-grid fixed the major false seam/sliver problem.
- Overlay semantics are now separated from display artifacts.
- MVP layer counts are still manageable.
- Existing city/popup/control behavior is easy to iterate.

Consider MapLibre/Mapbox later if concrete blockers appear:

- Need high-performance vector styling.
- Need many layered interactive overlays.
- Need smoother wrapped-world rendering with custom vector picking.
- Need denser, smarter city rendering at scale.

Google Maps remains less attractive for this app's boutique/custom feel and overlay control, unless city/place search becomes the overriding need.

## Recommendation

Stay on Leaflet for MVP.

Near-term polish order:

1. Set deliberate map/background styling so edge exposure does not feel like default gray.
2. Tune max bounds / edge behavior before enabling world copies.
3. Prototype wrapped tiles separately from production overlays.
4. Reassess only if Leaflet creates concrete blockers after overlay color/aura work.

