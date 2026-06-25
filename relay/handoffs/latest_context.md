# Latest relay context

**Updated:** 2026-06-25 (H4 autonomous comparison harmonization)

## Active executor plan

`relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md`

## Safety checkpoint

| | |
|--|--|
| **Tag** | `checkpoint/h4b_start` |
| **SHA** | `5f76990c73b45bbddf055aeb31e6dd76d998c242` |
| **Reset** | `git reset --hard checkpoint/h4b_start` on any smoke failure |

## Current position

| Slice | Status | Commit |
|-------|--------|--------|
| H4B Slice 1 — Authority (beta header, cmp-zone-b, city bar) | ✅ DONE | `e37bf9d` |
| H4 Slice 2 — AIS bottled shell | ⏳ NEXT | — |
| H4 Slice 3 — PIH shell | pending | — |
| H4 Slice 4 — A2A shell | pending | — |
| H4 Slice 5 — Notes rail | pending | — |
| H4 Slice 6 — CI shell | pending | — |
| H4 Slice 7 — Freeze audit (read-only) | pending | — |

## Frozen (do not touch)

- Profile (`rm-beta-profile`)
- Relocated (`rm-beta-relocated`)
- Backend, `/relocated-chart`, comparison set APIs
- Map, Settings, Auth, wheel colors

## Doctrine sources

- `comparison_v5_beta.html` (canonical mockup)
- `COMPARISON_VISUAL_ARCHAEOLOGY.md`
- `COMPARISON_RENDERER_OWNERSHIP_AUDIT.md`
- `COMPARISON_IMPLEMENTATION_READINESS.md`

## Start command

```
Execute H4 relay plan from relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md
Start Slice 2. Checkpoint checkpoint/h4b_start.
```

