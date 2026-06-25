# RESULT: 81_h4_slice6_ci_shell

**Roadmap ID:** H4-6
**Author:** Cursor (cloud executor)
**Commit:** `9530090`

## Files changed

- `app_shell.html` — collapsible City Intelligence shell (`renderComparisonCiSectionShellHtml`, beta-scoped `ci-section` CSS, `cmp-toggle-ci` collapse wired to workspace state, legacy workspace CI section hidden)
- `scripts/smoke_h4_slice6_ci_shell.py` — static DOM/CSS assertions for slice 6

## Exact changes

- `renderComparisonCiSectionShellHtml(ws, cs)` — mockup-aligned `ci-section` with collapse caret, per-city placeholder cards (`data-ci-wired="false"`), disabled “Open Full City Intelligence” stub
- `screenCompare()` — CI shell appended after bottled A2A block inside `comparison-main`
- `initComparisonWorkspace()` — `cmp-toggle-ci` persists `collapsed_sections.city_intelligence`
- `applyComparisonWorkspaceToDom()` — restores CI collapse from workspace state
- Legacy `rm-cmp-section[data-cmp-section="city_intelligence"]` hidden in beta compare (matches AIS/PIH/A2A pattern)

## Validation evidence

```text
python3 scripts/smoke_h4_slice6_ci_shell.py          PASS 16/16
python3 scripts/smoke_h4_slice5_notes_rail.py          PASS 15/15
python3 scripts/smoke_h4b_comparison_authority.py    PASS 14/14
```

Slice 6 smoke chains slice 5, slice 4, authority, and A2A matrix regressions (all green).

## Rollback command

```bash
git reset --hard checkpoint/h4b_start_clean
# or: git reset --hard e37bf9d
```

## Rejected scope

CI content engine / backend wiring, city intelligence API calls, Profile/Relocated/Map/Settings/backend, renderer/math/overlay changes, freeze audit (slice 7).

## Telegram

`relay_notify verified` skipped — `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` not configured in this environment.

**VERIFIED**
