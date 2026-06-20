# Relocation App — Methodology & Philosophy Doctrine

**Version:** 1.0
**Date:** 2026-06-20
**Status:** Canonical — future Help, tutorials, onboarding, Astro Assist behavior, and videos reference this document
**See also:** `docs/doctrine/ASTROLOGY_CALCULATION_DOCTRINE.md` for calculation-layer specifics

---

## Purpose

This document captures the core philosophy of the relocation research application. It explains the principles behind product decisions, default settings, and feature scope. It is intended to be referenced by:

- Help / Methodology pages
- Tutorial and course content
- Onboarding walkthrough copy
- Astro Assist behavioral constraints
- Engineering when evaluating feature requests that could compromise these principles

---

## 1. Humility Doctrine

**The app does not know what is best for you.**

Relocation decisions involve values, relationships, finances, career, health, family, and personal history — none of which the app can access or weigh. Even if astrology were a perfect predictive system (which is debated), the translation of chart patterns into life outcomes would still require the researcher's judgment about what they are optimizing for.

The app presents **astrological geometry and contextual data as facts**. It does not score locations, produce rankings, or recommend cities.

Any feature, copy, or AI behavior that implies "this city is better for you" violates this doctrine.

---

## 2. Tradeoff Doctrine

**Every location is a tradeoff.**

No location on Earth is uniformly favorable across all planetary conditions for a given chart. Even in a region where multiple desired conditions overlap, other conditions will be compromised. The researcher's task is to understand the tradeoffs and decide which combination best serves their current intentions.

Implications:

- The app should show the full picture, not just the favorable parts.
- Exclusion overlays (Mute / Not) are as important as inclusion overlays.
- Comparison tables show all conditions, not a filtered-to-favorable subset.
- Help content should consistently use tradeoff language, not optimization language.

---

## 3. Interactive Exploration Doctrine

**Research happens through interaction, not consumption.**

The app is a research environment, not a report generator. A user who sits back and receives a PDF is not using the app as intended. The intended flow is:

1. Form an intention.
2. Translate it into conditions.
3. Explore the map.
4. Notice intersections and gaps.
5. Refine.
6. Repeat.

This is iterative. It is exploratory. It cannot be compressed into a single output.

Implications:

- Features that try to "summarize everything" undermine the research process.
- Onboarding should teach the map controls, not generate a report.
- Astro Assist explains and surfaces — it does not produce a final answer.

---

## 4. Building Structure vs Silverware Doctrine

**Teach structure first; silverware (refinement tools) later.**

The map overlay geometry is the structural layer. A2A tables, Diffs, PIH tables, Dignities, and City Intelligence are refinement tools — silverware. They are useful only after the structural layer is understood.

Onboarding teaches the structural layer. Advanced courses teach the silverware.

This doctrine governs course sequencing:

- Beginners start with AIS (familiar reading format) → map (geometry) → tables.
- Advanced users go directly to Genie / map → A2A → Diffs → Dignities.
- Silverware is never hidden, but it is not the entry point.

---

## 5. No Finger on the Scale Doctrine

**The app must not influence the researcher's conclusion.**

The product presents geometry and context. It does not:

- Weight planetary conditions by "importance" in any universal sense.
- Apply any traditional hierarchy of planets without the user's explicit configuration.
- Give any condition a built-in positive or negative valence.
- Use language in the UI that implies any condition is inherently good or bad.

Default colors, layouts, and naming must be chosen to minimize implicit valence. The researcher assigns meaning.

This doctrine applies to:

- Overlay colors (no red = bad, green = good defaults).
- Genie variable labels (descriptive, not evaluative).
- Astro Assist summaries (must not say "favorable" or "unfavorable" without explicit researcher framing).
- Dignities display (shown as metadata, not as a scoring layer).

---

## 6. Professional Freedom Doctrine

**Experienced astrologers must be able to work according to their own system.**

The app's defaults are practical choices — not doctrinal assertions that one orb, house system, or dignity tradition is correct. Experienced astrologers have developed their own approaches through years of practice. The app must not impose its defaults on them.

This doctrine requires:

- **Full orb configurability** for chart display, A2A, and aspect-to-angle search — separately.
- **House system selection** (Placidus, Whole Sign, Koch, etc.).
- **Zodiac selection** (tropical, sidereal, etc.).
- **Dignity system selection** (optional display layer, never forced).
- **Applying/separating coloring** that can be disabled.
- **Direction-aware house-edge toggle** (ON by default but overridable).
- **Retrograde markers** that can be shown or hidden.

The defaults are chosen to be safe and informative for most researchers. The configuration surface allows experienced practitioners to override every significant default.

---

## 7. Geometry vs Ontology Separation (Layer 1 vs Layer 2)

**Chart facts are not interpretations.**

The application separates two distinct layers:

### Layer 1 — Geometric chart facts

Calculated from ephemeris positions, local horizon, and meridian. These are not subject to tradition, opinion, or school of thought:

- Planetary positions (zodiac degrees, house positions)
- Aspects (angular relationships, applying/separating direction)
- Retrograde status (current motion direction)
- House-edge placements (direction-aware; see `ASTROLOGY_CALCULATION_DOCTRINE.md`)
- Local angle relationships (ASC, MC, DSC, IC at a given location)

Layer 1 facts are the foundation of the map overlays, A2A tables, and chart display.

### Layer 2 — Interpretive ontology

Metadata sourced from one or more astrological traditions. These are not universal facts — they are a chosen lens:

- Traditional dignities (domicile, exaltation, detriment, fall)
- Modern dignity expansions
- Essential/accidental dignity combined scores
- Interpretive hints and keywords
- Rulership assignments
- Mutual reception

Layer 2 metadata is **optional display** in the PIH table. It is never used as input to the overlay search engine or as a scoring mechanism.

### Why this matters

Mixing Layer 1 and Layer 2 would mean the map geometry is influenced by a specific interpretive tradition — producing a map that is not a neutral geometric tool but an interpretation in disguise. This violates the No Finger on the Scale doctrine.

---

## 8. AI Assistance Doctrine

**Astro Assist explains and surfaces. It does not decide.**

The role of AI assistance in the app:

| Permitted | Not permitted |
|-----------|--------------|
| Explain what a condition means in plain language | Recommend a city |
| Summarize the pattern visible in a selected region | Score or rank locations |
| Surface conditions the user may not have noticed | Assert a condition is "good" or "bad" |
| Help translate intentions into candidate Genie variables | Replace the researcher's judgment |
| Clarify methodology questions | Generate a "final answer" |

Astro Assist is an aid. The researcher holds the judgment function.

This applies to all AI surfaces in the product, including:
- Inline chart explanations
- Map region summaries
- AIS text generation
- Future conversational interfaces

Any AI output that produces a ranking or recommendation must be flagged as non-compliant with this doctrine.

---

## 9. City Intelligence Doctrine

**Practical context complements astrological analysis. It does not score against it.**

City Intelligence surfaces non-astrological data: cost of living, climate, demographics, walkability, employment, safety, healthcare, and similar contextual factors.

Principles:

- City Intelligence data is **presented separately** from astrological data — never blended into a combined score.
- No "combined astrology + practicality score" exists. Such a score would require the system to weight two incommensurable value systems.
- The researcher integrates the two layers using their own judgment about what trade-offs matter.
- City Intelligence is labeled as a **practical context layer**, not an astrological analysis.
- Data sources are disclosed when available.

---

## 10. Methodology / Help / Video Implications

### Help / Methodology section

The Help surface must include a **Methodology & Doctrine** section, separate from the feature tutorials. Topics (each 300–600 words):

1. No scoring / no "best city" — the humility doctrine in plain language
2. Layer 1 vs Layer 2 — geometry vs interpretation
3. Dignities as optional metadata — why they are not a scoring layer
4. Orb configuration rationale — why defaults exist and how to override them
5. Retrograde, house-edge, and applying/separating philosophy
6. Why A/S is blue/red only — no intensity gradient
7. Station cases are conservative — why the app does not project
8. Why City Intelligence is separate — the non-mixing rule
9. Why AI assistance explains, not decides

### Tutorial content

Tutorials must reference this document's doctrines when explaining why the app works the way it does. Copy that implies scoring, ranking, or universal "good/bad" valence must be revised before shipping.

### Video implications

Future product videos should use language consistent with the Humility Doctrine, Tradeoff Doctrine, and No Finger on the Scale Doctrine. Suggested language patterns:

- "See where [condition] is strong" (not "find the best city for [condition]")
- "Explore the overlap" (not "find your ideal location")
- "These are the chart facts here" (not "this city is favorable")
- "You decide what the pattern means" (not "this indicates X")

---

## 11. Orb & Calculation Defaults Doctrine

**Defaults are practical choices, not doctrinal assertions.**

Every configurable calculation parameter in the app has a default. These defaults were chosen to be informative and safe for most researchers. They are not claims about which value is cosmically correct.

### Orb defaults

The app maintains separate orbs for:

1. **Chart display** — visual representation of aspects in the natal chart table and PIH. Default: 8° for major aspects, smaller for minors. Practical choice: wide enough to be informative, narrow enough to avoid false connections.
2. **A2A / aspect-to-angle search** — the orb used when searching for locations where a planet is within orb of a local angle. Default: tighter than chart display (typically 2–3°). Rationale: angle contacts tighten as the location is refined; a tighter search orb surfaces meaningful candidates without flooding the map.

Neither default implies a universal truth about orb boundaries. Experienced astrologers routinely work with different orbs. The configuration surface allows full override.

### Retrograde defaults

Retrograde status is shown by default (Layer-1 fact). The directional marker is factual, not evaluative.

Direction-aware house-edge logic is ON by default. A direct planet near the end of a house may be considered in the subsequent house; a retrograde planet near the beginning of a house may be considered in the prior house. This is a practical default; it can be disabled.

Station edge cases are handled conservatively: the app uses current motion, not ephemeris projection, to determine house boundary proximity. This prevents false precision.

Full technical specification: `docs/doctrine/ASTROLOGY_CALCULATION_DOCTRINE.md`.

### Applying/Separating coloring defaults

Applying aspects are shown in blue; separating in red. This is a directional fact display, not a valence assignment.

No intensity gradient: the gradient would imply that a tighter applying aspect is "more important" than a wider one — an interpretive judgment the app does not make. The researcher decides how much weight to give orb proximity.

Coloring can be disabled for researchers who prefer neutral tables.

---

## Related doctrine documents

| Document | Scope |
|----------|-------|
| `docs/doctrine/ASTROLOGY_CALCULATION_DOCTRINE.md` | Layer-1 calculation specifics: retrograde, A/S, house-edge, station |
| `results/130_edge_motion_applying_separating_doctrine.md` | Detailed capture of motion doctrine |
| `results/137_help_course_onboarding_doctrine_map.md` | Help structure, course outlines, walkthrough doctrine |

