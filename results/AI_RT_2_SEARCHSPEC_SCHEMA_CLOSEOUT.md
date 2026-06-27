# AI-RT-2 — SearchSpec Schema Closeout

**Date:** 2026-06-27  
**Task:** AI-RT-2 — Overlay-First SearchSpec Schema  

---

## Deliverable

| Artifact | Path | Status |
|----------|------|--------|
| SearchSpec canonical schema | `docs/canon/SEARCHSPEC_SCHEMA.md` | Created |
| Closeout report | `results/AI_RT_2_SEARCHSPEC_SCHEMA_CLOSEOUT.md` | This file |

---

## What was defined

`SEARCHSPEC_SCHEMA.md` establishes SearchSpec as the **overlay-first contract** between Navigator/Astro Assist and Engine.

### Schema sections (§3)

- §3.1 Spec identity / version
- §3.2 Manifest pinning
- §3.3 Source surface / context
- §3.4 Desired conditions
- §3.5 Avoids / exclusions / NOT conditions
- §3.6 Soft preferences
- §3.7 Geographic bounds
- §3.8 Birth-time uncertainty / range support
- §3.9 Branch variants
- §3.10 Tradeoff scan fields
- §3.11 Optimization / carving fields
- §3.12 Recalculate more
- §3.13 Genie / map / saved search handoff (overlay first)
- §3.14 City helper mode (explicit only)
- §3.15 User confirmation state
- §3.16 Audit / transparency notes

### Hard rules

- Engine default output: overlay branches, viable geographic regions, map configurations, shareable overlay sets
- Cities enter only after user pin/select, saved comparison, explicit selected-place query, City Intelligence, or explicit `city_helper_mode`
- Astro Assist: same schema; shareable overlay configurations by default

### Prohibitions (§5)

City ranking, city lists as default, raw user-facing scores, hidden optimization, in-place modification of confirmed specs.

---

## Acceptance

| Criterion | Met |
|-----------|-----|
| No doc implies city ranking/listing is default output | Yes |
| SearchSpec explicitly overlay-first | Yes |
| Genie/Map handoff overlays first | Yes |
| City Intelligence downstream of user-selected places | Yes |
| Astro Assist overlay-first by default | Yes |

---

## Follow-up (optional)

- Point `AI_RUNTIME_ARCHITECTURE.md` §2.6 at `SEARCHSPEC_SCHEMA.md`
- Correct `INTENT_TRANSLATION_ENGINE.md` §0 "candidate cities" in a separate pass
