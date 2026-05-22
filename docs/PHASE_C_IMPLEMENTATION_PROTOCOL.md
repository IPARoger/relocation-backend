# Phase-C Implementation Protocol
## Operational constitution for landing the validated architecture without future chaos

> **Status:** Operational doctrine. Implementation planning only.
> **Authority on conflict:** `docs/relocation_map_architecture.md`,
> then `docs/PHASE_C_RENDERING_ARCHITECTURE.md` (substrate charter),
> then `docs/PHASE_C_PRODUCTION_MIGRATION_PLAN.md` (substrate swap),
> then `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` (cache shape),
> then this document, then existing meta-governance under
> `docs/process/*` and `ai_context/memory_workflow.md`.
> **Yields to:** all four authorities above and the existing
> meta-governance cycle. Does not override slow doctrine.
> **Adopted draft:** 2026-05-21.
> **Stability:** Slow. Changes by explicit edit naming prior stance.
> **Non-goals:** Aura aesthetics. Animation. Renderer rewrite. New
> endpoints. Astrology-math changes. Validated-adaptive-refinement
> behaviour changes. Telemetry infrastructure. Bureaucracy.

This document does one thing: define **how** the Phase-C work lands
across commits without producing regression chaos. It composes
with — never duplicates — the existing meta-governance docs. Where
those already legislate, this defers; where they are silent on
operational mechanics of substrate migration, this fills in.

---

## 0. Where this fits

| Layer | Owner |
|------|-------|
| Slow philosophy / meaning | `docs/process/doctrine_review_cycle.md`, `decision_and_uncertainty_framework.md`, `ai_context/core_product_truths.md`, brand / UX foundations |
| Substrate canon | `docs/relocation_map_architecture.md`, `docs/PHASE_C_RENDERING_ARCHITECTURE.md` |
| Migration plan | `docs/PHASE_C_PRODUCTION_MIGRATION_PLAN.md` |
| Cache plan | `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` |
| **Implementation protocol (this doc)** | Commit discipline, validation cadence, AI workflow rules, regression doctrine |
| Memory pipeline | `docs/process/archaeology_and_synthesis_workflow.md`, `ai_context/memory_workflow.md` |
| Interpretive AI behaviour | `docs/process/ai_drift_audit_framework.md` (consumer-facing AI; this doc covers **coding AI**) |

When this doc and a slow doctrine doc disagree, the slow doc wins
(per the slow-docs policy in `doctrine_review_cycle.md` §2). When
this doc and a Phase-C doctrine doc disagree, the Phase-C doc wins
(per its authority chain). When this doc and the existing
meta-governance disagree on cadence or process, the existing doc
wins; this one is additive.

---

## 1. Implementation Phase Breakdown

The Phase-C implementation is a linear sequence of nine
operationally-scoped phases. Each phase has one purpose, one
rollback scope, one gate, one explicit "done means" definition.

### Phase 1.1 — Documentation alignment (no code)

| Property | Value |
|----------|-------|
| Purpose | Record the substrate-path decision; align `ai_context/decisions.md`, `current_state.md`, `CURRENT_RENDERING_DOCTRINE.md`, `DOCTRINE_INDEX.md` so they reference the four Phase-C docs explicitly |
| Risk profile | None (no code change) |
| Rollback scope | Single commit revert |
| Validation gate | All existing smokes still pass (they should — no code changed); the doctrine index lists the four Phase-C docs |
| Done means | The substrate-path decision sentence (per migration plan §3 Phase 0 Step 0.1) appears in `decisions.md`; `current_state.md` references the Phase-C docs as authoritative |

### Phase 1.2 — Archaeology fencing (low-risk cleanup)

| Property | Value |
|----------|-------|
| Purpose | Migration plan §3 Step 0.2 + Step 0.3: fence aura PoC endpoints in `map_CURRENT.html` behind `?debugAuraPoc=1`; annotate the `contour` branch of `/search-regions` as archaeology |
| Risk profile | Low. No behaviour change on default page loads; archaeological annotations are comments |
| Rollback scope | Two independent commits, each revertible in one `git revert` |
| Validation gate | `scripts/smoke_map_current.py` still passes; manual: default page load shows no aura PoC chrome |
| Done means | Default-load `map_CURRENT.html` does not call `/aura-raster*`; `contour` branch carries archaeology comment cross-referencing `PHASE_C_PRODUCTION_MIGRATION_PLAN.md` |

### Phase 1.3 — Scheduler extraction (no behaviour change)

| Property | Value |
|----------|-------|
| Purpose | Cache plan §10 Step 1: move the Phase-2 scheduler logic out of `map_SANDBOX_phase2_cache.html` into a reusable module (`static/phase2_cache_scheduler.js` or equivalent) |
| Risk profile | Medium-low. Sandbox behaviour must remain bit-identical |
| Rollback scope | One commit revert |
| Validation gate | `scripts/smoke_phase2_cache.py` passes against the sandbox after extraction (every test: first paint, pause, priority order, immediate-after-interrupt, no half-cached entries, budget, cache populated) |
| Done means | The scheduler module is importable; the sandbox imports it and behaves identically |

### Phase 1.4 — Substrate adapter scaffold (legacy-only)

| Property | Value |
|----------|-------|
| Purpose | Migration plan §3 Step 1.2: build `runOverlay(payload, substrate)` and `renderOverlay(result, substrate)` in `map_CURRENT.html`; legacy-only initially |
| Risk profile | Low. Functions wrap existing `postSearchRegions`/`renderHouseFeatures`; production behaviour unchanged |
| Rollback scope | One commit revert |
| Validation gate | `scripts/smoke_map_current.py` and `scripts/validate_sprint_dc_ic.py` both pass; `?substrate=legacy` and no flag yield identical behaviour |
| Done means | Adapter functions exist and route legacy by default; canonical path returns a clear `not_implemented` error |

### Phase 1.5 — Canonical substrate wiring (flag-gated)

| Property | Value |
|----------|-------|
| Purpose | Migration plan §3 Step 1.3: enable `?substrate=canonical` to route through `postScreenPixelTruth` + `paintMaskToCanvas`; default stays `legacy` |
| Risk profile | Medium. Introduces a second visible substrate that operators can engage |
| Rollback scope | One commit revert (the canonical branch in the adapter is added; reverting restores legacy-only) |
| Validation gate | All existing smokes still pass; `?substrate=canonical` produces a visible overlay; new `smoke_substrate_parity.py` (Phase 1.7) is a *follow-up*, not this step's gate |
| Done means | Operator can flip via URL param and see canonical paint; legacy default unchanged |

### Phase 1.6 — Scheduler/cache wiring on canonical (flag-gated)

| Property | Value |
|----------|-------|
| Purpose | Migration plan §3 Step 1.4: route canonical USER requests through the Phase-2 scheduler; legacy path remains direct-fetch |
| Risk profile | Medium. Scheduler integration in a new host (`map_CURRENT.html`) may surface event-handler conflicts with `currentRenderToken` |
| Rollback scope | One commit revert |
| Validation gate | `smoke_phase2_cache.py` adapted to run against `map_CURRENT.html` with `?substrate=canonical`; passes |
| Done means | Cache populates on canonical path; cancellation works end-to-end on `map_CURRENT.html` |

### Phase 1.7 — Parity validation harnesses

| Property | Value |
|----------|-------|
| Purpose | Migration plan §3 Step 2: land the new harnesses — `smoke_substrate_parity.py`, `smoke_popup_overlay_parity.py`, seam smoke, high-lat smoke |
| Risk profile | Low. Harnesses are read-only against running production; no production change |
| Rollback scope | Each harness in its own commit; trivially reversible |
| Validation gate | Each harness's first run produces an actionable JSON report under `validation/reports/`; thresholds defined in migration plan §4 hold |
| Done means | Each smoke is committed, runs in under 60 s wall (or under 5 min for heavy harnesses), and emits a JSON report |

### Phase 1.8 — Default flip + stabilisation

| Property | Value |
|----------|-------|
| Purpose | Migration plan §3 Step 3: flip `DEFAULT_SUBSTRATE = "canonical"`; stabilisation window |
| Risk profile | High. Default-visible behaviour changes |
| Rollback scope | Per-deploy revert of the default constant |
| Validation gate | All Phase 1.7 harnesses green; stabilisation window (operator-defined, e.g. 1–2 sessions of meaningful map work) closes with zero substrate-attributed regressions |
| Done means | Default loads render canonical; `?substrate=legacy` still works as the safety net; operator has done at least one full chart-exploration session without falling back |

### Phase 1.9 — Legacy retirement + supersession pass

| Property | Value |
|----------|-------|
| Purpose | Migration plan §3 Step 4: remove the legacy branch from `runOverlay`/`renderOverlay`; mark `/search-regions` legacy in docstring; update doctrine index |
| Risk profile | Medium. Deletes the safety net, but only after stabilisation passed |
| Rollback scope | One commit revert restores the legacy branch (it's a deletion, not a transformation) |
| Validation gate | All Phase 1.7 harnesses green on canonical-only; legacy code paths under `?debugLegacy=1` (if retained) work; doctrine index reflects the new state |
| Done means | `DEFAULT_SUBSTRATE` constant removed; substrate flag is a no-op; documents updated; this protocol document marked `STATUS: completed for Phase 1` |

### Phase 1.10 — Post-Phase-1 reflection

| Property | Value |
|----------|-------|
| Purpose | Per `doctrine_review_cycle.md` §7 (post-major-pivot review): update `decisions.md`, `current_state.md`, `open_questions.md`; one optional archaeology extract capturing the migration arc |
| Risk profile | None |
| Rollback scope | Standard doc revert |
| Validation gate | Doctrine coherence pass per `doctrine_review_cycle.md` §6.1 |
| Done means | Future contributors can read the Phase-C arc from `decisions.md` + the four Phase-C docs without needing the chat transcripts |

### Future Phases (not in this protocol's scope)

| Phase | Trigger |
|-------|---------|
| Phase 2: Aspect-overlay migration | Phase 1.10 done and operator chooses to migrate aspect from legacy to canonical |
| Phase 3: Aura aesthetic pass | Phase 2 done and the substrate is stable; aura doctrine per Phase C charter §10 step 3 |
| Phase 4: Advanced caching | Aesthetic pass landed and stable; per cache doctrine §3, §4 deferred items |
| Phase 5: Predictive behaviour | Telemetry exists and proves measured wins |

Each future phase requires its own protocol doc analogous to this one;
this document does not pre-write them.

---

## 2. Commit Doctrine

### 2.1 Commit sizing philosophy

The repo's existing commit style (observed from `git log`):

| Existing example | Style |
|-----------------|-------|
| `Add map smoke test and UI handoff workflow` | Short imperative, no prefix, no body |
| `Add DC/IC parity for angle-in-sign, aspect overlays, and popups` | Subject describes scope; no body needed |
| `Stabilize chart profiles and compact relocated popup` | One verb, one scope |

This style is **adopted, not replaced**. Phase-C commits use the
same shape:

| Aspect | Rule |
|--------|------|
| Subject form | Imperative, ≤ 72 chars: `Add canonical substrate adapter scaffold` |
| Prefix | None (no `feat:`, `chore:`, `refactor:`; the repo doesn't use them) |
| Body | Only when the subject alone is insufficient; one short paragraph explaining *why* |
| Trailers | None (no `Signed-off-by`, no `Co-authored-by`, no agent markers — the repo doesn't carry them) |
| Scope | One concern per commit (see §2.4) |
| Size | Small enough to revert in a single `git revert` without leaving the tree broken |

### 2.2 Commit message conventions (additive to repo style)

Phase-C-specific conventions:

| Convention | Rule |
|-----------|------|
| Reference docs in body when the change *operationalises* a doctrine clause | `Per PHASE_C_PRODUCTION_MIGRATION_PLAN §3 Step 0.2.` |
| Reference superseded docs when the change *retires* them | `Supersedes: validation/narratives/sun_conjunct_asc_truth_field_spine_phase_a.md (now archaeology).` |
| Reference smokes the change must keep green | `Smoke gate: smoke_map_current.py, smoke_phase2_cache.py.` |
| Never include "AI generated by …" or similar trailers | The repo doesn't carry them; adding them would be doctrine drift |
| Never include emoji in commit messages | Inconsistent with the repo's existing tone |

### 2.3 Reversible boundaries

A commit is at a reversible boundary if, after `git revert <commit>`:

- The tree builds and serves.
- All smokes that were green before the commit are green after the revert.
- No data migration is required to restore prior behaviour.
- No persistent state (cache, config, env var) needs manual cleanup.

If any of these fails, the commit is not at a reversible boundary
and must be split into smaller commits until each individual revert
is clean.

### 2.4 Prohibited mixed-purpose commits

| Forbidden mix | Reason |
|--------------|--------|
| Doctrine doc edit + code change | Doctrine changes are reviewed differently from code; mixing buries either |
| Two phases in one commit | Defeats per-phase rollback |
| Refactor + feature | Refactor must be no-behaviour-change by definition; feature is behaviour change; mixing makes regression bisection impossible |
| Test added + code it tests | First add the failing test, then add the code that makes it pass — two commits |
| Multiple smoke harnesses landing together | Each harness in its own commit so failures localise |
| Fix + cleanup | The cleanup may mask the fix's effect |
| Migration step + supersession pass | Step lands first; supersession is the closing pass |

### 2.5 "One instability source at a time" doctrine

If the tree has any failing smoke, the next commit must reduce
instability sources by **exactly one**:

| Current state | Permitted next commit |
|---------------|----------------------|
| All green | Land one new step (one new source possible) |
| One smoke red | Fix that smoke. Do not also land a new step |
| Two smokes red | Fix one of them. Do not also fix the other in the same commit |
| Smoke red and a doctrine clarification needed | Fix the smoke first; doctrine clarification is its own commit |

This is the most important rule in §2. Multiple-instability-source
commits are how migrations turn into chaos.

### 2.6 Archaeology annotation rules

When a commit retires a code path:

| Pattern | Requirement |
|---------|-------------|
| Code physically deleted | Commit body lists where the rationale lives (`See PHASE_C_PRODUCTION_MIGRATION_PLAN §5.1`) |
| Code retained behind a debug flag | Comment at the surface: `// ARCHAEOLOGY: legacy <substrate/feature>. Status superseded <date>. See <doc>.` |
| Endpoint retained for validation only | Docstring banner: `STATUS: legacy. Replaced in production by <X> on <date>. Retained for archaeology / validation.` |
| Document marked superseded | Header banner: `> **Status:** SUPERSEDED on <date> by <doc>. Reason: <sentence>. Retained as archaeology.` |

The annotation is the rollback documentation. A future developer
reading the surface sees in the first line: this was superseded,
here's the replacement, here's the reasoning.

### 2.7 Supersession annotation rules

A supersession is the formal end of a superseded path's role. The
rules:

| Rule | Why |
|------|-----|
| Date in ISO format (`YYYY-MM-DD`) | Disambiguates supersession history |
| Reason in one sentence | Forces clarity; full reasoning lives in the linked doc |
| Replacement doc path explicit | The reader can navigate forward in one click |
| Never delete the superseded artefact in the same commit | Supersession is annotation; deletion (if it happens at all) is a separate later commit |
| Update `DOCTRINE_INDEX.md` in the supersession commit | Index is the discovery surface; out-of-date index defeats archaeology |

---

## 3. Validation Harness Architecture

### 3.1 Three-tier model

| Tier | What | Runtime | Cadence |
|------|------|--------|---------|
| **Lightweight smokes** | Per-feature correctness checks against the running backend | < 30 s each | Every commit that touches code in the smoke's scope |
| **Heavy validation suites** | Full parity / drainage / chart-change / storm runs | ≤ 5 min each | Phase boundaries; before flipping default substrate |
| **Visual review artefacts** | Screenshots + capture scripts + narratives | Operator review | Phase boundaries + ad hoc when a regression is suspected |
| **Canonical benchmark datasets** | Versioned chart fixtures (§4) | Inputs only — no runtime | Updated only by explicit operator decision |

The cadence is **trigger-based**, not calendar-based, mirroring
`doctrine_review_cycle.md` §6. A smoke runs when its scope is
touched; a heavy suite runs at a phase boundary; visuals are
reviewed when the operator wants signal.

### 3.2 Lightweight smokes (existing + planned)

| Smoke | Owns | Status |
|-------|------|--------|
| `scripts/smoke_map_current.py` | Production map renders correctly (existing legacy substrate today; will own canonical substrate post-flip) | Exists |
| `scripts/smoke_phase2_cache.py` | Phase-2 scheduler/cache invariants in sandbox | Exists |
| `scripts/validate_sprint_dc_ic.py` | Sprint DC/IC fixture parity | Exists (heavier than a smoke; see §3.3) |
| `scripts/smoke_substrate_parity.py` | Canonical XOR vs brute-force wall within thresholds (per fixture) | **Planned (Phase 1.7)** |
| `scripts/smoke_popup_overlay_parity.py` | Popup classification matches overlay at sampled points | **Planned (Phase 1.7)** |
| `scripts/smoke_phase2_cache_drainage.py` | Full A→H drainage without interruption (cache plan §7.6) | **Planned (Phase 1.6 follow-up)** |
| `scripts/smoke_phase2_cache_storm.py` | Interruption-storm recovery | **Planned (Phase 1.6 follow-up)** |
| `scripts/smoke_phase2_cache_chart_change.py` | Per-chart cache invalidation | **Planned (Phase 1.6 follow-up)** |

Smokes are JSON-emitting Playwright/HTTP scripts that exit 0 on
pass, non-zero on fail. Each writes its report to
`validation/reports/<name>.json`. No new smoke surface (Datadog,
Prometheus, etc.) is built.

### 3.3 Heavy validation suites

These run longer but are still scripted, deterministic, and emit
JSON. They are **not** lightweight smokes; they should not gate
every commit.

| Suite | Scope | Trigger |
|-------|-------|---------|
| `scripts/validate_sprint_dc_ic.py` | Full sprint-DC/IC fixture validation across multiple conditions | Phase boundaries; before default flip |
| `scripts/smoke_substrate_parity.py` run against full fixture list | Cross-fixture XOR table | Same |
| New benchmark replay (planned, optional) | Replay a canonical user sequence and capture timing + sample count | When performance suspected to have regressed |

A heavy suite that newly fails is a stop-the-line event. Smokes
that fail are commit-level events.

### 3.4 Visual review artefacts

| Artefact | Owns |
|----------|------|
| `validation/screenshots/migration_baseline/<fixture>.png` | Reference renders for each canonical fixture; diffed at phase boundaries |
| `scripts/capture_*.py` (existing 14 captures) | One-off measurement runs for narratives; **archaeology** for prior validation, not Phase-1 gates |
| `validation/narratives/<phase>.md` | Per-phase write-up: what changed, what stayed, where mismatch persists |
| Per-phase doctrine-index update | Discoverability surface |

The 14 existing `capture_*.py` scripts are **historical** — they
captured the screen-pixel-adaptive work that grounded the substrate
charter. They remain in tree as archaeology. They are not Phase-1
gates; running them is optional.

### 3.5 Canonical benchmark datasets

Defined in §4.

### 3.6 What harness work is explicitly *not* built

| Avoided | Reason |
|---------|--------|
| A test-orchestration framework | Smokes are scripts; the operator runs them or wires them into a simple shell loop |
| A test-result database | Reports are JSON files in `validation/reports/`; diffing is `git diff` |
| A web UI for harness results | Operator reads JSON or screenshots; no dashboard needed |
| A nightly CI job system | No CI infrastructure today; operator runs smokes on demand |
| Mutation testing or fuzzing infrastructure | The substrate's correctness is grounded in the brute-force wall; mutation testing is YAGNI |

---

## 4. Benchmark Doctrine

### 4.1 Canonical chart fixtures

A fixed set of chart fixtures used as gold-standard inputs across
all parity, screenshot, and benchmark surfaces. The set is **small
and stable** by design. Adding a fixture is an operator decision,
recorded in `ai_context/decisions.md` with reason.

| Fixture | Source | Why canonical |
|---------|--------|---------------|
| `default_sample` | `chart-profiles` endpoint | Baseline general appearance; first fixture every smoke touches |
| `sprint_dc_ic` | Validated against `validation/reports/sprint_dc_ic_validation.json` | Hardest case for ASC/MC/DC/IC angle treatment |
| `dense_5_americas` | Per `screen_pixel_dense_residue.md` | Worst observed dense-overlap; budget-ceiling test |
| `greenland_iceland` | Per `aura_field_engine.py` `greenland_iceland` viewport | High-latitude edge case |
| `pacific_dateline` | Synthetic, lon ∈ [-200, -160] | Seam case |
| `svalbard` | Per `screen_pixel_adaptive_targeted.md` | Polar high-lat with active targeted refinement |

This list is the entire canonical set for Phase 1. Adding fixtures
later requires a decision-log entry.

### 4.2 Canonical edge-case viewports

| Viewport | Used to test |
|----------|--------------|
| World view (default) | General; baseline |
| North America zoom 4 | Dense overlap class |
| Europe zoom 4 | Aspect overlay class |
| Greenland zoom 4 | High-lat + lat-cap |
| Pacific basin centered lon=180 | Seam |
| Svalbard zoom 6 | Targeted refinement triggers |

The viewport set crosses with the fixture set. Not every fixture
runs every viewport; smoke harnesses pick the relevant pairs.

### 4.3 Acceptable XOR thresholds (measured ceilings)

Per migration plan §4.3, repeated here for operational clarity:

| Case | Threshold |
|------|-----------|
| Single condition, typical viewport | ≤ 0.10% |
| 3-condition overlap | ≤ 0.20% |
| Dense 5–6 conditions | ≤ 0.40% (worst observed 0.386%) |
| Greenland/Iceland (lat_cap) | ≤ 0.50% |
| Seam (dateline) | ≤ underlying-case threshold |

Thresholds are **measured ceilings, not goals**. A change that
moves XOR from 0.20% to 0.10% is welcome but never required.

### 4.4 Latency ceilings

| Surface | Ceiling |
|---------|---------|
| Single-condition USER fetch, 720×450 | ≤ 1.0 s end-to-end (measured ~0.5 s) |
| Dense-5-condition USER fetch, 720×450 | ≤ 2.0 s end-to-end |
| Smoke wall time (`smoke_phase2_cache.py`) | ≤ 30 s (measured 2.97 s) |
| Heavy-suite wall time | ≤ 5 min |

A ceiling breach in production blocks the phase advance. A
30%-tolerance band around the ceiling is permitted before treating
the breach as a regression.

### 4.5 Sample-budget ceilings

Per `screen_pixel_adaptive_targeted.md` + cache plan §1.1:

| Surface | Ceiling |
|---------|---------|
| Per-USER-fetch samples, 720×450 | ≤ 233 118 (Phase-2 budget) |
| Per-USER-fetch samples, dense 5 conditions | ~194 265 (worst observed) |
| Per-USER-fetch samples, dense 6 conditions | ~194 265 (worst observed) |
| Phase-2 cache aggregate background samples | ≤ 233 118 minus active USER consumption |

Exceeding the budget is a substrate regression, not a cache
regression. Cache jobs that would exceed are `deferred_budget` —
not failures.

### 4.6 Escalation rules

If a benchmark exceeds a ceiling:

| Severity | Action |
|----------|--------|
| ≤ 30% over ceiling, single fixture | Investigate; not yet a phase-blocker |
| > 30% over ceiling, single fixture | Phase-blocker until resolved |
| Multiple fixtures over ceiling | Phase-blocker; suspect substrate regression |
| All fixtures over ceiling | Stop the line; revert to last known good |

### 4.7 How future changes are judged

| Change type | Judgement criterion |
|------------|---------------------|
| Substrate change | Must maintain or improve XOR-vs-wall on every fixture; budgets unchanged |
| Cache change | Must maintain scheduler invariants (cancellation, no half-cached entries, budget); cache-hit ratio may rise but is not required to |
| Renderer change | Visual screenshot diff within pixel tolerance per fixture |
| Doctrine change | Per `doctrine_review_cycle.md` §7 post-pivot requirement |

Improvements are welcome; regressions block. The baseline is what
is measured today, recorded in `validation/reports/`.

---

## 5. Regression Doctrine

### 5.1 What counts as regression

A regression is **any change in measured behaviour** in one of these
categories, against the baseline established in `validation/reports/`
on the most recent green commit on the relevant branch:

| Category | What counts |
|----------|------------|
| **Truth regression** | Popup-overlay parity drops below 100% on canonical; brute-force XOR exceeds the threshold; classification semantics change for an unchanged input |
| **Visual regression** | Screenshot diff exceeds per-fixture pixel tolerance; visible artefacts appear (stripes, missing tiles, ghost layers) |
| **UX regression** | Render latency exceeds ceiling by >30%; debounce fails; pause-on-gesture stops working; gesture-storm produces stuck state |
| **Scheduler regression** | `__phase2.metrics.abortsObserved` does not rise on interrupt; cache populates with half-cached entries; priority order misregisters |
| **Cache regression** | Cache key collision; chart-change does not invalidate; substrate flip does not invalidate |
| **Doctrine regression** | Code change that contradicts a slow doctrine clause without first updating the doctrine; archaeological surface deleted without supersession trail; superseded doc revived without explicit edit |

### 5.2 Acceptable vs unacceptable drift

| Drift | Acceptable | Action |
|-------|-----------|--------|
| Sample count moves within ±10% on a fixture | Yes | Note in narrative; no smoke change |
| XOR moves within threshold | Yes | Same |
| Latency moves within 30% of ceiling | Yes | Same |
| Per-cell classification changes for unchanged input | **No** | Stop the line; this is a truth regression |
| Popup-overlay parity drops at all on canonical | **No** | Same |
| Cache-hit pattern changes on identical-input replays | **No** unless caused by an explicit cache-key change | Investigate |
| Screenshot diff visible but classifications unchanged | Discuss | Review visual; decide whether the visual change is acceptable evolution |
| Doctrine-doc edit without referenced rationale | **No** | Reject; require rationale |

### 5.3 Visual regressions specifically

| Visual change | Treatment |
|--------------|-----------|
| Block-edge appearance changes (canonical substrate) | Acceptable evolution if classifications unchanged |
| Polygon stroke style changes (legacy substrate, during Phase 1) | Treat as regression unless intended |
| Aura intensity / opacity changes | Out of scope (no aura yet); will block any Phase 1 commit |
| Animation / transition appearing | **Block** — animation forbidden by Phase C charter |
| Spinner appearing during cache-warm | **Block** — cache is invisible |
| Refinement-stage debug overlay appearing on default | **Block** — debug-only is debug-only |

### 5.4 Truth regressions specifically

These are the hardest violations:

| Violation | Severity |
|-----------|----------|
| Overlay says X at (lat, lon); popup says Y | **Catastrophic** — defeats truth hierarchy |
| Canonical XOR vs wall exceeds threshold on any fixture | **High** — substrate correctness violated |
| Substrate flip changes classifications for identical input | **High** — substrate is supposed to be input-deterministic |
| `swe.houses` answer for (lat, lon) varies across requests | **Catastrophic** — engine non-determinism |

Truth regressions block all advance until resolved. No phase
boundary crosses while a truth regression is open.

### 5.5 UX regressions specifically

| Regression | Severity |
|-----------|----------|
| First-paint latency exceeds 1.0 s consistently | High |
| Cancellation fails to pause within 200 ms of gesture | Medium |
| Layers stack across renders | High |
| Map-readability lost (cities/labels obscured) | High |
| Sidebar visible state mutates on substrate flip | High (per UX-continuity doctrine) |
| Aura layer leaks into default load | High (per archaeology fencing) |

### 5.6 Doctrine regressions specifically

| Regression | Severity |
|------------|----------|
| Code contradicts slow doctrine without slow-doctrine edit | **High** — implementation becoming secret law |
| Superseded surface revived without explicit doctrine reversal | **High** |
| Anti-pattern from `decisions.md` "Rejected institutional lessons" reappears | **High** |
| Tension resolved in code that doctrine names as open | **High** |
| Telemetry / persistence / pluggable architecture added without doctrine support | **High** |

Doctrine regressions are real regressions. They block phase advance
even when smokes are green.

---

## 6. Coding AI Collaboration Doctrine

This section governs how AI sessions (Cursor agent, this assistant,
future coding AI) participate in Phase-C work. It is **distinct from**
`docs/process/ai_drift_audit_framework.md`, which covers
consumer-facing interpretive AI. The patterns rejected here are
*coding* patterns, not interpretive ones.

### 6.1 Grounding requirements (mandatory before substantive work)

Before proposing any architectural change, the AI must:

| Action | Reason |
|--------|--------|
| Read the current state of the affected file(s) | Avoid arguing against memory or against a stale repo snapshot |
| Read the four Phase-C doctrine docs | They are the substrate-level law |
| Read `ai_context/current_state.md`, `decisions.md`, `core_product_truths.md` | They are the durable memory |
| Read the relevant narrative under `validation/narratives/` if one exists | Evidence ground |
| Check whether the proposal contradicts a "Rejected institutional lessons" entry | Avoid reviving rejected paths |

If any read is skipped, the AI must declare which read was skipped
and why before proposing.

### 6.2 Repo-reading discipline

| Pattern | Required |
|---------|---------|
| Read the actual current state of `main_centerline_FIXER.py` before discussing endpoint behaviour | The endpoint surface evolves |
| Read the actual current state of `map_CURRENT.html` before discussing frontend behaviour | Same |
| Read validation JSONs before citing numbers | Numbers in memory may be stale |
| Read narrative MDs before claiming prior decisions | Decisions in memory may be misremembered |

The default posture is **the repo is the truth**. Memory is a hint;
the repo is the source.

### 6.3 Archaeology-reading discipline

Before proposing a feature, abstraction, or behaviour:

| Action | Reason |
|--------|--------|
| Search `docs/` for SUPERSEDED markers near the proposal area | Avoid reviving a superseded path |
| Search `validation/narratives/` for similar prior attempts | Avoid re-running an already-disproven experiment |
| Search `decisions.md` "Rejected institutional lessons" for adjacency | Avoid known-bad patterns |
| If a superseded path is the right answer | **Reverse the supersession explicitly** in a doctrine edit; do not silently revive |

### 6.4 No speculative confidence

| Forbidden pattern | Replacement |
|-------------------|------------|
| "This will probably improve performance" | Measure first, then claim |
| "Users typically want X" | No telemetry; cite the doctrine doc that names the preference |
| "This is the standard pattern" | Cite the specific doctrine clause that prescribes it for this repo |
| "It looks like X" without reading | Read X first |
| Asserting that a smoke passes without running it | Run it or say "untested" |

Confidence is grounded in evidence (measured XOR, smoke output, doc
clause) or it is qualified as speculation.

### 6.5 No mixing aesthetics with substrate

| Pattern | Rule |
|---------|------|
| Substrate task arrives | Do substrate work only |
| Aesthetic task arrives | Substrate must be stable first |
| Both arrive together | Refuse the package; split into two |
| "While I'm here, let me also …" | Don't |
| Decorative animation appears in a substrate PR | Block at review |

The Phase-C charter §10 ordering is explicit. Mixing violates the
ordering and turns into doctrine regression.

### 6.6 No simultaneous architecture rewrites

| Scope | Rule |
|-------|------|
| One architectural surface per session | Substrate OR cache OR scheduler OR rendering, not multiple |
| Two architectures touched in one PR | Split |
| "Refactor while migrating" | The migration is enough work; the refactor waits |
| Doctrine doc edit + code change | Split (per §2.4) |

This is the single most important guardrail against AI-driven
patch cascades.

### 6.7 When to stop and ask

The AI stops and asks the operator when:

| Trigger | Why |
|---------|-----|
| Two contradictory doctrine clauses apply | Operator picks |
| The repo state contradicts the request's premise | Operator confirms or corrects |
| The proposal would supersede an existing doctrine doc | Supersession is a deliberate act; never silent |
| A smoke is failing and the cause is unclear | Stop; root-cause; don't speculate |
| The user prompt mixes multiple architectural surfaces | Ask which to prioritise |
| The user prompt would skip a phase boundary | Confirm explicitly |
| The user prompt implies aesthetic work mid-substrate | Confirm; usually refuse |

Stopping is a signal of discipline, not failure. The operator
prefers a clear stop to a confident wrong answer.

### 6.8 How to avoid AI patch cascades

A patch cascade is when each fix introduces a new error to fix.
Causes:

| Cause | Avoidance |
|-------|-----------|
| Fixing a symptom rather than a cause | Root-cause before patching |
| Patching one part of a contract while leaving the other inconsistent | Identify the full contract; patch all of it or none |
| Suppressing an error to keep moving | Errors are signal; surface them |
| Re-organising files mid-bug-fix | One concern at a time |
| Adding abstractions to "make the fix general" | YAGNI; fix the specific case |
| Ignoring a doctrine clause "just for this PR" | Doctrine clauses don't have exceptions; if one needs one, edit the doctrine |
| Assuming a previous session's code was correct because it ran | Run the smoke; verify |

### 6.9 Model-mode confirmation discipline

The pattern established in this thread:

| When | What |
|------|------|
| Start of a substantive doctrine session | AI confirms model identity and tool surface explicitly |
| Fallback signals (degraded tools, restricted context) | AI stops and reports |
| Operator confirms intended tier | AI proceeds |
| Operator does not confirm | AI may proceed with the confirmation it can make (model name) and explicitly note what it cannot introspect (UI reasoning tier) |

This is a soft contract. The AI cannot enforce the operator's Cursor
UI settings; it can be transparent about what it can and cannot
verify.

### 6.10 Cited evidence over rhetoric

| Pattern | Required form |
|---------|--------------|
| "The substrate works" | Cite the smoke run: "smoke_phase2_cache.py all_pass: true, wall 2.97 s, 2026-05-21" |
| "The user prefers calm chrome" | Cite the doc: "per ux_principles_and_emotional_tone.md §X" |
| "The cache is invalidated on chart change" | Cite the cache key shape: "PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md §2.7" |
| "Polygon smoothing is rejected" | Cite the supersession: "screen_pixel_truth_diagnosis.md §X" |
| "This is what we always do" | If true, the doctrine doc will say so; cite it. If false, don't say it. |

---

## 7. Documentation Hierarchy Refinement

### 7.1 Canonical docs (where new readers start)

| Level | Doc |
|-------|-----|
| **Onboarding entry point** | `ai_context/README.md` |
| **What's true now** | `ai_context/current_state.md` |
| **Architecture canon** | `docs/relocation_map_architecture.md` |
| **Substrate charter (Phase-C era)** | `docs/PHASE_C_RENDERING_ARCHITECTURE.md` |
| **Current rendering doctrine summary** | `docs/CURRENT_RENDERING_DOCTRINE.md` |
| **Doctrine index** | `docs/DOCTRINE_INDEX.md` |
| **Implementation protocol (this doc)** | `docs/PHASE_C_IMPLEMENTATION_PROTOCOL.md` |
| **Decisions log** | `ai_context/decisions.md` |
| **Open questions** | `ai_context/open_questions.md` |

A new contributor (human or AI) reading these in order has the full
operating picture in under an hour.

### 7.2 Superseded docs (preserved, not active)

| Doc | Status |
|-----|--------|
| `docs/technical_philosophy/progressive_field_reveal.md` | SUPERSEDED 2026-05-21 (per Phase-C charter §8) |
| `docs/technical_philosophy/truth_field_rendering_path.md` | SUPERSEDED 2026-05-21 (same) |
| `validation/narratives/sun_conjunct_asc_truth_field_spine_phase_a.md` | SUPERSEDED 2026-05-21 (per Phase-C charter §8) |
| `validation/narratives/progressive_reveal_phase_b.md` | SUPERSEDED 2026-05-21 (same) |

Each carries a header banner per §2.7. Removal of a SUPERSEDED doc
is a deliberate act and requires its own commit + doctrine note.

### 7.3 Archaeology docs (permanent)

Per `docs/PHASE_C_RENDERING_ARCHITECTURE.md` §8:

| Surface | Permanent because |
|---------|------------------|
| Every superseded narrative | Records the reasoning that produced the supersession |
| Every superseded sandbox HTML | Holds the experimental ground |
| `/brute-force-grid` endpoint | The canonical validation wall |
| `memory_archaeology_raw/` | Raw evidence underlying current doctrine |
| Old File/ directory | Pre-Phase-C history |

### 7.4 Experimental docs (active investigation)

| Surface | Lives in |
|---------|----------|
| Aesthetic / aura exploration | `docs/overlay_and_aura_visual_strategy.md`, `docs/cartographic_language_and_city_rendering.md`, `docs/brand_and_experience_foundations.md` |
| Geocoder strategy | `docs/geocoder_and_city_identity_strategy.md` |
| Future implementation sequencing | `docs/next_implementation_sequence.md` |

These are not canonical yet; they are working notes. They become
canonical when an explicit doctrine edit promotes them and the
slow-docs policy is honoured (`doctrine_review_cycle.md` §2).

### 7.5 Validation narratives

| Surface | Role |
|---------|------|
| `validation/narratives/<topic>.md` | Per-investigation write-up: hypothesis, method, result, what was learned |
| `validation/reports/<topic>.json` | Mechanical artefact (smoke output, capture output) |
| `validation/screenshots/<topic>/` | Visual evidence |

Narratives are written as work happens. They are not curated
canonical docs; they are evidence. The curated canonical docs
**cite** narratives; they do not absorb them.

### 7.6 Decision logs vs open questions

| Surface | Role |
|---------|------|
| `ai_context/decisions.md` | Decisions taken, with rationale; one source of truth |
| `ai_context/open_questions.md` | Decisions deferred; named explicitly so they don't get silently closed |
| `validation/narratives/*` cross-reference | Evidence underlying decisions |

A decision must appear in `decisions.md` before code that depends
on it lands. An open question must appear in `open_questions.md`
before the project advances around it.

### 7.7 Open tensions

Per `doctrine_review_cycle.md` §4 (tension preservation):

| Tension | Status |
|---------|--------|
| Substrate-path choice (legacy wrapping vs migrate-first) | **Resolved** — Path A (migrate first), per migration plan |
| Cache eviction policy | **Open** — no eviction yet; revisit if budget rises |
| Cross-zoom cache reuse | **Open** — deferred; prerequisite is interior-occupancy reuse |
| Condition-mask recombination | **Open** — deferred until backend semantics validated |
| Aspect-overlay migration timing | **Open** — Phase 2 of the broader migration; no date |
| Aura aesthetic timing | **Open** — Phase 3 of the broader migration; depends on substrate stability |
| Server-side / persistent cache | **Open** — deferred; no infrastructure |

This list is intentional. Some tensions stay open until practitioner
feedback, stress testing, or product evolution justifies closure.

### 7.8 Where future contributors should start

1. `ai_context/README.md` — what this folder is.
2. `ai_context/current_state.md` — what is true now.
3. `docs/DOCTRINE_INDEX.md` — what doctrine exists, where it lives.
4. `docs/CURRENT_RENDERING_DOCTRINE.md` — the rendering stack.
5. The four Phase-C docs — substrate, cache, migration, this protocol.
6. `ai_context/decisions.md` + `open_questions.md` — what was decided, what is open.
7. The validation narrative most relevant to the contributor's task.

That sequence is enough to operate.

---

## 8. Production Readiness Doctrine

The Phase-C work feeds multiple downstream readiness tiers. Each
tier has explicit prerequisites. Tiers are not crossed casually.

### 8.1 Tier 0 — Operator dogfood (now)

| Prerequisite | State |
|--------------|-------|
| Smokes pass | Yes (existing) |
| Operator runs `map_CURRENT.html` daily | Yes |
| Operator notes regressions in `ai_context/open_questions.md` | Workflow exists |

Tier 0 is the baseline. The operator is already here.

### 8.2 Tier 1 — Internal trusted-user testing

| Prerequisite | Required |
|--------------|----------|
| Phase 1.8 complete (canonical substrate default) | Yes |
| Phase 1.7 harnesses all green | Yes |
| Popup-overlay parity 100% on canonical | Yes |
| Brute-force XOR within thresholds on all canonical fixtures | Yes |
| Operator-driven stabilisation window passed | Yes |
| Aspect overlay still on legacy or migrated cleanly | Yes (Phase 2 acceptable; legacy acceptable for Tier 1) |
| Onboarding instructions for trusted users exist | Yes (this doc + `current_state.md`) |

### 8.3 Tier 2 — Professional astrologer testing

| Prerequisite | Required |
|--------------|----------|
| All Tier 1 prereqs | Yes |
| Aspect overlay on canonical substrate | Phase 2 done |
| One full UX coherence pass per `doctrine_review_cycle.md` §6.3 | Yes |
| Validation narrative covering practitioner-meaningful fixtures | Yes |
| Aura aesthetics: **explicitly not required**; raw block rendering is acceptable for professional testing | Honest rendering > polished rendering |
| Geocoder integration: not required for Tier 2 if the chart-profile UI is sufficient | Acceptable |

Tier 2 is where the substrate's truthfulness is professionally
verified. Aesthetics polish is intentionally not blocking.

### 8.4 Tier 3 — Production rollout (public-ish)

| Prerequisite | Required |
|--------------|----------|
| All Tier 2 prereqs | Yes |
| Practitioner feedback from Tier 2 incorporated or explicitly deferred | Yes |
| Aura aesthetic pass landed (Phase 3) | Yes |
| Onboarding UX exists for non-expert users | Yes |
| `docs/current_sidebar_ux_audit.md` revisited | Yes |
| Privacy / data-handling clarified if any user data persists | Yes (deferred otherwise) |

Tier 3 is the first time the product is shown to anyone who is not
a practitioner or trusted insider.

### 8.5 Tier 4 — Aesthetic passes (aura, polish)

| Prerequisite | Required |
|--------------|----------|
| Substrate stable in production for ≥ 1 month | Yes |
| Aura visual doctrine (`docs/overlay_and_aura_visual_strategy.md`) approved | Yes |
| Aura validation narrative produced | Yes (per Phase 3 work) |
| No regression in popup-overlay parity | Yes (aura must not redefine membership) |

Aesthetic passes never substitute for substrate correctness. They
follow it.

### 8.6 Tier 5 — Advanced caching

| Prerequisite | Required |
|--------------|----------|
| Phase 4 of broader plan kicked off | Yes |
| Cross-zoom reuse prerequisites met (cache plan §3.4) | Yes |
| Predictive caching telemetry not built yet | Yes (still forbidden until telemetry exists) |

### 8.7 Tier 6 — Predictive behaviour

| Prerequisite | Required |
|--------------|----------|
| Telemetry infrastructure exists | Yes |
| Telemetry captures signals the predictive feature would use | Yes |
| The predictive feature is demonstrated to outperform the static doctrine order on fixtures | Yes |
| The feature is reversible to the static doctrine without code change | Yes |

Tier 6 is the most forward tier. None of its prereqs are satisfied
today; it is named only so future work can find the gate.

---

## 9. Anti-Overengineering

### 9.1 Explicitly rejected for Phase 1

| Pattern | Rejected because |
|---------|------------------|
| Microservices / service decomposition | One FastAPI backend serves; decomposition adds operational surface for no win |
| Distributed schedulers | Cache scheduler is per-tab, single-active; distributed coordination is YAGNI |
| Telemetry stack (Prometheus, OpenTelemetry, Datadog) | No telemetry surface today; building one is its own doctrine pass |
| Persistence layers (Redis, Postgres, SQLite) | Cache is per-session; persistence requires invalidation contract that doesn't exist |
| Predictive AI behaviour | Telemetry-gated; no telemetry exists |
| "Smart" hidden automation | Visible / inspectable computation is doctrine; smart-and-hidden violates it |
| Over-abstracted render pipelines | Two substrates, one adapter, two render functions. Abstracting to N substrates is YAGNI |
| Plugin systems | Same |
| CI/CD platform integration | Operator runs smokes; no platform infra to maintain |
| Feature-flag service | URL param + Python constant suffices |
| Authentication system | Cache is per-session; multi-user is its own doctrine pass |
| Server-side cache | Same |
| WebSocket / SSE for "real-time" cache | Cache is client-side and inspection-on-demand |
| Background-job queue infrastructure (Celery, RQ) | Per-tab JavaScript scheduler is sufficient |
| Database for chart profiles | Existing `/chart-profiles` JSON file is enough |
| Migration automation tools | Per-phase `git revert` is the migration toolchain |

### 9.2 Premature microservices

Any decomposition would require:

| Concern | Why we don't have it |
|---------|---------------------|
| Inter-service contracts | Not needed for single backend |
| Service discovery | Not needed |
| Distributed tracing | No telemetry |
| Service-level objectives | Not measured |
| Multi-process deployment | Single-process FastAPI runs locally; production deployment surface doesn't exist |

### 9.3 Distributed scheduler fantasies

| Idea | Why fantasy |
|------|-------------|
| Server-pushed cache entries | Browser is the cache host; push requires WebSocket; YAGNI |
| Multi-tab cache coordination | Per-tab cache is correct; cross-tab is unsolved invalidation |
| Distributed scheduler across users | Cache is per-chart; cross-user is per-user-identity which doesn't exist |
| Worker pool on the backend | `swe.houses` is fast enough; FastAPI handles concurrency |
| Edge-cached overlay tiles | Substrate is not tile-based; CDN cache wouldn't help |

### 9.4 Telemetry empires

| Empire | Why rejected |
|--------|--------------|
| Prometheus + Grafana dashboards | No metrics; no operator to read dashboards |
| Sentry / error-tracking integration | No aggregation surface |
| RUM | No telemetry infrastructure; privacy implications |
| Distributed tracing | Single backend |
| Time-series database for cache metrics | No time-series consumer |
| Anomaly detection ML | Speculative |
| User-behaviour analytics | No telemetry |

### 9.5 Persistence complexity

| Layer | Why deferred |
|-------|--------------|
| `localStorage` cache | Per-cache doctrine; invalidation contract unsolved |
| `IndexedDB` cache | Same |
| Server-side cache | No infra |
| Database for charts | `/chart-profiles` JSON is enough |
| User session persistence | No user identity |
| Cross-device sync | No infrastructure |

### 9.6 Speculative AI prediction systems

| System | Why rejected |
|--------|--------------|
| AI-suggested next condition combos | No telemetry to ground; speculative |
| AI-driven cache prefetch | Same |
| AI-driven pan/zoom prediction | Same |
| AI-driven city ranking before geocoder | Speculative; geocoder strategy is its own doctrine |

### 9.7 "Smart" hidden automation

| Pattern | Why rejected |
|---------|--------------|
| Auto-fallback to legacy if canonical errors | Forbidden by migration plan §2.4 |
| Auto-retry on cache miss | Cache miss is just a fetch; retry is a separate fetch |
| Auto-clean stale cache entries | No staleness in per-session cache |
| Auto-tune debounce based on user gestures | Speculative; static value works |
| Auto-tune adaptive depth based on viewport | Static substrate policy is correct; auto-tune is speculative |

### 9.8 Over-abstracted render pipelines

| Abstraction | Why rejected |
|------------|--------------|
| `IRenderer` interface with N implementations | Two substrates with one adapter is enough |
| `IClassificationSource` | Same |
| `ICache` with multiple backing stores | Single in-memory Map suffices |
| `IScheduler` with strategy pattern | One scheduler with one policy is enough |
| Render pipeline composed of N stages | Substrate is two-step: classify, paint |
| Renderer-pluggable substrate registry | YAGNI |

The pattern: each abstraction sounds small; each introduces a
surface that needs validating, documenting, and maintaining. The
substrate is **correct because it is small**. Growth is gated on
measured evidence.

---

## 10. Final Deliverable Statement

| Deliverable | Status |
|-------------|--------|
| Implementation protocol / doctrine document | **This document** |
| Production code change | **None** |
| Renderer rewrite | **None** |
| Aura implementation | **None** (out of scope) |
| Animation implementation | **None** (out of scope) |
| New endpoint | **None** |
| Astrology-math change | **None** |
| New smoke harness | **None** (planned in §3.2; landing happens in Phase 1.6 / 1.7) |

This document is the operational constitution. Implementation lands
in per-phase commits per §1, each governed by the commit doctrine
in §2 and the validation cadence in §3.

---

## 11. Discoveries While Grounding This Document

These were surfaced while reading the existing operational
infrastructure to write the protocol. Recorded so future work can
address them; this document does not solve them.

### 11.1 Existing meta-governance is mature and orthogonal

`docs/process/doctrine_review_cycle.md`, `decision_and_uncertainty_framework.md`, `ai_drift_audit_framework.md`, and `archaeology_and_synthesis_workflow.md` together form a coherent
meta-governance layer. This protocol composes with them; the
boundary is clear:

| They own | This doc owns |
|---------|--------------|
| Slow-vs-fast doctrine cadence | Commit-by-commit operational sequencing for Phase-C work |
| Tension preservation | Regression doctrine |
| AI interpretive behaviour | AI coding-collaboration behaviour |
| Memory / archaeology pipeline | Validation harness architecture |

No overlap, no contradiction. This doc cross-references the others;
they don't need to know about this one.

### 11.2 Three smokes + one validation harness + fourteen captures is the existing surface

The validation harness architecture (§3) is built around what
exists, not around invention. The three planned harnesses
(`smoke_substrate_parity.py`, `smoke_popup_overlay_parity.py`,
Phase-2 cache variants) are the minimum new surface required by the
migration plan; no further expansion is planned.

### 11.3 Commit style is short imperative; no prefixes

The repo's git log is uniformly short imperative subjects with no
conventional-commits prefixes, no Co-authored-by trailers, no AI
markers. This doc codifies that style rather than imposing a new
one. Future commits should match.

### 11.4 The protocol is the AI's coding-collaboration manual

§6 is the most operationally novel section of this doc. The
existing `ai_drift_audit_framework.md` governs interpretive AI;
this doc's §6 governs coding AI. The patterns rejected — speculative
confidence, mixed-purpose commits, mid-substrate aesthetic drift,
AI patch cascades — are *coding* patterns the operator has seen in
this very thread and elsewhere. The discipline this thread has
adopted is now written down.

### 11.5 Production readiness tiers are explicit

§8 names six tiers (operator dogfood → predictive behaviour). Most
discussions of "production ready" elide the tier distinction. The
six-tier ladder allows the operator to ship at the appropriate tier
without overshooting or undershooting.

### 11.6 Doctrine docs now form a complete Phase-C set

After this document lands, the Phase-C doctrine set is:

1. `docs/PHASE_C_RENDERING_ARCHITECTURE.md` — substrate charter
2. `docs/PHASE_C_CACHE_INTEGRATION_ARCHITECTURE.md` — cache plan
3. `docs/PHASE_C_PRODUCTION_MIGRATION_PLAN.md` — migration plan
4. `docs/PHASE_C_IMPLEMENTATION_PROTOCOL.md` — operational
   constitution (this doc)

Together they define what the substrate is (1), how it caches (2),
how it lands in production (3), and how that landing is operated
(4). No fifth doctrine doc is required to begin Phase 1.

---

## 12. Recommended Next Implementation Step

**Phase 1.1 — Documentation alignment**, specifically:

1. Add the substrate-path decision sentence to `ai_context/decisions.md` (exact wording in migration plan §3 Phase 0 Step 0.1).
2. Update `ai_context/current_state.md` to reference the four Phase-C doctrine docs as authoritative.
3. Update `docs/DOCTRINE_INDEX.md` to list the four Phase-C docs.
4. Update `docs/CURRENT_RENDERING_DOCTRINE.md` to cite the implementation protocol as the operating manual.

These are doc-only changes. Smokes will be untouched. Reverting any
one of the four is trivial. After Phase 1.1, Phase 1.2 (archaeology
fencing) is the smallest reversible code commit; per §2.5, only
land Phase 1.2 if all smokes are green and Phase 1.1 is
already-merged.

After Phase 1.1 lands, the Phase-C implementation is unblocked. Each
subsequent phase composes onto the previous with its own gate, its
own rollback scope, and its own "done means" definition.

---

## 13. Document Provenance

| Field | Value |
|------|------|
| Author surface | Architecture draft, this conversation |
| Reviewed against | Three preceding Phase-C docs; `docs/process/*`; `ai_context/memory_workflow.md`; `ai_context/decisions.md`; `current_state.md`; existing smokes; git log |
| Authority on conflict | Slow doctrine (`doctrine_review_cycle.md` policy), then Phase-C doctrine chain, then this doc |
| Yields to | All existing meta-governance docs |
| Supersedes | Nothing |
| Operationalises | Phase-C charter §10; migration plan §3; cache plan §10 |
| Status | Design only; no code authorised |

This is the operational constitution for Phase-C implementation.
The constitution is short, specific, anchored in measured evidence,
and composes with — does not replace — the existing institutional
discipline. Future Phase-C implementation work cites this document
as the operating manual.
