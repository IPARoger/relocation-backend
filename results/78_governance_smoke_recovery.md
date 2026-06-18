# RESULT: 78_governance_smoke_recovery

**Roadmap ID:** Recovery Prompt 1
**Date:** 2026-06-18

## Files Changed

| File | Change |
|------|--------|
| `relay/ROADMAP_QUEUE.md` | Synced to audit reality: Chat 1–3 COMPLETE, Chat 2 process gaps noted, Chat 4 PARTIAL (C4-1 + C4-2 M2 OPEN), Chat 5 PAUSED |
| `relay/CHAT_INSTRUCTIONS.md` | Replaced placeholder with planner discipline rules |
| `scripts/smoke_favorites.py` | Clear `console_errors` + networkidle settle before shell phase |
| `scripts/smoke_comparison_sets.py` | `fe_compare_recovery`: `not broken` instead of `broken is False` |

## Smoke Results

| Script | Exit | Result |
|--------|------|--------|
| `smoke_favorites.py` | 0 | 17/17 PASS (incl. `fe_shell_no_console_errors`) |
| `smoke_comparison_sets.py` | 0 | 13/13 PASS (incl. `fe_compare_recovery`) |
| `smoke_legacy_writes_deprecated.py` | 0 | 25/25 PASS |

## Governance Updates

- **ROADMAP_QUEUE.md:** Removed stale "Chat 2 CURRENT"; marked C4-1 and C4-2 M2 OPEN; listed completed C4-3..C4-7 and partial Chat 5 status.
- **CHAT_INSTRUCTIONS.md:** One slice per commit, roadmap ID required, grep-before-delete, smoke gates, honest commits, no megacommits, hard stops for renderer and `_deprecated_legacy_write`.

## Diagnosis confirmed

- **smoke_favorites:** Map-phase `Failed to fetch` was timing/buffer bleed into shell assertion — fixed by settle + `console_errors.clear()`.
- **smoke_comparison_sets:** Healthy `comparisonSetId: null` returned JS `null` → Python `None`; `broken is False` incorrectly failed.

## Status

**VERIFIED**
