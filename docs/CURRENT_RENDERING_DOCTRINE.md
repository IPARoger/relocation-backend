# Current Rendering Doctrine — Summary

> **Status:** Canonical orientation page (fast to read).
> **Authority:** `docs/relocation_map_architecture.md` wins on conflict.
> **Adopted:** 2026-05-21.

This page is the short “where we are now” summary. Older documents that
describe geographic-grid sampling, polygon-reveal pacing, or global
block-size tuning are **preserved as archaeology** but marked
**SUPERSEDED** — see the list at the bottom.

---

## The stack (top to bottom)

| Layer | Role | Status |
|-------|------|--------|
| **Brute force** | Validation wall. Every optimisation must match it cell-for-cell (or pixel-for-pixel on screen). | Canonical control specimen |
| **Screen-space truth** | Production sampling axis for **visible overlays**. Classify what the user actually sees. | Canonical for rendering |
| **Adaptive refinement** | Production rendering substrate. Sparse → dense only where occupancy disagrees. | In use (`edge2_thin2_highlat2_probes` policy) |
| **Targeted escalation** | Extra halo / probes / lat-cap boundary rules **only** at known instability classes. | In use — not global |
| **Phase-2 cache** | User-first, interruptible background warm-up after first paint. | Prototype in `map_SANDBOX_phase2_cache.html` |
| **Aura / raindrops / palette** | Visual language on top of truthful occupancy. | Exploration: `map_SANDBOX_raindrop_aesthetic.html` (see `validation/narratives/raindrop_aesthetic_exploration.md`) |

Implementation must follow `docs/PHASE_C_IMPLEMENTATION_PROTOCOL.md` for reversible commit sequencing, validation gates, and anti-regression workflow.

---

## Non-negotiables

1. **Screen-space truth is canonical** for what appears on the map. Geographic lat/lon grids that paint sparse dots at projected centers are **diagnostic / history only** unless explicitly revived for a narrow comparison.
2. **Adaptive refinement is the production path**, not “find the largest global block size.” Preserve 1px-equivalent truth where needed; stop sampling stable empty regions.
3. **Targeted escalation** handles:
   - viewport edges,
   - high-latitude aspect-to-angle cases,
   - thin aspect lines (orb ≤ 0.5°),
   - lat-cap boundary tiles (`apply_lat_cap=true`).
   It does **not** slow down the whole renderer.
4. **Background cache is user-first and interruptible.** User request always wins; zoom/pan/condition change pauses cache; resume only after immediate render completes. Priority A→H per `docs/relocation_map_architecture.md`. No mouse prediction yet. No half-cached entries.
5. **Brute force remains the validation wall.** No negative-space house inference, no blur, no fake geometry for correctness.

---

## Phase-2 cache (product substrate)

Implemented in **`map_SANDBOX_phase2_cache.html`** (served at `/map_SANDBOX_phase2_cache.html`).

| Rule | Implementation |
|------|----------------|
| First paint = user conditions only | `SCHEDULER.serveUser()` runs before any background job |
| Interrupt on zoom/pan | `map.on("movestart zoomstart")` → `cachePaused=true`, `_cancelAll()`, `AbortController.abort()` |
| Resume after immediate render | `IDLE_GRACE_MS` then `_maybeStartNext()` |
| Priority A→H | Registered in `registerBackgroundJobs()` |
| H transits gated | `deferred_inactive` until `PHASE2.dateModeActive` |
| Budget | `233_118` samples (measured +20% from targeted stress) |
| Smoke test | `scripts/smoke_phase2_cache.py` → `validation/reports/phase2_cache_smoke.json` |

**Not yet wired:** `map_CURRENT.html` product UI, server-side cache persistence, zoom-level reuse of interior occupancy (edge-refinement pipeline).

---

## Evidence bundle (read in this order)

1. `validation/narratives/screen_pixel_truth_diagnosis.md` — why geographic grid failed
2. `validation/narratives/screen_pixel_adaptive_refinement.md` — adaptive proof
3. `validation/narratives/screen_pixel_adaptive_targeted.md` — targeted policy + Svalbard fix
4. `validation/narratives/screen_pixel_dense_residue.md` — dense overlap residue accepted
5. `validation/narratives/phase2_cache_implementation.md` — cache protocol implementation notes
6. `validation/reports/phase2_cache_smoke.json` — automated protocol smoke

---

## Documents marked SUPERSEDED (archaeology preserved)

Do **not** delete these. They record useful failed approaches and pacing experiments.

| Document | Why superseded | Current replacement |
|----------|----------------|---------------------|
| `docs/technical_philosophy/progressive_field_reveal.md` | Reveal/animation drove the solve; wrong priority order | `docs/relocation_map_architecture.md` |
| `docs/technical_philosophy/truth_field_rendering_path.md` | Truth-field / progressive reveal path | Screen-space adaptive + brute-force wall |
| `validation/narratives/polygon_reveal_sandbox_visual_qa.md` | Polygon reveal pacing before brute-force proof | Brute-force + adaptive screen-space |
| `validation/narratives/polygon_reveal_topology_target_v1.md` | Topology target via reveal mechanics | Adaptive refinement toward 1px truth |
| `validation/narratives/progressive_reveal_phase_b.md` | Progressive reveal phase | Adaptive screen-space refinement |
| `validation/narratives/screen_pixel_block_sweep.md` | Global block-size optimisation (wrong target) | `screen_pixel_adaptive_refinement.md` |

**Diagnostic sandboxes (not superseded, but not production):**

- `map_SANDBOX_brute_force.html` — geographic grid control specimen
- `map_SANDBOX_screen_pixel_truth.html` — screen-pixel diagnostic
- `map_SANDBOX_polygon_reveal.html`, `map_SANDBOX_truth_reveal.html` — reveal archaeology
- `map_SANDBOX_raindrop_aesthetic.html` — raindrop/virga aesthetic modes (5), pace/density sweeps

---

## Warnings against backsliding

| Obsolete approach | Why it fails | What to do instead |
|-------------------|--------------|-------------------|
| “Sample a lat/lon grid and paint dots” | Gaps at zoom, dashed centerlines, world-copy mismatch | Screen-space classify + paint blocks |
| “Find the largest global block size” | Loses 1px truth on thin lines / edges | Adaptive refinement with targeted escalation |
| “Reveal pacing discovers geometry” | Geometry is already defined; only sampling density is uncertain | Brute-force proof, then adaptive convergence |
| “Pre-cache everything eagerly” | Blocks user, wastes compute, date-dependent transit pollution | User-first Phase-2 priority queue |
| “Infer houses from negative space” | Not proven safe | Direct classification until validation bundle exists |

---

## Remaining gaps (structural, not aesthetic)

1. **Product wiring** — Phase-2 scheduler not yet integrated into `map_CURRENT.html`.
2. **Server-side cache** — client-only `Map` cache; no shared tile cache across sessions.
3. **Zoom edge-refinement** — interior occupancy reuse on zoom not implemented.
4. **Condition cap** — endpoint max 6 simultaneous conditions; 7–8 needs API + palette work.
5. **Transit date UI** — H-priority jobs need date-mode signals in product UI.
6. **Mouse telemetry cache** — explicitly deferred.

---

## Recommendation

**Ready for aesthetics** (Step 9 in development order). No further structural refinement rule is required before palette/aura work. Implement Phase-2 cache in product UI as parallel substrate work when shipping interactive map.
