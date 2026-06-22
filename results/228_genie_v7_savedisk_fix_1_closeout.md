# 228 — GENIE-V7-SAVEDISK-FIX-1 Closeout

**Date:** 2026-06-22  
**Ticket:** GENIE-V7-SAVEDISK-FIX-1  
**Target:** `map_SANDBOX_genie_v7.html` only (per corrected MOTION-QA-1)  
**Status:** **DONE**

---

## Summary

Fixed `flySave(true)` completion handler: `#saveDisk` no longer retains inline `opacity: 0` after the pill→disk morph. Cleanup now mirrors the `flySave(false)` branch.

**Change (one line):** in `flySave(true)` `setTimeout` completion, add `disk.style.opacity=''` alongside existing `disk.style.transition=''` restore.

No FLIP architecture changes. `map_CURRENT.html` untouched. No production/sandbox chrome crossover.

---

## Root cause

`flySave(true)` set `disk.style.opacity='0'` for ghost measurement/morph, then on completion cleared `pill.style.visibility` and `disk.style.transition` but **never cleared inline opacity**. CSS `body.explore .save-disk { opacity:1 }` cannot win while inline `opacity:0` remains.

`flySave(false)` already had `disk.style.opacity=''` in its completion handler.

---

## Validation

```text
python3 scripts/motion_visual_qa_genie_v7.py
→ 11/11 PASS, recommendation: READY FOR HUMAN QA
```

**Post-fix spot check (Playwright):** after `doSearch()`, at ~4s `#saveDisk` inline opacity is cleared and computed opacity animates to **1** via explore CSS transition; at 3s (pre-cleanup) opacity is still 0 during morph — expected.

Scenario 4 QA detail may still flag `disk_opacity_stuck_zero` at its 3000ms sample (before morph completes at ~3740ms); scenario pass criteria are explore + morph, not disk-at-rest timing.

---

## Files changed

| File | Change |
|------|--------|
| `map_SANDBOX_genie_v7.html` | `flySave(true)` cleanup clears `disk.style.opacity` |

---

## Rollback

Revert the single-line change in `flySave(true)` completion `setTimeout`.
