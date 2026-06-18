# ROADMAP QUEUE — 5-Chat Architecture Track (binding)

Planner: propose the **first incomplete item** below. One objective per task.
Put `**Roadmap ID:** C?_?` in every task header. Reference closeout in results/.

**Product track** (port 8000, city search, Notes UI, settings completion, etc.) is **CURRENT** — see `docs/architecture/ROADMAP_AND_SEQUENCE.md`.


## ROADMAP GOVERNANCE

* Multiple ACTIVE roadmaps are allowed.
* Only one ACTIVE roadmap may exist per workstream.
* Active roadmaps live in `docs/roadmaps/active/`
* Completed roadmaps move to `docs/roadmaps/completed/`
* Use naming convention: `<ROADMAP_NAME>__<STATUS>__<YYYY-MM-DD>.md`
* Never create `roadmap_v2.md`, `roadmap_new.md`, `final.md`, `roadmap-final-final.md`, etc.
* Most recent roadmap for a workstream is authoritative.

See `docs/roadmaps/ROADMAP_INDEX.md` for the full registry.

**Status (2026-06-18):** Chats 1–5 **COMPLETE**. Cleanup track **CLOSED**. Product track **CURRENT**. Chat 5 closure: `3bb5905` (C5-6), governance sync per `results/82_chat5_closure_audit.md`.

---

## Chat 1 — Backend Ownership Migration ✅ COMPLETE

JWT write routes live. Browser → JWT → Repository → RLS.

Done: profiles CRUD/archive, favorites, comparison sets, saved investigations, places resolve-or-create, GET /profiles hardening, POST /places → 410, library scaffold default-off.

**No new Chat 1 tasks** unless regression found.

---

## Chat 2 — Legacy Route Retirement ✅ COMPLETE (process caveat retained)

**Goal:** 410-quarantine legacy **service-role write** routes the production UI no longer uses.

**Verified:** C2-7 smoke gate — 25/25 legacy writes return 410; ownership smokes pass (`results/57_c2_7_*`).

**Process debt (non-blocking):** Per-family closeouts C2-3..C2-6 were bundled into C2-7 rather than individual closeout files. Functionally complete.

| ID | Status | Item |
|----|--------|------|
| C2-1 | ✅ | Audit legacy write routes |
| C2-2 | ✅ | 410 quarantine profiles legacy writes |
| C2-3 | ✅ | 410 quarantine saved-searches legacy writes (bundled) |
| C2-4 | ✅ | 410 quarantine comparison-sets legacy writes (bundled) |
| C2-5 | ✅ | 410 quarantine favorite-places legacy writes (bundled) |
| C2-6 | ✅ | 410 quarantine notes legacy writes (bundled) |
| C2-7 | ✅ | Smoke gate — all legacy writes 410 |

---

## Chat 3 — Read Path Consolidation Audit ✅ COMPLETE

| ID | Status | Item | Closeout |
|----|--------|------|----------|
| C3-1 | ✅ | Read path inventory | `results/59_c3_1_closeout.md` |
| C3-2 | ✅ | Read-path architecture plan | `results/60_c3_2_read_path_plan.md` |

**Audit only — implementation was Chat 4.**

---

## Chat 4 — Read Path Simplification ✅ COMPLETE

Executed Chat 3 plan (`results/60_c3_2_read_path_plan.md`). All seven slices verified. No direct Supabase reads remain in `app_shell.html` or `map_CURRENT.html`.

**Closure commits:** `aeaaa6d` (C4-1), `8a934d9` (C4-2 M2). Recovery gate: `bd4100a`.

| ID | Status | Item | Closeout |
|----|--------|------|----------|
| C4-1 | ✅ | `planProfileArchive` → `SupabaseStore.clients` + `SupabaseStoreReady` | `results/75_c4_1_*` (`aeaaa6d`) |
| C4-2 M2 | ✅ | Geonames lookup → `GET /places/search?geonames_id=` | `results/76_c4_2_m2_*` (`8a934d9`) |
| C4-2 M5 | ✅ | Handoff centering → `GET /place/{id}` | `results/62_c4_2_*` |
| C4-3 | ✅ | `GET /favorites` + map M3/M4 migration | `results/63_c4_3_*` |
| C4-4 | ✅ | `GET /saved-investigations/{id}` + map M1 | `results/64_c4_4_*` |
| C4-5 | ✅ | `refreshProfile()` in bridge + app_shell A2 | `results/65_c4_5_*` |
| C4-6 | ✅ | `comparison_sets` in bridge + app_shell A1 | `results/66_c4_6_*` |
| C4-7 | ✅ | 410 dead GET routes (4 routes) | `results/67_c4_7_*` |

**No new Chat 4 tasks** unless regression found.

---

## Chat 5 — Dead Code Retirement & Cleanup ✅ COMPLETE

Incremental cleanup per C5-1 audit. All approved slices verified. **Cleanup track CLOSED.**

**Closure commits:** `75a3443` (C5-5), `3bb5905` (C5-6). **Closure audit:** `results/82_chat5_closure_audit.md`.

| ID | Status | Item | Closeout |
|----|--------|------|----------|
| C5-1 | ✅ | Dead code audit | `results/68_c5_1_*` |
| C5-2 | ⏸ BLOCKED | Remove dead helpers — live shim callers (`_deprecated_legacy_write`) | `results/69_*` |
| C5-2a | ✅ | Narrow removal — 6 dead functions | `results/69b_*` |
| C5-3 | ⏸ BLOCKED | Bridge helpers — live internal callers | `results/70_*` |
| C5-4 | ✅ | Legacy map audit (read-only) | `results/71_*` |
| C5-4a | ✅ | Quarantine `renderBellAuraBandsAroundLine` (partial) | `results/72_*` |
| C5-5 | ✅ | Remove `orb_defaults` legacy mirror write (`app_shell.html`) | `results/79_*` |
| C5-6 | ✅ | Remove unused back-compat `state` proxy (`app_shell.html`) | `results/80_*` |

**Closure notes:**
- C5-2 blocked by live callers (25 legacy-write 410 shims) — do not retry without new approved roadmap spec.
- C5-3 blocked by live callers (`buildSupabaseStore` / `refreshProfile`) — do not retry without new approved roadmap spec.
- No remaining required cleanup slices. Candidate audit: `results/81_c5_7_candidate_audit.md` (read-only; no implementation slice).

**Do not touch (if cleanup is ever reopened):** `_deprecated_legacy_write`, LIVE renderer (`LEGACY_SEARCH_REGIONS`), bridge helpers used by `buildSupabaseStore` / `refreshProfile`.

---

## Product track ▶ CURRENT

Settings completion, saved comparisons UX, Help/onboarding, exports, city search, port 8000 migration — see `docs/architecture/ROADMAP_AND_SEQUENCE.md`.

| ID | Status | Item | Closeout |
|----|--------|------|----------|
| S-UX-1 | ✅ | Settings IA shell + Charts regroup + About & Data Sources (`app_shell.html`) | `results/91_sux1_settings_ia_shell.md` |
| S-UX-1C | ✅ | Settings subpage router (`#/settings/{sub}`) | `results/94_sux1c_settings_subpage_router.md` |
| S-UX-2 | ✅ | Guided onboarding overlay — 7-slide app tour (`app_shell.html`) | `results/92_sux2_onboarding_overlay.md` |

### Comparison UX (workstream: `COMPARISON_UX__ACTIVE__2026-06-18.md`)

| ID | Status | Item | Closeout |
|----|--------|------|----------|
| C-UX-1 | ✅ | Comparison workflow truth audit | `results/95_comparison_workflow_truth_audit.md` |
| C-UX-2 | ✅ | Comparison workspace state via `settings_snapshot_json` | `results/97_cux2_comparison_workspace_state.md` |
| C-UX-3 | ✅ verified 2026-06-18 | ✅ | Unified saved-location search architecture | `results/98_cux3_unified_saved_location_search.md` |
| C-UX-4 | ✅ verified 2026-06-18 | Comparison overlay (New / Saved / unified search) | — |



---

## Planner rules

1. **Product track is CURRENT.** Architecture chats 1–5 are **COMPLETE**; cleanup track is **CLOSED**. Do not reopen C5-2 or C5-3 without a new approved roadmap specification.
2. One slice per task — do not bundle.
3. Always grep production UI + ownership smokes before quarantining or deleting.
4. If active caller found → PAUSE, cite route.
5. Honest VERIFIED / NOT VERIFIED in every closeout.
6. Size S → Haiku; M/L → Sonnet (via RELAY_AUTO_MODEL) when planner API is used.
