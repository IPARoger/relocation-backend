# TASK: H4-7

**Roadmap ID:** 85_h4_slice7_freeze_audit
**Status:** Authorized — execute exactly one slice, then stop.

## Objective
Produce `COMPARISON_FREEZE_AUDIT.md` read-only (no product code changes unless audit file only).

## Authority
- `relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md`
- Rollback: `checkpoint/h4b_start_clean` (`e37bf9d`)
- On smoke failure: `git reset --hard e37bf9d` and STOP with NOT VERIFIED closeout.

## Scope
Comparison surface (`app_shell.html`) shell/CSS/DOM only. Do not touch frozen surfaces or backend.

## Mode
READ ONLY audit doc. No app_shell changes.

## Validation
```bash
test -f COMPARISON_FREEZE_AUDIT.md
```

## Commit (when VERIFIED)
```
docs: comparison freeze audit (H4 slice 7)
```

## Closeout
Write `results/H4-7.md` with VERIFIED or NOT VERIFIED. Commit product changes. Send Telegram via relay_notify if available.
