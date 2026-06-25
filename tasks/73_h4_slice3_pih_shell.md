# TASK: 73_h4_slice3_pih_shell

**Author:** relay handoff (H4 autonomous comparison plan)
**Roadmap ID:** H4-3
**Status:** Authorized — execute now

## Objective

Add the PIH bottled block shell on `#/compare` (H4 Slice 3 only): collapsible `cmp-block` chrome around existing `renderPihComparisonHtml` output.

## Authority

Read and obey:
- `relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md` (Slice 3 section)
- `validation/mockups/beta/comparison_v5_beta.html` (mockup `#pih` block)
- Rollback anchor: `checkpoint/h4b_start_clean` (`e37bf9d`)

## Scope

- Comparison surface only (`app_shell.html` compare route/CSS/DOM shell).
- Mirror Slice 2 AIS bottle pattern for PIH.
- Shell/CSS/DOM only — wrap existing PIH comparison renderers.

## Files to read

- `relay/handoffs/20260625T051014Z_h4_autonomous_comparison_plan.md`
- `app_shell.html` (compare route, existing AIS bottle from Slice 2)
- `validation/mockups/beta/comparison_v5_beta.html`

## Files expected to change

- `app_shell.html`
- `scripts/smoke_h4_slice3_pih_shell.py` (new static smoke)

## Required behavior

1. Port mockup `#pih` collapsible block chrome around existing `renderPihComparisonHtml` output.
2. Reuse shared `cmp-block` CSS from Slice 2; do not rewrite PIH data logic.
3. Hydrate bottle body and keep legacy PIH section working (dual-mount like AIS).
4. Wire collapse toggle synced with `collapsed_sections.pih` if present.
5. One slice only: implement → smoke → commit → stop. Do not start Slice 4.

## Hard stops

- Do not touch Profile, Relocated, Map, Settings, Auth, backend, APIs, hydration.
- Do not change AIS bottle except shared block CSS.
- On smoke failure: `git reset --hard e37bf9d` and STOP with NOT VERIFIED closeout.

## Validation plan

```bash
python3 scripts/smoke_h4_slice3_pih_shell.py
python3 scripts/smoke_h4_slice2_ais_shell.py
python3 scripts/smoke_h4b_comparison_authority.py
python3 scripts/smoke_comparison_a2a_matrix.py
```

## Rollback plan

```bash
git reset --hard checkpoint/h4b_start_clean
```

## Commit (when VERIFIED)

```
comparison: add PIH bottled block shell (H4 slice 3)
```

## Closeout required

Write `results/73_h4_slice3_pih_shell.md` with files changed, smoke exit codes, rollback command, VERIFIED or NOT VERIFIED.
