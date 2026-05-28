# Birth Time Uncertainty and Confidence Doctrine

## Status

**CANONICAL** for Phase 3 strategic product architecture.

Defines **epistemic tiers**, **user-facing honesty**, **data recording**, and **engine behavior boundaries** for uncertain birth times. Not implementation. Not rectification software spec.

**Reads with:** `docs/constitutional/conversational_discovery_and_intentionality.md` (Birth Data Integrity), `docs/process/decision_and_uncertainty_framework.md`, `docs/relocation_app_product_roadmap.md` §8, `docs/data_model/local_first_data_objects_v1.md`, `validation/narratives/post_truth_grid_staged_asc_backlog.md`.

---

## Purpose

Birth time uncertainty is **product-critical** for relocation work:

- houses and angles move rapidly with time,
- false precision destroys professional trust,
- lay users often know approximate times only,
- AI intake may help later — **MVP must handle tiers without AI**.

---

## Core principle

**Honest uncertainty beats fabricated exactness.**

The system must:

- record what is known,
- surface confidence tier everywhere downstream,
- warn when precision is assumed,
- never silently treat a guess as exact.

---

## Confidence tiers

| Tier | Definition | Example intake |
|------|------------|----------------|
| **T0 — Exact** | Documented precise time, professional source | “7:42 AM, birth certificate” |
| **T1 — Narrow range** | Bounded interval ≤ ~30 min | “between 7:00 and 7:30 AM” |
| **T2 — Wide range** | Bounded interval > 30 min, same day | “early morning” |
| **T3 — Unknown time** | Date known, time unknown | “time unknown” → solar chart policy |
| **T4 — Rectification in progress** | professional working estimate | flagged provisional |

Tiers are **product epistemology**, not astrology doctrine. Engine behavior must map explicitly per tier.

---

## User-facing copy principles

### Do

- explain **why time matters** for houses/angles without hostility,
- offer examples of valid approximate intake,
- show active tier on client dashboard and exports,
- use calm professional language.

### Do not

- shame uncertain users,
- collapse tiers into silent exact time,
- imply rectification certainty without source,
- use oracle language (“the chart demands 7:15 AM”).

**Example good copy:**

> “House and angle placements depend on birth time. If your time is approximate, we'll show results for your stated range and flag where the chart may shift.”

**Example bad copy:**

> “Enter your exact birth time for accurate results.” *(when user already said they don't know)*

---

## Engine behavior matrix (MVP boundaries)

| Tier | Houses / angles | Map overlays | Popup at point | Comparison |
|------|-----------------|--------------|----------------|------------|
| **T0** | full compute | standard | authoritative | standard |
| **T1** | compute at bounds + midpoint default for search | standard with **confidence badge** | show range sensitivity note if cusp-near | flag rows near cusp |
| **T2** | search may use representative time + **warning** | same + stronger warning | warn on angle/house instability | disclaimer on exports |
| **T3** | solar chart / noon policy **explicitly documented** | limited house reliability — warn | popup cites solar policy | comparisons qualified |
| **T4** | provisional time flagged | watermark “provisional” | source note | export requires acknowledgment |

**MVP implementation scope:** record tier + warnings + UI badges. **Do not** implement multi-domain ambiguity rendering or animated uncertainty fields yet.

---

## Data recording

On `BirthProfile`:

```text
confidenceTier: T0 | T1 | T2 | T3 | T4
timeSource: certificate | parent_report | rectification | unknown
timeRangeStart?: ISO
timeRangeEnd?: ISO
representativeTime?: ISO  // explicit, never implicit
solarChartPolicy?: enum   // when T3
notes?: string
```

**Forbidden:**

- storing rounded guess as exact without `representativeTime` flag,
- omitting tier on saved investigations,
- exporting T2/T3 work without confidence watermark.

---

## Natural language intake (future AI — not MVP)

Later conversational intake may parse:

- “early morning,”
- “around sunrise,”
- “between 7 and 7:30,”
- “sometime in the evening.”

Parser must **map to tier + range**, not invent precision.

AI layer is **Layer 3 assist** — must not bypass recorded tier or fabricate T0.

---

## Timezone and DST (P3 product-critical)

Documented in validation backlog — not optional forever:

- historical timezone correctness,
- DST edge cases,
- place vs timezone table mismatches,
- warning when timezone inference low confidence.

**MVP:** use best-available timezone with visible assumption; log for audit.

---

## Cache and scheduler implications (future)

From roadmap Phase 2.5:

- pre-map idle may warm likely scopes,
- cache must tolerate **multiple candidate chart domains** when tier > T0,
- overlap-confidence rendering is **future** — schema may reserve `candidateChartDomains[]` without UI.

**Do not** implement ambiguity overlays that masquerade as confirmed truth (`docs/constitutional/runtime_and_renderer_sovereignty.md`).

---

## Rectification workflow (out of MVP scope)

Professional rectification may produce T4 provisional times.

Product may later:

- version rectification history,
- require explicit promotion to T0,
- never overwrite certificate time without audit trail.

Not MVP — document boundary only.

---

## Export and professional handoff

Client-authoritative exports must include:

- `confidenceTier`,
- time source,
- representative time policy if used,
- explicit solar chart note if T3,
- disclaimer block for range tiers.

Exploration-tier screenshots inherit badge if visible on screen.

---

## Validation fixtures

Maintain edge-case birth times:

- cusp-crossing within T1 range,
- DST transition days,
- high-latitude ASC instability,
- T3 solar chart policy spot checks.

Compare popup vs overlay — tier warnings must not contradict point truth.

---

## Explicit non-goals (this phase)

- animated uncertainty fields (rain/virga/emergence),
- automatic rectification,
- AI guessing birth time silently,
- rendering multiple simultaneous house sets on map without user opt-in,
- false precision in marketing copy.

---

## Missing abstractions

1. **`CuspProximityFlag`** at popup — near house boundary under range tier
2. **`ChartDomainCandidate`** — { time, label, weight } for cache
3. **Timezone confidence** field on birth place resolution
4. **Export disclaimer template** per tier

---

## Source consolidation

| Topic | Prior art |
|-------|-----------|
| Birth data integrity | `docs/constitutional/conversational_discovery_and_intentionality.md` |
| Uncertainty framework | `docs/process/decision_and_uncertainty_framework.md` |
| Roadmap uncertain time | `docs/relocation_app_product_roadmap.md` §8 |
| P3 backlog | `validation/narratives/post_truth_grid_staged_asc_backlog.md` |
| Archaeology chat_06 | `memory_archaeology_raw/pending_imports/chat_06_memory_and_workflow_infrastructure.md` |

---

## Revision

Revise when MVP intake ships, when solar chart policy is coded, or when multi-domain cache schema is activated. Any change to tier definitions requires migration note on existing client records.
