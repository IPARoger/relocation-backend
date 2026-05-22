# Screen-space adaptive refinement proof

This is the corrected optimisation target.

We are **not** searching for a globally acceptable replacement for 1px
truth. A global `block_px=2` or `block_px=4` is the wrong architecture:
it lowers fidelity everywhere, including narrow centerlines and overlap
boundaries where precision matters most.

The right target is:

- sample sparsely over the full visible screen,
- stop almost immediately in stable empty regions,
- preserve/coarsen stable filled interiors,
- refine only around occupied areas, transitions, centerlines, and overlap
  boundaries,
- continue locally down toward 1px only where uncertainty remains.

This script proves that architecture against full 1px screen-space truth.
No astrology math changed. No smoothing. No interpolation. No aura.

## Output

- Script: `scripts/capture_screen_pixel_adaptive_refinement.py`
- Screenshot folder: `validation/screenshots/screen_pixel_adaptive_refinement/`
- Manifest: `validation/screenshots/screen_pixel_adaptive_refinement/manifest.json`
- Progression sheets: one per case, e.g.
  `validation/screenshots/screen_pixel_adaptive_refinement/triple_overlap_americas/progression_sheet.png`

Each progression sheet shows:

1. full 1px reference,
2. sparse 16px exploratory pass,
3. 8px regional concentration,
4. 4px boundary concentration,
5. 2px near-final convergence,
6. 1px final local convergence.

## Algorithm tested

This is intentionally simple and conservative.

1. Build a Leaflet-matched screen projection for the current viewport.
2. Compute the full 1px reference by classifying every screen pixel.
3. Start adaptive refinement with 16px screen tiles.
4. For each tile, classify a small probe lattice.
5. If the tile is stable empty, stop sampling there.
6. If the tile is stable filled, accept the tile as filled and stop.
7. If the tile is mixed, occupied, or adjacent to occupancy, subdivide.
8. Repeat at 8px, 4px, 2px, then 1px only for remaining local uncertainty.

The key governance detail: the final phase does **not** run 1px globally.
It only runs 1px inside the refined local candidate set.

## Results

All tests used a 960 × 600 viewport: 576,000 pixels for full 1px truth.

| case | full 1px samples | adaptive samples | reduction | full 1px time | adaptive classify time | speedup | final overlay XOR vs 1px |
|---|---:|---:|---:|---:|---:|---:|---:|
| Sun 1st, world | 576,000 | 70,329 | 87.8% | 4.89s | 0.58s | 8.5× | 0.140% |
| Sun 1st, Americas | 576,000 | 72,868 | 87.3% | 5.06s | 0.66s | 7.7× | 0.125% |
| Saturn ☌ MC, orb 0.5, Pacific | 576,000 | 50,580 | 91.2% | 5.41s | 0.47s | 11.5× | 0.000% |
| Saturn ☌ MC, orb 1, Pacific | 576,000 | 53,130 | 90.8% | 5.38s | 0.49s | 11.1× | 0.000% |
| Saturn ☌ ASC, orb 1, world | 576,000 | 56,168 | 90.2% | 4.98s | 0.48s | 10.4× | 0.000% |
| Triple overlap, Americas | 576,000 | 109,423 | 81.0% | 5.03s | 1.00s | 5.0× | 0.018% |

The centerline cases are the clearest validation of the architecture:
they require local 1px truth, but only along a narrow corridor. The
adaptive algorithm classifies roughly 9% of the viewport and converges
to exact overlay equivalence against the full 1px reference.

The triple-overlap case is harder because the occupied and boundary
surface is much larger. It still saves 81% of classifications and ends
with only 0.018% overlay XOR versus full 1px truth.

## Phase behavior

The phase progression confirms the expected computational shape.

### Narrow centerlines

For `Saturn ☌ MC, orb 0.5`:

| phase | tile size | cumulative samples | overlay XOR vs 1px |
|---:|---:|---:|---:|
| 1 | 16px | 36,480 | 100.00% |
| 2 | 8px | 41,880 | 100.00% |
| 3 | 4px | 46,380 | 100.00% |
| 4 | 2px | 50,580 | 50.00% |
| 5 | local 1px | 50,580 | 0.00% |

This looks strange numerically until viewed as architecture: coarse
passes discover the corridor and decide where to refine, but they cannot
faithfully paint a sub-pixel/narrow centerline. That is fine. The goal
is not to render the early pass as final. The goal is to spend the 1px
work only where the corridor exists.

### Polygon fields

For `Sun in 1st, world`:

| phase | tile size | cumulative samples | overlay XOR vs 1px |
|---:|---:|---:|---:|
| 1 | 16px | 36,480 | 25.01% |
| 2 | 8px | 49,920 | 10.68% |
| 3 | 4px | 61,740 | 5.85% |
| 4 | 2px | 70,329 | 1.85% |
| 5 | local 1px | 70,329 | 0.14% |

The interior becomes stable quickly; the remaining difference collapses
around boundary pixels.

### Multi-condition overlap

For `Sun 1st + ASC Capricorn + MC Libra`:

| phase | tile size | cumulative samples | overlay XOR vs 1px |
|---:|---:|---:|---:|
| 1 | 16px | 36,480 | 46.53% |
| 2 | 8px | 61,080 | 23.10% |
| 3 | 4px | 87,800 | 11.28% |
| 4 | 2px | 109,423 | 3.85% |
| 5 | local 1px | 109,423 | 0.018% |

Overlap boundaries are the expensive part. This confirms the product
intuition: the more semantic regions overlap, the more local refinement
is required, but still nowhere near full-screen 1px brute force.

## Recommendation

Use adaptive screen-space refinement as the production architecture.

| role | recommendation |
|---|---|
| Initial exploratory pass | 16px tiles with multi-point probe lattice |
| Occupancy expansion | refine occupied/mixed tiles plus a one-tile halo |
| Polygon interiors | stop early once tile probes are stable filled |
| Empty regions | stop immediately once tile probes are stable empty |
| Boundaries and overlaps | refine through 8px → 4px → 2px → local 1px |
| Narrow centerlines | always allow local 1px convergence along the corridor |
| Validation/inspection mode | full 1px screen-space truth remains the control specimen |

The conservative production target is:

- Start at 16px.
- Refine all mixed / occupied / adjacent tiles.
- Use 2px as the normal near-final visual pass.
- Use local 1px only where 2px still differs or where condition geometry
  is intrinsically narrow: low-orb aspect-to-angle, overlap boundaries,
  sharp sign-angle edges, or highly compressed high-latitude corridors.

This preserves maximal fidelity where needed and eliminates wasted
sampling elsewhere.

## Edge cases

- **Very narrow orb centerlines:** coarse phases may visually miss the
  final line or show 100% overlay XOR until local 1px runs. This is
  expected. The early phases are discovery/refinement control, not the
  final product.
- **Large triple-overlap surfaces:** require more refinement than single
  condition fields because overlap colors create more boundaries.
- **Stable empty viewports:** should terminate almost immediately after
  sparse probing.
- **World wrap / dateline copies:** this script uses screen-space
  projection for the actual visible viewport, so the same adaptive logic
  applies to whatever the user sees. Production should continue to treat
  the screen as the source of truth.

## Architectural conclusion

The raindrop model is computational first.

It should not be treated primarily as animation. It is the visible form
of adaptive truth discovery:

1. sparse exploratory probes ask where truth exists,
2. empty areas stop consuming compute,
3. occupied and uncertain areas receive more samples,
4. boundaries and centerlines converge to local 1px truth,
5. the final overlay becomes visually indistinguishable from full 1px
   brute force without paying for full-screen 1px brute force.

This is the correct bridge between the brute-force control specimen and
an interactive production renderer.
