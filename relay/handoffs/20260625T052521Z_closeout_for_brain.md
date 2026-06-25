# Closeout ingested for next Claude/GPT plan

This replaces pasting Cursor output back into Claude by hand.
On the next `relay_robot.py` plan step, this file is included in the context pack.

## Source: results/99_cux4_comparison_overlay.md

# C-UX-4 — Comparison Overlay

**Status:** Verified  
**Date:** 2026-06-18

## Overlay Architecture

Chrome **Compare** nav opens `#comparisonOverlayModal` (modal-backdrop pattern shared with onboarding). Profile entry path unchanged: Chart Record → `data-nav="compare"` lands on Screen 5 picker without overlay.

Auto-pick of first saved comparison set removed from `normalizeNavContext`.

## Saved Comparison Section

Lists active `comparison_sets` for the selected profile: **name**, **last updated**, **location count**. Actions: **Open** (navigate to workspace + C-UX-2 restore), **Archive** (POST `/comparison-sets/archive`). Shared list renderer with Chart Record module (`renderComparisonSetsListHtml` / `wireComparisonSetListActions`).

## New Comparison Section

Family B search via `RMSavedLocationSearchUI.mount()` on `#rm-cmp-overlay-search-mount`. Empty focus shows favorites + teaching locations (Rome, Bali). Selected chips in `#rm-cmp-overlay-selected`. **Compare** creates set via shared `createComparisonSetFromPlaceIds()` with workspace defaults, then opens Screen 5.

## Family B Integration

Reuses C-UX-3 service/UI. Overlay enables `includeTeaching: true` and ★ Favorite badge formatting. Teaching rows resolve through GeoNames on select.

## Selection Limits

2–5 locations. Compare disabled below 2. Sixth add shows **Maximum 5 locations** (no counter).

## Component Reuse

- `createComparisonSetFromPlaceIds` — overlay + Screen 5 build
- `archiveComparisonSet` — overlay + Chart Record module
- `addComparisonPick(hostId, msgId)` — overlay + Screen 5 chips

## Validation

`scripts/smoke_comparison_sets.py` — PASS (overlay chrome open, Family B, compare enabled, max-5 block, open saved → workspace restore + existing C-UX-2/3 checks).

## Verdict

**VERIFIED** — Chrome Compare entry completes the comparison workflow without requiring Profile first.
