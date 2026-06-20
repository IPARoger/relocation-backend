# PHILOSOPHY-0: Relocation Methodology & Philosophy Doctrine Capture

**Date:** 2026-06-20
**Slice:** PHILOSOPHY-0
**Status:** Complete — document only, no implementation

---

## Goal

Create the canonical philosophy document for the relocation application.

---

## What was created

### docs/doctrine/RELOCATION_METHODOLOGY_DOCTRINE.md

A canonical doctrine file covering 11 numbered sections:

| # | Section |
|---|---------|
| 1 | Humility Doctrine — app does not know what is best for you |
| 2 | Tradeoff Doctrine — every location is a tradeoff; show the full picture |
| 3 | Interactive Exploration Doctrine — research through iteration, not report generation |
| 4 | Building Structure vs Silverware Doctrine — geometry first, refinement tools later |
| 5 | No Finger on the Scale Doctrine — no implied valence in colors, labels, or AI outputs |
| 6 | Professional Freedom Doctrine — full configurability of orbs, house system, zodiac, dignities, A/S coloring |
| 7 | Geometry vs Ontology Separation (Layer 1 vs Layer 2) |
| 8 | AI Assistance Doctrine — Astro Assist explains and surfaces; does not rank or decide |
| 9 | City Intelligence Doctrine — practical context is separate, never blended into astrological scores |
| 10 | Methodology / Help / Video Implications — language patterns, tutorial principles |
| 11 | Orb & Calculation Defaults Doctrine — why defaults exist and how they may be overridden |

### Section 11 specifically captures

Per the user note about orb/retrograde/A/S philosophy:

- **Orb defaults**: chart display orb vs A2A/search orb are separate and configurable. Defaults are practical, not doctrinal.
- **Retrograde defaults**: ON by default; direction-aware house-edge ON by default; station cases conservative by default. All overridable.
- **Applying/separating coloring**: blue/red directional fact only; no intensity gradient (would imply scoring); coloring can be disabled.
- These are explicitly framed as practical defaults that give **maximum flexibility to experienced astrologers** to configure according to their practice.

### docs/doctrine/README.md

Updated to add `RELOCATION_METHODOLOGY_DOCTRINE.md` to the doctrine index table, and linked `results/137_help_course_onboarding_doctrine_map.md` in Related section.

---

## Files changed

| File | Change |
|------|--------|
| `docs/doctrine/RELOCATION_METHODOLOGY_DOCTRINE.md` | Created (new canonical doctrine, 11 sections) |
| `docs/doctrine/README.md` | Updated: added new doctrine to index |

---

## Audience / usage

- **Help / Methodology pages**: reference §1–§9 for explanation page copy
- **Tutorial / video content**: use §10 language patterns
- **Engineering**: reference before implementing any feature that could imply scoring, ranking, or valence
- **Astro Assist behavioral constraints**: §8 is the binding constraint
- **Settings configurability**: §6 and §11 define what must remain configurable

---

## Non-goals

- No implementation
- No app_shell.html changes
- No backend changes
- No Help page UI (future slice)
