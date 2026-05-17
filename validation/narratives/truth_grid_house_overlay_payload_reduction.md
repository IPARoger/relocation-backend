# Truth-grid House Overlay Payload Reduction

## What This Test Proves

This prototype derives Sun house regions from direct point truth, then merges only adjacent same-house grid cells into larger axis-aligned rectangles. It does not smooth boundaries, infer topology, or cross false cells.

## Fixture

- Fixture: Edge Case - High Northern Birth
- Birth data: `{"birth_year": 1988, "birth_month": 6, "birth_day": 21, "birth_hour_utc": 3.2}`
- Latitude cap: `-65.0` to `65.0`
- Planet: Sun
- Houses benchmarked: all 12; GeoJSON samples preserved for houses 7, 8, and 9.

## Benchmark Summary

| Resolution | Points | Classify | Merge+Validate | Raw All Houses | Merged All Houses | Merged Features |
|---|---:|---:|---:|---:|---:|---:|
| 1.0 deg | 46800 | 0.4492s | 0.589s | 14209035 bytes | 261037 bytes | 916 |
| 0.75 deg | 83040 | 0.6544s | 1.5543s | 26465933 bytes | 361222 bytes | 1221 |
| 0.5 deg | 187200 | 1.6603s | 3.2387s | 58066571 bytes | 557760 bytes | 1932 |

## Validation

- Known false probes are excluded from the wrong houses.
- Interior validation found zero contradictions across merged rectangles.
- Seam behavior remains honest: rectangles are split at the display seam rather than smoothed across it.

## MVP Interpretation

Merged truth-grid rectangles are likely viable for house overlays. They trade smooth visual polish for deterministic truth, small payloads, and predictable rendering. Marching squares can be evaluated later as a visual-polish layer, but should remain truth-validated.
