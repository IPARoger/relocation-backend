# Polygon Reveal — Truth-Target & Density Pass v1

> **STATUS: SUPERSEDED** (2026-05-21) — preserved as archaeology.
>
> **Why superseded:** Topology-via-reveal was replaced by brute-force +
> adaptive screen-space refinement. Polygons *emerge* from occupancy, not from
> a separate reveal engine.
>
> **Current doctrine:** `docs/CURRENT_RENDERING_DOCTRINE.md`

**Status:** Visual R&D evidence bundle (post–language reset, post–blob critique).
**Scope:** Establish what the **fully-discovered** topology should look like for one polygon, and only then work backward to the reveal that builds it.
**Sandbox:** `map_SANDBOX_polygon_reveal.html` (no commit, no replacement of `map_CURRENT.html`).

The previous v0 bundle had three honest problems the doctrine flagged:
**too blobby, too sparse, too visibly algorithmic.** Edges were drawn with stroke widths and large match-circles overlapping each other. The polygon was implied by big yellow blobs rather than emerging from occupancy.

This pass corrects the rendering model first and reproduces the reveal on top of it.

---

## 1. Truth-target rendering rules (now enforced)

| Rule | Implementation |
|---|---|
| **Constant probe radius for life** | All probes use `URL_PROBE_RADIUS` (default 1.1 px). There is no `setRadius()` call anywhere after spawn. |
| **No stroke fills** | Every probe class uses `stroke: none`. The polygon never has an outline — only occupancy. |
| **Refinement = more probes, not bigger probes** | Phase 02 & 04 spawn interior probes near each match; phase 03 & 05 spawn boundary probes between match/non-match pairs. Both add to the total, never resize existing. |
| **Organic distribution** | Initial scatter and the "broad" phase use a **jittered-grid sampler**: stratified into `~sqrt(n)` cells, one probe randomly placed within each cell, then shuffled. No visible rows/columns/lattice; no Poisson-disk machinery required. |
| **Six-phase model** | Phases are explicitly named so the capture harness can export each one. |

Six-phase model:

| Phase | Kind | Effect |
|---|---|---|
| `phase_00_initial_sparse` | jittered-grid scatter | Sparse exploratory probes spread evenly across the viewport. |
| `phase_01_broad_cluster` | jittered-grid (denser) | Second scatter pass; broad coverage without re-touching existing points. |
| `phase_02_regional_focus` | interior densification | For each match probe, add `k` jittered neighbours within a wide radius. Fills the cluster interior. |
| `phase_03_boundary_hunt` | midpoint boundary | For each (match, non-match) pair within radius R, spawn a jittered midpoint probe. Locates the transition. |
| `phase_04_dense_fill` | interior densification (tighter) | Same as `regional` but at half the radius and more neighbours per match. |
| `phase_05_final_topology` | midpoint boundary (tighter) | Same as `boundary_hunt` at ~½ the radius. Sharpens the edge. |

---

## 2. Final topology renders — task A

All three targets at **dense** pacing, **Americas** viewport, seed 42, constant 1.1 px probes.

| File | Target | Probes | Matches | Engine calls |
|---|---|---:|---:|---:|
| `final_sun_1st_dense.png` | Sun in 1st | 7,654 | 4,623 | 6 |
| `final_moon_4th_dense.png` | Moon in 4th | 7,396 | 4,406 | 6 |
| `final_mars_2nd_dense.png` | Mars in 2nd | 7,457 | 4,396 | 6 |

What this set establishes:

1. **The macro-topology survives the rendering change.** The Sun-in-1st band still runs through the Americas, the Moon-in-4th band shifts east, the Mars-in-2nd band lives on the right edge of the viewport (entering Africa/Europe). None of these shapes is hand-drawn — they all come from `swe.houses` evaluated at every probe and the probes are placed by stratified random jitter, not by knowing the polygon in advance.
2. **Edges read crisply without ever being stroked.** At ~4–5k matching probes inside a continental-scale polygon, the eye reads a clean band whose edge is the **density falloff**, not a polyline.
3. **The Mars-in-2nd polygon visibly continues off-frame** — refinement only fired on probes inside the viewport. This is honest: the sandbox sampled what was visible, and nothing else.

---

## 3. Phase frame exports for Sun-in-1st — task B

Same chart, same target, same seed, captured at every `stopAtPhase=N` boundary.

| File | Phase | Probes | Matches |
|---|---|---:|---:|
| `phase_00_initial_sparse.png` | scatter | 420 | 63 |
| `phase_01_broad_cluster.png` | broad | 1,120 | 171 |
| `phase_02_regional_focus.png` | regional densification | 1,804 | 710 |
| `phase_03_boundary_hunt.png` | boundary midpoints | 2,854 | 1,349 |
| `phase_04_dense_fill.png` | tighter interior densification | 5,254 | 3,333 |
| `phase_05_final_topology.png` | tighter boundary sharpening | 7,654 | 4,623 |

Per-phase reading order:

- **00 → 01:** A handful of golden matches scattered through a sparse cloud. Reads as "stars in the sky, two have been recognised."
- **01 → 02:** Interior densification doubles the match count without adding boundary probes. The polygon body becomes legible *before* its edges do.
- **02 → 03:** Boundary midpoints fill the band-edge zone. Edges sharpen from "implied" to "drawn-by-density."
- **03 → 04 → 05:** Pure densification. Phase 05 is phase 04 with a tighter boundary radius — the topology is now "filled" in the way the doctrine called for.

This ordering enforces the rule that the polygon **emerges** rather than being drawn. No phase makes geometric assertions ahead of the truth that supports them.

---

## 4. Density experiments — task C

Same Sun-in-1st topology, same chart, same viewport, **probe radius held constant at ≤ 1 px**. Only probe count changes.

| File | Probes | Matches | Effective spacing in band | Reading |
|---|---:|---:|---|---|
| `density_sparse_micro.png` | 1,968 | 1,113 | ~10–14 display px | Polygon implied but not occupied — eye reads "scattered hits in a band." |
| `density_medium_micro.png` | 7,654 | 4,623 | ~4–6 px | Polygon reads as **a continuous region with crisp falloff**. Threshold of "geography" begins here. |
| `density_extreme_micro.png` | 19,183 | 12,186 | ~2–3 px | Polygon reads as **filled**. Edges look like the boundary of a coloured region rather than a cloud of dots. |

The transition between "particles" and "continuous geography" sits between the medium and extreme densities for the Americas viewport at 1480 × 900 device pixels.

**Implication for the doctrine:** continuous-region perception requires ~3 probes per pixel along the polygon edge. For a continental viewport, that's tens of thousands of probes — large but not catastrophic, as the throughput data below shows.

---

## 5. Visual changes test — task D

The previous bundle grew probe radius with refinement (match probes were 3.0 px, non-matches 1.6 px, capped 1.5 px). That made matches feel like overlapping blobs and gave the polygon a false fill.

**This pass uses constant radii throughout.** Searching the sandbox HTML for `setRadius` returns zero hits. The CSS `.probe-*` classes do not change the SVG `r` attribute — they only change `fill` and `fill-opacity`. The dense topology renders show that the polygon is now constituted by **occupancy** alone:

- the polygon **body** is dense gold (because thousands of matches occupy the region);
- the polygon **edge** is crisp (because density falls off sharply at the cusp);
- the polygon **interior anomalies** (the apparent two-band structure of Sun-in-1st) are visible (because dense occupancy makes small gaps legible);
- **non-match probes** at 0.32 opacity sit as the surrounding "explored, did not match" cloud.

No edge anywhere is drawn with a stroke. No probe ever changes size.

---

## 6. Organic distribution test — task E

The initial-scatter phase now uses **jittered-grid sampling** (stratified Latin-hypercube-ish placement, then shuffled). Visual check: `phase_00_initial_sparse.png` shows 420 probes across the Americas viewport with no visible rows, no visible cells, no formalised spacing. The pattern reads "random across the field" without the clumpy Voronoi-cell artefacts that pure uniform random produces.

Refinement phases inherit the same property because:

- `interior_candidates` jitters within `interiorRadiusFactor × spacing` of each match, where `spacing` itself is derived from the *initial* probe count (so the candidate cloud around each match is sized to the initial scatter's natural neighbourhood);
- `boundary` midpoints are jittered by `radius × jitterFrac` so the midpoint chain doesn't read as a line of dots between every match/non-match pair.

I did not implement Poisson-disk rejection sampling because (a) it costs O(n²) without spatial hashing and (b) the jittered-grid approach already passes the "feels organic" reading at 7k probes.

---

## 7. Feasibility — task F: could we just classify every visible pixel?

I measured `/classify-points` throughput directly with `scripts/benchmark_classify_throughput.py` (report at `validation/reports/classify_points_throughput.json`). Numbers below are medians across 3 trials per batch size, on this MacBook (Apple silicon, Python 3.11, `swisseph` via `pyswisseph`):

| Batch size | Median client wall time | Server compute | Throughput (server) | Throughput (client) |
|---:|---:|---:|---:|---:|
| 100 | 5 ms | 2 ms | ~55,000 pts/s | ~19,000 pts/s |
| 500 | 19 ms | 7 ms | ~67,500 pts/s | ~27,000 pts/s |
| 1,000 | 36 ms | 15 ms | ~68,000 pts/s | ~27,800 pts/s |
| 5,000 | 197 ms | 74 ms | ~67,500 pts/s | ~25,400 pts/s |
| 20,000 | 745 ms | 315 ms | ~63,500 pts/s | ~26,900 pts/s |
| 50,000 | 1.89 s | 0.76 s | **~65,400 pts/s** | **~26,400 pts/s** |

Server-side `/classify-points` sustains ~65,000 points per second per single core. The client-observed rate is about 2.5× lower, dominated by JSON serialisation + HTTP framing of the input array.

### What that means for "full pixel solve" scenarios

| Scenario | Points | Single-core server | 8-core optimistic |
|---|---:|---:|---:|
| World @ 2.0° grid (90 × 180) | 11,700 | 0.18 s | 0.03 s |
| World @ 1.0° grid | 46,800 | 0.72 s | 0.12 s |
| **World @ 0.5° grid** | **187,200** | **2.86 s** | **0.48 s** |
| Continent @ 1.0° grid | 7,200 | 0.11 s | 0.02 s |
| Continent @ 0.5° grid | 28,800 | 0.44 s | 0.07 s |
| Continent @ 0.25° grid | 115,200 | 1.76 s | 0.29 s |
| Continent @ 0.1° grid | 720,000 | 11.0 s | 1.84 s |
| **1480 × 900 viewport @ 1 sample / 4 display px** | **83,250** | **1.27 s** | **0.21 s** |
| 1480 × 900 viewport @ 1 sample / display pixel | 1,332,000 | 20.4 s | 3.40 s |

### Memory

A single probe in the in-page sandbox carries an SVG `<circle>` (~500 B DOM) + its JS record (~300 B incl. all-planet house map). At 50,000 probes that's ~40 MB browser-side, comfortable; at 1,000,000 probes you'd want a `<canvas>` overlay. Server-side, the response for 50,000 points is ~7 MB JSON, ~700 KB gzipped — fine.

### Conclusion to the feasibility question

> *Could we theoretically classify every visible display pixel at once on a modern machine?*

**Yes — for any practical sampling resolution.** The honest answer is:

- **Truly every screen pixel (1480 × 900 = 1.33 M)**: not interactive single-core (20 s), but achievable in ~3.4 s on 8 cores via multiprocessing. Borderline for "feels instant"; fine for "feels considered."
- **1 sample per 4 display pixels (≈ 83 k)**: 1.3 s single-core, 0.2 s on 8 cores. Comfortably interactive.
- **World at 0.5° grid (≈ 187 k)**: 2.9 s single core, 0.5 s on 8 cores. Also interactive.

This **inverts the design assumption** that drove the previous reveal sandbox. We do not need progressive reveal to drive the solve — we can do a **full instant solve at coarse-to-medium resolution** and then layer reveal on top for emotional pacing.

Suggested next architecture (not implemented in this pass):

1. On Find regions, kick off a one-shot solve at the smallest of {viewport @ 0.25° grid, 100,000 points}. Budget < 2 s on 8 cores.
2. While that returns, render a sparse jittered scatter (~200 probes) so the user sees something immediate.
3. When the full solve returns, the truth is **already in cache**. The reveal becomes a pure pacing decision over already-known data, not a discovery process under uncertainty.
4. Boundary refinement can still spawn extra probes at finer-than-grid resolution where the user's eye lands, but it is no longer load-bearing for correctness.

This is closer to the doctrine's stated preference ("the world is already defined; the engine is *not* inventing truth") than the current discovery-driven reveal, where the engine pretends not to know what the sandbox in fact already knows after one batch call.

---

## 8. Honest self-critique

Where I think this pass succeeds:

- The tiny-constant-radius rendering eliminates the blob look entirely. Compare `density_extreme_micro.png` to anything in the v0 bundle — the new image reads as continuous geography, the old as overlapping circles.
- The jittered-grid sampler removes the "obvious random" feeling at sparse densities. Phase 00 looks like scattered points, not like sample positions.
- The six-phase model gives the reveal a legible narrative ("scatter → broad → cluster → boundary → fill → topology") without inventing a single dot.

Where it does not yet succeed:

- **Phase 03 (boundary_hunt) is still visibly algorithmic** when you stare at it. The boundary probes form a chain along the previous-phase edge. The jitter helps but does not hide the algorithm. A possible fix is to spawn boundary probes in a **shell** around the match cluster rather than only at midpoints to non-matches, which would produce a softer boundary cloud. Not done here.
- **Mars-in-2nd is visibly cropped** at the viewport edge. This is honest about what was sampled, but visually it reads as "the polygon stops there," which it doesn't. A possible fix is to sample slightly beyond the visible bounds; a doctrinal fix is to keep the cropping honest and label it.
- **Sparse_micro is a weaker frame than the spec suggests.** I dialed it to 0.6× density on bloom pacing; in practice the result still has ~2,000 probes which is not very sparse. A truer sparse_micro would be ~500 probes total. I kept the current setting because anything sparser stops communicating the polygon shape at all — but the experiment would be more revealing at the lower end.
- **The cache-from-previous-target ghost cluster identified in v0 still exists**; I did not address it in this pass because the task was the final-topology language, not the cache UX. It remains an open item.

Where I'm flagging AI over-generosity risk:

- The phrase "crisp edges from density alone" in this narrative is technically accurate but selectively framed. The crispness in `density_extreme_micro.png` is partly because at 0.85 px radius the dots themselves are small enough to look like rasterised pixels, which the eye reads as anti-aliased fill. A skeptical reviewer could legitimately argue that at radius < 1 device pixel we're crossing from "occupancy" into "subpixel rendering" — i.e., the renderer is doing the smoothing the doctrine forbade. The dense (1.1 px) version is the cleaner doctrinal claim; the extreme micro is more of a "what happens past the doctrine" experiment than a target.
- I claim the feasibility numbers make progressive reveal architecturally optional. That's true for single-overlay queries at sensible resolutions. It is **not** true for a multi-overlay product that wants all 12 houses × N planets × multiple zoom levels resident in cache. The feasibility argument needs to be re-run before committing to "instant full solve" as a product architecture.

---

## 9. Files in this evidence bundle

```
validation/screenshots/polygon_reveal_topology/
├── manifest.json
├── final_sun_1st_dense.png
├── final_moon_4th_dense.png
├── final_mars_2nd_dense.png
├── phase_00_initial_sparse.png
├── phase_01_broad_cluster.png
├── phase_02_regional_focus.png
├── phase_03_boundary_hunt.png
├── phase_04_dense_fill.png
├── phase_05_final_topology.png
├── density_sparse_micro.png
├── density_medium_micro.png
└── density_extreme_micro.png

validation/reports/classify_points_throughput.json
```

Source files touched (no production paths altered):

```
map_SANDBOX_polygon_reveal.html                       (constant-radius probes; jittered-grid sampler; 6-phase model)
scripts/capture_polygon_topology_targets.py           (new)
scripts/benchmark_classify_throughput.py              (new)
validation/narratives/polygon_reveal_topology_target_v1.md  (this file)
```

No commits, no replacement of `map_CURRENT.html`, no changes to existing rendering paths or production routes.
