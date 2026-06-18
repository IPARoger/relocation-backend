# Roadmap Index

**Last updated:** 2026-06-18  
**Authority:** See **ROADMAP AUTHORITY RULES** below. This index is the discovery entry point for all workstreams.

---

## ROADMAP AUTHORITY RULES

* Multiple ACTIVE roadmaps are allowed.
* Each ACTIVE roadmap must belong to a clearly named workstream.
* Only one ACTIVE roadmap may exist per workstream.
* The most recent roadmap for a workstream is authoritative.
* Never overwrite roadmap files.
* Create a new dated roadmap instead.

### Naming convention

`<ROADMAP_NAME>__<STATUS>__<YYYY-MM-DD>.md`

Examples:

- `WEB2_COMPLETION__ACTIVE__2026-06-18.md`
- `WEB2_COMPLETION__COMPLETED__2026-06-25.md`
- `RELAY_AUTOMATION__ACTIVE__2026-06-18.md`
- `WEB3_FOUNDATION__DRAFT__2026-07-01.md`

### Roadmap lifecycle

| Folder | Purpose |
|--------|---------|
| `active/` | Current authoritative roadmaps (one per workstream) |
| `completed/` | Immutable historical snapshots |

Completed roadmaps are immutable historical snapshots. When a workstream finishes, copy or promote the final version to `completed/` with `COMPLETED` status and a new date — do not edit the archived file.


## Active Roadmaps

| Roadmap | File | Status | Date |
| Comparison UX | `active/COMPARISON_UX__ACTIVE__2026-06-18.md` | ACTIVE | 2026-06-18 |
|---------|------|--------|------|
| Web2 Completion | [`active/WEB2_COMPLETION__ACTIVE__2026-06-18.md`](active/WEB2_COMPLETION__ACTIVE__2026-06-18.md) | ACTIVE | 2026-06-18 |

**Planner binding:** `relay/ROADMAP_QUEUE.md` and `relay/CHAT_INSTRUCTIONS.md` remain the execution queue for relay tasks. This index is the durable roadmap registry.

---

## Completed Roadmaps

| Roadmap | File / Reference | Completed |
|---------|------------------|-----------|
| Backend Ownership Migration (Chat 1) | `relay/ROADMAP_QUEUE.md` § Chat 1; closeouts in `results/` | 2026-06-18 |
| Legacy Write Retirement (Chat 2) | `relay/ROADMAP_QUEUE.md` § Chat 2; `results/57_c2_7_*` | 2026-06-18 |
| Read Path Consolidation Audit (Chat 3) | `relay/ROADMAP_QUEUE.md` § Chat 3; `results/59_c3_1_*`, `results/60_c3_2_*` | 2026-06-18 |
| Read Path Simplification (Chat 4) | `relay/ROADMAP_QUEUE.md` § Chat 4; `results/75_c4_1_*` … `results/67_c4_7_*` | 2026-06-18 |
| Dead Code Retirement & Cleanup (Chat 5) | `relay/ROADMAP_QUEUE.md` § Chat 5; `results/82_chat5_closure_audit.md` | 2026-06-18 |

Completed roadmap documents may be added to `completed/` as immutable snapshots. Existing closeouts in `results/` remain authoritative historical records until migrated.

---

## Superseded Roadmaps

| Roadmap | File | Superseded by | Notes |
|---------|------|---------------|-------|
| _(none yet)_ | — | — | Place superseded roadmaps in `superseded/` |

---

## Archive

Long-retired or exploratory roadmaps that are no longer referenced in planning live in `archive/`. Do not delete; preserve for archaeology.

---

## Governance Rules

* **Active roadmap per workstream is source of truth** for that workstream's direction.
* **Completed roadmaps are historical** — immutable once marked COMPLETED.
* **Superseded roadmaps are preserved** — never deleted; moved to `superseded/` with a successor reference.
* **New roadmap versions never overwrite old versions** — create a new dated file instead.
* **Name first, date second** — use `<ROADMAP_NAME>__<STATUS>__<YYYY-MM-DD>.md`.
* **Most recent roadmap per workstream is authoritative** — when two files in the same workstream conflict, the newer dated file wins.

### Folder layout

```
docs/roadmaps/
  ROADMAP_INDEX.md          ← this file
  active/                   ← current direction
  completed/                ← immutable completed snapshots
  superseded/               ← replaced but preserved
  archive/                  ← retired / exploratory
```

### Status values

| Status | Meaning |
|--------|---------|
| `ACTIVE` | Current authoritative roadmap |
| `COMPLETED` | Finished; do not edit — create successor if scope reopens |
| `DRAFT` | Proposed; not yet authoritative |
| `SUPERSEDED` | Replaced by a newer roadmap; preserved for history |

### Related governance

* Execution queue: `relay/ROADMAP_QUEUE.md`
* Planner discipline: `relay/CHAT_INSTRUCTIONS.md`
* Detailed sequence: `docs/architecture/ROADMAP_AND_SEQUENCE.md`
