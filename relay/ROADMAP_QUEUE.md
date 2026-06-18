# ROADMAP QUEUE — 5-Chat Architecture Track (binding)

Planner: propose the **first incomplete item** below. One objective per task.
Put `**Roadmap ID:** C?_?` in every task header. Reference closeout in results/.

**Product features** (port 8000, city search, Notes UI, etc.) are **after Chat 5** — do not plan them until this queue is done.

**Status (2026-06-18):** Chat 4 **COMPLETE**. Chat 5 **READY** (CURRENT). Closure commits: `aeaaa6d` (C4-1), `8a934d9` (C4-2 M2). See `results/75_c4_1_*`, `results/76_c4_2_m2_*`, closure audit in `results/73_*` / `results/74_*`.

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

## Chat 5 — Dead Code Retirement & Cleanup ▶ READY (CURRENT)

Chat 4 complete — resume incremental cleanup per C5-1 audit. One slice per task.

| ID | Status | Item | Closeout |
|----|--------|------|----------|
| C5-1 | ✅ | Dead code audit | `results/68_c5_1_*` |
| C5-2 | ⏸ | Remove dead helpers — **NOT VERIFIED** (24 shim callers) | `results/69_*` |
| C5-2a | ✅ | Narrow removal — 6 dead functions | `results/69b_*` |
| C5-3 | ⏸ | Bridge helpers — **NOT VERIFIED** (live internal callers) | `results/70_*` |
| C5-4 | ✅ | Legacy map audit (read-only) | `results/71_*` |
| C5-4a | ✅ | Quarantine `renderBellAuraBandsAroundLine` (partial) | `results/72_*` |
| C5-5+ | **NEXT** | Further cleanup per C5-1 priority — confirmed-dead only | closeout C5-N |

**Do not touch:** `_deprecated_legacy_write`, LIVE renderer (`LEGACY_SEARCH_REGIONS`), bridge helpers used by `buildSupabaseStore` / `refreshProfile`.

---

## After Chat 5 → Product track

Settings completion, saved comparisons UX, Help/onboarding, exports, city search, port 8000 migration — see `docs/architecture/ROADMAP_AND_SEQUENCE.md`.

---

## Planner rules

1. **Chat 5 is CURRENT.** Resume C5-5+ per C5-1 audit priority. Do not retry C5-2/C5-3 without new task spec.
2. One slice per task — do not bundle.
3. Always grep production UI + ownership smokes before quarantining or deleting.
4. If active caller found → PAUSE, cite route.
5. Honest VERIFIED / NOT VERIFIED in every closeout.
6. Size S → Haiku; M/L → Sonnet (via RELAY_AUTO_MODEL) when planner API is used.
