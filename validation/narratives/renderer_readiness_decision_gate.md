# Renderer Readiness and Blocker Classification Gate

Phase 1.19. Date: 2026-05-22. Governance pass only — no code or renderer changes.

## Scope

This document is a product-governance review of the rendering substrate against the listed validation narratives. It classifies remaining work as production-blocking, product-trust-protecting, professional-mode, deferrable-research, or aesthetic-future. It does not propose new algorithms, does not switch substrates, does not add aura, and does not run new experiments.

Sources consulted:

- `connected_component_topology_solver.md` (Phase 1.18)
- `wall_guided_topology_extraction.md` (Phase 1.16)
- `full_pixel_wall_anomaly_check.md` (Phase 1.14)
- `multicondition_parity_stress.md` (Phase 1.13)
- `topology_aware_refinement.md` (Phase 1.11)
- `canonical_legacy_parity.md` (Phase 1.12)
- `raindrop_aesthetic_exploration.md` (sandbox aesthetics)

## Anti-Death-Spiral Doctrine

> **Do not continue math/rendering work unless it removes a named production blocker or protects future product trust.**

Intellectual interest is not a justification. Diagnostic completeness is not a justification. Aesthetic ambition is not a justification. Every further renderer/math/architecture commit must reference an item from the blocker tables below or be deferred.

## What Has Been Proven

- Production rendering still uses `legacy_search_regions`. Canonical is observable only with `?canonicalDryRun=1`, `?canonicalVisible=1`, or `?canonicalShowAllSamples=1`. The substrate adapter contract is enforced and renderer-host-owned.
- Pixel-center truth (`/screen-pixel-truth`) plus adaptive 16→1 refinement plus targeted edge/thin/high-lat/lat-cap halo policy (`edge2_thin2_highlat2_probes`) is the proven substrate for both production-grade truth and diagnostic comparison.
- Topology-refined canonical is at-or-better than legacy against the 1 px screen-space wall in 3 of 5 wall cases, tied in the negative control, and worse only at narrow-orb ASC where the refined sample set is sparse (Phase 1.14).
- ASC/MC canonical positive samples form coherent trajectories near the wall-positive locus (Phase 1.16): mean wall distance is sub-pixel in all measured cases, max distance is 1 px or less except in high-latitude ASC (max 1 px to wall, max 2.83 px to legacy).
- The connected-component nearest-neighbor path solver (Phase 1.18) gives meaningful before/after gains on ordering-derived metrics without smoothing or new samples: ASC+house total length 265.453 → 220.328 px and curvature variance 4920.445 → 1831.553; high-lat ASC curvature variance 4018.272 → 713.342; seam Saturn/MC total length 1150.337 → 960 px; seam/cap discontinuities remain 0 across all cases.
- MC is clean across continuity, parity, wall, and topology checks at and away from the seam. The seam-centered Saturn/MC parity regression in Phase 1.13 was traced to legacy line-width representation rather than canonical geometry (Phase 1.14, 1.16).
- Multi-condition house overlap is tractable: refined overlap 99.129% for MC+Saturn-10th and refined overlap 77.278% for triple house overlap (Phase 1.13).
- All three smoke gates pass: `smoke_map_current.py`, `smoke_substrate_adapter.py`, `smoke_phase2_cache.py`.
- Phase-2 cache protocol is documented and prototyped; cache window budget is consistent with the 5 s reveal pace from the raindrop aesthetic sandbox.
- Raindrop sandbox produced an aesthetic recommendation (`bacteria` + harmonic opacity, 5 s pace, `readable` density) that is decoupled from truth math; aesthetics is a separable layer.

## What Is Still Uncertain

- Refined parity for narrow-orb ASC and ASC + house overlap plateaus at 23–68% refined overlap and shows false-negative-dominated disagreement (Phase 1.13). Cause is sampling density and one-level refinement, not astrology math.
- Cap-adjacent disagreement appears in coarse comparison even when refined cap disagreement is zero (Phase 1.12, 1.14). The lat-cap boundary refinement protects the worst case but the perceived behavior near ±65° is not yet product-defined.
- The path solver is greedy nearest-neighbor. It is enough for diagnostic confidence but does not produce stable component IDs across zoom/pan and does not handle branching overlapping conditions (Phase 1.18).
- Six-condition aesthetic readability is currently capped at ~3 visible overlays on dense density (raindrop sandbox). API supports 6 but mush appears above 3 under dense settings.

## What Is Production-Blocking

The renderer is **not blocking production launch** for a single-condition or 2–3 condition relocation map on `legacy_search_regions`. Production blockers below are scoped to the canonical substrate becoming default; they do **not** block accounts, chart library, favorites, or client sharing.

| # | Blocker | Why |
|---|---------|-----|
| P1 | None for current legacy-default launch | Legacy substrate is stable; smoke gates pass; popup math is unchanged. |
| P2 | (Canonical-default migration only) Stable component IDs across zoom/pan | Without this, debug overlays will visibly shimmer between zoom levels and break trust. |
| P3 | (Canonical-default migration only) Narrow-orb ASC false-negative bound | Refined parity must reach a defined floor before canonical replaces legacy for thin loci. |

Only P1 is relevant for MVP. P2/P3 are pre-requisites for the future canonical-default switch, not for shipping.

## What Protects Product Trust

These are not blockers, but skipping them risks user trust erosion later.

| # | Trust item | Why |
|---|------------|-----|
| T1 | Cap policy + on-screen lat-cap label | Already implemented on `map_CURRENT.html`. Must remain in MVP. |
| T2 | Explicit “experimental mode” gate for narrow-orb (< 0.5°) aspects | User should know thin loci are advanced-mode and may show stricter resolution behavior. |
| T3 | Phase-2 cache user-first protocol | Background warm-up must remain interruptible; cache must never block first paint. |
| T4 | One source of truth doctrine (`/screen-pixel-truth` + adaptive policy) | Already documented in `docs/relocation_map_architecture.md` and `docs/CURRENT_RENDERING_DOCTRINE.md`. |

## Classification Table

| ID | Item | Class | Rationale |
|----|------|-------|-----------|
| C1 | Connected-component path solver | **D — Deferrable research** | Phase 1.18 is sufficient for current debug confidence. Future graph/global path solver only if visible line/aura phase needs stable component IDs. |
| C2 | Narrow-orb ASC refinement beyond one level | **C — Professional/experimental mode** | Already explainable as a sampling plateau. Gate behind expert mode rather than block MVP. |
| C3 | High-latitude ASC second-level refinement | **C — Professional/experimental mode** | Wall comparison shows canonical closer than legacy. Acceptable with cap policy + advanced-mode disclosure. |
| C4 | Seam-centered MC representation tolerance | **B — Product-trust** | Root cause classified (legacy line width). Document the rule; do not re-investigate. |
| C5 | Cap-adjacent coarse disagreement | **B — Product-trust** | Acceptable with explicit cap label/policy already shipped. |
| C6 | Canonical substrate becomes default | **D — Deferrable research** | Not required for MVP; only worth doing when P2 + P3 are resolved. |
| C7 | Aura / raindrop / virga / harmonic opacity | **E — Aesthetic/future** | Sandbox proven, recommendation captured. Build only after MVP scaffolding. |
| C8 | Six-condition readability tuning | **E — Aesthetic/future** | Visual cap of 3 today; product can ship 1–3 condition mainline first. |
| C9 | Popup truth integration on canonical pixels | **D — Deferrable research** | Popups still use legacy substrate, which is correct for production today. |
| C10 | Phase-2 cache wired into `map_CURRENT.html` | **B — Product-trust** | Doctrine and prototype exist. Wire-in is product-trust work, not blocker. Schedule after accounts/chart library if not done sooner. |
| C11 | Smoke suite breadth (current 3 scripts) | **A — Production-blocker for regressions** | Keep green during every change. Failure of any smoke is a production blocker. |
| C12 | Aesthetic exploration recommendation | **E — Aesthetic/future** | Park; revisit during perceptual phase. |

Legend: A = production-blocking, B = product-trust, C = professional/experimental mode, D = deferrable research, E = aesthetic/future.

## Specific Answers To Required Questions

- **Is more topology work required before production migration?** No. The legacy substrate is the current production. Canonical migration is not in MVP scope. The connected-component solver is sufficient evidence to stop topology investment until accounts/chart library/MVP scaffolding lands.
- **Is connected-component topology strong enough for a debug-gated canonical renderer?** Yes for debug-only visible line experiments. No for a production-default canonical renderer until stable component IDs across zoom/pan are demonstrated.
- **Is ASC/narrow-orb still a production blocker or an advanced-mode refinement?** Advanced-mode refinement. Pixel-overlap undercounting on thin loci is now understood; current canonical positives are coherent and within 1 px of the wall. Gate narrow-orb behind an experimental flag rather than blocking shipment.
- **Are cap/high-latitude issues blocking mainstream release if default cap/warning policy exists?** No. The product already exposes a lat-cap label and the targeted refinement policy protects the lat-cap boundary. Mainstream release can ship with the existing policy.
- **Is raindrop/virga work product-blocking or polish?** Polish. The aesthetic sandbox is decoupled from truth math. Aesthetic finishing belongs after MVP scaffolding and after canonical substrate stability work.
- **What is the minimum renderer state needed before building accounts/chart library/favorites/client sharing?**
  1. `legacy_search_regions` substrate (already shipped).
  2. Phase-2 cache doctrine documented (shipped) and prototype available; production wire-in can lag MVP.
  3. Lat-cap policy + on-screen label (shipped).
  4. Three smoke scripts green (shipped).
  5. Public sharing format for a chart = `chart-profiles` JSON shape + selected viewport + condition slots A–F (already supported by the screen-pixel-truth schema).
  6. Stable URL contract for `?profile=`, `?viewport=`, and condition slots (already supported by smoke harness usage).

## Commercial / Product Implications

- The renderer is **ship-grade for MVP** on legacy substrate. There is no commercial reason to continue topology investment now.
- Accounts, chart library, favorites, and client sharing are unblocked by rendering. Building them earns user-trust signal far faster than another renderer refinement.
- Continuing renderer work in isolation risks an indefinite diagnostic loop with no commercial output. The anti-death-spiral doctrine exists to prevent that.

## Recommended Next Implementation Phase

**Shift to product scaffolding.** The recommended next prompt:

> Phase 2.0 — Account + chart-library scaffolding behind a feature flag. Use the existing `chart-profiles` shape as the persisted unit. Expose a list/save/favorite UI and a shareable URL contract. Do not change the renderer, do not change astrology math, do not touch the smoke suite. Continue to honor lat-cap label, legacy substrate default, and Phase-2 cache doctrine.

If product feedback after Phase 2.0 names a renderer blocker, it returns to this table as an A or B item and the doctrine reopens that lane. Until then, renderer/math/architecture work pauses.

## Readiness Verdict

- MVP-renderer readiness: **READY** on legacy substrate with lat-cap label, Phase-2 cache doctrine, and the three smoke gates.
- Canonical-default readiness: **NOT READY**. P2 (stable component IDs across zoom/pan) and P3 (narrow-orb ASC false-negative bound) are open.
- Aesthetic finishing readiness: **DEFERRED** by doctrine; aesthetic recommendation already captured.

## Remaining Risks (Documented, Not Acted On)

- Visible shimmer if canonical-default substrate is forced today.
- Narrow-orb ASC will look sparse in expert mode without P3.
- Cap-adjacent visual behavior must remain consistent with the on-screen lat-cap label.
- Sharing/chart-library will need to declare condition slot semantics carefully to avoid future regressions when canonical substrate eventually becomes default.

## Decision

Stop renderer/math/architecture investment now. Move to product scaffolding (accounts, chart library, favorites, client sharing). Reopen renderer work only when a named production blocker or a named product-trust risk appears in real user data.
