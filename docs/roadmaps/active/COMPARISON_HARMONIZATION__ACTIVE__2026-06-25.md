# Comparison Harmonization — Active Roadmap

**Workstream:** Comparison visual harmonization (H4)  
**Status:** ACTIVE  
**Date:** 2026-06-25  
**Executor contract:** `relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md`  
**Checkpoint:** `checkpoint/h4b_start_clean` (`e37bf9d`) — do not use `5f76990`

## Scope

Port `comparison_v5_beta.html` bottled layout onto live `app_shell.html` `#/compare` route **without** changing backend, hydration, or frozen Profile/Relocated surfaces.

## Slice queue

| ID | Slice | Status |
|----|-------|--------|
| H4B-1 | Authority system (header, cmp-zone-b, city bar) | ✅ `e37bf9d` |
| H4-2 | AIS bottled shell | NEXT |
| H4-3 | PIH bottled shell | pending |
| H4-4 | A2A bottled shell | pending |
| H4-5 | Notes rail | pending |
| H4-6 | CI shell (placeholder content) | pending |
| H4-7 | Freeze audit (read-only) | pending |

## Out of scope

Map, Settings, Auth, backend, wheel colors, visual redesign, cleanup/refactors.

