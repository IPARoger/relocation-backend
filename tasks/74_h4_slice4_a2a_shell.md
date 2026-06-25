# TASK: H4-4

**Roadmap ID:** 74_h4_slice4_a2a_shell
**Status:** Authorized — execute exactly one slice, then stop.

## Objective
Add A2A bottled block shell around existing `renderA2aComparisonHtml`. Preserve `data-a2a-shape="matrix"`.

## Authority
- `relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md`
- Rollback: `checkpoint/h4b_start_clean` (`e37bf9d`)
- On smoke failure: `git reset --hard e37bf9d` and STOP with NOT VERIFIED closeout.

## Scope
Comparison surface (`app_shell.html`) shell/CSS/DOM only. Do not touch frozen surfaces or backend.

## Critical
Preserve `smoke_comparison_a2a_matrix.py` guards. Do not change matrix data logic.

## Validation
```bash
python3 scripts/smoke_h4_slice4_a2a_shell.py
python3 scripts/smoke_h4_slice3_pih_shell.py
python3 scripts/smoke_h4b_comparison_authority.py
python3 scripts/smoke_comparison_a2a_matrix.py
```

## Commit (when VERIFIED)
```
comparison: add A2A bottled block shell (H4 slice 4)
```

## Closeout
Write `results/H4-4.md` with VERIFIED or NOT VERIFIED. Commit product changes. Send Telegram via relay_notify if available.
