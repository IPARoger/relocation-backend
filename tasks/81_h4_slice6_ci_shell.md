# TASK: H4-6

**Roadmap ID:** 81_h4_slice6_ci_shell
**Status:** Authorized — execute exactly one slice, then stop.

## Objective
Add City Intelligence collapsible shell only (placeholder content OK, `wired: false`).

## Authority
- `relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md`
- Rollback: `checkpoint/h4b_start_clean` (`e37bf9d`)
- On smoke failure: `git reset --hard e37bf9d` and STOP with NOT VERIFIED closeout.

## Scope
Comparison surface (`app_shell.html`) shell/CSS/DOM only. Do not touch frozen surfaces or backend.

## May NOT
Wire CI content engine or backend.

## Validation
```bash
python3 scripts/smoke_h4_slice6_ci_shell.py
python3 scripts/smoke_h4_slice5_notes_rail.py
python3 scripts/smoke_h4b_comparison_authority.py
```

## Commit (when VERIFIED)
```
comparison: add location intelligence shell (H4 slice 6)
```

## Closeout
Write `results/H4-6.md` with VERIFIED or NOT VERIFIED. Commit product changes. Send Telegram via relay_notify if available.
