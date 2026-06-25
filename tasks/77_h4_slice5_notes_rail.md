# TASK: H4-5

**Roadmap ID:** 77_h4_slice5_notes_rail
**Status:** Authorized — execute exactly one slice, then stop.

## Objective
Port comparison notes rail shell; move existing notepad + `saveComparisonSetNote` into rail layout.

## Authority
- `relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md`
- Rollback: `checkpoint/h4b_start_clean` (`e37bf9d`)
- On smoke failure: `git reset --hard e37bf9d` and STOP with NOT VERIFIED closeout.

## Scope
Comparison surface (`app_shell.html`) shell/CSS/DOM only. Do not touch frozen surfaces or backend.

## May NOT
Change notes API or storage.

## Validation
```bash
python3 scripts/smoke_h4_slice5_notes_rail.py
python3 scripts/smoke_h4_slice4_a2a_shell.py
python3 scripts/smoke_h4b_comparison_authority.py
```

## Commit (when VERIFIED)
```
comparison: add notes rail shell (H4 slice 5)
```

## Closeout
Write `results/H4-5.md` with VERIFIED or NOT VERIFIED. Commit product changes. Send Telegram via relay_notify if available.
