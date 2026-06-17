# Phase 2.52 - Validation-Only Map + Overlap Sandbox

This phase moves the stabilized transported-material beta renderer onto map-like validation surfaces without production integration. It does not edit `map_CURRENT.html`, add UI controls, build production multi-aspect selection, or deeply optimize aesthetics.

## Cases Rendered

1. Single transported-material aspect band over static map geography.
2. Fixed asymmetry band over map.
3. Dynamic asymmetry band over map.
4. Planet/sign/house-style polygon overlap.
5. Polygon overlap on polygon overlap.
6. Aspect-to-angle band crossing a polygon.
7. Two aspect-to-angle bands crossing each other.
8. Aspect-to-angle band crossing an already-overlapped polygon region.

Forced sandbox geometry is used intentionally so rare chart configurations do not block validation.

## QA Summary

Single-band, fixed-asymmetry, and dynamic-asymmetry panels are acceptable for beta sandbox validation. Labels and coastlines remain broadly readable, though exact ridges can obscure local labels.

Polygon overlap and band-over-polygon cases are mechanically inspectable but need future child-color, opacity, and pane-order design refinement. Two-band crossings and band-over-already-overlapped polygons show that mute/solo or automatic quieting will likely be needed before production multi-aspect workflows.

Overlap problems are mixed: simple cases are mostly aesthetic tuning; dense stack cases become mechanical readability problems because several truth languages compete in the same pixels.

## Recommended Next Step

Keep the next implementation as a standalone validation sandbox. Do not integrate with `map_CURRENT.html` yet. The next map pass should test the same panels at multiple zoom levels with real Leaflet labels and explicit pane ordering.
