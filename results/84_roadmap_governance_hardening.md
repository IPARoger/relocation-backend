# Roadmap Governance Hardening Closeout

**Roadmap ID:** Roadmap Governance Hardening  
**Date:** 2026-06-18  
**Mode:** Governance only — no product, backend, or UI changes

---

## Files Changed

| File | Change |
|------|--------|
| `docs/roadmaps/ROADMAP_INDEX.md` | Added **ROADMAP AUTHORITY RULES** — parallel workstreams, per-workstream authority, naming convention, lifecycle |
| `relay/ROADMAP_QUEUE.md` | Added **ROADMAP GOVERNANCE** section with index pointer and anti-patterns |
| `relay/CHAT_INSTRUCTIONS.md` | Added **Before creating a roadmap** checklist (5 steps) |

---

## Doctrine Added

### Workstream authority
- Multiple ACTIVE roadmaps allowed (one per workstream)
- Most recent roadmap per workstream is authoritative
- Never overwrite; create new dated files

### Naming convention
`<ROADMAP_NAME>__<STATUS>__<YYYY-MM-DD>.md`

### Lifecycle
- `docs/roadmaps/active/` — current
- `docs/roadmaps/completed/` — immutable snapshots

### Forbidden patterns
`roadmap_v2.md`, `roadmap_new.md`, `final.md`, `roadmap-final-final.md`, etc.

---

## Validation Output

```
grep -rn "Only one ACTIVE roadmap may exist per workstream" docs/roadmaps relay
```

```
docs/roadmaps/ROADMAP_INDEX.md:12:* Only one ACTIVE roadmap may exist per workstream.
relay/ROADMAP_QUEUE.md:12:* Only one ACTIVE roadmap may exist per workstream.
```

```
grep -rn '<ROADMAP_NAME>__<STATUS>__<YYYY-MM-DD>.md' docs/roadmaps relay
```

```
docs/roadmaps/ROADMAP_INDEX.md:19:`<ROADMAP_NAME>__<STATUS>__<YYYY-MM-DD>.md`
docs/roadmaps/ROADMAP_INDEX.md:82:* **Name first, date second** — use `<ROADMAP_NAME>__<STATUS>__<YYYY-MM-DD>.md`.
relay/CHAT_INSTRUCTIONS.md:12:3. Follow naming convention exactly: `<ROADMAP_NAME>__<STATUS>__<YYYY-MM-DD>.md`
relay/ROADMAP_QUEUE.md:15:* Use naming convention: `<ROADMAP_NAME>__<STATUS>__<YYYY-MM-DD>.md`
```

Doctrine confirmed in:
- [x] `docs/roadmaps/ROADMAP_INDEX.md`
- [x] `relay/ROADMAP_QUEUE.md`
- [x] `relay/CHAT_INSTRUCTIONS.md`

---

## Final Verdict

**VERIFIED** — roadmap authority, naming, and lifecycle doctrine is now binding in index, relay queue, and chat instructions. Parallel workstreams supported; per-workstream singularity enforced.
