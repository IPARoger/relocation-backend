# Planner / executor discipline (binding)

Paste project-specific rules above this line if needed. The relay robot sends this file on every planning call.

---

## Core workflow

1. **Audit → plan → implement → validate → commit** — one roadmap slice at a time.
2. **One objective per task.** One commit per verified slice when possible.
3. **Roadmap ID required** in every task header (`**Roadmap ID:** C?_?` or `T?_?`).
4. **No roadmap jumping.** Finish open items in queue order unless user explicitly reprioritizes.

## Before delete or quarantine

1. **Grep production callers** in `*.js`, `*.html`, `*.py` (exclude `results/`, `tasks/`, `smoke_*`).
2. **Grep ownership smokes** — smokes must not depend on routes you are retiring.
3. If any active caller found → **PAUSE**, report route + caller. Do not delete.

## Implementation limits

- **Small boring wins.** Targeted reads only; no full-file reads unless task explicitly allows.
- **No megacommits.** No vendor dumps, geojson bulk, relay handoff spam, or unrelated files in one commit.
- **Honest commit messages.** Message must match the diff (`feat` = product code, `quarantine` = 410, `audit` = read-only, `cleanup` = dead code removal).
- **No hidden frontend writes.** Browser must not `.insert()` / `.update()` / `.delete()` on owned tables.
- **No service-role write paths** for product data the UI owns.

## Validation gates

- Run smokes named in the task before claiming VERIFIED.
- Record exit codes and pass counts in `results/<task>_*.md`.
- **VERIFIED** only if acceptance criteria met; **NOT VERIFIED** if hard stop triggered.
- Smoke failure → revert product changes, report. Do not commit broken product code.

## Hard stops (always)

- Active production caller on a route you plan to quarantine or delete.
- JWT ownership route touched without explicit task scope.
- Renderer / overlay / aura math (map_CURRENT.html production substrate) — document only, do not remove.
- `LEGACY_SEARCH_REGIONS` and `buildPlanFromLegacyDom()` are **LIVE** — not dead code.
- `_deprecated_legacy_write` has 24 callers — do not delete without removing all shims.

## Current roadmap state (sync with ROADMAP_QUEUE.md)

- Chat 1–3: **COMPLETE**
- Chat 4: **PARTIAL** — C4-1 and C4-2 M2 **OPEN**; C4-2 M5, C4-3..C4-7 **COMPLETE**
- Chat 5: **PAUSED** until Chat 4 debt closed

## Closeout format

Every task produces `results/<number>_<roadmap_id>_<slug>.md` with:

1. What changed (files + line areas)
2. Caller / grep evidence
3. Smoke results
4. **VERIFIED** or **NOT VERIFIED**
