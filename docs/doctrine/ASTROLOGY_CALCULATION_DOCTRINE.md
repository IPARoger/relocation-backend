# ASTROLOGY CALCULATION DOCTRINE

**Status:** Canonical calculation doctrine (permanent anchor)  
**Date:** 2026-06-20  
**Type:** Layer-1 chart-fact rules — no implementation authorized by this document alone  
**Supersedes:** Informal "late in house = next house" assumptions where they conflict with direction-aware rules below

---

## Purpose

Define how **Layer-1 chart facts** derived from ephemeris and chart calculation behave in the product: retrograde notation, applying/separating display, and direction-aware house-edge reassignment.

This document is the **canonical doctrine-tree anchor** for motion and direction rules. Implementation tickets and slice closeouts may live under `results/`; developers should start here.

**Full capture (EDGE-DOCTRINE-0):** `results/130_edge_motion_applying_separating_doctrine.md`

**Layer boundary:** Motion facts here are **Layer-1** (chart truth). They must not be folded into **Layer-2** ontology (dignities, interpretive hints, scoring). See `docs/constitutional/CORE_CONCEPTS_AND_LAYERS.md`.

---

## Motion & Direction Doctrine

### Retrograde

- Retrograde status is a **Layer-1 chart fact**, not Layer-2 ontology.
- Display: **`R`** marker adjacent to retrograde planets in chart and table contexts (wheels, PIH, relocated tables).
- Factual notation only — not judgment, scoring, or dignity.
- **Default setting (future):** show retrograde markers **ON**.

### Applying / Separating

- Applying and separating state is a **Layer-1 aspect fact** — belongs to A2A / aspect display, not ontology.
- **Applying = blue.** **Separating = red.**
- v1: no strength gradient by orb closeness, no scoring, no ranking.
- Users may disable A/S coloring for neutral tables.
- **Default setting (future):** A/S coloring **ON** (with neutral option).

### Direction-aware house-edge

House-edge reassignment must be **direction-aware**. Do not blindly treat all late-house placements as subsequent-house placements.

| Motion | Position near boundary | May assign to |
|--------|------------------------|---------------|
| **Direct** | Near **end** of house | **Subsequent** house, within configured orb |
| **Retrograde** | Near **beginning** of house | **Previous** house, within configured orb |

- Edge reassignment applies on the **leading edge of travel** (direct → forward exit; retrograde → backward entry).
- **Default orb:** 2°.
- **Default setting (future):** direction-aware house-edge rule **ON**.

Settings copy currently framed as "late sign / subsequent house" must align with this doctrine when implemented (`house_proximity_orb_degrees`, `subsequent_house_policy`).

### Station edge case

If a planet is near a house boundary but **about to station** before crossing that boundary, do **not** automatically assign it to the adjacent house.

**Unresolved (implementation):**

| Approach | Summary |
|----------|---------|
| Current motion only | Instantaneous speed/direction; no forward projection |
| Short-window ephemeris projection | Verify actual boundary crossing before reassignment |

**Conservative default:** do **not** project unless explicitly implemented and tested. When station ambiguity exists near a cusp, do not auto-assign adjacent house solely because position is within orb.

---

## Settings & help (future)

Astrology settings (not Appearance) should eventually expose:

- Show retrograde markers (default ON)
- Direction-aware house-edge rule (default ON)
- House-edge orb (default 2°)
- Show applying/separating coloring (default ON; neutral option)

Help copy should explain: direction-aware house edge, conservative station handling, factual (non-scoring) A/S coloring, and Layer-1 vs Layer-2 separation.

---

## Acceptance criteria (implementation)

Future slices must satisfy:

- [ ] Retrograde planets marked `R` in chart/table contexts when enabled
- [ ] Direct late-house and retrograde early-house handled differently
- [ ] Station-near-cusp behavior documented before projection is added
- [ ] A/S: blue/red only; no intensity scoring in v1
- [ ] No Layer-2 contamination (dignities, hints, scoring modules)

---

## Related doctrine

| Document | Role |
|----------|------|
| `results/130_edge_motion_applying_separating_doctrine.md` | EDGE-DOCTRINE-0 full capture |
| `results/119_dignities_diffs_display_doctrine_v1.md` | Layer-2 dignity boundaries |
| `results/114_settings_doctrine_capture_v1.md` | Settings defaults and Astrology IA |
| `docs/design/RELOCATED_FACTS_PRESENTATION_DOCTRINE.md` | Relocated-facts surface coordination |
