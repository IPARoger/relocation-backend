# Next Implementation Sequence

Small, **low-risk**, **testable**, **isolated** chunks—ordered by current product priorities. This is **sequencing and planning only**, not a commitment to build everything listed.

**Reference:** `ai_context/current_state.md`, `docs/relocation_app_product_roadmap.md`, `ai_context/open_questions.md`.

---

## Priority band 1 — UX polish (minimal architecture risk)

### Chunk 1.1 — Sidebar density and “debug vs ship” clarity

- **Why:** Prototype sidebar is tall and noisy; professionals need long-session focus (`current_state.md`).
- **Dependencies:** None structural; CSS/layout in `map_CURRENT.html` (or extracted styles later).
- **Validation:** Visual pass; confirm map remains primary; no regression on popup/dropdown behavior.
- **UX risks:** Hiding too much—power users lose discoverability. Mitigation: progressive disclosure, keep debug behind explicit mode.
- **Architecture risks:** Low if changes stay presentational.
- **Do not overengineer:** No new framework, no drawer rewrite here—**incremental compression** only.

### Chunk 1.2 — Popup and typography refinement

- **Why:** Popup is diagnostic truth; typography should match premium, calm instrument tone.
- **Dependencies:** None on backend.
- **Validation:** Side-by-side screenshots; high-north / southern fixtures; dateline popups unchanged logically.
- **UX risks:** Over-styling reduces scan speed for numbers.
- **Architecture risks:** Low.
- **Do not overengineer:** Avoid custom tooltip framework; tune CSS and copy.

### Chunk 1.3 — Native select stability + legend clutter reduction

- **Why:** Dropdown bugs were recurring; legend consumes space (roadmap §4).
- **Dependencies:** Prior click-through / select fixes must remain intact.
- **Validation:** JSON reports pattern already in `validation/reports/`; extend with short checklist.
- **UX risks:** Custom dropdowns too early—**prefer native** until a proven blocker.
- **Architecture risks:** Medium if abandoning native selects without a11y plan.
- **Do not overengineer:** “Legend in control chrome” can be a **small** change before full semantic color system.

---

## Priority band 2 — Validator / stress tooling

### Chunk 2.1 — Fixture manifest + “run these five” script

- **Why:** Institutional repeatability; wrong-file / stale-server class of errors.
- **Dependencies:** Existing validation JSON/Markdown outputs.
- **Validation:** Script exits non-zero on regression; doc lists commands.
- **UX risks:** N/A (developer-facing).
- **Architecture risks:** Low—read-only orchestration.
- **Do not overbuild:** One Makefile or shell script beats a framework.

### Chunk 2.2 — Latitude / polar stress suite expansion

- **Why:** `+/-65` cap and polar policy remain open (`open_questions.md`).
- **Dependencies:** Agreed chart fixtures; maybe `docs/calculation_assumptions.md` later.
- **Validation:** Contradiction counts + narrative per case.
- **UX risks:** Users see confusing caps—needs **copy**, not only math.
- **Architecture risks:** Medium if math changes without documented policy.
- **Do not overengineer:** Add cases before rewriting house engines.

### Chunk 2.3 — Brute-force / truth export hygiene

- **Why:** Separating **math truth** from **renderer truth** (archaeology doctrine).
- **Dependencies:** Existing validator/experiment scripts; workspace policy for big GeoJSON (`workspace_hygiene_and_cleanup.md`).
- **Validation:** Compare exports to app overlays on static fixtures.
- **Architecture risks:** Low if exports stay side tools.
- **Do not overengineer:** CI wiring can wait until fixture stability.

---

## Priority band 3 — Account + birth-data workflows

### Chunk 3.1 — Birth data model (local-only MVP)

- **Why:** Professional tool needs repeatable charts; today may be implicit/single-session.
- **Dependencies:** Product decision on persistence (localStorage vs backend DB)—**decide before coding**.
- **Validation:** Save/load round-trip; timezone edge cases.
- **UX risks:** Intake friction; scary forms.
- **Architecture risks:** **High if scope creep** (auth, sync, multi-device). Start **single-device, explicit save**.
- **Do not overengineer:** No full account system until birth-data UX is proven.

### Chunk 3.2 — Chart list + “open on map”

- **Why:** Comparison workflows (band 6) prerequisites.
- **Dependencies:** Chunk 3.1.
- **Validation:** Two charts, no cross-contamination of API params.
- **UX risks:** Modal proliferation.
- **Architecture risks:** Medium—state management in monolithic HTML.

---

## Priority band 4 — Geocoder / city intelligence

### Chunk 4.1 — Disambiguation UX stub

- **Why:** Global search quality is a core product problem, not polish.
- **Dependencies:** Geocoder provider choice stable enough for MVP.
- **Validation:** Ambiguous city queries; narrative in `validation/narratives/city_search_and_polar_strategy_notes.md`.
- **UX risks:** Confusing labels (astro.com-style cryptic names called out in open questions).
- **Architecture risks:** Medium—API quotas, caching.
- **Do not overengineer:** “Pick one city” flow before ML ranking.

### Chunk 4.2 — Ranking + intent heuristics (later within band)

- **Why:** Population-only ranking fails famous small places.
- **Dependencies:** Telemetry or manual scoring table; ethics of “importance.”
- **Validation:** Curated query list; no silent reorder surprises.
- **Architecture risks:** Data pipeline creep.

---

## Priority band 5 — Aura visualization experiments

### Chunk 5.1 — Read-only aura prototype (frontend-only, one aspect family)

- **Why:** Centerlines are correct but incomplete visually (`overlay_and_aura_visual_strategy.md`).
- **Dependencies:** Stable centerline GeoJSON; performance baseline on low-end machine.
- **Validation:** Visual diff—**centerline must not move**; compare to “thick line” hack.
- **UX risks:** Aura implies false precision or membership.
- **Architecture risks:** Medium—canvas/WebGL later; start with SVG/canvas **experiments off main branch** or feature flag.
- **Do not overengineer:** No orb field computed as new astrology layer on backend until frontend vocabulary settles.

### Chunk 5.2 — Validation-only transported-material map sandbox

- **Why:** Phase 2.47/2.48 validation proved texture-coordinate transport, side-local proportional scaling, and extreme asymmetry behavior in static artifacts; the next question is whether the beta placeholder material survives real map projection, labels, zoom, and Leaflet pane constraints.
- **Dependencies:** Phase 2.47 stabilization recommendation; Phase 2.48 stress-test caveats; locked centerline/boundary geometry from validation fixtures.
- **Validation:** New sandbox artifact only, not `map_CURRENT.html`: one MC and one ASC case, one fixed asymmetry and one dynamic asymmetry, screenshot comparison against the static validation boards, and a narrative explicitly checking label readability, pane ordering, pixel collapse, and no centerline drift.
- **UX risks:** Users may mistake the beta placeholder material for final aesthetic approval. Mitigation: sandbox banner and report must state "beta renderer placeholder, not final visual language."
- **Architecture risks:** Medium if the map sandbox quietly becomes production integration. Keep it behind a standalone validation file with no production imports, no scheduler/cache work, and no runtime flags.
- **Do not overengineer:** No multi-palette controls, no UI settings, no animation, no production toggle; prove map survival first.

---

## Priority band 6 — Comparison workflows

### Chunk 6.1 — Two-city compare mode (same chart, two locations)

- **Why:** “Best place on Earth” is the wrong frame; constrained comparison is the product story.
- **Dependencies:** Reliable single-chart runs; possibly 3.1.
- **Validation:** Numeric parity with two manual runs; map doesn't desync.
- **UX risks:** Cognitive overload—**side-by-side summary** before triple-map.
- **Architecture risks:** Medium—dual state in UI.
- **Do not overengineer:** Spreadsheet export can follow; start **on-map + small summary panel**.

---

## Priority band 7 — Professional mode

### Chunk 7.1 — “Professional defaults” preset

- **Why:** Hide lay clutter; expose inspectability toggles.
- **Dependencies:** Cleaner base UI (band 1).
- **Validation:** Session with practitioner script; no loss of popup truth.
- **UX risks:** Segmentation too early—**toggle**, not separate app.
- **Architecture risks:** Low.

### Chunk 7.2 — Export / report stub

- **Why:** Professional workflow artifact (roadmap / archaeology).
- **Dependencies:** What exactly exports—image, PDF, GeoJSON bundle—**scope small**.
- **Validation:** Lawyer/editor feedback not required for MVP stub—**technical correctness** first.
- **Do not overengineer:** PNG export before PDF pipeline.

---

## Priority band 8 — AI-assisted workflows (later)

### Chunk 8.1 — Reviewer prompt templates only

- **Why:** Institutional guardrails without product AI (`ai_context/memory_workflow.md`).
- **Dependencies:** None on app.
- **Validation:** Human feels reviews got sharper—qualitative.
- **Do not overengineer:** No autonomous agents editing repo.

### Chunk 8.2 — In-app optional assist (far)

- **Why:** After non-AI core is unassailable (`decisions.md`).
- **Dependencies:** Account/chart model; ethics review.
- **Architecture risks:** High—latency, trust, hallucination.

---

## Recommended “first sprint” after stabilization

**Chunks 1.1 + 1.2 + 2.1** — maximum clarity per unit risk: visible UX win, repeatable validation ritual.

---

## Related docs

- `docs/ux_principles_and_emotional_tone.md`
- `docs/map_and_overlay_design_research.md`
- `docs/workspace_hygiene_and_cleanup.md`
- `docs/relocation_app_product_roadmap.md`
