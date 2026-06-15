# Relocated Truth Field Benchmark

## Purpose

This validation-only benchmark measures Layer 1 relocated truth-field throughput for the existing `baseline_validated` chart. It does not implement production caching, renderer integration, aura styling, rain, virga, scheduler/cache execution, or production behavior.

## Workloads

- A: `swe.houses` only, extracting ASC, MC, cusps, and house spans.
- B: full relocated point payload: ASC, MC, DSC, IC, all cusps, all spans.
- C: derived classifiers from cached point payload: planet-in-house, angle-in-sign, aspect-to-angle signed separation, and dynamic side-cap widths.

## Key Result

Largest measured full-payload sample: `83040` points in `0.713818` seconds.

Projected `83,040` sample full-payload time: `0.714` seconds.

Projected 0.5 degree world-grid full-payload time (`187200` points): `1.609` seconds.

Projected 0.25 degree world-grid full-payload time (`748800` points): `6.437` seconds.

## Cache Window Assessment

- 3 second window plausible for 83,040 samples: `True`
- 10 second window plausible for 83,040 samples: `True`
- 3 second window plausible for 0.5 degree world grid: `True`
- 10 second window plausible for 0.5 degree world grid: `True`

These are in-process timings only and do not include HTTP overhead.

## Governance

No production code or renderer behavior was changed. This is evidence-gathering only.
