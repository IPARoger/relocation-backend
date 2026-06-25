# RESULT: 81_h4_slice6_ci_shell

**Roadmap ID:** H4-6
**Author:** Cursor (local completion)
**Status:** VERIFIED

## Files changed

- `app_shell.html` — CI bottled shell (`renderComparisonCiBlockShellHtml`, `renderComparisonCiWorkbookSectionBody`, `refreshComparisonCiSection`); beta hide for workspace `city_intelligence`; collapse toggle synced with workspace state
- `scripts/smoke_h4_slice6_ci_shell.py` — static DOM/CSS assertions for slice 6

## Exact changes

- `renderComparisonCiBlockShellHtml(ws)` — collapsible `.cmp-block-ci.ci-section` with `data-cmp-ci-wired="false"`
- `screenCompare()` — CI bottle appended after A2A in `comparison-main`
- Dual hydrate: `refreshComparisonCiSection` targets `#rm-cmp-bottle-ci-body` and `#rm-cmp-sec-city_intelligence`
- `initComparisonWorkspace` / `applyComparisonWorkspaceToDom` — `cmp-toggle-bottle-ci` handler

## Validation evidence

```text
python3 scripts/smoke_h4_slice6_ci_shell.py          PASS 14/14 (+ regressions)
python3 scripts/smoke_h4_slice5_notes_rail.py        PASS
python3 scripts/smoke_h4b_comparison_authority.py    PASS
python3 scripts/smoke_comparison_a2a_matrix.py       10/10 passed
```

## Rollback command

```bash
git reset --hard e37bf9d
```
