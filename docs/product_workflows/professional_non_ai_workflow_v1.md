# Professional Non-AI Workflow v1

## Status

**CANONICAL** for Phase 3 strategic product architecture.

This document defines the **professional MVP workflow** without AI dependency. It consolidates product training, roadmap, and constitutional workflow doctrine into one inspectable workflow spec.

**This is not implementation.** Code, API contracts, and UI shells must trace to this document; this document does not mandate ship dates.

**Reads with:** `docs/constitutional/professional_mode_vs_lay_mode_strategy.md`, `docs/product_training/professional_workflow_and_explanatory_language.md`, `docs/relocation_app_product_roadmap.md` §8–9, `docs/constitutional/layer_sovereignty_and_forbidden_crossings.md`.

---

## Purpose

Define how a **professional astrologer or informed relocation explorer** uses the instrument when:

- the map is the primary experience,
- overlays are the decision object,
- AI is **absent or explicitly off**,
- and trust depends on inspectable geometry, not interpretation theater.

The workflow must remain **fully usable** without Astro Assist, scoring engines, or conversational intake.

---

## Core workflow principle

**Browse, do not oracle.**

The product helps professionals:

1. declare conditions,
2. discover geographic overlap,
3. inspect point truth,
4. compare constrained options,
5. save and share work.

It does **not** default to:

- one “best city,”
- benefic/malefic scoring,
- hidden optimization,
- or narrative closure.

---

## Actor model

| Actor | Role |
|-------|------|
| **Professional account** | Owns clients, settings, saved work, export permissions. |
| **Client** | One natal chart per client record; subject of relocation exploration. |
| **Investigation** | A saved semantic search session (conditions + viewport + chart context). |
| **Place** | A named or coordinate-defined location with stable identity when possible. |

**MVP constraint:** one natal chart per client. Relocated charts are **place + natal profile**, not separate natal identities.

---

## Primary workflow loop

```text
Account home → select client → client dashboard → map exploration
     ↓                                              ↓
Settings / orbs (Layer 2)                    Condition search + overlays
     ↓                                              ↓
Export / share ← compare / favorites ← point inspect + full chart
```

### Step 1 — Establish client context

On **client dashboard / home**:

- confirm birth data record (date, time, place, timezone integrity),
- surface birth-time confidence tier if known (see `docs/future/birth_time_uncertainty_and_confidence_doctrine.md`),
- show recent investigations, favorite cities, and comparison drafts.

**Non-goals:** tutorial tours, astrology emoji chrome, dashboard widgets that compete with map entry.

### Step 2 — Declare investigation conditions

Professional selects **semantic conditions** (Layer 1 truth requests):

- planet in house,
- angle in sign,
- aspect to angle,
- explicit **NOT / exclusion** conditions.

Each condition is a **track**, not a form section label. Future UI uses flexible **Add condition** rows; current A/B/C blocks are **legacy scaffold only**.

**Layer 2 settings** (orbs, visible minors, helper layers, ontology packs) apply **before or during** search but must **never alter Layer 1 membership**.

### Step 3 — Search and read overlap

User runs search. Map shows:

- categorical regions (house, angle-sign),
- exact aspect centerlines,
- overlap zones where multiple truths coincide.

**Overlap is often the answer.** Multi-condition intersection is the primary discovery object.

Controls must support **mute / solo / NOT** without forcing single-variable mode (see `docs/ui/map_drawer_and_layer_control_doctrine.md`).

### Step 4 — Inspect point truth

At a candidate location:

- **right-click** (desktop) or future long-press equivalent → **popup = canonical point truth**,
- optional **full relocated chart** for dense inspection (account/chart surface).

Popup wins over overlay impression. Aura and cusp softness are **non-certifying**.

### Step 5 — Save favorites and investigations

- **Favorite city:** stable place reference + optional notes; not a renderer snapshot.
- **Saved investigation:** birth profile + semantic conditions + viewport context; **not** GeoJSON/canvas/renderer artifacts.

### Step 6 — Compare and decide

Comparison workspace supports:

- multiple cities for **one** chart,
- side-by-side tables on account surfaces (dense allowed off-map),
- explicit tradeoff language — no paternalistic “winner.”

### Step 7 — Export / share with client

Export tiers:

| Tier | Use | Authority |
|------|-----|-----------|
| **Exploration** | Map screenshot, annotated viewport | Illustrative; popup truth still required for claims |
| **Client-authoritative** | Structured chart + location record + stated conditions | Suitable for professional handoff; must cite data source and confidence |

**MVP export scope:** PNG/viewport capture before PDF/report systems.

Sharing must preserve **semantic replay** (conditions + chart + viewport), not merely a pretty image.

---

## Layer separation in workflow

| Layer | Workflow ownership | Examples |
|-------|-------------------|----------|
| **Layer 1 — Geometry / truth** | Search conditions, popup truth, membership | house placement, angle sign, exact aspect geometry |
| **Layer 2 — Interpretive ontology** | Settings, orbs, helper layers, ontology packs | minor aspect visibility, dignity helpers, Astro Assist (future) |
| **Layer 3 — Intentionality** | Client goals, comparison framing (future AI) | “avoid isolation,” “career visibility” — not MVP-hard |
| **Layer 4 — Optimization** | Explicit constrained ranking only | college shortlist compare — deferred |

**Forbidden:** letting Layer 2 settings silently change Layer 1 results; letting export copy imply Layer 3 certainty.

---

## Mute / solo / NOT workflow semantics

| Control | Behavior | User intent |
|---------|----------|-------------|
| **Mute** | Hide layer visually; condition remains in investigation | Declutter dense overlap |
| **Solo** | Temporarily isolate one layer; restore restores all | Inspect one boundary set |
| **NOT / exclusion** | Show deprioritized regions with calm veil semantics | Explicit dealbreakers |
| **Send to background / foreground** | Adjust visual priority without astrological ranking | Dissect overlap stack |

**Professional rule:** the system may **highlight** structure; it must not **block** inspection of ambiguity when the user understands the tradeoff.

---

## Account surfaces vs map surface

| Surface | Job | Density |
|---------|-----|---------|
| **Map** | Explore geography-as-astrology; overlays + popup | Sparse, contemplative |
| **Client dashboard** | Orient, resume work, manage favorites | Calm list/cards |
| **Chart / comparison pages** | Full tables, aspects, relocation record | Dense allowed |
| **Settings** | Layer 2 ontology and display prefs | Restrained forms |

Account and intake screens **establish premium tone**; they are not “admin afterthoughts.” Map drawer controls **inherit** that language later — drawer is deferred until hierarchy is proven (`docs/ux_principles_and_emotional_tone.md` §6).

---

## Explicit non-goals (MVP)

- AI intake, AI scoring, AI oracle closure
- Rain / virga / emergence animation as product behavior
- Travel mode, GPS notifications
- Social features, referral marketplace
- Deterministic “best city” without declared constraints
- Planet-to-planet relocation search (domain-invalid)

---

## Workflow risks (documented)

| Risk | Mitigation |
|------|------------|
| Saved view without condition capture | Persist semantic investigation, not viewport-only deep links |
| Local JSON becomes product DB | Explicit storage boundary in data model doc; migration plan before accounts |
| Half-migrated flexible conditions UI | Coordinate API + UI; do not ship UI-only A/B/C removal |
| Export overclaims certainty | Tier exports; birth-time confidence on client records |
| Professional mode hidden behind AI | Non-AI path remains default-capable |

---

## Validation method (when implemented)

Each workflow slice must prove:

1. **Scope** — which steps touched
2. **Evidence** — manual script or fixture replay
3. **Rollback** — feature flag or revert list
4. **Files changed** — exact list
5. **Layer check** — no Layer 2 → Layer 1 contamination

---

## Source consolidation

| Topic | Prior art |
|-------|-----------|
| Professional steps 1–12 | `docs/product_training/professional_workflow_and_explanatory_language.md` |
| Saved object taxonomy | `docs/relocation_app_product_roadmap.md` §8 |
| Non-AI professional mode | `docs/constitutional/mvp_beta_and_future_feature_roadmap.md` Stage 2 |
| Overlap as answer | `memory_archaeology_raw/consolidated_notes/foundational_product_truths.md` |
| Export / compare | `docs/process/decision_and_uncertainty_framework.md` |

---

## Revision

Revise when account/client MVP ships, when flexible condition rows land, or when export/share ACL is defined. AI workflow additions require a **new document version**, not silent edits to this non-AI contract.
