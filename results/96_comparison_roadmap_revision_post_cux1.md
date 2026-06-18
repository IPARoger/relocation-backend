# Comparison Roadmap Revision (Post C-UX-1)

**Date:** 2026-06-18  
**Mode:** Planning — implementation authorized only after truth report  
**Truth report:** `results/95_comparison_workflow_truth_audit.md` (C-UX-1)  
**Active roadmap:** `docs/roadmaps/active/COMPARISON_UX__ACTIVE__2026-06-18.md`

---

## Audit Conclusions (Binding)

The comparison **backend is substantially complete**. This is **not** a backend construction project.

**Done today:**

- `comparison_sets` + `comparison_set_places` tables
- Ownership enforcement (JWT → repository → RLS)
- Save (create) / open / archive
- Notes persistence (`notes` table)
- Place ordering (`sort_order`)
- Hydration on reopen (`hydrateComparisonColumns` + `/relocated-chart`)
- Hash routing + store bridge

**Remaining work:** UX completion + **reading-state persistence** via `settings_snapshot_json`.

---

## Decision 1 — Unified Search Doctrine

Two search families. Do not merge them.

### A. General Location Search

**Used for:** Birth place, current location, relocated location, general city search.

**Sources:** Places database, GeoNames, custom places.

**Not favorites.** Birth and chart locations are locations, not saved destinations.

### B. Saved Location Search

**Used for:** Map search bar, comparison add-location, comparison overlay, future investigation builders, future road trip mode.

**Sources:** Favorites, saved custom places, general place search (merged in one UI).

**Doctrine:** Single unified saved-location experience. Favorites are first-class reusable destinations.

**C-UX-3** owns the shared service/component. Comparison overlay (C-UX-4) consumes it.

---

## Decision 2 — Comparison Persistence V1 (Option B)

Reopening a saved comparison restores **working reading state**, not arbitrary layout.

**Vehicle:** `comparison_sets.settings_snapshot_json` (existing column; currently unused on owned create).

**Persist (bookmark, not Photoshop):**

| State | Notes |
|-------|-------|
| Selected locations | Align with `comparison_set_places` or snapshot mirror |
| Location order | Already in DB; snapshot may echo for UI sync |
| Notes | Already in `notes` table; may duplicate pointer in snapshot |
| Collapsed sections | Reading state |
| Visible sections | Reading state |
| Active angle tab | Reading state |
| Diff mode state | Toggle only — **no diff engine** in guardrail phases |
| Future dignity state | Placeholder key only — **no dignity engine** |
| Column visibility | Reading state |

**Do NOT persist:**

- Arbitrary layouts, pixel positions, drag geometry, dashboard arrangements

**Do NOT build:** Generic workspace engine.

**C-UX-2** owns state model + save/restore plumbing + smokes.

---

## Implementation Order (Stop After Each Slice)

| ID | Slice | Deliver | Stop |
|----|-------|---------|------|
| **C-UX-1** | Truth audit | `results/95_*` | ✅ Done |
| **C-UX-2** | Persistence foundation | `settings_snapshot_json` usage, state model, save/restore plumbing, smokes | Stop |
| **C-UX-3** | Unified search architecture | Shared search service, favorites + custom + `/places/search`, reusable component | Stop |
| **C-UX-4** | Comparison overlay | Open / New / Saved / Archive, Add Location, unified search integration | Stop |

**Deferred (explicitly out of scope for C-UX-2..4):**

- Comparison diffs implementation
- Dignity implementation
- Ranking / recommendation / analytics
- Schema expansion unless strictly required for snapshot or search

---

## Guardrails

- Use existing `comparison_sets` infrastructure wherever possible
- Maintain ownership enforcement on all writes
- Maintain read-budget discipline
- Smoke coverage required for every phase
- No new comparison analytics
- Rename / post-create place membership may follow C-UX-4 if product requires — not bundled into C-UX-2 unless snapshot demands it

---

## Corrections to Prior Docs

| Doc | Stale claim | Correction |
|-----|-------------|------------|
| `results/85_web2_completion_audit.md` | Comparison facts mocked | Facts are live via `hydrateComparisonColumns` |
| `docs/architecture/OPERATIONAL_SMOKE_TESTS.md` | Placeholder comparison text | Update in C-UX-2 truth-sync subtask |
| `WEB2_COMPLETION` P2 | “Mocked placeholder text” | Superseded by COMPARISON_UX roadmap |

---

## Verdict

**Authorize C-UX-2** as next implementation slice. Backend construction is complete; proceed with persistence foundation before overlay or unified search UI.
