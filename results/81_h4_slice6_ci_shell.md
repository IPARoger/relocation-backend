# RESULT: 81_h4_slice6_ci_shell

**Roadmap ID:** H4-6
**Author:** Cursor (cloud executor)

## Files changed

- `app_shell.html` — City Intelligence collapsible shell (`renderComparisonCiSectionShellHtml`, beta-scoped `.ci-section` CSS, collapse sync with workspace `city_intelligence`, legacy workspace section hidden in beta)
- `scripts/smoke_h4_slice6_ci_shell.py` — static DOM/CSS assertions for slice 6

## Exact changes

- `renderComparisonCiSectionShellHtml(ws)` — mockup-style `ci-section` with collapse caret, `City Intelligence` title, placeholder body (`data-cmp-ci-wired="false"`)
- `screenCompare()` — CI shell appended after A2A bottled block inside `comparison-main`
- `initComparisonWorkspace()` — `cmp-toggle-ci-section` collapse handler synced to workspace state and legacy section
- `applyComparisonWorkspaceToDom()` / `collectComparisonWorkspaceFromDom()` — CI collapse state round-trip
- Beta CSS hides `rm-cmp-section[data-cmp-section="city_intelligence"]` (workspace bookmark panel)

## Validation evidence

```text
python3 scripts/smoke_h4_slice6_ci_shell.py          PASS 14/14
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

CI content engine / backend wiring, Profile/Relocated/Map/Settings/backend changes, renderer/math/overlay changes, freeze audit (slice 7).

## Telegram

`relay_notify verified` skipped — `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` not configured in this environment.

**VERIFIED**
