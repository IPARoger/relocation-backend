# EDGE-DOCTRINE-0: Retrograde, House Edge, Applying/Separating Doctrine

**Status:** Authoritative product doctrine (capture only)  
**Date:** 2026-06-20  
**Type:** Motion / edge-case doctrine — no implementation authorized by this document  
**Ticket:** EDGE-DOCTRINE-0 (capture)

---

## Purpose

Capture authoritative doctrine for **Layer-1 chart motion facts** and **direction-aware house-edge logic**, and their separation from **Layer-2 interpretive ontology** (dignities, interpretive hints, scoring systems).

This document does **not** authorize changes to `app_shell.html`, backend services, or persisted settings beyond recording future intent.

**Canonical anchor:** `docs/doctrine/ASTROLOGY_CALCULATION_DOCTRINE.md`

**Related doctrine:**

- `results/114_settings_doctrine_capture_v1.md` — Subsequent House Rule toggle + orb (currently framed as late-in-house; this document refines direction-aware behavior)
- `results/119_dignities_diffs_display_doctrine_v1.md` — Layer-2 dignity ontology boundaries
- `results/128_settings2d_astrology_reorder.md` — Astrology settings section order

---

## Layer model (boundary)

| Layer | Examples | Nature |
|-------|----------|--------|
| **Layer-1** | Retrograde status, applying/separating, house placement, motion direction, station state | **Chart fact** — derived from ephemeris / chart calculation |
| **Layer-2** | Dignities, interpretive hints, mutual reception, scoring, ranking | **Ontology / interpretation** — data-driven or subjective overlays |

**Engineering rule:** Layer-1 motion facts must not be folded into Layer-2 ontology modules. Display may combine them on the same surface, but calculation, settings keys, and help copy must keep the boundary explicit.

---

## 1. Retrograde status

### Classification

Retrograde status is a **Layer-1 chart fact**, not Layer-2 ontology.

It is determined from ephemeris motion at chart time (or equivalent chart-engine output). It is **not** a dignity, hint, score, or interpretive label.

### Display doctrine

- Retrograde planets should eventually display an **`R`** marker adjacent to the planet in **chart and table contexts** (wheels, PIH tables, relocated chart tables, and comparable tabular chart surfaces).
- The marker is **factual notation**, not a judgment or ranking.
- Marker visibility should be user-configurable (see §5); default **ON**.

### Non-goals

- Do not encode retrograde meaning in dignity presets or interpretive-hints copy.
- Do not use retrograde status to auto-tint, score, or rank locations or aspects in v1.

---

## 2. House-edge / late-in-house logic (direction-aware)

### Problem

A naive rule — *"late in sign / late in house ⇒ treat as subsequent house"* — is **incorrect for retrograde motion**. House-edge reassignment must be **direction-aware**.

### Rules (doctrine)

**Direct planet near the end of a house**

- May be considered as occupying the **subsequent house**, within the configured house-edge orb.

**Retrograde planet near the beginning of a house**

- May be considered as occupying the **previous house**, within the configured house-edge orb.

**General principle**

- Do **not** blindly treat all late-house placements as subsequent-house placements.
- Edge reassignment applies on the **leading edge of travel** (direct: forward toward house exit; retrograde: backward toward house entry).

### Relation to current settings copy

Settings currently expose *"Treat late sign placements as subsequent house"* with an orb control (`house_proximity_orb_degrees`, `subsequent_house_policy`). Future implementation must align UI copy and engine behavior with this direction-aware doctrine — not merely rename the toggle.

### Default orb

**2°** (consistent with `results/114_settings_doctrine_capture_v1.md`).

---

## 3. Station edge case

### Problem

If a planet is near a house boundary but **about to station** before crossing that boundary, the system must not automatically assume it reaches the adjacent house.

Stationary or near-stationary bodies may linger near a cusp without completing a house crossing within any reasonable display window.

### Unresolved implementation question

| Approach | Description |
|----------|-------------|
| **A. Current motion only** | Use instantaneous speed / direction at chart time; apply direction-aware edge rule without forward projection. |
| **B. Short-window ephemeris projection** | Project motion over a bounded time window to verify whether the body actually crosses the house boundary before station or direction change. |

### Default conservative choice (doctrine)

**Do not project unless explicitly implemented and tested.**

Until projection is designed, validated against ephemeris edge cases, and covered by acceptance tests:

- Prefer **current-motion / conservative** handling.
- When station ambiguity exists near a cusp, **do not** auto-assign to the adjacent house solely because apparent position is within orb of the boundary.
- Document ambiguous cases in implementation notes before enabling projection.

---

## 4. Applying / Separating (A/S)

### Classification

Applying and separating state is a **Layer-1 aspect fact**.

A/S belongs to **A2A / aspect display logic**, not Layer-2 ontology. It describes whether an aspect is tightening or loosening at chart time — not interpretive quality, dignity, or user-facing "advice."

### Display doctrine (v1)

| State | Color |
|-------|-------|
| **Applying** | Blue |
| **Separating** | Red |

### v1 constraints

- **No strength gradient** by closeness of orb.
- **No scoring.**
- **No ranking.**
- Color encodes motion direction only — not "good/bad," "strong/weak," or interpretive weight.

### Surfaces

A/S coloring applies where aspect relationships are shown in chart/A2A contexts — not on map search overlays, favorites, or Layer-2 dignity cells unless explicitly scoped in a future amendment.

---

## 5. Settings implications (future)

These controls belong under **Astrology** (calculation / display defaults), not Appearance (visual styling shells).

| Setting | Default (doctrine) | Notes |
|---------|-------------------|-------|
| Show retrograde markers | **ON** | `R` beside retrograde planets in chart/table contexts |
| Direction-aware house-edge rule | **ON** | Enables §2 logic; OFF reverts to strict cusp placement |
| House-edge orb | **2°** | Shared orb for direct-late → subsequent and retrograde-early → previous |
| Show applying/separating coloring | **ON** (or configurable) | Blue / red per §4 |
| Disable A/S coloring | User option | Neutral tables for users who want motion facts without color |

### Persistence note

Existing keys (`house_proximity_orb_degrees`, `subsequent_house_policy`) may require **semantic refinement** when direction-aware logic is implemented. This document does not authorize schema changes — only records intended behavior.

New keys (e.g. retrograde markers, A/S coloring toggles) require explicit schema design before stub-save.

---

## 6. Documentation / Help implications

Settings (or linked help) should eventually include a short **doctrine / explanation** page covering:

1. **Why house-edge logic is direction-aware** — direct and retrograde motion assign adjacent houses on opposite physical edges; a single "late = next house" rule misstates retrograde charts.
2. **Why station cases are conservative** — without verified projection, the app must not assume a body crosses a cusp it may never reach.
3. **Why A/S coloring is factual, not scoring** — blue/red indicate tightening vs loosening, not quality or recommendation.
4. **Why Layer-1 motion facts stay separate from Layer-2 systems** — dignities and interpretive hints are optional interpretive overlays; retrograde, house-edge reassignment, and A/S are chart-derived facts.

Help copy must not conflate Layer-1 markers with Layer-2 dignity or hint language.

---

## 7. Acceptance criteria (future implementation)

Implementation slices referencing this doctrine should not ship until:

- [ ] **Retrograde markers** — Retrograde planets visibly marked (`R`) in chart/table contexts when the setting is ON.
- [ ] **Direction-aware house edge** — Direct late-house and retrograde early-house cases handled **differently** per §2; no blanket late ⇒ subsequent rule.
- [ ] **Station edge cases documented** — Before automated projection is added, station-near-cusp behavior is specified in implementation notes and covered by targeted tests.
- [ ] **Conservative default for projection** — No short-window ephemeris projection in production until explicitly implemented and tested (§3).
- [ ] **A/S display simplicity** — Applying = blue, separating = red; **no** intensity gradient, scoring, or ranking in v1.
- [ ] **No Layer-2 contamination** — Retrograde, house-edge, and A/S logic remain outside dignity ontology, interpretive hints, and scoring modules.

---

## Explicit non-goals (this capture)

- Implementing retrograde markers, direction-aware house-edge engine changes, or A/S coloring
- Ephemeris projection design or station-detection algorithms
- Settings UI wiring or new persistence keys
- Help page / in-app copy authoring
- Map overlay or search behavior for A/S or retrograde
- Amending PIH dignity display (see `results/119_dignities_diffs_display_doctrine_v1.md`)

---

## Summary

| Topic | Layer | v1 display | Default setting |
|-------|-------|------------|-----------------|
| Retrograde | Layer-1 fact | `R` marker | ON |
| House edge | Layer-1 fact | Direction-aware reassignment within orb | ON, 2° |
| Station near cusp | Layer-1 edge case | Conservative; no auto-adjacent-house without projection | No projection until tested |
| Applying / Separating | Layer-1 fact | Blue / red; no gradient | ON (with neutral option) |
