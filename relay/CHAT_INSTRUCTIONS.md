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

- Chat 1–4: **COMPLETE**
- Chat 5: **COMPLETE** — closure audit `results/82_chat5_closure_audit.md`; final slice `3bb5905` (C5-6)
- Cleanup track: **CLOSED** — no remaining required cleanup slices
- **Product track: CURRENT** — settings, UX, city search, port 8000, etc.

Do not reopen C5-2 or C5-3 without a new approved roadmap specification (both blocked by live callers).

## Closeout format

Every task produces `results/<number>_<roadmap_id>_<slug>.md` with:

1. What changed (files + line areas)
2. Caller / grep evidence
3. Smoke results
4. **VERIFIED** or **NOT VERIFIED**
