# Latest relay context

**Updated:** 2026-06-25 (checkpoint corrected)

## Active executor plan

`relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md`

## Safety checkpoint (CLEAN)

| | |
|--|--|
| **Tag** | `checkpoint/h4b_start_clean` |
| **SHA** | `e37bf9d6d572973e9b4f834ed084cd2f39878fff` |
| **Reset** | `git reset --hard e37bf9d` on any smoke failure |

**Do not use** commit `5f76990` or tag `checkpoint/h4b_start` — dirty accidental `git add -A` (removed from history).

## Current position

| Slice | Status | Commit |
|-------|--------|--------|
| H4B Slice 1 — Authority | ✅ DONE | `e37bf9d` |
| H4 Slice 2 — AIS bottled shell | ⏳ NEXT | — |
| H4 Slice 3–7 | pending | — |

## Relay docs commit

`61d48a7` — relay contract (on top of `e37bf9d`; safe to keep during Slice 2+)

## Start command

```
Execute H4 relay plan from relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md
Start Slice 2. Checkpoint: e37bf9d (checkpoint/h4b_start_clean).
On smoke failure: git reset --hard e37bf9d and STOP.
```
