# COMPARISON UX — Active Roadmap

**Workstream:** Comparison UX & reading-state persistence  
**Status:** ACTIVE  
**Date:** 2026-06-18  
**Supersedes:** WEB2_COMPLETION “Comparison Intake UX” row (facts portion)  
**Truth audit:** `results/95_comparison_workflow_truth_audit.md`  
**Revision:** `results/96_comparison_roadmap_revision_post_cux1.md`

---

## Executive Summary

Comparison **backend is done** (create, archive, notes, order, hydration, routing, bridge). Remaining work is **UX completion** and **bookmark-style workspace restore** via `settings_snapshot_json`.

This is not a greenfield backend project.

---

## Decisions (Binding)

### Unified Search Doctrine

1. **General Location Search** — birth, current, relocated, general city. Sources: places DB, GeoNames, custom places. **Not favorites.**
2. **Saved Location Search** — map bar, comparison add, overlay, future builders. Sources: favorites + custom saved + place search in one UI.

### Persistence V1 (Option B)

Restore reading state on reopen using `settings_snapshot_json`. Bookmark, not Photoshop. No generic workspace engine.

---

## Slice Queue

### C-UX-1 ✅ Truth audit

- **Closeout:** `results/95_comparison_workflow_truth_audit.md`
- **Verdict:** Backend substantially complete; gaps are overlay, unified search, snapshot, smokes

### C-UX-2 — Persistence foundation (NEXT)

**Goal:** Saved comparison feels like returning to a workspace.

**Deliver:**

- `settings_snapshot_json` schema (versioned document)
- Write snapshot on explicit save and/or meaningful UI state change (define minimal triggers)
- Restore on open saved comparison
- State fields: locations/order (sync with DB), notes pointer, collapsed/visible sections, active angle tab, diff toggle (no engine), dignity placeholder (no engine), column visibility
- Extend owned create/update path if needed — **no schema expansion** unless unavoidable
- Smokes: save snapshot → reload → assert restored UI flags

**Stop.** No overlay. No unified search component.

### C-UX-3 — Unified search architecture

**Goal:** Reusable **Saved Location Search** for map, comparison, overlay.

**Deliver:**

- Shared search service merging: active profile favorites, custom saved places, `GET /places/search`
- Ranking: favorites first, then backend results
- Reusable component (adapter from `place_search_client.js` / `current_location_editor.js` patterns)
- Smokes: favorites filter + GeoNames result merge

**Stop.** No full comparison overlay.

### C-UX-4 — Comparison overlay

**Goal:** Chrome/profile compare entry matches product doctrine.

**Deliver:**

- Overlay on compare entry when no valid workspace
- **New Comparison** / **Saved Comparisons** / **Open** / **Archive**
- **Add Location** with unified search (C-UX-3)
- 2–5 location enforcement; max warning on exceed only
- Selected chips visible (no redundant counter)
- Do not auto-pick first saved set on chrome nav without user intent

**Stop.** No diffs. No dignities.

---

## Guardrails

| Rule | |
|------|---|
| No comparison diffs implementation | Toggle state only in snapshot |
| No dignity implementation | Placeholder keys only |
| No ranking/recommendation/analytics | |
| No schema expansion | Unless strictly required |
| Use existing `comparison_sets` | Prefer `settings_snapshot_json` over new tables |
| Ownership + smokes | Every slice |

---

## Out of Scope (This Roadmap)

- Comparison diffs engine (P3 / separate spec)
- Dignities layer on comparison surface
- Rename / post-create place membership (optional follow-on after C-UX-4)
- `last_opened_at` column (optional product slice)
- v5 full layout port (collapsible blocks, angle tabs UI) — may overlap C-UX-2 restore targets

---

## Dependencies

| Slice | Depends on |
|-------|------------|
| C-UX-2 | C-UX-1 audit |
| C-UX-3 | A3 place search (done) |
| C-UX-4 | C-UX-2 (restore), C-UX-3 (search) |

---

## Smoke Baseline

| Script | Status |
|--------|--------|
| `smoke_comparison_sets.py` | Create, archive, picker build |
| `smoke_app_shell_context_transport.py` | Chrome compare + returnTo |
| `smoke_app_shell_map_handoff.py` | Compare context on map |

**Gaps to close in C-UX-2:** open saved set, snapshot round-trip, column order assertion.

---

## WEB2 Cross-Reference

WEB2_COMPLETION remains parent track for shell/settings/onboarding/export. Comparison UX detail lives **here** until this roadmap moves to `completed/`.
