# Phase 2.36f - Truth Dynamic Polygon Renderer

## Purpose

Phase 2.36f proves that truth-derived dynamic side-cap bands can be emitted as real polygon geometry and rendered through the normal Leaflet GeoJSON polygon substrate used by overlays.

This is validation-only. It does not edit production code, `map_CURRENT.html`, backend behavior, scheduler/cache execution, aura color/gradient implementation, rain, virga, product UI, roadmap files, or unrelated files.

## Method

For each sampled point on the solved centerline:

1. compute adjacent house spans with Swiss Ephemeris Placidus houses,
2. compute each side independently with `min(10, adjacent_house_span * 0.30)` when the adjacent span is below 30 degrees,
3. generate left and right polygon boundaries from the evolving widths,
4. emit a GeoJSON `FeatureCollection`,
5. render it with Leaflet `L.geoJSON`.

This replaces constant asymmetry with evolving truth-derived polygon geometry.

## Cases

- MC: `baseline_validated`, Moon square MC, adjacent houses 9/10.
- ASC: `baseline_validated` relocated near Fairbanks, Uranus conjunct ASC, adjacent houses 12/1.

## Governance

No gradients, aura opacity, animation, rain, virga, cache optimization, or production integration were created.
