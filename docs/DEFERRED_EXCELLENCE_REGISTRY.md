# Deferred Excellence Registry

Date: 2026-05-22. Preservation-of-intent pass. Read-only architectural memory.

## Purpose

This registry captures everything we know we *could* improve in the renderer, architecture, UX, product, and reliability stack — and have intentionally deferred to protect MVP velocity. Its primary purpose is **not** to accumulate shiny feature ideas. Features are comparatively easy to remember because users ask for them, demos expose them, and commercialization pressure keeps them visible.

The primary purpose is preserving hidden robustness and institutional memory: invisible infrastructure improvements, architecture refinements, reliability upgrades, governance ideas, performance optimizations, renderer trust improvements, scaling concerns, cache/system improvements, synchronization concerns, testing discipline, CI/regression infrastructure, security hardening, migration doctrine, topology robustness, AI workflow governance, anti-drift protections, rollback/recovery systems, observability/debugging improvements, backend/data integrity concerns, and anti-fragility ideas.

These are the things founders and AI systems tend to forget because users do not directly see them, they do not demo well, short-term success can mask their absence, and commercial pressure naturally favors visible product work. The registry exists to preserve long-term engineering intent and product trust so temporary compromises do not silently become permanent doctrine.

Short rule: when choosing what to capture here, prefer invisible engineering and infrastructure concerns over visible feature wishes. Feature wishes may be listed when they carry trust, platform, or operational consequences, but the registry's center of gravity is hidden robustness.

This document does not change behavior. It does not implement features, modify the renderer, or alter production. It only preserves architectural intent and the rationale for each deferral.

## Cross-Cutting Doctrine

1. **Anti-death-spiral doctrine (from Phase 1.19):** Do not continue math/rendering work unless it removes a named production blocker or protects future product trust. Items in this registry are evidence of restraint, not a to-do list.
2. **One source of truth:** Production substrate is `legacy_search_regions`; the proven adaptive engine is `/screen-pixel-truth` plus the targeted `edge2_thin2_highlat2_probes` policy. Every deferred item must respect that boundary.
3. **Honest provenance over visual identity:** Aesthetic finishing must come *after* topology is stable. Deferred polish items below are explicitly downstream of topology lock.
4. **Reversibility:** Every deferral here must remain reversible without a database migration. Schema choices (chart-profile shape, `library/library.json` v1, share-URL contract) are designed to outlive the deferrals.

## Status Legend

| Class | Meaning |
|-------|---------|
| MVP blocker | Must land before public launch |
| Trust blocker | Not blocking launch, but skipping erodes long-term trust |
| Polish | Visual/perceptual finishing |
| Experimental/professional | Advanced-mode or expert-only surface |
| Future platform | Belongs to later product phases (accounts/payments/sharing) |

Priorities: `high`, `medium`, `low`. Defaults are aligned with the Phase 1.19 blocker table.

---

## 1. Renderer / Topology Improvements

### 1.1 Stable component IDs across zoom/pan
- **Why it matters:** Without stable IDs, any future canonical-default renderer or visible-line experiment will visibly shimmer between zoom levels and undermine trust.
- **Why deferred:** Phase 1.18 connected-component solver is sufficient for current debug confidence. Stable IDs require either graph signatures or persistent-feature tracking that has no MVP payoff.
- **Class:** Trust blocker (for canonical-default migration). Not MVP blocker.
- **Priority:** Medium. Becomes high if canonical-default is reopened.
- **Risk if ignored:** Future aura/line rendering shimmers; users perceive instability.

### 1.2 Graph / global path solver
- **Why it matters:** Greedy nearest-neighbor handles current diagnostic confidence but cannot represent branching overlapping conditions or score multiple valid topologies.
- **Why deferred:** Connected-component metrics are already meaningful (Phase 1.18). Investment beyond greedy is not warranted until a visible canonical line is on the roadmap.
- **Class:** Experimental/professional.
- **Priority:** Low.
- **Risk if ignored:** Topology metrics underrepresent multi-condition branching geometry.

### 1.3 Canonical-default migration
- **Why it matters:** Canonical is closer to truth than legacy at sub-pixel resolution (Phase 1.14, 1.16).
- **Why deferred:** Two named prerequisites — stable component IDs (1.1) and narrow-orb ASC false-negative bound (1.5).
- **Class:** Future platform.
- **Priority:** Low until prerequisites land.
- **Risk if ignored:** Long-term, legacy linework will visibly diverge from truth in expert/professional mode.

### 1.4 Continuous topology extraction refinement
- **Why it matters:** Topology is the right source for any future line/aura phase rather than raw blocks (Phase 1.16).
- **Why deferred:** Phase 1.17/1.18 are sufficient as diagnostic evidence; further refinement (endpoint-aware path starts, graph scoring) adds no MVP value.
- **Class:** Experimental/professional.
- **Priority:** Medium.
- **Risk if ignored:** Future aura/line work re-derives this from scratch.

### 1.5 Subpixel/edge extraction refinement for narrow-orb ASC
- **Why it matters:** Refined parity for narrow-orb ASC plateaus around 23–68% (Phase 1.13). Cause is sampling density and one-level refinement, not astrology math.
- **Why deferred:** Acceptable behind an experimental-mode flag (Phase 1.19 doctrine). Mainstream charts rarely need < 0.5° orbs.
- **Class:** Experimental/professional.
- **Priority:** Medium (rises to high if canonical-default is opened).
- **Risk if ignored:** Narrow-orb experts mistrust thin-line rendering.

### 1.6 Seam-aware topology continuity
- **Why it matters:** Future canonical line/aura must not falsely bridge across the longitude seam.
- **Why deferred:** Solver already refuses seam jumps in component formation (Phase 1.18). Further seam-aware joining only needed when canonical lines are visible.
- **Class:** Trust blocker (for canonical-default migration).
- **Priority:** Medium.
- **Risk if ignored:** Visible seam artifacts in future canonical line layer.

### 1.7 Signed-distance-field experiments
- **Why it matters:** SDF would enable smooth perceptual rendering without losing truth provenance.
- **Why deferred:** Premature given current truth substrate is screen-pixel-discrete. Topology must lock first.
- **Class:** Experimental/professional.
- **Priority:** Low.
- **Risk if ignored:** None for MVP. Limits long-term aesthetic finishing options.

### 1.8 Adaptive confidence policies
- **Why it matters:** Per-condition or per-region confidence could drive context-aware sampling and rendering.
- **Why deferred:** Current `edge2_thin2_highlat2_probes` policy is already targeted and proven (Phase 1.10/targeted refinement).
- **Class:** Experimental/professional.
- **Priority:** Low.
- **Risk if ignored:** Slightly suboptimal sampling in long tail of edge cases.

### 1.9 Canonical popup truth integration
- **Why it matters:** Popups would always reflect canonical-classified truth instead of legacy point-in-polygon.
- **Why deferred:** Production popup math is already correct against legacy substrate (which is the default). Premature optimization.
- **Class:** Future platform.
- **Priority:** Low.
- **Risk if ignored:** Popup truth and canvas truth diverge after future canonical-default migration.

### 1.10 High-latitude expert mode
- **Why it matters:** High-latitude ASC and lat-cap behavior need explicit product framing for professional users.
- **Why deferred:** Lat-cap label is shipped; targeted refinement protects the worst case (Phase 1.10/targeted). Advanced-mode UX is enough for MVP.
- **Class:** Trust blocker.
- **Priority:** Medium.
- **Risk if ignored:** Professional users find the cap behavior surprising.

### 1.11 Anti-aliasing / perceptual finishing after topology lock
- **Why it matters:** Final aesthetic polish: typography-grade edges, harmonic opacity, restrained color.
- **Why deferred:** Cannot be applied honestly until topology is stable. Doctrine forbids smoothing-before-truth.
- **Class:** Polish.
- **Priority:** Medium (downstream of topology lock).
- **Risk if ignored:** Product looks unfinished against premium aesthetic peers.

---

## 2. Performance / Infrastructure

### 2.1 Reduce browser ↔ API round trips
- **Why it matters:** Adaptive renderer makes many small POSTs; consolidating reduces tail latency.
- **Why deferred:** Phase-1 stress runs are within budget. Wins are micro until topology lock.
- **Class:** Polish.
- **Priority:** Medium.
- **Risk if ignored:** Mobile / low-bandwidth UX degrades.

### 2.2 Production cache integration
- **Why it matters:** Phase-2 cache doctrine is documented and prototyped (`map_SANDBOX_phase2_cache.html`) but not wired into `map_CURRENT.html`.
- **Why deferred:** Doctrine and prototype are stable; wire-in is product-trust work, not MVP-blocking.
- **Class:** Trust blocker.
- **Priority:** Medium. Becomes high after accounts/library land in Phase 2.1+.
- **Risk if ignored:** Repeated viewport requests for the same chart waste latency budget.

### 2.3 Streaming / refinement scheduler
- **Why it matters:** Future renderer could stream refinement updates as they classify, enabling progressive reveal without aesthetic overlay.
- **Why deferred:** Adaptive renderer already converges quickly enough on tested viewports.
- **Class:** Experimental/professional.
- **Priority:** Low.
- **Risk if ignored:** Large viewports / high-density future overlays may feel sluggish.

### 2.4 GPU / canvas optimization
- **Why it matters:** Sample-paint cycles on dense overlays can drop frames on low-end devices.
- **Why deferred:** No measured MVP-blocking frame drop yet.
- **Class:** Polish.
- **Priority:** Low.
- **Risk if ignored:** Mobile and older-laptop UX suffers at high density.

### 2.5 Viewport tile persistence
- **Why it matters:** Server-side tile cache would amortize repeat viewport fetches for popular cities.
- **Why deferred:** No measured pressure yet; introduces cache-invalidation complexity.
- **Class:** Future platform.
- **Priority:** Medium when account-backed library lands.
- **Risk if ignored:** Cost growth at scale.

### 2.6 Precomputed regional caches
- **Why it matters:** Popular travel corridors (US, EU, Pacific Rim) can be precomputed for fast first paint.
- **Why deferred:** Premature without traffic data.
- **Class:** Future platform.
- **Priority:** Low.
- **Risk if ignored:** First-paint latency for popular charts higher than peers.

### 2.7 Mobile optimization
- **Why it matters:** Relocation maps are intrinsically global; mobile pinch/zoom and overlay readability need explicit work.
- **Why deferred:** Desktop MVP first; mobile responsive scaffolding can ride on the library/dashboard Phase.
- **Class:** Trust blocker.
- **Priority:** High once accounts land.
- **Risk if ignored:** Major user segment underserved at launch.

### 2.8 Offline route / travel mode substrate
- **Why it matters:** Travel/transit modes are an explicit roadmap surface (`docs/relocation_app_product_roadmap.md`).
- **Why deferred:** Different math substrate; needs its own scaffolding phase.
- **Class:** Future platform.
- **Priority:** Low until base product validated.
- **Risk if ignored:** Long-term roadmap blocked.

---

## 3. UX / Visual System

### 3.1 Refined virga / reveal pacing
- **Why it matters:** Raindrop sandbox identified `bacteria` clustering + harmonic opacity at 5 s as the preferred direction.
- **Why deferred:** Aesthetic must wait until topology lock (Phase 1.19 doctrine).
- **Class:** Polish.
- **Priority:** Medium.
- **Risk if ignored:** Reveal feels mechanical at launch.

### 3.2 Harmonic opacity polish
- **Why it matters:** Tested in raindrop sandbox; supports accelerated reveal toward exactness.
- **Why deferred:** Same as 3.1 — needs topology lock first.
- **Class:** Polish.
- **Priority:** Medium.
- **Risk if ignored:** Visual hierarchy feels flat.

### 3.3 Typography system
- **Why it matters:** Premium relocation product needs a coherent type voice; current UI uses system fonts.
- **Why deferred:** Below-the-line polish; not MVP-blocking.
- **Class:** Polish.
- **Priority:** Medium.
- **Risk if ignored:** Brand feels generic.

### 3.4 Restrained color doctrine
- **Why it matters:** Six-condition palette currently averages overlap colors; mush appears above 3 conditions on dense density.
- **Why deferred:** Aesthetic finishing is downstream; cap visible overlays at 3 in product copy for MVP.
- **Class:** Polish + trust blocker (against mush).
- **Priority:** Medium.
- **Risk if ignored:** Multi-condition charts look noisy.

### 3.5 Popup polish
- **Why it matters:** Popup is the primary "explain this place" surface.
- **Why deferred:** Current popup is functional; deep polish belongs after canonical popup truth (1.9).
- **Class:** Polish.
- **Priority:** Medium.
- **Risk if ignored:** Popups feel like dev UI.

### 3.6 Transition / cusp grayscale language
- **Why it matters:** Cusps and transitions need a distinct visual language to avoid being misread as occupied area.
- **Why deferred:** Requires topology lock and color doctrine first.
- **Class:** Polish.
- **Priority:** Medium.
- **Risk if ignored:** Users misread transition zones as full effect.

### 3.7 Professional / expert mode separation
- **Why it matters:** Narrow-orb, high-lat, and canonical debug should live in an explicit advanced surface.
- **Why deferred:** Settings stub already includes `experimental_mode_enabled`; surface only matters once advanced features exist.
- **Class:** Future platform.
- **Priority:** Medium.
- **Risk if ignored:** Mainstream UX leaks expert tooling.

### 3.8 Onboarding refinement
- **Why it matters:** First-touch UX defines trust.
- **Why deferred:** Existing `skipOnboarding` flag is sufficient for MVP smoke and demo.
- **Class:** Trust blocker.
- **Priority:** High.
- **Risk if ignored:** Drop-off on first session.

### 3.9 Map readability tuning
- **Why it matters:** Base map labels must remain legible under overlays.
- **Why deferred:** Acceptable on tested tilesets; future tile change will require revisiting.
- **Class:** Polish.
- **Priority:** Medium.
- **Risk if ignored:** Cities/labels disappear behind overlays.

### 3.10 City-label hierarchy
- **Why it matters:** Major-vs-minor city labels need a stable hierarchy to support relocation comparisons.
- **Why deferred:** Geocoder/city identity strategy in `docs/geocoder_and_city_identity_strategy.md` already framed but not implemented.
- **Class:** Future platform.
- **Priority:** Medium.
- **Risk if ignored:** Comparison UX feels random.

### 3.11 Responsive / mobile map ergonomics
- **Why it matters:** Same as 2.7 but framed UX-side: hit targets, sidebar collapse, popup overflow.
- **Why deferred:** Desktop first.
- **Class:** Trust blocker.
- **Priority:** High after MVP.
- **Risk if ignored:** Half the audience cannot use the product.

---

## 4. Product / Platform

### 4.1 Accounts / auth
- **Why it matters:** Required for cloud sync, sharing, payments.
- **Why deferred:** Phase 2.0 ships file-based local persistence behind `RM_PHASE2_LIBRARY` to keep MVP velocity.
- **Class:** Future platform.
- **Priority:** High immediately after Phase 2.1 wire-in.
- **Risk if ignored:** Sharing, payments, and multi-device are all blocked.

### 4.2 Payments / subscriptions
- **Why it matters:** Commercial model.
- **Why deferred:** Premature before accounts.
- **Class:** Future platform.
- **Priority:** Medium.
- **Risk if ignored:** No revenue path.

### 4.3 Chart library
- **Why it matters:** Phase 2.0 scaffolds the basics.
- **Why deferred:** Already partially shipped (Phase 2.0).
- **Class:** Future platform (continuing).
- **Priority:** High.
- **Risk if ignored:** No way to manage multiple charts at scale.

### 4.4 Favorites system
- **Why it matters:** Shipped in Phase 2.0 scaffold; mature treatment (smart lists, sorting, tags) still deferred.
- **Class:** Polish.
- **Priority:** Medium.
- **Risk if ignored:** Power users outgrow the scaffold.

### 4.5 Client sharing / export
- **Why it matters:** Professional astrologers need shareable links and exportable assets.
- **Why deferred:** ACL surface depends on accounts.
- **Class:** Future platform.
- **Priority:** Medium.
- **Risk if ignored:** Professional segment underserved.

### 4.5a Saved-view condition replay
- **Why it matters:** Phase 2.2 map deep links now replay chart and viewport, but the active condition set remains stored as `[]`. Professional share links will eventually need to reopen the exact planet/house/sign/aspect query, not just the camera.
- **Why deferred:** Capturing and replaying UI conditions is separate from viewport replay and would add a second instability source to Phase 2.2. Date: 2026-05-22.
- **Class:** Trust blocker for professional/client sharing. Not an MVP blocker for viewport-only links.
- **Priority:** High for the next saved-view phase.
- **Risk if ignored:** Shared map links restore the place but not the interpretive context, forcing clients or practitioners to manually reconstruct conditions.

### 4.6 Comparison workflows
- **Why it matters:** Relocation is fundamentally a comparison question (current vs candidate cities).
- **Why deferred:** Single-chart MVP first.
- **Class:** Future platform.
- **Priority:** High immediately after library wire-in.
- **Risk if ignored:** Core relocation use-case underserved.

### 4.7 AI interpretation layer
- **Why it matters:** Translate truth fields into language a non-astrologer can act on.
- **Why deferred:** Truth substrate must be stable before any AI interpretation can be honest.
- **Class:** Future platform.
- **Priority:** Medium.
- **Risk if ignored:** Competitors win the interpretation surface.

### 4.8 AI assistant modes / personas
- **Why it matters:** Different audiences (curious / professional / educator) need different voices.
- **Why deferred:** Same as 4.7.
- **Class:** Future platform.
- **Priority:** Low.
- **Risk if ignored:** UX feels one-note.

### 4.9 Notes / workspaces
- **Why it matters:** Users want to annotate cities, charts, comparisons.
- **Why deferred:** Library schema already has `notes` per chart; richer workspaces require accounts.
- **Class:** Future platform.
- **Priority:** Medium.
- **Risk if ignored:** Power users self-host their notes externally.

### 4.10 Professional dashboards
- **Why it matters:** Astrologers serving clients need batch / list / annotated workflows.
- **Why deferred:** Premature without accounts and sharing.
- **Class:** Future platform.
- **Priority:** Medium.
- **Risk if ignored:** Professional revenue path delayed.

### 4.11 Collaboration / share links
- **Why it matters:** Share-link contract is in Phase 2.0; ACL and presence are not.
- **Why deferred:** Needs accounts + payments.
- **Class:** Future platform.
- **Priority:** Medium.
- **Risk if ignored:** Sharing becomes a forwarded URL with no controls.

### 4.12 Educational / certification ecosystem
- **Why it matters:** Astrology is an educational market.
- **Why deferred:** Far downstream of MVP.
- **Class:** Future platform.
- **Priority:** Low.
- **Risk if ignored:** Long-term ecosystem opportunity missed.

---

## 5. Reliability / Governance

### 5.1 Regression dossiers
- **Why it matters:** Per-bug capture of repro, hypothesis, classification, and fix lineage.
- **Why deferred:** Narratives in `validation/narratives/` already serve this informally; formal dossiers add overhead without MVP payoff.
- **Class:** Trust blocker.
- **Priority:** Medium.
- **Risk if ignored:** Tribal knowledge loss across phases.

### 5.2 Golden screenshot suites
- **Why it matters:** Catch visual regressions early.
- **Why deferred:** Validation screenshots exist ad-hoc (`validation/screenshots/*`); golden gating requires careful sample selection.
- **Class:** Trust blocker.
- **Priority:** Medium.
- **Risk if ignored:** Visual regression slips by smoke gates.

### 5.3 Automated topology parity tests
- **Why it matters:** Phase 1.13–1.18 parity diagnostics are run inside the substrate adapter smoke, but not as a dedicated suite.
- **Why deferred:** Coverage is adequate today.
- **Class:** Polish.
- **Priority:** Medium.
- **Risk if ignored:** Future refactor breaks parity silently.

### 5.4 Renderer migration gates
- **Why it matters:** Canonical-default migration needs explicit acceptance gates.
- **Why deferred:** Phase 1.19 named the gates (P2/P3); no migration in flight.
- **Class:** Trust blocker.
- **Priority:** Low until migration is reopened.
- **Risk if ignored:** Migration risks regressions.

### 5.5 Doctrine drift detection
- **Why it matters:** Doctrine docs (`docs/CURRENT_RENDERING_DOCTRINE.md`, `docs/relocation_map_architecture.md`) must stay aligned with code.
- **Why deferred:** Reviewed manually each phase; automation deferred.
- **Class:** Trust blocker.
- **Priority:** Low.
- **Risk if ignored:** Docs become aspirational rather than truthful.

### 5.6 Archaeology preservation
- **Why it matters:** `memory_archaeology_raw/` consolidates prior chats and decisions; preservation policy must remain explicit.
- **Why deferred:** Already documented in `docs/process/archaeology_and_synthesis_workflow.md` and friends.
- **Class:** Trust blocker.
- **Priority:** Medium.
- **Risk if ignored:** Replays of solved problems.

### 5.7 Rollback snapshots
- **Why it matters:** `backups/truth_grid_staged_asc_success_*` snapshots show informal rollback memory; formal versioned snapshots would be safer.
- **Why deferred:** Git history covers this for now.
- **Class:** Polish.
- **Priority:** Low.
- **Risk if ignored:** Hard recoveries take longer than necessary.

### 5.8 Renderer benchmark CI
- **Why it matters:** Performance regressions can slip past correctness gates.
- **Why deferred:** Manual stress runs catch the worst cases (`scripts/capture_screen_pixel_adaptive_*.py`).
- **Class:** Polish.
- **Priority:** Medium.
- **Risk if ignored:** Slow regressions go undetected.

---

## Temporary Compromises Currently Accepted For MVP

These are real compromises, accepted on purpose, with clear off-ramps:

- **Local file persistence for the library scaffold** (Phase 2.0). Off-ramp: account-backed sync in a later phase reads the same `library/library.json` shape.
- **Legacy substrate as production default**. Off-ramp: canonical-default migration once 1.1 and 1.5 land.
- **Single-tenant** persistence and no auth. Off-ramp: accounts/auth phase.
- **Map sidebar UX uses dev-style controls**. Off-ramp: typography + restrained color polish (3.3, 3.4) once topology locks.
- **Narrow-orb (< 0.5°) ASC behind experimental flag**. Off-ramp: 1.5 lands a refined floor.
- **Lat-cap behavior documented by on-screen label only**. Off-ramp: 1.10 high-latitude expert mode.
- **Phase-2 cache doctrine documented but not wired into `map_CURRENT.html`**. Off-ramp: 2.2 production cache integration.
- **Aesthetic raindrop/virga work paused after sandbox**. Off-ramp: 3.1/3.2 polish after topology lock.
- **No mobile-first UX**. Off-ramp: 2.7 / 3.11 after accounts.
- **No formal regression dossiers; we rely on per-phase narratives**. Off-ramp: 5.1 formal dossier template.
- **No golden screenshot CI**. Off-ramp: 5.2 once sample-set design is stable.

## Things Explicitly Rejected Unless Future Evidence Changes

Rejection is not deferral — these are choices we will not casually revisit:

- **Fake blur as a truth substitute.** Blur hides defects, does not reveal them. Rejected unless a future perceptual phase can prove honest provenance.
- **Uncontrolled aura fog.** A dense, soft glow that obscures wall classification was tested and rejected (`docs/overlay_and_aura_visual_strategy.md`, aura prototypes). Future aura must read from locked topology.
- **Excessive simultaneous virga / ghost layers.** Raindrop sandbox: > 3 visible conditions on dense density becomes mush. Cap visible overlays at 3.
- **Gimmick animation.** Aesthetic motion for its own sake. Reveal pace exists to widen the Phase-2 cache window honestly, not to perform.
- **Arbitrary smoothing before topology validation.** Smoothing without topology lock turns artifacts into "design language" and cannot be reasoned about later.
- **Uncontrolled feature sprawl.** Phase 1.19 doctrine: every renderer/math commit must remove a named blocker or protect product trust. Otherwise defer or reject.
- **Replacing the proven adaptive renderer with an untested alternative.** Targeted refinement (`edge2_thin2_highlat2_probes`) and the lat-cap boundary policy are the proven floor.
- **Visual identity with legacy linework instead of truth.** Exact visual identity with legacy was explicitly rejected in Phase 1.12 because it would reward legacy artifacts.

## Items That Probably Should Not Be Deferred

This pass surfaces three items that are flagged as deferred above but are close to "open now" given current product state:

1. **Onboarding refinement (3.8)** — priority `high`. As Phase 2.1 wires the library handoff, the onboarding gap becomes the next visible product-trust risk. Move from deferred to "next-after-2.1" candidate.
2. **Mobile / responsive UX (2.7 + 3.11)** — priority `high` post-MVP. Should not be allowed to slip beyond Phase 2.x without explicit decision.
3. **Production cache integration (2.2)** — priority `medium` but rises fast: with accounts/library coming, repeat-viewport latency becomes visible. Consider wiring Phase-2 cache into `map_CURRENT.html` immediately after Phase 2.1.

All three are still consistent with the anti-death-spiral doctrine because each removes a named product-trust risk rather than chasing intellectual novelty.

## Operating Rules For This Registry

- **Read-only by default.** Items are added or graduated to active work only with explicit phase gating.
- **Graduation criteria.** When a deferred item becomes active, link the phase narrative that reopened it and update its status here.
- **No silent permanence.** If a "temporary compromise" persists across two product phases without explicit decision, surface it for review.
- **No copies.** This file is the single source of truth for deferred excellence; doctrine docs reference it rather than restating items.
- **Hidden robustness first.** Prefer capturing non-demoable engineering memory over visible feature ideas: scaling limits, migration risks, cache invalidation, testing gaps, security hardening, rollback paths, observability, topology trust, and AI/governance drift.
- **Audit for promotion.** Periodically ask whether deferred items have silently become important enough to promote because product usage, revenue exposure, client sharing, or operational risk changed.
- **Beware normalized debt.** Temporary local storage, manual validation, debug-only tooling, unowned scripts, brittle smoke assumptions, missing CI gates, absent rollback, and undocumented migration steps must not become invisible doctrine.

## Maintenance Protocol

- **End-of-phase review required.** This registry must be reviewed at the end of every significant phase, whether or not it changes.
- **Immediate capture.** New deferred hidden work, temporary compromises, rejected approaches, future-platform ideas, architecture debt, reliability gaps, testing/CI gaps, security hardening, observability needs, synchronization concerns, rollback/recovery needs, and governance protections must be added as soon as they are identified, not reconstructed later from memory.
- **Dated status changes.** Promoted, deprioritized, reclassified, or removed items must be dated and explained in the relevant item or section.
- **Explicit no-op justification.** If a phase closes with no registry update, the closeout must state why no new deferred hidden robustness work, promoted work, deprioritized work, rejected work, or normalized temporary compromise was created.
- **Governance protocol.** Follow `docs/AI_WORKFLOW_GOVERNANCE.md` for mandatory closeout checks and the standard future-task prompt footer.

---

End of registry. Next governance review: triggered when Phase 2.1 lands or when any item in section 1.1–1.6 changes class.
